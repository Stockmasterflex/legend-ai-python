# Enterprise Backtesting Platform

Comprehensive backtesting framework for Legend AI with strategy definition, walk-forward optimization, Monte Carlo simulation, and machine learning integration.

## Overview

The Enterprise Backtesting Platform provides institutional-grade backtesting capabilities with:

- **Strategy Definition Language**: YAML, Python, and Visual strategy builders
- **Realistic Execution Simulation**: Slippage, commissions, market impact, partial fills
- **Walk-Forward Optimization**: Rolling window testing with out-of-sample validation
- **Monte Carlo Analysis**: Random entry timing, position size variation, market regimes
- **ML Integration**: Feature engineering, model training, hyperparameter optimization, ensembles

## Architecture

```
app/backtesting/
├── __init__.py                 # Main exports
├── strategy.py                 # Base strategy framework
├── portfolio.py                # Portfolio management
├── execution.py                # Execution simulator
├── engine.py                   # Backtesting engine
├── metrics.py                  # Performance metrics
├── walk_forward.py             # Walk-forward optimization
├── monte_carlo.py              # Monte Carlo simulation
├── ml/                         # Machine learning
│   ├── features.py             # Feature engineering
│   ├── models.py               # Model training
│   ├── optimization.py         # Hyperparameter optimization
│   └── ensemble.py             # Ensemble methods
├── strategies/                 # Pre-built strategies
│   ├── vcp_strategy.py         # VCP pattern strategy
│   ├── minervini_strategy.py   # Minervini template
│   └── cup_handle_strategy.py  # Cup & Handle
└── templates/                  # YAML templates
    └── vcp_breakout.yaml       # VCP template
```

## Features

### 1. Strategy Definition Language

Define strategies using YAML, Python, or Visual builder:

#### YAML Strategy Example

```yaml
name: "VCP Breakout Strategy"
description: "Enters on VCP pattern completion"

parameters:
  min_vcp_score: 70.0
  risk_per_trade: 0.02
  reward_ratio: 3.0

indicators:
  - name: sma_50
    type: SMA
    parameters:
      period: 50

entry_rules:
  operator: AND
  conditions:
    - indicator: sma_50
      operator: ">"
      value: sma_200

exit_rules:
  operator: OR
  conditions:
    - type: stop_loss
      multiplier: 2.0
    - type: take_profit
      multiplier: 3.0
```

#### Python Strategy Example

```python
from app.backtesting.strategy import Strategy, Signal, SignalType

class CustomStrategy(Strategy):
    async def on_data(self, ticker, data, timestamp, portfolio_value, cash):
        signals = []

        # Custom logic here
        if self._should_buy(ticker, data):
            signal = Signal(
                type=SignalType.BUY,
                ticker=ticker,
                timestamp=timestamp,
                price=data.iloc[-1]["close"],
                stop_loss=self._calculate_stop(data),
                take_profit=self._calculate_target(data),
            )
            signals.append(signal)

        return signals

    async def calculate_position_size(self, signal, portfolio_value, cash, current_price):
        # Position sizing logic
        risk_amount = portfolio_value * 0.02
        risk_per_share = abs(current_price - signal.stop_loss)
        return int(risk_amount / risk_per_share)
```

### 2. Execution Simulation

Realistic order execution with multiple models:

```python
from app.backtesting.execution import (
    ExecutionSimulator,
    CommissionModel,
    SlippageModel,
    MarketImpactModel,
)

# Configure execution
simulator = ExecutionSimulator(
    commission_model=CommissionModel(
        type="per_share",
        value=0.005,  # $0.005 per share
        minimum=1.0,
    ),
    slippage_model=SlippageModel(
        type="volume_based",
        value=0.02,  # 2% of participation rate
    ),
    market_impact_model=MarketImpactModel(
        enabled=True,
        impact_coefficient=0.1,
    ),
)

# Execute order
result = simulator.execute_order(
    quantity=1000,
    price=50.0,
    is_buy=True,
    volume=1000000,
)
```

### 3. Walk-Forward Optimization

Rolling window optimization with overfitting detection:

```python
from app.backtesting.walk_forward import WalkForwardOptimizer, WalkForwardConfig

config = WalkForwardConfig(
    strategy=strategy,
    start_date=datetime(2020, 1, 1),
    end_date=datetime(2023, 12, 31),
    initial_capital=100000,
    universe=["AAPL", "MSFT", "GOOGL"],

    # Window configuration
    in_sample_days=252,   # 1 year in-sample
    out_sample_days=63,   # 3 months out-of-sample
    step_days=63,         # Roll forward quarterly

    # Optimization
    parameter_ranges={
        "stop_multiplier": [1.5, 2.0, 2.5, 3.0],
        "reward_ratio": [2.0, 3.0, 4.0],
    },
    optimization_metric="sharpe_ratio",
)

optimizer = WalkForwardOptimizer(config)
results = await optimizer.run()

print(f"Overfitting Score: {results['overfitting_score']:.2f}")
print(f"Robust Parameters: {results['robust_parameters']}")
```

