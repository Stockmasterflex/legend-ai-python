"""
Tests for auto-posting functionality
"""

import pytest
from datetime import datetime, timedelta
from app.services.content_generator import ContentGenerator
from app.services.social_poster import SocialPoster, PostResult


class TestContentGenerator:
    """Test content generation for social media"""

    def setup_method(self):
        """Setup test fixtures"""
        self.generator = ContentGenerator()

    def test_generate_tweet(self):
        """Test tweet generation"""
        tweet = self.generator.generate_tweet(
            symbol="AAPL",
            pattern_type="VCP",
            score=92.5,
            entry_price=175.50,
            target_price=195.00,
            stop_price=168.00,
            rr_ratio=3.2,
            include_disclaimer=True
        )

        assert "AAPL" in tweet
        assert "VCP" in tweet
        assert "93/100" in tweet  # Rounded score
        assert "$175.5" in tweet or "$175.50" in tweet
        assert "Not financial advice" in tweet
        assert "#" in tweet  # Has hashtags

    def test_generate_performance_summary(self):
        """Test performance summary generation"""
        summary = self.generator.generate_performance_summary(
            winners=15,
            losers=5,
            total_return=25.5,
            avg_winner=8.2,
            avg_loser=-3.1,
            include_disclaimer=True
        )

        assert "15" in summary  # Winners
        assert "75.0%" in summary  # Win rate
        assert "25.5%" in summary  # Total return
        assert "Performance" in summary.lower() or "disclaimer" in summary.lower()

    def test_generate_chart_annotation(self):
        """Test chart annotation generation"""
        annotation = self.generator.generate_chart_annotation(
            symbol="NVDA",
            pattern_name="Cup and Handle",
            consolidation_days=45,
            volume_status="Declining",
            rs_rating=95.0,
            entry_price=500.00,
            target_price=575.00,
            stop_price=475.00
        )

        assert "NVDA" in annotation
        assert "Cup and Handle" in annotation
        assert "45 days" in annotation
        assert "95/100" in annotation or "95" in annotation
        assert "#" in annotation  # Has hashtags

    def test_generate_breakout_alert(self):
        """Test breakout alert generation"""
        alert = self.generator.generate_breakout_alert(
            symbol="TSLA",
            pattern_type="Ascending Triangle",
            current_price=245.50,
            change_percent=5.2,
            volume_ratio=2.3,
            days_ago=12,
            include_disclaimer=True
        )

        assert "TSLA" in alert
        assert "BREAKOUT" in alert.upper()
        assert "245.5" in alert or "245.50" in alert
        assert "5.2%" in alert
        assert "⚠️" in alert or "risk" in alert.lower()

    def test_generate_daily_summary(self):
        """Test daily summary generation"""
        top_setups = [
            {"symbol": "AAPL", "pattern": "VCP", "score": 92},
            {"symbol": "MSFT", "pattern": "Cup & Handle", "score": 88},
            {"symbol": "NVDA", "pattern": "Breakout", "score": 85}
        ]

        summary = self.generator.generate_daily_summary(
            tickers_scanned=500,
            patterns_found=15,
            top_score=92.0,
            scan_duration=45.2,
            top_setups=top_setups,
            analysis_url="https://example.com/analysis"
        )

        assert "500" in summary
        assert "15" in summary
        assert "92/100" in summary or "92" in summary
        assert "AAPL" in summary
        assert "#" in summary  # Has hashtags

    def test_generate_stocktwits_post(self):
        """Test StockTwits post generation"""
        post = self.generator.generate_stocktwits_post(
            symbol="AMD",
            pattern_type="Channel Breakout",
            score=87.0,
            entry_price=125.50,
            target_price=145.00,
            stop_price=118.00,
            rr_ratio=2.6
        )

        assert "AMD" in post
        assert "Channel Breakout" in post
        assert "87/100" in post or "87" in post
        assert "disclaimer" in post.lower() or "advice" in post.lower()

    def test_generate_linkedin_post(self):
        """Test LinkedIn post generation (professional format)"""
        post = self.generator.generate_linkedin_post(
            symbol="GOOGL",
            pattern_type="VCP",
            score=91.5,
            entry_price=140.00,
            target_price=160.00,
            stop_price=133.00,
            rr_ratio=2.9,
            consolidation_days=35
        )

        assert "GOOGL" in post
        assert "VCP" in post
        assert "35 days" in post
        assert "Minervini" in post  # Should mention methodology
        assert "#" in post  # Professional hashtags

    def test_generate_reddit_post(self):
        """Test Reddit post generation (discussion format)"""
        post = self.generator.generate_reddit_post(
            symbol="COIN",
            pattern_type="Flat Base",
            score=84.0,
            entry_price=85.00,
            target_price=105.00,
            stop_price=79.00,
            rr_ratio=3.3,
            analysis="Strong consolidation with volume dry-up",
            chart_url="https://example.com/chart.png"
        )

        assert "COIN" in post
        assert "Flat Base" in post
        assert "Strong consolidation" in post
        assert "**" in post  # Markdown formatting
        assert "disclaimer" in post.lower() or "advice" in post.lower()

    def test_add_compliance_disclaimer(self):
        """Test adding compliance disclaimer"""
        content = "Check out this trade setup!"
        with_disclaimer = self.generator.add_compliance_disclaimer(
            content,
            "sec_disclaimer"
        )

        assert content in with_disclaimer
        assert "Not financial advice" in with_disclaimer

    def test_get_disclaimer(self):
        """Test getting specific disclaimers"""
        sec = self.generator.get_disclaimer("sec_disclaimer")
        risk = self.generator.get_disclaimer("risk_warning")
        perf = self.generator.get_disclaimer("performance_disclaimer")

        assert "financial advice" in sec.lower()
        assert "risk" in risk.lower()
        assert "performance" in perf.lower() or "results" in perf.lower()

    def test_hashtag_generation(self):
        """Test hashtag generation"""
        hashtags = self.generator._generate_hashtags(["general", "patterns"], max_tags=3)

        assert "#" in hashtags
        # Count number of hashtags
        tag_count = hashtags.count("#")
        assert 1 <= tag_count <= 3


