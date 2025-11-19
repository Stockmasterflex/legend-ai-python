"""
Pattern Validation Service
Tracks pattern accuracy, win/loss rates, and performance metrics
"""

from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from sqlalchemy import select, func, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import PatternScan, Ticker
from app.services.database import DatabaseService
from app.services.market_data import MarketDataService


class PatternValidationService:
    """
    Tracks and validates pattern detection accuracy
    """

    def __init__(self):
        self.db_service = DatabaseService()
        self.market_service = MarketDataService()

    async def record_pattern_outcome(
        self,
        scan_id: int,
        outcome: str,
        outcome_price: float,
        actual_gain_loss: float,
        notes: Optional[str] = None
    ):
        """
        Record the actual outcome of a pattern prediction

        Args:
            scan_id: Pattern scan ID
            outcome: 'hit_target', 'hit_stop', 'expired', 'partial'
            outcome_price: Price at outcome
            actual_gain_loss: Actual percentage gain/loss
            notes: Optional notes about the outcome
        """
        async with self.db_service.get_session() as session:
            # Find the pattern scan
            result = await session.execute(
                select(PatternScan).where(PatternScan.id == scan_id)
            )
            scan = result.scalar_one_or_none()

            if not scan:
                raise ValueError(f"Pattern scan {scan_id} not found")

            # Update with outcome
            scan.actual_outcome = outcome
            scan.outcome_date = datetime.utcnow()
            scan.outcome_price = outcome_price
            scan.actual_gain_loss = actual_gain_loss
            scan.was_successful = outcome in ['hit_target', 'partial']

            await session.commit()

    async def auto_validate_patterns(self, lookback_days: int = 30):
        """
        Automatically validate patterns by checking if targets/stops were hit

        Args:
            lookback_days: How many days back to check

        Returns:
            Number of patterns validated
        """
        cutoff_date = datetime.utcnow() - timedelta(days=lookback_days)

        async with self.db_service.get_session() as session:
            # Get unvalidated patterns from the lookback period
            result = await session.execute(
                select(PatternScan)
                .join(Ticker)
                .where(
                    and_(
                        PatternScan.scanned_at >= cutoff_date,
                        PatternScan.actual_outcome == None
                    )
                )
            )

            scans = result.scalars().all()

            validated_count = 0

            for scan in scans:
                # Get price data since pattern detection
                try:
                    df = await self.market_service.get_time_series(
                        scan.ticker.symbol,
                        interval="1d",
                        outputsize=lookback_days
                    )

                    if df is None or df.empty:
                        continue

                    # Filter to data after pattern detection
                    df = df[df.index >= scan.scanned_at]

                    if df.empty:
                        continue

                    # Check if target or stop was hit
                    target_hit = (df['high'] >= scan.target_price).any()
                    stop_hit = (df['low'] <= scan.stop_loss).any()

                    if target_hit and stop_hit:
                        # Both hit - check which came first
                        target_date = df[df['high'] >= scan.target_price].index[0]
                        stop_date = df[df['low'] <= scan.stop_loss].index[0]

                        if target_date < stop_date:
                            outcome = 'hit_target'
                            outcome_price = scan.target_price
                            gain_loss = ((scan.target_price - scan.entry_price) / scan.entry_price) * 100
                        else:
                            outcome = 'hit_stop'
                            outcome_price = scan.stop_loss
                            gain_loss = ((scan.stop_loss - scan.entry_price) / scan.entry_price) * 100

                    elif target_hit:
                        outcome = 'hit_target'
                        outcome_price = scan.target_price
                        gain_loss = ((scan.target_price - scan.entry_price) / scan.entry_price) * 100

                    elif stop_hit:
                        outcome = 'hit_stop'
                        outcome_price = scan.stop_loss
                        gain_loss = ((scan.stop_loss - scan.entry_price) / scan.entry_price) * 100

                    else:
                        # Neither hit yet - check if expired (30+ days old)
                        age_days = (datetime.utcnow() - scan.scanned_at).days
                        if age_days >= 30:
                            outcome = 'expired'
                            latest_price = df['close'].iloc[-1]
                            outcome_price = latest_price
                            gain_loss = ((latest_price - scan.entry_price) / scan.entry_price) * 100
                        else:
                            # Still active, skip
                            continue

                    # Record outcome
                    scan.actual_outcome = outcome
                    scan.outcome_date = datetime.utcnow()
                    scan.outcome_price = outcome_price
                    scan.actual_gain_loss = gain_loss
                    scan.was_successful = outcome == 'hit_target'

                    validated_count += 1

                except Exception as e:
                    print(f"Error validating scan {scan.id}: {e}")
                    continue

            await session.commit()

            return validated_count

    async def get_pattern_performance(
        self,
        pattern_type: Optional[str] = None,
        min_samples: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Get performance metrics for each pattern type

        Args:
            pattern_type: Filter by specific pattern (optional)
            min_samples: Minimum number of samples to include pattern

        Returns:
            List of pattern performance metrics
        """
        async with self.db_service.get_session() as session:
            # Query for patterns with outcomes
            query = select(
                PatternScan.pattern_type,
                func.count(PatternScan.id).label('total_count'),
                func.sum(func.cast(PatternScan.was_successful, func.Integer())).label('successful_count'),
                func.avg(PatternScan.actual_gain_loss).label('avg_gain_loss'),
                func.avg(PatternScan.score).label('avg_confidence'),
                func.max(PatternScan.actual_gain_loss).label('max_gain'),
                func.min(PatternScan.actual_gain_loss).label('max_loss')
            ).where(
                PatternScan.actual_outcome != None
            )

            if pattern_type:
                query = query.where(PatternScan.pattern_type == pattern_type)

            query = query.group_by(PatternScan.pattern_type)

            result = await session.execute(query)
            rows = result.all()

            performance = []
            for row in rows:
                if row.total_count < min_samples:
                    continue

                win_rate = (row.successful_count / row.total_count * 100) if row.total_count > 0 else 0

                performance.append({
                    'pattern_type': row.pattern_type,
                    'total_trades': row.total_count,
                    'wins': row.successful_count or 0,
                    'losses': row.total_count - (row.successful_count or 0),
                    'win_rate': round(win_rate, 2),
                    'avg_gain_loss': round(row.avg_gain_loss or 0, 2),
                    'avg_confidence': round(row.avg_confidence or 0, 2),
                    'max_gain': round(row.max_gain or 0, 2),
                    'max_loss': round(row.max_loss or 0, 2),
                    'status': self._get_pattern_status(win_rate, row.total_count)
                })

            # Sort by win rate
            performance.sort(key=lambda x: x['win_rate'], reverse=True)

            return performance

    def _get_pattern_status(self, win_rate: float, sample_size: int) -> str:
        """Determine pattern status based on performance"""
        if sample_size < 10:
            return 'testing'  # Not enough data
        elif win_rate >= 60:
            return 'excellent'
        elif win_rate >= 50:
            return 'good'
        elif win_rate >= 40:
            return 'acceptable'
        else:
            return 'poor'

    async def get_patterns_to_disable(self, min_samples: int = 20, max_win_rate: float = 35.0) -> List[str]:
        """
        Get list of pattern types that should be disabled due to poor performance

        Args:
            min_samples: Minimum trades to consider disabling
            max_win_rate: Maximum win rate threshold

        Returns:
            List of pattern types to disable
        """
        performance = await self.get_pattern_performance(min_samples=min_samples)

        to_disable = [
            p['pattern_type']
            for p in performance
            if p['win_rate'] < max_win_rate and p['total_trades'] >= min_samples
        ]

        return to_disable

    async def get_pattern_leaderboard(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get top performing patterns"""
        performance = await self.get_pattern_performance()
        return performance[:limit]

    async def get_recent_validations(self, days: int = 7, limit: int = 50) -> List[Dict[str, Any]]:
        """Get recently validated patterns"""
        cutoff = datetime.utcnow() - timedelta(days=days)

        async with self.db_service.get_session() as session:
            result = await session.execute(
                select(PatternScan)
                .join(Ticker)
                .where(
                    and_(
                        PatternScan.outcome_date != None,
                        PatternScan.outcome_date >= cutoff
                    )
                )
                .order_by(PatternScan.outcome_date.desc())
                .limit(limit)
            )

            scans = result.scalars().all()

            validations = []
            for scan in scans:
                validations.append({
                    'id': scan.id,
                    'ticker': scan.ticker.symbol,
                    'pattern_type': scan.pattern_type,
                    'scanned_at': scan.scanned_at.isoformat(),
                    'outcome': scan.actual_outcome,
                    'outcome_date': scan.outcome_date.isoformat(),
                    'entry_price': scan.entry_price,
                    'target_price': scan.target_price,
                    'stop_loss': scan.stop_loss,
                    'outcome_price': scan.outcome_price,
                    'gain_loss': round(scan.actual_gain_loss, 2),
                    'was_successful': scan.was_successful,
                    'confidence': scan.score
                })

            return validations

    async def backtest_pattern(
        self,
        pattern_type: str,
        ticker_symbol: str,
        start_date: datetime,
        end_date: datetime
    ) -> Dict[str, Any]:
        """
        Backtest a pattern on historical data

        Args:
            pattern_type: Pattern to test
            ticker_symbol: Ticker symbol
            start_date: Start of backtest period
            end_date: End of backtest period

        Returns:
            Backtest results
        """
        # This would integrate with the pattern detectors
        # For now, return structure
        return {
            'pattern_type': pattern_type,
            'ticker': ticker_symbol,
            'period': {
                'start': start_date.isoformat(),
                'end': end_date.isoformat()
            },
            'results': {
                'total_signals': 0,
                'winning_trades': 0,
                'losing_trades': 0,
                'win_rate': 0.0,
                'avg_gain': 0.0,
                'avg_loss': 0.0,
                'max_drawdown': 0.0,
                'profit_factor': 0.0
            }
        }

    async def get_validation_summary(self) -> Dict[str, Any]:
        """Get overall validation statistics"""
        async with self.db_service.get_session() as session:
            # Total patterns detected
            total_result = await session.execute(
                select(func.count(PatternScan.id))
            )
            total_patterns = total_result.scalar()

            # Validated patterns
            validated_result = await session.execute(
                select(func.count(PatternScan.id))
                .where(PatternScan.actual_outcome != None)
            )
            validated_count = validated_result.scalar()

            # Success rate
            success_result = await session.execute(
                select(func.count(PatternScan.id))
                .where(PatternScan.was_successful == True)
            )
            success_count = success_result.scalar()

            validation_rate = (validated_count / total_patterns * 100) if total_patterns > 0 else 0
            success_rate = (success_count / validated_count * 100) if validated_count > 0 else 0

            # Average gain/loss
            avg_result = await session.execute(
                select(func.avg(PatternScan.actual_gain_loss))
                .where(PatternScan.actual_gain_loss != None)
            )
            avg_gain_loss = avg_result.scalar() or 0

            return {
                'total_patterns': total_patterns,
                'validated_patterns': validated_count,
                'unvalidated_patterns': total_patterns - validated_count,
                'validation_rate': round(validation_rate, 2),
                'successful_patterns': success_count,
                'failed_patterns': validated_count - success_count,
                'success_rate': round(success_rate, 2),
                'avg_gain_loss': round(avg_gain_loss, 2)
            }
