"""
Auto-posting scheduler service
Handles scheduled posts, analytics tracking, and community engagement
"""

import logging
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.models import (
    ScheduledPost, PostLog, PostAnalytics, CommunityEngagement,
    ComplianceLog, PatternScan
)
from app.services.content_generator import ContentGenerator
from app.services.social_poster import SocialPoster

logger = logging.getLogger(__name__)


class AutoPostingService:
    """Manage scheduled posts and auto-posting workflow"""

    def __init__(
        self,
        db: Session,
        content_generator: ContentGenerator,
        social_poster: SocialPoster
    ):
        """Initialize auto-posting service"""
        self.db = db
        self.content_generator = content_generator
        self.social_poster = social_poster
        self.scheduler = AsyncIOScheduler()

        # Configure best posting times (can be customized based on analytics)
        self.best_posting_times = {
            "twitter": ["09:00", "12:00", "16:00", "20:00"],  # ET
            "reddit": ["08:00", "13:00", "18:00"],
            "linkedin": ["07:00", "12:00", "17:00"],
            "stocktwits": ["09:30", "12:00", "15:30"]  # Market hours
        }

    def start_scheduler(self):
        """Start the posting scheduler"""
        # Check for pending posts every minute
        self.scheduler.add_job(
            self._process_pending_posts,
            trigger=IntervalTrigger(minutes=1),
            id="process_pending_posts",
            replace_existing=True
        )

        # Update analytics every hour
        self.scheduler.add_job(
            self._update_analytics,
            trigger=IntervalTrigger(hours=1),
            id="update_analytics",
            replace_existing=True
        )

        # Generate daily summary at 4 PM ET (after market close)
        self.scheduler.add_job(
            self._generate_daily_summary,
            trigger=CronTrigger(hour=16, minute=0),
            id="daily_summary",
            replace_existing=True
        )

        self.scheduler.start()
        logger.info("Auto-posting scheduler started")

    def stop_scheduler(self):
        """Stop the posting scheduler"""
        if self.scheduler.running:
            self.scheduler.shutdown()
            logger.info("Auto-posting scheduler stopped")

    async def schedule_pattern_post(
        self,
        pattern_scan_id: int,
        platforms: List[str],
        scheduled_time: Optional[datetime] = None,
        post_immediately: bool = False
    ) -> ScheduledPost:
        """Schedule a post for a detected pattern"""
        # Get pattern scan details
        pattern_scan = self.db.query(PatternScan).filter(
            PatternScan.id == pattern_scan_id
        ).first()

        if not pattern_scan:
            raise ValueError(f"Pattern scan {pattern_scan_id} not found")

        # Generate content for each platform
        content = {}
        if "twitter" in platforms:
            content["twitter"] = self.content_generator.generate_tweet(
                symbol=pattern_scan.ticker.symbol,
                pattern_type=pattern_scan.pattern_type,
                score=pattern_scan.score,
                entry_price=pattern_scan.entry_price,
                target_price=pattern_scan.target_price,
                stop_price=pattern_scan.stop_price,
                rr_ratio=pattern_scan.risk_reward_ratio
            )

        if "stocktwits" in platforms:
            content["stocktwits"] = self.content_generator.generate_stocktwits_post(
                symbol=pattern_scan.ticker.symbol,
                pattern_type=pattern_scan.pattern_type,
                score=pattern_scan.score,
                entry_price=pattern_scan.entry_price,
                target_price=pattern_scan.target_price,
                stop_price=pattern_scan.stop_price,
                rr_ratio=pattern_scan.risk_reward_ratio
            )

        if "linkedin" in platforms:
            content["linkedin"] = self.content_generator.generate_linkedin_post(
                symbol=pattern_scan.ticker.symbol,
                pattern_type=pattern_scan.pattern_type,
                score=pattern_scan.score,
                entry_price=pattern_scan.entry_price,
                target_price=pattern_scan.target_price,
                stop_price=pattern_scan.stop_price,
                rr_ratio=pattern_scan.risk_reward_ratio,
                consolidation_days=pattern_scan.consolidation_days or 0
            )

        if "reddit" in platforms:
            content["reddit"] = self.content_generator.generate_reddit_post(
                symbol=pattern_scan.ticker.symbol,
                pattern_type=pattern_scan.pattern_type,
                score=pattern_scan.score,
                entry_price=pattern_scan.entry_price,
                target_price=pattern_scan.target_price,
                stop_price=pattern_scan.stop_price,
                rr_ratio=pattern_scan.risk_reward_ratio,
                analysis=pattern_scan.analysis or "Strong technical setup",
                chart_url=pattern_scan.chart_url or ""
            )

        # Determine posting time
        if post_immediately:
            post_time = datetime.now()
        elif scheduled_time:
            post_time = scheduled_time
        else:
            # Schedule for next optimal posting time
            post_time = self._get_next_optimal_time(platforms[0])

        # Create scheduled post
        scheduled_post = ScheduledPost(
            content_type="pattern_detection",
            platforms=platforms,
            ticker_id=pattern_scan.ticker_id,
            pattern_scan_id=pattern_scan_id,
            title=f"{pattern_scan.pattern_type} - {pattern_scan.ticker.symbol}",
            content=str(content),  # Store as JSON string
            image_url=pattern_scan.chart_url,
            hashtags=["trading", "stockmarket", "technicalanalysis"],
            scheduled_time=post_time,
            status="pending" if not post_immediately else "posting",
            metadata={"symbol": pattern_scan.ticker.symbol}
        )

        self.db.add(scheduled_post)
        self.db.commit()

        # Post immediately if requested
        if post_immediately:
            await self._execute_post(scheduled_post.id)

        return scheduled_post

    async def _process_pending_posts(self):
        """Process all pending scheduled posts"""
        now = datetime.now()

        pending_posts = self.db.query(ScheduledPost).filter(
            ScheduledPost.status == "pending",
            ScheduledPost.scheduled_time <= now
        ).all()

        for post in pending_posts:
            try:
                await self._execute_post(post.id)
            except Exception as e:
                logger.error(f"Failed to execute post {post.id}: {e}")
                post.status = "failed"
                post.error_message = str(e)
                self.db.commit()

    async def _execute_post(self, scheduled_post_id: int):
        """Execute a scheduled post"""
        post = self.db.query(ScheduledPost).filter(
            ScheduledPost.id == scheduled_post_id
        ).first()

        if not post:
            logger.error(f"Scheduled post {scheduled_post_id} not found")
            return

        post.status = "posting"
        self.db.commit()

        try:
            # Parse content (stored as JSON string)
            import json
            content = json.loads(post.content) if isinstance(post.content, str) else post.content

            # Post to all platforms
            results = await self.social_poster.post_to_platforms(
                platforms=post.platforms,
                content=content,
                image_path=post.image_url,
                metadata=post.metadata
            )

            # Log results
            for result in results:
                post_log = PostLog(
                    scheduled_post_id=post.id,
                    platform=result.platform,
                    post_id=result.post_id,
                    content=content.get(result.platform, ""),
                    url=result.url,
                    status="success" if result.success else "failed",
                    error_message=result.error,
                    compliance_disclaimer=self.content_generator.get_disclaimer("sec_disclaimer")
                )
                self.db.add(post_log)

                # Log compliance
                if result.success:
                    compliance_log = ComplianceLog(
                        post_log_id=post_log.id,
                        compliance_type="sec_disclaimer",
                        disclaimer_text=self.content_generator.get_disclaimer("sec_disclaimer"),
                        platform=result.platform
                    )
                    self.db.add(compliance_log)

            # Update post status
            all_success = all(r.success for r in results)
            post.status = "posted" if all_success else "partial"
            post.posted_at = datetime.now()

            if not all_success:
                errors = [r.error for r in results if not r.success]
                post.error_message = "; ".join(errors)

            self.db.commit()
            logger.info(f"Successfully executed post {post.id}")

        except Exception as e:
            logger.error(f"Failed to execute post {post.id}: {e}")
            post.status = "failed"
            post.error_message = str(e)
            self.db.commit()

    async def _update_analytics(self):
        """Update analytics for recent posts"""
        # Get posts from last 7 days
        cutoff_date = datetime.now() - timedelta(days=7)

        recent_posts = self.db.query(PostLog).filter(
            PostLog.posted_at >= cutoff_date,
            PostLog.status == "success"
        ).all()

        for post_log in recent_posts:
            try:
                analytics_data = self.social_poster.get_post_analytics(
                    post_log.platform,
                    post_log.post_id
                )

                if analytics_data:
                    # Calculate engagement rate
                    impressions = analytics_data.get("impressions", 0)
                    engagement = analytics_data.get("likes", 0) + \
                                analytics_data.get("shares", 0) + \
                                analytics_data.get("comments", 0)
                    engagement_rate = (engagement / impressions * 100) if impressions > 0 else 0

                    # Get follower count
                    follower_count = self.social_poster.get_follower_count(post_log.platform)

                    # Create or update analytics record
                    analytics = PostAnalytics(
                        post_log_id=post_log.id,
                        platform=post_log.platform,
                        likes=analytics_data.get("likes", 0),
                        shares=analytics_data.get("retweets", 0) or analytics_data.get("shares", 0),
                        comments=analytics_data.get("replies", 0) or analytics_data.get("comments", 0),
                        impressions=impressions,
                        engagement_rate=engagement_rate,
                        follower_count=follower_count,
                        metadata=analytics_data
                    )
                    self.db.add(analytics)

                self.db.commit()

            except Exception as e:
                logger.error(f"Failed to update analytics for post {post_log.id}: {e}")

    async def _generate_daily_summary(self):
        """Generate and post daily market scan summary"""
        from app.models import UniverseScan

        # Get latest scan
        latest_scan = self.db.query(UniverseScan).order_by(
            desc(UniverseScan.scan_date)
        ).first()

        if not latest_scan:
            logger.warning("No scan data available for daily summary")
            return

        # Get top patterns from today
        today = datetime.now().date()
        top_patterns = self.db.query(PatternScan).filter(
            PatternScan.scanned_at >= today
        ).order_by(desc(PatternScan.score)).limit(5).all()

        top_setups = [
            {
                "symbol": p.ticker.symbol,
                "pattern": p.pattern_type,
                "score": p.score
            }
            for p in top_patterns
        ]

        # Generate summary content
        content = self.content_generator.generate_daily_summary(
            tickers_scanned=latest_scan.total_scanned,
            patterns_found=latest_scan.patterns_found,
            top_score=latest_scan.top_score or 0,
            scan_duration=latest_scan.duration_seconds,
            top_setups=top_setups,
            analysis_url="https://yourdomain.com/analysis"
        )

        # Schedule post for Twitter
        scheduled_post = ScheduledPost(
            content_type="daily_summary",
            platforms=["twitter"],
            title="Daily Market Scan",
            content=content,
            scheduled_time=datetime.now(),
            status="posting"
        )

        self.db.add(scheduled_post)
        self.db.commit()

        # Execute immediately
        await self._execute_post(scheduled_post.id)

    def _get_next_optimal_time(self, platform: str) -> datetime:
        """Get next optimal posting time for a platform"""
        now = datetime.now()
        times = self.best_posting_times.get(platform, ["12:00"])

        # Find next available time today or tomorrow
        for time_str in times:
            hour, minute = map(int, time_str.split(":"))
            post_time = now.replace(hour=hour, minute=minute, second=0, microsecond=0)

            if post_time > now:
                return post_time

        # If all times today have passed, use first time tomorrow
        hour, minute = map(int, times[0].split(":"))
        tomorrow = now + timedelta(days=1)
        return tomorrow.replace(hour=hour, minute=minute, second=0, microsecond=0)

    def get_analytics_summary(
        self,
        platform: Optional[str] = None,
        days: int = 7
    ) -> Dict[str, Any]:
        """Get analytics summary for posts"""
        cutoff_date = datetime.now() - timedelta(days=days)

        query = self.db.query(PostAnalytics).join(PostLog).filter(
            PostLog.posted_at >= cutoff_date
        )

        if platform:
            query = query.filter(PostAnalytics.platform == platform)

        analytics = query.all()

        if not analytics:
            return {
                "total_posts": 0,
                "total_engagement": 0,
                "avg_engagement_rate": 0,
                "follower_growth": 0
            }

        total_posts = len(analytics)
        total_likes = sum(a.likes for a in analytics)
        total_shares = sum(a.shares for a in analytics)
        total_comments = sum(a.comments for a in analytics)
        avg_engagement_rate = sum(a.engagement_rate for a in analytics) / total_posts

        # Calculate follower growth
        first_follower_count = analytics[0].follower_count or 0
        last_follower_count = analytics[-1].follower_count or 0
        follower_growth = last_follower_count - first_follower_count

        return {
            "total_posts": total_posts,
            "total_likes": total_likes,
            "total_shares": total_shares,
            "total_comments": total_comments,
            "total_engagement": total_likes + total_shares + total_comments,
            "avg_engagement_rate": round(avg_engagement_rate, 2),
            "follower_growth": follower_growth,
            "platform": platform or "all"
        }
