"""
Content generation service for auto-posting trading analysis
Generates tweets, chart annotations, performance summaries, and pattern explanations
"""

import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
from jinja2 import Template
import random

logger = logging.getLogger(__name__)


class ContentGenerator:
    """Generate engaging social media content for trading analysis"""

    # Compliance disclaimers
    DISCLAIMERS = {
        "sec_disclaimer": "Not financial advice. For educational purposes only. Trade at your own risk.",
        "risk_warning": "⚠️ Trading involves substantial risk of loss. Past performance is not indicative of future results.",
        "performance_disclaimer": "Results shown are hypothetical and do not represent actual trading. Individual results may vary."
    }

    # Common trading hashtags
    HASHTAGS = {
        "general": ["trading", "stockmarket", "daytrading", "swingtrading", "technicalanalysis"],
        "patterns": ["chartpatterns", "priceaction", "breakout", "vcp", "cupandhandle"],
        "performance": ["tradingresults", "stockperformance", "marketanalysis"],
        "education": ["tradingsetup", "stockeducation", "learntotrade"]
    }

    def __init__(self):
        """Initialize content generator with templates"""
        self.templates = self._load_templates()

    def _load_templates(self) -> Dict[str, Template]:
        """Load Jinja2 templates for different content types"""
        return {
            "tweet_pattern": Template("""🚀 {{ pattern_type }} pattern detected in ${{ symbol }}!

📊 Score: {{ score }}/100
💰 Entry: ${{ entry_price }}
🎯 Target: ${{ target_price }} ({{ upside }}% upside)
🛑 Stop: ${{ stop_price }}
📈 R/R Ratio: {{ rr_ratio }}

{{ disclaimer }}
{{ hashtags }}"""),

            "tweet_performance": Template("""📊 Trading Performance Update

{% if winners > 0 %}✅ Winners: {{ winners }} ({{ win_rate }}%){% endif %}
{% if losers > 0 %}❌ Losers: {{ losers }}{% endif %}
💵 Total Return: {{ total_return }}%
📈 Avg Winner: {{ avg_winner }}%
📉 Avg Loser: {{ avg_loser }}%

{{ disclaimer }}
{{ hashtags }}"""),

            "chart_annotation": Template("""📈 ${{ symbol }} Technical Analysis

{{ pattern_name }} pattern forming
⏱️ Consolidation: {{ consolidation_days }} days
📊 Volume: {{ volume_status }}
💪 RS Rating: {{ rs_rating }}/100

Key levels:
• Entry: ${{ entry_price }}
• Target: ${{ target_price }}
• Stop: ${{ stop_price }}

{{ hashtags }}"""),

            "pattern_explanation": Template("""📚 Pattern Spotlight: {{ pattern_type }}

What to look for:
{{ criteria }}

Why it works:
{{ explanation }}

Current example: ${{ symbol }}
Chart: {{ chart_url }}

{{ disclaimer }}
{{ hashtags }}"""),

            "breakout_alert": Template("""🔔 BREAKOUT ALERT: ${{ symbol }}

{{ pattern_type }} breaking out NOW!
💥 Price: ${{ current_price }} (+{{ change_percent }}%)
📊 Volume: {{ volume_ratio }}x avg
⏰ Time: {{ timestamp }}

Setup from {{ days_ago }} days ago playing out perfectly!

{{ disclaimer }}
{{ hashtags }}"""),

            "daily_summary": Template("""📊 Daily Market Scan Results

🔍 Scanned: {{ tickers_scanned }} stocks
🎯 Patterns Found: {{ patterns_found }}
⭐ Top Score: {{ top_score }}/100
⏱️ Scan Time: {{ scan_duration }}s

Top Setups:
{% for setup in top_setups %}• ${{ setup.symbol }}: {{ setup.pattern }} ({{ setup.score }}/100)
{% endfor %}

Full analysis: {{ analysis_url }}

{{ hashtags }}"""),

            "stocktwits_post": Template("""${{ symbol }} - {{ pattern_type }} Pattern

Score: {{ score }}/100
Entry: ${{ entry_price }} | Target: ${{ target_price }} | Stop: ${{ stop_price }}
R/R: {{ rr_ratio }}

{{ disclaimer }}"""),

            "linkedin_post": Template("""Technical Analysis Update: {{ symbol }}

I've identified a {{ pattern_type }} pattern in {{ symbol }} with a technical score of {{ score }}/100.

Key Metrics:
• Entry Price: ${{ entry_price }}
• Price Target: ${{ target_price }} ({{ upside }}% potential upside)
• Stop Loss: ${{ stop_price }}
• Risk/Reward Ratio: {{ rr_ratio }}
• Consolidation Period: {{ consolidation_days }} days

This setup aligns with Mark Minervini's stage analysis methodology, showing tight consolidation with volume dry-up and strong relative strength.

{{ disclaimer }}

#TechnicalAnalysis #StockTrading #InvestmentStrategy"""),

            "reddit_post": Template("""**{{ pattern_type }} Setup: ${{ symbol }}**

Just ran my scanner and found this setup that meets Minervini's criteria:

**Technical Details:**
- Pattern: {{ pattern_type }}
- Score: {{ score }}/100
- Entry: ${{ entry_price }}
- Target: ${{ target_price }} ({{ upside }}% upside)
- Stop: ${{ stop_price }}
- Risk/Reward: {{ rr_ratio }}

**Why I like it:**
{{ analysis }}

**Chart:** {{ chart_url }}

{{ disclaimer }}

What do you all think? Anyone else watching this one?""")
        }

    def generate_tweet(
        self,
        symbol: str,
        pattern_type: str,
        score: float,
        entry_price: float,
        target_price: float,
        stop_price: float,
        rr_ratio: float,
        include_disclaimer: bool = True
    ) -> str:
        """Generate a tweet about a pattern detection"""
        upside = round(((target_price - entry_price) / entry_price) * 100, 1)

        hashtags = self._generate_hashtags(["general", "patterns"], max_tags=3)
        disclaimer = self.DISCLAIMERS["sec_disclaimer"] if include_disclaimer else ""

        content = self.templates["tweet_pattern"].render(
            symbol=symbol,
            pattern_type=pattern_type,
            score=round(score),
            entry_price=round(entry_price, 2),
            target_price=round(target_price, 2),
            stop_price=round(stop_price, 2),
            upside=upside,
            rr_ratio=round(rr_ratio, 1),
            disclaimer=disclaimer,
            hashtags=hashtags
        )

        return content.strip()

    def generate_performance_summary(
        self,
        winners: int,
        losers: int,
        total_return: float,
        avg_winner: float,
        avg_loser: float,
        include_disclaimer: bool = True
    ) -> str:
        """Generate a performance summary tweet"""
        total_trades = winners + losers
        win_rate = round((winners / total_trades) * 100, 1) if total_trades > 0 else 0

        hashtags = self._generate_hashtags(["performance", "general"], max_tags=3)
        disclaimer = self.DISCLAIMERS["performance_disclaimer"] if include_disclaimer else ""

        content = self.templates["tweet_performance"].render(
            winners=winners,
            losers=losers,
            win_rate=win_rate,
            total_return=round(total_return, 1),
            avg_winner=round(avg_winner, 1),
            avg_loser=round(avg_loser, 1),
            disclaimer=disclaimer,
            hashtags=hashtags
        )

        return content.strip()

    def generate_chart_annotation(
        self,
        symbol: str,
        pattern_name: str,
        consolidation_days: int,
        volume_status: str,
        rs_rating: float,
        entry_price: float,
        target_price: float,
        stop_price: float
    ) -> str:
        """Generate chart annotation content"""
        hashtags = self._generate_hashtags(["patterns", "general"], max_tags=4)

        content = self.templates["chart_annotation"].render(
            symbol=symbol,
            pattern_name=pattern_name,
            consolidation_days=consolidation_days,
            volume_status=volume_status,
            rs_rating=round(rs_rating),
            entry_price=round(entry_price, 2),
            target_price=round(target_price, 2),
            stop_price=round(stop_price, 2),
            hashtags=hashtags
        )

        return content.strip()

    def generate_pattern_explanation(
        self,
        pattern_type: str,
        criteria: str,
        explanation: str,
        symbol: str,
        chart_url: str,
        include_disclaimer: bool = True
    ) -> str:
        """Generate educational pattern explanation"""
        hashtags = self._generate_hashtags(["education", "patterns"], max_tags=4)
        disclaimer = self.DISCLAIMERS["sec_disclaimer"] if include_disclaimer else ""

        content = self.templates["pattern_explanation"].render(
            pattern_type=pattern_type,
            criteria=criteria,
            explanation=explanation,
            symbol=symbol,
            chart_url=chart_url,
            disclaimer=disclaimer,
            hashtags=hashtags
        )

        return content.strip()

    def generate_breakout_alert(
        self,
        symbol: str,
        pattern_type: str,
        current_price: float,
        change_percent: float,
        volume_ratio: float,
        days_ago: int,
        include_disclaimer: bool = True
    ) -> str:
        """Generate breakout alert content"""
        hashtags = self._generate_hashtags(["patterns", "general"], max_tags=3)
        disclaimer = self.DISCLAIMERS["risk_warning"] if include_disclaimer else ""

        content = self.templates["breakout_alert"].render(
            symbol=symbol,
            pattern_type=pattern_type,
            current_price=round(current_price, 2),
            change_percent=round(change_percent, 1),
            volume_ratio=round(volume_ratio, 1),
            timestamp=datetime.now().strftime("%I:%M %p ET"),
            days_ago=days_ago,
            disclaimer=disclaimer,
            hashtags=hashtags
        )

        return content.strip()

    def generate_daily_summary(
        self,
        tickers_scanned: int,
        patterns_found: int,
        top_score: float,
        scan_duration: float,
        top_setups: List[Dict[str, Any]],
        analysis_url: str
    ) -> str:
        """Generate daily scan summary"""
        hashtags = self._generate_hashtags(["general", "patterns"], max_tags=4)

        content = self.templates["daily_summary"].render(
            tickers_scanned=tickers_scanned,
            patterns_found=patterns_found,
            top_score=round(top_score),
            scan_duration=round(scan_duration, 1),
            top_setups=top_setups[:5],  # Top 5 setups
            analysis_url=analysis_url,
            hashtags=hashtags
        )

        return content.strip()

    def generate_stocktwits_post(
        self,
        symbol: str,
        pattern_type: str,
        score: float,
        entry_price: float,
        target_price: float,
        stop_price: float,
        rr_ratio: float
    ) -> str:
        """Generate StockTwits post (shorter format)"""
        content = self.templates["stocktwits_post"].render(
            symbol=symbol,
            pattern_type=pattern_type,
            score=round(score),
            entry_price=round(entry_price, 2),
            target_price=round(target_price, 2),
            stop_price=round(stop_price, 2),
            rr_ratio=round(rr_ratio, 1),
            disclaimer=self.DISCLAIMERS["sec_disclaimer"]
        )

        return content.strip()

    def generate_linkedin_post(
        self,
        symbol: str,
        pattern_type: str,
        score: float,
        entry_price: float,
        target_price: float,
        stop_price: float,
        rr_ratio: float,
        consolidation_days: int
    ) -> str:
        """Generate LinkedIn post (professional format)"""
        upside = round(((target_price - entry_price) / entry_price) * 100, 1)

        content = self.templates["linkedin_post"].render(
            symbol=symbol,
            pattern_type=pattern_type,
            score=round(score),
            entry_price=round(entry_price, 2),
            target_price=round(target_price, 2),
            stop_price=round(stop_price, 2),
            upside=upside,
            rr_ratio=round(rr_ratio, 1),
            consolidation_days=consolidation_days,
            disclaimer=self.DISCLAIMERS["sec_disclaimer"]
        )

        return content.strip()

    def generate_reddit_post(
        self,
        symbol: str,
        pattern_type: str,
        score: float,
        entry_price: float,
        target_price: float,
        stop_price: float,
        rr_ratio: float,
        analysis: str,
        chart_url: str
    ) -> str:
        """Generate Reddit post (discussion format)"""
        upside = round(((target_price - entry_price) / entry_price) * 100, 1)

        content = self.templates["reddit_post"].render(
            symbol=symbol,
            pattern_type=pattern_type,
            score=round(score),
            entry_price=round(entry_price, 2),
            target_price=round(target_price, 2),
            stop_price=round(stop_price, 2),
            upside=upside,
            rr_ratio=round(rr_ratio, 1),
            analysis=analysis,
            chart_url=chart_url,
            disclaimer=self.DISCLAIMERS["sec_disclaimer"]
        )

        return content.strip()

    def _generate_hashtags(self, categories: List[str], max_tags: int = 5) -> str:
        """Generate hashtags from specified categories"""
        tags = []
        for category in categories:
            if category in self.HASHTAGS:
                tags.extend(self.HASHTAGS[category])

        # Randomly select tags and deduplicate
        selected_tags = random.sample(list(set(tags)), min(max_tags, len(set(tags))))
        return " ".join([f"#{tag}" for tag in selected_tags])

    def add_compliance_disclaimer(
        self,
        content: str,
        disclaimer_type: str = "sec_disclaimer"
    ) -> str:
        """Add compliance disclaimer to content"""
        if disclaimer_type in self.DISCLAIMERS:
            disclaimer = self.DISCLAIMERS[disclaimer_type]
            return f"{content}\n\n{disclaimer}"
        return content

    def get_disclaimer(self, disclaimer_type: str) -> str:
        """Get a specific disclaimer"""
        return self.DISCLAIMERS.get(disclaimer_type, "")