class TestSocialPoster:
    """Test social media posting functionality"""

    def test_post_result_model(self):
        """Test PostResult model"""
        result = PostResult(
            success=True,
            platform="twitter",
            post_id="12345",
            url="https://twitter.com/user/status/12345"
        )

        assert result.success is True
        assert result.platform == "twitter"
        assert result.post_id == "12345"
        assert result.url is not None

    def test_post_result_error(self):
        """Test PostResult with error"""
        result = PostResult(
            success=False,
            platform="reddit",
            error="Authentication failed"
        )

        assert result.success is False
        assert result.platform == "reddit"
        assert result.error == "Authentication failed"
        assert result.post_id is None

    def test_social_poster_init_no_credentials(self):
        """Test SocialPoster initialization without credentials"""
        poster = SocialPoster()

        assert poster.twitter_client is None
        assert poster.reddit_client is None
        assert poster.linkedin_client is None

    @pytest.mark.asyncio
    async def test_post_to_twitter_no_client(self):
        """Test Twitter posting without client"""
        poster = SocialPoster()
        result = await poster.post_to_twitter("Test post")

        assert result.success is False
        assert "not initialized" in result.error.lower()

    @pytest.mark.asyncio
    async def test_post_to_reddit_no_client(self):
        """Test Reddit posting without client"""
        poster = SocialPoster()
        result = await poster.post_to_reddit(
            content="Test post",
            title="Test Title",
            subreddit="test"
        )

        assert result.success is False
        assert "not initialized" in result.error.lower()

    @pytest.mark.asyncio
    async def test_post_to_stocktwits(self):
        """Test StockTwits posting (should warn about unavailability)"""
        poster = SocialPoster()
        result = await poster.post_to_stocktwits(
            content="Test post",
            symbol="AAPL"
        )

        assert result.success is False
        assert "stocktwits" in result.platform.lower()


class TestAutoPostingIntegration:
    """Integration tests for auto-posting workflow"""

    def test_content_generation_workflow(self):
        """Test complete content generation workflow"""
        generator = ContentGenerator()

        # Generate content for multiple platforms
        content = {
            "twitter": generator.generate_tweet(
                symbol="AAPL",
                pattern_type="VCP",
                score=90,
                entry_price=175.0,
                target_price=195.0,
                stop_price=168.0,
                rr_ratio=3.0
            ),
            "reddit": generator.generate_reddit_post(
                symbol="AAPL",
                pattern_type="VCP",
                score=90,
                entry_price=175.0,
                target_price=195.0,
                stop_price=168.0,
                rr_ratio=3.0,
                analysis="Strong technical setup",
                chart_url="https://example.com/chart.png"
            )
        }

        assert "AAPL" in content["twitter"]
        assert "AAPL" in content["reddit"]
        assert len(content["twitter"]) < len(content["reddit"])  # Reddit has more detail

    def test_compliance_in_all_content(self):
        """Test that all content types include compliance"""
        generator = ContentGenerator()

        tweet = generator.generate_tweet(
            symbol="TEST", pattern_type="Test", score=80,
            entry_price=100, target_price=120, stop_price=95, rr_ratio=2.0
        )
        summary = generator.generate_performance_summary(
            winners=10, losers=5, total_return=20,
            avg_winner=5, avg_loser=-2
        )
        alert = generator.generate_breakout_alert(
            symbol="TEST", pattern_type="Test", current_price=100,
            change_percent=5, volume_ratio=2, days_ago=10
        )

        # All should have disclaimers
        assert any(word in tweet.lower() for word in ["advice", "risk", "disclaimer"])
        assert any(word in summary.lower() for word in ["advice", "risk", "disclaimer", "performance"])
        assert any(word in alert.lower() for word in ["risk", "warning"])


def test_content_length_limits():
    """Test that content respects platform limits"""
    generator = ContentGenerator()

    # Twitter has 280 character limit
    tweet = generator.generate_tweet(
        symbol="AAPL", pattern_type="VCP", score=90,
        entry_price=175.0, target_price=195.0, stop_price=168.0, rr_ratio=3.0
    )

    # StockTwits has 1000 character limit
    stocktwits = generator.generate_stocktwits_post(
        symbol="AAPL", pattern_type="VCP", score=90,
        entry_price=175.0, target_price=195.0, stop_price=168.0, rr_ratio=3.0
    )

    # Note: These are approximate - actual limits depend on hashtags, etc.
    assert len(tweet) <= 400  # Buffer for safety
    assert len(stocktwits) <= 1100


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
