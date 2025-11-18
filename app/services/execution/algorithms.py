"""
Execution Algorithms
Implements TWAP, VWAP, Implementation Shortfall, and Percentage of Volume algorithms
"""

import logging
import random
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass
import numpy as np

logger = logging.getLogger(__name__)


@dataclass
class OrderSlice:
    """Represents a slice of a larger order"""
    quantity: int
    scheduled_time: datetime
    limit_price: Optional[float] = None
    is_iceberg: bool = False
    display_quantity: Optional[int] = None


@dataclass
class MarketData:
    """Market data snapshot"""
    price: float
    volume: int
    vwap: Optional[float] = None
    bid: Optional[float] = None
    ask: Optional[float] = None
    spread: Optional[float] = None


class ExecutionAlgorithm:
    """Base class for execution algorithms"""

    def __init__(
        self,
        ticker: str,
        side: str,
        total_quantity: int,
        duration_minutes: int,
        randomize_timing: bool = True,
        randomize_size: bool = True
    ):
        self.ticker = ticker
        self.side = side
        self.total_quantity = total_quantity
        self.duration_minutes = duration_minutes
        self.randomize_timing = randomize_timing
        self.randomize_size = randomize_size

    def _add_randomization(
        self,
        value: float,
        variance_pct: float = 10.0
    ) -> float:
        """Add random variance to a value"""
        variance = value * (variance_pct / 100.0)
        return value + random.uniform(-variance, variance)

    def _add_timing_jitter(
        self,
        scheduled_time: datetime,
        max_jitter_seconds: int = 30
    ) -> datetime:
        """Add random jitter to scheduled time"""
        if not self.randomize_timing:
            return scheduled_time

        jitter = random.randint(-max_jitter_seconds, max_jitter_seconds)
        return scheduled_time + timedelta(seconds=jitter)

    def generate_slices(self, market_data: Optional[MarketData] = None) -> List[OrderSlice]:
        """Generate order slices - to be implemented by subclasses"""
        raise NotImplementedError("Subclasses must implement generate_slices")


