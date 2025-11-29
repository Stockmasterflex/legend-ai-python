"""
Legend AI Pattern Recognition Engine

Professional-grade pattern detection system developed by Legend AI.
Institutional-quality technical analysis with advanced pattern recognition.
"""

from .candlesticks import find_candlesticks
from .detector import PatternDetector, get_pattern_detector
from .export import PatternExporter
from .filter import PatternFilter
from .helpers import PatternData, PatternHelpers, get_pattern_helpers
from .patterns import (find_ascending_triangle, find_cpr_down, find_cpr_up,
                       find_cup, find_descending_triangle, find_double_bottoms,
                       find_inside_day, find_nr4, find_nr7, find_ocr_down,
                       find_ocr_up, find_outside_day, find_single_day_patterns,
                       find_spike_down, find_spike_up, find_sym_triangle,
                       find_three_bar, find_wide_range_down,
                       find_wide_range_up)
from .scanner import ScanConfig, UniverseScanner
from .scoring import PatternScorer, ScoreComponents

__all__ = [
    "PatternData",
    "PatternHelpers",
    "PatternDetector",
    "PatternFilter",
    "PatternExporter",
    "PatternScorer",
    "ScoreComponents",
    "UniverseScanner",
    "ScanConfig",
    "get_pattern_helpers",
    "get_pattern_detector",
    "find_candlesticks",
    "find_cup",
    "find_double_bottoms",
    "find_ascending_triangle",
    "find_descending_triangle",
    "find_sym_triangle",
    "find_single_day_patterns",
    "find_inside_day",
    "find_outside_day",
    "find_nr4",
    "find_nr7",
    "find_wide_range_up",
    "find_wide_range_down",
    "find_spike_up",
    "find_spike_down",
    "find_three_bar",
    "find_cpr_up",
    "find_cpr_down",
    "find_ocr_up",
    "find_ocr_down",
]

__version__ = "2.0.0"
__author__ = "Legend AI Research Team"
__copyright__ = "Copyright © 2025 Legend AI. All rights reserved."
