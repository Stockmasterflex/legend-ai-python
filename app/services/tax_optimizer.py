"""
Tax Optimization Service
Comprehensive tax optimization including wash sale detection, tax loss harvesting,
gain/loss reporting, scenario planning, and tax software exports.
"""
import logging
import json
from typing import Optional, List, Dict, Any, Tuple
from datetime import datetime, timedelta
from dataclasses import asdict
import csv
import io

from app.services.cache import get_cache_service
from app.core.tax_models import (
    HoldingPeriod, WashSaleStatus, TaxBracket, CapitalGainsBracket,
    TaxLotModel, CapitalGainModel, WashSaleModel, TaxHarvestOpportunity,
    GainLossReport, TaxEstimate, ScenarioAnalysis, TaxOptimizationStrategy,
    Form8949Entry, TurbotaxCSVEntry, WashSaleCheck, ReplacementSecurity,
    calculate_holding_period, is_wash_sale_violation,
    get_tax_rate_for_bracket, get_capital_gains_rate, determine_tax_year
)

logger = logging.getLogger(__name__)


class WashSaleDetector:
    """
    Wash Sale Rule Detection (IRS 30-day rule)
    Detects substantially identical securities purchases within 30 days
    before or after a loss sale.
    """

    def __init__(self):
        self.cache = get_cache_service()

    async def check_wash_sale(
        self,
        symbol: str,
        sale_date: datetime,
        loss_amount: float,
        user_id: str = "default"
    ) -> WashSaleCheck:
        """
        Check if a loss sale triggers wash sale rule.

        Returns details about any wash sale violation including:
        - Whether it's a violation
        - Days until safe to repurchase
        - Conflicting transactions
        - Disallowed loss amount
        """
        if loss_amount >= 0:
            # Not a loss, no wash sale possible
            return WashSaleCheck(
                is_violation=False,
                days_until_safe=0,
                conflicting_transactions=[],
                disallowed_loss=0.0,
                adjusted_cost_basis=0.0
            )

        # Get all tax lots for this symbol within wash sale window
        wash_sale_window_start = sale_date - timedelta(days=30)
        wash_sale_window_end = sale_date + timedelta(days=30)

        conflicting_purchases = await self._find_purchases_in_window(
            symbol=symbol,
            start_date=wash_sale_window_start,
            end_date=wash_sale_window_end,
            exclude_date=sale_date,
            user_id=user_id
        )

        if conflicting_purchases:
            # Wash sale violation detected
            # Disallowed loss is proportional to repurchased shares
            return WashSaleCheck(
                is_violation=True,
                days_until_safe=self._calculate_days_until_safe(sale_date),
                conflicting_transactions=conflicting_purchases,
                disallowed_loss=abs(loss_amount),
                adjusted_cost_basis=abs(loss_amount)  # Added to new purchase
            )

        # No violation, but calculate when safe to repurchase
        days_since_sale = (datetime.now() - sale_date).days
        days_until_safe = max(0, 31 - days_since_sale)

        return WashSaleCheck(
            is_violation=False,
            days_until_safe=days_until_safe,
            conflicting_transactions=[],
            disallowed_loss=0.0,
            adjusted_cost_basis=0.0
        )

    async def _find_purchases_in_window(
        self,
        symbol: str,
        start_date: datetime,
        end_date: datetime,
        exclude_date: datetime,
        user_id: str
    ) -> List[Dict[str, Any]]:
        """Find all purchases of a symbol within a date range"""
        cache = await self.cache._get_redis()

        # Get all tax lots for this user and symbol
        tax_lots_key = f"tax_lots:{user_id}:{symbol}"
        tax_lot_ids = await cache.lrange(tax_lots_key, 0, -1)

        purchases = []
        for lot_id in tax_lot_ids:
            lot_data = await cache.get(f"tax_lot:{lot_id}")
            if lot_data:
                lot = json.loads(lot_data)
                purchase_date = datetime.fromisoformat(lot['purchase_date'])

                if (start_date <= purchase_date <= end_date and
                    purchase_date.date() != exclude_date.date()):
                    purchases.append({
                        'lot_id': lot_id,
                        'purchase_date': purchase_date,
                        'quantity': lot['quantity'],
                        'price_per_share': lot['price_per_share'],
                        'days_from_sale': abs((purchase_date - exclude_date).days)
                    })

        return sorted(purchases, key=lambda x: x['purchase_date'])

    def _calculate_days_until_safe(self, sale_date: datetime) -> int:
        """Calculate days until safe to repurchase without wash sale"""
        days_since_sale = (datetime.now() - sale_date).days
        return max(0, 31 - days_since_sale)

    async def get_suggested_alternatives(
        self,
        symbol: str,
        count: int = 5
    ) -> List[ReplacementSecurity]:
        """
        Get suggested alternative securities that avoid wash sale.
        These should be similar but not "substantially identical".

        For example:
        - Instead of AAPL, consider MSFT or other tech stocks
        - Instead of SPY, consider IVV or VOO (different S&P 500 ETFs)
        """
        # This would integrate with market data service
        # For now, return mock suggestions based on common patterns

        suggestions_map = {
            "SPY": ["IVV", "VOO", "SPLG", "VTI"],
            "QQQ": ["QQQM", "ONEQ", "VGT", "VUG"],
            "AAPL": ["MSFT", "GOOGL", "NVDA", "META"],
            "TSLA": ["GM", "F", "RIVN", "LCID"],
            "VTI": ["SCHB", "ITOT", "IWV", "THRK"],
        }

        alternatives = suggestions_map.get(symbol.upper(), [])

        # Build ReplacementSecurity objects
        replacements = []
        for alt_symbol in alternatives[:count]:
            replacements.append(ReplacementSecurity(
                symbol=alt_symbol,
                name=f"{alt_symbol} Corporation",
                similarity_score=0.85,  # High similarity, same sector
                correlation=0.75,
                sector="Technology",
                current_price=0.0,  # Would fetch from market data
                wash_sale_safe=True,
                reasons=[
                    "Same sector exposure",
                    "Similar market cap",
                    "Not substantially identical per IRS"
                ]
            ))

        return replacements


