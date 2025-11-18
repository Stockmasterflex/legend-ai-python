"""
Order Slicing and Iceberg Orders
Breaks large orders into smaller pieces to minimize market impact
"""

import logging
import random
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


@dataclass
class SlicedOrder:
    """A sliced portion of a larger order"""
    slice_id: str
    quantity: int
    scheduled_time: datetime
    limit_price: Optional[float] = None
    is_iceberg: bool = False
    display_quantity: Optional[int] = None
    hidden_quantity: Optional[int] = None
    venue_id: Optional[int] = None
    priority: int = 0  # Higher priority executes first


class OrderSlicer:
    """
    Intelligent order slicing to minimize market impact
    """

    def __init__(
        self,
        min_slice_size: int = 100,
        max_slice_size: Optional[int] = None,
        randomize: bool = True
    ):
        """
        Initialize order slicer

        Args:
            min_slice_size: Minimum size for a slice
            max_slice_size: Maximum size for a slice (None = no limit)
            randomize: Whether to randomize slice sizes
        """
        self.min_slice_size = min_slice_size
        self.max_slice_size = max_slice_size
        self.randomize = randomize

    def slice_order(
        self,
        total_quantity: int,
        num_slices: Optional[int] = None,
        target_slice_size: Optional[int] = None
    ) -> List[int]:
        """
        Slice an order into smaller pieces

        Args:
            total_quantity: Total quantity to slice
            num_slices: Target number of slices (if None, uses target_slice_size)
            target_slice_size: Target size per slice (if None, uses num_slices)

        Returns:
            List of slice quantities
        """

        if total_quantity < self.min_slice_size:
            logger.warning(f"⚠️ Order size {total_quantity} below minimum slice size")
            return [total_quantity]

        # Determine number of slices
        if num_slices is None:
            if target_slice_size is None:
                # Default: slice into chunks of ~500 shares
                target_slice_size = min(500, total_quantity // 2)

            num_slices = max(2, total_quantity // target_slice_size)

        # Calculate base slice size
        base_size = total_quantity // num_slices
        remainder = total_quantity % num_slices

        # Ensure minimum slice size
        if base_size < self.min_slice_size:
            num_slices = total_quantity // self.min_slice_size
            base_size = self.min_slice_size

        slices = []
        allocated = 0

        for i in range(num_slices):
            # Calculate slice size
            size = base_size

            # Distribute remainder
            if i < remainder:
                size += 1

            # Add randomization if enabled
            if self.randomize and i > 0 and i < num_slices - 1:
                variance = int(size * 0.15)  # ±15% variance
                size = size + random.randint(-variance, variance)

            # Enforce max slice size
            if self.max_slice_size:
                size = min(size, self.max_slice_size)

            # Ensure we don't exceed total
            if allocated + size > total_quantity:
                size = total_quantity - allocated

            if size >= self.min_slice_size or i == num_slices - 1:
                slices.append(size)
                allocated += size

        # Adjust last slice to account for any rounding
        if allocated < total_quantity:
            slices[-1] += (total_quantity - allocated)

        logger.info(f"📊 Sliced {total_quantity} shares into {len(slices)} pieces")

        return slices

    def create_iceberg_order(
        self,
        total_quantity: int,
        display_quantity: int,
        clip_size: Optional[int] = None
    ) -> List[SlicedOrder]:
        """
        Create an iceberg order (large order with hidden quantity)

        Args:
            total_quantity: Total order quantity
            display_quantity: Visible quantity in the market
            clip_size: Size of each clip/refresh (defaults to display_quantity)

        Returns:
            List of SlicedOrder objects representing iceberg clips
        """

        if clip_size is None:
            clip_size = display_quantity

        if display_quantity > total_quantity:
            logger.warning(
                f"⚠️ Display quantity ({display_quantity}) > total ({total_quantity}), "
                f"adjusting to total"
            )
            display_quantity = total_quantity

        num_clips = (total_quantity + clip_size - 1) // clip_size  # Ceiling division
        hidden_quantity = total_quantity - display_quantity

        clips = []
        allocated = 0

        for i in range(num_clips):
            # Calculate clip size
            if allocated + clip_size > total_quantity:
                quantity = total_quantity - allocated
            else:
                quantity = clip_size

            # First clip shows display quantity, others are hidden refills
            is_first = (i == 0)
            display = display_quantity if is_first else min(quantity, display_quantity)

            clip = SlicedOrder(
                slice_id=f"iceberg_{i}",
                quantity=quantity,
                scheduled_time=datetime.now(),  # Will be updated when executing
                is_iceberg=True,
                display_quantity=display,
                hidden_quantity=quantity - display if not is_first else 0
            )

            clips.append(clip)
            allocated += quantity

        logger.info(
            f"🧊 Created iceberg order: {total_quantity} shares, "
            f"display={display_quantity}, {len(clips)} clips"
        )

        return clips


class AdaptiveSlicer:
    """
    Adaptive order slicer that adjusts based on market conditions
    """

    def __init__(self, base_slicer: Optional[OrderSlicer] = None):
        self.base_slicer = base_slicer or OrderSlicer()

    def slice_with_market_impact(
        self,
        total_quantity: int,
        avg_daily_volume: int,
        current_volatility: Optional[float] = None,
        spread_bps: Optional[float] = None
    ) -> List[int]:
        """
        Slice order based on market conditions to minimize impact

        Args:
            total_quantity: Total quantity to execute
            avg_daily_volume: Average daily volume for the security
            current_volatility: Current volatility (if available)
            spread_bps: Bid-ask spread in basis points

        Returns:
            List of slice quantities optimized for market conditions
        """

        # Calculate order size as % of daily volume
        volume_participation = (total_quantity / avg_daily_volume) * 100

        logger.info(
            f"📊 Order size: {volume_participation:.2f}% of avg daily volume"
        )

        # Determine slicing strategy based on size
        if volume_participation < 1:
            # Small order - fewer, larger slices
            num_slices = max(2, int(volume_participation * 10))
        elif volume_participation < 5:
            # Medium order - moderate slicing
            num_slices = max(5, int(volume_participation * 5))
        else:
            # Large order - aggressive slicing
            num_slices = max(10, int(volume_participation * 3))

        # Adjust for volatility
        if current_volatility is not None:
            if current_volatility > 0.03:  # High volatility (>3%)
                # Use more slices to reduce impact during volatile periods
                num_slices = int(num_slices * 1.3)
                logger.info(f"📈 High volatility detected, increasing slices")

        # Adjust for spread
        if spread_bps is not None:
            if spread_bps > 20:  # Wide spread
                # Use more slices to work the order carefully
                num_slices = int(num_slices * 1.2)
                logger.info(f"📏 Wide spread detected, increasing slices")

        # Slice the order
        slices = self.base_slicer.slice_order(
            total_quantity=total_quantity,
            num_slices=num_slices
        )

        return slices

    def create_stealth_slices(
        self,
        total_quantity: int,
        duration_minutes: int,
        adv: int  # Average daily volume
    ) -> List[SlicedOrder]:
        """
        Create randomized slices to avoid detection by algorithms

        Args:
            total_quantity: Total quantity
            duration_minutes: Execution window
            adv: Average daily volume

        Returns:
            List of SlicedOrder with randomized timing and sizes
        """

        # Target participation rate (avoid >10% of volume)
        target_participation = min(0.05, total_quantity / adv)

        # Calculate minute-by-minute volume estimate
        minutes_in_day = 390  # 6.5 hour trading day
        volume_per_minute = adv / minutes_in_day

        # Target execution per minute
        target_per_minute = volume_per_minute * target_participation

        # Calculate number of slices
        num_slices = max(5, int(total_quantity / target_per_minute))

        # Generate base slices
        slice_sizes = self.base_slicer.slice_order(
            total_quantity=total_quantity,
            num_slices=num_slices
        )

        # Create sliced orders with randomized timing
        start_time = datetime.now()
        interval = duration_minutes / len(slice_sizes)

        sliced_orders = []

        for i, size in enumerate(slice_sizes):
            # Randomize timing within interval
            offset = random.uniform(0, interval) if i > 0 else 0
            scheduled_time = start_time + timedelta(minutes=(i * interval + offset))

            # Randomly decide if this should be an iceberg
            use_iceberg = size > 1000 and random.random() < 0.3

            if use_iceberg:
                # Show only 30-50% of quantity
                display_pct = random.uniform(0.3, 0.5)
                display_qty = int(size * display_pct)
            else:
                display_qty = None

            order = SlicedOrder(
                slice_id=f"stealth_{i}",
                quantity=size,
                scheduled_time=scheduled_time,
                is_iceberg=use_iceberg,
                display_quantity=display_qty,
                hidden_quantity=size - display_qty if use_iceberg else 0
            )

            sliced_orders.append(order)

        logger.info(
            f"🥷 Created {len(sliced_orders)} stealth slices over {duration_minutes} minutes, "
            f"{sum(1 for o in sliced_orders if o.is_iceberg)} with iceberg"
        )

        return sliced_orders


class MarketImpactCalculator:
    """
    Estimate market impact of order execution
    """

    @staticmethod
    def estimate_impact_bps(
        order_quantity: int,
        avg_daily_volume: int,
        volatility: float,
        spread_bps: float
    ) -> float:
        """
        Estimate market impact in basis points

        Uses simplified square-root model:
        Impact = Spread/2 + Volatility * sqrt(Quantity / ADV) * multiplier

        Args:
            order_quantity: Size of order
            avg_daily_volume: Average daily volume
            volatility: Daily volatility (e.g., 0.02 for 2%)
            spread_bps: Bid-ask spread in basis points

        Returns:
            Estimated impact in basis points
        """

        if avg_daily_volume == 0:
            return spread_bps

        # Volume participation
        participation = order_quantity / avg_daily_volume

        # Square-root impact model
        # Impact scales with sqrt(participation)
        temporary_impact = volatility * (participation ** 0.5) * 10000  # Convert to bps

        # Add spread cost (pay half spread on average)
        spread_cost = spread_bps / 2

        # Total impact
        total_impact = spread_cost + temporary_impact

        logger.debug(
            f"📊 Impact estimate: {total_impact:.2f} bps "
            f"(spread={spread_cost:.2f}, temp={temporary_impact:.2f})"
        )

        return total_impact

    @staticmethod
    def optimal_slice_size(
        total_quantity: int,
        avg_daily_volume: int,
        volatility: float,
        duration_minutes: int
    ) -> int:
        """
        Calculate optimal slice size to balance impact vs. time risk

        Args:
            total_quantity: Total order quantity
            avg_daily_volume: Average daily volume
            volatility: Daily volatility
            duration_minutes: Total execution window

        Returns:
            Recommended slice size
        """

        # Trading day is 390 minutes
        volume_per_minute = avg_daily_volume / 390

        # Target participation rate (typically 5-10%)
        target_rate = 0.075  # 7.5%

        # Calculate slices per minute based on participation
        quantity_per_minute = volume_per_minute * target_rate

        # Calculate number of slices needed
        num_slices = max(1, int(total_quantity / quantity_per_minute))

        # Optimal slice size
        optimal_size = total_quantity // num_slices

        logger.debug(
            f"📐 Optimal slice size: {optimal_size} shares "
            f"({num_slices} slices over {duration_minutes} min)"
        )

        return optimal_size
