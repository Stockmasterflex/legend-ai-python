# Tax Optimization System - Quick Start Guide

## Key Findings Summary

### Current State
- **No existing tax functionality** - Complete greenfield opportunity
- **Strong trade tracking foundation** - Trade dataclass, API endpoints, statistics
- **Database infrastructure ready** - SQLAlchemy ORM, PostgreSQL, Alembic migrations
- **Redis caching available** - For high-performance lookups
- **Testing patterns established** - pytest with fixtures, mocking, async support

### Project Structure
```
Legend AI Platform
├── API Layer (25+ routes in /app/api/)
├── Service Layer (16+ services in /app/services/)
├── Core Logic (algorithms in /app/core/)
├── Database Models (SQLAlchemy in /app/models.py)
└── Tests (19 test files with pytest)
```

---

## Tax System Architecture (High Level)

```
User Interface
    ↓
/api/tax/* Endpoints (NEW)
    ↓
TaxOptimizer Service (NEW) ← CapitalGainsCalculator, WashSaleDetector, TaxHarvester
    ↓
Tax Models in Database (NEW) ← Position, TaxLot, CapitalGain, TaxHarvestLog tables
    ↓
Integration with Trade Service ← Enhanced Trade dataclass with tax fields
```

---

## Implementation Checklist

### Phase 1: Data Models (Week 1)

- [ ] **1.1 Extend `/app/models.py`** with 4 new tables:
  ```python
  class Position(Base)         # Track current holdings
  class TaxLot(Base)          # Track acquisition cost per lot
  class CapitalGain(Base)     # Track realized gains/losses
  class TaxHarvestLog(Base)   # Audit trail of tax strategies
  ```

- [ ] **1.2 Create Alembic migration**:
  ```bash
  alembic revision --autogenerate -m "Add tax optimization models"
  alembic upgrade head
  ```

- [ ] **1.3 Update Trade dataclass** in `/app/services/trades.py`:
  ```python
  @dataclass
  class Trade:
      # ... existing fields ...
      cost_basis: Optional[float] = None
      holding_period_days: Optional[int] = None
      is_long_term: Optional[bool] = None
      capital_gain: Optional[float] = None
      tax_impact: Optional[float] = None
  ```

### Phase 2: Core Tax Logic (Week 2)

- [ ] **2.1 Create `/app/core/tax_models.py`** with:
  ```python
  from enum import Enum
  from dataclasses import dataclass
  
  class CapitalGainType(Enum):
      SHORT_TERM = "short_term"   # < 365 days
      LONG_TERM = "long_term"     # >= 365 days
  
  class TaxStrategy(Enum):
      HARVEST_LOSS = "harvest_loss"
      HARVEST_GAIN = "harvest_gain"
      REBALANCE = "rebalance"
      WASH_SALE_PREVENTION = "wash_sale_prevention"
  
  @dataclass
  class CapitalGainResult:
      quantity: int
      acquisition_date: date
      disposition_date: date
      cost_basis: float
      sale_proceeds: float
      gain_loss: float
      holding_days: int
      is_long_term: bool
      gain_type: CapitalGainType
  
  @dataclass
  class WashSaleMatch:
      original_symbol: str
      original_sale_date: date
      loss_amount: float
      wash_sale_dates: tuple  # (start, end)
      replacement_symbols: list[str]
      disallowed_loss: float
  
  @dataclass
  class TaxHarvestOpportunity:
      symbol: str
      current_price: float
      cost_basis: float
      unrealized_loss: float
      estimated_tax_savings: float
      recommended_action: str
  ```

- [ ] **2.2 Implement CapitalGainsCalculator** with methods:
  ```python
  def calculate_capital_gain(
      acquisition_date: date,
      disposition_date: date,
      cost_basis: float,
      sale_proceeds: float
  ) -> CapitalGainResult
  
  def determine_holding_period(
      acquisition_date: date,
      disposition_date: date
  ) -> int  # days held
  
  def classify_gain_type(
      holding_days: int
  ) -> CapitalGainType  # ST/LT
  ```

- [ ] **2.3 Implement WashSaleDetector** with methods:
  ```python
  def detect_wash_sales(
      transactions: List[Trade],
      lookback_days: int = 30
  ) -> List[WashSaleMatch]
  
  def calculate_disallowed_loss(
      loss_amount: float,
      replacement_cost: float
  ) -> float
  
  def find_replacement_purchases(
      sold_ticker: str,
      sale_date: date,
      lookback_days: int,
      lookforward_days: int
  ) -> List[str]  # Similar security symbols
  ```

### Phase 3: Service Implementation (Week 2-3)

