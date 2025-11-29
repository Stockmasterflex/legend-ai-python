"""
Backtesting API Endpoints
Comprehensive API for running backtests, optimizations, and Monte Carlo simulations
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks, Depends
from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any
from datetime import datetime
from sqlalchemy.orm import Session
import asyncio
import logging

from app.services.database import get_db
from app.models import (
    Strategy as StrategyModel,
    BacktestRun,
    BacktestTrade,
    BacktestMetrics,
    StrategyTemplate,
    WalkForwardRun,
    MonteCarloRun,
    HyperparameterOptimization,
)
from app.backtesting.engine import BacktestEngine, BacktestConfig
from app.backtesting.strategy import YAMLStrategy, PythonStrategy, VisualStrategy
from app.backtesting.execution import ExecutionSimulator
from app.backtesting.walk_forward import WalkForwardOptimizer, WalkForwardConfig
from app.backtesting.monte_carlo import MonteCarloEngine, MonteCarloConfig
from app.backtesting.ml.optimization import HyperparameterOptimizer, OptimizationConfig, OptimizationType
from app.backtesting.ml.models import ModelType

router = APIRouter(prefix="/api/backtest", tags=["backtesting"])
logger = logging.getLogger(__name__)


# =====================================================================
# Request/Response Models
# =====================================================================

class CreateStrategyRequest(BaseModel):
    name: str
    description: Optional[str] = None
    strategy_type: str = Field(..., description="yaml, python, or visual")
    yaml_config: Optional[str] = None
    python_code: Optional[str] = None
    visual_config: Optional[Dict] = None
    parameters: Dict[str, Any] = Field(default_factory=dict)
    entry_rules: Optional[Dict] = None
    exit_rules: Optional[Dict] = None
    risk_management: Optional[Dict] = None


class RunBacktestRequest(BaseModel):
    strategy_id: int
    name: str
    start_date: datetime
    end_date: datetime
    initial_capital: float = 100000.0
    universe: List[str]  # List of tickers

    # Execution simulation
    commission_type: str = "per_share"
    commission_value: float = 0.005
    slippage_type: str = "fixed_bps"
    slippage_value: float = 5.0
    enable_market_impact: bool = False
    allow_partial_fills: bool = False


class RunWalkForwardRequest(BaseModel):
    strategy_id: int
    name: str
    start_date: datetime
    end_date: datetime
    initial_capital: float = 100000.0
    universe: List[str]

    in_sample_days: int = 252
    out_sample_days: int = 63
    step_days: int = 63

    parameter_ranges: Dict[str, List[Any]]
    optimization_metric: str = "sharpe_ratio"
    optimization_type: str = "grid"
    n_trials: int = 100


class RunMonteCarloRequest(BaseModel):
    backtest_run_id: int
    name: str
    n_simulations: int = 1000
    simulation_types: List[str] = ["random_entry", "position_size"]

    entry_delay_min_days: int = -5
    entry_delay_max_days: int = 5
    position_size_variation_pct: float = 20.0
    include_regime_changes: bool = False


class OptimizeHyperparametersRequest(BaseModel):
    strategy_id: Optional[int] = None
    model_type: str
    parameter_space: Dict[str, List[Any]]
    optimization_type: str = "grid"
    n_trials: int = 100
    objective_metric: str = "val_accuracy"


# =====================================================================
# Strategy Management Endpoints
# =====================================================================

@router.post("/strategies", status_code=201)
async def create_strategy(
    request: CreateStrategyRequest,
    db: Session = Depends(get_db),
) -> Dict:
    """Create a new trading strategy"""
    try:
        # Create strategy model
        strategy = StrategyModel(
            name=request.name,
            description=request.description,
            strategy_type=request.strategy_type,
            yaml_config=request.yaml_config,
            python_code=request.python_code,
            visual_config=request.visual_config,
            parameters=request.parameters,
            entry_rules=request.entry_rules,
            exit_rules=request.exit_rules,
            risk_management=request.risk_management,
        )

        db.add(strategy)
        db.commit()
        db.refresh(strategy)

        return {
            "id": strategy.id,
            "name": strategy.name,
            "strategy_type": strategy.strategy_type,
            "created_at": strategy.created_at.isoformat(),
        }

    except Exception as e:
        logger.error(f"Failed to create strategy: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/strategies")
async def list_strategies(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
) -> List[Dict]:
    """List all strategies"""
    strategies = db.query(StrategyModel).offset(skip).limit(limit).all()

    return [
        {
            "id": s.id,
            "name": s.name,
            "strategy_type": s.strategy_type,
            "is_active": s.is_active,
            "created_at": s.created_at.isoformat(),
        }
        for s in strategies
    ]


@router.get("/strategies/{strategy_id}")
async def get_strategy(
    strategy_id: int,
    db: Session = Depends(get_db),
) -> Dict:
    """Get strategy details"""
    strategy = db.query(StrategyModel).filter(StrategyModel.id == strategy_id).first()

    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")

    return {
        "id": strategy.id,
        "name": strategy.name,
        "description": strategy.description,
        "strategy_type": strategy.strategy_type,
        "yaml_config": strategy.yaml_config,
        "python_code": strategy.python_code,
        "visual_config": strategy.visual_config,
        "parameters": strategy.parameters,
        "entry_rules": strategy.entry_rules,
        "exit_rules": strategy.exit_rules,
        "risk_management": strategy.risk_management,
        "version": strategy.version,
        "is_active": strategy.is_active,
        "created_at": strategy.created_at.isoformat(),
    }


# =====================================================================
# Backtesting Endpoints
# =====================================================================

@router.post("/run", status_code=202)
async def run_backtest(
    request: RunBacktestRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
) -> Dict:
    """Run a backtest (async)"""
    # Get strategy
    strategy_model = db.query(StrategyModel).filter(StrategyModel.id == request.strategy_id).first()

    if not strategy_model:
        raise HTTPException(status_code=404, detail="Strategy not found")

    # Create backtest run record
    backtest_run = BacktestRun(
        strategy_id=request.strategy_id,
        name=request.name,
        start_date=request.start_date,
        end_date=request.end_date,
        initial_capital=request.initial_capital,
        universe=request.universe,
        commission_model={"type": request.commission_type, "value": request.commission_value},
        slippage_model={"type": request.slippage_type, "value": request.slippage_value},
        market_impact_model={"enabled": request.enable_market_impact},
        allow_partial_fills=request.allow_partial_fills,
        status="pending",
    )

    db.add(backtest_run)
    db.commit()
    db.refresh(backtest_run)

    # Run backtest in background
    background_tasks.add_task(_run_backtest_task, backtest_run.id, strategy_model, request)

    return {
        "backtest_id": backtest_run.id,
        "status": "pending",
        "message": "Backtest queued for execution",
    }


async def _run_backtest_task(
    backtest_id: int,
    strategy_model: StrategyModel,
    request: RunBacktestRequest,
):
    """Background task to run backtest"""
    # This is a placeholder - implement with actual market data provider
    logger.info(f"Starting backtest {backtest_id}")

    # Note: In production, implement data_provider to fetch real market data
    # For now, this is a skeleton implementation


@router.get("/runs/{backtest_id}")
async def get_backtest_status(
    backtest_id: int,
    db: Session = Depends(get_db),
) -> Dict:
    """Get backtest status and results"""
    backtest = db.query(BacktestRun).filter(BacktestRun.id == backtest_id).first()

    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")

    return {
        "id": backtest.id,
        "name": backtest.name,
        "status": backtest.status,
        "progress": backtest.progress,
        "start_date": backtest.start_date.isoformat(),
        "end_date": backtest.end_date.isoformat(),
        "initial_capital": backtest.initial_capital,
        "final_value": backtest.final_value,
        "total_return": backtest.total_return,
        "sharpe_ratio": backtest.sharpe_ratio,
        "max_drawdown": backtest.max_drawdown,
        "total_trades": backtest.total_trades,
        "win_rate": backtest.win_rate,
        "profit_factor": backtest.profit_factor,
        "created_at": backtest.created_at.isoformat() if backtest.created_at else None,
        "completed_at": backtest.completed_at.isoformat() if backtest.completed_at else None,
    }


@router.get("/runs/{backtest_id}/trades")
async def get_backtest_trades(
    backtest_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
) -> List[Dict]:
    """Get trades from a backtest"""
    trades = (
        db.query(BacktestTrade)
        .filter(BacktestTrade.backtest_run_id == backtest_id)
        .offset(skip)
        .limit(limit)
        .all()
    )

    return [
        {
            "id": t.id,
            "ticker": t.ticker_id,
            "entry_date": t.entry_date.isoformat() if t.entry_date else None,
            "exit_date": t.exit_date.isoformat() if t.exit_date else None,
            "entry_price": t.entry_price,
            "exit_price": t.exit_price,
            "position_size": t.position_size,
            "net_profit_loss": t.net_profit_loss,
            "profit_loss_pct": t.profit_loss_pct,
            "r_multiple": t.r_multiple,
            "days_held": t.days_held,
            "exit_reason": t.exit_reason,
        }
        for t in trades
    ]


# =====================================================================
# Walk-Forward Optimization Endpoints
# =====================================================================

@router.post("/walk-forward", status_code=202)
async def run_walk_forward_optimization(
    request: RunWalkForwardRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
) -> Dict:
    """Run walk-forward optimization"""
    # Get strategy
    strategy_model = db.query(StrategyModel).filter(StrategyModel.id == request.strategy_id).first()

    if not strategy_model:
        raise HTTPException(status_code=404, detail="Strategy not found")

    # Create walk-forward run record
    wf_run = WalkForwardRun(
        strategy_id=request.strategy_id,
        name=request.name,
        total_start_date=request.start_date,
        total_end_date=request.end_date,
        in_sample_period_days=request.in_sample_days,
        out_sample_period_days=request.out_sample_days,
        step_size_days=request.step_days,
        parameter_ranges=request.parameter_ranges,
        optimization_metric=request.optimization_metric,
        n_trials=request.n_trials,
        status="pending",
    )

    db.add(wf_run)
    db.commit()
    db.refresh(wf_run)

    return {
        "walk_forward_id": wf_run.id,
        "status": "pending",
        "message": "Walk-forward optimization queued",
    }


# =====================================================================
# Monte Carlo Endpoints
# =====================================================================

@router.post("/monte-carlo", status_code=202)
async def run_monte_carlo(
    request: RunMonteCarloRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
) -> Dict:
    """Run Monte Carlo simulation"""
    # Get baseline backtest
    baseline = db.query(BacktestRun).filter(BacktestRun.id == request.backtest_run_id).first()

    if not baseline:
        raise HTTPException(status_code=404, detail="Baseline backtest not found")

    # Create Monte Carlo run record
    mc_run = MonteCarloRun(
        backtest_run_id=request.backtest_run_id,
        name=request.name,
        n_simulations=request.n_simulations,
        simulation_types=request.simulation_types,
        entry_delay_range={"min_days": request.entry_delay_min_days, "max_days": request.entry_delay_max_days},
        position_size_variation_pct=request.position_size_variation_pct,
        include_regime_changes=request.include_regime_changes,
        status="pending",
    )

    db.add(mc_run)
    db.commit()
    db.refresh(mc_run)

    return {
        "monte_carlo_id": mc_run.id,
        "status": "pending",
        "message": "Monte Carlo simulation queued",
    }


# =====================================================================
# Template Library Endpoints
# =====================================================================

@router.get("/templates")
async def list_strategy_templates(
    category: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
) -> List[Dict]:
    """List strategy templates"""
    query = db.query(StrategyTemplate)

    if category:
        query = query.filter(StrategyTemplate.category == category)

    templates = query.offset(skip).limit(limit).all()

    return [
        {
            "id": t.id,
            "name": t.name,
            "description": t.description,
            "category": t.category,
            "strategy_type": t.strategy_type,
            "risk_profile": t.risk_profile,
            "typical_win_rate": t.typical_win_rate,
            "typical_sharpe": t.typical_sharpe,
            "tags": t.tags,
        }
        for t in templates
    ]


@router.get("/templates/{template_id}")
async def get_strategy_template(
    template_id: int,
    db: Session = Depends(get_db),
) -> Dict:
    """Get strategy template details"""
    template = db.query(StrategyTemplate).filter(StrategyTemplate.id == template_id).first()

    if not template:
        raise HTTPException(status_code=404, detail="Template not found")

    return {
        "id": template.id,
        "name": template.name,
        "description": template.description,
        "category": template.category,
        "strategy_type": template.strategy_type,
        "template_config": template.template_config,
        "parameters_schema": template.parameters_schema,
        "default_parameters": template.default_parameters,
        "risk_profile": template.risk_profile,
        "tags": template.tags,
    }


@router.post("/templates/{template_id}/instantiate")
async def instantiate_template(
    template_id: int,
    parameters: Optional[Dict[str, Any]] = None,
    db: Session = Depends(get_db),
) -> Dict:
    """Create a strategy from a template"""
    template = db.query(StrategyTemplate).filter(StrategyTemplate.id == template_id).first()

    if not template:
        raise HTTPException(status_code=404, detail="Template not found")

    # Merge default parameters with provided parameters
    final_params = template.default_parameters or {}
    if parameters:
        final_params.update(parameters)

    # Create strategy from template
    strategy = StrategyModel(
        name=f"{template.name} Instance",
        description=f"Instantiated from template: {template.name}",
        strategy_type=template.strategy_type,
        template_id=template_id,
        parameters=final_params,
        yaml_config=template.template_config.get("yaml") if template.template_config else None,
        python_code=template.template_config.get("python") if template.template_config else None,
        visual_config=template.template_config.get("visual") if template.template_config else None,
    )

    db.add(strategy)
    db.commit()
    db.refresh(strategy)

    return {
        "strategy_id": strategy.id,
        "template_id": template_id,
        "name": strategy.name,
    }


# =====================================================================
# Utility Endpoints
# =====================================================================

@router.get("/runs")
async def list_backtest_runs(
    strategy_id: Optional[int] = None,
    status: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
) -> List[Dict]:
    """List all backtest runs"""
    query = db.query(BacktestRun)

    if strategy_id:
        query = query.filter(BacktestRun.strategy_id == strategy_id)

    if status:
        query = query.filter(BacktestRun.status == status)

    runs = query.order_by(BacktestRun.created_at.desc()).offset(skip).limit(limit).all()

    return [
        {
            "id": r.id,
            "strategy_id": r.strategy_id,
            "name": r.name,
            "status": r.status,
            "total_return": r.total_return,
            "sharpe_ratio": r.sharpe_ratio,
            "created_at": r.created_at.isoformat() if r.created_at else None,
        }
        for r in runs
    ]


@router.delete("/runs/{backtest_id}")
async def delete_backtest(
    backtest_id: int,
    db: Session = Depends(get_db),
) -> Dict:
    """Delete a backtest run"""
    backtest = db.query(BacktestRun).filter(BacktestRun.id == backtest_id).first()

    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")

    db.delete(backtest)
    db.commit()

    return {"message": "Backtest deleted successfully"}
