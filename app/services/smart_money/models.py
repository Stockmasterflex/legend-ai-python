"""
Smart Money Data Models
"""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List, Dict, Any
from enum import Enum


class TradeType(str, Enum):
    """Trade type classification"""
    SWEEP = "sweep"
    BLOCK = "block"
    SPLIT = "split"
    DARK_POOL = "dark_pool"
    REGULAR = "regular"


class Sentiment(str, Enum):
    """Trade sentiment"""
    BULLISH = "bullish"
    BEARISH = "bearish"
    NEUTRAL = "neutral"


class DarkPoolPrint(BaseModel):
    """Dark pool transaction print"""
    symbol: str
    timestamp: datetime
    price: float
    size: int = Field(description="Number of shares")
    value: float = Field(description="Dollar value of trade")
    exchange: str = Field(default="DARK_POOL")
    premium_discount: float = Field(
        description="Percentage premium/discount to market price"
    )
    market_price: float = Field(description="Market price at time of print")
    is_premium: bool = Field(description="Whether trade was at premium")
    sentiment: Sentiment

    class Config:
        json_schema_extra = {
            "example": {
                "symbol": "AAPL",
                "timestamp": "2025-11-18T10:30:00",
                "price": 178.50,
                "size": 500000,
                "value": 89250000.0,
                "exchange": "DARK_POOL",
                "premium_discount": 0.5,
                "market_price": 178.00,
                "is_premium": True,
                "sentiment": "bullish"
            }
        }


class InstitutionalHolder(BaseModel):
    """Institutional holder information"""
    name: str
    shares: int
    value: float
    percentage: float = Field(description="Percentage of total shares")
    change: float = Field(description="Change in shares from last filing")
    change_percentage: float
    filing_date: datetime
    is_new_position: bool = Field(default=False)
    is_sold_out: bool = Field(default=False)

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Vanguard Group Inc",
                "shares": 1250000000,
                "value": 222500000000.0,
                "percentage": 8.5,
                "change": 5000000,
                "change_percentage": 0.4,
                "filing_date": "2025-11-15T00:00:00",
                "is_new_position": False,
                "is_sold_out": False
            }
        }


class InsiderTransaction(BaseModel):
    """Insider transaction record"""
    symbol: str
    insider_name: str
    title: str
    transaction_type: str = Field(description="Buy, Sell, Option Exercise, etc.")
    shares: int
    price: float
    value: float
    filing_date: datetime
    transaction_date: datetime
    ownership_type: str = Field(description="Direct or Indirect")
    shares_owned_after: int

    class Config:
        json_schema_extra = {
            "example": {
                "symbol": "AAPL",
                "insider_name": "Tim Cook",
                "title": "CEO",
                "transaction_type": "Sell",
                "shares": 100000,
                "price": 178.50,
                "value": 17850000.0,
                "filing_date": "2025-11-17T00:00:00",
                "transaction_date": "2025-11-15T00:00:00",
                "ownership_type": "Direct",
                "shares_owned_after": 3000000
            }
        }


class BlockTrade(BaseModel):
    """Block trade alert"""
    symbol: str
    timestamp: datetime
    trade_type: TradeType
    price: float
    size: int
    value: float
    is_options: bool = Field(default=False)
    strike: Optional[float] = None
    expiration: Optional[datetime] = None
    call_put: Optional[str] = None
    sentiment: Sentiment
    premium: Optional[float] = Field(
        None, description="Options premium for options trades"
    )
    open_interest_change: Optional[int] = None
    volume_ratio: float = Field(description="Volume to average volume ratio")

    class Config:
        json_schema_extra = {
            "example": {
                "symbol": "AAPL",
                "timestamp": "2025-11-18T10:30:00",
                "trade_type": "sweep",
                "price": 178.50,
                "size": 250000,
                "value": 44625000.0,
                "is_options": False,
                "sentiment": "bullish",
                "volume_ratio": 3.5
            }
        }


