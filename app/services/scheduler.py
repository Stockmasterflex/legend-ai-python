"""
Scheduler Service for Automated Market Analysis Tasks
Handles daily briefs, news scraping, and automated alerts
"""

import logging
from datetime import datetime, time
from typing import Optional
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
import pytz

from app.config import get_settings
from app.services.ai_market_analysis import get_ai_market_analysis_service

logger = logging.getLogger(__name__)


class MarketSchedulerService:
    """Scheduler for automated market analysis tasks"""

    def __init__(self):
        self.settings = get_settings()
        self.scheduler = AsyncIOScheduler(timezone=pytz.timezone('US/Eastern'))
        self.ai_service = get_ai_market_analysis_service()
        self.telegram_service = None  # Will be set externally
        self._started = False

    def set_telegram_service(self, telegram_service):
        """Set Telegram service for sending notifications"""
        self.telegram_service = telegram_service

    async def start(self):
        """Start all scheduled tasks"""
        if self._started:
            logger.warning("Scheduler already started")
            return

        logger.info("Starting market scheduler service")

        # Daily market brief at 9:30 AM ET
        if self.settings.enable_daily_brief:
            brief_time = self.settings.daily_brief_time.split(":")
            self.scheduler.add_job(
                self._send_daily_brief,
                CronTrigger(
                    hour=int(brief_time[0]),
                    minute=int(brief_time[1]),
                    timezone=pytz.timezone('US/Eastern')
                ),
                id="daily_market_brief",
                name="Daily Market Brief",
                replace_existing=True
            )
            logger.info(f"Scheduled daily brief at {self.settings.daily_brief_time} ET")

        # News scraping every 30 minutes (configurable)
        if self.settings.enable_news_sentiment:
            self.scheduler.add_job(
                self._scrape_and_analyze_news,
                IntervalTrigger(minutes=self.settings.news_scrape_interval_minutes),
                id="news_scraping",
                name="News Scraping & Sentiment Analysis",
                replace_existing=True
            )
            logger.info(f"Scheduled news scraping every {self.settings.news_scrape_interval_minutes} minutes")

        # Pattern monitoring every hour during market hours
        self.scheduler.add_job(
            self._monitor_patterns,
            CronTrigger(
                hour='9-16',  # 9 AM to 4 PM ET
                minute='*/60',  # Every hour
                day_of_week='mon-fri',
                timezone=pytz.timezone('US/Eastern')
            ),
            id="pattern_monitoring",
            name="Pattern Monitoring",
            replace_existing=True
        )
        logger.info("Scheduled pattern monitoring during market hours")

        self.scheduler.start()
        self._started = True
        logger.info("Market scheduler started successfully")

    async def stop(self):
        """Stop the scheduler"""
        if self._started:
            self.scheduler.shutdown()
            self._started = False
            logger.info("Market scheduler stopped")

    async def _send_daily_brief(self):
        """Generate and send daily market brief"""
        try:
            logger.info("Generating daily market brief...")

            # Generate the brief
            brief = await self.ai_service.generate_daily_brief()

            # Format for Telegram
            message = self._format_brief_for_telegram(brief)

            # Send via Telegram if configured
            if self.telegram_service:
                await self.telegram_service.send_message(message)
                logger.info("Daily brief sent via Telegram")

                # Update database to mark as sent
                from app.services.database import get_database_service
                from app.models import MarketBrief

                db = get_database_service()
                with db.get_session() as session:
                    brief_record = session.query(MarketBrief).get(brief.get("id"))
                    if brief_record:
                        brief_record.sent_to_telegram = True
                        brief_record.telegram_sent_at = datetime.now()
                        session.commit()

            logger.info("Daily brief completed successfully")

        except Exception as e:
            logger.error(f"Error sending daily brief: {e}", exc_info=True)

    async def _scrape_and_analyze_news(self):
        """Scrape news and perform sentiment analysis"""
        try:
            logger.info("Starting news scraping and sentiment analysis...")

            # Scrape general market news
            articles = await self.ai_service.scrape_news(ticker=None, limit=20)

            if articles:
                # Analyze sentiment
                sentiment = await self.ai_service.analyze_news_sentiment(max_articles=10)

                logger.info(
                    f"News analysis complete: {len(articles)} articles, "
                    f"sentiment: {sentiment.get('sentiment')} ({sentiment.get('score'):.2f})"
                )

                # If significant news, send alert
                if abs(sentiment.get('score', 0)) > 0.5:  # Strong sentiment
                    if self.telegram_service:
                        message = f"📰 **Market News Alert**\n\n"
                        message += f"Sentiment: {sentiment.get('sentiment').upper()} ({sentiment.get('score'):.2f})\n"
                        message += f"Analyzed {sentiment.get('articles_analyzed')} recent articles\n\n"
                        message += "Check /brief for full analysis"

                        await self.telegram_service.send_message(message)

        except Exception as e:
            logger.error(f"Error in news scraping: {e}", exc_info=True)

    async def _monitor_patterns(self):
        """Monitor for pattern breakouts and alerts"""
        try:
            logger.info("Monitoring patterns for alerts...")

            from app.services.database import get_database_service
            from app.models import Watchlist, Ticker, PatternScan
            from datetime import timedelta

            db = get_database_service()

            with db.get_session() as session:
                # Get active watchlist items
                watchlist_items = session.query(Watchlist).filter(
                    Watchlist.status == "Watching",
                    Watchlist.alerts_enabled == True
                ).all()

                for item in watchlist_items:
                    # Check if pattern triggered
                    ticker = session.query(Ticker).get(item.ticker_id)
                    if not ticker:
                        continue

                    # Get latest market data
                    from app.services.market_data import market_data_service
                    quote = await market_data_service.get_quote(ticker.symbol)

                    current_price = quote.get('price')
                    if not current_price:
                        continue

                    # Check if breakout occurred
                    if item.target_entry and current_price >= item.target_entry:
                        # Pattern triggered!
                        item.status = "Breaking Out"
                        item.triggered_at = datetime.now()
                        session.commit()

                        # Send alert
                        if self.telegram_service:
                            message = f"🚀 **BREAKOUT ALERT**\n\n"
                            message += f"**{ticker.symbol}** - {ticker.name}\n"
                            message += f"Price: ${current_price:.2f}\n"
                            message += f"Entry: ${item.target_entry:.2f}\n"
                            if item.target_price:
                                message += f"Target: ${item.target_price:.2f}\n"
                            if item.target_stop:
                                message += f"Stop: ${item.target_stop:.2f}\n"
                            message += f"\nReason: {item.reason}"

                            await self.telegram_service.send_message(message)

                        logger.info(f"Breakout alert sent for {ticker.symbol}")

            logger.info("Pattern monitoring complete")

        except Exception as e:
            logger.error(f"Error in pattern monitoring: {e}", exc_info=True)

    def _format_brief_for_telegram(self, brief: dict) -> str:
        """Format market brief for Telegram message"""
        message = "📊 **DAILY MARKET BRIEF**\n"
        message += f"_{datetime.now().strftime('%B %d, %Y')}_\n\n"

        # Market Summary
        message += "**Market Overview**\n"
        message += f"{brief.get('market_summary', 'N/A')}\n\n"

        # Sentiment
        sentiment = brief.get('sentiment', 'neutral')
        sentiment_emoji = {
            'bullish': '🟢',
            'bearish': '🔴',
            'neutral': '⚪',
            'mixed': '🟡'
        }.get(sentiment, '⚪')

        message += f"**Overall Sentiment:** {sentiment_emoji} {sentiment.upper()}\n"
        if brief.get('sentiment_score'):
            message += f"Score: {brief.get('sentiment_score'):.2f}\n"
        message += "\n"

        # Top Trade Ideas
        trade_ideas = brief.get('trade_ideas', [])
        if trade_ideas:
            message += "**💡 Trade Ideas**\n"
            for i, idea in enumerate(trade_ideas[:3], 1):  # Top 3
                message += f"{i}. **{idea.get('ticker')}** - {idea.get('setup')}\n"
                message += f"   Entry: ${idea.get('entry'):.2f} | "
                message += f"Stop: ${idea.get('stop'):.2f} | "
                message += f"Target: ${idea.get('target'):.2f}\n"
                message += f"   _{idea.get('reasoning', '')}_\n"
            message += "\n"

        # Pattern Highlights
        patterns = brief.get('pattern_highlights', [])
        if patterns:
            message += "**📈 Pattern Highlights**\n"
            for pattern in patterns[:3]:
                message += f"• {pattern}\n"
            message += "\n"

        # Risk Factors
        risks = brief.get('risk_factors', [])
        if risks:
            message += "**⚠️ Risks to Watch**\n"
            for risk in risks[:3]:
                message += f"• {risk}\n"
            message += "\n"

        message += "_Generated by Legend AI Market Analysis_"

        return message

    async def trigger_manual_brief(self):
        """Manually trigger a market brief (for testing or on-demand)"""
        await self._send_daily_brief()


# Global service instance
_scheduler_service = None


def get_scheduler_service() -> MarketSchedulerService:
    """Get or create scheduler service instance"""
    global _scheduler_service
    if _scheduler_service is None:
        _scheduler_service = MarketSchedulerService()
    return _scheduler_service