### 4. Monte Carlo Simulation

Test strategy robustness through randomized simulations:

```python
from app.backtesting.monte_carlo import MonteCarloEngine, MonteCarloConfig

config = MonteCarloConfig(
    baseline_backtest_results=baseline_results,
    strategy=strategy,
    start_date=datetime(2020, 1, 1),
    end_date=datetime(2023, 12, 31),
    initial_capital=100000,
    universe=["AAPL", "MSFT"],

    # Simulations
    n_simulations=1000,
    simulation_types=["random_entry", "position_size", "regime"],

    # Variations
    entry_delay_min_days=-5,
    entry_delay_max_days=5,
    position_size_variation_pct=20.0,
    include_regime_changes=True,
)

mc_engine = MonteCarloEngine(config)
results = await mc_engine.run()

print(f"Mean Return: {results['mean_return']:.2f}%")
print(f"95% CI: [{results['ci_95_lower_return']:.2f}%, {results['ci_95_upper_return']:.2f}%]")
print(f"Probability of Profit: {results['probability_of_profit']:.1f}%")
```

### 5. Machine Learning Integration

#### Feature Engineering

```python
from app.backtesting.ml import FeatureEngineer, FeatureConfig

config = FeatureConfig(
    feature_groups=["price", "technical", "volume", "pattern"],
    lookback_periods=[5, 10, 20, 50, 200],
    include_ratios=True,
    include_lagged=True,
)

engineer = FeatureEngineer(config)
features = engineer.transform(data)  # OHLCV DataFrame
labels = engineer.create_labels(data, target_type="classification", threshold=0.02)
```

#### Model Training

```python
from app.backtesting.ml import MLModel, ModelConfig, ModelType

config = ModelConfig(
    model_type=ModelType.RANDOM_FOREST_CLASSIFIER,
    hyperparameters={
        "n_estimators": 100,
        "max_depth": 10,
    },
)

model = MLModel(config)
metrics = model.train(features, labels)

print(f"Test Accuracy: {metrics['test_accuracy']:.4f}")
print(f"AUC: {metrics['test_auc']:.4f}")
```

#### Hyperparameter Optimization

```python
from app.backtesting.ml import HyperparameterOptimizer, OptimizationConfig

config = OptimizationConfig(
    model_type=ModelType.RANDOM_FOREST_CLASSIFIER,
    parameter_space={
        "n_estimators": [50, 100, 200],
        "max_depth": [5, 10, 20],
        "min_samples_split": [2, 5, 10],
    },
    optimization_type="bayesian",
    n_trials=100,
    objective_metric="val_auc",
)

optimizer = HyperparameterOptimizer(config)
results = await optimizer.optimize(X, y)

print(f"Best Parameters: {results['best_params']}")
print(f"Best Score: {results['best_score']:.4f}")
```

#### Ensemble Methods

```python
from app.backtesting.ml import EnsembleModel, EnsembleConfig, EnsembleType

config = EnsembleConfig(
    ensemble_type=EnsembleType.STACKING,
    member_models=[model1, model2, model3],
    meta_learner="logistic",
)

ensemble = EnsembleModel(config)
metrics = ensemble.train(X_train, y_train)

diversity = ensemble.get_diversity_metrics(X_val, y_val)
print(f"Diversity Score: {diversity['diversity_score']:.4f}")
```

## API Endpoints

### Strategy Management

```bash
# Create strategy
POST /api/backtest/strategies
{
  "name": "My VCP Strategy",
  "strategy_type": "yaml",
  "yaml_config": "...",
  "parameters": {...}
}

# List strategies
GET /api/backtest/strategies

# Get strategy details
GET /api/backtest/strategies/{id}
```

### Run Backtest

```bash
POST /api/backtest/run
{
  "strategy_id": 1,
  "name": "VCP Backtest 2020-2023",
  "start_date": "2020-01-01T00:00:00",
  "end_date": "2023-12-31T00:00:00",
  "initial_capital": 100000,
  "universe": ["AAPL", "MSFT", "GOOGL"],
  "commission_type": "per_share",
  "commission_value": 0.005,
  "slippage_type": "fixed_bps",
  "slippage_value": 5.0
}

# Get backtest status
GET /api/backtest/runs/{id}

# Get backtest trades
GET /api/backtest/runs/{id}/trades
```

### Walk-Forward Optimization

```bash
POST /api/backtest/walk-forward
{
  "strategy_id": 1,
  "name": "WF Optimization",
  "start_date": "2020-01-01T00:00:00",
  "end_date": "2023-12-31T00:00:00",
  "in_sample_days": 252,
  "out_sample_days": 63,
  "parameter_ranges": {
    "stop_multiplier": [1.5, 2.0, 2.5],
    "reward_ratio": [2.0, 3.0, 4.0]
  },
  "optimization_type": "grid"
}
```

### Monte Carlo Simulation

