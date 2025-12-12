import logging
from typing import Optional

from fastapi import APIRouter
from pydantic import BaseModel

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/trade", tags=["trade"])


class PlanRequest(BaseModel):
    ticker: str
    entry: float
    stop: float
    target: Optional[float] = None
    account_size: float = 10000
    risk_percent: float = 1.0


class PlanResponse(BaseModel):
    ticker: str
    entry: float
    stop: float
    target: float
    risk_amount: float
    position_size: int
    position_value: float
    risk_reward: float


@router.post("/plan")
async def create_trade_plan(req: PlanRequest):
    risk_per_share = abs(req.entry - req.stop)
    risk_amount = req.account_size * (req.risk_percent / 100)
    position_size = int(risk_amount / risk_per_share) if risk_per_share > 0 else 0
    position_value = position_size * req.entry

    target = req.target if req.target else req.entry + (risk_per_share * 2)
    reward_per_share = abs(target - req.entry)
    risk_reward = reward_per_share / risk_per_share if risk_per_share > 0 else 0

    logger.info(f"📋 Trade plan: {req.ticker} - {position_size} shares @ ${req.entry}")

    return PlanResponse(
        ticker=req.ticker,
        entry=req.entry,
        stop=req.stop,
        target=target,
        risk_amount=round(risk_amount, 2),
        position_size=position_size,
        position_value=round(position_value, 2),
        risk_reward=round(risk_reward, 2),
    )
