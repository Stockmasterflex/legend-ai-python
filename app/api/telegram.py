from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from typing import Optional
import re
import httpx
import logging
import json

from app.config import get_settings
from app.services.ai_market_analysis import get_ai_market_analysis_service
from app.services.scheduler import get_scheduler_service

logger = logging.getLogger(__name__)
settings = get_settings()

router = APIRouter()

class TelegramUpdate(BaseModel):
    """Telegram webhook update model"""
    update_id: int
    message: Optional[dict] = None

class CommandRequest(BaseModel):
    """Parsed command request"""
    chat_id: str
    cmd: str
    ticker: str = ""
    original_text: str = ""
    is_natural_language: bool = False

class TelegramService:
    """Service for handling Telegram operations"""

    def __init__(self):
        self.client = httpx.AsyncClient(
            timeout=30.0,
            follow_redirects=True,
            verify=True
        )
        self.ai_service = get_ai_market_analysis_service()
        self.default_chat_id = settings.telegram_chat_id  # For scheduled messages

    async def send_message(self, chat_id: str, text: str, parse_mode: str = "Markdown") -> bool:
        """Send message to Telegram chat"""
        try:
            url = f"https://api.telegram.org/bot{settings.telegram_bot_token}/sendMessage"
            payload = {
                "chat_id": chat_id,
                "text": text,
                "parse_mode": parse_mode
            }

            response = await self.client.post(url, json=payload)
            response.raise_for_status()

            logger.info(f"Sent message to chat {chat_id}: {text[:50]}...")
            return True

        except Exception as e:
            logger.error(f"Failed to send message to {chat_id}: {e}")
            return False

    async def send_photo(self, chat_id: str, photo_url: str, caption: str = "") -> bool:
        """Send photo to Telegram chat"""
        try:
            url = f"https://api.telegram.org/bot{settings.telegram_bot_token}/sendPhoto"
            payload = {
                "chat_id": chat_id,
                "photo": photo_url,
                "caption": caption,
                "parse_mode": "Markdown"
            }

            response = await self.client.post(url, json=payload)
            response.raise_for_status()

            logger.info(f"Sent photo to chat {chat_id}: {photo_url}")
            return True

        except Exception as e:
            logger.error(f"Failed to send photo to {chat_id}: {e}")
            return False

    async def classify_intent(self, text: str) -> str:
        """Use AI to classify user intent for natural language queries"""
        try:
            # Heuristic shortcuts for common patterns (fast path)
            low = text.lower()
            if any(phrase in low for phrase in ["top setup", "best setup", "today setup", "find pattern", "scan for pattern"]):
                return "scan"

            if any(phrase in low for phrase in ["check", "analyze", "does", "have pattern"]):
                return "pattern"

            if any(phrase in low for phrase in ["show chart", "chart", "graph"]):
                return "chart"

            # Use AI for complex queries
            prompt = f"""You are a stock trading assistant. Classify this user request and respond ONLY with a single word:

User said: "{text}"

Intent types: chart, pattern, scan, help

Response:"""

            response = await self.client.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {settings.openrouter_api_key}",
                    "Content-Type": "application/json",
                    "HTTP-Referer": "https://legend-ai-python-production.up.railway.app",
                    "X-Title": "Legend AI Bot"
                },
                json={
                    "model": "openai/gpt-4o-mini",
                    "messages": [{"role": "user", "content": prompt}],
                    "max_tokens": 10,
                    "temperature": 0
                }
            )

            if response.status_code == 200:
                result = response.json()
                intent = result["choices"][0]["message"]["content"].strip().lower()

                # Validate intent
                if intent in ["chart", "pattern", "scan", "help"]:
                    return intent

            return "help"  # Default fallback

        except Exception as e:
            logger.error(f"AI intent classification failed: {e}")
            return "help"

    def parse_command(self, text: str, chat_id: str) -> CommandRequest:
        """Parse incoming message into command structure (similar to n8n Handle Command)"""
        if not text:
            return CommandRequest(chat_id=chat_id, cmd="/help")

        original_text = text.strip()
        parts = original_text.split()
        cmd = parts[0].lower()

        # Check for natural language patterns
        low = original_text.lower()
        is_natural = any(keyword in low for keyword in [
            "best", "top", "find", "scan", "show", "check", "analyze",
            "chart", "pattern", "setup", "today"
        ])

        # Route natural language to AI intent classifier
        if not cmd.startswith("/") and is_natural:
            cmd = "/ai"
        elif not cmd.startswith("/"):
            cmd = "/" + cmd

        cmd = cmd.split("@")[0]  # Remove bot username if present
        ticker = (parts[1] or "").upper() if len(parts) > 1 else ""

        return CommandRequest(
            chat_id=chat_id,
            cmd=cmd,
            ticker=ticker,
            original_text=original_text,
            is_natural_language=is_natural
        )

    async def handle_start_command(self, chat_id: str) -> str:
        """Handle /start command"""
        return """🤖 *Legend Trading AI*

AI-powered market analysis with multi-model intelligence!

💬 *Natural Language:*
Just ask: "Find bullish setups in tech sector"

🤖 *AI Commands:*
/brief - Daily market brief
/analyze TICKER - Deep AI analysis
/ask QUERY - Ask anything about markets
/news TICKER - News sentiment
/sentiment - Market sentiment

📊 *Classic Commands:*
/pattern TICKER - Pattern detection
/chart TICKER - Generate chart
/scan - Quick pattern scan
/help - Show this message"""

    async def handle_help_command(self, chat_id: str) -> str:
        """Handle /help command"""
        return await self.handle_start_command(chat_id)

    async def handle_pattern_command(self, chat_id: str, ticker: str) -> str:
        """Handle /pattern command - single ticker analysis"""
        if not ticker:
            return "❌ Usage: /pattern TICKER\n\nExample: /pattern NVDA"

        try:
            # Call pattern detection endpoint using internal service
            base_url = settings.telegram_webhook_url or "http://localhost:8000"
            response = await self.client.post(
                f"{base_url}/api/patterns/detect",
                json={"ticker": ticker, "interval": "1day"}
            )

            if response.status_code == 200:
                result = response.json()
                if result.get("success"):
                    data = result["data"]
                    pattern = data.get("pattern", "NONE")
                    score = data.get("score", 0)
                    entry = data.get("entry", 0)
                    stop = data.get("stop", 0)
                    target = data.get("target", 0)
                    risk_reward = data.get("risk_reward", 0)
                    criteria = data.get("criteria_met", [])

                    if pattern != "NONE" and score >= 7:
                        criteria_text = "\n".join(f"✅ {c}" for c in criteria[:3])  # Show top 3
                        return f"""📊 *{ticker} Pattern Analysis*

🎯 *Pattern:* {pattern}
⭐ *Score:* {score}/10
💰 *Entry:* ${entry:.2f}
🛑 *Stop:* ${stop:.2f}
🎯 *Target:* ${target:.2f}
📈 *Risk/Reward:* {risk_reward:.1f}

{criteria_text}

✅ Strong setup detected!"""
                    else:
                        return f"""📊 *{ticker} Pattern Analysis*

🎯 *Pattern:* {pattern}
⭐ *Score:* {score}/10

⚠️ No strong patterns found."""
                else:
                    return f"❌ Pattern analysis failed: {result.get('error', 'Unknown error')}"
            else:
                return f"❌ Service error ({response.status_code})"

        except Exception as e:
            logger.error(f"Pattern analysis error: {e}")
            return f"❌ Analysis failed: {str(e)}"

    async def handle_chart_command(self, chat_id: str, ticker: str) -> dict:
        """Handle /chart command - generate chart"""
        if not ticker:
            return {"text": "❌ Usage: /chart TICKER\n\nExample: /chart AAPL", "chart_url": None}

        try:
            # Call chart generation endpoint using internal service
            base_url = settings.telegram_webhook_url or "http://localhost:8000"
            response = await self.client.post(
                f"{base_url}/api/charts/generate",
                json={"ticker": ticker, "interval": "1D"}
            )

            if response.status_code == 200:
                result = response.json()
                if result.get("success") and result.get("chart_url"):
                    chart_url = result["chart_url"]
                    caption = f"📊 {ticker} Chart"

                    # Send photo directly
                    photo_success = await self.send_photo(chat_id, chart_url, caption)

                    if photo_success:
                        return {"text": "", "chart_url": chart_url}  # Photo sent, no text needed
                    else:
                        return {
                            "text": f"❌ Chart generated but failed to send photo.\n\nChart URL: {chart_url}",
                            "chart_url": chart_url
                        }
                else:
                    return {
                        "text": f"❌ Chart generation failed: {result.get('error', 'Unknown error')}",
                        "chart_url": None
                    }
            else:
                return {
                    "text": f"❌ Service error ({response.status_code})",
                    "chart_url": None
                }

        except Exception as e:
            logger.error(f"Chart generation error: {e}")
            return {
                "text": f"❌ Chart failed: {str(e)}",
                "chart_url": None
            }

    async def handle_scan_command(self, chat_id: str, pattern: str = "VCP", min_score: int = 8) -> str:
        """Handle /scan command - scan universe for patterns"""
        try:
            base_url = settings.telegram_webhook_url or "http://localhost:8000"
            response = await self.client.post(
                f"{base_url}/api/universe/scan/quick",
                timeout=10.0
            )
            if response.status_code == 200:
                data = response.json()
                if data.get("success") and data.get("results"):
                    results = data["results"][:5]
                    msg = "🔍 *Quick Scan Results*\n\n"
                    for r in results:
                        msg += f"📊 *{r['ticker']}* - {r['pattern']} ({r['score']}/10)\n"
                        msg += f"   Entry: ${r['entry']:.2f} | Stop: ${r['stop']:.2f}\n\n"
                    return msg
            return "🔍 *Scanning Universe*\n\nUse /scan for quick results from cached data!"
        except Exception as e:
            logger.warning(f"Error generating scan summary: {e}")
            return "🔍 Scanner ready! Checking top stocks..."

    async def handle_ai_intent(self, chat_id: str, original_text: str) -> str:
        """Handle natural language queries using AI intent classification"""
        intent = await self.classify_intent(original_text)

        if intent == "scan":
            return await self.handle_scan_command(chat_id, "VCP", 8)
        elif intent == "pattern":
            # Extract potential ticker from text
            ticker = self._extract_ticker_from_text(original_text)
            return await self.handle_pattern_command(chat_id, ticker)
        elif intent == "chart":
            # Extract potential ticker from text
            ticker = self._extract_ticker_from_text(original_text)
            result = await self.handle_chart_command(chat_id, ticker)
            return result.get("text", "Chart command processed")
        else:
            return await self.handle_help_command(chat_id)

    async def handle_brief_command(self, chat_id: str) -> str:
        """Handle /brief - Get daily market brief"""
        try:
            # Check if there's a recent brief in database
            from app.services.database import get_database_service
            from app.models import MarketBrief
            from datetime import datetime, timedelta

            db = get_database_service()
            with db.get_session() as session:
                # Get today's brief or most recent
                today = datetime.now().date()
                recent_brief = session.query(MarketBrief).filter(
                    MarketBrief.brief_date >= datetime.combine(today, datetime.min.time())
                ).order_by(MarketBrief.generated_at.desc()).first()

                if recent_brief:
                    # Use existing brief
                    scheduler = get_scheduler_service()
                    brief_data = {
                        "market_summary": recent_brief.market_summary,
                        "sentiment": recent_brief.market_sentiment,
                        "sentiment_score": recent_brief.sentiment_score,
                        "trade_ideas": json.loads(recent_brief.trade_ideas) if recent_brief.trade_ideas else [],
                        "pattern_highlights": json.loads(recent_brief.pattern_highlights) if recent_brief.pattern_highlights else [],
                        "risk_factors": json.loads(recent_brief.risk_factors) if recent_brief.risk_factors else []
                    }
                    return scheduler._format_brief_for_telegram(brief_data)

            # Generate new brief
            brief = await self.ai_service.generate_daily_brief()
            scheduler = get_scheduler_service()
            return scheduler._format_brief_for_telegram(brief)

        except Exception as e:
            logger.error(f"Error getting market brief: {e}")
            return "❌ Failed to generate market brief. Please try again."

    async def handle_analyze_command(self, chat_id: str, ticker: str) -> str:
        """Handle /analyze - Deep AI analysis with chart vision"""
        if not ticker:
            return "❌ Usage: /analyze TICKER\n\nExample: /analyze NVDA"

        try:
            # First generate chart
            base_url = settings.telegram_webhook_url or "http://localhost:8000"
            chart_response = await self.client.post(
                f"{base_url}/api/charts/generate",
                json={"ticker": ticker, "interval": "1D"}
            )

            chart_url = None
            if chart_response.status_code == 200:
                result = chart_response.json()
                if result.get("success") and result.get("chart_url"):
                    chart_url = result["chart_url"]

            # Perform AI analysis with vision
            if chart_url and settings.enable_chart_analysis:
                analysis = await self.ai_service.analyze_chart(ticker, chart_url, use_vision=True)

                # Format response
                message = f"🤖 **AI Analysis: {ticker}**\n\n"
                message += f"**Trend:** {analysis.get('trend_direction', 'neutral').upper()}\n"
                if analysis.get('trend_strength'):
                    message += f"**Strength:** {analysis.get('trend_strength')}/10\n"

                if analysis.get('support_levels'):
                    supports = ', '.join([f"${s:.2f}" for s in analysis['support_levels'][:3]])
                    message += f"**Support:** {supports}\n"

                if analysis.get('resistance_levels'):
                    resistances = ', '.join([f"${r:.2f}" for r in analysis['resistance_levels'][:3]])
                    message += f"**Resistance:** {resistances}\n"

                message += f"\n**Analysis:**\n{analysis.get('summary', 'No summary available')[:500]}\n"

                if analysis.get('trade_ideas'):
                    message += f"\n**💡 Trade Ideas:**\n"
                    for idea in analysis['trade_ideas'][:2]:
                        message += f"Entry: ${idea.get('entry', 0):.2f} | "
                        message += f"Stop: ${idea.get('stop', 0):.2f} | "
                        message += f"Target: ${idea.get('target', 0):.2f}\n"
                        message += f"_{idea.get('reasoning', '')[:100]}_\n"

                # Send chart
                if chart_url:
                    await self.send_photo(chat_id, chart_url, f"Chart for {ticker}")

                return message
            else:
                return f"❌ Unable to analyze {ticker}. Chart generation failed."

        except Exception as e:
            logger.error(f"Error in analyze command: {e}")
            return f"❌ Analysis failed: {str(e)}"

    async def handle_news_command(self, chat_id: str, ticker: Optional[str] = None) -> str:
        """Handle /news - News sentiment analysis"""
        try:
            # Scrape recent news
            await self.ai_service.scrape_news(ticker=ticker, limit=10)

            # Analyze sentiment
            sentiment = await self.ai_service.analyze_news_sentiment(ticker=ticker, max_articles=10)

            subject = ticker or "Market"
            message = f"📰 **News Sentiment: {subject}**\n\n"

            sentiment_emoji = {
                'bullish': '🟢',
                'bearish': '🔴',
                'neutral': '⚪'
            }.get(sentiment.get('sentiment', 'neutral'), '⚪')

            message += f"**Overall:** {sentiment_emoji} {sentiment.get('sentiment', 'neutral').upper()}\n"
            message += f"**Score:** {sentiment.get('score', 0):.2f}\n"
            message += f"**Articles Analyzed:** {sentiment.get('articles_analyzed', 0)}\n\n"

            # Show key points from detailed sentiments
            if sentiment.get('detailed_sentiments'):
                message += "**Key Insights:**\n"
                for i, detail in enumerate(sentiment['detailed_sentiments'][:3], 1):
                    key_points = detail.get('key_points', [])
                    if key_points:
                        message += f"{i}. {key_points[0]}\n"

            return message

        except Exception as e:
            logger.error(f"Error in news command: {e}")
            return "❌ Failed to analyze news sentiment. Please try again."

    async def handle_sentiment_command(self, chat_id: str) -> str:
        """Handle /sentiment - Overall market sentiment"""
        try:
            # Get general market sentiment
            sentiment = await self.ai_service.analyze_news_sentiment(ticker=None, max_articles=20)

            message = "📊 **Market Sentiment Overview**\n\n"

            sentiment_emoji = {
                'bullish': '🟢',
                'bearish': '🔴',
                'neutral': '⚪'
            }.get(sentiment.get('sentiment', 'neutral'), '⚪')

            message += f"**Sentiment:** {sentiment_emoji} {sentiment.get('sentiment', 'neutral').upper()}\n"
            message += f"**Score:** {sentiment.get('score', 0):.2f} (-1 to +1)\n"
            message += f"**Based on {sentiment.get('articles_analyzed', 0)} recent articles**\n\n"

            # Interpretation
            score = sentiment.get('score', 0)
            if score > 0.5:
                message += "📈 Strong bullish sentiment in the market"
            elif score > 0.2:
                message += "📊 Moderately bullish sentiment"
            elif score < -0.5:
                message += "📉 Strong bearish sentiment in the market"
            elif score < -0.2:
                message += "📊 Moderately bearish sentiment"
            else:
                message += "⚖️ Neutral market sentiment"

            return message

        except Exception as e:
            logger.error(f"Error in sentiment command: {e}")
            return "❌ Failed to get market sentiment. Please try again."

    async def handle_ask_command(self, chat_id: str, query: str) -> str:
        """Handle /ask - Natural language queries with full AI"""
        if not query:
            return "❌ Usage: /ask YOUR QUESTION\n\nExamples:\n• /ask Find bullish setups in tech\n• /ask What stocks are breaking out?\n• /ask Market sentiment today?"

        try:
            # Process natural language query
            result = await self.ai_service.process_natural_language_query(
                query=query,
                user_id=chat_id
            )

            return result.get('response', 'No response generated')

        except Exception as e:
            logger.error(f"Error in ask command: {e}")
            return f"❌ Query failed: {str(e)}"

    def _extract_ticker_from_text(self, text: str) -> str:
        """Extract ticker symbol from natural language text"""
        # Simple regex to find potential tickers (3-5 uppercase letters)
        matches = re.findall(r'\b[A-Z]{2,5}\b', text.upper())
        # Filter out common words that might match
        common_words = {"FOR", "THE", "AND", "ARE", "BUT", "CAN", "DID", "HAS", "HAD", "HER", "HIS", "ITS", "OUR", "THEIR", "WAS", "WILL", "YOU"}
        tickers = [m for m in matches if m not in common_words and len(m) >= 2]
        return tickers[0] if tickers else ""

