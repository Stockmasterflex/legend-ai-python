"""
Legend AI Pattern Recognition Engine

Professional-grade pattern detection system developed by Legend AI.
Institutional-quality technical analysis with advanced pattern recognition.
"""
from .helpers import PatternData, PatternHelpers, get_pattern_helpers
from .detector import PatternDetector, get_pattern_detector
from .filter import PatternFilter
from .candlesticks import find_candlesticks
from .export import PatternExporter
from .scoring import PatternScorer, ScoreComponents
from .scanner import UniverseScanner, ScanConfig
from .patterns import (
    find_cup,
    find_double_bottoms,
    find_ascending_triangle,
    find_descending_triangle,
    find_sym_triangle,
    find_single_day_patterns,
    find_inside_day,
    find_outside_day,
    find_nr4,
    find_nr7,
    find_wide_range_up,
    find_wide_range_down,
    find_spike_up,
    find_spike_down,
    find_three_bar,
    find_cpr_up,
    find_cpr_down,
    find_ocr_up,
    find_ocr_down,
)

__all__ = [
    'PatternData',
    'PatternHelpers',
    'PatternDetector',
    'PatternFilter',
    'PatternExporter',
    'PatternScorer',
    'ScoreComponents',
    'UniverseScanner',
    'ScanConfig',
    'get_pattern_helpers',
    'get_pattern_detector',
    'find_candlesticks',
    'find_cup',
    'find_double_bottoms',
    'find_ascending_triangle',
    'find_descending_triangle',
    'find_sym_triangle',
    'find_single_day_patterns',
    'find_inside_day',
    'find_outside_day',
    'find_nr4',
    'find_nr7',
    'find_wide_range_up',
    'find_wide_range_down',
    'find_spike_up',
    'find_spike_down',
    'find_three_bar',
    'find_cpr_up',
    'find_cpr_down',
    'find_ocr_up',
    'find_ocr_down',
]

__version__ = '2.0.0'
__author__ = 'Legend AI Research Team'
__copyright__ = 'Copyright © 2025 Legend AI. All rights reserved.'
