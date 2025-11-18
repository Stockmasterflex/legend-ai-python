"""
Alert Rule Engine - Evaluates alert conditions and triggers alerts
Supports complex conditions with AND/OR logic, time-based conditions, and multi-field comparisons
"""
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from app.models import AlertRule, AlertCondition, AlertLog, AlertDelivery, Ticker
from app.services.market_data import market_data_service
from app.core.indicators import TechnicalIndicators

logger = logging.getLogger(__name__)


class AlertRuleEngine:
    """Engine for evaluating alert rules and triggering alerts"""

    def __init__(self, db: Session):
        self.db = db
        self.indicators = TechnicalIndicators()

    async def evaluate_rule(self, rule: AlertRule, market_data: Dict[str, Any]) -> tuple[bool, Dict[str, Any]]:
        """
        Evaluate an alert rule against current market data

        Args:
            rule: AlertRule to evaluate
            market_data: Current market data for the ticker

        Returns:
            Tuple of (triggered: bool, context: Dict with trigger details)
        """
        try:
            # Check if rule is enabled and not snoozed
            if not rule.is_enabled:
                return False, {"reason": "rule_disabled"}

            if rule.is_snoozed and rule.snoozed_until:
                if datetime.now() < rule.snoozed_until:
                    return False, {"reason": "rule_snoozed"}
                else:
                    # Un-snooze if time has passed
                    rule.is_snoozed = False
                    rule.snoozed_until = None
                    self.db.commit()

            # Check cooldown period
            if rule.last_triggered_at:
                cooldown_seconds = rule.cooldown_period or 3600
                time_since_last = (datetime.now() - rule.last_triggered_at).total_seconds()
                if time_since_last < cooldown_seconds:
                    return False, {"reason": "cooldown_active", "seconds_remaining": cooldown_seconds - time_since_last}

            # Evaluate conditions
            conditions = rule.conditions
            if not conditions:
                return False, {"reason": "no_conditions"}

            condition_results = []
            conditions_met = []

            for condition in conditions:
                result = await self._evaluate_condition(condition, market_data, rule)
                condition_results.append(result)
                if result:
                    conditions_met.append(condition)

            # Apply logic (AND/OR)
            logic = rule.condition_logic or "AND"
            triggered = False

            if logic == "AND":
                triggered = all(condition_results)
            elif logic == "OR":
                triggered = any(condition_results)

            context = {
                "conditions_evaluated": len(conditions),
                "conditions_met": conditions_met,
                "logic": logic,
                "triggered": triggered,
                "market_data": market_data
            }

            return triggered, context

        except Exception as e:
            logger.error(f"Error evaluating rule {rule.id}: {e}")
            return False, {"reason": "error", "error": str(e)}

    async def _evaluate_condition(self, condition: Dict[str, Any], market_data: Dict[str, Any], rule: AlertRule) -> bool:
        """
        Evaluate a single condition

        Args:
            condition: Condition definition
            market_data: Current market data
            rule: Parent alert rule

        Returns:
            True if condition is met, False otherwise
        """
        try:
            field = condition.get("field")
            operator = condition.get("operator")
            value = condition.get("value")
            value_type = condition.get("value_type", "absolute")

            # Get current field value from market data or calculate it
            current_value = await self._get_field_value(field, market_data, rule)

            if current_value is None:
                return False

            # Convert value if needed (percentage, etc.)
            if value_type == "percentage":
                # Convert percentage to actual value
                base_value = current_value
                value = base_value * (value / 100)

            # Evaluate operator
            return self._evaluate_operator(operator, current_value, value, market_data)

        except Exception as e:
            logger.error(f"Error evaluating condition {condition}: {e}")
            return False

    async def _get_field_value(self, field: str, market_data: Dict[str, Any], rule: AlertRule) -> Optional[float]:
        """Get the current value of a field from market data or calculate it"""
        try:
            # Direct price fields
            if field == "price":
                return market_data.get("close")
            elif field == "open":
                return market_data.get("open")
            elif field == "high":
                return market_data.get("high")
            elif field == "low":
                return market_data.get("low")
            elif field == "volume":
                return market_data.get("volume")

            # Price change fields
            elif field == "price_change":
                close = market_data.get("close")
                previous_close = market_data.get("previous_close")
                if close and previous_close:
                    return close - previous_close
                return None

            elif field == "price_change_percent":
                close = market_data.get("close")
                previous_close = market_data.get("previous_close")
                if close and previous_close:
                    return ((close - previous_close) / previous_close) * 100
                return None

            # Volume fields
            elif field == "volume_change_percent":
                volume = market_data.get("volume")
                avg_volume = market_data.get("avg_volume")
                if volume and avg_volume:
                    return ((volume - avg_volume) / avg_volume) * 100
                return None

            # Technical indicators (RSI, MACD, etc.)
            elif field in ["rsi", "macd", "macd_signal", "macd_histogram", "sma_20", "sma_50", "sma_200", "ema_20", "ema_50"]:
                # These would come from pre-calculated indicators in market_data
                # or we calculate them on the fly
                indicators = market_data.get("indicators", {})
                return indicators.get(field)

            # Sentiment (from news analysis)
            elif field == "sentiment_score":
                return market_data.get("sentiment_score")

            # Options flow
            elif field == "options_volume":
                return market_data.get("options_volume")
            elif field == "put_call_ratio":
                return market_data.get("put_call_ratio")

            else:
                logger.warning(f"Unknown field: {field}")
                return None

        except Exception as e:
            logger.error(f"Error getting field value for {field}: {e}")
            return None

    def _evaluate_operator(self, operator: str, current_value: float, target_value: float, market_data: Dict[str, Any]) -> bool:
        """Evaluate an operator comparison"""
        try:
            if operator == "greater_than" or operator == ">":
                return current_value > target_value
            elif operator == "greater_than_or_equal" or operator == ">=":
                return current_value >= target_value
            elif operator == "less_than" or operator == "<":
                return current_value < target_value
            elif operator == "less_than_or_equal" or operator == "<=":
                return current_value <= target_value
            elif operator == "equals" or operator == "==":
                return abs(current_value - target_value) < 0.01  # Small tolerance for floats
            elif operator == "not_equals" or operator == "!=":
                return abs(current_value - target_value) >= 0.01

            # Crosses
            elif operator == "crosses_above":
                # Check if value crossed above target in recent data
                previous_value = market_data.get("previous_value")
                if previous_value is not None:
                    return previous_value <= target_value and current_value > target_value
                return False

            elif operator == "crosses_below":
                # Check if value crossed below target in recent data
                previous_value = market_data.get("previous_value")
                if previous_value is not None:
                    return previous_value >= target_value and current_value < target_value
                return False

            # Percentage change
            elif operator == "percentage_change_above":
                return current_value > target_value

            elif operator == "percentage_change_below":
                return current_value < target_value

            else:
                logger.warning(f"Unknown operator: {operator}")
                return False

        except Exception as e:
            logger.error(f"Error evaluating operator {operator}: {e}")
            return False

    async def trigger_alert(self, rule: AlertRule, context: Dict[str, Any]) -> AlertLog:
        """
        Create and send an alert for a triggered rule

        Args:
            rule: AlertRule that was triggered
            context: Context from rule evaluation

        Returns:
            AlertLog record
        """
        try:
            # Get ticker info
            ticker = None
            if rule.ticker_id:
                ticker = self.db.query(Ticker).filter(Ticker.id == rule.ticker_id).first()

            # Create alert message
            alert_title = f"{rule.name} - {ticker.symbol if ticker else 'Alert'}"
            alert_message = self._format_alert_message(rule, context, ticker)

            # Create AlertLog
            alert_log = AlertLog(
                rule_id=rule.id,
                ticker_id=rule.ticker_id,
                user_id=rule.user_id,
                alert_type=rule.alert_type,
                alert_title=alert_title,
                alert_message=alert_message,
                trigger_price=context.get("market_data", {}).get("close"),
                trigger_value=context.get("market_data", {}).get("close"),
                trigger_data=context.get("market_data"),
                conditions_met=context.get("conditions_met"),
                delivery_channels=rule.delivery_channels,
                delivery_status={},
                status="pending"
            )

            self.db.add(alert_log)
            self.db.commit()
            self.db.refresh(alert_log)

            # Update rule
            rule.last_triggered_at = datetime.now()
            rule.trigger_count = (rule.trigger_count or 0) + 1
            self.db.commit()

            logger.info(f"Alert triggered: {alert_title} (ID: {alert_log.id})")

            return alert_log

        except Exception as e:
            logger.error(f"Error triggering alert for rule {rule.id}: {e}")
            self.db.rollback()
            raise

    def _format_alert_message(self, rule: AlertRule, context: Dict[str, Any], ticker: Optional[Ticker]) -> str:
        """Format alert message for delivery"""
        market_data = context.get("market_data", {})

        msg = f"""
🚨 ALERT: {rule.name}
{'=' * 50}

📊 Ticker: {ticker.symbol if ticker else 'N/A'}
📈 Alert Type: {rule.alert_type.upper()}

💰 Current Price: ${market_data.get('close', 0):.2f}
📊 Volume: {market_data.get('volume', 0):,.0f}

📝 Description: {rule.description or 'No description'}

✅ Conditions Met: {len(context.get('conditions_met', []))} / {context.get('conditions_evaluated', 0)}
🔗 Logic: {context.get('logic', 'AND')}

⏰ Triggered: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

"""
        return msg


