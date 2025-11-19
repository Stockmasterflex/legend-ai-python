"""
Crypto-Specific Alert System

Features:
- Price alerts (threshold-based)
- Whale alerts (large transactions)
- Exchange inflow/outflow alerts
- Network congestion alerts
- Funding rate extremes
- Open interest spikes
- Bitcoin dominance changes
"""

import asyncio
import logging
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
import httpx

from app.config import get_settings
from app.services.cache import get_cache_service
from app.services.crypto_data import crypto_data_service
from app.services.crypto_patterns import crypto_pattern_analyzer
from app.services.correlation_analysis import correlation_analysis_service

logger = logging.getLogger(__name__)
settings = get_settings()


class CryptoAlertService:
    """
    Crypto-specific alert service

    Alert types:
    1. Price alerts (above/below threshold)
    2. Whale movement alerts
    3. Exchange flow alerts (large inflows/outflows)
    4. Network congestion (high gas fees)
    5. Funding rate extremes
    6. Open interest spikes
    7. Bitcoin dominance shifts
    """

    def __init__(self):
        self.cache = get_cache_service()
        self.telegram_api_key = settings.telegram_bot_token
        self.telegram_chat_id = settings.telegram_chat_id
        self.last_alerted = {}  # Track last alert time per symbol to avoid spam
        self.alert_cooldown_seconds = 3600  # 1 hour between similar alerts

        # Alert thresholds
        self.price_change_threshold = 5.0  # 5% price change
        self.whale_volume_threshold = 3.0  # 3 std dev
        self.funding_rate_threshold = 0.05  # 5% annualized
        self.gas_price_threshold = 100  # Gwei
        self.btc_dominance_change_threshold = 2.0  # 2% change

    async def monitor_price_alerts(
        self,
        watchlist: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Monitor price alerts for watchlist

        Watchlist format:
        [
            {
                "symbol": "BTCUSDT",
                "alert_above": 50000,
                "alert_below": 40000
            }
        ]
        """
        alerts = []

        for item in watchlist:
            symbol = item.get("symbol", "")
            alert_above = item.get("alert_above")
            alert_below = item.get("alert_below")

            if not symbol:
                continue

            # Get current price
            price_data = await crypto_data_service.get_realtime_price(
                symbol.replace("USDT", ""),
                "USDT"
            )

            if not price_data:
                continue

            current_price = price_data.get("price", 0)

            # Check thresholds
            triggered = False
            alert_type = None

            if alert_above and current_price >= alert_above:
                triggered = True
                alert_type = "price_above"
            elif alert_below and current_price <= alert_below:
                triggered = True
                alert_type = "price_below"

            if triggered:
                # Check cooldown
                alert_key = f"{symbol}_{alert_type}"
                if not self._check_cooldown(alert_key):
                    continue

                alert_data = {
                    "type": alert_type,
                    "symbol": symbol,
                    "current_price": current_price,
                    "threshold": alert_above if alert_type == "price_above" else alert_below,
                    "timestamp": datetime.now().isoformat()
                }

                await self._send_telegram_alert(
                    f"🚨 Price Alert: {symbol}\n"
                    f"Current: ${current_price:,.2f}\n"
                    f"Threshold: ${alert_data['threshold']:,.2f}\n"
                    f"Condition: {'Above' if alert_type == 'price_above' else 'Below'}"
                )

                alerts.append(alert_data)
                self._update_cooldown(alert_key)

        return alerts

    async def monitor_whale_movements(
        self,
        symbols: List[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Monitor whale movements for specified symbols

        Default symbols: BTCUSDT, ETHUSDT
        """
        if symbols is None:
            symbols = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT"]

        alerts = []

        for symbol in symbols:
            # Analyze whale activity
            whale_data = await crypto_pattern_analyzer.whale_detector.detect_whale_activity(
                symbol=symbol,
                lookback_hours=24
            )

            if whale_data.get("whale_detected"):
                # Check cooldown
                alert_key = f"{symbol}_whale"
                if not self._check_cooldown(alert_key):
                    continue

                volume_spike = whale_data.get("volume_spike", 0)
                sentiment = whale_data.get("sentiment", "unknown")
                total_volume = whale_data.get("total_whale_volume_usd", 0)

                alert_data = {
                    "type": "whale_movement",
                    "symbol": symbol,
                    "volume_spike": volume_spike,
                    "sentiment": sentiment,
                    "total_volume_usd": total_volume,
                    "confidence": whale_data.get("confidence", 0),
                    "timestamp": datetime.now().isoformat()
                }

                await self._send_telegram_alert(
                    f"🐋 Whale Alert: {symbol}\n"
                    f"Volume Spike: {volume_spike:.1f}σ above mean\n"
                    f"Sentiment: {sentiment.upper()}\n"
                    f"Total Volume: ${total_volume:,.0f}\n"
                    f"Confidence: {whale_data.get('confidence', 0):.0%}"
                )

                alerts.append(alert_data)
                self._update_cooldown(alert_key)

        return alerts

    async def monitor_exchange_flows(
        self,
        symbols: List[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Monitor exchange inflows/outflows

        Large outflows = potentially bullish (accumulation)
        Large inflows = potentially bearish (distribution)
        """
        if symbols is None:
            symbols = ["BTCUSDT", "ETHUSDT"]

        alerts = []

        for symbol in symbols:
            # Analyze exchange flow
            flow_data = await crypto_pattern_analyzer.flow_analyzer.analyze_exchange_flow(
                symbol=symbol,
                lookback_hours=24
            )

            if flow_data.get("confidence", 0) > 0.6:
                flow_trend = flow_data.get("flow_trend", "")
                net_flow_usd = flow_data.get("net_flow_usd", 0)

                # Alert on significant flows (> $10M)
                if abs(net_flow_usd) > 10_000_000:
                    alert_key = f"{symbol}_flow_{flow_trend}"
                    if not self._check_cooldown(alert_key):
                        continue

                    alert_data = {
                        "type": "exchange_flow",
                        "symbol": symbol,
                        "flow_trend": flow_trend,
                        "net_flow_usd": net_flow_usd,
                        "signal": flow_data.get("signal", ""),
                        "timestamp": datetime.now().isoformat()
                    }

                    emoji = "📤" if flow_trend == "outflow" else "📥"
                    signal = flow_data.get("signal", "neutral").upper()

                    await self._send_telegram_alert(
                        f"{emoji} Exchange Flow Alert: {symbol}\n"
                        f"Trend: {flow_trend.upper()}\n"
                        f"Net Flow: ${net_flow_usd:,.0f}\n"
                        f"Signal: {signal}\n"
                        f"Confidence: {flow_data.get('confidence', 0):.0%}"
                    )

                    alerts.append(alert_data)
                    self._update_cooldown(alert_key)

        return alerts

    async def monitor_network_congestion(self) -> List[Dict[str, Any]]:
        """
        Monitor network congestion (high gas fees)
        """
        alerts = []

        # Get current gas prices
        from app.services.defi_analytics import defi_analytics_service
        gas_data = await defi_analytics_service.gas_optimizer.get_gas_prices("ethereum")

        if not gas_data:
            return alerts

        standard_gas = gas_data.get("standard", 0)

        # Alert if gas is above threshold
        if standard_gas > self.gas_price_threshold:
            alert_key = "eth_gas_high"
            if not self._check_cooldown(alert_key):
                return alerts

            alert_data = {
                "type": "network_congestion",
                "chain": "ethereum",
                "standard_gas": standard_gas,
                "recommendation": gas_data.get("recommendation", ""),
                "timestamp": datetime.now().isoformat()
            }

            await self._send_telegram_alert(
                f"⛽ High Gas Alert: Ethereum\n"
                f"Standard Gas: {standard_gas} Gwei\n"
                f"Recommendation: {gas_data.get('recommendation', 'Wait for lower fees')}"
            )

            alerts.append(alert_data)
            self._update_cooldown(alert_key)

        return alerts

    async def monitor_funding_rates(
        self,
        symbols: List[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Monitor funding rate extremes
        """
        if symbols is None:
            symbols = ["BTCUSDT", "ETHUSDT"]

        alerts = []

        for symbol in symbols:
            # Get funding rate analysis
            funding_data = await crypto_pattern_analyzer.funding_analyzer.analyze_funding_rate(symbol)

            if funding_data.get("reversal_risk") == "high":
                alert_key = f"{symbol}_funding_{funding_data.get('signal')}"
                if not self._check_cooldown(alert_key):
                    continue

                funding_rate_pct = funding_data.get("funding_rate_annualized_pct", 0)
                signal = funding_data.get("signal", "")
                sentiment = funding_data.get("sentiment", "")

                alert_data = {
                    "type": "funding_rate_extreme",
                    "symbol": symbol,
                    "funding_rate_annualized_pct": funding_rate_pct,
                    "signal": signal,
                    "sentiment": sentiment,
                    "timestamp": datetime.now().isoformat()
                }

                emoji = "⚠️" if "top" in signal else "💡"

                await self._send_telegram_alert(
                    f"{emoji} Funding Rate Alert: {symbol}\n"
                    f"Annualized Rate: {funding_rate_pct:+.2f}%\n"
                    f"Sentiment: {sentiment.upper()}\n"
                    f"Signal: {signal.replace('_', ' ').title()}\n"
                    f"⚠️ High reversal risk!"
                )

                alerts.append(alert_data)
                self._update_cooldown(alert_key)

        return alerts

    async def monitor_open_interest(
        self,
        symbols: List[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Monitor open interest spikes
        """
        if symbols is None:
            symbols = ["BTCUSDT", "ETHUSDT"]

        alerts = []

        for symbol in symbols:
            # Get OI analysis
            oi_data = await crypto_pattern_analyzer.oi_analyzer.analyze_open_interest(symbol, 24)

            if oi_data.get("liquidation_risk") == "high":
                alert_key = f"{symbol}_oi_high"
                if not self._check_cooldown(alert_key):
                    continue

                trend = oi_data.get("trend", "")
                signal = oi_data.get("signal", "")

                alert_data = {
                    "type": "open_interest_spike",
                    "symbol": symbol,
                    "trend": trend,
                    "signal": signal,
                    "liquidation_risk": "high",
                    "timestamp": datetime.now().isoformat()
                }

                await self._send_telegram_alert(
                    f"⚡ Open Interest Alert: {symbol}\n"
                    f"Trend: {trend.replace('_', ' ').title()}\n"
                    f"Signal: {signal.upper()}\n"
                    f"⚠️ High liquidation risk - expect volatility!"
                )

                alerts.append(alert_data)
                self._update_cooldown(alert_key)

        return alerts

    async def monitor_btc_dominance(self) -> List[Dict[str, Any]]:
        """
        Monitor Bitcoin dominance shifts
        """
        alerts = []

        # Get BTC dominance
        dominance_data = await correlation_analysis_service.btc_dominance.get_bitcoin_dominance()

        if dominance_data.get("signal") in ["flight_to_quality", "alt_rotation"]:
            alert_key = f"btc_dominance_{dominance_data.get('signal')}"
            if not self._check_cooldown(alert_key):
                return alerts

            btc_dom = dominance_data.get("btc_dominance", 0)
            regime = dominance_data.get("regime", "")
            signal = dominance_data.get("signal", "")

            alert_data = {
                "type": "btc_dominance_shift",
                "btc_dominance": btc_dom,
                "regime": regime,
                "signal": signal,
                "timestamp": datetime.now().isoformat()
            }

            emoji = "🏃" if signal == "flight_to_quality" else "🔄"

            await self._send_telegram_alert(
                f"{emoji} BTC Dominance Alert\n"
                f"Current: {btc_dom:.1f}%\n"
                f"Regime: {regime.replace('_', ' ').title()}\n"
                f"Signal: {signal.replace('_', ' ').title()}\n"
                f"{dominance_data.get('interpretation', '')}"
            )

            alerts.append(alert_data)
            self._update_cooldown(alert_key)

        return alerts

    async def monitor_all(
        self,
        price_watchlist: List[Dict[str, Any]] = None,
        symbols: List[str] = None
    ) -> Dict[str, Any]:
        """
        Monitor all crypto alert types

        Returns:
            {
                "price_alerts": [...],
                "whale_alerts": [...],
                "flow_alerts": [...],
                "gas_alerts": [...],
                "funding_alerts": [...],
                "oi_alerts": [...],
                "dominance_alerts": [...],
                "total_alerts": 10
            }
        """
        if symbols is None:
            symbols = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT"]

        # Run all monitors in parallel
        tasks = [
            self.monitor_whale_movements(symbols),
            self.monitor_exchange_flows(symbols[:2]),  # Only BTC and ETH for flows
            self.monitor_network_congestion(),
            self.monitor_funding_rates(symbols[:2]),
            self.monitor_open_interest(symbols[:2]),
            self.monitor_btc_dominance()
        ]

        if price_watchlist:
            tasks.insert(0, self.monitor_price_alerts(price_watchlist))

        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Process results
        price_alerts = results[0] if price_watchlist and not isinstance(results[0], Exception) else []
        whale_alerts = results[1 if price_watchlist else 0] if not isinstance(results[1 if price_watchlist else 0], Exception) else []
        flow_alerts = results[2 if price_watchlist else 1] if not isinstance(results[2 if price_watchlist else 1], Exception) else []
        gas_alerts = results[3 if price_watchlist else 2] if not isinstance(results[3 if price_watchlist else 2], Exception) else []
        funding_alerts = results[4 if price_watchlist else 3] if not isinstance(results[4 if price_watchlist else 3], Exception) else []
        oi_alerts = results[5 if price_watchlist else 4] if not isinstance(results[5 if price_watchlist else 4], Exception) else []
        dominance_alerts = results[6 if price_watchlist else 5] if not isinstance(results[6 if price_watchlist else 5], Exception) else []

        total_alerts = (
            len(price_alerts) + len(whale_alerts) + len(flow_alerts) +
            len(gas_alerts) + len(funding_alerts) + len(oi_alerts) +
            len(dominance_alerts)
        )

        return {
            "price_alerts": price_alerts,
            "whale_alerts": whale_alerts,
            "flow_alerts": flow_alerts,
            "gas_alerts": gas_alerts,
            "funding_alerts": funding_alerts,
            "oi_alerts": oi_alerts,
            "dominance_alerts": dominance_alerts,
            "total_alerts": total_alerts,
            "timestamp": datetime.now().isoformat()
        }

    def _check_cooldown(self, alert_key: str) -> bool:
        """Check if alert is not on cooldown"""
        last_time = self.last_alerted.get(alert_key)
        if last_time:
            elapsed = (datetime.now() - last_time).total_seconds()
            return elapsed > self.alert_cooldown_seconds
        return True

    def _update_cooldown(self, alert_key: str):
        """Update last alerted time"""
        self.last_alerted[alert_key] = datetime.now()

    async def _send_telegram_alert(self, message: str):
        """Send Telegram alert"""
        if not self.telegram_api_key or not self.telegram_chat_id:
            logger.warning("Telegram not configured, skipping alert")
            return

        try:
            async with httpx.AsyncClient() as client:
                url = f"https://api.telegram.org/bot{self.telegram_api_key}/sendMessage"
                data = {
                    "chat_id": self.telegram_chat_id,
                    "text": message,
                    "parse_mode": "HTML"
                }
                response = await client.post(url, json=data)

                if response.status_code == 200:
                    logger.info(f"✅ Telegram alert sent: {message[:50]}...")
                else:
                    logger.error(f"❌ Telegram alert failed: {response.status_code}")

        except Exception as e:
            logger.exception(f"Failed to send Telegram alert: {e}")


# Global instance
crypto_alert_service = CryptoAlertService()
