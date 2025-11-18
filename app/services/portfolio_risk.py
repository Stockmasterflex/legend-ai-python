"""
Portfolio Risk Measurement Service
Comprehensive risk analytics for portfolio management
"""
import logging
import numpy as np
import pandas as pd
from typing import List, Dict, Optional, Tuple, Any
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from scipy import stats
from scipy.optimize import minimize
import warnings

warnings.filterwarnings('ignore')

logger = logging.getLogger(__name__)


@dataclass
class Position:
    """Individual position in a portfolio"""
    symbol: str
    quantity: float
    entry_price: float
    current_price: float
    sector: Optional[str] = None

    # Greeks (for options or delta-adjusted positions)
    delta: float = 1.0  # 1.0 for stocks, varies for options
    gamma: float = 0.0
    vega: float = 0.0
    theta: float = 0.0

    @property
    def market_value(self) -> float:
        """Current market value of position"""
        return self.quantity * self.current_price

    @property
    def cost_basis(self) -> float:
        """Cost basis of position"""
        return self.quantity * self.entry_price

    @property
    def pnl(self) -> float:
        """Profit and loss"""
        return self.market_value - self.cost_basis

    @property
    def pnl_percent(self) -> float:
        """Profit and loss percentage"""
        if self.cost_basis == 0:
            return 0.0
        return (self.pnl / self.cost_basis) * 100


@dataclass
class Portfolio:
    """Portfolio containing multiple positions"""
    positions: List[Position]
    cash: float = 0.0
    name: str = "Portfolio"

    @property
    def total_market_value(self) -> float:
        """Total market value of all positions"""
        return sum(pos.market_value for pos in self.positions) + self.cash

    @property
    def total_cost_basis(self) -> float:
        """Total cost basis of all positions"""
        return sum(pos.cost_basis for pos in self.positions) + self.cash

    @property
    def total_pnl(self) -> float:
        """Total profit and loss"""
        return sum(pos.pnl for pos in self.positions)

    @property
    def total_pnl_percent(self) -> float:
        """Total profit and loss percentage"""
        if self.total_cost_basis == 0:
            return 0.0
        return (self.total_pnl / self.total_cost_basis) * 100

    def get_weights(self) -> Dict[str, float]:
        """Get position weights in portfolio"""
        total_value = self.total_market_value
        if total_value == 0:
            return {}
        return {
            pos.symbol: pos.market_value / total_value
            for pos in self.positions
        }


@dataclass
class VaRResult:
    """Value at Risk calculation result"""
    confidence_level: float
    var_amount: float
    var_percent: float
    method: str
    time_horizon_days: int
    portfolio_value: float
    additional_info: Dict[str, Any] = field(default_factory=dict)


@dataclass
class StressTestResult:
    """Stress test scenario result"""
    scenario_name: str
    scenario_type: str  # historical or hypothetical
    portfolio_loss: float
    portfolio_loss_percent: float
    position_impacts: Dict[str, float]
    description: str


@dataclass
class GreeksResult:
    """Portfolio Greeks result"""
    portfolio_delta: float
    portfolio_gamma: float
    portfolio_vega: float
    portfolio_theta: float
    delta_exposure: float  # Delta-adjusted exposure
    position_greeks: Dict[str, Dict[str, float]]


@dataclass
class DrawdownResult:
    """Drawdown analysis result"""
    max_drawdown: float
    max_drawdown_percent: float
    average_drawdown: float
    average_drawdown_percent: float
    current_drawdown: float
    current_drawdown_percent: float
    max_drawdown_duration_days: int
    recovery_time_days: Optional[int]
    underwater_periods: List[Dict[str, Any]]
    drawdown_series: Optional[pd.Series] = None


@dataclass
class RiskAttributionResult:
    """Risk attribution result"""
    total_risk: float
    risk_by_position: Dict[str, float]
    risk_by_sector: Dict[str, float]
    marginal_risk: Dict[str, float]
    risk_contribution_percent: Dict[str, float]
    concentration_metrics: Dict[str, Any]