- [ ] **3.1 Create `/app/services/tax_optimizer.py`** with:
  ```python
  class TaxOptimizer:
      def __init__(self):
          self.capital_gains_calc = CapitalGainsCalculator()
          self.wash_sale_detector = WashSaleDetector()
          self.tax_harvester = TaxHarvester()
          self.rebalancer = PortfolioRebalancer()
          self.report_gen = TaxReportGenerator()
      
      async def calculate_capital_gains(trades: List[Trade]) -> Dict
      async def detect_wash_sales(trades: List[Trade]) -> List[WashSaleMatch]
      async def identify_harvest_opportunities(portfolio: Dict) -> List[HarvestOption]
      async def estimate_tax_impact(transaction: Trade, tax_rate: float) -> TaxImpact
      async def rebalance_efficiently(portfolio: Dict, target: Dict) -> Result
      async def generate_tax_report(date_range: Tuple) -> TaxReport
  
  def get_tax_optimizer() -> TaxOptimizer:
      """Singleton accessor"""
      global _tax_optimizer
      if _tax_optimizer is None:
          _tax_optimizer = TaxOptimizer()
      return _tax_optimizer
  ```

- [ ] **3.2 Implement helper classes**:
  ```python
  class TaxHarvester:
      async def identify_losses_to_harvest(
          portfolio: Dict,
          min_loss: float = 100  # Harvest losses over $100
      ) -> List[HarvestOpportunity]
      
      async def suggest_replacement_positions(
          harvested_ticker: str,
          portfolio: Dict
      ) -> List[str]  # Similar securities
  
  class PortfolioRebalancer:
      async def calculate_tax_efficient_rebalance(
          current_allocation: Dict,
          target_allocation: Dict,
          tax_rate: float
      ) -> RebalanceResult
  
  class TaxReportGenerator:
      async def generate_annual_report(
          year: int
      ) -> Dict  # Summary of all gains/losses
      
      async def generate_pdf_report(
          year: int
      ) -> bytes  # PDF format
  ```

### Phase 4: API Endpoints (Week 3)

- [ ] **4.1 Create `/app/api/tax_optimization.py`** with endpoints:

  ```python
  from fastapi import APIRouter, HTTPException
  from pydantic import BaseModel
  
  router = APIRouter(prefix="/api/tax", tags=["tax"])
  
  class CalculateGainsRequest(BaseModel):
      trades: List[Dict]  # Closed trades
  
  class CalculateGainsResponse(BaseModel):
      total_gain_loss: float
      short_term_gains: float
      long_term_gains: float
      by_ticker: Dict[str, Dict]
  
  @router.post("/calculate-gains")
  async def calculate_capital_gains(request: CalculateGainsRequest):
      """Calculate capital gains from closed trades"""
      optimizer = get_tax_optimizer()
      result = await optimizer.calculate_capital_gains(request.trades)
      return CalculateGainsResponse(**result)
  
  @router.post("/detect-wash-sales")
  async def detect_wash_sales(request: DetectWashSalesRequest):
      """Identify wash sale violations"""
      optimizer = get_tax_optimizer()
      violations = await optimizer.detect_wash_sales(request.trades)
      return {"wash_sales": violations}
  
  @router.post("/harvest-losses")
  async def harvest_losses(request: HarvestRequest):
      """Get tax loss harvesting recommendations"""
      optimizer = get_tax_optimizer()
      opportunities = await optimizer.identify_harvest_opportunities(
          request.portfolio
      )
      return {"opportunities": opportunities}
  
  @router.post("/estimate-impact")
  async def estimate_tax_impact(request: EstimateImpactRequest):
      """Estimate tax impact of a trade"""
      optimizer = get_tax_optimizer()
      impact = await optimizer.estimate_tax_impact(
          request.trade,
          request.tax_rate
      )
      return {"impact": impact}
  
  @router.post("/rebalance-efficiently")
  async def rebalance_efficiently(request: RebalanceRequest):
      """Get tax-efficient rebalancing suggestions"""
      optimizer = get_tax_optimizer()
      result = await optimizer.rebalance_efficiently(
          request.current_allocation,
          request.target_allocation
      )
      return {"rebalance": result}
  
  @router.get("/report")
  async def get_tax_report(year: int = None):
      """Generate annual tax report"""
      optimizer = get_tax_optimizer()
      if year is None:
          year = datetime.now().year
      report = await optimizer.generate_annual_report(year)
      return {"report": report}
  
  @router.get("/summary")
  async def get_tax_summary():
      """Get YTD tax summary"""
      optimizer = get_tax_optimizer()
      trades = await get_trade_manager().get_closed_trades(limit=1000)
      summary = await optimizer.calculate_capital_gains(trades)
      return {"summary": summary}
  ```

