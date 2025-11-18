"""
Smart Alerts - AI-powered alert suggestions
Analyzes patterns, market conditions, and historical data to suggest relevant alerts
"""
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
import httpx

from app.models import AlertRule, Ticker, PatternScan, AlertLog
from app.config import get_settings
from app.services.market_data import market_data_service
from app.core.indicators import TechnicalIndicators

logger = logging.getLogger(__name__)
settings = get_settings()


class SmartAlertService:
    """Service for AI-powered alert suggestions"""

    def __init__(self, db: Session):
        self.db = db
        self.indicators = TechnicalIndicators()
        self.openrouter_api_key = settings.openrouter_api_key

    async def suggest_alerts_for_ticker(self, ticker_symbol: str) -> List[Dict[str, Any]]:
        """
        Generate AI-powered alert suggestions for a ticker

        Args:
            ticker_symbol: Stock ticker symbol

        Returns:
            List of suggested alert configurations
        """
        try:
            # Get ticker from database
            ticker = self.db.query(Ticker).filter(Ticker.symbol == ticker_symbol.upper()).first()
            if not ticker:
                ticker = Ticker(symbol=ticker_symbol.upper())
                self.db.add(ticker)
                self.db.commit()
                self.db.refresh(ticker)

            # Get market data
            price_data = await market_data_service.get_time_series(ticker_symbol, "1day", 100)
            if not price_data:
                return []

            # Analyze market conditions
            analysis = await self._analyze_market_conditions(ticker_symbol, price_data)

            # Get AI suggestions
            suggestions = await self._get_ai_suggestions(ticker_symbol, analysis)

            return suggestions

        except Exception as e:
            logger.error(f"Error suggesting alerts for {ticker_symbol}: {e}")
            return []

    async def suggest_pattern_based_alerts(self, user_id: str = "default") -> List[Dict[str, Any]]:
        """
        Suggest alerts based on detected patterns

        Args:
            user_id: User ID to generate suggestions for

        Returns:
            List of pattern-based alert suggestions
        """
        try:
            # Get recent pattern scans
            recent_scans = self.db.query(PatternScan).filter(
                PatternScan.scanned_at >= datetime.now() - timedelta(days=7)
            ).order_by(PatternScan.score.desc()).limit(20).all()

            suggestions = []

            for scan in recent_scans:
                # Get ticker
                ticker = self.db.query(Ticker).filter(Ticker.id == scan.ticker_id).first()
                if not ticker:
                    continue

                # Check if alert already exists
                existing_alert = self.db.query(AlertRule).filter(
                    AlertRule.ticker_id == ticker.id,
                    AlertRule.alert_type == "pattern",
                    AlertRule.is_enabled == True
                ).first()

                if existing_alert:
                    continue  # Skip if alert already exists

                # Create suggestion based on pattern
                suggestion = {
                    "ticker_symbol": ticker.symbol,
                    "alert_type": "pattern",
                    "name": f"{ticker.symbol} - {scan.pattern_type} Breakout Alert",
                    "description": f"Alert when {ticker.symbol} breaks out from {scan.pattern_type} pattern",
                    "pattern_type": scan.pattern_type,
                    "entry_price": scan.entry_price,
                    "conditions": [
                        {
                            "field": "price",
                            "operator": "greater_than",
                            "value": scan.entry_price,
                            "value_type": "absolute"
                        },
                        {
                            "field": "volume",
                            "operator": "greater_than",
                            "value": 50,  # 50% above average
                            "value_type": "percentage"
                        }
                    ],
                    "condition_logic": "AND",
                    "confidence": scan.score,
                    "reason": f"Strong {scan.pattern_type} pattern detected with {scan.score:.1%} confidence"
                }

                suggestions.append(suggestion)

            return suggestions

        except Exception as e:
            logger.error(f"Error suggesting pattern-based alerts: {e}")
            return []

    async def suggest_risk_based_alerts(self, ticker_symbol: str) -> List[Dict[str, Any]]:
        """
        Suggest risk-based alerts (stop losses, take profits)

        Args:
            ticker_symbol: Stock ticker symbol

        Returns:
            List of risk-based alert suggestions
        """
        try:
            # Get current price and ATR for volatility
            price_data = await market_data_service.get_time_series(ticker_symbol, "1day", 50)
            if not price_data:
                return []

            current_price = price_data[-1]["close"]

            # Calculate ATR (Average True Range) for stop loss
            atr = await self._calculate_atr(price_data)

            suggestions = []

            # Stop loss suggestion (2x ATR below current price)
            stop_loss_price = current_price - (2 * atr)
            suggestions.append({
                "ticker_symbol": ticker_symbol,
                "alert_type": "price",
                "name": f"{ticker_symbol} - Stop Loss Alert",
                "description": f"Alert if {ticker_symbol} drops below stop loss level",
                "conditions": [
                    {
                        "field": "price",
                        "operator": "less_than",
                        "value": stop_loss_price,
                        "value_type": "absolute"
                    }
                ],
                "condition_logic": "AND",
                "delivery_channels": ["telegram", "email", "sms"],  # High priority
                "reason": f"Risk management: 2x ATR stop loss at ${stop_loss_price:.2f}"
            })

            # Take profit suggestion (3x ATR above current price for 1.5:1 R/R)
            take_profit_price = current_price + (3 * atr)
            suggestions.append({
                "ticker_symbol": ticker_symbol,
                "alert_type": "price",
                "name": f"{ticker_symbol} - Take Profit Alert",
                "description": f"Alert if {ticker_symbol} reaches profit target",
                "conditions": [
                    {
                        "field": "price",
                        "operator": "greater_than",
                        "value": take_profit_price,
                        "value_type": "absolute"
                    }
                ],
                "condition_logic": "AND",
                "delivery_channels": ["telegram", "email"],
                "reason": f"Profit target: 1.5:1 R/R at ${take_profit_price:.2f}"
            })

            # Trailing stop suggestion (5% below high)
            suggestions.append({
                "ticker_symbol": ticker_symbol,
                "alert_type": "price",
                "name": f"{ticker_symbol} - Trailing Stop Alert",
                "description": f"Alert if {ticker_symbol} drops 5% from recent high",
                "conditions": [
                    {
                        "field": "price_change_percent",
                        "operator": "less_than",
                        "value": -5,
                        "value_type": "percentage"
                    }
                ],
                "condition_logic": "AND",
                "delivery_channels": ["telegram", "email"],
                "reason": "Trailing stop: Protect profits if price drops 5% from recent high"
            })

            return suggestions

        except Exception as e:
            logger.error(f"Error suggesting risk-based alerts for {ticker_symbol}: {e}")
            return []

    async def suggest_correlation_alerts(self, ticker_symbol: str) -> List[Dict[str, Any]]:
        """
        Suggest correlation-based alerts (SPY, sector correlation)

        Args:
            ticker_symbol: Stock ticker symbol

        Returns:
            List of correlation-based alert suggestions
        """
        try:
            suggestions = []

            # SPY correlation alert
            suggestions.append({
                "ticker_symbol": "SPY",
                "alert_type": "indicator",
                "name": f"Market Weakness Alert (for {ticker_symbol})",
                "description": "Alert when SPY shows weakness that might affect your position",
                "conditions": [
                    {
                        "field": "rsi",
                        "operator": "less_than",
                        "value": 30,
                        "value_type": "absolute"
                    }
                ],
                "condition_logic": "OR",
                "delivery_channels": ["telegram"],
                "reason": "Monitor market conditions - SPY weakness could impact individual positions"
            })

            # VIX spike alert
            suggestions.append({
                "ticker_symbol": "VIX",
                "alert_type": "indicator",
                "name": "Volatility Spike Alert",
                "description": "Alert when market volatility spikes",
                "conditions": [
                    {
                        "field": "price_change_percent",
                        "operator": "greater_than",
                        "value": 20,
                        "value_type": "percentage"
                    }
                ],
                "condition_logic": "AND",
                "delivery_channels": ["telegram", "email"],
                "reason": "High volatility warning - consider tightening stops"
            })

            return suggestions

        except Exception as e:
            logger.error(f"Error suggesting correlation alerts: {e}")
            return []

    async def _analyze_market_conditions(self, ticker_symbol: str, price_data: List[Dict]) -> Dict[str, Any]:
        """Analyze current market conditions for a ticker"""
        try:
            if not price_data or len(price_data) < 20:
                return {}

            # Calculate basic indicators
            current_price = price_data[-1]["close"]
            previous_close = price_data[-2]["close"] if len(price_data) > 1 else current_price

            # Price change
            price_change = current_price - previous_close
            price_change_percent = (price_change / previous_close) * 100

            # Volume analysis
            current_volume = price_data[-1].get("volume", 0)
            avg_volume = sum(d.get("volume", 0) for d in price_data[-20:]) / 20
            volume_change_percent = ((current_volume - avg_volume) / avg_volume * 100) if avg_volume > 0 else 0

            # Calculate RSI
            rsi = await self._calculate_rsi(price_data)

            # Trend analysis
            sma_20 = sum(d["close"] for d in price_data[-20:]) / 20
            sma_50 = sum(d["close"] for d in price_data[-50:]) / 50 if len(price_data) >= 50 else sma_20

            trend = "bullish" if sma_20 > sma_50 else "bearish"

            return {
                "ticker": ticker_symbol,
                "current_price": current_price,
                "price_change_percent": price_change_percent,
                "volume_change_percent": volume_change_percent,
                "rsi": rsi,
                "trend": trend,
                "sma_20": sma_20,
                "sma_50": sma_50,
                "is_oversold": rsi < 30,
                "is_overbought": rsi > 70,
                "high_volume": volume_change_percent > 50
            }

        except Exception as e:
            logger.error(f"Error analyzing market conditions: {e}")
            return {}

    async def _get_ai_suggestions(self, ticker_symbol: str, analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get AI-powered alert suggestions using OpenRouter"""
        try:
            if not self.openrouter_api_key:
                logger.warning("OpenRouter API key not configured, skipping AI suggestions")
                return []

            # Create prompt for AI
            prompt = f"""
You are a professional swing trader analyzing {ticker_symbol}. Based on the following market analysis, suggest 2-3 relevant alerts that would be valuable for monitoring this stock.

Market Analysis:
- Current Price: ${analysis.get('current_price', 0):.2f}
- Price Change: {analysis.get('price_change_percent', 0):.2f}%
- Volume Change: {analysis.get('volume_change_percent', 0):.2f}%
- RSI: {analysis.get('rsi', 0):.1f}
- Trend: {analysis.get('trend', 'neutral')}
- Oversold: {analysis.get('is_oversold', False)}
- Overbought: {analysis.get('is_overbought', False)}
- High Volume: {analysis.get('high_volume', False)}

Please suggest alerts in the following JSON format:
[
  {{
    "name": "Alert name",
    "description": "Why this alert is important",
    "alert_type": "price|volume|indicator",
    "conditions": [
      {{
        "field": "price|volume|rsi|price_change_percent",
        "operator": "greater_than|less_than|crosses_above|crosses_below",
        "value": <number>,
        "value_type": "absolute|percentage"
      }}
    ],
    "condition_logic": "AND|OR",
    "reason": "Strategic reasoning for this alert"
  }}
]

Focus on actionable alerts that align with swing trading strategies.
"""

            # Call OpenRouter API
            url = "https://openrouter.ai/api/v1/chat/completions"

            headers = {
                "Authorization": f"Bearer {self.openrouter_api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://legendai.com",
                "X-Title": "Legend AI - Smart Alerts"
            }

            payload = {
                "model": "anthropic/claude-3.5-sonnet",
                "messages": [
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.7,
                "max_tokens": 2000
            }

            async with httpx.AsyncClient(timeout=30) as client:
                response = await client.post(url, json=payload, headers=headers)
                response.raise_for_status()
                result = response.json()

                # Extract AI response
                ai_response = result.get("choices", [{}])[0].get("message", {}).get("content", "")

                # Parse JSON from AI response
                import json
                import re

                # Extract JSON array from response
                json_match = re.search(r'\[[\s\S]*\]', ai_response)
                if json_match:
                    suggestions_json = json_match.group(0)
                    suggestions = json.loads(suggestions_json)

                    # Add ticker symbol to each suggestion
                    for suggestion in suggestions:
                        suggestion["ticker_symbol"] = ticker_symbol

                    return suggestions
                else:
                    logger.warning("Could not parse AI suggestions")
                    return []

        except Exception as e:
            logger.error(f"Error getting AI suggestions: {e}")
            return []

    async def _calculate_rsi(self, price_data: List[Dict], period: int = 14) -> float:
        """Calculate RSI indicator"""
        try:
            if len(price_data) < period + 1:
                return 50.0  # Default neutral

            closes = [d["close"] for d in price_data[-period-1:]]

            gains = []
            losses = []

            for i in range(1, len(closes)):
                change = closes[i] - closes[i-1]
                if change > 0:
                    gains.append(change)
                    losses.append(0)
                else:
                    gains.append(0)
                    losses.append(abs(change))

            avg_gain = sum(gains) / period
            avg_loss = sum(losses) / period

            if avg_loss == 0:
                return 100.0

            rs = avg_gain / avg_loss
            rsi = 100 - (100 / (1 + rs))

            return rsi

        except Exception as e:
            logger.error(f"Error calculating RSI: {e}")
            return 50.0

    async def _calculate_atr(self, price_data: List[Dict], period: int = 14) -> float:
        """Calculate Average True Range"""
        try:
            if len(price_data) < period + 1:
                return 1.0  # Default

            true_ranges = []

            for i in range(1, len(price_data)):
                high = price_data[i]["high"]
                low = price_data[i]["low"]
                prev_close = price_data[i-1]["close"]

                tr = max(
                    high - low,
                    abs(high - prev_close),
                    abs(low - prev_close)
                )
                true_ranges.append(tr)

            atr = sum(true_ranges[-period:]) / period

            return atr

        except Exception as e:
            logger.error(f"Error calculating ATR: {e}")
            return 1.0

    async def auto_create_alert(self, suggestion: Dict[str, Any], user_id: str = "default") -> Optional[AlertRule]:
        """
        Automatically create an alert rule from a suggestion

        Args:
            suggestion: Alert suggestion dictionary
            user_id: User ID to create alert for

        Returns:
            Created AlertRule or None if failed
        """
        try:
            # Get or create ticker
            ticker_symbol = suggestion.get("ticker_symbol")
            if not ticker_symbol:
                return None

            ticker = self.db.query(Ticker).filter(Ticker.symbol == ticker_symbol.upper()).first()
            if not ticker:
                ticker = Ticker(symbol=ticker_symbol.upper())
                self.db.add(ticker)
                self.db.commit()
                self.db.refresh(ticker)

            # Create alert rule
            rule = AlertRule(
                name=suggestion.get("name"),
                description=suggestion.get("description"),
                ticker_id=ticker.id,
                alert_type=suggestion.get("alert_type", "price"),
                condition_logic=suggestion.get("condition_logic", "AND"),
                conditions=suggestion.get("conditions", []),
                delivery_channels=suggestion.get("delivery_channels", ["telegram", "email"]),
                delivery_config=suggestion.get("delivery_config"),
                is_enabled=True,
                user_id=user_id,
                created_by="ai"
            )

            self.db.add(rule)
            self.db.commit()
            self.db.refresh(rule)

            logger.info(f"Auto-created alert rule: {rule.name} (ID: {rule.id}) from AI suggestion")

            return rule

        except Exception as e:
            logger.error(f"Error auto-creating alert: {e}")
            self.db.rollback()
            return None
