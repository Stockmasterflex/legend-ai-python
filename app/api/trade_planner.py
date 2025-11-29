"""
Trade planner API - Position sizing and risk management
"""
import logging
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, field_validator
from typing import Optional, List, Dict, Any
from datetime import datetime

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/trade", tags=["trade_planner"])

class TradePlanRequest(BaseModel):
    ticker: str
    pattern: Optional[str] = None
    entry: float
    stop: float
    target: float
    account_size: float
    risk_percent: float = 1.0  # Default 1% risk
    
    @field_validator("ticker")
    @classmethod
    def uppercase_ticker(cls, v: str) -> str:
        return v.upper().strip()
    
    @field_validator("risk_percent")
    @classmethod
    def validate_risk_percent(cls, v: float) -> float:
        if v <= 0 or v > 5.0:
            raise ValueError("risk_percent must be between 0 and 5.0")
        return v
    
    @field_validator("entry", "stop", "target")
    @classmethod
    def validate_prices(cls, v: float) -> float:
        if v <= 0:
            raise ValueError("Prices must be positive")
        return v

class PartialExit(BaseModel):
    shares: int
    price: float
    r_multiple: float
    percentage: float

class TradePlanResponse(BaseModel):
    ticker: str
    pattern: Optional[str]
    entry: float
    stop: float
    target: float
    position_size: int
    dollar_amount: float
    risk_amount: float
    potential_profit: float
    r_multiple: float
    risk_per_share: float
    concentration_pct: float
    partial_exits: List[PartialExit]
    warnings: List[str]

def calculate_position_size(
    entry: float,
    stop: float,
    account_size: float,
    risk_percent: float
) -> tuple[int, float, float]:
    """
    Calculate position size based on risk management rules
    
    Returns:
        (position_size, dollar_amount, risk_amount)
    """
    # Risk per share
    risk_per_share = abs(entry - stop)
    
    # Maximum risk amount (1% of account)
    max_risk = account_size * (risk_percent / 100.0)
    
    # Position size = risk amount / risk per share
    position_size = int(max_risk / risk_per_share)
    
    # Dollar amount invested
    dollar_amount = position_size * entry
    
    # Actual risk amount
    risk_amount = position_size * risk_per_share
    
    return position_size, dollar_amount, risk_amount

def calculate_partial_exits(
    entry: float,
    stop: float,
    target: float,
    position_size: int
) -> List[PartialExit]:
    """
    Calculate suggested partial exit levels at 1R, 2R, 3R
    
    Strategy:
    - 1R (50% of position): Lock in initial risk
    - 2R (30% of position): Capture swing target
    - 3R (20% of position): Let winners run
    """
    risk_per_share = abs(entry - stop)
    
    # Calculate R-multiple prices
    price_1r = entry + (1.0 * risk_per_share)
    price_2r = entry + (2.0 * risk_per_share)
    price_3r = entry + (3.0 * risk_per_share)
    
    # Distribute shares across exits
    shares_1r = int(position_size * 0.50)  # 50% at 1R
    shares_2r = int(position_size * 0.30)  # 30% at 2R
    shares_3r = position_size - shares_1r - shares_2r  # Remainder at 3R
    
    return [
        PartialExit(
            shares=shares_1r,
            price=round(price_1r, 2),
            r_multiple=1.0,
            percentage=50.0
        ),
        PartialExit(
            shares=shares_2r,
            price=round(price_2r, 2),
            r_multiple=2.0,
            percentage=30.0
        ),
        PartialExit(
            shares=shares_3r,
            price=round(price_3r, 2),
            r_multiple=3.0,
            percentage=20.0
        ),
    ]

@router.post("/plan", response_model=TradePlanResponse)
async def plan_trade(request: TradePlanRequest):
    """
    Calculate position size and trade plan based on risk management rules
    
    **Risk Management Rules:**
    - Maximum 1-2% account risk per trade
    - Position size must be < 20% of account (concentration limit)
    - Stop loss required for every trade
    
    **Returns:**
    - Position size (shares)
    - Dollar amount invested
    - Risk amount
    - R:R ratio
    - Partial exit levels (1R, 2R, 3R)
    """
    try:
        # Validate entry/stop/target relationship
        if request.entry <= request.stop:
            raise HTTPException(
                status_code=400,
                detail="Entry must be above stop for long positions"
            )
        
        if request.target <= request.entry:
            raise HTTPException(
                status_code=400,
                detail="Target must be above entry for long positions"
            )
        
        # Calculate position size
        position_size, dollar_amount, risk_amount = calculate_position_size(
            request.entry,
            request.stop,
            request.account_size,
            request.risk_percent
        )
        
        # Calculate potential profit
        profit_per_share = request.target - request.entry
        potential_profit = position_size * profit_per_share
        
        # Calculate R:R ratio
        risk_per_share = request.entry - request.stop
        reward_per_share = request.target - request.entry
        r_multiple = reward_per_share / risk_per_share if risk_per_share > 0 else 0
        
        # Calculate concentration percentage
        concentration_pct = (dollar_amount / request.account_size) * 100
        
        # Calculate partial exits
        partial_exits = calculate_partial_exits(
            request.entry,
            request.stop,
            request.target,
            position_size
        )
        
        # Generate warnings
        warnings = []
        
        if concentration_pct > 20:
            warnings.append(
                f"⚠️ Position size ({concentration_pct:.1f}%) exceeds 20% concentration limit. "
                f"Consider reducing risk or using a higher-priced stock."
            )
        
        if r_multiple < 2.0:
            warnings.append(
                f"⚠️ R:R ratio ({r_multiple:.1f}:1) is below 2:1 minimum. "
                f"Consider wider target or tighter stop."
            )
        
        if position_size < 10:
            warnings.append(
                f"⚠️ Position size ({position_size} shares) is very small. "
                f"Consider increasing risk % or using a lower-priced stock."
            )
        
        logger.info(
            f"Trade plan calculated for {request.ticker}: "
            f"{position_size} shares @ ${request.entry:.2f}, "
            f"R:R {r_multiple:.1f}:1"
        )
        
        return TradePlanResponse(
            ticker=request.ticker,
            pattern=request.pattern,
            entry=request.entry,
            stop=request.stop,
            target=request.target,
            position_size=position_size,
            dollar_amount=round(dollar_amount, 2),
            risk_amount=round(risk_amount, 2),
            potential_profit=round(potential_profit, 2),
            r_multiple=round(r_multiple, 2),
            risk_per_share=round(risk_per_share, 2),
            concentration_pct=round(concentration_pct, 2),
            partial_exits=partial_exits,
            warnings=warnings
        )
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Trade planning error: {e}")
        raise HTTPException(status_code=500, detail="Trade planning failed")

@router.post("/quick-size")
async def quick_position_size(
    entry: float,
    stop: float,
    account_size: float,
    risk_percent: float = 1.0
):
    """Quick position size calculator without full trade plan"""
    try:
        position_size, dollar_amount, risk_amount = calculate_position_size(
            entry, stop, account_size, risk_percent
        )
        
        return {
            "position_size": position_size,
            "dollar_amount": round(dollar_amount, 2),
            "risk_amount": round(risk_amount, 2),
            "risk_per_share": round(abs(entry - stop), 2)
        }
    except Exception as e:
        logger.error(f"Quick size calculation error: {e}")
        raise HTTPException(status_code=500, detail="Calculation failed")

