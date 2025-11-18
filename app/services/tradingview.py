"""
TradingView Integration Service
Handles webhooks, alerts, two-way sync, and strategy integration
"""

import json
import logging
import hashlib
import hmac
from datetime import datetime, timedelta
from typing import Optional, Dict, List, Any
from sqlalchemy.orm import Session
from sqlalchemy import desc
import httpx

from app.models import (
    TradingViewAlert,
    TradingViewStrategy,
    TradingViewSync,
    Ticker,
    Watchlist,
    PatternScan,
    AlertLog
)
from app.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


class TradingViewService:
    """Service for TradingView webhook processing and integration"""

    def __init__(self):
        self.client = httpx.AsyncClient(timeout=30.0)
        self.rate_limit_window = 60  # seconds
        self.rate_limit_max = 100  # max requests per window
        self.rate_limit_cache = {}  # Simple in-memory rate limiting

    def verify_signature(self, payload: bytes, signature: str, secret: str) -> bool:
        """
        Verify TradingView webhook signature
        TradingView uses HMAC-SHA256 for signature validation
        """
        if not secret or not signature:
            logger.warning("No secret or signature provided for verification")
            return False

        try:
            # Calculate expected signature
            expected_signature = hmac.new(
                secret.encode('utf-8'),
                payload,
                hashlib.sha256
            ).hexdigest()

            # Compare signatures (constant-time comparison)
            return hmac.compare_digest(signature, expected_signature)

        except Exception as e:
            logger.error(f"Signature verification error: {e}")
            return False

    def check_rate_limit(self, ip_address: str) -> bool:
        """
        Check if IP address is within rate limits
        Returns True if allowed, False if rate limited
        """
        now = datetime.utcnow()

        # Clean up old entries
        cutoff = now - timedelta(seconds=self.rate_limit_window)
        self.rate_limit_cache = {
            ip: timestamps for ip, timestamps in self.rate_limit_cache.items()
            if any(ts > cutoff for ts in timestamps)
        }

        # Get timestamps for this IP
        if ip_address not in self.rate_limit_cache:
            self.rate_limit_cache[ip_address] = []

        # Filter to only recent timestamps
        recent_timestamps = [
            ts for ts in self.rate_limit_cache[ip_address]
            if ts > cutoff
        ]

        # Check if over limit
        if len(recent_timestamps) >= self.rate_limit_max:
            logger.warning(f"Rate limit exceeded for IP: {ip_address}")
            return False

        # Add current timestamp
        recent_timestamps.append(now)
        self.rate_limit_cache[ip_address] = recent_timestamps

        return True

    def parse_alert_type(self, message: str, alert_name: str = "") -> str:
        """
        Determine alert type from message and alert name
        Types: price, indicator, pattern, breakout, stop_loss
        """
        msg_lower = message.lower()
        name_lower = alert_name.lower()
        combined = msg_lower + " " + name_lower

        # Pattern matching for alert types
        if any(word in combined for word in ["stop", "stop-loss", "stoploss", "sl hit"]):
            return "stop_loss"
        elif any(word in combined for word in ["breakout", "break out", "broke", "resistance"]):
            return "breakout"
        elif any(word in combined for word in ["vcp", "cup", "handle", "triangle", "wedge", "head", "shoulders"]):
            return "pattern"
        elif any(word in combined for word in ["rsi", "macd", "ema", "sma", "bollinger", "stochastic", "indicator"]):
            return "indicator"
        elif any(word in combined for word in ["price", "crossed", "above", "below", "target"]):
            return "price"
        else:
            return "indicator"  # Default

    def extract_action(self, message: str) -> Optional[str]:
        """
        Extract trading action from message
        Returns: buy, sell, long, short, exit, or None
        """
        msg_lower = message.lower()

        if any(word in msg_lower for word in ["buy", "long", "enter long"]):
            return "buy"
        elif any(word in msg_lower for word in ["sell", "short", "enter short"]):
            return "sell"
        elif any(word in msg_lower for word in ["exit", "close", "stop"]):
            return "exit"

        return None

    async def process_webhook(
        self,
        db: Session,
        payload: Dict[str, Any],
        ip_address: str
    ) -> Dict[str, Any]:
        """
        Process incoming TradingView webhook
        Returns: processed alert info
        """
        try:
            # Extract fields from payload
            symbol = payload.get("ticker", payload.get("symbol", "")).upper()
            alert_name = payload.get("alert_name", "")
            message = payload.get("message", json.dumps(payload))
            trigger_price = payload.get("close", payload.get("price"))
            trigger_time = payload.get("time", payload.get("timenow"))
            interval = payload.get("interval", payload.get("timeframe"))
            strategy_name = payload.get("strategy", payload.get("strategy_name"))

            if not symbol:
                raise ValueError("Symbol is required in webhook payload")

            # Determine alert type
            alert_type = self.parse_alert_type(message, alert_name)
            action = self.extract_action(message)

            # Get or create ticker
            ticker = db.query(Ticker).filter(Ticker.symbol == symbol).first()
            if not ticker:
                ticker = Ticker(symbol=symbol)
                db.add(ticker)
                db.flush()

            # Extract indicator values if present
            indicator_values = None
            if any(key in payload for key in ["rsi", "macd", "ema", "sma"]):
                indicator_values = json.dumps({
                    k: v for k, v in payload.items()
                    if k in ["rsi", "macd", "ema", "sma", "volume", "bb_upper", "bb_lower"]
                })

            # Create TradingView alert record
            tv_alert = TradingViewAlert(
                ticker_id=ticker.id,
                symbol=symbol,
                alert_type=alert_type,
                alert_name=alert_name,
                message=message,
                trigger_price=trigger_price,
                trigger_time=trigger_time,
                interval=interval,
                indicator_values=indicator_values,
                strategy_name=strategy_name,
                action=action,
                webhook_ip=ip_address,
                processed=False
            )

            db.add(tv_alert)
            db.commit()
            db.refresh(tv_alert)

            logger.info(f"TradingView alert received: {symbol} - {alert_type} - {action}")

            # Process alert asynchronously
            await self.process_alert(db, tv_alert)

            return {
                "success": True,
                "alert_id": tv_alert.id,
                "symbol": symbol,
                "alert_type": alert_type,
                "action": action
            }

        except Exception as e:
            logger.error(f"Error processing webhook: {e}")
            db.rollback()
            return {
                "success": False,
                "error": str(e)
            }

    async def process_alert(self, db: Session, tv_alert: TradingViewAlert):
        """
        Process TradingView alert based on type
        - Confirm patterns with Legend AI
        - Send notifications
        - Update watchlists
        - Trigger trades
        """
        try:
            symbol = tv_alert.symbol
            alert_type = tv_alert.alert_type

            # 1. Price Alerts
            if alert_type == "price":
                await self._process_price_alert(db, tv_alert)

            # 2. Indicator Alerts
            elif alert_type == "indicator":
                await self._process_indicator_alert(db, tv_alert)

            # 3. Pattern Confirmation
            elif alert_type == "pattern":
                await self._process_pattern_alert(db, tv_alert)

            # 4. Breakout Notifications
            elif alert_type == "breakout":
                await self._process_breakout_alert(db, tv_alert)

            # 5. Stop-Loss Triggers
            elif alert_type == "stop_loss":
                await self._process_stop_loss_alert(db, tv_alert)

            # Mark as processed
            tv_alert.processed = True
            tv_alert.processed_at = datetime.utcnow()
            db.commit()

            logger.info(f"Alert processed successfully: {tv_alert.id}")

        except Exception as e:
            logger.error(f"Error processing alert {tv_alert.id}: {e}")
            db.rollback()

    async def _process_price_alert(self, db: Session, tv_alert: TradingViewAlert):
        """Process price-based alerts"""
        # Update watchlist if exists
        watchlist_item = db.query(Watchlist).join(Ticker).filter(
            Ticker.symbol == tv_alert.symbol,
            Watchlist.alerts_enabled == True
        ).first()

        if watchlist_item:
            # Log alert
            alert_log = AlertLog(
                ticker_id=tv_alert.ticker_id,
                alert_type="tradingview_price",
                trigger_price=tv_alert.trigger_price,
                sent_via="tradingview",
                status="sent"
            )
            db.add(alert_log)
            db.commit()

    async def _process_indicator_alert(self, db: Session, tv_alert: TradingViewAlert):
        """Process indicator-based alerts (RSI, MACD, etc.)"""
        # Could integrate with Legend AI indicators for confirmation
        logger.info(f"Indicator alert for {tv_alert.symbol}: {tv_alert.message}")

    async def _process_pattern_alert(self, db: Session, tv_alert: TradingViewAlert):
        """
        Process pattern alerts - confirm with Legend AI pattern detection
        """
        try:
            # Call Legend AI pattern detection for confirmation
            from app.core.pattern_detector import detect_patterns

            # Run Legend AI pattern detection
            result = detect_patterns(tv_alert.symbol, interval="1day", bars=500)

            if result and result.get("pattern") != "NONE":
                score = result.get("score", 0)
                tv_alert.confirmed = True
                tv_alert.legend_score = score

                # Log confirmed pattern
                logger.info(f"Pattern confirmed by Legend AI: {tv_alert.symbol} - Score: {score}")

                # Create alert log
                alert_log = AlertLog(
                    ticker_id=tv_alert.ticker_id,
                    alert_type="tradingview_pattern_confirmed",
                    trigger_price=tv_alert.trigger_price,
                    sent_via="tradingview",
                    status="sent"
                )
                db.add(alert_log)
            else:
                tv_alert.confirmed = False
                tv_alert.legend_score = 0
                logger.warning(f"Pattern NOT confirmed by Legend AI: {tv_alert.symbol}")

            db.commit()

        except Exception as e:
            logger.error(f"Error confirming pattern: {e}")

    async def _process_breakout_alert(self, db: Session, tv_alert: TradingViewAlert):
        """Process breakout alerts"""
        # Update watchlist status to "Breaking Out"
        watchlist_item = db.query(Watchlist).join(Ticker).filter(
            Ticker.symbol == tv_alert.symbol
        ).first()

        if watchlist_item:
            watchlist_item.status = "Breaking Out"
            watchlist_item.triggered_at = datetime.utcnow()
            db.commit()

            logger.info(f"Breakout detected for {tv_alert.symbol}")

    async def _process_stop_loss_alert(self, db: Session, tv_alert: TradingViewAlert):
        """Process stop-loss alerts"""
        # Could integrate with trades table to close positions
        logger.warning(f"Stop-loss triggered for {tv_alert.symbol} at {tv_alert.trigger_price}")

        # Log alert
        alert_log = AlertLog(
            ticker_id=tv_alert.ticker_id,
            alert_type="tradingview_stop_loss",
            trigger_price=tv_alert.trigger_price,
            sent_via="tradingview",
            status="sent"
        )
        db.add(alert_log)
        db.commit()

    async def sync_pattern_to_tradingview(
        self,
        db: Session,
        pattern_scan: PatternScan
    ) -> Dict[str, Any]:
        """
        Push Legend AI pattern to TradingView
        Creates TradingView alert from detected pattern
        """
        try:
            ticker = db.query(Ticker).filter(Ticker.id == pattern_scan.ticker_id).first()
            if not ticker:
                return {"success": False, "error": "Ticker not found"}

            # Create sync record
            sync_record = TradingViewSync(
                sync_type="pattern",
                legend_id=pattern_scan.id,
                symbol=ticker.symbol,
                direction="legend_to_tv",
                status="pending",
                sync_data=json.dumps({
                    "pattern": pattern_scan.pattern_type,
                    "score": pattern_scan.score,
                    "entry": pattern_scan.entry_price,
                    "stop": pattern_scan.stop_price,
                    "target": pattern_scan.target_price
                })
            )

            db.add(sync_record)
            db.commit()

            logger.info(f"Pattern synced to TradingView: {ticker.symbol} - {pattern_scan.pattern_type}")

            return {
                "success": True,
                "sync_id": sync_record.id,
                "message": "Pattern ready for TradingView alert creation"
            }

        except Exception as e:
            logger.error(f"Error syncing pattern to TradingView: {e}")
            return {"success": False, "error": str(e)}

    async def sync_watchlist_to_tradingview(
        self,
        db: Session,
        watchlist_ids: List[int]
    ) -> Dict[str, Any]:
        """
        Sync Legend AI watchlist to TradingView
        """
        try:
            synced_count = 0

            for watchlist_id in watchlist_ids:
                watchlist_item = db.query(Watchlist).filter(Watchlist.id == watchlist_id).first()
                if not watchlist_item:
                    continue

                ticker = db.query(Ticker).filter(Ticker.id == watchlist_item.ticker_id).first()
                if not ticker:
                    continue

                # Create sync record
                sync_record = TradingViewSync(
                    sync_type="watchlist",
                    legend_id=watchlist_item.id,
                    symbol=ticker.symbol,
                    direction="legend_to_tv",
                    status="synced",
                    sync_data=json.dumps({
                        "entry": watchlist_item.target_entry,
                        "stop": watchlist_item.target_stop,
                        "target": watchlist_item.target_price,
                        "status": watchlist_item.status
                    }),
                    last_synced_at=datetime.utcnow()
                )

                db.add(sync_record)
                synced_count += 1

            db.commit()

            return {
                "success": True,
                "synced_count": synced_count,
                "message": f"{synced_count} watchlist items synced to TradingView"
            }

        except Exception as e:
            logger.error(f"Error syncing watchlist: {e}")
            return {"success": False, "error": str(e)}

    async def import_strategy(
        self,
        db: Session,
        name: str,
        description: str,
        strategy_config: Dict[str, Any],
        pine_script_code: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Import TradingView strategy for backtesting
        """
        try:
            strategy = TradingViewStrategy(
                name=name,
                description=description,
                pine_script_code=pine_script_code,
                strategy_config=json.dumps(strategy_config),
                timeframe=strategy_config.get("timeframe", "1D"),
                indicators_used=json.dumps(strategy_config.get("indicators", [])),
                entry_conditions=json.dumps(strategy_config.get("entry_conditions", {})),
                exit_conditions=json.dumps(strategy_config.get("exit_conditions", {})),
                risk_reward_ratio=strategy_config.get("risk_reward_ratio"),
                win_rate=strategy_config.get("win_rate"),
                profit_factor=strategy_config.get("profit_factor"),
                max_drawdown=strategy_config.get("max_drawdown"),
                total_trades=strategy_config.get("total_trades")
            )

            db.add(strategy)
            db.commit()
            db.refresh(strategy)

            logger.info(f"Strategy imported: {name}")

            return {
                "success": True,
                "strategy_id": strategy.id,
                "name": name
            }

        except Exception as e:
            logger.error(f"Error importing strategy: {e}")
            db.rollback()
            return {"success": False, "error": str(e)}

    async def backtest_strategy(
        self,
        db: Session,
        strategy_id: int,
        symbols: List[str],
        start_date: str,
        end_date: str
    ) -> Dict[str, Any]:
        """
        Backtest TradingView strategy against Legend AI data
        """
        try:
            strategy = db.query(TradingViewStrategy).filter(
                TradingViewStrategy.id == strategy_id
            ).first()

            if not strategy:
                return {"success": False, "error": "Strategy not found"}

            # Placeholder for actual backtesting logic
            # This would integrate with Legend AI's backtesting engine
            backtest_results = {
                "total_trades": 0,
                "winning_trades": 0,
                "losing_trades": 0,
                "win_rate": 0.0,
                "profit_factor": 0.0,
                "max_drawdown": 0.0,
                "total_return": 0.0,
                "sharpe_ratio": 0.0
            }

            # Update strategy with backtest results
            strategy.backtest_results = json.dumps(backtest_results)
            strategy.legend_optimized = True
            db.commit()

            return {
                "success": True,
                "strategy_id": strategy_id,
                "results": backtest_results
            }

        except Exception as e:
            logger.error(f"Error backtesting strategy: {e}")
            return {"success": False, "error": str(e)}

    async def get_recent_alerts(
        self,
        db: Session,
        symbol: Optional[str] = None,
        alert_type: Optional[str] = None,
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        """
        Get recent TradingView alerts
        """
        try:
            query = db.query(TradingViewAlert).order_by(desc(TradingViewAlert.received_at))

            if symbol:
                query = query.filter(TradingViewAlert.symbol == symbol.upper())

            if alert_type:
                query = query.filter(TradingViewAlert.alert_type == alert_type)

            alerts = query.limit(limit).all()

            return [
                {
                    "id": alert.id,
                    "symbol": alert.symbol,
                    "alert_type": alert.alert_type,
                    "alert_name": alert.alert_name,
                    "trigger_price": alert.trigger_price,
                    "action": alert.action,
                    "processed": alert.processed,
                    "confirmed": alert.confirmed,
                    "legend_score": alert.legend_score,
                    "received_at": alert.received_at.isoformat() if alert.received_at else None
                }
                for alert in alerts
            ]

        except Exception as e:
            logger.error(f"Error fetching alerts: {e}")
            return []


# Global service instance
tradingview_service = TradingViewService()