class OwnershipChange(BaseModel):
    """13F ownership change summary"""
    symbol: str
    quarter: str
    total_holders: int
    holders_increased: int
    holders_decreased: int
    holders_new: int
    holders_sold_out: int
    total_shares: int
    total_value: float
    institutional_ownership_percentage: float
    net_change_shares: int
    net_change_percentage: float

    class Config:
        json_schema_extra = {
            "example": {
                "symbol": "AAPL",
                "quarter": "Q3 2025",
                "total_holders": 5234,
                "holders_increased": 2100,
                "holders_decreased": 1800,
                "holders_new": 450,
                "holders_sold_out": 380,
                "total_shares": 15000000000,
                "total_value": 2670000000000.0,
                "institutional_ownership_percentage": 62.5,
                "net_change_shares": 150000000,
                "net_change_percentage": 1.0
            }
        }


class SmartMoneyFlow(BaseModel):
    """Aggregated smart money flow data"""
    symbol: str
    date: datetime
    dark_pool_volume: int
    dark_pool_value: float
    dark_pool_ratio: float = Field(
        description="Dark pool volume / total volume"
    )
    block_trades_count: int
    block_trades_value: float
    institutional_buying: float
    institutional_selling: float
    net_institutional_flow: float
    insider_buying: float
    insider_selling: float
    net_insider_flow: float
    smart_money_confidence: float = Field(
        ge=0, le=100, description="Smart money confidence score 0-100"
    )
    accumulation_distribution: str = Field(
        description="accumulation, distribution, or neutral"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "symbol": "AAPL",
                "date": "2025-11-18T00:00:00",
                "dark_pool_volume": 5000000,
                "dark_pool_value": 892500000.0,
                "dark_pool_ratio": 0.35,
                "block_trades_count": 45,
                "block_trades_value": 1250000000.0,
                "institutional_buying": 500000000.0,
                "institutional_selling": 250000000.0,
                "net_institutional_flow": 250000000.0,
                "insider_buying": 10000000.0,
                "insider_selling": 25000000.0,
                "net_insider_flow": -15000000.0,
                "smart_money_confidence": 72.5,
                "accumulation_distribution": "accumulation"
            }
        }


class SmartMoneyIndicators(BaseModel):
    """Smart money technical indicators"""
    symbol: str
    timestamp: datetime

    # Dark Pool Metrics
    dark_pool_ratio: float
    dark_pool_sentiment: Sentiment
    dark_pool_trend: str = Field(description="increasing, decreasing, stable")

    # Institutional Metrics
    institutional_ownership: float
    institutional_flow_5d: float
    institutional_flow_20d: float
    institutional_momentum: str

    # Block Trade Metrics
    block_trade_frequency: float = Field(description="Trades per day")
    block_trade_sentiment: Sentiment
    unusual_activity_score: float = Field(ge=0, le=100)

    # Combined Indicators
    smart_money_index: float = Field(
        ge=0, le=100, description="Overall smart money strength"
    )
    divergence_score: float = Field(
        description="Price vs smart money divergence"
    )
    accumulation_score: float = Field(ge=-100, le=100)

    class Config:
        json_schema_extra = {
            "example": {
                "symbol": "AAPL",
                "timestamp": "2025-11-18T10:30:00",
                "dark_pool_ratio": 0.35,
                "dark_pool_sentiment": "bullish",
                "dark_pool_trend": "increasing",
                "institutional_ownership": 62.5,
                "institutional_flow_5d": 250000000.0,
                "institutional_flow_20d": 750000000.0,
                "institutional_momentum": "strong_buying",
                "block_trade_frequency": 45.0,
                "block_trade_sentiment": "bullish",
                "unusual_activity_score": 78.5,
                "smart_money_index": 75.0,
                "divergence_score": 12.5,
                "accumulation_score": 65.0
            }
        }


class SmartMoneyAlert(BaseModel):
    """Smart money alert/signal"""
    symbol: str
    timestamp: datetime
    alert_type: str = Field(
        description="dark_pool_spike, institutional_buying, unusual_options, etc."
    )
    severity: str = Field(description="low, medium, high")
    title: str
    message: str
    data: Dict[str, Any] = Field(default_factory=dict)
    sentiment: Sentiment

    class Config:
        json_schema_extra = {
            "example": {
                "symbol": "AAPL",
                "timestamp": "2025-11-18T10:30:00",
                "alert_type": "dark_pool_spike",
                "severity": "high",
                "title": "Large Dark Pool Activity Detected",
                "message": "Dark pool volume 3x above average with 65% premium trades",
                "data": {
                    "dark_pool_volume": 5000000,
                    "average_volume": 1500000,
                    "premium_percentage": 65.0
                },
                "sentiment": "bullish"
            }
        }