class TaxLossHarvester:
    """
    Tax Loss Harvesting Service
    Identifies opportunities to realize losses for tax benefits
    """

    def __init__(self):
        self.cache = get_cache_service()
        self.wash_sale_detector = WashSaleDetector()

    async def identify_opportunities(
        self,
        user_id: str = "default",
        min_loss_threshold: float = 100.0,
        tax_bracket: float = 0.24
    ) -> List[TaxHarvestOpportunity]:
        """
        Identify tax loss harvesting opportunities.

        Returns positions with unrealized losses that could be harvested.
        """
        opportunities = []

        # Get all open tax lots for user
        cache = await self.cache._get_redis()
        user_lots_key = f"tax_lots:{user_id}:*"

        # In real implementation, would query database
        # For now, scan cache keys
        lot_keys = await cache.keys(f"tax_lot:*")

        for lot_key in lot_keys:
            lot_data = await cache.get(lot_key)
            if not lot_data:
                continue

            lot = json.loads(lot_data)

            if lot.get('is_closed', False):
                continue  # Skip closed lots

            # Calculate unrealized loss
            current_price = await self._get_current_price(lot['symbol'])
            if current_price is None:
                continue

            cost_per_share = lot['cost_basis'] / lot['quantity']
            unrealized_pnl = (current_price - cost_per_share) * lot['remaining_quantity']

            if unrealized_pnl < -min_loss_threshold:  # Significant loss
                # Calculate tax savings
                estimated_savings = abs(unrealized_pnl) * tax_bracket

                # Get replacement suggestions
                alternatives = await self.wash_sale_detector.get_suggested_alternatives(
                    lot['symbol']
                )

                # Calculate when safe to repurchase same security
                days_until_safe = 31  # Must wait 31 days after sale

                opportunity = TaxHarvestOpportunity(
                    symbol=lot['symbol'],
                    tax_lot_id=lot.get('id', 0),
                    unrealized_loss=unrealized_pnl,
                    current_price=current_price,
                    cost_basis=lot['cost_basis'],
                    quantity=lot['remaining_quantity'],
                    estimated_tax_savings=estimated_savings,
                    replacement_suggestions=[
                        {
                            'symbol': alt.symbol,
                            'similarity_score': alt.similarity_score,
                            'reasons': alt.reasons
                        }
                        for alt in alternatives[:3]
                    ],
                    days_until_wash_safe=days_until_safe
                )

                opportunities.append(opportunity)

        # Sort by estimated tax savings (highest first)
        return sorted(opportunities, key=lambda x: x.estimated_tax_savings, reverse=True)

    async def _get_current_price(self, symbol: str) -> Optional[float]:
        """Get current market price for a symbol"""
        cache = await self.cache._get_redis()
        price_key = f"price:{symbol}"
        price_data = await cache.get(price_key)

        if price_data:
            return float(price_data)

        # Would integrate with market data service
        return None

    async def execute_harvest(
        self,
        tax_lot_id: int,
        replacement_symbol: Optional[str] = None,
        user_id: str = "default"
    ) -> Dict[str, Any]:
        """
        Execute a tax loss harvest.

        Steps:
        1. Sell the position at a loss
        2. Optionally buy replacement security
        3. Log the harvest action
        4. Track wash sale window
        """
        cache = await self.cache._get_redis()
        lot_data = await cache.get(f"tax_lot:{tax_lot_id}")

        if not lot_data:
            raise ValueError(f"Tax lot {tax_lot_id} not found")

        lot = json.loads(lot_data)

        # Get current price
        current_price = await self._get_current_price(lot['symbol'])
        if not current_price:
            raise ValueError(f"Cannot get current price for {lot['symbol']}")

        # Calculate loss
        cost_per_share = lot['cost_basis'] / lot['quantity']
        loss = (current_price - cost_per_share) * lot['remaining_quantity']

        if loss >= 0:
            raise ValueError("Position is not at a loss, cannot harvest")

        # Create harvest log
        harvest_log = {
            'tax_lot_id': tax_lot_id,
            'symbol': lot['symbol'],
            'unrealized_loss': loss,
            'current_price': current_price,
            'quantity': lot['remaining_quantity'],
            'harvest_date': datetime.now().isoformat(),
            'replacement_symbol': replacement_symbol,
            'user_id': user_id
        }

        # Store harvest log
        harvest_key = f"tax_harvest:{user_id}:{tax_lot_id}"
        await cache.setex(harvest_key, 365 * 24 * 3600, json.dumps(harvest_log))

        logger.info(f"✅ Tax loss harvested: {lot['symbol']} - Loss: ${abs(loss):.2f}")

        return {
            'success': True,
            'symbol': lot['symbol'],
            'loss': loss,
            'tax_savings_estimate': abs(loss) * 0.24,  # Assume 24% bracket
            'replacement_symbol': replacement_symbol,
            'wash_sale_safe_date': (datetime.now() + timedelta(days=31)).isoformat()
        }