- [ ] **4.2 Update `/app/main.py`** to register router:
  ```python
  from app.api.tax_optimization import router as tax_router
  # ...
  app.include_router(tax_router)
  ```

- [ ] **4.3 Update `/app/config.py`** with tax settings:
  ```python
  class Settings(BaseSettings):
      # ... existing ...
      tax_rate_short_term: float = 0.37  # Configurable tax rates
      tax_rate_long_term: float = 0.20
      wash_sale_lookback_days: int = 30
      wash_sale_lookahead_days: int = 30
  ```

### Phase 5: Testing (Week 4)

- [ ] **5.1 Create `/tests/test_tax_optimization.py`**:
  ```python
  import pytest
  from app.services.tax_optimizer import get_tax_optimizer
  from app.core.tax_models import CapitalGainType
  
  @pytest.mark.asyncio
  async def test_calculate_capital_gains():
      optimizer = get_tax_optimizer()
      trades = [
          # Mock trades...
      ]
      result = await optimizer.calculate_capital_gains(trades)
      assert result["total_gain_loss"] > 0
  
  @pytest.mark.asyncio
  async def test_detect_wash_sales():
      optimizer = get_tax_optimizer()
      violations = await optimizer.detect_wash_sales(trades)
      assert len(violations) > 0
      assert violations[0].loss_amount > 0
  
  @pytest.mark.asyncio
  async def test_harvest_opportunities():
      optimizer = get_tax_optimizer()
      opportunities = await optimizer.identify_harvest_opportunities(portfolio)
      assert len(opportunities) > 0
  ```

- [ ] **5.2 Create `/tests/test_tax_api.py`**:
  ```python
  def test_calculate_gains_endpoint(client):
      response = client.post("/api/tax/calculate-gains", json={
          "trades": [...]
      })
      assert response.status_code == 200
      data = response.json()
      assert "total_gain_loss" in data
  ```

- [ ] **5.3 Run tests**:
  ```bash
  pytest tests/test_tax_* -v --cov=app.services.tax_optimizer
  ```

### Phase 6: Integration & Documentation (Week 5)

- [ ] **6.1 Update trade endpoints** to include tax info in responses
- [ ] **6.2 Create documentation** in `/docs/tax_optimization.md`
- [ ] **6.3 Add tax fields** to dashboard/UI
- [ ] **6.4 Production testing** with real trade data

---

## Code Organization Reference

### New Files to Create
```
app/
├── api/
│   └── tax_optimization.py              # ~300 lines
├── core/
│   └── tax_models.py                    # ~200 lines
├── services/
│   └── tax_optimizer.py                 # ~600 lines
│       ├── TaxOptimizer
│       ├── CapitalGainsCalculator
│       ├── WashSaleDetector
│       ├── TaxHarvester
│       ├── PortfolioRebalancer
│       └── TaxReportGenerator
└── tests/
    ├── test_tax_optimization.py         # ~300 lines
    └── test_tax_api.py                  # ~200 lines
```

### Files to Modify
```
app/
├── models.py                            # Add 4 new tables
├── main.py                              # Add router registration
├── config.py                            # Add tax-related settings
└── services/
    └── trades.py                        # Extend Trade dataclass
```

---

## Key Dependencies

Already in requirements.txt:
- fastapi, asyncio
- sqlalchemy, alembic
- redis
- pydantic
- pandas, numpy
- pytest, pytest-asyncio

Optional additions:
- `python-dateutil` - For date calculations
- `reportlab` - For PDF report generation

---

## Integration Points

1. **Trade Creation**: Create TaxLot record
2. **Trade Closing**: Calculate CapitalGain, check wash sales
3. **Statistics**: Include tax impact in trade stats
4. **Dashboard**: Show tax summary and opportunities
5. **Reporting**: Generate tax reports for compliance

---

## Testing Strategy

- **Unit Tests**: Individual tax calculations
- **Integration Tests**: Trade → Tax flow
- **Contract Tests**: API response formats
- **Performance Tests**: Large portfolio analysis

---

## Deployment Notes

1. Run Alembic migrations before deploying
2. Test with historical trade data
3. Validate capital gains calculations against manual computation
4. Monitor for edge cases (splits, dividends, etc.)
5. Keep audit trail for all tax decisions

---

## Success Criteria

- All trades have associated tax lots
- Capital gains calculated within 0.01% of manual verification
- Wash sales detected and reported accurately
- Tax harvesting recommendations save >5% on taxes
- All API endpoints tested with 80%+ coverage
- Documentation complete and tested