class TWAPAlgorithm(ExecutionAlgorithm):
    """
    Time-Weighted Average Price Algorithm
    Splits order into equal slices over time
    """

    def __init__(
        self,
        ticker: str,
        side: str,
        total_quantity: int,
        duration_minutes: int,
        num_slices: Optional[int] = None,
        randomize_timing: bool = True,
        randomize_size: bool = True
    ):
        super().__init__(ticker, side, total_quantity, duration_minutes, randomize_timing, randomize_size)

        # Default to one slice per 5 minutes, minimum 2 slices
        if num_slices is None:
            self.num_slices = max(2, duration_minutes // 5)
        else:
            self.num_slices = num_slices

    def generate_slices(self, market_data: Optional[MarketData] = None) -> List[OrderSlice]:
        """Generate time-weighted order slices"""

        base_quantity = self.total_quantity // self.num_slices
        remainder = self.total_quantity % self.num_slices

        interval_minutes = self.duration_minutes / self.num_slices
        start_time = datetime.now()

        slices = []

        for i in range(self.num_slices):
            # Calculate quantity for this slice
            quantity = base_quantity
            if i < remainder:  # Distribute remainder across first slices
                quantity += 1

            # Add randomization if enabled
            if self.randomize_size and i > 0 and i < self.num_slices - 1:
                quantity = int(self._add_randomization(quantity, variance_pct=15))

            # Calculate scheduled time
            scheduled_time = start_time + timedelta(minutes=i * interval_minutes)
            scheduled_time = self._add_timing_jitter(scheduled_time)

            slices.append(OrderSlice(
                quantity=quantity,
                scheduled_time=scheduled_time
            ))

        logger.info(f"✅ TWAP: Generated {len(slices)} slices for {self.total_quantity} shares over {self.duration_minutes} minutes")

        return slices


class VWAPAlgorithm(ExecutionAlgorithm):
    """
    Volume-Weighted Average Price Algorithm
    Adjusts slice sizes based on historical volume patterns
    """

    def __init__(
        self,
        ticker: str,
        side: str,
        total_quantity: int,
        duration_minutes: int,
        volume_profile: Optional[List[float]] = None,
        randomize_timing: bool = True,
        randomize_size: bool = True
    ):
        super().__init__(ticker, side, total_quantity, duration_minutes, randomize_timing, randomize_size)

        # Default intraday volume profile (U-shaped: high at open/close, low mid-day)
        if volume_profile is None:
            self.volume_profile = self._generate_default_volume_profile()
        else:
            self.volume_profile = volume_profile

    def _generate_default_volume_profile(self) -> List[float]:
        """Generate a typical U-shaped intraday volume profile"""
        # Simulate 30-minute intervals across trading day
        # Higher volume at open (9:30-10:00, 15:30-16:00), lower mid-day
        profile = [
            0.15,  # 9:30-10:00 (high opening volume)
            0.12,  # 10:00-10:30
            0.08,  # 10:30-11:00
            0.06,  # 11:00-11:30
            0.05,  # 11:30-12:00
            0.04,  # 12:00-12:30 (lunch, low volume)
            0.04,  # 12:30-13:00
            0.05,  # 13:00-13:30
            0.06,  # 13:30-14:00
            0.08,  # 14:00-14:30
            0.10,  # 14:30-15:00
            0.12,  # 15:00-15:30
            0.05   # 15:30-16:00 (high closing volume)
        ]
        return profile

    def generate_slices(self, market_data: Optional[MarketData] = None) -> List[OrderSlice]:
        """Generate volume-weighted order slices"""

        num_slices = len(self.volume_profile)
        interval_minutes = self.duration_minutes / num_slices
        start_time = datetime.now()

        slices = []
        allocated = 0

        for i, volume_weight in enumerate(self.volume_profile):
            # Calculate quantity based on volume profile
            if i == num_slices - 1:
                # Last slice gets remainder
                quantity = self.total_quantity - allocated
            else:
                quantity = int(self.total_quantity * volume_weight)
                allocated += quantity

            # Add randomization if enabled
            if self.randomize_size and i > 0 and i < num_slices - 1:
                max_variance = int(quantity * 0.1)
                quantity += random.randint(-max_variance, max_variance)

            # Calculate scheduled time
            scheduled_time = start_time + timedelta(minutes=i * interval_minutes)
            scheduled_time = self._add_timing_jitter(scheduled_time)

            if quantity > 0:
                slices.append(OrderSlice(
                    quantity=quantity,
                    scheduled_time=scheduled_time
                ))

        logger.info(f"✅ VWAP: Generated {len(slices)} volume-weighted slices for {self.total_quantity} shares")

        return slices


class ImplementationShortfallAlgorithm(ExecutionAlgorithm):
    """
    Implementation Shortfall Algorithm
    Balances urgency vs. market impact - front-loaded execution
    """

    def __init__(
        self,
        ticker: str,
        side: str,
        total_quantity: int,
        duration_minutes: int,
        urgency: float = 0.5,  # 0 = patient, 1 = aggressive
        randomize_timing: bool = True,
        randomize_size: bool = True
    ):
        super().__init__(ticker, side, total_quantity, duration_minutes, randomize_timing, randomize_size)
        self.urgency = max(0.0, min(1.0, urgency))  # Clamp between 0 and 1

    def generate_slices(self, market_data: Optional[MarketData] = None) -> List[OrderSlice]:
        """Generate front-loaded slices based on urgency"""

        # More urgent = more slices early on
        num_slices = max(3, int(10 * self.urgency) + 5)

        start_time = datetime.now()
        slices = []
        allocated = 0

        # Generate exponentially decreasing slice sizes
        weights = []
        decay_factor = 2.0 + (self.urgency * 3.0)  # Higher urgency = steeper decay

        for i in range(num_slices):
            weight = np.exp(-i / decay_factor)
            weights.append(weight)

        # Normalize weights
        total_weight = sum(weights)
        weights = [w / total_weight for w in weights]

        interval_minutes = self.duration_minutes / num_slices

        for i, weight in enumerate(weights):
            if i == num_slices - 1:
                quantity = self.total_quantity - allocated
            else:
                quantity = int(self.total_quantity * weight)
                allocated += quantity

            # Add randomization
            if self.randomize_size and i > 0 and i < num_slices - 1:
                max_variance = int(quantity * 0.12)
                quantity += random.randint(-max_variance, max_variance)

            scheduled_time = start_time + timedelta(minutes=i * interval_minutes)
            scheduled_time = self._add_timing_jitter(scheduled_time)

            if quantity > 0:
                slices.append(OrderSlice(
                    quantity=quantity,
                    scheduled_time=scheduled_time
                ))

        logger.info(f"✅ IS: Generated {len(slices)} front-loaded slices (urgency={self.urgency:.1f}) for {self.total_quantity} shares")

        return slices


class PercentageOfVolumeAlgorithm(ExecutionAlgorithm):
    """
    Percentage of Volume (POV) Algorithm
    Executes as a target percentage of market volume
    """

    def __init__(
        self,
        ticker: str,
        side: str,
        total_quantity: int,
        duration_minutes: int,
        target_pov: float = 10.0,  # Target % of market volume
        estimated_daily_volume: Optional[int] = None,
        randomize_timing: bool = True,
        randomize_size: bool = True
    ):
        super().__init__(ticker, side, total_quantity, duration_minutes, randomize_timing, randomize_size)
        self.target_pov = target_pov / 100.0  # Convert to decimal
        self.estimated_daily_volume = estimated_daily_volume

    def generate_slices(self, market_data: Optional[MarketData] = None) -> List[OrderSlice]:
        """Generate slices based on percentage of volume"""

        # If we don't have estimated volume, fall back to TWAP-like behavior
        if self.estimated_daily_volume is None:
            logger.warning(f"⚠️ POV: No volume estimate, falling back to TWAP-like behavior")
            num_slices = max(3, self.duration_minutes // 5)
            base_quantity = self.total_quantity // num_slices
        else:
            # Estimate volume during our execution window
            # Assume trading day is 6.5 hours (390 minutes)
            volume_ratio = self.duration_minutes / 390.0
            expected_volume = int(self.estimated_daily_volume * volume_ratio)

            # Calculate slice size to match target POV
            # POV = our_volume / market_volume
            # Slice frequently enough to track market volume
            num_slices = max(3, self.duration_minutes // 3)  # Every 3 minutes

            base_quantity = int((expected_volume * self.target_pov) / num_slices)

        interval_minutes = self.duration_minutes / num_slices
        start_time = datetime.now()

        slices = []
        allocated = 0

        for i in range(num_slices):
            if i == num_slices - 1:
                quantity = self.total_quantity - allocated
            else:
                quantity = base_quantity
                allocated += quantity

            # Add randomization
            if self.randomize_size and i > 0 and i < num_slices - 1:
                max_variance = int(quantity * 0.15)
                quantity += random.randint(-max_variance, max_variance)

            scheduled_time = start_time + timedelta(minutes=i * interval_minutes)
            scheduled_time = self._add_timing_jitter(scheduled_time)

            if quantity > 0:
                slices.append(OrderSlice(
                    quantity=quantity,
                    scheduled_time=scheduled_time
                ))

        logger.info(f"✅ POV: Generated {len(slices)} slices targeting {self.target_pov*100:.1f}% of volume for {self.total_quantity} shares")

        return slices


class AlgorithmFactory:
    """Factory for creating execution algorithms"""

    @staticmethod
    def create_algorithm(
        algo_type: str,
        ticker: str,
        side: str,
        total_quantity: int,
        duration_minutes: int,
        **kwargs
    ) -> ExecutionAlgorithm:
        """
        Create an execution algorithm

        Args:
            algo_type: "twap", "vwap", "is", or "pov"
            ticker: Stock ticker
            side: "buy" or "sell"
            total_quantity: Total shares to execute
            duration_minutes: Execution time window
            **kwargs: Algorithm-specific parameters

        Returns:
            ExecutionAlgorithm instance
        """

        algo_type = algo_type.lower()

        if algo_type == "twap":
            return TWAPAlgorithm(
                ticker=ticker,
                side=side,
                total_quantity=total_quantity,
                duration_minutes=duration_minutes,
                num_slices=kwargs.get("num_slices"),
                randomize_timing=kwargs.get("randomize_timing", True),
                randomize_size=kwargs.get("randomize_size", True)
            )

        elif algo_type == "vwap":
            return VWAPAlgorithm(
                ticker=ticker,
                side=side,
                total_quantity=total_quantity,
                duration_minutes=duration_minutes,
                volume_profile=kwargs.get("volume_profile"),
                randomize_timing=kwargs.get("randomize_timing", True),
                randomize_size=kwargs.get("randomize_size", True)
            )

        elif algo_type == "is":
            return ImplementationShortfallAlgorithm(
                ticker=ticker,
                side=side,
                total_quantity=total_quantity,
                duration_minutes=duration_minutes,
                urgency=kwargs.get("urgency", 0.5),
                randomize_timing=kwargs.get("randomize_timing", True),
                randomize_size=kwargs.get("randomize_size", True)
            )

        elif algo_type == "pov":
            return PercentageOfVolumeAlgorithm(
                ticker=ticker,
                side=side,
                total_quantity=total_quantity,
                duration_minutes=duration_minutes,
                target_pov=kwargs.get("target_pov", 10.0),
                estimated_daily_volume=kwargs.get("estimated_daily_volume"),
                randomize_timing=kwargs.get("randomize_timing", True),
                randomize_size=kwargs.get("randomize_size", True)
            )

        else:
            raise ValueError(f"Unknown algorithm type: {algo_type}. Must be one of: twap, vwap, is, pov")