# Global service instance
telegram_service = TelegramService()

@router.post("/webhook/telegram")
async def telegram_webhook(request: Request):
    """Telegram webhook endpoint"""
    try:
        # Get raw JSON
        data = await request.json()

        # Parse update
        update = TelegramUpdate(**data)

        if not update.message:
            # Not a message update, ignore
            return {"status": "ignored"}

        message = update.message
        chat_id = str(message.get("chat", {}).get("id", ""))
        text = message.get("text", "").strip()

        if not chat_id or not text:
            return {"status": "invalid"}

        logger.info(f"Received message from {chat_id}: {text[:50]}...")

        # Parse command
        cmd_request = telegram_service.parse_command(text, chat_id)

        # Route to appropriate handler
        response_text = ""

        if cmd_request.cmd == "/start":
            response_text = await telegram_service.handle_start_command(chat_id)
        elif cmd_request.cmd in ["/help", "/"]:
            response_text = await telegram_service.handle_help_command(chat_id)
        elif cmd_request.cmd == "/pattern":
            response_text = await telegram_service.handle_pattern_command(chat_id, cmd_request.ticker)
        elif cmd_request.cmd == "/chart":
            result = await telegram_service.handle_chart_command(chat_id, cmd_request.ticker)
            response_text = result.get("text", "")
            # Chart photo is already sent within handle_chart_command
        elif cmd_request.cmd == "/scan":
            response_text = await telegram_service.handle_scan_command(chat_id)
        elif cmd_request.cmd == "/brief":
            response_text = await telegram_service.handle_brief_command(chat_id)
        elif cmd_request.cmd == "/analyze":
            response_text = await telegram_service.handle_analyze_command(chat_id, cmd_request.ticker)
        elif cmd_request.cmd == "/news":
            response_text = await telegram_service.handle_news_command(chat_id, cmd_request.ticker or None)
        elif cmd_request.cmd == "/sentiment":
            response_text = await telegram_service.handle_sentiment_command(chat_id)
        elif cmd_request.cmd == "/ask":
            # Extract query (everything after /ask)
            query = cmd_request.original_text.replace("/ask", "").strip()
            response_text = await telegram_service.handle_ask_command(chat_id, query)
        elif cmd_request.cmd == "/ai":
            response_text = await telegram_service.handle_ai_intent(chat_id, cmd_request.original_text)
        else:
            response_text = "❓ Unknown command. Try /help for available commands."

        # Send response
        if response_text:
            success = await telegram_service.send_message(chat_id, response_text)
            if not success:
                logger.error(f"Failed to send response to {chat_id}")

        return {"status": "ok"}

    except Exception as e:
        logger.error(f"Error processing Telegram webhook: {e}")
        raise HTTPException(status_code=500, detail=str(e))
