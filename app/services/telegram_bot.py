"""
Telegram bot integration for Legend AI alerts and commands
"""
import logging
import os
from typing import Optional, Dict, Any, List
from datetime import datetime

logger = logging.getLogger(__name__)

class TelegramBot:
    """Telegram bot for sending alerts and handling commands"""
    
    def __init__(self):
        self.bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
        self.chat_id = os.getenv("TELEGRAM_CHAT_ID")
        self.enabled = bool(self.bot_token and self.chat_id)
        
        if not self.enabled:
            logger.warning("Telegram bot not configured (missing TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID)")
    
    async def send_alert(self, alert: Dict[str, Any]) -> bool:
        """
        Send alert message to Telegram
        
        Args:
            alert: Alert dictionary with ticker, alert_type, prices, etc.
        
        Returns:
            True if sent successfully, False otherwise
        """
        if not self.enabled:
            logger.debug("Telegram bot disabled, skipping alert")
            return False
        
        try:
            message = self._format_alert_message(alert)
            
            # Use Telegram MCP to send message
            from app.mcp_tools import send_telegram_message
            
            result = await send_telegram_message(
                chat_id=int(self.chat_id),
                text=message,
                parse_mode="Markdown"
            )
            
            if result:
                logger.info(f"📤 Telegram alert sent for {alert.get('ticker')}")
                return True
            else:
                logger.warning(f"Failed to send Telegram alert for {alert.get('ticker')}")
                return False
        
        except Exception as e:
            logger.error(f"Telegram alert error: {e}")
            return False
    
    def _format_alert_message(self, alert: Dict[str, Any]) -> str:
        """Format alert as Telegram message"""
        ticker = alert.get("ticker", "???")
        alert_type = alert.get("alert_type", "unknown")
        current_price = alert.get("current_price", 0)
        entry = alert.get("entry")
        stop = alert.get("stop")
        target = alert.get("target")
        volume_ratio = alert.get("volume_ratio", 1.0)
        
        # Emoji mapping
        emoji_map = {
            "breakout": "🚀",
            "stop_hit": "🛑",
            "target_hit": "🎯",
        }
        emoji = emoji_map.get(alert_type, "📊")
        
        # Calculate percentage moves if possible
        entry_pct = ""
        if entry and entry > 0:
            pct_change = ((current_price - entry) / entry) * 100
            entry_pct = f" ({pct_change:+.1f}%)"
        
        # Build message
        if alert_type == "breakout":
            message = f"{emoji} *{ticker} Breaking Out!*\n\n"
            message += f"Entry: ${entry:.2f}\n"
            message += f"Current: ${current_price:.2f}{entry_pct}\n"
            if stop:
                message += f"Stop: ${stop:.2f}\n"
            if target:
                message += f"Target: ${target:.2f}\n"
            if volume_ratio > 1:
                message += f"Volume: {volume_ratio:.1f}x average\n"
            
            # Calculate R:R if we have all prices
            if entry and stop and target:
                risk = entry - stop
                reward = target - entry
                if risk > 0:
                    rr = reward / risk
                    message += f"R:R: {rr:.1f}:1\n"
        
        elif alert_type == "stop_hit":
            message = f"{emoji} *{ticker} Stop Hit*\n\n"
            if stop:
                message += f"Stop: ${stop:.2f}\n"
            message += f"Current: ${current_price:.2f}\n"
        
        elif alert_type == "target_hit":
            message = f"{emoji} *{ticker} Target Hit!*\n\n"
            if target:
                message += f"Target: ${target:.2f}\n"
            message += f"Current: ${current_price:.2f}\n"
            if entry:
                gain_pct = ((current_price - entry) / entry) * 100
                message += f"Gain: +{gain_pct:.1f}%\n"
        
        else:
            message = f"{emoji} *{ticker} Alert*\n\n"
            message += f"Price: ${current_price:.2f}\n"
            message += f"Status: {alert.get('new_status', 'Unknown')}\n"
        
        # Add timestamp
        timestamp = datetime.now().strftime("%I:%M %p ET")
        message += f"\n_Time: {timestamp}_"
        
        return message
    
    async def send_message(self, text: str) -> bool:
        """Send a plain text message to Telegram"""
        if not self.enabled:
            return False
        
        try:
            from app.mcp_tools import send_telegram_message
            
            result = await send_telegram_message(
                chat_id=int(self.chat_id),
                text=text,
                parse_mode="Markdown"
            )
            
            return bool(result)
        
        except Exception as e:
            logger.error(f"Telegram send error: {e}")
            return False
    
    async def send_watchlist_summary(self, items: List[Dict[str, Any]]) -> bool:
        """Send a formatted watchlist summary"""
        if not items:
            return await self.send_message("📋 *Watchlist Empty*\n\nNo tickers currently being watched.")
        
        message = f"📋 *Watchlist* ({len(items)} items)\n\n"
        
        for item in items[:10]:  # Limit to 10 items
            ticker = item.get("ticker", "???")
            status = item.get("status", "Unknown")
            reason = item.get("reason", "")
            
            status_emoji = {
                "Watching": "👁",
                "Breaking Out": "🚀",
                "Triggered": "✅",
                "Completed": "✓",
            }.get(status, "•")
            
            message += f"{status_emoji} *{ticker}*"
            if reason:
                message += f" - {reason[:30]}"
            message += f"\n  Status: {status}\n"
        
        if len(items) > 10:
            message += f"\n_...and {len(items) - 10} more_"
        
        return await self.send_message(message)

# Singleton instance
_bot = None

def get_telegram_bot() -> TelegramBot:
    """Get singleton Telegram bot instance"""
    global _bot
    if _bot is None:
        _bot = TelegramBot()
    return _bot