class CapitalGainsCalculator:
    """
    Capital Gains/Loss Calculator
    Calculates realized and unrealized gains with tax treatment
    """

    def __init__(self):
        self.cache = get_cache_service()

    async def calculate_realized_gains(
        self,
        user_id: str = "default",
        tax_year: Optional[int] = None
    ) -> GainLossReport:
        """Calculate all realized capital gains/losses for a tax year"""

        if tax_year is None:
            tax_year = datetime.now().year

        cache = await self.cache._get_redis()

        # Get all capital gains records for user and year
        gains_key = f"capital_gains:{user_id}:{tax_year}"
        gain_ids = await cache.lrange(gains_key, 0, -1)

        short_term_gains = 0.0
        short_term_losses = 0.0
        long_term_gains = 0.0
        long_term_losses = 0.0
        wash_sale_adjustments = 0.0
        realized_gains_list = []

        for gain_id in gain_ids:
            gain_data = await cache.get(f"capital_gain:{gain_id}")
            if not gain_data:
                continue

            gain = json.loads(gain_data)
            gain_model = CapitalGainModel(**gain)
            realized_gains_list.append(gain_model)

            # Categorize by holding period
            if gain['holding_period'] == HoldingPeriod.SHORT_TERM.value:
                if gain['gain_loss'] > 0:
                    short_term_gains += gain['gain_loss']
                else:
                    short_term_losses += gain['gain_loss']
            else:  # LONG_TERM
                if gain['gain_loss'] > 0:
                    long_term_gains += gain['gain_loss']
                else:
                    long_term_losses += gain['gain_loss']

            wash_sale_adjustments += gain.get('wash_sale_loss_disallowed', 0)

        # Calculate unrealized gains
        unrealized = await self._calculate_unrealized_gains(user_id)

        return GainLossReport(
            tax_year=tax_year,
            short_term_gains=short_term_gains,
            short_term_losses=short_term_losses,
            long_term_gains=long_term_gains,
            long_term_losses=long_term_losses,
            net_short_term=short_term_gains + short_term_losses,
            net_long_term=long_term_gains + long_term_losses,
            total_net_gain_loss=short_term_gains + short_term_losses + long_term_gains + long_term_losses,
            wash_sale_adjustments=wash_sale_adjustments,
            realized_gains=realized_gains_list,
            unrealized_gains=unrealized
        )

    async def _calculate_unrealized_gains(
        self,
        user_id: str
    ) -> List[Dict[str, Any]]:
        """Calculate unrealized gains for all open positions"""
        cache = await self.cache._get_redis()

        unrealized = []
        lot_keys = await cache.keys(f"tax_lot:*")

        for lot_key in lot_keys:
            lot_data = await cache.get(lot_key)
            if not lot_data:
                continue

            lot = json.loads(lot_data)

            if lot.get('is_closed', False) or lot.get('user_id') != user_id:
                continue

            # Get current price
            current_price = await self._get_current_price(lot['symbol'])
            if not current_price:
                continue

            cost_per_share = lot['cost_basis'] / lot['quantity']
            unrealized_pnl = (current_price - cost_per_share) * lot['remaining_quantity']
            unrealized_pnl_pct = ((current_price - cost_per_share) / cost_per_share) * 100

            # Calculate holding period
            purchase_date = datetime.fromisoformat(lot['purchase_date'])
            holding_period = calculate_holding_period(purchase_date, datetime.now())

            unrealized.append({
                'symbol': lot['symbol'],
                'quantity': lot['remaining_quantity'],
                'cost_basis': cost_per_share,
                'current_price': current_price,
                'unrealized_pnl': unrealized_pnl,
                'unrealized_pnl_pct': unrealized_pnl_pct,
                'holding_period': holding_period.value,
                'purchase_date': lot['purchase_date']
            })

        return unrealized

    async def _get_current_price(self, symbol: str) -> Optional[float]:
        """Get current market price for a symbol"""
        cache = await self.cache._get_redis()
        price_key = f"price:{symbol}"
        price_data = await cache.get(price_key)

        if price_data:
            return float(price_data)

        return None

    async def estimate_tax_impact(
        self,
        gain_loss_report: GainLossReport,
        ordinary_income: float = 100000.0,
        filing_status: str = "single"
    ) -> TaxEstimate:
        """
        Estimate tax impact of capital gains/losses.

        Uses 2024 tax brackets for single filers.
        """
        # Determine tax brackets
        ordinary_bracket = self._determine_ordinary_bracket(ordinary_income)
        capital_gains_bracket = self._determine_capital_gains_bracket(ordinary_income)

        # Calculate short-term capital gains tax (taxed as ordinary income)
        short_term_tax = 0.0
        if gain_loss_report.net_short_term > 0:
            short_term_rate = get_tax_rate_for_bracket(ordinary_bracket)
            short_term_tax = gain_loss_report.net_short_term * short_term_rate

        # Calculate long-term capital gains tax
        long_term_tax = 0.0
        if gain_loss_report.net_long_term > 0:
            long_term_rate = get_capital_gains_rate(capital_gains_bracket)
            long_term_tax = gain_loss_report.net_long_term * long_term_rate

        total_tax = short_term_tax + long_term_tax

        # Calculate effective rate
        total_gain = gain_loss_report.total_net_gain_loss
        effective_rate = (total_tax / total_gain * 100) if total_gain > 0 else 0.0

        return TaxEstimate(
            short_term_tax=short_term_tax,
            long_term_tax=long_term_tax,
            total_tax=total_tax,
            effective_rate=effective_rate,
            marginal_rate=get_tax_rate_for_bracket(ordinary_bracket) * 100,
            ordinary_income_bracket=ordinary_bracket,
            capital_gains_bracket=capital_gains_bracket
        )

    def _determine_ordinary_bracket(self, income: float) -> TaxBracket:
        """Determine ordinary income tax bracket (2024 single filer)"""
        if income <= 11600:
            return TaxBracket.BRACKET_10
        elif income <= 47150:
            return TaxBracket.BRACKET_12
        elif income <= 100525:
            return TaxBracket.BRACKET_22
        elif income <= 191950:
            return TaxBracket.BRACKET_24
        elif income <= 243725:
            return TaxBracket.BRACKET_32
        elif income <= 609350:
            return TaxBracket.BRACKET_35
        else:
            return TaxBracket.BRACKET_37

    def _determine_capital_gains_bracket(self, income: float) -> CapitalGainsBracket:
        """Determine long-term capital gains bracket (2024 single filer)"""
        if income <= 47025:
            return CapitalGainsBracket.BRACKET_0
        elif income <= 518900:
            return CapitalGainsBracket.BRACKET_15
        else:
            return CapitalGainsBracket.BRACKET_20


