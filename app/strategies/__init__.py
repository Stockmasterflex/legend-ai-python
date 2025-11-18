"""
Trading Strategies Module

This module contains implementations of proven trading strategies from legendary traders:
- Mark Minervini (SEPA, VCP, Stage Analysis)
- William O'Neil (CAN SLIM, Cup & Handle)
- Stan Weinstein (4-Stage Cycle Analysis)

Each strategy module provides:
- Stock screening/scanning based on criteria
- Entry/exit signal generation
- Position sizing recommendations
- Risk management rules
"""

from .minervini import MinerviniStrategy
from .oneil import ONeilStrategy
from .weinstein import WeinsteinStrategy

__all__ = ['MinerviniStrategy', 'ONeilStrategy', 'WeinsteinStrategy']