class PortfolioRiskMeasurement:
    """Comprehensive portfolio risk measurement service"""

    def __init__(self):
        """Initialize portfolio risk measurement service"""
        pass

    # ==================== VALUE AT RISK ====================

    def calculate_var_historical(
        self,
        returns: np.ndarray,
        portfolio_value: float,
        confidence_level: float = 0.95,
        time_horizon_days: int = 1
    ) -> VaRResult:
        """
        Calculate Historical Value at Risk (VaR)

        Uses historical returns distribution to estimate potential losses.
        Non-parametric method that doesn't assume normal distribution.

        Args:
            returns: Array of historical returns
            portfolio_value: Current portfolio value
            confidence_level: Confidence level (e.g., 0.95 for 95%)
            time_horizon_days: Time horizon in days

        Returns:
            VaRResult with historical VaR calculation
        """
        if len(returns) == 0:
            raise ValueError("Returns array cannot be empty")

        # Scale returns for time horizon
        scaled_returns = returns * np.sqrt(time_horizon_days)

        # Calculate VaR at the specified confidence level
        var_percentile = (1 - confidence_level) * 100
        var_return = np.percentile(scaled_returns, var_percentile)

        # Convert to dollar amount
        var_amount = abs(var_return * portfolio_value)
        var_percent = abs(var_return * 100)

        # Additional statistics
        additional_info = {
            "mean_return": float(np.mean(returns)),
            "std_return": float(np.std(returns)),
            "skewness": float(stats.skew(returns)),
            "kurtosis": float(stats.kurtosis(returns)),
            "worst_return": float(np.min(returns)),
            "best_return": float(np.max(returns)),
            "observations": len(returns)
        }

        return VaRResult(
            confidence_level=confidence_level,
            var_amount=var_amount,
            var_percent=var_percent,
            method="Historical Simulation",
            time_horizon_days=time_horizon_days,
            portfolio_value=portfolio_value,
            additional_info=additional_info
        )

    def calculate_var_parametric(
        self,
        returns: np.ndarray,
        portfolio_value: float,
        confidence_level: float = 0.95,
        time_horizon_days: int = 1
    ) -> VaRResult:
        """
        Calculate Parametric Value at Risk (VaR)

        Assumes returns follow a normal distribution.
        Also known as Variance-Covariance method.

        Args:
            returns: Array of historical returns
            portfolio_value: Current portfolio value
            confidence_level: Confidence level (e.g., 0.95 for 95%)
            time_horizon_days: Time horizon in days

        Returns:
            VaRResult with parametric VaR calculation
        """
        if len(returns) == 0:
            raise ValueError("Returns array cannot be empty")

        # Calculate mean and standard deviation
        mean_return = np.mean(returns)
        std_return = np.std(returns)

        # Get z-score for confidence level
        z_score = stats.norm.ppf(1 - confidence_level)

        # Calculate VaR
        # VaR = μ - z * σ * sqrt(t)
        var_return = mean_return + z_score * std_return * np.sqrt(time_horizon_days)

        # Convert to dollar amount
        var_amount = abs(var_return * portfolio_value)
        var_percent = abs(var_return * 100)

        # Additional statistics
        additional_info = {
            "mean_return": float(mean_return),
            "std_return": float(std_return),
            "z_score": float(z_score),
            "annualized_volatility": float(std_return * np.sqrt(252)),
            "observations": len(returns)
        }

        return VaRResult(
            confidence_level=confidence_level,
            var_amount=var_amount,
            var_percent=var_percent,
            method="Parametric (Normal Distribution)",
            time_horizon_days=time_horizon_days,
            portfolio_value=portfolio_value,
            additional_info=additional_info
        )

    def calculate_var_monte_carlo(
        self,
        returns: np.ndarray,
        portfolio_value: float,
        confidence_level: float = 0.95,
        time_horizon_days: int = 1,
        num_simulations: int = 10000
    ) -> VaRResult:
        """
        Calculate Monte Carlo Value at Risk (VaR)

        Simulates future portfolio values using random sampling
        from the returns distribution.

        Args:
            returns: Array of historical returns
            portfolio_value: Current portfolio value
            confidence_level: Confidence level (e.g., 0.95 for 95%)
            time_horizon_days: Time horizon in days
            num_simulations: Number of Monte Carlo simulations

        Returns:
            VaRResult with Monte Carlo VaR calculation
        """
        if len(returns) == 0:
            raise ValueError("Returns array cannot be empty")

        # Fit distribution parameters
        mean_return = np.mean(returns)
        std_return = np.std(returns)

        # Run Monte Carlo simulations
        simulated_returns = np.random.normal(
            mean_return,
            std_return,
            num_simulations
        ) * np.sqrt(time_horizon_days)

        # Calculate VaR at the specified confidence level
        var_percentile = (1 - confidence_level) * 100
        var_return = np.percentile(simulated_returns, var_percentile)

        # Convert to dollar amount
        var_amount = abs(var_return * portfolio_value)
        var_percent = abs(var_return * 100)

        # Calculate CVaR (Conditional VaR / Expected Shortfall)
        cvar_returns = simulated_returns[simulated_returns <= var_return]
        cvar_return = np.mean(cvar_returns) if len(cvar_returns) > 0 else var_return
        cvar_amount = abs(cvar_return * portfolio_value)

        # Additional statistics
        additional_info = {
            "mean_return": float(mean_return),
            "std_return": float(std_return),
            "num_simulations": num_simulations,
            "cvar_amount": float(cvar_amount),
            "cvar_percent": float(abs(cvar_return * 100)),
            "worst_simulated_return": float(np.min(simulated_returns)),
            "best_simulated_return": float(np.max(simulated_returns))
        }

        return VaRResult(
            confidence_level=confidence_level,
            var_amount=var_amount,
            var_percent=var_percent,
            method="Monte Carlo Simulation",
            time_horizon_days=time_horizon_days,
            portfolio_value=portfolio_value,
            additional_info=additional_info
        )

    def calculate_all_var_methods(
        self,
        returns: np.ndarray,
        portfolio_value: float,
        confidence_levels: List[float] = [0.95, 0.99],
        time_horizon_days: int = 1,
        num_simulations: int = 10000
    ) -> Dict[str, List[VaRResult]]:
        """
        Calculate VaR using all methods for comparison

        Args:
            returns: Array of historical returns
            portfolio_value: Current portfolio value
            confidence_levels: List of confidence levels to calculate
            time_horizon_days: Time horizon in days
            num_simulations: Number of Monte Carlo simulations

        Returns:
            Dictionary with VaR results for all methods and confidence levels
        """
        results = {
            "historical": [],
            "parametric": [],
            "monte_carlo": []
        }

        for conf_level in confidence_levels:
            # Historical VaR
            hist_var = self.calculate_var_historical(
                returns, portfolio_value, conf_level, time_horizon_days
            )
            results["historical"].append(hist_var)

            # Parametric VaR
            param_var = self.calculate_var_parametric(
                returns, portfolio_value, conf_level, time_horizon_days
            )
            results["parametric"].append(param_var)

            # Monte Carlo VaR
            mc_var = self.calculate_var_monte_carlo(
                returns, portfolio_value, conf_level, time_horizon_days, num_simulations
            )
            results["monte_carlo"].append(mc_var)

        return results

    # ==================== STRESS TESTING ====================

    def stress_test_historical_scenario(
        self,
        portfolio: Portfolio,
        scenario_shocks: Dict[str, float],
        scenario_name: str,
        description: str = ""
    ) -> StressTestResult:
        """
        Apply historical stress scenario to portfolio

        Args:
            portfolio: Portfolio to stress test
            scenario_shocks: Dict of symbol -> price shock (e.g., -0.20 for -20%)
            scenario_name: Name of the scenario
            description: Description of the scenario

        Returns:
            StressTestResult with scenario impact
        """
        position_impacts = {}
        total_loss = 0.0

        for position in portfolio.positions:
            shock = scenario_shocks.get(position.symbol, 0.0)
            position_loss = position.market_value * shock
            position_impacts[position.symbol] = position_loss
            total_loss += position_loss

        portfolio_value = portfolio.total_market_value
        loss_percent = (total_loss / portfolio_value * 100) if portfolio_value > 0 else 0.0

        return StressTestResult(
            scenario_name=scenario_name,
            scenario_type="historical",
            portfolio_loss=total_loss,
            portfolio_loss_percent=loss_percent,
            position_impacts=position_impacts,
            description=description
        )

    def stress_test_market_crash(
        self,
        portfolio: Portfolio,
        crash_severity: float = -0.30
    ) -> StressTestResult:
        """
        Test portfolio against market crash scenario

        Args:
            portfolio: Portfolio to stress test
            crash_severity: Market crash severity (e.g., -0.30 for -30%)

        Returns:
            StressTestResult with crash scenario impact
        """
        # Apply uniform shock to all positions
        scenario_shocks = {
            pos.symbol: crash_severity for pos in portfolio.positions
        }

        return self.stress_test_historical_scenario(
            portfolio,
            scenario_shocks,
            scenario_name=f"Market Crash ({crash_severity*100:.0f}%)",
            description=f"Uniform {abs(crash_severity)*100:.0f}% decline across all positions"
        )

    def stress_test_sector_shock(
        self,
        portfolio: Portfolio,
        sector: str,
        shock: float = -0.20
    ) -> StressTestResult:
        """
        Test portfolio against sector-specific shock

        Args:
            portfolio: Portfolio to stress test
            sector: Sector to shock
            shock: Shock magnitude (e.g., -0.20 for -20%)

        Returns:
            StressTestResult with sector shock impact
        """
        scenario_shocks = {}
        for pos in portfolio.positions:
            if pos.sector == sector:
                scenario_shocks[pos.symbol] = shock
            else:
                scenario_shocks[pos.symbol] = 0.0

        return self.stress_test_historical_scenario(
            portfolio,
            scenario_shocks,
            scenario_name=f"{sector} Sector Shock",
            description=f"{abs(shock)*100:.0f}% decline in {sector} sector"
        )

    def stress_test_volatility_spike(
        self,
        portfolio: Portfolio,
        vol_multiplier: float = 2.0
    ) -> Dict[str, Any]:
        """
        Test portfolio under volatility spike scenario

        Args:
            portfolio: Portfolio to stress test
            vol_multiplier: Volatility increase multiplier

        Returns:
            Dict with volatility spike impact analysis
        """
        # Calculate current portfolio Greeks
        greeks = self.calculate_portfolio_greeks(portfolio)

        # Impact of volatility spike on vega
        vega_impact = greeks.portfolio_vega * (vol_multiplier - 1.0) * 0.01

        return {
            "scenario_name": f"Volatility Spike ({vol_multiplier}x)",
            "scenario_type": "hypothetical",
            "current_vega": greeks.portfolio_vega,
            "volatility_multiplier": vol_multiplier,
            "estimated_impact": vega_impact,
            "description": f"Impact of {vol_multiplier}x increase in implied volatility"
        }

    def stress_test_factor_shock(
        self,
        portfolio: Portfolio,
        factor_name: str,
        factor_shock: float,
        factor_exposures: Dict[str, float]
    ) -> StressTestResult:
        """
        Test portfolio against factor shock

        Args:
            portfolio: Portfolio to stress test
            factor_name: Name of the factor (e.g., "Interest Rate", "Oil Price")
            factor_shock: Factor shock magnitude (e.g., 0.01 for +1%)
            factor_exposures: Dict of symbol -> factor exposure (beta)

        Returns:
            StressTestResult with factor shock impact
        """
        scenario_shocks = {}
        for pos in portfolio.positions:
            exposure = factor_exposures.get(pos.symbol, 0.0)
            scenario_shocks[pos.symbol] = exposure * factor_shock

        return self.stress_test_historical_scenario(
            portfolio,
            scenario_shocks,
            scenario_name=f"{factor_name} Shock",
            description=f"{factor_shock*100:+.2f}% shock to {factor_name}"
        )

    def stress_test_reverse(
        self,
        portfolio: Portfolio,
        target_loss: float
    ) -> Dict[str, Any]:
        """
        Reverse stress test: find scenarios that would cause target loss

        Args:
            portfolio: Portfolio to analyze
            target_loss: Target loss amount to reverse engineer

        Returns:
            Dict with reverse stress test results
        """
        portfolio_value = portfolio.total_market_value
        target_loss_pct = target_loss / portfolio_value if portfolio_value > 0 else 0

        # Calculate uniform shock needed
        uniform_shock = target_loss_pct

        # Calculate position-specific shocks for same total loss
        position_shocks = {}
        for pos in portfolio.positions:
            weight = pos.market_value / portfolio_value if portfolio_value > 0 else 0
            # Individual position shock to achieve target loss
            if weight > 0:
                position_shocks[pos.symbol] = target_loss_pct / weight
            else:
                position_shocks[pos.symbol] = 0.0

        return {
            "scenario_name": "Reverse Stress Test",
            "scenario_type": "reverse",
            "target_loss": target_loss,
            "target_loss_percent": target_loss_pct * 100,
            "uniform_shock_required": uniform_shock * 100,
            "position_specific_shocks": {
                symbol: shock * 100 for symbol, shock in position_shocks.items()
            },
            "description": f"Scenarios that would cause ${target_loss:,.2f} loss"
        }

    # ==================== PORTFOLIO GREEKS ====================

    def calculate_portfolio_greeks(
        self,
        portfolio: Portfolio
    ) -> GreeksResult:
        """
        Calculate portfolio-level Greeks

        Greeks measure sensitivity to various market factors:
        - Delta: Sensitivity to price changes
        - Gamma: Rate of change of delta
        - Vega: Sensitivity to volatility changes
        - Theta: Sensitivity to time decay

        Args:
            portfolio: Portfolio to calculate Greeks for

        Returns:
            GreeksResult with portfolio Greeks
        """
        portfolio_delta = 0.0
        portfolio_gamma = 0.0
        portfolio_vega = 0.0
        portfolio_theta = 0.0
        position_greeks = {}

        for pos in portfolio.positions:
            # Position Greeks (weighted by quantity)
            pos_delta = pos.delta * pos.quantity
            pos_gamma = pos.gamma * pos.quantity
            pos_vega = pos.vega * pos.quantity
            pos_theta = pos.theta * pos.quantity

            portfolio_delta += pos_delta
            portfolio_gamma += pos_gamma
            portfolio_vega += pos_vega
            portfolio_theta += pos_theta

            position_greeks[pos.symbol] = {
                "delta": pos_delta,
                "gamma": pos_gamma,
                "vega": pos_vega,
                "theta": pos_theta,
                "quantity": pos.quantity,
                "market_value": pos.market_value
            }

        # Delta-adjusted exposure
        delta_exposure = portfolio_delta * (
            sum(pos.current_price for pos in portfolio.positions) /
            len(portfolio.positions) if portfolio.positions else 0
        )

        return GreeksResult(
            portfolio_delta=portfolio_delta,
            portfolio_gamma=portfolio_gamma,
            portfolio_vega=portfolio_vega,
            portfolio_theta=portfolio_theta,
            delta_exposure=delta_exposure,
            position_greeks=position_greeks
        )

    def calculate_hedging_suggestions(
        self,
        portfolio: Portfolio,
        target_delta: float = 0.0
    ) -> Dict[str, Any]:
        """
        Calculate hedging suggestions to reach target delta

        Args:
            portfolio: Portfolio to hedge
            target_delta: Target portfolio delta (0 = delta neutral)

        Returns:
            Dict with hedging suggestions
        """
        current_greeks = self.calculate_portfolio_greeks(portfolio)
        current_delta = current_greeks.portfolio_delta

        delta_to_hedge = current_delta - target_delta

        # Suggest hedge using index (assuming SPY or similar)
        if abs(delta_to_hedge) < 1:
            return {
                "current_delta": current_delta,
                "target_delta": target_delta,
                "hedge_needed": False,
                "message": "Portfolio is approximately delta neutral"
            }

        # Assume SPY at $450 with delta of 1.0
        spy_shares_to_short = int(delta_to_hedge)
        hedge_cost_estimate = abs(spy_shares_to_short * 450)  # Rough estimate

        return {
            "current_delta": current_delta,
            "target_delta": target_delta,
            "delta_to_hedge": delta_to_hedge,
            "hedge_needed": True,
            "suggestions": [
                {
                    "strategy": "Short Index ETF (e.g., SPY)",
                    "shares": abs(spy_shares_to_short),
                    "direction": "short" if delta_to_hedge > 0 else "long",
                    "estimated_cost": hedge_cost_estimate,
                    "description": f"{'Short' if delta_to_hedge > 0 else 'Long'} {abs(spy_shares_to_short)} shares of SPY"
                },
                {
                    "strategy": "Index Futures",
                    "contracts": abs(int(delta_to_hedge / 100)),
                    "direction": "short" if delta_to_hedge > 0 else "long",
                    "description": "More capital efficient than ETFs"
                },
                {
                    "strategy": "Index Put/Call Options",
                    "description": "For more sophisticated hedging with defined risk",
                    "note": "Requires options analysis"
                }
            ]
        }

    # ==================== DRAWDOWN ANALYSIS ====================

    def calculate_drawdowns(
        self,
        equity_curve: pd.Series
    ) -> DrawdownResult:
        """
        Calculate comprehensive drawdown metrics

        Args:
            equity_curve: Time series of portfolio values

        Returns:
            DrawdownResult with drawdown analysis
        """
        if len(equity_curve) == 0:
            raise ValueError("Equity curve cannot be empty")

        # Calculate running maximum
        running_max = equity_curve.expanding().max()

        # Calculate drawdown
        drawdown = equity_curve - running_max
        drawdown_pct = (drawdown / running_max) * 100

        # Maximum drawdown
        max_dd = drawdown.min()
        max_dd_pct = drawdown_pct.min()

        # Average drawdown (only negative periods)
        negative_dd = drawdown[drawdown < 0]
        avg_dd = negative_dd.mean() if len(negative_dd) > 0 else 0.0
        avg_dd_pct = drawdown_pct[drawdown_pct < 0].mean() if len(negative_dd) > 0 else 0.0

        # Current drawdown
        current_dd = drawdown.iloc[-1]
        current_dd_pct = drawdown_pct.iloc[-1]

        # Find underwater periods (periods in drawdown)
        underwater_periods = []
        in_drawdown = False
        start_idx = None

        for idx, dd in enumerate(drawdown):
            if dd < 0 and not in_drawdown:
                # Start of drawdown period
                in_drawdown = True
                start_idx = idx
            elif dd >= 0 and in_drawdown:
                # End of drawdown period
                in_drawdown = False
                end_idx = idx - 1

                period_dd = drawdown.iloc[start_idx:end_idx+1].min()
                period_dd_pct = drawdown_pct.iloc[start_idx:end_idx+1].min()
                duration = end_idx - start_idx + 1

                underwater_periods.append({
                    "start_date": str(equity_curve.index[start_idx]) if hasattr(equity_curve.index[start_idx], '__str__') else start_idx,
                    "end_date": str(equity_curve.index[end_idx]) if hasattr(equity_curve.index[end_idx], '__str__') else end_idx,
                    "duration_days": duration,
                    "max_drawdown": float(period_dd),
                    "max_drawdown_pct": float(period_dd_pct)
                })

        # If still in drawdown
        if in_drawdown:
            duration = len(drawdown) - start_idx
            underwater_periods.append({
                "start_date": str(equity_curve.index[start_idx]) if hasattr(equity_curve.index[start_idx], '__str__') else start_idx,
                "end_date": "Ongoing",
                "duration_days": duration,
                "max_drawdown": float(drawdown.iloc[start_idx:].min()),
                "max_drawdown_pct": float(drawdown_pct.iloc[start_idx:].min())
            })

        # Maximum drawdown duration
        max_dd_duration = max([p["duration_days"] for p in underwater_periods]) if underwater_periods else 0

        # Recovery time (for completed drawdowns only)
        completed_periods = [p for p in underwater_periods if p["end_date"] != "Ongoing"]
        avg_recovery = np.mean([p["duration_days"] for p in completed_periods]) if completed_periods else None

        return DrawdownResult(
            max_drawdown=float(max_dd),
            max_drawdown_percent=float(max_dd_pct),
            average_drawdown=float(avg_dd),
            average_drawdown_percent=float(avg_dd_pct),
            current_drawdown=float(current_dd),
            current_drawdown_percent=float(current_dd_pct),
            max_drawdown_duration_days=int(max_dd_duration),
            recovery_time_days=int(avg_recovery) if avg_recovery is not None else None,
            underwater_periods=underwater_periods,
            drawdown_series=drawdown_pct
        )

    # ==================== RISK ATTRIBUTION ====================

    def calculate_risk_attribution(
        self,
        portfolio: Portfolio,
        returns_data: Dict[str, np.ndarray]
    ) -> RiskAttributionResult:
        """
        Calculate risk attribution across positions and sectors

        Args:
            portfolio: Portfolio to analyze
            returns_data: Dict of symbol -> returns array

        Returns:
            RiskAttributionResult with risk attribution
        """
        # Calculate portfolio volatility (total risk)
        weights = portfolio.get_weights()

        # Build covariance matrix
        symbols = [pos.symbol for pos in portfolio.positions]
        returns_matrix = []

        for symbol in symbols:
            if symbol in returns_data:
                returns_matrix.append(returns_data[symbol])
            else:
                # Use zero returns if data not available
                logger.warning(f"No returns data for {symbol}, using zeros")
                returns_matrix.append(np.zeros(100))

        if len(returns_matrix) == 0:
            raise ValueError("No returns data available")

        # Convert to DataFrame for covariance calculation
        returns_df = pd.DataFrame(
            np.array(returns_matrix).T,
            columns=symbols
        )

        cov_matrix = returns_df.cov()

        # Portfolio variance
        weights_array = np.array([weights.get(s, 0) for s in symbols])
        portfolio_variance = np.dot(weights_array, np.dot(cov_matrix, weights_array))
        portfolio_risk = np.sqrt(portfolio_variance) * 100  # Convert to percentage

        # Marginal risk contribution (MRC)
        marginal_risk = {}
        for i, symbol in enumerate(symbols):
            # MRC = (Cov * w) / portfolio_risk
            cov_contribution = np.dot(cov_matrix.iloc[i], weights_array)
            mrc = cov_contribution / np.sqrt(portfolio_variance) if portfolio_variance > 0 else 0
            marginal_risk[symbol] = float(mrc * 100)

        # Risk contribution
        risk_contribution = {}
        risk_contribution_pct = {}

        for symbol in symbols:
            weight = weights.get(symbol, 0)
            mrc = marginal_risk.get(symbol, 0) / 100
            contrib = weight * mrc * 100
            risk_contribution[symbol] = float(contrib)
            risk_contribution_pct[symbol] = float(
                (contrib / portfolio_risk * 100) if portfolio_risk > 0 else 0
            )

        # Risk by sector
        risk_by_sector = {}
        for pos in portfolio.positions:
            if pos.sector:
                sector_risk = risk_contribution.get(pos.symbol, 0)
                if pos.sector in risk_by_sector:
                    risk_by_sector[pos.sector] += sector_risk
                else:
                    risk_by_sector[pos.sector] = sector_risk

        # Concentration metrics
        position_weights = list(weights.values())
        herfindahl_index = sum(w**2 for w in position_weights)
        effective_positions = 1 / herfindahl_index if herfindahl_index > 0 else 0

        concentration_metrics = {
            "herfindahl_index": float(herfindahl_index),
            "effective_number_of_positions": float(effective_positions),
            "largest_position_weight": float(max(position_weights)) if position_weights else 0,
            "top_5_concentration": float(sum(sorted(position_weights, reverse=True)[:5])),
            "diversification_ratio": float(len(portfolio.positions) / effective_positions) if effective_positions > 0 else 0
        }

        return RiskAttributionResult(
            total_risk=float(portfolio_risk),
            risk_by_position=risk_contribution,
            risk_by_sector=risk_by_sector,
            marginal_risk=marginal_risk,
            risk_contribution_percent=risk_contribution_pct,
            concentration_metrics=concentration_metrics
        )


# Global instance
_portfolio_risk: Optional[PortfolioRiskMeasurement] = None


def get_portfolio_risk_service() -> PortfolioRiskMeasurement:
    """Get or create portfolio risk measurement service singleton"""
    global _portfolio_risk
    if _portfolio_risk is None:
        _portfolio_risk = PortfolioRiskMeasurement()
    return _portfolio_risk
