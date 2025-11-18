"""
Comprehensive tests for Tax Optimization functionality.
Tests wash sale detection, tax loss harvesting, gain/loss reporting, and exports.
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, MagicMock, patch
from datetime import datetime, timedelta
import json

from app.main import app
from app.core.tax_models import (
    HoldingPeriod, WashSaleStatus, TaxBracket,
    calculate_holding_period, is_wash_sale_violation
)


@pytest.fixture
def client():
    """Test client fixture"""
    return TestClient(app)


@pytest.fixture
def mock_cache():
    """Mock Redis cache"""
    cache = AsyncMock()
    cache._get_redis = AsyncMock()
    redis_mock = AsyncMock()
    cache._get_redis.return_value = redis_mock
    return cache, redis_mock


# ==================== Health & Status ====================

def test_tax_health_endpoint(client):
    """Test tax service health check"""
    response = client.get("/api/tax/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "wash_sale_detection" in data["features"]
    assert "tax_loss_harvesting" in data["features"]


# ==================== Core Helper Functions ====================

def test_calculate_holding_period_short_term():
    """Test short-term holding period calculation"""
    purchase = datetime(2024, 1, 1)
    sale = datetime(2024, 6, 1)  # 5 months
    period = calculate_holding_period(purchase, sale)
    assert period == HoldingPeriod.SHORT_TERM


def test_calculate_holding_period_long_term():
    """Test long-term holding period calculation"""
    purchase = datetime(2023, 1, 1)
    sale = datetime(2024, 6, 1)  # 1.5 years
    period = calculate_holding_period(purchase, sale)
    assert period == HoldingPeriod.LONG_TERM


def test_wash_sale_violation_within_30_days():
    """Test wash sale violation detection within 30 days"""
    loss_date = datetime(2024, 6, 1)
    purchase_date = datetime(2024, 6, 15)  # 14 days after
    assert is_wash_sale_violation(loss_date, purchase_date) is True


def test_wash_sale_violation_before_30_days():
    """Test wash sale violation detection 30 days before"""
    loss_date = datetime(2024, 6, 1)
    purchase_date = datetime(2024, 5, 5)  # 27 days before
    assert is_wash_sale_violation(loss_date, purchase_date) is True


def test_no_wash_sale_violation_after_30_days():
    """Test no wash sale violation after 30 days"""
    loss_date = datetime(2024, 6, 1)
    purchase_date = datetime(2024, 7, 5)  # 34 days after
    assert is_wash_sale_violation(loss_date, purchase_date) is False


# ==================== Wash Sale Detection API ====================

@patch("app.api.tax.get_wash_sale_detector")
def test_check_wash_sale_violation(mock_detector, client):
    """Test wash sale check endpoint - violation case"""
    from app.core.tax_models import WashSaleCheck

    # Setup mock
    detector = AsyncMock()
    mock_detector.return_value = detector

    wash_sale_check = WashSaleCheck(
        is_violation=True,
        days_until_safe=15,
        conflicting_transactions=[
            {
                'lot_id': 'lot123',
                'purchase_date': datetime(2024, 6, 15),
                'quantity': 100,
                'price_per_share': 150.0,
                'days_from_sale': 14
            }
        ],
        disallowed_loss=500.0,
        adjusted_cost_basis=500.0
    )

    detector.check_wash_sale = AsyncMock(return_value=wash_sale_check)
    detector.get_suggested_alternatives = AsyncMock(return_value=[])

    response = client.post(
        "/api/tax/wash-sale/check",
        json={
            "symbol": "AAPL",
            "sale_date": "2024-06-01T00:00:00",
            "loss_amount": -500.0,
            "user_id": "test_user"
        }
    )

    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["wash_sale"]["is_violation"] is True
    assert data["wash_sale"]["days_until_safe"] == 15
    assert "IRS 30-day rule applies" in data["wash_sale"]["warning"]


@patch("app.api.tax.get_wash_sale_detector")
def test_check_wash_sale_clean(mock_detector, client):
    """Test wash sale check endpoint - clean case"""
    from app.core.tax_models import WashSaleCheck

    detector = AsyncMock()
    mock_detector.return_value = detector

    wash_sale_check = WashSaleCheck(
        is_violation=False,
        days_until_safe=0,
        conflicting_transactions=[],
        disallowed_loss=0.0,
        adjusted_cost_basis=0.0
    )

    detector.check_wash_sale = AsyncMock(return_value=wash_sale_check)

    response = client.post(
        "/api/tax/wash-sale/check",
        json={
            "symbol": "AAPL",
            "sale_date": "2024-06-01T00:00:00",
            "loss_amount": -500.0
        }
    )

    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["wash_sale"]["is_violation"] is False


@patch("app.api.tax.get_wash_sale_detector")
def test_get_wash_sale_alternatives(mock_detector, client):
    """Test wash sale alternatives endpoint"""
    from app.core.tax_models import ReplacementSecurity

    detector = AsyncMock()
    mock_detector.return_value = detector

    alternatives = [
        ReplacementSecurity(
            symbol="MSFT",
            name="Microsoft Corporation",
            similarity_score=0.85,
            correlation=0.75,
            sector="Technology",
            current_price=380.0,
            wash_sale_safe=True,
            reasons=["Same sector", "Similar market cap"]
        )
    ]

    detector.get_suggested_alternatives = AsyncMock(return_value=alternatives)

    response = client.get("/api/tax/wash-sale/alternatives/AAPL?count=5")

    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["symbol"] == "AAPL"
    assert len(data["alternatives"]) == 1
    assert data["alternatives"][0]["symbol"] == "MSFT"


# ==================== Tax Loss Harvesting API ====================

@patch("app.api.tax.get_tax_loss_harvester")
def test_get_harvest_opportunities(mock_harvester, client):
    """Test harvest opportunities endpoint"""
    from app.core.tax_models import TaxHarvestOpportunity

    harvester = AsyncMock()
    mock_harvester.return_value = harvester

    opportunities = [
        TaxHarvestOpportunity(
            symbol="TSLA",
            tax_lot_id=1,
            unrealized_loss=-1000.0,
            current_price=200.0,
            cost_basis=2500.0,
            quantity=10,
            estimated_tax_savings=240.0,
            replacement_suggestions=[],
            days_until_wash_safe=31
        )
    ]

    harvester.identify_opportunities = AsyncMock(return_value=opportunities)

    response = client.get(
        "/api/tax/harvest/opportunities?user_id=test&min_loss=100&tax_bracket=0.24"
    )

    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["count"] == 1
    assert data["total_potential_savings"] == 240.0
    assert len(data["opportunities"]) == 1


@patch("app.api.tax.get_tax_loss_harvester")
def test_execute_harvest(mock_harvester, client):
    """Test execute harvest endpoint"""
    harvester = AsyncMock()
    mock_harvester.return_value = harvester

    result = {
        'success': True,
        'symbol': 'TSLA',
        'loss': -1000.0,
        'tax_savings_estimate': 240.0,
        'replacement_symbol': 'GM',
        'wash_sale_safe_date': (datetime.now() + timedelta(days=31)).isoformat()
    }

    harvester.execute_harvest = AsyncMock(return_value=result)

    response = client.post(
        "/api/tax/harvest/execute",
        json={
            "tax_lot_id": 1,
            "replacement_symbol": "GM",
            "user_id": "test"
        }
    )

    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["harvest"]["symbol"] == "TSLA"
    assert "Successfully harvested" in data["harvest"]["message"]


# ==================== Gain/Loss Reporting API ====================

@patch("app.api.tax.get_gains_calculator")
def test_get_gains_losses_report(mock_calculator, client):
    """Test gain/loss report endpoint"""
    from app.core.tax_models import GainLossReport, CapitalGainModel

    calculator = AsyncMock()
    mock_calculator.return_value = calculator

    report = GainLossReport(
        tax_year=2024,
        short_term_gains=5000.0,
        short_term_losses=-1000.0,
        long_term_gains=10000.0,
        long_term_losses=-500.0,
        net_short_term=4000.0,
        net_long_term=9500.0,
        total_net_gain_loss=13500.0,
        wash_sale_adjustments=100.0,
        realized_gains=[
            CapitalGainModel(
                symbol="AAPL",
                quantity=100,
                sale_price=180.0,
                sale_date=datetime(2024, 6, 1),
                proceeds=18000.0,
                cost_basis=15000.0,
                adjusted_cost_basis=15000.0,
                gain_loss=3000.0,
                holding_period=HoldingPeriod.SHORT_TERM,
                tax_year=2024
            )
        ],
        unrealized_gains=[]
    )

    calculator.calculate_realized_gains = AsyncMock(return_value=report)

    response = client.get("/api/tax/report/gains-losses?user_id=test&tax_year=2024")

    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["tax_year"] == 2024
    assert data["realized_count"] == 1


@patch("app.api.tax.get_gains_calculator")
def test_get_tax_estimate(mock_calculator, client):
    """Test tax estimate endpoint"""
    from app.core.tax_models import GainLossReport, TaxEstimate

    calculator = AsyncMock()
    mock_calculator.return_value = calculator

    report = GainLossReport(
        tax_year=2024,
        short_term_gains=5000.0,
        short_term_losses=0.0,
        long_term_gains=10000.0,
        long_term_losses=0.0,
        net_short_term=5000.0,
        net_long_term=10000.0,
        total_net_gain_loss=15000.0,
        wash_sale_adjustments=0.0,
        realized_gains=[],
        unrealized_gains=[]
    )

    tax_estimate = TaxEstimate(
        short_term_tax=1200.0,
        long_term_tax=1500.0,
        total_tax=2700.0,
        effective_rate=18.0,
        marginal_rate=24.0,
        ordinary_income_bracket=TaxBracket.BRACKET_24,
        capital_gains_bracket=None
    )

    calculator.calculate_realized_gains = AsyncMock(return_value=report)
    calculator.estimate_tax_impact = AsyncMock(return_value=tax_estimate)

    response = client.post(
        "/api/tax/report/tax-estimate",
        json={
            "ordinary_income": 100000.0,
            "filing_status": "single",
            "user_id": "test",
            "tax_year": 2024
        }
    )

    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "total_tax" in data["tax_estimate"]


# ==================== Scenario Planning API ====================

@patch("app.api.tax.get_scenario_planner")
def test_analyze_sale_timing(mock_planner, client):
    """Test sale timing scenario analysis"""
    from app.core.tax_models import ScenarioAnalysis

    planner = AsyncMock()
    mock_planner.return_value = planner

    scenarios = [
        ScenarioAnalysis(
            scenario_name="Sell Now (Short-Term)",
            description="Sell immediately at short-term rate",
            current_gain_loss=5000.0,
            projected_gain_loss=5000.0,
            current_tax=1200.0,
            projected_tax=1200.0,
            tax_savings=0.0,
            recommended_actions=["Sell now"],
            assumptions={'tax_rate': 0.24}
        ),
        ScenarioAnalysis(
            scenario_name="Wait for Long-Term",
            description="Hold for >1 year",
            current_gain_loss=5000.0,
            projected_gain_loss=5000.0,
            current_tax=1200.0,
            projected_tax=750.0,
            tax_savings=450.0,
            recommended_actions=["Wait for long-term treatment"],
            assumptions={'tax_rate': 0.15}
        )
    ]

    planner.analyze_sale_timing = AsyncMock(return_value=scenarios)

    response = client.post(
        "/api/tax/scenario/sale-timing",
        json={
            "symbol": "AAPL",
            "quantity": 100,
            "current_gain": 5000.0,
            "user_id": "test"
        }
    )

    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert len(data["scenarios"]) == 2
    assert data["best_scenario"] == "Wait for Long-Term"


# ==================== Export API ====================

@patch("app.api.tax.get_tax_exporter")
def test_export_turbotax(mock_exporter, client):
    """Test TurboTax CSV export"""
    exporter = AsyncMock()
    mock_exporter.return_value = exporter

    csv_data = """Security Name,Symbol,Shares,Date Acquired,Date Sold,Sales Price,Cost Basis,Gain/Loss,Term
