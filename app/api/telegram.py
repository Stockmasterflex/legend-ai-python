from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from typing import Optional
import re
import httpx
import logging

from app.config import get_settings

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

Now with AI-powered natural language! Just talk to me:

💬 *Natural Language Examples:*
• "Find VCP patterns"
• "Show me NVDA chart"
• "Check TSLA for patterns"
• "Scan for bases"

📊 *Or use slash commands:*
/pattern TICKER - Analyze patterns
/chart TICKER - Generate chart
/scan - Today's best setups
/help - Show this message

I understand both!"""

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
