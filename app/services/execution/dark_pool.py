"""
Dark Pool Routing
Routes orders to dark pools for price improvement and size discovery
"""

import logging
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime, timedelta
import random

logger = logging.getLogger(__name__)


@dataclass
class DarkPoolVenue:
    """Dark pool venue information"""
    venue_id: int
    name: str
    min_size: int  # Minimum order size
    max_size: Optional[int]  # Maximum order size (None = no limit)
    typical_spread_improvement_bps: float  # Historical spread improvement
    fill_rate: float  # Historical fill rate (0-100%)
    avg_fill_time_ms: float  # Average time to fill
    supports_midpoint_peg: bool  # Supports midpoint pegging
    supports_size_discovery: bool  # Supports size discovery
    is_active: bool


@dataclass
class DarkPoolOrder:
    """Dark pool order details"""
    order_id: str
    venue_id: int
    venue_name: str
    quantity: int
    limit_price: Optional[float]
    peg_to_midpoint: bool
    time_in_force: str  # "IOC", "FOK", "DAY"
    min_fill_quantity: Optional[int]  # Minimum acceptable fill
    posted_at: datetime
    expires_at: Optional[datetime]


@dataclass
class DarkPoolFill:
    """Dark pool fill result"""
    order_id: str
    venue_id: int
    venue_name: str
    quantity: int
    fill_price: float
    spread_improvement_bps: float
    filled_at: datetime
    was_passive: bool  # True if we provided liquidity


