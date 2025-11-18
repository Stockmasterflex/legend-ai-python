"""
Pre-built Strategy Templates
Ready-to-use trading strategies based on proven patterns
"""

from .vcp_strategy import VCPStrategy
from .minervini_strategy import MinerviniStrategy
from .cup_handle_strategy import CupHandleStrategy
from .templates import StrategyTemplateLibrary

__all__ = [
    "VCPStrategy",
    "MinerviniStrategy",
    "CupHandleStrategy",
    "StrategyTemplateLibrary",
]
