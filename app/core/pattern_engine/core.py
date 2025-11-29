"""
Bulkowski Pattern Detection - Main Entry Point

This module provides the main interface to Bulkowski's pattern detection algorithms
ported from Patternz (C#/.NET).
"""
from .helpers import PatternData, PatternHelpers, get_pattern_helpers
from .detector import BulkowskiDetector, get_bulkowski_detector
from .filter import PatternFilter
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
    'BulkowskiDetector',
    'PatternFilter',
    'get_pattern_helpers',
    'get_bulkowski_detector',
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

# Version info
__version__ = '1.0.0'
__author__ = 'Legend AI (ported from Thomas Bulkowski\'s Patternz)'