```bash
POST /api/backtest/monte-carlo
{
  "backtest_run_id": 1,
  "name": "Monte Carlo Analysis",
  "n_simulations": 1000,
  "simulation_types": ["random_entry", "position_size"],
  "entry_delay_min_days": -5,
  "entry_delay_max_days": 5,
  "position_size_variation_pct": 20.0
}
```

### Template Library

```bash
# List templates
GET /api/backtest/templates?category=Pattern-Based

# Get template
GET /api/backtest/templates/{id}

# Instantiate template
POST /api/backtest/templates/{id}/instantiate
{
  "parameters": {
    "risk_per_trade": 0.02
  }
}
```

## Performance Metrics

The platform calculates comprehensive performance metrics:

### Return Metrics
- Total Return
- Annualized Return
- Cumulative Return

### Risk-Adjusted Metrics
- Sharpe Ratio
- Sortino Ratio
- Calmar Ratio
- Omega Ratio

### Risk Metrics
- Maximum Drawdown
- Maximum Drawdown Duration
- Volatility (Annualized)
- Downside Deviation
- Value at Risk (VaR 95%)
- Conditional VaR (CVaR 95%)

### Trade Statistics
- Total Trades
- Win Rate
- Profit Factor
- Average Win/Loss
- Largest Win/Loss
- Expectancy
- Average Hold Time
- R-Multiples

### Relative Metrics
- Alpha (vs benchmark)
- Beta (vs benchmark)

## Database Models

The platform uses the following database tables:

- `strategies` - Strategy definitions
- `strategy_templates` - Pre-built templates
- `backtest_runs` - Backtest execution records
- `backtest_trades` - Individual trades
- `backtest_metrics` - Time-series metrics
- `walk_forward_runs` - Walk-forward optimization runs
- `walk_forward_windows` - Individual windows
- `monte_carlo_runs` - Monte Carlo simulations
- `monte_carlo_simulations` - Individual simulation results
- `ml_models` - ML model records
- `hyperparameter_optimizations` - Optimization runs
- `ensemble_models` - Ensemble configurations

## Dependencies

Required packages (add to `requirements.txt`):

```
pandas>=2.2.0
numpy>=1.26.0
scikit-learn>=1.3.0
scipy>=1.11.0
pyyaml>=6.0.0
optuna>=3.0.0  # Optional, for Bayesian optimization
```

## Usage Examples

### Complete Backtest Example

```python
import asyncio
from datetime import datetime
from app.backtesting import BacktestEngine, BacktestConfig
from app.backtesting.strategies import VCPStrategy
from app.backtesting.execution import ExecutionSimulator

async def run_backtest():
    # Create strategy
    strategy = VCPStrategy(
        name="VCP Breakout",
        parameters={
            "min_score": 75.0,
            "risk_per_trade": 0.02,
            "reward_ratio": 3.0,
        }
    )

    # Configure execution
    execution = ExecutionSimulator.get_realistic_config("retail")

    # Create backtest config
    config = BacktestConfig(
        strategy=strategy,
        start_date=datetime(2020, 1, 1),
        end_date=datetime(2023, 12, 31),
        initial_capital=100000,
        universe=["AAPL", "MSFT", "GOOGL", "NVDA"],
        execution_simulator=execution,
        data_provider=your_data_provider,  # Implement this
    )

    # Run backtest
    engine = BacktestEngine(config)
    results = await engine.run()

    # Display results
    print(f"Total Return: {results['performance']['total_return']:.2f}%")
    print(f"Sharpe Ratio: {results['performance']['sharpe_ratio']:.2f}")
    print(f"Max Drawdown: {results['performance']['max_drawdown']:.2f}%")
    print(f"Win Rate: {results['performance']['win_rate']:.1f}%")
    print(f"Total Trades: {results['performance']['total_trades']}")

asyncio.run(run_backtest())
```

## Best Practices

1. **Always use walk-forward optimization** to avoid overfitting
2. **Run Monte Carlo simulations** to understand strategy robustness
3. **Include realistic execution costs** (slippage, commissions, market impact)
4. **Test on out-of-sample data** before live trading
5. **Monitor overfitting scores** during optimization
6. **Use ensemble methods** for ML-based strategies
7. **Track MAE/MFE** to optimize exit strategies
8. **Calculate confidence intervals** for expected returns

## Troubleshooting

### Common Issues

1. **Memory errors with large backtests**: Reduce universe size or use chunked processing
2. **Slow optimization**: Use random/bayesian search instead of grid search
3. **Unrealistic results**: Check execution simulation parameters
4. **Overfitting**: Increase out-of-sample period, reduce parameter count

## Contributing

When adding new features:

1. Follow the existing architecture patterns
2. Add comprehensive docstrings
3. Include unit tests
4. Update this README
5. Add API endpoints if applicable

## License

MIT License - See LICENSE file for details

---

**Legend AI Enterprise Backtesting Platform** - Built for serious traders and quantitative analysts.
