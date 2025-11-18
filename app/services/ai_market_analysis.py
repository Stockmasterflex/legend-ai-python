"""
AI-Powered Market Analysis Service
Provides multi-model AI analysis, chart-to-text, news sentiment, and market briefs
"""

import json
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import asyncio
from openai import AsyncOpenAI
import aiohttp
from bs4 import BeautifulSoup

from app.config import get_settings
from app.services.database import get_database_service
from app.services.market_data import market_data_service
from app.models import (
    MarketAnalysis, NewsArticle, NewsSentiment,
    MarketBrief, AIQuery, Ticker
)
from sqlalchemy import desc

logger = logging.getLogger(__name__)


class AIMarketAnalysisService:
    """Multi-model AI market analysis service"""

    def __init__(self):
        self.settings = get_settings()
        self.db = get_database_service()

        # Initialize OpenAI client for OpenRouter
        self.openrouter_client = None
        if self.settings.openrouter_api_key:
            self.openrouter_client = AsyncOpenAI(
                api_key=self.settings.openrouter_api_key,
                base_url="https://openrouter.ai/api/v1"
            )

        # Initialize direct OpenAI client (if available)
        self.openai_client = None
        if self.settings.openai_api_key:
            self.openai_client = AsyncOpenAI(api_key=self.settings.openai_api_key)

    async def _call_ai_model(
        self,
        model: str,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 4000,
        image_url: Optional[str] = None
    ) -> str:
        """Call AI model via OpenRouter or direct OpenAI"""

        try:
            client = self.openrouter_client or self.openai_client
            if not client:
                raise ValueError("No AI API key configured")

            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})

            # Handle vision models with images
            if image_url and "vision" in model.lower():
                messages.append({
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": {"url": image_url}}
                    ]
                })
            else:
                messages.append({"role": "user", "content": prompt})

            response = await client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )

            return response.choices[0].message.content

        except Exception as e:
            logger.error(f"Error calling AI model {model}: {e}")
            raise

    async def analyze_chart(
        self,
        ticker: str,
        chart_url: str,
        use_vision: bool = True
    ) -> Dict[str, Any]:
        """
        Analyze chart using GPT-4 Vision or text-based analysis

        Args:
            ticker: Stock ticker symbol
            chart_url: URL to the chart image
            use_vision: Whether to use vision model (GPT-4V)

        Returns:
            Analysis results with support/resistance, trends, patterns
        """
        logger.info(f"Analyzing chart for {ticker} using vision={use_vision}")

        # Get current market data for context
        market_data = await market_data_service.get_quote(ticker)

        if use_vision and self.settings.enable_chart_analysis:
            # Use GPT-4 Vision for chart analysis
            prompt = f"""Analyze this stock chart for {ticker} (current price: ${market_data.get('price', 'N/A')}).

Provide a detailed technical analysis including:

1. **Support Levels**: Identify key support price levels (provide as array of numbers)
2. **Resistance Levels**: Identify key resistance price levels (provide as array of numbers)
3. **Trend Analysis**: Current trend (bullish/bearish/neutral) and strength
4. **Chart Patterns**: Any recognizable patterns (head & shoulders, triangles, flags, etc.)
5. **Volume Analysis**: Volume trends and significance
6. **Risk Assessment**: Key risks and potential catalysts
7. **Entry/Exit Recommendations**: Suggested entry points, stop loss, and targets

Format your response as JSON with these keys:
- support_levels: [prices]
- resistance_levels: [prices]
- trend_direction: "bullish"|"bearish"|"neutral"|"mixed"
- trend_strength: 1-10
- patterns: ["pattern1", "pattern2"]
- volume_analysis: "description"
- risk_assessment: "description"
- trade_ideas: [{{entry: price, stop: price, target: price, reasoning: "text"}}]
- summary: "overall analysis"
- confidence: 1-100
"""

            system_prompt = "You are an expert technical analyst specializing in chart pattern recognition and technical analysis. Provide clear, actionable insights backed by technical indicators."

            try:
                response = await self._call_ai_model(
                    model=self.settings.ai_model_gpt4_vision,
                    prompt=prompt,
                    system_prompt=system_prompt,
                    temperature=0.5,
                    image_url=chart_url
                )

                # Parse JSON response
                analysis_data = json.loads(response)

                # Save to database
                with self.db.get_session() as session:
                    # Get or create ticker
                    ticker_obj = session.query(Ticker).filter(Ticker.symbol == ticker).first()

                    analysis = MarketAnalysis(
                        ticker_id=ticker_obj.id if ticker_obj else None,
                        analysis_type="chart",
                        ai_model=self.settings.ai_model_gpt4_vision,
                        analysis_text=response,
                        support_levels=json.dumps(analysis_data.get("support_levels", [])),
                        resistance_levels=json.dumps(analysis_data.get("resistance_levels", [])),
                        trend_direction=analysis_data.get("trend_direction", "neutral"),
                        sentiment_score=analysis_data.get("trend_strength", 5) / 10.0,
                        risk_assessment=analysis_data.get("risk_assessment"),
                        trade_ideas=json.dumps(analysis_data.get("trade_ideas", [])),
                        confidence_score=analysis_data.get("confidence", 70),
                        chart_url=chart_url
                    )
                    session.add(analysis)
                    session.commit()

                logger.info(f"Chart analysis completed for {ticker}")
                return analysis_data

            except json.JSONDecodeError:
                # Fallback: return structured response from text
                logger.warning("Failed to parse JSON, using text response")
                return {
                    "summary": response,
                    "trend_direction": "neutral",
                    "confidence": 50
                }
        else:
            # Use Claude for text-based technical analysis
            prompt = f"""Analyze {ticker} based on current data:
Price: ${market_data.get('price', 'N/A')}
Change: {market_data.get('change_percent', 'N/A')}%
Volume: {market_data.get('volume', 'N/A')}

Provide technical analysis including support/resistance levels, trend, and trading ideas."""

            response = await self._call_ai_model(
                model=self.settings.ai_model_claude,
                prompt=prompt,
                temperature=0.5
            )

            return {"summary": response, "trend_direction": "neutral"}

    async def scrape_news(self, ticker: Optional[str] = None, limit: int = 20) -> List[Dict[str, Any]]:
        """
        Scrape news articles for a ticker or general market news

        Args:
            ticker: Stock ticker (None for general market news)
            limit: Maximum number of articles to scrape

        Returns:
            List of news articles
        """
        logger.info(f"Scraping news for {ticker or 'market'}")

        articles = []
        sources = self.settings.news_sources.split(",")

        async with aiohttp.ClientSession() as session:
            for source in sources:
                try:
                    if source.strip() == "yahoo":
                        articles.extend(await self._scrape_yahoo_finance(session, ticker, limit // len(sources)))
                    elif source.strip() == "marketwatch":
                        articles.extend(await self._scrape_marketwatch(session, ticker, limit // len(sources)))
                    elif source.strip() == "benzinga":
                        articles.extend(await self._scrape_benzinga(session, ticker, limit // len(sources)))
                except Exception as e:
                    logger.error(f"Error scraping {source}: {e}")
                    continue

        # Save to database
        with self.db.get_session() as db_session:
            ticker_obj = None
            if ticker:
                ticker_obj = db_session.query(Ticker).filter(Ticker.symbol == ticker).first()

            for article in articles:
                # Check if article already exists
                existing = db_session.query(NewsArticle).filter(
                    NewsArticle.url == article["url"]
                ).first()

                if not existing:
                    news_article = NewsArticle(
                        ticker_id=ticker_obj.id if ticker_obj else None,
                        title=article["title"],
                        source=article["source"],
                        url=article["url"],
                        content=article.get("content"),
                        published_at=article.get("published_at"),
                        category=article.get("category")
                    )
                    db_session.add(news_article)

            db_session.commit()

        logger.info(f"Scraped {len(articles)} articles")
        return articles

    async def _scrape_yahoo_finance(self, session: aiohttp.ClientSession, ticker: Optional[str], limit: int) -> List[Dict]:
        """Scrape Yahoo Finance news"""
        articles = []

        try:
            if ticker:
                url = f"https://finance.yahoo.com/quote/{ticker}/news"
            else:
                url = "https://finance.yahoo.com/news"

            async with session.get(url, headers={"User-Agent": "Mozilla/5.0"}) as response:
                html = await response.text()
                soup = BeautifulSoup(html, 'html.parser')

                # Find news articles (simplified - adjust selectors as needed)
                news_items = soup.find_all('div', class_='Ov(h)', limit=limit)

                for item in news_items:
                    try:
                        title_elem = item.find('h3')
                        link_elem = item.find('a')

                        if title_elem and link_elem:
                            articles.append({
                                "title": title_elem.text.strip(),
                                "source": "yahoo",
                                "url": f"https://finance.yahoo.com{link_elem['href']}" if link_elem['href'].startswith('/') else link_elem['href'],
                                "published_at": datetime.now(),
                                "category": "market"
                            })
                    except Exception as e:
                        logger.debug(f"Error parsing Yahoo article: {e}")
                        continue

        except Exception as e:
            logger.error(f"Error scraping Yahoo Finance: {e}")

        return articles

    async def _scrape_marketwatch(self, session: aiohttp.ClientSession, ticker: Optional[str], limit: int) -> List[Dict]:
        """Scrape MarketWatch news"""
        # Simplified implementation - expand as needed
        return []

    async def _scrape_benzinga(self, session: aiohttp.ClientSession, ticker: Optional[str], limit: int) -> List[Dict]:
        """Scrape Benzinga news"""
        # Simplified implementation - expand as needed
        return []

    async def analyze_news_sentiment(
        self,
        ticker: Optional[str] = None,
        max_articles: int = 10
    ) -> Dict[str, Any]:
        """
        Analyze sentiment of recent news articles

        Args:
            ticker: Stock ticker (None for general market)
            max_articles: Maximum articles to analyze

        Returns:
            Aggregated sentiment analysis
        """
        logger.info(f"Analyzing news sentiment for {ticker or 'market'}")

        # Get recent articles from database
        with self.db.get_session() as session:
            query = session.query(NewsArticle)

            if ticker:
                ticker_obj = session.query(Ticker).filter(Ticker.symbol == ticker).first()
                if ticker_obj:
                    query = query.filter(NewsArticle.ticker_id == ticker_obj.id)

            # Only recent articles
            cutoff_time = datetime.now() - timedelta(hours=self.settings.news_max_age_hours)
            query = query.filter(NewsArticle.scraped_at >= cutoff_time)

            articles = query.order_by(desc(NewsArticle.published_at)).limit(max_articles).all()

        if not articles:
            logger.info("No articles found for sentiment analysis")
            return {"sentiment": "neutral", "score": 0.0, "articles_analyzed": 0}

        # Analyze each article with AI
        sentiments = []

        for article in articles:
            prompt = f"""Analyze the sentiment of this news article for {ticker or 'the market'}:

Title: {article.title}
Content: {article.content[:500] if article.content else 'N/A'}

Provide sentiment analysis as JSON:
{{
    "sentiment": "bullish"|"bearish"|"neutral",
    "score": -1.0 to 1.0,
    "key_points": ["point1", "point2"],
    "impact": "high"|"medium"|"low",
    "relevance": 0.0 to 1.0
}}
"""

            try:
                response = await self._call_ai_model(
                    model=self.settings.ai_model_claude,
                    prompt=prompt,
                    temperature=0.3,
                    max_tokens=500
                )

                sentiment_data = json.loads(response)
                sentiments.append(sentiment_data)

                # Save to database
                with self.db.get_session() as db_session:
                    ticker_obj = None
                    if ticker:
                        ticker_obj = db_session.query(Ticker).filter(Ticker.symbol == ticker).first()

                    news_sentiment = NewsSentiment(
                        article_id=article.id,
                        ticker_id=ticker_obj.id if ticker_obj else None,
                        ai_model=self.settings.ai_model_claude,
                        sentiment=sentiment_data.get("sentiment", "neutral"),
                        sentiment_score=sentiment_data.get("score", 0.0),
                        key_points=json.dumps(sentiment_data.get("key_points", [])),
                        impact_assessment=sentiment_data.get("impact", "medium"),
                        relevance_score=sentiment_data.get("relevance", 0.5)
                    )
                    db_session.add(news_sentiment)
                    db_session.commit()

            except Exception as e:
                logger.error(f"Error analyzing article sentiment: {e}")
                continue

        # Aggregate sentiments
        if sentiments:
            avg_score = sum(s.get("score", 0) for s in sentiments) / len(sentiments)
            overall_sentiment = "bullish" if avg_score > 0.2 else "bearish" if avg_score < -0.2 else "neutral"

            return {
                "sentiment": overall_sentiment,
                "score": avg_score,
                "articles_analyzed": len(sentiments),
                "detailed_sentiments": sentiments
            }

        return {"sentiment": "neutral", "score": 0.0, "articles_analyzed": 0}

    async def generate_daily_brief(self) -> Dict[str, Any]:
        """
        Generate comprehensive daily market brief with AI analysis

        Returns:
            Daily market brief data
        """
        logger.info("Generating daily market brief")

        # Get top movers
        movers = await self._get_top_movers()

        # Get sector performance
        sector_perf = await self._get_sector_performance()

        # Get recent pattern detections
        patterns = await self._get_recent_patterns()

        # Get news sentiment
        news_sentiment = await self.analyze_news_sentiment(max_articles=20)

        # Generate AI analysis
        prompt = f"""Generate a comprehensive daily market brief based on this data:

**Top Movers:**
{json.dumps(movers, indent=2)}

**Sector Performance:**
{json.dumps(sector_perf, indent=2)}

**Pattern Detections:**
{json.dumps(patterns, indent=2)}

**News Sentiment:**
Overall: {news_sentiment.get('sentiment', 'neutral')} (Score: {news_sentiment.get('score', 0):.2f})

Provide a JSON response with:
{{
    "market_summary": "Overall market analysis and key themes",
    "top_movers_analysis": ["Analysis of notable movers"],
    "sector_insights": ["Sector-specific insights"],
    "pattern_highlights": ["Notable patterns worth watching"],
    "risk_factors": ["Key risks to watch"],
    "trade_ideas": [
        {{
            "ticker": "SYMBOL",
            "setup": "pattern/setup type",
            "entry": price,
            "stop": price,
            "target": price,
            "reasoning": "why this trade"
        }}
    ],
    "sentiment": "bullish"|"bearish"|"neutral"|"mixed",
    "sentiment_score": -1.0 to 1.0
}}
"""

        system_prompt = "You are a professional market analyst providing daily market briefs for traders. Be concise, actionable, and focus on high-probability setups."

        try:
            response = await self._call_ai_model(
                model=self.settings.ai_model_claude,
                prompt=prompt,
                system_prompt=system_prompt,
                temperature=0.6,
                max_tokens=3000
            )

            brief_data = json.loads(response)

            # Save to database
            with self.db.get_session() as session:
                market_brief = MarketBrief(
                    brief_date=datetime.now(),
                    market_summary=brief_data.get("market_summary", ""),
                    top_movers=json.dumps(movers),
                    sector_performance=json.dumps(sector_perf),
                    pattern_highlights=json.dumps(brief_data.get("pattern_highlights", [])),
                    risk_factors=json.dumps(brief_data.get("risk_factors", [])),
                    trade_ideas=json.dumps(brief_data.get("trade_ideas", [])),
                    market_sentiment=brief_data.get("sentiment", "neutral"),
                    sentiment_score=brief_data.get("sentiment_score", 0.0),
                    ai_model=self.settings.ai_model_claude
                )
                session.add(market_brief)
                session.commit()

                brief_data["id"] = market_brief.id

            logger.info("Daily market brief generated successfully")
            return brief_data

        except Exception as e:
            logger.error(f"Error generating daily brief: {e}")
            raise

    async def _get_top_movers(self, limit: int = 10) -> List[Dict]:
        """Get top gaining/losing stocks"""
        # Simplified - would integrate with real market data
        return []

    async def _get_sector_performance(self) -> Dict[str, float]:
        """Get sector performance data"""
        # Simplified - would integrate with real sector data
        return {}

    async def _get_recent_patterns(self, hours: int = 24, limit: int = 10) -> List[Dict]:
        """Get recent pattern detections"""
        from app.models import PatternScan

        with self.db.get_session() as session:
            cutoff = datetime.now() - timedelta(hours=hours)
            patterns = session.query(PatternScan).filter(
                PatternScan.scanned_at >= cutoff,
                PatternScan.score >= 70  # Only high-quality patterns
            ).order_by(desc(PatternScan.score)).limit(limit).all()

            return [{
                "ticker": p.ticker_id,  # Would need to join with Ticker table
                "pattern": p.pattern_type,
                "score": p.score,
                "entry": p.entry_price,
                "target": p.target_price
            } for p in patterns]

    async def process_natural_language_query(
        self,
        query: str,
        user_id: str = "api"
    ) -> Dict[str, Any]:
        """
        Process natural language query and execute appropriate actions

        Args:
            query: User's natural language query
            user_id: User identifier

        Returns:
            Query results with AI response
        """
        logger.info(f"Processing NL query: {query}")
        start_time = datetime.now()

        # Use AI to interpret the query
        interpret_prompt = f"""Interpret this trading/market query and extract actionable parameters:

Query: "{query}"

Provide JSON response:
{{
    "query_type": "search"|"analysis"|"education"|"alert",
    "action": "scan_patterns"|"analyze_ticker"|"get_news"|"explain_pattern",
    "tickers": ["SYMBOL1", "SYMBOL2"],
    "filters": {{
        "sector": "Tech"|null,
        "pattern": "VCP"|"Cup and Handle"|null,
        "trend": "bullish"|"bearish"|null,
        "min_score": 70
    }},
    "intent": "Brief description of what user wants"
}}
"""

        try:
            interpretation = await self._call_ai_model(
                model=self.settings.ai_model_claude,
                prompt=interpret_prompt,
                temperature=0.3,
                max_tokens=500
            )

            query_params = json.loads(interpretation)

            # Execute action based on interpretation
            results = await self._execute_query_action(query_params)

            # Generate natural language response
            response_prompt = f"""User asked: "{query}"

We found these results:
{json.dumps(results, indent=2)}

Provide a helpful, conversational response explaining the findings."""

            response_text = await self._call_ai_model(
                model=self.settings.ai_model_claude,
                prompt=response_prompt,
                temperature=0.7,
                max_tokens=1000
            )

            execution_time = (datetime.now() - start_time).total_seconds() * 1000

            # Save to database
            with self.db.get_session() as session:
                ai_query = AIQuery(
                    user_id=user_id,
                    query_text=query,
                    query_type=query_params.get("query_type"),
                    ai_model=self.settings.ai_model_claude,
                    response_text=response_text,
                    tickers_mentioned=json.dumps(query_params.get("tickers", [])),
                    actions_taken=json.dumps([query_params.get("action")]),
                    results_found=len(results.get("results", [])),
                    execution_time_ms=execution_time
                )
                session.add(ai_query)
                session.commit()

            return {
                "query": query,
                "interpretation": query_params,
                "results": results,
                "response": response_text,
                "execution_time_ms": execution_time
            }

        except Exception as e:
            logger.error(f"Error processing NL query: {e}")
            return {
                "query": query,
                "error": str(e),
                "response": "I encountered an error processing your query. Please try rephrasing."
            }

    async def _execute_query_action(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the action based on query interpretation"""
        action = params.get("action")

        if action == "scan_patterns":
            # Run pattern scan with filters
            return {"results": [], "action": "pattern_scan"}
        elif action == "analyze_ticker":
            # Analyze specific tickers
            tickers = params.get("tickers", [])
            analyses = []
            for ticker in tickers:
                # Get analysis for ticker
                analyses.append({"ticker": ticker, "analysis": "..."})
            return {"results": analyses, "action": "ticker_analysis"}
        elif action == "get_news":
            # Get news for tickers
            return {"results": [], "action": "news_fetch"}
        else:
            return {"results": [], "action": "unknown"}


# Global service instance
_ai_market_analysis_service = None


def get_ai_market_analysis_service() -> AIMarketAnalysisService:
    """Get or create AI market analysis service instance"""
    global _ai_market_analysis_service
    if _ai_market_analysis_service is None:
        _ai_market_analysis_service = AIMarketAnalysisService()
    return _ai_market_analysis_service
