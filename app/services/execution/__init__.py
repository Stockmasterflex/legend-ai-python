"""
Intelligent Trade Execution System

This module provides comprehensive trade execution capabilities including:
- Execution algorithms (TWAP, VWAP, Implementation Shortfall, POV)
- Venue selection and smart routing
- Order slicing with iceberg orders
- Execution analytics and benchmarking
- Dark pool routing and price improvement
"""

from .algorithms import (
    ExecutionAlgorithm,
    TWAPAlgorithm,
    VWAPAlgorithm,
    ImplementationShortfallAlgorithm,
    PercentageOfVolumeAlgorithm,
    AlgorithmFactory,
    OrderSlice,
    MarketData
)

from .venue_selection import (
    VenueSelector,
    SmartRouter,
    VenueInfo,
    VenueScore,
    VenuePerformanceTracker
)

from .order_slicer import (
    OrderSlicer,
    AdaptiveSlicer,
    SlicedOrder,
    MarketImpactCalculator
)

from .analytics import (
    ExecutionAnalyzer,
    ExecutionReport,
    BenchmarkCalculator,
    PerformanceTracker,
    Fill
)

from .dark_pool import (
    DarkPoolRouter,
    DarkPoolVenue,
    DarkPoolOrder,
    DarkPoolFill,
    SizeDiscovery,
    PriceImprovementTracker,
    DarkPoolReporting
)

__all__ = [
    # Algorithms
    "ExecutionAlgorithm",
    "TWAPAlgorithm",
    "VWAPAlgorithm",
    "ImplementationShortfallAlgorithm",
    "PercentageOfVolumeAlgorithm",
    "AlgorithmFactory",
    "OrderSlice",
    "MarketData",

    # Venue Selection
    "VenueSelector",
    "SmartRouter",
    "VenueInfo",
    "VenueScore",
    "VenuePerformanceTracker",

    # Order Slicing
    "OrderSlicer",
    "AdaptiveSlicer",
    "SlicedOrder",
    "MarketImpactCalculator",

    # Analytics
    "ExecutionAnalyzer",
    "ExecutionReport",
    "BenchmarkCalculator",
    "PerformanceTracker",
    "Fill",

    # Dark Pool
    "DarkPoolRouter",
    "DarkPoolVenue",
    "DarkPoolOrder",
    "DarkPoolFill",
    "SizeDiscovery",
    "PriceImprovementTracker",
    "DarkPoolReporting",
]
