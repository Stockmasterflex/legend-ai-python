"""
Enhanced Telegram Bot Service
Handles all bot commands and natural language queries
"""
from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from typing import Optional, Dict, Any
import httpx
import logging
import json

from app.config import get_settings
from app.services.market_data import market_data_service
from app.core.pattern_detector import PatternDetector

logger = logging.getLogger(__name__)
settings = get_settings()

router = APIRouter(tags=["telegram"])


class TelegramUpdate(BaseModel):
    """Telegram webhook update"""
    update_id: int
    message: Optional[dict] = None


class TelegramService:
    """Telegram bot service"""

    def __init__(self):
        self.client = httpx.AsyncClient(timeout=30.0)
        self.base_url = f"https://api.telegram.org/bot{settings.telegram_bot_token}"

    async def send_message(self, chat_id: str, text: str, parse_mode: str = "Markdown") -> bool:
        """Send text message"""
        try:
            response = await self.client.post(
                f"{self.base_url}/sendMessage",
                json={
                    "chat_id": chat_id,
                    "text": text,
                    "parse_mode": parse_mode
                }
            )
            response.raise_for_status()
            logger.info(f"✅ Sent message to {chat_id}")
            return True
        except Exception as e:
            logger.error(f"❌ Failed to send message: {e}")
            return False

    async def send_photo(self, chat_id: str, photo_url: str, caption: str = "") -> bool:
        """Send photo"""
        try:
            response = await self.client.post(
                f"{self.base_url}/sendPhoto",
                json={
                    "chat_id": chat_id,
                    "photo": photo_url,
                    "caption": caption,
                    "parse_mode": "Markdown"
                }
            )
            response.raise_for_status()
            logger.info(f"✅ Sent photo to {chat_id}")
            return True
        except Exception as e:
            logger.error(f"❌ Failed to send photo: {e}")
            return False

    async def handle_start(self, chat_id: str) -> str:
        """Handle /start command"""
        return f"""🚀 *Welcome to Legend AI Trading Bot!*

I'm your professional trading assistant powered by AI and multi-source market data.

*📊 Available Commands:*

/pattern TICKER - Analyze pattern setup
_Example: /pattern NVDA_

/scan - Quick scan for top setups
_Scans 30 high-growth stocks_

/chart TICKER - Get annotated chart
_Example: /chart AAPL_

/watchlist - View your watchlist
/add TICKER - Add to watchlist
_Example: /add TSLA_

/remove TICKER - Remove from watchlist
/plan TICKER - Get trading plan
_Example: /plan NVDA_

/market - Market internals
/usage - API usage stats
/help - Show this message

*💡 Natural Language:*
You can also just ask me things like:
- "What are the best setups today?"
- "Analyze Tesla for me"
- "Show me NVIDIA chart"

*Let's find some winning trades!* 📈
"""

    async def handle_help(self, chat_id: str) -> str:
        """Handle /help command"""
        return await self.handle_start(chat_id)

    async def handle_pattern(self, chat_id: str, ticker: str) -> str:
        """Handle /pattern command"""
        if not ticker:
            return "❌ Please provide a ticker symbol.\n\n*Usage:* `/pattern NVDA`"

        ticker = ticker.upper().strip()

        try:
            # Send typing indicator
            await self.client.post(
                f"{self.base_url}/sendChatAction",
                json={"chat_id": chat_id, "action": "typing"}
            )

            # Get pattern data
            from app.services.market_data import market_data_service
            from app.core.pattern_detector import PatternDetector

            price_data = await market_data_service.get_time_series(ticker, "1day", 500)

            if not price_data:
                return f"❌ Could not fetch data for {ticker}. Please check the ticker symbol."

            spy_data = await market_data_service.get_time_series("SPY", "1day", 500)

            detector = PatternDetector()
            result = await detector.analyze_ticker(ticker, price_data, spy_data)

            if not result:
                return f"❌ Could not analyze {ticker}"

            # Format response
            score_emoji = "🔥" if result.score >= 8 else "⭐" if result.score >= 7 else "📊"

            response = f"""{score_emoji} *{ticker} Pattern Analysis*

*Pattern:* {result.pattern}
*Score:* {result.score}/10

*💰 Trading Levels:*
Entry: ${result.entry:.2f}
Stop: ${result.stop:.2f}
Target: ${result.target:.2f}
R:R Ratio: {result.risk_reward:.2f}:1

*📈 Technical:*
Current: ${result.current_price:.2f}
RS Rating: {result.rs_rating:.0f}

*Data Source:* {price_data.get('source', 'unknown')}
*Cached:* {'Yes' if price_data.get('cached') else 'No'}
"""

            if result.score >= 8:
                response += "\n🚀 *Strong setup! Consider this carefully.*"
            elif result.score >= 7:
                response += "\n✅ *Good setup worth monitoring.*"

            return response

        except Exception as e:
            logger.error(f"Error in handle_pattern: {e}")
            return f"❌ Error analyzing {ticker}: {str(e)}"

    async def handle_scan(self, chat_id: str) -> str:
        """Handle /scan command - quick universe scan"""
        try:
            await self.client.post(
                f"{self.base_url}/sendChatAction",
                json={"chat_id": chat_id, "action": "typing"}
            )

            # Quick scan of top stocks
            from app.services.universe_data import get_quick_scan_universe
            from app.core.pattern_detector import PatternDetector

            tickers = get_quick_scan_universe()
            detector = PatternDetector()
            results = []

            await self.send_message(chat_id, f"🔍 Scanning {len(tickers)} stocks... (this may take 30-60s)")

            for ticker in tickers[:30]:  # Limit to 30 for speed
                try:
                    price_data = await market_data_service.get_time_series(ticker, "1day", 500)
                    if not price_data:
                        continue

                    spy_data = await market_data_service.get_time_series("SPY", "1day", 500)
                    result = await detector.analyze_ticker(ticker, price_data, spy_data)

                    if result and result.score >= 7.0:
                        results.append({
                            "ticker": ticker,
                            "pattern": result.pattern,
                            "score": result.score,
                            "entry": result.entry,
                            "rr": result.risk_reward
                        })
                except Exception as e:
                    logger.debug(f"Scan error for {ticker}: {e}")
                    continue

            # Sort by score
            results.sort(key=lambda x: x["score"], reverse=True)

            if not results:
                return "📊 No strong setups found in quick scan. Try again later!"

            response = f"🔍 *Top Setups Found ({len(results)})*\n\n"

            for i, r in enumerate(results[:10], 1):
                emoji = "🔥" if r["score"] >= 8 else "⭐"
                response += f"{emoji} *{r['ticker']}* - {r['pattern']}\n"
                response += f"   Score: {r['score']}/10 | Entry: ${r['entry']:.2f} | R:R: {r['rr']:.2f}:1\n\n"

            response += f"\n_Scanned {len(tickers)} stocks. Use /pattern TICKER for details._"

            return response

        except Exception as e:
            logger.error(f"Error in handle_scan: {e}")
            return f"❌ Scan error: {str(e)}"

    async def handle_chart(self, chat_id: str, ticker: str) -> tuple[str, str]:
        """Handle /chart command - returns (message, photo_url)"""
        if not ticker:
            return ("❌ Please provide a ticker symbol.\n\n*Usage:* `/chart NVDA`", None)

        ticker = ticker.upper().strip()

        try:
            # Generate chart
            from app.core.chart_generator import ChartGenerator

            generator = ChartGenerator()
            chart_url = await generator.generate_chart(
                ticker=ticker,
                interval="1D",
                indicators=["SMA(50)", "SMA(150)", "SMA(200)", "Volume"],
                timeframe="6M"
            )

            if not chart_url:
                return (f"❌ Could not generate chart for {ticker}", None)

            caption = f"📊 *{ticker} Chart*\n\n_6-month daily chart with key moving averages_"
            return (caption, chart_url)

        except Exception as e:
            logger.error(f"Error in handle_chart: {e}")
            return (f"❌ Chart error: {str(e)}", None)

    async def handle_watchlist(self, chat_id: str) -> str:
        """Handle /watchlist command"""
        try:
            # Get watchlist from API
            response = await self.client.get(f"{settings.auto_webhook_url}/api/watchlist")
            data = response.json()

            if not data.get("success") or not data.get("items"):
                return "📝 *Your Watchlist is Empty*\n\nAdd stocks with: `/add TICKER`"

            items = data["items"]
            message = f"📋 *Your Watchlist ({len(items)} stocks)*\n\n"

            for item in items:
                message += f"• *{item['ticker']}* - {item.get('reason', 'N/A')}\n"
                message += f"  _Added: {item.get('added_date', 'Unknown')[:10]}_\n\n"

            message += "\n_Use /remove TICKER to remove stocks_"

            return message

        except Exception as e:
            logger.error(f"Error in handle_watchlist: {e}")
            return f"❌ Error: {str(e)}"

    async def handle_add(self, chat_id: str, ticker: str, reason: str = "") -> str:
        """Handle /add command"""
        if not ticker:
            return "❌ Please provide a ticker symbol.\n\n*Usage:* `/add NVDA VCP breakout setup`"

        ticker = ticker.upper().strip()

        try:
            response = await self.client.post(
                f"{settings.auto_webhook_url}/api/watchlist/add",
                json={"ticker": ticker, "reason": reason or "Monitoring"}
            )
            data = response.json()

            if data.get("success"):
                return f"✅ Added *{ticker}* to watchlist!\n\n_Reason: {reason or 'Monitoring'}_"
            else:
                return f"❌ Failed to add {ticker}: {data.get('detail', 'Unknown error')}"

        except Exception as e:
            logger.error(f"Error in handle_add: {e}")
            return f"❌ Error: {str(e)}"

    async def handle_remove(self, chat_id: str, ticker: str) -> str:
        """Handle /remove command"""
        if not ticker:
            return "❌ Please provide a ticker symbol.\n\n*Usage:* `/remove NVDA`"

        ticker = ticker.upper().strip()

        try:
            response = await self.client.delete(
                f"{settings.auto_webhook_url}/api/watchlist/{ticker}"
            )
            data = response.json()

            if data.get("success"):
                return f"✅ Removed *{ticker}* from watchlist"
            else:
                return f"❌ Failed to remove {ticker}: {data.get('detail', 'Unknown error')}"

        except Exception as e:
            logger.error(f"Error in handle_remove: {e}")
            return f"❌ Error: {str(e)}"

    async def handle_plan(self, chat_id: str, ticker: str) -> str:
        """Handle /plan command - trading plan"""
        if not ticker:
            return "❌ Please provide a ticker symbol.\n\n*Usage:* `/plan NVDA`"

        ticker = ticker.upper().strip()

        try:
            # Get pattern first
            price_data = await market_data_service.get_time_series(ticker, "1day", 500)
            if not price_data:
                return f"❌ Could not fetch data for {ticker}"

            spy_data = await market_data_service.get_time_series("SPY", "1day", 500)

            detector = PatternDetector()
            result = await detector.analyze_ticker(ticker, price_data, spy_data)

            if not result:
                return f"❌ Could not analyze {ticker}"

            # Create trading plan
            account_size = 10000  # Default
            risk_percent = 2.0

            risk_amount = account_size * (risk_percent / 100)
            stop_distance = result.entry - result.stop
            shares = int(risk_amount / stop_distance) if stop_distance > 0 else 0
            position_value = shares * result.entry

            response = f"""💼 *Trading Plan: {ticker}*

*Pattern:* {result.pattern} ({result.score}/10)

*Entry & Exit Levels:*
Entry: ${result.entry:.2f}
Stop: ${result.stop:.2f}
Target: ${result.target:.2f}

*Position Sizing:*
Shares: {shares}
Position Value: ${position_value:,.2f}
Risk Amount: ${risk_amount:.2f} ({risk_percent}%)

*Risk/Reward:*
R:R Ratio: {result.risk_reward:.2f}:1
Potential Profit: ${(result.target - result.entry) * shares:.2f}
Potential Loss: ${risk_amount:.2f}

*Account:* ${account_size:,.2f}
*Risk per Trade:* {risk_percent}%

_Adjust position size based on your account and risk tolerance._
"""

            return response

        except Exception as e:
            logger.error(f"Error in handle_plan: {e}")
            return f"❌ Error: {str(e)}"

    async def handle_market(self, chat_id: str) -> str:
        """Handle /market command - market internals"""
        try:
            # Get SPY data
            spy_data = await market_data_service.get_time_series("SPY", "1day", 200)

            if not spy_data or not spy_data.get("c"):
                return "❌ Could not fetch market data"

            current_price = spy_data["c"][-1]
            sma_50 = sum(spy_data["c"][-50:]) / 50
            sma_200 = sum(spy_data["c"][-200:]) / 200

            # Determine market regime
            if current_price > sma_50 > sma_200:
                regime = "🟢 UPTREND"
                status = "Bullish"
            elif current_price > sma_200:
                regime = "🟡 CONSOLIDATION"
                status = "Neutral"
            else:
                regime = "🔴 DOWNTREND"
                status = "Bearish"

            response = f"""📈 *Market Internals*

*S&P 500 (SPY):* ${current_price:.2f}

*Moving Averages:*
50 SMA: ${sma_50:.2f}
200 SMA: ${sma_200:.2f}

*Market Regime:* {regime}
*Status:* {status}

*Data Source:* {spy_data.get('source', 'unknown')}
_Updated: {spy_data.get('t', [])[-1][:10] if spy_data.get('t') else 'Unknown'}_
"""

            return response

        except Exception as e:
            logger.error(f"Error in handle_market: {e}")
            return f"❌ Error: {str(e)}"

    async def handle_usage(self, chat_id: str) -> str:
        """Handle /usage command - API usage stats"""
        try:
            stats = await market_data_service.get_usage_stats()

            response = f"""📊 *API Usage Statistics*

*TwelveData:*
Used: {stats['twelvedata']['used']}/{stats['twelvedata']['limit']}
Remaining: {stats['twelvedata']['remaining']}
Usage: {stats['twelvedata']['percent']:.1f}%

*Finnhub:*
Used: {stats['finnhub']['used']}/{stats['finnhub']['limit']}
Remaining: {stats['finnhub']['remaining']}
Usage: {stats['finnhub']['percent']:.1f}%

*Alpha Vantage:*
Used: {stats['alphavantage']['used']}/{stats['alphavantage']['limit']}
Remaining: {stats['alphavantage']['remaining']}
Usage: {stats['alphavantage']['percent']:.1f}%

_Usage resets daily at midnight UTC_
"""

            return response

        except Exception as e:
            logger.error(f"Error in handle_usage: {e}")
            return f"❌ Error: {str(e)}"

    async def handle_natural_language(self, chat_id: str, text: str) -> str:
        """Handle natural language queries"""
        text_lower = text.lower()

        # Extract ticker symbols from text (3-5 uppercase letters)
        import re
        ticker_pattern = r'\b[A-Z]{2,5}\b'
        tickers = re.findall(ticker_pattern, text)
        ticker = tickers[0] if tickers else None

        # Intent detection based on keywords
        scan_keywords = ["scan", "best setups", "top stocks", "find", "search", "what's good"]
        pattern_keywords = ["analyze", "analysis", "pattern", "check", "look at", "review"]
        chart_keywords = ["chart", "graph", "show me"]
        market_keywords = ["market", "spy", "indices", "how is the market"]
        plan_keywords = ["trading plan", "position size", "how much", "trade"]

        # Check intents
        if any(kw in text_lower for kw in scan_keywords):
            return await self.handle_scan(chat_id)

        elif any(kw in text_lower for kw in chart_keywords) and ticker:
            caption, photo_url = await self.handle_chart(chat_id, ticker)
            if photo_url:
                await self.send_photo(chat_id, photo_url, caption)
                return ""
            return caption

        elif any(kw in text_lower for kw in pattern_keywords) and ticker:
            return await self.handle_pattern(chat_id, ticker)

        elif any(kw in text_lower for kw in plan_keywords) and ticker:
            return await self.handle_plan(chat_id, ticker)

        elif any(kw in text_lower for kw in market_keywords):
            return await self.handle_market(chat_id)

        # If ticker found but no clear intent, default to pattern analysis
        elif ticker:
            return await self.handle_pattern(chat_id, ticker)

        # No clear intent
        else:
            return """💡 *I can help you with:*

• "Scan for best setups"
• "Analyze NVDA"
• "Show me TSLA chart"
• "Trading plan for AAPL"
• "How is the market?"

Or use commands like /pattern, /scan, /chart, etc.
Type /help for full command list."""


