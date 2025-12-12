"""
Pattern detection modules for the Legend AI pattern engine.
"""

from .broadening import (find_broadening_bottom, find_broadening_formations,
                         find_broadening_top)
from .channels import (find_ascending_channel, find_channels,
                       find_descending_channel, find_horizontal_channel)
from .cup_handle import find_cup
from .double_bottoms import find_double_bottoms
from .flags import find_flags, find_ht_flag, find_pennants
from .head_shoulders import find_head_shoulders_bottom, find_head_shoulders_top
from .mmu_vcp import find_mmd, find_mmu
from .rectangles import find_rectangles
from .single_day import (find_cpr_down, find_cpr_up, find_inside_day, find_nr4,
                         find_nr7, find_ocr_down, find_ocr_up,
                         find_outside_day, find_single_day_patterns,
                         find_spike_down, find_spike_up, find_three_bar,
                         find_wide_range_down, find_wide_range_up)
from .triangles import (find_ascending_triangle, find_descending_triangle,
                        find_sym_triangle)
from .triple_formations import find_triple_bottoms, find_triple_tops
from .wedges import find_wedges

__all__ = [
    # Classic patterns
    "find_cup",
    "find_double_bottoms",
    "find_ascending_triangle",
    "find_descending_triangle",
    "find_sym_triangle",
    # Single-day patterns
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
    # Critical Minervini patterns
    "find_mmu",
    "find_mmd",
    # Flag patterns
    "find_ht_flag",
    "find_flags",
    "find_pennants",
    # Wedge patterns
    "find_wedges",
    # Triple formations
    "find_triple_bottoms",
    "find_triple_tops",
    # Head & Shoulders
    "find_head_shoulders_top",
    "find_head_shoulders_bottom",
    # Rectangles
    "find_rectangles",
    # Channels
    "find_channels",
    "find_ascending_channel",
    "find_descending_channel",
    "find_horizontal_channel",
    # Broadening formations
    "find_broadening_formations",
    "find_broadening_top",
    "find_broadening_bottom",
]