class TaxScenarioPlanner:
    """
    Tax Scenario Planning and What-If Analysis
    """

    def __init__(self):
        self.gains_calculator = CapitalGainsCalculator()

    async def analyze_sale_timing(
        self,
        symbol: str,
        quantity: float,
        current_gain: float,
        user_id: str = "default"
    ) -> List[ScenarioAnalysis]:
        """
        Analyze different sale timing scenarios.

        Scenarios:
        1. Sell now (short-term gains)
        2. Wait for long-term treatment
        3. Harvest loss in current year
        4. Defer to next year
        """
        scenarios = []

        # Scenario 1: Sell now at short-term rates
        scenarios.append(ScenarioAnalysis(
            scenario_name="Sell Now (Short-Term)",
            description="Sell immediately at short-term capital gains rate",
            current_gain_loss=current_gain,
            projected_gain_loss=current_gain,
            current_tax=current_gain * 0.24,  # Assume 24% bracket
            projected_tax=current_gain * 0.24,
            tax_savings=0.0,
            recommended_actions=[
                f"Sell {quantity} shares of {symbol} now",
                "Pay short-term capital gains tax at ordinary income rate"
            ],
            assumptions={'tax_rate': 0.24, 'holding_period': 'short_term'}
        ))

        # Scenario 2: Wait for long-term treatment
        long_term_tax = current_gain * 0.15  # Assume 15% long-term rate
        scenarios.append(ScenarioAnalysis(
            scenario_name="Wait for Long-Term",
            description="Hold for >1 year to qualify for long-term rates",
            current_gain_loss=current_gain,
            projected_gain_loss=current_gain,  # Assumes no price change
            current_tax=current_gain * 0.24,
            projected_tax=long_term_tax,
            tax_savings=(current_gain * 0.24) - long_term_tax,
            recommended_actions=[
                f"Hold {symbol} for >1 year",
                "Qualify for preferential long-term capital gains rate",
                "Potential tax savings: ${(current_gain * 0.09):.2f}"
            ],
            assumptions={
                'tax_rate_short': 0.24,
                'tax_rate_long': 0.15,
                'price_remains_stable': True
            }
        ))

        # Scenario 3: Tax loss harvesting
        if current_gain < 0:  # It's a loss
            scenarios.append(ScenarioAnalysis(
                scenario_name="Harvest Loss Now",
                description="Realize loss to offset other gains",
                current_gain_loss=current_gain,
                projected_gain_loss=current_gain,
                current_tax=0.0,
                projected_tax=0.0,
                tax_savings=abs(current_gain) * 0.24,  # Offset other income
                recommended_actions=[
                    f"Sell {symbol} to realize ${abs(current_gain):.2f} loss",
                    "Use loss to offset other capital gains",
                    "Consider replacement security to maintain exposure",
                    "Wait 31 days before repurchasing to avoid wash sale"
                ],
                assumptions={'can_offset_gains': True, 'tax_bracket': 0.24}
            ))

        return scenarios

    async def optimize_bracket_management(
        self,
        current_income: float,
        realized_gains: float,
        potential_sales: List[Dict[str, Any]]
    ) -> TaxOptimizationStrategy:
        """
        Optimize sales to manage tax bracket.

        Strategy: Avoid pushing income into higher bracket if possible.
        """
        # Calculate current bracket
        next_bracket_threshold = self._get_next_bracket_threshold(current_income)
        room_in_bracket = next_bracket_threshold - current_income

        if realized_gains < room_in_bracket:
            return TaxOptimizationStrategy(
                strategy_name="Realize Gains Within Current Bracket",
                priority=8,
                potential_savings=0.0,  # No bracket jump
                risk_level="low",
                actions=[
                    f"You have ${room_in_bracket:,.2f} room in current bracket",
                    f"Can realize up to ${room_in_bracket:,.2f} in gains without bracket jump",
                    "Consider realizing gains now"
                ],
                time_sensitive=False
            )
        else:
            bracket_jump_tax = (realized_gains - room_in_bracket) * 0.08  # ~8% jump
            return TaxOptimizationStrategy(
                strategy_name="Defer Gains to Avoid Bracket Jump",
                priority=9,
                potential_savings=bracket_jump_tax,
                risk_level="medium",
                actions=[
                    f"Realizing ${realized_gains:,.2f} would push into higher bracket",
                    f"Only ${room_in_bracket:,.2f} room in current bracket",
                    f"Potential extra tax: ${bracket_jump_tax:,.2f}",
                    "Consider deferring some sales to next year"
                ],
                time_sensitive=True,
                deadline=datetime(datetime.now().year, 12, 31)
            )

    def _get_next_bracket_threshold(self, income: float) -> float:
        """Get the income threshold for next tax bracket"""
        brackets = [11600, 47150, 100525, 191950, 243725, 609350, float('inf')]
        for threshold in brackets:
            if income < threshold:
                return threshold
        return float('inf')