# Global service instance
telegram_service = TelegramService()


@router.post("/webhook/telegram")
async def telegram_webhook(update: TelegramUpdate):
    """Handle incoming Telegram webhook updates"""
    try:
        if not update.message:
            return {"ok": True}

        message = update.message
        chat_id = str(message.get("chat", {}).get("id"))
        text = message.get("text", "").strip()

        if not text:
            return {"ok": True}

        logger.info(f"📱 Received from {chat_id}: {text}")

        # Parse command
        parts = text.split(maxsplit=2)
        cmd = parts[0].lower() if parts else ""
        ticker = parts[1] if len(parts) > 1 else ""
        reason = parts[2] if len(parts) > 2 else ""

        # Handle commands
        if cmd == "/start":
            response = await telegram_service.handle_start(chat_id)
            await telegram_service.send_message(chat_id, response)

        elif cmd == "/help":
            response = await telegram_service.handle_help(chat_id)
            await telegram_service.send_message(chat_id, response)

        elif cmd == "/pattern":
            response = await telegram_service.handle_pattern(chat_id, ticker)
            await telegram_service.send_message(chat_id, response)

        elif cmd == "/scan":
            response = await telegram_service.handle_scan(chat_id)
            await telegram_service.send_message(chat_id, response)

        elif cmd == "/chart":
            caption, photo_url = await telegram_service.handle_chart(chat_id, ticker)
            if photo_url:
                await telegram_service.send_photo(chat_id, photo_url, caption)
            else:
                await telegram_service.send_message(chat_id, caption)

        elif cmd == "/watchlist":
            response = await telegram_service.handle_watchlist(chat_id)
            await telegram_service.send_message(chat_id, response)

        elif cmd == "/add":
            response = await telegram_service.handle_add(chat_id, ticker, reason)
            await telegram_service.send_message(chat_id, response)

        elif cmd == "/remove":
            response = await telegram_service.handle_remove(chat_id, ticker)
            await telegram_service.send_message(chat_id, response)

        elif cmd == "/plan":
            response = await telegram_service.handle_plan(chat_id, ticker)
            await telegram_service.send_message(chat_id, response)

        elif cmd == "/market":
            response = await telegram_service.handle_market(chat_id)
            await telegram_service.send_message(chat_id, response)

        elif cmd == "/usage":
            response = await telegram_service.handle_usage(chat_id)
            await telegram_service.send_message(chat_id, response)

        elif cmd.startswith("/"):
            # Unknown command
            response = "❌ Unknown command. Use /help to see available commands."
            await telegram_service.send_message(chat_id, response)

        else:
            # Handle natural language
            response = await telegram_service.handle_natural_language(chat_id, text)
            if response:  # Only send if not empty (chart already sent photo)
                await telegram_service.send_message(chat_id, response)

        return {"ok": True}

    except Exception as e:
        logger.error(f"Telegram webhook error: {e}")
        return {"ok": False, "error": str(e)}
