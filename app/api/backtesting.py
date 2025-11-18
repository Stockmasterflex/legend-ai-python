"""
Backtesting API Endpoints
RESTful API for running backtests, Monte Carlo simulations, and walk-forward analysis
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel, Field
from typing import Dict, List, Any, Optional
from datetime import datetime
import logging
import json

from app.backtesting import (
    Strategy,
    BacktestEngine,
    BacktestResult,
    PerformanceMetrics,
    MonteCarloSimulator,
    WalkForwardAnalyzer,
    BacktestVisualizer,
    PatternBasedStrategy,
    IndicatorBasedStrategy,
    PositionSizingMethod
)
from app.services.market_data import MarketDataService
from app.models import Backtest, BacktestTrade
from app.config import get_db_session

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/backtest", tags=["Backtesting"])


# Request/Response Models
class BacktestRequest(BaseModel):
    """Request model for running a backtest"""
    name: str = Field(..., description="Backtest name")
    description: Optional[str] = Field(None, description="Backtest description")
    strategy_type: str = Field(..., description="Strategy type: 'pattern_based' or 'indicator_based'")

    # Strategy configuration
    strategy_config: Dict[str, Any] = Field(default_factory=dict, description="Strategy parameters")

    # Backtest parameters
    ticker: Optional[str] = Field(None, description="Single ticker (or null for universe)")
    universe: Optional[str] = Field(None, description="Universe: 'SP500', 'NASDAQ100'")
    start_date: str = Field(..., description="Start date (YYYY-MM-DD)")
    end_date: str = Field(..., description="End date (YYYY-MM-DD)")

    # Capital and risk
    initial_capital: float = Field(100000, description="Initial capital")
    position_sizing_method: str = Field("risk_based", description="Position sizing method")
    risk_per_trade: float = Field(0.02, description="Risk per trade (e.g., 0.02 = 2%)")
    commission_per_trade: float = Field(0, description="Commission per trade")
    slippage_percent: float = Field(0, description="Slippage percentage")

    # Advanced options
    run_monte_carlo: bool = Field(False, description="Run Monte Carlo simulation")
    monte_carlo_runs: int = Field(1000, description="Number of Monte Carlo simulations")
    run_walk_forward: bool = Field(False, description="Run walk-forward analysis")
    walk_forward_windows: int = Field(5, description="Number of walk-forward windows")


class BacktestResponse(BaseModel):
    """Response model for backtest results"""
    backtest_id: int
    status: str
    message: str
    results: Optional[Dict[str, Any]] = None


class BacktestListResponse(BaseModel):
    """Response model for listing backtests"""
    backtests: List[Dict[str, Any]]
    total: int


# API Endpoints
@router.post("/run", response_model=BacktestResponse)
async def run_backtest(request: BacktestRequest, background_tasks: BackgroundTasks):
    """
    Run a backtest

    This endpoint:
    1. Creates strategy based on configuration
    2. Fetches historical data
    3. Runs backtest simulation
    4. Optionally runs Monte Carlo and walk-forward analysis
    5. Saves results to database
    """
    try:
        logger.info(f"Starting backtest: {request.name}")

        # Parse dates
        start_date = datetime.fromisoformat(request.start_date)
        end_date = datetime.fromisoformat(request.end_date)

        # Create strategy
        strategy = _create_strategy(request.strategy_type, request.strategy_config)

        # Fetch historical data
        tickers = _get_tickers(request.ticker, request.universe)
        if not tickers:
            raise HTTPException(status_code=400, detail="No tickers specified")

        market_data = MarketDataService()
        data = {}

        for ticker in tickers[:10]:  # Limit to 10 tickers for performance
            try:
                df = await market_data.get_historical_data(
                    ticker,
                    interval="1d",
                    outputsize="full"
                )
                if df is not None and len(df) > 0:
                    data[ticker] = df
            except Exception as e:
                logger.warning(f"Failed to fetch data for {ticker}: {e}")

        if not data:
            raise HTTPException(status_code=400, detail="No data available for specified tickers")

        # Run backtest
        engine = BacktestEngine(
            initial_capital=request.initial_capital,
            commission_per_trade=request.commission_per_trade,
            slippage_percent=request.slippage_percent
        )

        result = engine.run_backtest(
            strategy,
            data,
            start_date,
            end_date
        )

        # Run Monte Carlo if requested
        monte_carlo_result = None
        if request.run_monte_carlo:
            trades_dict = [
                {
                    "profit_loss": t.profit_loss,
                    "profit_loss_pct": t.profit_loss_pct,
                }
                for t in result.trades
            ]
            mc = MonteCarloSimulator.run_simulation(
                trades_dict,
                request.initial_capital,
                request.monte_carlo_runs
            )
            monte_carlo_result = mc.to_dict()

        # Run walk-forward if requested
        walk_forward_result = None
        if request.run_walk_forward:
            wf_analyzer = WalkForwardAnalyzer(in_sample_ratio=0.7)
            wf = wf_analyzer.run_walk_forward(
                strategy,
                data,
                num_windows=request.walk_forward_windows,
                initial_capital=request.initial_capital
            )
            walk_forward_result = wf.to_dict()

        # Save to database
        backtest_id = await _save_backtest_to_db(
            request,
            result,
            monte_carlo_result,
            walk_forward_result
        )

        # Generate response
        response_data = {
            "backtest_id": backtest_id,
            "summary": result.to_dict(),
            "metrics": result.metrics.to_dict(),
            "trades": [
                {
                    "ticker": t.ticker,
                    "entry_date": t.entry_date.isoformat(),
                    "entry_price": t.entry_price,
                    "exit_date": t.exit_date.isoformat(),
                    "exit_price": t.exit_price,
                    "profit_loss": t.profit_loss,
                    "profit_loss_pct": t.profit_loss_pct,
                    "duration_days": t.duration_days,
                }
                for t in result.trades
            ],
            "visualizations": {
                "equity_curve": BacktestVisualizer.create_equity_curve_data(result.equity_curve),
                "drawdown": BacktestVisualizer.create_drawdown_chart_data(result.equity_curve),
                "trade_distribution": BacktestVisualizer.create_trade_distribution_data(
                    [{"profit_loss_pct": t.profit_loss_pct} for t in result.trades]
                ),
            }
        }

        if monte_carlo_result:
            response_data["monte_carlo"] = monte_carlo_result
            response_data["visualizations"]["monte_carlo"] = BacktestVisualizer.create_monte_carlo_distribution(
                monte_carlo_result
            )

        if walk_forward_result:
            response_data["walk_forward"] = walk_forward_result

        return BacktestResponse(
            backtest_id=backtest_id,
            status="completed",
            message="Backtest completed successfully",
            results=response_data
        )

    except Exception as e:
        logger.error(f"Backtest failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Backtest failed: {str(e)}")


@router.get("/{backtest_id}", response_model=BacktestResponse)
async def get_backtest_results(backtest_id: int):
    """Get backtest results by ID"""
    try:
        db = next(get_db_session())
        backtest = db.query(Backtest).filter(Backtest.id == backtest_id).first()

        if not backtest:
            raise HTTPException(status_code=404, detail="Backtest not found")

        # Get trades
        trades = db.query(BacktestTrade).filter(BacktestTrade.backtest_id == backtest_id).all()

        results = {
            "backtest_id": backtest.id,
            "name": backtest.name,
            "description": backtest.description,
            "strategy_type": backtest.strategy_type,
            "ticker": backtest.ticker,
            "period": {
                "start": backtest.start_date.isoformat(),
                "end": backtest.end_date.isoformat(),
            },
            "metrics": {
                "total_return": backtest.total_return,
                "total_return_pct": backtest.total_return_pct,
                "sharpe_ratio": backtest.sharpe_ratio,
                "max_drawdown_pct": backtest.max_drawdown_pct,
                "win_rate": backtest.win_rate,
                "total_trades": backtest.total_trades,
            },
            "trades": [
                {
                    "ticker": t.ticker,
                    "entry_date": t.entry_date.isoformat(),
                    "exit_date": t.exit_date.isoformat() if t.exit_date else None,
                    "profit_loss": t.profit_loss,
                    "profit_loss_pct": t.profit_loss_pct,
                }
                for t in trades
            ]
        }

        return BacktestResponse(
            backtest_id=backtest.id,
            status=backtest.status,
            message="Backtest results retrieved",
            results=results
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to retrieve backtest: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/list", response_model=BacktestListResponse)
async def list_backtests(limit: int = 50, offset: int = 0):
    """List all backtests"""
    try:
        db = next(get_db_session())
        backtests = db.query(Backtest).order_by(Backtest.created_at.desc()).limit(limit).offset(offset).all()
        total = db.query(Backtest).count()

        backtest_list = [
            {
                "id": b.id,
                "name": b.name,
                "strategy_type": b.strategy_type,
                "ticker": b.ticker,
                "total_return_pct": b.total_return_pct,
                "sharpe_ratio": b.sharpe_ratio,
                "max_drawdown_pct": b.max_drawdown_pct,
                "total_trades": b.total_trades,
                "created_at": b.created_at.isoformat(),
                "status": b.status,
            }
            for b in backtests
        ]

        return BacktestListResponse(backtests=backtest_list, total=total)

    except Exception as e:
        logger.error(f"Failed to list backtests: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/compare")
async def compare_backtests(backtest_ids: List[int]):
    """Compare multiple backtests"""
    try:
        db = next(get_db_session())
        backtests = db.query(Backtest).filter(Backtest.id.in_(backtest_ids)).all()

        if not backtests:
            raise HTTPException(status_code=404, detail="No backtests found")

        results = [
            {
                "id": b.id,
                "strategy_name": b.name,
                "metrics": {
                    "returns": {
                        "total_return_pct": b.total_return_pct,
                        "cagr": b.total_return_pct,  # Simplified
                    },
                    "risk": {
                        "sharpe_ratio": b.sharpe_ratio,
                        "max_drawdown_pct": b.max_drawdown_pct,
                        "annual_volatility": 0,  # Would need to calculate
                    },
                    "trades": {
                        "total_trades": b.total_trades,
                        "win_rate": b.win_rate,
                    },
                    "profit_loss": {
                        "profit_factor": b.profit_factor,
                    }
                }
            }
            for b in backtests
        ]

        # Generate comparison chart
        comparison_chart = BacktestVisualizer.create_risk_adjusted_returns_chart(results)

        return {
            "backtests": results,
            "visualization": comparison_chart
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to compare backtests: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{backtest_id}")
async def delete_backtest(backtest_id: int):
    """Delete a backtest"""
    try:
        db = next(get_db_session())
        backtest = db.query(Backtest).filter(Backtest.id == backtest_id).first()

        if not backtest:
            raise HTTPException(status_code=404, detail="Backtest not found")

        # Delete trades first
        db.query(BacktestTrade).filter(BacktestTrade.backtest_id == backtest_id).delete()

        # Delete backtest
        db.delete(backtest)
        db.commit()

        return {"message": "Backtest deleted successfully"}

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to delete backtest: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Helper Functions
def _create_strategy(strategy_type: str, config: Dict[str, Any]) -> Strategy:
    """Create strategy instance based on type and configuration"""
    if strategy_type == "pattern_based":
        return PatternBasedStrategy(
            name=config.get("name", "Pattern Strategy"),
            pattern_types=config.get("pattern_types", ["vcp", "cup_and_handle"]),
            min_pattern_score=config.get("min_pattern_score", 7.0),
            position_sizing_method=PositionSizingMethod(config.get("position_sizing_method", "risk_based"))
        )

    elif strategy_type == "indicator_based":
        return IndicatorBasedStrategy(
            name=config.get("name", "Indicator Strategy"),
            use_rsi=config.get("use_rsi", True),
            rsi_oversold=config.get("rsi_oversold", 30),
            rsi_overbought=config.get("rsi_overbought", 70),
            use_macd=config.get("use_macd", True),
            use_ma_cross=config.get("use_ma_cross", True),
            fast_ma=config.get("fast_ma", 20),
            slow_ma=config.get("slow_ma", 50),
            position_sizing_method=PositionSizingMethod(config.get("position_sizing_method", "risk_based"))
        )

    else:
        raise ValueError(f"Unknown strategy type: {strategy_type}")


def _get_tickers(ticker: Optional[str], universe: Optional[str]) -> List[str]:
    """Get list of tickers to backtest"""
    if ticker:
        return [ticker.upper()]

    if universe:
        from app.services.universe_store import UniverseStore
        store = UniverseStore()

        if universe.upper() == "SP500":
            return store.get_sp500_tickers()
        elif universe.upper() == "NASDAQ100":
            return store.get_nasdaq100_tickers()

    return []


async def _save_backtest_to_db(
    request: BacktestRequest,
    result: BacktestResult,
    monte_carlo: Optional[Dict[str, Any]],
    walk_forward: Optional[Dict[str, Any]]
) -> int:
    """Save backtest results to database"""
    try:
        db = next(get_db_session())

        # Create backtest record
        backtest = Backtest(
            name=request.name,
            description=request.description,
            strategy_type=request.strategy_type,
            strategy_config=json.dumps(request.strategy_config),
            ticker=request.ticker,
            universe=request.universe,
            start_date=datetime.fromisoformat(request.start_date),
            end_date=datetime.fromisoformat(request.end_date),
            initial_capital=request.initial_capital,
            position_sizing_method=request.position_sizing_method,
            risk_per_trade=request.risk_per_trade,
            commission_per_trade=request.commission_per_trade,
            slippage_percent=request.slippage_percent,
            final_capital=result.final_capital,
            total_return=result.final_capital - result.initial_capital,
            total_return_pct=result.metrics.total_return_pct,
            sharpe_ratio=result.metrics.sharpe_ratio,
            sortino_ratio=result.metrics.sortino_ratio,
            max_drawdown=result.metrics.max_drawdown,
            max_drawdown_pct=result.metrics.max_drawdown_pct,
            calmar_ratio=result.metrics.calmar_ratio,
            win_rate=result.metrics.win_rate,
            loss_rate=result.metrics.loss_rate,
            total_trades=result.metrics.total_trades,
            winning_trades=result.metrics.winning_trades,
            losing_trades=result.metrics.losing_trades,
            avg_win=result.metrics.avg_win,
            avg_loss=result.metrics.avg_loss,
            largest_win=result.metrics.largest_win,
            largest_loss=result.metrics.largest_loss,
            profit_factor=result.metrics.profit_factor,
            expectancy=result.metrics.expectancy,
            avg_trade_duration_days=result.metrics.avg_trade_duration_days,
            monte_carlo_runs=monte_carlo.get("num_simulations") if monte_carlo else None,
            monte_carlo_mean_return=monte_carlo.get("statistics", {}).get("mean_return") if monte_carlo else None,
            monte_carlo_std_return=monte_carlo.get("statistics", {}).get("std_return") if monte_carlo else None,
            monte_carlo_var_95=monte_carlo.get("risk", {}).get("var_95") if monte_carlo else None,
            completed_at=datetime.now(),
            status="completed"
        )

        db.add(backtest)
        db.flush()

        # Save trades
        for trade in result.trades:
            bt_trade = BacktestTrade(
                backtest_id=backtest.id,
                ticker=trade.ticker,
                signal_type=trade.signal_type,
                entry_date=trade.entry_date,
                entry_price=trade.entry_price,
                entry_reason=trade.entry_reason,
                position_size=trade.shares,
                position_value=trade.shares * trade.entry_price,
                stop_loss=trade.stop_loss,
                target_price=trade.target_price,
                exit_date=trade.exit_date,
                exit_price=trade.exit_price,
                exit_reason=trade.exit_reason,
                profit_loss=trade.profit_loss,
                profit_loss_pct=trade.profit_loss_pct,
                r_multiple=trade.r_multiple,
                commission_paid=trade.commission,
                duration_days=trade.duration_days,
                mae=trade.mae,
                mfe=trade.mfe,
                status="closed",
                is_win=trade.is_win
            )
            db.add(bt_trade)

        db.commit()
        return backtest.id

    except Exception as e:
        db.rollback()
        logger.error(f"Failed to save backtest to database: {e}")
        raise
