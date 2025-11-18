"""
Risk Analytics Service
Handles correlation matrix, diversification scores, position sizing, and portfolio heat
"""

from typing import List, Dict, Optional, Tuple
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
import logging
import numpy as np
import pandas as pd
from scipy.stats import pearsonr

from app.models import Portfolio, Position, Ticker
from app.services.market_data import get_historical_data

logger = logging.getLogger(__name__)


class RiskAnalyticsService:
    """Service for advanced risk analytics"""

    def __init__(self, db: Session):
        self.db = db

    async def calculate_position_size(
        self,
        portfolio_id: int,
        symbol: str,
        entry_price: float,
        stop_loss: float,
        risk_percent: float = 2.0,
        use_kelly: bool = False,
        win_rate: Optional[float] = None,
        avg_win_loss_ratio: Optional[float] = None
    ) -> Dict:
        """
        Calculate optimal position size based on risk parameters

        Args:
            portfolio_id: Portfolio ID
            symbol: Stock symbol
            entry_price: Intended entry price
            stop_loss: Stop loss price
            risk_percent: Risk per trade as % of portfolio (default 2%)
            use_kelly: Use Kelly Criterion for sizing
            win_rate: Historical win rate (required for Kelly)
            avg_win_loss_ratio: Average win/loss ratio (required for Kelly)

        Returns:
            Position sizing recommendations
        """
        portfolio = self.db.query(Portfolio).filter(Portfolio.id == portfolio_id).first()
        if not portfolio:
            raise ValueError(f"Portfolio {portfolio_id} not found")

        # Calculate risk per share
        risk_per_share = abs(entry_price - stop_loss)
        if risk_per_share == 0:
            raise ValueError("Stop loss must be different from entry price")

        # Calculate dollar risk
        portfolio_value = portfolio.total_value or portfolio.initial_capital
        dollar_risk = (risk_percent / 100) * portfolio_value

        # Basic position sizing (2% rule)
        shares_2pct = int(dollar_risk / risk_per_share)
        position_value_2pct = shares_2pct * entry_price
        position_pct_2pct = (position_value_2pct / portfolio_value) * 100

        result = {
            "symbol": symbol,
            "entry_price": entry_price,
            "stop_loss": stop_loss,
            "risk_per_share": risk_per_share,
            "risk_percent": risk_percent,
            "portfolio_value": portfolio_value,
            "dollar_risk": dollar_risk,
            "recommended_shares_2pct": shares_2pct,
            "position_value": position_value_2pct,
            "position_pct": position_pct_2pct
        }

        # Kelly Criterion calculation
        if use_kelly and win_rate and avg_win_loss_ratio:
            # Kelly % = W - [(1 - W) / R]
            # Where W = win rate, R = average win/loss ratio
            kelly_pct = win_rate - ((1 - win_rate) / avg_win_loss_ratio)

            # Apply safety factor (use half-Kelly for safety)
            kelly_pct_safe = kelly_pct * 0.5

            # Ensure Kelly doesn't exceed reasonable limits
            kelly_pct_capped = min(max(kelly_pct_safe, 0), 0.25)  # Cap at 25%

            dollar_risk_kelly = kelly_pct_capped * portfolio_value
            shares_kelly = int(dollar_risk_kelly / risk_per_share)
            position_value_kelly = shares_kelly * entry_price

            result["kelly_criterion"] = {
                "kelly_pct": round(kelly_pct * 100, 2),
                "kelly_pct_safe": round(kelly_pct_safe * 100, 2),
                "kelly_pct_capped": round(kelly_pct_capped * 100, 2),
                "recommended_shares": shares_kelly,
                "position_value": position_value_kelly,
                "position_pct": round((position_value_kelly / portfolio_value) * 100, 2)
            }

        # Conservative and aggressive alternatives
        result["alternatives"] = {
            "conservative_1pct": {
                "risk_pct": 1.0,
                "shares": int((0.01 * portfolio_value) / risk_per_share),
                "position_value": int((0.01 * portfolio_value) / risk_per_share) * entry_price
            },
            "aggressive_3pct": {
                "risk_pct": 3.0,
                "shares": int((0.03 * portfolio_value) / risk_per_share),
                "position_value": int((0.03 * portfolio_value) / risk_per_share) * entry_price
            }
        }

        return result

    async def calculate_portfolio_heat(self, portfolio_id: int) -> Dict:
        """
        Calculate portfolio heat (total risk exposure)

        Portfolio heat = sum of all position risks
        """
        portfolio = self.db.query(Portfolio).filter(Portfolio.id == portfolio_id).first()
        if not portfolio:
            raise ValueError(f"Portfolio {portfolio_id} not found")

        positions = self.db.query(Position).filter(
            Position.portfolio_id == portfolio_id,
            Position.status == "open"
        ).all()

        portfolio_value = portfolio.total_value or portfolio.initial_capital
        total_heat = 0
        position_risks = []

        for position in positions:
            if position.stop_loss and position.current_price:
                # Calculate risk per position
                risk_per_share = abs(position.current_price - position.stop_loss)
                total_position_risk = risk_per_share * position.quantity
                risk_pct = (total_position_risk / portfolio_value) * 100

                total_heat += risk_pct

                ticker = self.db.query(Ticker).filter(Ticker.id == position.ticker_id).first()
                position_risks.append({
                    "symbol": ticker.symbol,
                    "quantity": position.quantity,
                    "current_price": position.current_price,
                    "stop_loss": position.stop_loss,
                    "risk_per_share": risk_per_share,
                    "total_risk_dollar": total_position_risk,
                    "risk_pct": round(risk_pct, 2)
                })

        # Determine risk level
        if total_heat < 6:
            risk_level = "LOW"
            recommendation = "Portfolio heat is healthy. You have room for additional positions."
        elif total_heat < 10:
            risk_level = "MODERATE"
            recommendation = "Portfolio heat is elevated. Be cautious with new positions."
        elif total_heat < 15:
            risk_level = "HIGH"
            recommendation = "Portfolio heat is high. Avoid new positions until some close."
        else:
            risk_level = "CRITICAL"
            recommendation = "Portfolio heat is critical! Consider reducing position sizes."

        return {
            "total_heat_pct": round(total_heat, 2),
            "risk_level": risk_level,
            "recommendation": recommendation,
            "num_positions": len(positions),
            "position_risks": position_risks,
            "max_recommended_heat": 10.0
        }

    async def calculate_correlation_matrix(
        self,
        portfolio_id: int,
        period_days: int = 60
    ) -> Dict:
        """
        Calculate correlation matrix for portfolio positions

        Args:
            portfolio_id: Portfolio ID
            period_days: Historical period for correlation calculation

        Returns:
            Correlation matrix and analysis
        """
        positions = self.db.query(Position).filter(
            Position.portfolio_id == portfolio_id,
            Position.status == "open"
        ).all()

        if len(positions) < 2:
            return {
                "correlation_matrix": [],
                "symbols": [],
                "note": "Need at least 2 positions to calculate correlations"
            }

        # Get symbols
        symbols = []
        for position in positions:
            ticker = self.db.query(Ticker).filter(Ticker.id == position.ticker_id).first()
            symbols.append(ticker.symbol)

        # Fetch historical data for all symbols
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=period_days)

        price_data = {}
        for symbol in symbols:
            try:
                data = await get_historical_data(
                    symbol,
                    start_date.strftime("%Y-%m-%d"),
                    end_date.strftime("%Y-%m-%d")
                )
                if data and len(data) > 0:
                    df = pd.DataFrame(data)
                    price_data[symbol] = df['close'].values
            except Exception as e:
                logger.warning(f"Failed to get data for {symbol}: {e}")

        # Create returns DataFrame
        returns_data = {}
        min_length = min([len(v) for v in price_data.values()]) if price_data else 0

        if min_length < 10:
            return {
                "correlation_matrix": [],
                "symbols": symbols,
                "note": "Insufficient historical data for correlation calculation"
            }

        for symbol, prices in price_data.items():
            # Truncate to minimum length
            prices_truncated = prices[-min_length:]
            returns = np.diff(prices_truncated) / prices_truncated[:-1]
            returns_data[symbol] = returns

        # Calculate correlation matrix
        df_returns = pd.DataFrame(returns_data)
        corr_matrix = df_returns.corr()

        # Convert to list format
        correlation_matrix = corr_matrix.values.tolist()

        # Find highly correlated pairs
        high_correlations = []
        for i in range(len(symbols)):
            for j in range(i + 1, len(symbols)):
                corr = corr_matrix.iloc[i, j]
                if abs(corr) > 0.7:
                    high_correlations.append({
                        "symbol1": symbols[i],
                        "symbol2": symbols[j],
                        "correlation": round(corr, 3),
                        "warning": "High correlation" if corr > 0.7 else "High negative correlation"
                    })

        # Calculate average absolute correlation
        avg_correlation = np.mean(np.abs(corr_matrix.values[np.triu_indices_from(corr_matrix.values, k=1)]))

        return {
            "symbols": symbols,
            "correlation_matrix": [[round(v, 3) for v in row] for row in correlation_matrix],
            "high_correlations": high_correlations,
            "avg_correlation": round(avg_correlation, 3),
            "diversification_note": "Lower average correlation indicates better diversification"
        }

    async def calculate_diversification_score(self, portfolio_id: int) -> Dict:
        """
        Calculate portfolio diversification score (0-100)

        Factors:
        - Number of positions (more is better, up to a point)
        - Sector diversity
        - Correlation between positions
        - Position size concentration
        """
        positions = self.db.query(Position).filter(
            Position.portfolio_id == portfolio_id,
            Position.status == "open"
        ).all()

        if len(positions) == 0:
            return {
                "score": 0,
                "grade": "F",
                "factors": {},
                "note": "No open positions"
            }

        score = 0
        factors = {}

        # Factor 1: Number of positions (0-25 points)
        num_positions = len(positions)
        if num_positions >= 10:
            position_score = 25
        elif num_positions >= 5:
            position_score = 20
        elif num_positions >= 3:
            position_score = 15
        else:
            position_score = num_positions * 5

        score += position_score
        factors["num_positions"] = {
            "value": num_positions,
            "score": position_score,
            "max_score": 25
        }

        # Factor 2: Sector diversity (0-25 points)
        sectors = set()
        for position in positions:
            ticker = self.db.query(Ticker).filter(Ticker.id == position.ticker_id).first()
            if ticker and ticker.sector:
                sectors.add(ticker.sector)

        num_sectors = len(sectors)
        if num_sectors >= 5:
            sector_score = 25
        elif num_sectors >= 3:
            sector_score = 20
        elif num_sectors >= 2:
            sector_score = 15
        else:
            sector_score = 10

        score += sector_score
        factors["sector_diversity"] = {
            "num_sectors": num_sectors,
            "score": sector_score,
            "max_score": 25
        }

        # Factor 3: Position size concentration (0-25 points)
        # Lower concentration is better
        position_sizes = [p.position_size_pct or 0 for p in positions if p.position_size_pct]
        if position_sizes:
            max_position_size = max(position_sizes)
            if max_position_size < 15:
                concentration_score = 25
            elif max_position_size < 25:
                concentration_score = 20
            elif max_position_size < 35:
                concentration_score = 15
            else:
                concentration_score = 10
        else:
            concentration_score = 15

        score += concentration_score
        factors["concentration"] = {
            "max_position_pct": round(max(position_sizes), 2) if position_sizes else 0,
            "score": concentration_score,
            "max_score": 25
        }

        # Factor 4: Correlation (0-25 points)
        # Lower correlation is better
        try:
            corr_data = await self.calculate_correlation_matrix(portfolio_id)
            if "avg_correlation" in corr_data:
                avg_corr = corr_data["avg_correlation"]
                if avg_corr < 0.3:
                    correlation_score = 25
                elif avg_corr < 0.5:
                    correlation_score = 20
                elif avg_corr < 0.7:
                    correlation_score = 15
                else:
                    correlation_score = 10
            else:
                correlation_score = 15  # Default if can't calculate
        except:
            correlation_score = 15

        score += correlation_score
        factors["correlation"] = {
            "avg_correlation": round(corr_data.get("avg_correlation", 0), 3) if corr_data else 0,
            "score": correlation_score,
            "max_score": 25
        }

        # Determine grade
        if score >= 90:
            grade = "A+"
        elif score >= 85:
            grade = "A"
        elif score >= 80:
            grade = "A-"
        elif score >= 75:
            grade = "B+"
        elif score >= 70:
            grade = "B"
        elif score >= 65:
            grade = "B-"
        elif score >= 60:
            grade = "C+"
        elif score >= 55:
            grade = "C"
        else:
            grade = "D"

        return {
            "score": score,
            "grade": grade,
            "factors": factors,
            "recommendations": self._get_diversification_recommendations(factors)
        }

    def _get_diversification_recommendations(self, factors: Dict) -> List[str]:
        """Generate recommendations based on diversification factors"""
        recommendations = []

        if factors["num_positions"]["value"] < 5:
            recommendations.append("Consider adding more positions to improve diversification")

        if factors["sector_diversity"]["num_sectors"] < 3:
            recommendations.append("Diversify across more sectors to reduce sector-specific risk")

        if factors["concentration"]["max_position_pct"] > 25:
            recommendations.append("Reduce position size concentration - largest position is too big")

        if "avg_correlation" in factors["correlation"] and factors["correlation"]["avg_correlation"] > 0.6:
            recommendations.append("Positions are highly correlated - consider uncorrelated assets")

        if not recommendations:
            recommendations.append("Portfolio diversification is good!")

        return recommendations
