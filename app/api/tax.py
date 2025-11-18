"""
Tax Optimization API endpoints
Wash sale detection, tax loss harvesting, gain/loss reporting, scenario planning, and exports
"""
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import logging

from app.services.tax_optimizer import (
    get_tax_optimizer,
    get_wash_sale_detector,
    get_tax_loss_harvester,
    get_gains_calculator,
    get_scenario_planner,
    get_tax_exporter
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/tax", tags=["tax"])


# Request/Response Models

class WashSaleCheckRequest(BaseModel):
    """Wash sale check request"""
    symbol: str
    sale_date: str  # ISO format
    loss_amount: float
    user_id: str = "default"


class TaxHarvestRequest(BaseModel):
    """Tax loss harvest execution request"""
    tax_lot_id: int
    replacement_symbol: Optional[str] = None
    user_id: str = "default"


class ScenarioAnalysisRequest(BaseModel):
    """Scenario analysis request"""
    symbol: str
    quantity: float
    current_gain: float
    user_id: str = "default"


class TaxEstimateRequest(BaseModel):
    """Tax estimate request"""
    ordinary_income: float = 100000.0
    filing_status: str = "single"
    user_id: str = "default"
    tax_year: Optional[int] = None


# Endpoints

@router.get("/health")
async def tax_health():
    """Health check for tax optimization service"""
    return {
        "status": "healthy",
        "service": "tax optimization",
        "features": [
            "wash_sale_detection",
            "tax_loss_harvesting",
            "gain_loss_reporting",
            "scenario_planning",
            "tax_exports"
        ]
    }


@router.get("/dashboard")
async def get_tax_dashboard(
    user_id: str = Query("default", description="User ID"),
    tax_year: Optional[int] = Query(None, description="Tax year (default: current)")
):
    """
    Get comprehensive tax optimization dashboard.

    Returns:
        - Current year gain/loss summary
        - Tax loss harvesting opportunities
        - Wash sale warnings
        - Estimated tax impact
        - Optimization strategies
    """
    try:
        optimizer = get_tax_optimizer()
        dashboard = await optimizer.get_tax_dashboard(user_id, tax_year)

        return {
            "success": True,
            "dashboard": dashboard
        }

    except Exception as e:
        logger.error(f"Error getting tax dashboard: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/wash-sale/check")
async def check_wash_sale(request: WashSaleCheckRequest):
    """
    Check if a sale triggers the IRS 30-day wash sale rule.

    Args:
        request: Symbol, sale date, and loss amount

    Returns:
        - Whether it's a violation
        - Days until safe to repurchase
        - Conflicting transactions
        - Suggested alternative securities
    """
    try:
        detector = get_wash_sale_detector()

        sale_date = datetime.fromisoformat(request.sale_date)
        result = await detector.check_wash_sale(
            symbol=request.symbol,
            sale_date=sale_date,
            loss_amount=request.loss_amount,
            user_id=request.user_id
        )

        # Get alternative suggestions if violation
        alternatives = []
        if result.is_violation:
            alt_securities = await detector.get_suggested_alternatives(
                symbol=request.symbol
            )
            alternatives = [
                {
                    'symbol': alt.symbol,
                    'name': alt.name,
                    'similarity_score': alt.similarity_score,
                    'reasons': alt.reasons
                }
                for alt in alt_securities
            ]

        return {
            "success": True,
            "wash_sale": {
                "is_violation": result.is_violation,
                "days_until_safe": result.days_until_safe,
                "conflicting_transactions": result.conflicting_transactions,
                "disallowed_loss": f"${abs(result.disallowed_loss):,.2f}",
                "alternative_securities": alternatives,
                "warning": "IRS 30-day rule applies" if result.is_violation else None
            }
        }

    except Exception as e:
        logger.error(f"Error checking wash sale: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/wash-sale/alternatives/{symbol}")
async def get_wash_sale_alternatives(
    symbol: str,
    count: int = Query(5, ge=1, le=10, description="Number of alternatives")
):
    """
    Get suggested alternative securities to avoid wash sale.

    Returns securities that are similar but not "substantially identical"
    according to IRS rules.
    """
    try:
        detector = get_wash_sale_detector()
        alternatives = await detector.get_suggested_alternatives(symbol, count)

        return {
            "success": True,
            "symbol": symbol,
            "alternatives": [
                {
                    'symbol': alt.symbol,
                    'name': alt.name,
                    'similarity_score': alt.similarity_score,
                    'correlation': alt.correlation,
                    'sector': alt.sector,
                    'reasons': alt.reasons,
                    'wash_sale_safe': alt.wash_sale_safe
                }
                for alt in alternatives
            ]
        }

    except Exception as e:
        logger.error(f"Error getting alternatives: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/harvest/opportunities")
async def get_harvest_opportunities(
    user_id: str = Query("default", description="User ID"),
    min_loss: float = Query(100.0, ge=0, description="Minimum loss threshold"),
    tax_bracket: float = Query(0.24, ge=0, le=0.37, description="Tax bracket")
):
    """
    Identify tax loss harvesting opportunities.

    Returns positions with unrealized losses that could be harvested
    for tax benefits.
    """
    try:
        harvester = get_tax_loss_harvester()
        opportunities = await harvester.identify_opportunities(
            user_id=user_id,
            min_loss_threshold=min_loss,
            tax_bracket=tax_bracket
        )

        return {
            "success": True,
            "count": len(opportunities),
            "total_potential_savings": sum(opp.estimated_tax_savings for opp in opportunities),
            "opportunities": [
                {
                    'symbol': opp.symbol,
                    'tax_lot_id': opp.tax_lot_id,
                    'unrealized_loss': f"${abs(opp.unrealized_loss):,.2f}",
                    'current_price': f"${opp.current_price:.2f}",
                    'cost_basis': f"${opp.cost_basis:.2f}",
                    'quantity': opp.quantity,
                    'estimated_tax_savings': f"${opp.estimated_tax_savings:,.2f}",
                    'replacement_suggestions': opp.replacement_suggestions,
                    'days_until_wash_safe': opp.days_until_wash_safe
                }
                for opp in opportunities[:10]  # Limit to top 10
            ]
        }

    except Exception as e:
        logger.error(f"Error getting harvest opportunities: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/harvest/execute")
async def execute_harvest(request: TaxHarvestRequest):
    """
    Execute a tax loss harvest.

    Steps:
    1. Sell the position at a loss
    2. Optionally buy replacement security
    3. Log the harvest action
    4. Track 31-day wash sale window
    """
    try:
        harvester = get_tax_loss_harvester()
        result = await harvester.execute_harvest(
            tax_lot_id=request.tax_lot_id,
            replacement_symbol=request.replacement_symbol,
            user_id=request.user_id
        )

        return {
            "success": True,
            "harvest": {
                "symbol": result['symbol'],
                "loss_realized": f"${abs(result['loss']):,.2f}",
                "tax_savings_estimate": f"${result['tax_savings_estimate']:,.2f}",
                "replacement_symbol": result.get('replacement_symbol'),
                "wash_sale_safe_date": result['wash_sale_safe_date'],
                "message": f"Successfully harvested ${abs(result['loss']):,.2f} loss"
            }
        }

    except Exception as e:
        logger.error(f"Error executing harvest: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/report/gains-losses")
async def get_gains_losses_report(
    user_id: str = Query("default", description="User ID"),
    tax_year: Optional[int] = Query(None, description="Tax year (default: current)")
):
    """
    Get comprehensive gain/loss report for tax year.

    Includes:
    - Short-term vs long-term gains/losses
    - Realized vs unrealized positions
    - Wash sale adjustments
    - Net gain/loss calculation
    """
    try:
        calculator = get_gains_calculator()
        report = await calculator.calculate_realized_gains(user_id, tax_year)

        return {
            "success": True,
            "tax_year": report.tax_year,
            "summary": {
                "short_term_gains": f"${report.short_term_gains:,.2f}",
                "short_term_losses": f"${abs(report.short_term_losses):,.2f}",
                "net_short_term": f"${report.net_short_term:,.2f}",
                "long_term_gains": f"${report.long_term_gains:,.2f}",
                "long_term_losses": f"${abs(report.long_term_losses):,.2f}",
                "net_long_term": f"${report.net_long_term:,.2f}",
                "total_net_gain_loss": f"${report.total_net_gain_loss:,.2f}",
                "wash_sale_adjustments": f"${report.wash_sale_adjustments:,.2f}"
            },
            "realized_count": len(report.realized_gains),
            "unrealized_count": len(report.unrealized_gains),
            "realized_gains": [
                {
                    'symbol': gain.symbol,
                    'quantity': gain.quantity,
                    'sale_date': gain.sale_date.isoformat(),
                    'proceeds': f"${gain.proceeds:,.2f}",
                    'cost_basis': f"${gain.cost_basis:,.2f}",
                    'gain_loss': f"${gain.gain_loss:,.2f}",
                    'holding_period': gain.holding_period.value,
                }
                for gain in report.realized_gains
            ],
            "unrealized_positions": report.unrealized_gains
        }

    except Exception as e:
        logger.error(f"Error getting gains/losses report: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/report/tax-estimate")
async def get_tax_estimate(request: TaxEstimateRequest):
    """
    Estimate tax impact of capital gains/losses.

    Takes into account:
    - Ordinary income tax bracket
    - Short-term vs long-term capital gains rates
    - 2024 tax brackets
    """
    try:
        calculator = get_gains_calculator()

        # Get gain/loss report
        report = await calculator.calculate_realized_gains(
            request.user_id,
            request.tax_year
        )

        # Calculate tax estimate
        tax_estimate = await calculator.estimate_tax_impact(
            report,
            request.ordinary_income,
            request.filing_status
        )

        return {
            "success": True,
            "tax_estimate": {
                "short_term_tax": f"${tax_estimate.short_term_tax:,.2f}",
                "long_term_tax": f"${tax_estimate.long_term_tax:,.2f}",
                "total_tax": f"${tax_estimate.total_tax:,.2f}",
                "effective_rate": f"{tax_estimate.effective_rate:.2f}%",
                "marginal_rate": f"{tax_estimate.marginal_rate:.2f}%",
                "ordinary_income_bracket": tax_estimate.ordinary_income_bracket.value if tax_estimate.ordinary_income_bracket else None,
                "capital_gains_bracket": tax_estimate.capital_gains_bracket.value if tax_estimate.capital_gains_bracket else None
            },
            "breakdown": {
                "net_short_term": f"${report.net_short_term:,.2f}",
                "net_long_term": f"${report.net_long_term:,.2f}",
                "total_net": f"${report.total_net_gain_loss:,.2f}"
            }
        }

    except Exception as e:
        logger.error(f"Error calculating tax estimate: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/scenario/sale-timing")
async def analyze_sale_timing(request: ScenarioAnalysisRequest):
    """
    Analyze different sale timing scenarios.

    Compares:
    1. Sell now (short-term)
    2. Wait for long-term treatment
    3. Harvest loss now
    4. Defer to next year
    """
    try:
        planner = get_scenario_planner()
        scenarios = await planner.analyze_sale_timing(
            symbol=request.symbol,
            quantity=request.quantity,
            current_gain=request.current_gain,
            user_id=request.user_id
        )

        return {
            "success": True,
            "symbol": request.symbol,
            "scenarios": [
                {
                    'name': scenario.scenario_name,
                    'description': scenario.description,
                    'current_gain_loss': f"${scenario.current_gain_loss:,.2f}",
                    'projected_gain_loss': f"${scenario.projected_gain_loss:,.2f}",
                    'current_tax': f"${scenario.current_tax:,.2f}",
                    'projected_tax': f"${scenario.projected_tax:,.2f}",
                    'tax_savings': f"${scenario.tax_savings:,.2f}",
                    'recommended_actions': scenario.recommended_actions,
                    'assumptions': scenario.assumptions
                }
                for scenario in scenarios
            ],
            "best_scenario": max(scenarios, key=lambda s: s.tax_savings).scenario_name
        }

    except Exception as e:
        logger.error(f"Error analyzing scenarios: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/export/turbotax")
async def export_turbotax(
    user_id: str = Query("default", description="User ID"),
    tax_year: Optional[int] = Query(None, description="Tax year (default: current)")
):
    """
    Export transactions in TurboTax CSV format.

    Downloads a CSV file compatible with TurboTax import.
    """
    try:
        exporter = get_tax_exporter()
        csv_data = await exporter.export_turbotax_csv(user_id, tax_year)

        return {
            "success": True,
            "format": "turbotax_csv",
            "tax_year": tax_year or datetime.now().year,
            "csv_data": csv_data,
            "instructions": [
                "1. Save the CSV data to a file (e.g., capital_gains_2024.csv)",
                "2. In TurboTax, go to 'Wages & Income' → 'Investment Income'",
                "3. Select 'Import from CSV'",
                "4. Upload the saved file",
                "5. Review imported transactions"
            ]
        }

    except Exception as e:
        logger.error(f"Error exporting TurboTax CSV: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/export/form-8949")
async def export_form_8949(
    user_id: str = Query("default", description="User ID"),
    tax_year: Optional[int] = Query(None, description="Tax year (default: current)")
):
    """
    Prepare data for IRS Form 8949.

    Returns structured data ready for Form 8949 filing
    (Sales and Other Dispositions of Capital Assets).
    """
    try:
        exporter = get_tax_exporter()
        form_data = await exporter.export_form_8949(user_id, tax_year)

        return {
            "success": True,
            "form": "8949",
            "tax_year": tax_year or datetime.now().year,
            "entries": [
                {
                    'description': entry.description,
                    'date_acquired': entry.date_acquired,
                    'date_sold': entry.date_sold,
                    'proceeds': f"${entry.proceeds:,.2f}",
                    'cost_basis': f"${entry.cost_basis:,.2f}",
                    'adjustment_code': entry.adjustment_code,
                    'adjustment_amount': f"${entry.adjustment_amount:,.2f}" if entry.adjustment_amount else None,
                    'gain_loss': f"${entry.gain_loss:,.2f}"
                }
                for entry in form_data
            ],
            "instructions": [
                "Use this data to complete IRS Form 8949",
                "Separate short-term (Part I) and long-term (Part II) transactions",
                "Adjustment code 'W' indicates wash sale",
                "Transfer totals to Schedule D"
            ]
        }

    except Exception as e:
        logger.error(f"Error exporting Form 8949: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/export/cpa-report")
async def export_cpa_report(
    user_id: str = Query("default", description="User ID"),
    tax_year: Optional[int] = Query(None, description="Tax year (default: current)")
):
    """
    Generate comprehensive report for CPA review.

    Includes:
    - Summary of all transactions
    - Wash sale adjustments
    - Tax lot details
    - Unrealized positions
    - Tax estimates
    """
    try:
        exporter = get_tax_exporter()
        report = await exporter.export_cpa_report(user_id, tax_year)

        return {
            "success": True,
            "report": report
        }

    except Exception as e:
        logger.error(f"Error generating CPA report: {e}")
        raise HTTPException(status_code=500, detail=str(e))
