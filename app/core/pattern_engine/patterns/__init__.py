"""
Pattern detection modules for the Legend AI pattern engine.
"""
from .cup_handle import find_cup
from .double_bottoms import find_double_bottoms
from .triangles import (
    find_ascending_triangle,
    find_descending_triangle,
    find_sym_triangle,
)
from .single_day import (
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
from .mmu_vcp import find_mmu, find_mmd
from .flags import find_ht_flag, find_flags, find_pennants
from .wedges import find_wedges
from .triple_formations import find_triple_bottoms, find_triple_tops
from .head_shoulders import find_head_shoulders_top, find_head_shoulders_bottom
from .rectangles import find_rectangles
from .channels import (
    find_channels,
    find_ascending_channel,
    find_descending_channel,
    find_horizontal_channel,
)
from .broadening import (
    find_broadening_formations,
    find_broadening_top,
    find_broadening_bottom,
)

__all__ = [
    # Classic patterns
    'find_cup',
    'find_double_bottoms',
    'find_ascending_triangle',
    'find_descending_triangle',
    'find_sym_triangle',
    
    # Single-day patterns
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
    
    # Critical Minervini patterns
    'find_mmu',
    'find_mmd',
    
    # Flag patterns
    'find_ht_flag',
    'find_flags',
    'find_pennants',
    
    # Wedge patterns
    'find_wedges',

    # Triple formations
    'find_triple_bottoms',
    'find_triple_tops',

    # Head & Shoulders
    'find_head_shoulders_top',
    'find_head_shoulders_bottom',

    # Rectangles
    'find_rectangles',

    # Channels
    'find_channels',
    'find_ascending_channel',
    'find_descending_channel',
    'find_horizontal_channel',

    # Broadening formations
    'find_broadening_formations',
    'find_broadening_top',
    'find_broadening_bottom',
]