AAPL Corporation,AAPL,100,01/01/2024,06/01/2024,180.00,150.00,3000.00,Short
"""

    exporter.export_turbotax_csv = AsyncMock(return_value=csv_data)

    response = client.get("/api/tax/export/turbotax?user_id=test&tax_year=2024")

    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["format"] == "turbotax_csv"
    assert "csv_data" in data
    assert "instructions" in data


@patch("app.api.tax.get_tax_exporter")
def test_export_form_8949(mock_exporter, client):
    """Test Form 8949 export"""
    from app.core.tax_models import Form8949Entry

    exporter = AsyncMock()
    mock_exporter.return_value = exporter

    entries = [
        Form8949Entry(
            description="100 shares AAPL",
            date_acquired="01/01/2024",
            date_sold="06/01/2024",
            proceeds=18000.0,
            cost_basis=15000.0,
            adjustment_code=None,
            adjustment_amount=0.0,
            gain_loss=3000.0
        )
    ]

    exporter.export_form_8949 = AsyncMock(return_value=entries)

    response = client.get("/api/tax/export/form-8949?user_id=test&tax_year=2024")

    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["form"] == "8949"
    assert len(data["entries"]) == 1


@patch("app.api.tax.get_tax_exporter")
def test_export_cpa_report(mock_exporter, client):
    """Test CPA report export"""
    exporter = AsyncMock()
    mock_exporter.return_value = exporter

    report = {
        'tax_year': 2024,
        'user_id': 'test',
        'summary': {
            'total_transactions': 5,
            'short_term_net': 4000.0,
            'long_term_net': 9500.0,
            'total_net_gain_loss': 13500.0
        }
    }

    exporter.export_cpa_report = AsyncMock(return_value=report)

    response = client.get("/api/tax/export/cpa-report?user_id=test&tax_year=2024")

    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "report" in data


# ==================== Dashboard API ====================

@patch("app.api.tax.get_tax_optimizer")
def test_get_tax_dashboard(mock_optimizer, client):
    """Test tax dashboard endpoint"""
    optimizer = AsyncMock()
    mock_optimizer.return_value = optimizer

    dashboard = {
        'tax_year': 2024,
        'summary': {
            'total_net_gain_loss': 13500.0,
            'estimated_tax': 2700.0,
            'effective_rate': 20.0,
            'short_term_net': 4000.0,
            'long_term_net': 9500.0
        },
        'harvest_opportunities': [],
        'wash_sale_count': 0,
        'unrealized_positions': 10,
        'optimization_tips': [
            "💰 Tax Loss Harvesting: $1,200 potential savings from 3 opportunities"
        ]
    }

    optimizer.get_tax_dashboard = AsyncMock(return_value=dashboard)

    response = client.get("/api/tax/dashboard?user_id=test&tax_year=2024")

    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "dashboard" in data
    assert data["dashboard"]["tax_year"] == 2024


# ==================== Service Layer Tests ====================

@pytest.mark.asyncio
async def test_wash_sale_detector_service():
    """Test WashSaleDetector service directly"""
    from app.services.tax_optimizer import WashSaleDetector

    detector = WashSaleDetector()

    # Test _calculate_days_until_safe
    sale_date = datetime.now() - timedelta(days=15)
    days_safe = detector._calculate_days_until_safe(sale_date)
    assert days_safe == 16  # 31 - 15


@pytest.mark.asyncio
async def test_tax_bracket_determination():
    """Test tax bracket determination"""
    from app.services.tax_optimizer import CapitalGainsCalculator

    calculator = CapitalGainsCalculator()

    # Test ordinary income brackets
    bracket_50k = calculator._determine_ordinary_bracket(50000)
    assert bracket_50k == TaxBracket.BRACKET_22

    bracket_200k = calculator._determine_ordinary_bracket(200000)
    assert bracket_200k == TaxBracket.BRACKET_32

    # Test capital gains brackets
    cg_bracket_50k = calculator._determine_capital_gains_bracket(50000)
    from app.core.tax_models import CapitalGainsBracket
    assert cg_bracket_50k == CapitalGainsBracket.BRACKET_15


# ==================== Error Handling ====================

@patch("app.api.tax.get_wash_sale_detector")
def test_wash_sale_check_error_handling(mock_detector, client):
    """Test error handling in wash sale check"""
    detector = AsyncMock()
    mock_detector.return_value = detector
    detector.check_wash_sale = AsyncMock(side_effect=Exception("Database error"))

    response = client.post(
        "/api/tax/wash-sale/check",
        json={
            "symbol": "AAPL",
            "sale_date": "2024-06-01T00:00:00",
            "loss_amount": -500.0
        }
    )

    assert response.status_code == 500


@patch("app.api.tax.get_tax_loss_harvester")
def test_execute_harvest_invalid_lot(mock_harvester, client):
    """Test harvest execution with invalid lot"""
    harvester = AsyncMock()
    mock_harvester.return_value = harvester
    harvester.execute_harvest = AsyncMock(
        side_effect=ValueError("Tax lot not found")
    )

    response = client.post(
        "/api/tax/harvest/execute",
        json={
            "tax_lot_id": 99999,
            "user_id": "test"
        }
    )

    assert response.status_code == 400