class DarkPoolRouter:
    """
    Routes orders to dark pools for price improvement
    """

    def __init__(self, sweep_timeout_ms: int = 500):
        """
        Initialize dark pool router

        Args:
            sweep_timeout_ms: Timeout for dark pool sweep in milliseconds
        """
        self.sweep_timeout_ms = sweep_timeout_ms

    def route_to_dark_pools(
        self,
        ticker: str,
        side: str,
        quantity: int,
        limit_price: float,
        nbbo_mid: float,  # National Best Bid/Offer midpoint
        dark_pools: List[DarkPoolVenue],
        strategy: str = "aggressive"  # "aggressive", "passive", "hybrid"
    ) -> List[DarkPoolOrder]:
        """
        Route order to dark pools

        Args:
            ticker: Stock ticker
            side: "buy" or "sell"
            quantity: Order quantity
            limit_price: Maximum price willing to pay (buy) or minimum to receive (sell)
            nbbo_mid: Current NBBO midpoint
            dark_pools: Available dark pool venues
            strategy: Routing strategy

        Returns:
            List of dark pool orders created
        """

        # Filter eligible dark pools
        eligible = self._filter_eligible_venues(dark_pools, quantity)

        if not eligible:
            logger.warning(f"⚠️ No eligible dark pools for {quantity} shares of {ticker}")
            return []

        # Sort by preference
        ranked = self._rank_dark_pools(eligible, quantity, strategy)

        # Create orders based on strategy
        if strategy == "aggressive":
            # Sweep all dark pools simultaneously
            orders = self._create_sweep_orders(
                ticker, side, quantity, limit_price, nbbo_mid, ranked
            )
        elif strategy == "passive":
            # Post to best dark pool and wait
            orders = self._create_passive_orders(
                ticker, side, quantity, limit_price, nbbo_mid, ranked[:1]
            )
        else:  # hybrid
            # Post to top 2-3 pools
            orders = self._create_passive_orders(
                ticker, side, quantity, limit_price, nbbo_mid, ranked[:3]
            )

        logger.info(
            f"🌑 Created {len(orders)} dark pool orders for {ticker} "
            f"({strategy} strategy)"
        )

        return orders

    def _filter_eligible_venues(
        self,
        venues: List[DarkPoolVenue],
        quantity: int
    ) -> List[DarkPoolVenue]:
        """Filter dark pools that can handle this order"""

        eligible = []

        for venue in venues:
            if not venue.is_active:
                continue

            if quantity < venue.min_size:
                continue

            if venue.max_size and quantity > venue.max_size:
                continue

            eligible.append(venue)

        return eligible

    def _rank_dark_pools(
        self,
        venues: List[DarkPoolVenue],
        quantity: int,
        strategy: str
    ) -> List[DarkPoolVenue]:
        """
        Rank dark pools by preference

        Args:
            venues: Dark pool venues
            quantity: Order quantity
            strategy: Routing strategy

        Returns:
            Sorted list of venues
        """

        def score_venue(venue: DarkPoolVenue) -> float:
            # Base score from spread improvement
            score = venue.typical_spread_improvement_bps * 10

            # Add fill rate bonus
            score += venue.fill_rate * 0.5

            # Speed bonus (lower time = higher score)
            if venue.avg_fill_time_ms < 100:
                score += 20
            elif venue.avg_fill_time_ms < 250:
                score += 10

            # Feature bonuses
            if venue.supports_midpoint_peg:
                score += 15
            if venue.supports_size_discovery:
                score += 10

            # Adjust for strategy
            if strategy == "aggressive":
                # Prefer fast fills
                score += (500 - min(venue.avg_fill_time_ms, 500)) / 10
            elif strategy == "passive":
                # Prefer high spread improvement
                score += venue.typical_spread_improvement_bps * 5

            return score

        ranked = sorted(venues, key=score_venue, reverse=True)

        return ranked

    def _create_sweep_orders(
        self,
        ticker: str,
        side: str,
        total_quantity: int,
        limit_price: float,
        nbbo_mid: float,
        venues: List[DarkPoolVenue]
    ) -> List[DarkPoolOrder]:
        """
        Create IOC sweep orders across dark pools

        Sends small quantities to multiple pools simultaneously
        to find hidden liquidity quickly
        """

        orders = []

        # For sweeps, send smaller test quantities
        # Allocate quantity across venues
        num_venues = min(len(venues), 5)  # Don't spam too many
        quantity_per_venue = max(100, total_quantity // (num_venues * 2))

        now = datetime.now()

        for venue in venues[:num_venues]:
            order = DarkPoolOrder(
                order_id=f"dp_sweep_{ticker}_{venue.venue_id}_{now.timestamp()}",
                venue_id=venue.venue_id,
                venue_name=venue.name,
                quantity=quantity_per_venue,
                limit_price=limit_price,
                peg_to_midpoint=venue.supports_midpoint_peg,
                time_in_force="IOC",  # Immediate or Cancel
                min_fill_quantity=None,
                posted_at=now,
                expires_at=now + timedelta(milliseconds=self.sweep_timeout_ms)
            )

            orders.append(order)

        return orders

    def _create_passive_orders(
        self,
        ticker: str,
        side: str,
        total_quantity: int,
        limit_price: float,
        nbbo_mid: float,
        venues: List[DarkPoolVenue]
    ) -> List[DarkPoolOrder]:
        """
        Create passive orders that wait for fills

        Posts full quantity and waits, potentially getting better prices
        """

        orders = []
        now = datetime.now()

        # Split quantity across top venues
        if len(venues) == 1:
            quantities = [total_quantity]
        else:
            # Allocate more to better venues
            weights = [3, 2, 1][:len(venues)]
            total_weight = sum(weights)
            quantities = [int(total_quantity * w / total_weight) for w in weights]

            # Ensure we allocate everything
            quantities[-1] += total_quantity - sum(quantities)

        for venue, qty in zip(venues, quantities):
            if qty < venue.min_size:
                continue

            # For passive orders, we can use midpoint pegging if available
            use_midpoint = venue.supports_midpoint_peg

            order = DarkPoolOrder(
                order_id=f"dp_passive_{ticker}_{venue.venue_id}_{now.timestamp()}",
                venue_id=venue.venue_id,
                venue_name=venue.name,
                quantity=qty,
                limit_price=limit_price,
                peg_to_midpoint=use_midpoint,
                time_in_force="DAY",
                min_fill_quantity=None,
                posted_at=now,
                expires_at=None  # Day order
            )

            orders.append(order)

        return orders


class SizeDiscovery:
    """
    Size discovery in dark pools
    Finds hidden liquidity without revealing full order size
    """

    def __init__(self):
        self.discovered_sizes: Dict[str, List[Tuple[datetime, int]]] = {}

    def probe_for_size(
        self,
        ticker: str,
        side: str,
        estimated_size: int,
        dark_pools: List[DarkPoolVenue],
        nbbo_mid: float
    ) -> Dict[int, int]:
        """
        Probe dark pools to discover available size

        Args:
            ticker: Stock ticker
            side: "buy" or "sell"
            estimated_size: Estimated order size
            dark_pools: Dark pools to probe
            nbbo_mid: NBBO midpoint

        Returns:
            Dict of venue_id -> estimated_available_size
        """

        discovered = {}

        # Filter to venues supporting size discovery
        discovery_venues = [
            v for v in dark_pools
            if v.supports_size_discovery and v.is_active
        ]

        if not discovery_venues:
            logger.warning("⚠️ No dark pools support size discovery")
            return discovered

        # Send small probe orders
        probe_size = min(100, estimated_size // 10)

        logger.info(
            f"🔍 Probing {len(discovery_venues)} dark pools with {probe_size} share orders"
        )

        for venue in discovery_venues:
            # Simulate probe (in reality, would send IOC order)
            # Based on historical fill rate, estimate available size
            expected_fill_rate = venue.fill_rate / 100.0

            if expected_fill_rate > 0.8:
                # High fill rate = good liquidity
                estimated_available = int(estimated_size * random.uniform(0.5, 1.5))
            elif expected_fill_rate > 0.5:
                # Medium fill rate
                estimated_available = int(estimated_size * random.uniform(0.2, 0.7))
            else:
                # Low fill rate
                estimated_available = int(estimated_size * random.uniform(0.05, 0.3))

            discovered[venue.venue_id] = estimated_available

            logger.info(
                f"  📊 {venue.name}: ~{estimated_available:,} shares available "
                f"(fill rate: {venue.fill_rate:.1f}%)"
            )

        # Store discovery results
        self.discovered_sizes[ticker] = [(datetime.now(), sum(discovered.values()))]

        return discovered

    def get_discovered_size(self, ticker: str) -> Optional[int]:
        """Get most recent discovered size for a ticker"""

        if ticker not in self.discovered_sizes:
            return None

        if not self.discovered_sizes[ticker]:
            return None

        # Return most recent
        return self.discovered_sizes[ticker][-1][1]


class PriceImprovementTracker:
    """
    Track price improvement from dark pool executions
    """

    def __init__(self):
        self.improvements: List[Dict[str, Any]] = []

    def record_fill(
        self,
        ticker: str,
        venue_id: int,
        venue_name: str,
        fill_price: float,
        nbbo_mid: float,
        quantity: int,
        side: str
    ):
        """
        Record a dark pool fill and calculate price improvement

        Args:
            ticker: Stock ticker
            venue_id: Venue ID
            venue_name: Venue name
            fill_price: Actual fill price
            nbbo_mid: NBBO midpoint at time of fill
            quantity: Fill quantity
            side: "buy" or "sell"
        """

        # Calculate improvement vs midpoint
        if side.lower() == "buy":
            # For buys, lower is better
            improvement_bps = ((nbbo_mid - fill_price) / nbbo_mid) * 10000
        else:  # sell
            # For sells, higher is better
            improvement_bps = ((fill_price - nbbo_mid) / nbbo_mid) * 10000

        # Calculate dollar improvement
        dollar_improvement = abs(fill_price - nbbo_mid) * quantity

        record = {
            "timestamp": datetime.now(),
            "ticker": ticker,
            "venue_id": venue_id,
            "venue_name": venue_name,
            "side": side,
            "quantity": quantity,
            "fill_price": fill_price,
            "nbbo_mid": nbbo_mid,
            "improvement_bps": improvement_bps,
            "dollar_improvement": dollar_improvement
        }

        self.improvements.append(record)

        if improvement_bps > 0:
            logger.info(
                f"✅ Dark pool price improvement: {venue_name} - "
                f"{improvement_bps:.2f} bps (${dollar_improvement:.2f})"
            )
        else:
            logger.warning(
                f"⚠️ Dark pool price deterioration: {venue_name} - "
                f"{improvement_bps:.2f} bps"
            )

    def get_statistics(
        self,
        ticker: Optional[str] = None,
        venue_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Get price improvement statistics

        Args:
            ticker: Filter by ticker (None = all)
            venue_id: Filter by venue (None = all)

        Returns:
            Statistics dictionary
        """

        filtered = self.improvements

        if ticker:
            filtered = [r for r in filtered if r["ticker"] == ticker]

        if venue_id:
            filtered = [r for r in filtered if r["venue_id"] == venue_id]

        if not filtered:
            return {"message": "No dark pool fills recorded"}

        total_fills = len(filtered)
        total_quantity = sum(r["quantity"] for r in filtered)
        avg_improvement_bps = sum(r["improvement_bps"] for r in filtered) / total_fills
        total_dollar_improvement = sum(r["dollar_improvement"] for r in filtered)

        fills_with_improvement = len([r for r in filtered if r["improvement_bps"] > 0])
        improvement_rate = (fills_with_improvement / total_fills * 100) if total_fills > 0 else 0

        return {
            "total_dark_pool_fills": total_fills,
            "total_quantity": total_quantity,
            "avg_improvement_bps": round(avg_improvement_bps, 2),
            "total_dollar_improvement": round(total_dollar_improvement, 2),
            "fills_with_improvement": fills_with_improvement,
            "improvement_rate_pct": round(improvement_rate, 1),
            "best_venue": max(
                filtered, key=lambda x: x["improvement_bps"]
            )["venue_name"] if filtered else None
        }


class DarkPoolReporting:
    """
    Reporting and compliance for dark pool executions
    """

    @staticmethod
    def generate_fill_report(
        fills: List[DarkPoolFill],
        nbbo_at_time: Dict[datetime, Tuple[float, float]]  # timestamp -> (bid, ask)
    ) -> Dict[str, Any]:
        """
        Generate regulatory-compliant fill report

        Args:
            fills: List of dark pool fills
            nbbo_at_time: NBBO quotes at fill times

        Returns:
            Compliance report
        """

        if not fills:
            return {"message": "No fills to report"}

        report = {
            "report_date": datetime.now().isoformat(),
            "total_fills": len(fills),
            "total_quantity": sum(f.quantity for f in fills),
            "venues_used": list(set(f.venue_name for f in fills)),
            "fills": []
        }

        for fill in fills:
            # Get NBBO at fill time
            nbbo = nbbo_at_time.get(fill.filled_at)

            if nbbo:
                bid, ask = nbbo
                mid = (bid + ask) / 2
                spread = ask - bid
            else:
                bid = ask = mid = spread = None

            fill_record = {
                "order_id": fill.order_id,
                "venue": fill.venue_name,
                "quantity": fill.quantity,
                "price": fill.fill_price,
                "timestamp": fill.filled_at.isoformat(),
                "nbbo_bid": bid,
                "nbbo_ask": ask,
                "nbbo_mid": mid,
                "spread_improvement_bps": fill.spread_improvement_bps,
                "was_passive": fill.was_passive,
                "price_vs_midpoint": (fill.fill_price - mid) if mid else None
            }

            report["fills"].append(fill_record)

        logger.info(
            f"📋 Generated dark pool report: {len(fills)} fills across "
            f"{len(report['venues_used'])} venues"
        )

        return report
