"""
Data models for Legend AI SDK
"""

from typing import Optional, Dict, Any, List
from dataclasses import dataclass
from datetime import datetime


@dataclass
class PatternResult:
    """Result from pattern detection"""
    pattern: str
    score: float
    entry: float
    stop: float
    target: float
    risk_reward_ratio: float
    chart_url: Optional[str] = None
    rs_rating: Optional[int] = None
    criteria_met: Optional[Dict[str, Any]] = None
    cached: bool = False
    processing_time: Optional[float] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PatternResult":
        """Create PatternResult from API response"""
        result_data = data.get("data", {})
        return cls(
            pattern=result_data.get("pattern", ""),
            score=result_data.get("score", 0.0),
            entry=result_data.get("entry", 0.0),
            stop=result_data.get("stop", 0.0),
            target=result_data.get("target", 0.0),
            risk_reward_ratio=result_data.get("risk_reward_ratio", 0.0),
            chart_url=result_data.get("chart_url"),
            rs_rating=result_data.get("rs_rating"),
            criteria_met=result_data.get("criteria_met"),
            cached=data.get("cached", False),
            processing_time=data.get("processing_time"),
        )


@dataclass
class ChartResult:
    """Result from chart generation"""
    chart_url: str
    cached: bool = False
    processing_time: Optional[float] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ChartResult":
        """Create ChartResult from API response"""
        return cls(
            chart_url=data.get("chart_url", ""),
            cached=data.get("cached", False),
            processing_time=data.get("processing_time"),
        )


@dataclass
class ScanResult:
    """Result from universe scan"""
    ticker: str
    pattern: str
    score: float
    entry: float
    stop: float
    target: float
    chart_url: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ScanResult":
        """Create ScanResult from dict"""
        return cls(
            ticker=data.get("ticker", ""),
            pattern=data.get("pattern", ""),
            score=data.get("score", 0.0),
            entry=data.get("entry", 0.0),
            stop=data.get("stop", 0.0),
            target=data.get("target", 0.0),
            chart_url=data.get("chart_url"),
        )


@dataclass
class WatchlistItem:
    """Watchlist item"""
    id: int
    ticker: str
    status: str
    target_entry: Optional[float] = None
    target_stop: Optional[float] = None
    reason: Optional[str] = None
    added_at: Optional[datetime] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "WatchlistItem":
        """Create WatchlistItem from dict"""
        added_at = None
        if data.get("added_at"):
            try:
                added_at = datetime.fromisoformat(data["added_at"].replace("Z", "+00:00"))
            except Exception:
                pass

        return cls(
            id=data.get("id", 0),
            ticker=data.get("ticker", ""),
            status=data.get("status", ""),
            target_entry=data.get("target_entry"),
            target_stop=data.get("target_stop"),
            reason=data.get("reason"),
            added_at=added_at,
        )


@dataclass
class PositionSize:
    """Position sizing calculation result"""
    position_size: int
    risk_amount: float
    kelly_criterion: Optional[float] = None
    breakeven: Optional[float] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PositionSize":
        """Create PositionSize from dict"""
        return cls(
            position_size=data.get("position_size", 0),
            risk_amount=data.get("risk_amount", 0.0),
            kelly_criterion=data.get("kelly_criterion"),
            breakeven=data.get("breakeven"),
        )


@dataclass
class Trade:
    """Trade record"""
    id: int
    ticker: str
    entry_price: float
    stop_loss: float
    target_price: Optional[float] = None
    position_size: Optional[int] = None
    risk_amount: Optional[float] = None
    created_at: Optional[datetime] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Trade":
        """Create Trade from dict"""
        created_at = None
        if data.get("created_at"):
            try:
                created_at = datetime.fromisoformat(data["created_at"].replace("Z", "+00:00"))
            except Exception:
                pass

        return cls(
            id=data.get("id", 0),
            ticker=data.get("ticker", ""),
            entry_price=data.get("entry_price", 0.0),
            stop_loss=data.get("stop_loss", 0.0),
            target_price=data.get("target_price"),
            position_size=data.get("position_size"),
            risk_amount=data.get("risk_amount"),
            created_at=created_at,
        )


@dataclass
class AIResponse:
    """AI chat/analysis response"""
    response: str
    conversation_id: Optional[str] = None
    processing_time: Optional[float] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AIResponse":
        """Create AIResponse from dict"""
        return cls(
            response=data.get("response", ""),
            conversation_id=data.get("conversation_id"),
            processing_time=data.get("processing_time"),
        )