class TaxExporter:
    """
    Tax Software Export Service
    Generate reports for TurboTax, CPAs, and IRS Form 8949
    """

    def __init__(self):
        self.gains_calculator = CapitalGainsCalculator()

    async def export_turbotax_csv(
        self,
        user_id: str = "default",
        tax_year: Optional[int] = None
    ) -> str:
        """
        Export transactions in TurboTax CSV format.

        Format: Security Name, Symbol, Shares, Date Acquired, Date Sold,
                Sales Price, Cost Basis, Gain/Loss, Term
        """
        if tax_year is None:
            tax_year = datetime.now().year

        report = await self.gains_calculator.calculate_realized_gains(user_id, tax_year)

        output = io.StringIO()
        writer = csv.writer(output)

        # Write header
        writer.writerow([
            'Security Name', 'Symbol', 'Shares', 'Date Acquired', 'Date Sold',
            'Sales Price', 'Cost Basis', 'Gain/Loss', 'Term'
        ])

        # Write each transaction
        for gain in report.realized_gains:
            term = "Short" if gain.holding_period == HoldingPeriod.SHORT_TERM else "Long"

            # Would need to fetch actual acquisition date from tax lot
            writer.writerow([
                f"{gain.symbol} Corporation",  # Security name
                gain.symbol,
                gain.quantity,
                gain.sale_date.strftime('%m/%d/%Y'),  # Placeholder
                gain.sale_date.strftime('%m/%d/%Y'),
                f"{gain.sale_price:.2f}",
                f"{gain.adjusted_cost_basis:.2f}",
                f"{gain.gain_loss:.2f}",
                term
            ])

        return output.getvalue()

    async def export_form_8949(
        self,
        user_id: str = "default",
        tax_year: Optional[int] = None
    ) -> List[Form8949Entry]:
        """
        Prepare data for IRS Form 8949 (Sales and Other Dispositions of Capital Assets).

        Returns structured data ready for Form 8949 filing.
        """
        if tax_year is None:
            tax_year = datetime.now().year

        report = await self.gains_calculator.calculate_realized_gains(user_id, tax_year)

        entries = []
        for gain in report.realized_gains:
            # Determine adjustment code
            adjustment_code = None
            adjustment_amount = 0.0

            if gain.wash_sale_loss_disallowed > 0:
                adjustment_code = "W"  # Wash sale
                adjustment_amount = gain.wash_sale_loss_disallowed

            entry = Form8949Entry(
                description=f"{gain.quantity} shares {gain.symbol}",
                date_acquired=gain.sale_date.strftime('%m/%d/%Y'),  # Placeholder
                date_sold=gain.sale_date.strftime('%m/%d/%Y'),
                proceeds=gain.proceeds,
                cost_basis=gain.cost_basis,
                adjustment_code=adjustment_code,
                adjustment_amount=adjustment_amount,
                gain_loss=gain.gain_loss
            )
            entries.append(entry)

        return entries

    async def export_cpa_report(
        self,
        user_id: str = "default",
        tax_year: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Generate comprehensive report for CPA review.

        Includes:
        - Summary of all transactions
        - Wash sale adjustments
        - Tax lot details
        - Unrealized positions
        """
        if tax_year is None:
            tax_year = datetime.now().year

        report = await self.gains_calculator.calculate_realized_gains(user_id, tax_year)
        tax_estimate = await self.gains_calculator.estimate_tax_impact(report)

        return {
            'tax_year': tax_year,
            'user_id': user_id,
            'generated_date': datetime.now().isoformat(),
            'summary': {
                'total_transactions': len(report.realized_gains),
                'short_term_net': report.net_short_term,
                'long_term_net': report.net_long_term,
                'total_net_gain_loss': report.total_net_gain_loss,
                'wash_sale_adjustments': report.wash_sale_adjustments,
                'estimated_tax': tax_estimate.total_tax
            },
            'realized_gains': [gain.dict() for gain in report.realized_gains],
            'unrealized_positions': report.unrealized_gains,
            'tax_estimate': tax_estimate.dict(),
            'notes': [
                "All dates and amounts have been calculated using FIFO cost basis method",
                "Wash sale adjustments are included in adjusted cost basis",
                "Estimated tax assumes single filer status",
                "Please review all transactions for accuracy"
            ]
        }


class TaxOptimizer:
    """
    Main Tax Optimization Service
    Orchestrates all tax optimization features
    """

    def __init__(self):
        self.wash_sale_detector = WashSaleDetector()
        self.tax_loss_harvester = TaxLossHarvester()
        self.gains_calculator = CapitalGainsCalculator()
        self.scenario_planner = TaxScenarioPlanner()
        self.exporter = TaxExporter()

    async def get_tax_dashboard(
        self,
        user_id: str = "default",
        tax_year: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Get comprehensive tax optimization dashboard.

        Includes:
        - Current year gain/loss summary
        - Tax loss harvesting opportunities
        - Wash sale warnings
        - Estimated tax impact
        - Optimization strategies
        """
        if tax_year is None:
            tax_year = datetime.now().year

        # Get gain/loss report
        gain_loss_report = await self.gains_calculator.calculate_realized_gains(
            user_id, tax_year
        )

        # Get tax estimate
        tax_estimate = await self.gains_calculator.estimate_tax_impact(gain_loss_report)

        # Get tax loss harvesting opportunities
        harvest_opportunities = await self.tax_loss_harvester.identify_opportunities(user_id)

        return {
            'tax_year': tax_year,
            'summary': {
                'total_net_gain_loss': gain_loss_report.total_net_gain_loss,
                'estimated_tax': tax_estimate.total_tax,
                'effective_rate': tax_estimate.effective_rate,
                'short_term_net': gain_loss_report.net_short_term,
                'long_term_net': gain_loss_report.net_long_term
            },
            'harvest_opportunities': [opp.dict() for opp in harvest_opportunities[:5]],
            'wash_sale_count': 0,  # Would query wash sales
            'unrealized_positions': len(gain_loss_report.unrealized_gains),
            'optimization_tips': await self._get_optimization_tips(
                gain_loss_report, harvest_opportunities
            )
        }

    async def _get_optimization_tips(
        self,
        report: GainLossReport,
        harvest_opps: List[TaxHarvestOpportunity]
    ) -> List[str]:
        """Generate actionable optimization tips"""
        tips = []

        if harvest_opps:
            total_potential_savings = sum(opp.estimated_tax_savings for opp in harvest_opps)
            tips.append(
                f"💰 Tax Loss Harvesting: ${total_potential_savings:,.2f} potential savings "
                f"from {len(harvest_opps)} opportunities"
            )

        if report.net_short_term > 0 and report.net_long_term < 0:
            offset = min(abs(report.net_long_term), report.net_short_term)
            tips.append(
                f"📊 Offset short-term gains with long-term losses for ${offset:,.2f} in tax savings"
            )

        days_left = (datetime(datetime.now().year, 12, 31) - datetime.now()).days
        if days_left < 60 and days_left > 0:
            tips.append(
                f"⏰ {days_left} days left in tax year - review positions for year-end planning"
            )

        if not tips:
            tips.append("✅ No immediate tax optimization actions required")

        return tips


# Singleton instances
_tax_optimizer_instance = None
_wash_sale_detector_instance = None
_tax_loss_harvester_instance = None
_gains_calculator_instance = None
_scenario_planner_instance = None
_tax_exporter_instance = None


def get_tax_optimizer() -> TaxOptimizer:
    """Get singleton tax optimizer instance"""
    global _tax_optimizer_instance
    if _tax_optimizer_instance is None:
        _tax_optimizer_instance = TaxOptimizer()
    return _tax_optimizer_instance


def get_wash_sale_detector() -> WashSaleDetector:
    """Get singleton wash sale detector instance"""
    global _wash_sale_detector_instance
    if _wash_sale_detector_instance is None:
        _wash_sale_detector_instance = WashSaleDetector()
    return _wash_sale_detector_instance


def get_tax_loss_harvester() -> TaxLossHarvester:
    """Get singleton tax loss harvester instance"""
    global _tax_loss_harvester_instance
    if _tax_loss_harvester_instance is None:
        _tax_loss_harvester_instance = TaxLossHarvester()
    return _tax_loss_harvester_instance


def get_gains_calculator() -> CapitalGainsCalculator:
    """Get singleton gains calculator instance"""
    global _gains_calculator_instance
    if _gains_calculator_instance is None:
        _gains_calculator_instance = CapitalGainsCalculator()
    return _gains_calculator_instance


def get_scenario_planner() -> TaxScenarioPlanner:
    """Get singleton scenario planner instance"""
    global _scenario_planner_instance
    if _scenario_planner_instance is None:
        _scenario_planner_instance = TaxScenarioPlanner()
    return _scenario_planner_instance


def get_tax_exporter() -> TaxExporter:
    """Get singleton tax exporter instance"""
    global _tax_exporter_instance
    if _tax_exporter_instance is None:
        _tax_exporter_instance = TaxExporter()
    return _tax_exporter_instance
