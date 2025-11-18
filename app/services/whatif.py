"""
What-if analysis engine for exploring alternative trading scenarios
Answer questions like "What if I entered earlier?" or "What if I held longer?"
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import pandas as pd
import numpy as np
import json

from app.models import WhatIfScenario, Ticker
from app.services.database import DatabaseService
from app.services.market_data import MarketDataService


class WhatIfEngine:
    """
    Scenario analysis engine for comparing alternative trading decisions
    """

    def __init__(self, db_service: DatabaseService, market_data_service: MarketDataService):
        self.db = db_service
        self.market_data = market_data_service

    async def analyze_entry_timing(
        self,
        user_id: str,
        ticker_symbol: str,
        base_entry_date: datetime,
        base_entry_price: float,
        alternative_entry_date: datetime,
        exit_date: datetime,
        position_size: int = 100,
        scenario_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Compare different entry timings

        Args:
            user_id: User identifier
            ticker_symbol: Stock ticker
            base_entry_date: Original entry date
            base_entry_price: Original entry price
            alternative_entry_date: Alternative entry date
            exit_date: Common exit date for comparison
            position_size: Number of shares
            scenario_name: Optional scenario name

        Returns:
            Comparison results
        """
        # Fetch historical data
        data = await self._fetch_price_data(ticker_symbol, base_entry_date, exit_date)

        # Find alternative entry price
        alt_entry_idx = (data['timestamp'] - alternative_entry_date).abs().idxmin()
        alt_entry_price = data.loc[alt_entry_idx, 'close']

        # Find exit price
        exit_idx = (data['timestamp'] - exit_date).abs().idxmin()
        exit_price = data.loc[exit_idx, 'close']

        # Calculate P&L for both scenarios
        base_pnl = (exit_price - base_entry_price) * position_size
        base_pnl_pct = ((exit_price - base_entry_price) / base_entry_price) * 100

        alt_pnl = (exit_price - alt_entry_price) * position_size
        alt_pnl_pct = ((exit_price - alt_entry_price) / alt_entry_price) * 100

        pnl_difference = alt_pnl - base_pnl
        pnl_diff_pct = ((alt_pnl / base_pnl) - 1) * 100 if base_pnl != 0 else 0

        # Save scenario
        with self.db.get_db() as session:
            ticker = session.query(Ticker).filter(Ticker.symbol == ticker_symbol.upper()).first()
            if not ticker:
                ticker = Ticker(symbol=ticker_symbol.upper(), name=ticker_symbol.upper())
                session.add(ticker)
                session.flush()

            scenario = WhatIfScenario(
                user_id=user_id,
                ticker_id=ticker.id,
                scenario_name=scenario_name or f"Entry timing: {ticker_symbol}",
                scenario_type="entry_timing",
                base_date=base_entry_date,
                base_price=base_entry_price,
                alternative_entry_date=alternative_entry_date,
                alternative_entry_price=alt_entry_price,
                base_pnl=base_pnl,
                alternative_pnl=alt_pnl,
                pnl_difference=pnl_difference,
                pnl_difference_pct=pnl_diff_pct,
                description=f"What if I entered on {alternative_entry_date.date()} instead of {base_entry_date.date()}?",
                results_data=json.dumps({
                    "exit_price": float(exit_price),
                    "exit_date": exit_date.isoformat(),
                    "position_size": position_size,
                    "base_pnl_pct": base_pnl_pct,
                    "alt_pnl_pct": alt_pnl_pct
                })
            )
            session.add(scenario)
            session.commit()
            session.refresh(scenario)

            return {
                "scenario_id": scenario.id,
                "scenario_type": "entry_timing",
                "ticker": ticker_symbol,
                "base_scenario": {
                    "entry_date": base_entry_date.isoformat(),
                    "entry_price": base_entry_price,
                    "exit_date": exit_date.isoformat(),
                    "exit_price": float(exit_price),
                    "pnl": base_pnl,
                    "pnl_pct": base_pnl_pct
                },
                "alternative_scenario": {
                    "entry_date": alternative_entry_date.isoformat(),
                    "entry_price": float(alt_entry_price),
                    "exit_date": exit_date.isoformat(),
                    "exit_price": float(exit_price),
                    "pnl": alt_pnl,
                    "pnl_pct": alt_pnl_pct
                },
                "comparison": {
                    "pnl_difference": pnl_difference,
                    "pnl_difference_pct": pnl_diff_pct,
                    "better_scenario": "alternative" if alt_pnl > base_pnl else "base",
                    "improvement": pnl_difference if alt_pnl > base_pnl else -pnl_difference
                }
            }

    async def analyze_exit_timing(
        self,
        user_id: str,
        ticker_symbol: str,
        entry_date: datetime,
        entry_price: float,
        base_exit_date: datetime,
        alternative_exit_date: datetime,
        position_size: int = 100,
        scenario_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Compare different exit timings

        Args:
            user_id: User identifier
            ticker_symbol: Stock ticker
            entry_date: Entry date
            entry_price: Entry price
            base_exit_date: Original exit date
            alternative_exit_date: Alternative exit date
            position_size: Number of shares
            scenario_name: Optional scenario name

        Returns:
            Comparison results
        """
        # Fetch historical data
        data = await self._fetch_price_data(ticker_symbol, entry_date, alternative_exit_date)

        # Find exit prices
        base_exit_idx = (data['timestamp'] - base_exit_date).abs().idxmin()
        base_exit_price = data.loc[base_exit_idx, 'close']

        alt_exit_idx = (data['timestamp'] - alternative_exit_date).abs().idxmin()
        alt_exit_price = data.loc[alt_exit_idx, 'close']

        # Calculate P&L for both scenarios
        base_pnl = (base_exit_price - entry_price) * position_size
        base_pnl_pct = ((base_exit_price - entry_price) / entry_price) * 100

        alt_pnl = (alt_exit_price - entry_price) * position_size
        alt_pnl_pct = ((alt_exit_price - entry_price) / entry_price) * 100

        pnl_difference = alt_pnl - base_pnl
        pnl_diff_pct = ((alt_pnl / base_pnl) - 1) * 100 if base_pnl != 0 else 0

        # Save scenario
        with self.db.get_db() as session:
            ticker = session.query(Ticker).filter(Ticker.symbol == ticker_symbol.upper()).first()
            if not ticker:
                ticker = Ticker(symbol=ticker_symbol.upper(), name=ticker_symbol.upper())
                session.add(ticker)
                session.flush()

            scenario = WhatIfScenario(
                user_id=user_id,
                ticker_id=ticker.id,
                scenario_name=scenario_name or f"Exit timing: {ticker_symbol}",
                scenario_type="exit_timing",
                base_date=base_exit_date,
                base_price=base_exit_price,
                alternative_exit_date=alternative_exit_date,
                alternative_exit_price=alt_exit_price,
                base_pnl=base_pnl,
                alternative_pnl=alt_pnl,
                pnl_difference=pnl_difference,
                pnl_difference_pct=pnl_diff_pct,
                description=f"What if I held until {alternative_exit_date.date()} instead of {base_exit_date.date()}?",
                results_data=json.dumps({
                    "entry_price": entry_price,
                    "entry_date": entry_date.isoformat(),
                    "position_size": position_size,
                    "base_pnl_pct": base_pnl_pct,
                    "alt_pnl_pct": alt_pnl_pct
                })
            )
            session.add(scenario)
            session.commit()
            session.refresh(scenario)

            return {
                "scenario_id": scenario.id,
                "scenario_type": "exit_timing",
                "ticker": ticker_symbol,
                "base_scenario": {
                    "exit_date": base_exit_date.isoformat(),
                    "exit_price": float(base_exit_price),
                    "pnl": base_pnl,
                    "pnl_pct": base_pnl_pct
                },
                "alternative_scenario": {
                    "exit_date": alternative_exit_date.isoformat(),
                    "exit_price": float(alt_exit_price),
                    "pnl": alt_pnl,
                    "pnl_pct": alt_pnl_pct
                },
                "comparison": {
                    "pnl_difference": pnl_difference,
                    "pnl_difference_pct": pnl_diff_pct,
                    "better_scenario": "alternative" if alt_pnl > base_pnl else "base",
                    "improvement": pnl_difference if alt_pnl > base_pnl else -pnl_difference
                }
            }

    async def analyze_position_size(
        self,
        user_id: str,
        ticker_symbol: str,
        entry_date: datetime,
        entry_price: float,
        exit_date: datetime,
        exit_price: float,
        base_position_size: int,
        alternative_position_size: int,
        scenario_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Compare different position sizes

        Args:
            user_id: User identifier
            ticker_symbol: Stock ticker
            entry_date: Entry date
            entry_price: Entry price
            exit_date: Exit date
            exit_price: Exit price
            base_position_size: Original position size
            alternative_position_size: Alternative position size
            scenario_name: Optional scenario name

        Returns:
            Comparison results
        """
        # Calculate P&L for both scenarios
        base_pnl = (exit_price - entry_price) * base_position_size
        base_pnl_pct = ((exit_price - entry_price) / entry_price) * 100

        alt_pnl = (exit_price - entry_price) * alternative_position_size
        alt_pnl_pct = base_pnl_pct  # Same percentage, different dollar amount

        pnl_difference = alt_pnl - base_pnl
        pnl_diff_pct = ((alt_pnl / base_pnl) - 1) * 100 if base_pnl != 0 else 0

        # Save scenario
        with self.db.get_db() as session:
            ticker = session.query(Ticker).filter(Ticker.symbol == ticker_symbol.upper()).first()
            if not ticker:
                ticker = Ticker(symbol=ticker_symbol.upper(), name=ticker_symbol.upper())
                session.add(ticker)
                session.flush()

            scenario = WhatIfScenario(
                user_id=user_id,
                ticker_id=ticker.id,
                scenario_name=scenario_name or f"Position size: {ticker_symbol}",
                scenario_type="position_size",
                base_date=entry_date,
                base_price=entry_price,
                alternative_position_size=alternative_position_size,
                base_pnl=base_pnl,
                alternative_pnl=alt_pnl,
                pnl_difference=pnl_difference,
                pnl_difference_pct=pnl_diff_pct,
                description=f"What if I traded {alternative_position_size} shares instead of {base_position_size}?",
                results_data=json.dumps({
                    "entry_price": entry_price,
                    "exit_price": exit_price,
                    "base_position_size": base_position_size,
                    "alternative_position_size": alternative_position_size,
                    "base_pnl_pct": base_pnl_pct,
                    "alt_pnl_pct": alt_pnl_pct
                })
            )
            session.add(scenario)
            session.commit()
            session.refresh(scenario)

            return {
                "scenario_id": scenario.id,
                "scenario_type": "position_size",
                "ticker": ticker_symbol,
                "base_scenario": {
                    "position_size": base_position_size,
                    "pnl": base_pnl,
                    "pnl_pct": base_pnl_pct,
                    "capital_required": entry_price * base_position_size
                },
                "alternative_scenario": {
                    "position_size": alternative_position_size,
                    "pnl": alt_pnl,
                    "pnl_pct": alt_pnl_pct,
                    "capital_required": entry_price * alternative_position_size
                },
                "comparison": {
                    "pnl_difference": pnl_difference,
                    "better_scenario": "alternative" if alt_pnl > base_pnl else "base",
                    "size_increase_pct": ((alternative_position_size / base_position_size) - 1) * 100
                }
            }

    async def analyze_stop_loss(
        self,
        user_id: str,
        ticker_symbol: str,
        entry_date: datetime,
        entry_price: float,
        exit_date: datetime,
        base_stop_loss: float,
        alternative_stop_loss: float,
        position_size: int = 100,
        scenario_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Compare different stop loss levels

        Args:
            user_id: User identifier
            ticker_symbol: Stock ticker
            entry_date: Entry date
            entry_price: Entry price
            exit_date: Observation end date
            base_stop_loss: Original stop loss price
            alternative_stop_loss: Alternative stop loss price
            position_size: Number of shares
            scenario_name: Optional scenario name

        Returns:
            Comparison results including whether stops were hit
        """
        # Fetch historical data
        data = await self._fetch_price_data(ticker_symbol, entry_date, exit_date)

        # Check if stops were hit
        base_stop_hit = (data['low'] <= base_stop_loss).any()
        alt_stop_hit = (data['low'] <= alternative_stop_loss).any()

        # Find when stops were hit
        base_exit_price = base_stop_loss if base_stop_hit else data.iloc[-1]['close']
        alt_exit_price = alternative_stop_loss if alt_stop_hit else data.iloc[-1]['close']

        # Calculate P&L
        base_pnl = (base_exit_price - entry_price) * position_size
        base_pnl_pct = ((base_exit_price - entry_price) / entry_price) * 100

        alt_pnl = (alt_exit_price - entry_price) * position_size
        alt_pnl_pct = ((alt_exit_price - entry_price) / entry_price) * 100

        pnl_difference = alt_pnl - base_pnl

        # Calculate risk metrics
        base_risk = abs(entry_price - base_stop_loss) * position_size
        alt_risk = abs(entry_price - alternative_stop_loss) * position_size

        # Save scenario
        with self.db.get_db() as session:
            ticker = session.query(Ticker).filter(Ticker.symbol == ticker_symbol.upper()).first()
            if not ticker:
                ticker = Ticker(symbol=ticker_symbol.upper(), name=ticker_symbol.upper())
                session.add(ticker)
                session.flush()

            scenario = WhatIfScenario(
                user_id=user_id,
                ticker_id=ticker.id,
                scenario_name=scenario_name or f"Stop loss: {ticker_symbol}",
                scenario_type="stop_loss",
                base_date=entry_date,
                base_price=entry_price,
                alternative_stop_loss=alternative_stop_loss,
                base_pnl=base_pnl,
                alternative_pnl=alt_pnl,
                pnl_difference=pnl_difference,
                description=f"What if I used ${alternative_stop_loss:.2f} stop instead of ${base_stop_loss:.2f}?",
                results_data=json.dumps({
                    "entry_price": entry_price,
                    "base_stop_hit": base_stop_hit,
                    "alt_stop_hit": alt_stop_hit,
                    "base_exit_price": float(base_exit_price),
                    "alt_exit_price": float(alt_exit_price),
                    "base_risk": base_risk,
                    "alt_risk": alt_risk,
                    "position_size": position_size
                })
            )
            session.add(scenario)
            session.commit()
            session.refresh(scenario)

            return {
                "scenario_id": scenario.id,
                "scenario_type": "stop_loss",
                "ticker": ticker_symbol,
                "base_scenario": {
                    "stop_loss": base_stop_loss,
                    "stop_hit": base_stop_hit,
                    "exit_price": float(base_exit_price),
                    "pnl": base_pnl,
                    "pnl_pct": base_pnl_pct,
                    "risk_amount": base_risk
                },
                "alternative_scenario": {
                    "stop_loss": alternative_stop_loss,
                    "stop_hit": alt_stop_hit,
                    "exit_price": float(alt_exit_price),
                    "pnl": alt_pnl,
                    "pnl_pct": alt_pnl_pct,
                    "risk_amount": alt_risk
                },
                "comparison": {
                    "pnl_difference": pnl_difference,
                    "risk_difference": alt_risk - base_risk,
                    "better_scenario": "alternative" if alt_pnl > base_pnl else "base",
                    "recommendation": self._get_stop_recommendation(
                        base_stop_hit, alt_stop_hit, base_pnl, alt_pnl
                    )
                }
            }

    def _get_stop_recommendation(
        self,
        base_hit: bool,
        alt_hit: bool,
        base_pnl: float,
        alt_pnl: float
    ) -> str:
        """Generate recommendation based on stop loss analysis"""
        if base_hit and not alt_hit:
            return "Wider stop (alternative) avoided stop-out and improved outcome"
        elif alt_hit and not base_hit:
            return "Tighter stop (base) avoided larger loss"
        elif base_pnl > alt_pnl:
            return "Base stop level performed better"
        else:
            return "Alternative stop level performed better"

    async def get_scenario(self, scenario_id: int) -> Dict[str, Any]:
        """Get a saved scenario by ID"""
        with self.db.get_db() as session:
            scenario = session.get(WhatIfScenario, scenario_id)
            if not scenario:
                raise ValueError(f"Scenario {scenario_id} not found")

            ticker = session.get(Ticker, scenario.ticker_id)

            return {
                "scenario_id": scenario.id,
                "user_id": scenario.user_id,
                "ticker": ticker.symbol if ticker else "UNKNOWN",
                "scenario_name": scenario.scenario_name,
                "scenario_type": scenario.scenario_type,
                "description": scenario.description,
                "base_pnl": scenario.base_pnl,
                "alternative_pnl": scenario.alternative_pnl,
                "pnl_difference": scenario.pnl_difference,
                "pnl_difference_pct": scenario.pnl_difference_pct,
                "results_data": json.loads(scenario.results_data) if scenario.results_data else None,
                "created_at": scenario.created_at.isoformat()
            }

    async def list_scenarios(
        self,
        user_id: str,
        scenario_type: Optional[str] = None,
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        """List scenarios for a user"""
        with self.db.get_db() as session:
            query = session.query(WhatIfScenario).filter(
                WhatIfScenario.user_id == user_id
            )

            if scenario_type:
                query = query.filter(WhatIfScenario.scenario_type == scenario_type)

            scenarios = query.order_by(WhatIfScenario.created_at.desc()).limit(limit).all()

            result = []
            for scenario in scenarios:
                ticker = session.get(Ticker, scenario.ticker_id)
                result.append({
                    "scenario_id": scenario.id,
                    "ticker": ticker.symbol if ticker else "UNKNOWN",
                    "scenario_name": scenario.scenario_name,
                    "scenario_type": scenario.scenario_type,
                    "pnl_difference": scenario.pnl_difference,
                    "pnl_difference_pct": scenario.pnl_difference_pct,
                    "created_at": scenario.created_at.isoformat()
                })

            return result

    async def _fetch_price_data(
        self,
        ticker: str,
        start_date: datetime,
        end_date: datetime
    ) -> pd.DataFrame:
        """Fetch and prepare historical price data"""
        # Calculate required bars
        days_diff = (end_date - start_date).days
        outputsize = max(100, min(5000, days_diff + 50))

        # Fetch from market data service
        data = await self.market_data.get_time_series(
            ticker=ticker,
            interval="1day",
            outputsize=outputsize
        )

        # Convert to DataFrame
        df = pd.DataFrame({
            'timestamp': pd.to_datetime(data['t'], unit='s'),
            'open': data['o'],
            'high': data['h'],
            'low': data['l'],
            'close': data['c'],
            'volume': data['v']
        })

        # Filter to date range
        df = df[(df['timestamp'] >= start_date) & (df['timestamp'] <= end_date)]
        df = df.sort_values('timestamp').reset_index(drop=True)

        return df