class ConditionBuilder:
    """Builder for creating alert conditions with fluent API"""

    def __init__(self):
        self.conditions = []
        self.logic = "AND"

    def price(self, operator: str, value: float, value_type: str = "absolute"):
        """Add price condition"""
        self.conditions.append({
            "field": "price",
            "operator": operator,
            "value": value,
            "value_type": value_type
        })
        return self

    def volume(self, operator: str, value: float, value_type: str = "absolute"):
        """Add volume condition"""
        self.conditions.append({
            "field": "volume",
            "operator": operator,
            "value": value,
            "value_type": value_type
        })
        return self

    def rsi(self, operator: str, value: float):
        """Add RSI condition"""
        self.conditions.append({
            "field": "rsi",
            "operator": operator,
            "value": value,
            "value_type": "absolute"
        })
        return self

    def macd_cross(self, direction: str = "above"):
        """Add MACD cross condition"""
        operator = "crosses_above" if direction == "above" else "crosses_below"
        self.conditions.append({
            "field": "macd",
            "operator": operator,
            "value": 0,  # Crosses zero line
            "value_type": "absolute"
        })
        return self

    def percentage_change(self, operator: str, value: float):
        """Add percentage change condition"""
        self.conditions.append({
            "field": "price_change_percent",
            "operator": operator,
            "value": value,
            "value_type": "percentage"
        })
        return self

    def custom(self, field: str, operator: str, value: float, value_type: str = "absolute"):
        """Add custom condition"""
        self.conditions.append({
            "field": field,
            "operator": operator,
            "value": value,
            "value_type": value_type
        })
        return self

    def and_logic(self):
        """Use AND logic for conditions"""
        self.logic = "AND"
        return self

    def or_logic(self):
        """Use OR logic for conditions"""
        self.logic = "OR"
        return self

    def build(self) -> Dict[str, Any]:
        """Build the final conditions object"""
        return {
            "logic": self.logic,
            "conditions": self.conditions
        }
