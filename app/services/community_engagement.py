"""
Community engagement automation service
Handles auto-replies, follow-backs, DMs, and community building
"""

import logging
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
import re

from app.models import CommunityEngagement

logger = logging.getLogger(__name__)


class CommunityEngagementService:
    """Automate community engagement across platforms"""

    def __init__(self, db: Session, social_poster):
        """Initialize community engagement service"""
        self.db = db
        self.social_poster = social_poster

        # Auto-reply templates
        self.reply_templates = {
            "thanks": [
                "Thanks for the feedback! 🙏",
                "Appreciate it! 📊",
                "Thanks! Let me know if you have questions. 💡"
            ],
            "question": [
                "Great question! {response}",
                "Good point. {response}",
                "Let me clarify: {response}"
            ],
            "setup_share": [
                "Nice setup! What's your entry/target? 📈",
                "Love this! Are you in the trade? 💰",
                "Good eye! What made you spot this? 🔍"
            ],
            "disagreement": [
                "I see your point. Different perspectives make better traders! 📊",
                "Valid concern. Always good to consider multiple angles. 💡",
                "Fair point. Risk management is key! ⚠️"
            ]
        }

        # DM templates
        self.dm_templates = {
            "welcome_follower": """Hey {username}! 👋

Thanks for following! I share daily technical analysis and trading setups based on Mark Minervini's methodology.

Let me know if you have any questions about the patterns or setups I post!

Happy trading! 📈""",

            "response_inquiry": """Hi {username},

Thanks for reaching out! {custom_response}

Feel free to ask any questions about trading setups or technical analysis.

Best,
Legend AI""",

            "setup_request": """Hi {username},

I'd be happy to analyze {symbol} for you! I'll add it to my watchlist and share my analysis in the next scan.

Keep an eye on my feed! 📊"""
        }

        # Engagement rules
        self.engagement_rules = {
            "auto_reply_to_mentions": True,
            "auto_reply_to_comments": True,
            "auto_follow_back": True,
            "auto_dm_new_followers": False,  # Can be spammy, disabled by default
            "auto_like_mentions": True,
            "auto_share_top_setups": True,
            "min_follower_count_for_reply": 10,  # Avoid spam accounts
            "max_replies_per_hour": 10,  # Rate limiting
            "max_dms_per_day": 20
        }

    async def process_mentions(self, platform: str, limit: int = 50):
        """Process and respond to mentions"""
        if not self.engagement_rules["auto_reply_to_mentions"]:
            return

        try:
            mentions = await self._get_mentions(platform, limit)

            for mention in mentions:
                # Check if we've already replied
                if await self._has_replied_to(platform, mention["id"]):
                    continue

                # Classify mention type and generate response
                mention_type = self._classify_mention(mention["text"])
                response = self._generate_reply(mention_type, mention)

                if response:
                    # Create engagement record
                    engagement = CommunityEngagement(
                        platform=platform,
                        engagement_type="reply",
                        target_user=mention["username"],
                        target_post_id=mention["id"],
                        content=response,
                        status="pending"
                    )
                    self.db.add(engagement)
                    self.db.commit()

                    # Execute reply
                    await self._execute_reply(engagement.id)

        except Exception as e:
            logger.error(f"Failed to process mentions on {platform}: {e}")

    async def process_new_followers(self, platform: str):
        """Process new followers and optionally follow back"""
        if not self.engagement_rules["auto_follow_back"]:
            return

        try:
            new_followers = await self._get_new_followers(platform)

            for follower in new_followers:
                # Check follower quality (avoid spam accounts)
                if not self._is_quality_follower(follower):
                    continue

                # Follow back
                engagement = CommunityEngagement(
                    platform=platform,
                    engagement_type="follow",
                    target_user=follower["username"],
                    status="pending"
                )
                self.db.add(engagement)
                self.db.commit()

                await self._execute_follow(engagement.id)

                # Optionally send welcome DM
                if self.engagement_rules["auto_dm_new_followers"]:
                    await self._send_welcome_dm(platform, follower["username"])

        except Exception as e:
            logger.error(f"Failed to process new followers on {platform}: {e}")

    async def share_community_setup(
        self,
        platform: str,
        original_post_id: str,
        comment: Optional[str] = None
    ):
        """Share a community member's trading setup"""
        try:
            if platform == "twitter" and self.social_poster.twitter_client:
                # Retweet with comment
                if comment:
                    self.social_poster.twitter_client.update_status(
                        status=comment,
                        attachment_url=f"https://twitter.com/user/status/{original_post_id}"
                    )
                else:
                    self.social_poster.twitter_client.retweet(original_post_id)

                logger.info(f"Shared community setup: {original_post_id}")
                return True

        except Exception as e:
            logger.error(f"Failed to share community setup: {e}")
            return False

    async def _get_mentions(self, platform: str, limit: int = 50) -> List[Dict[str, Any]]:
        """Get recent mentions from a platform"""
        mentions = []

        try:
            if platform == "twitter" and self.social_poster.twitter_client:
                api_mentions = self.social_poster.twitter_client.mentions_timeline(count=limit)
                for mention in api_mentions:
                    mentions.append({
                        "id": str(mention.id),
                        "username": mention.user.screen_name,
                        "text": mention.text,
                        "created_at": mention.created_at,
                        "user_followers": mention.user.followers_count
                    })

            elif platform == "reddit" and self.social_poster.reddit_client:
                user = self.social_poster.reddit_client.user.me()
                for item in user.inbox.mentions(limit=limit):
                    mentions.append({
                        "id": item.id,
                        "username": item.author.name if item.author else "[deleted]",
                        "text": item.body,
                        "created_at": datetime.fromtimestamp(item.created_utc),
                        "user_followers": 0  # Reddit doesn't have followers concept
                    })

        except Exception as e:
            logger.error(f"Failed to get mentions from {platform}: {e}")

        return mentions

    async def _get_new_followers(self, platform: str, since_hours: int = 24) -> List[Dict[str, Any]]:
        """Get new followers from the last N hours"""
        followers = []

        try:
            if platform == "twitter" and self.social_poster.twitter_client:
                # Twitter API v1.1 doesn't have a good way to get recent followers
                # This would require API v2 or storing follower IDs
                logger.warning("Getting recent followers requires Twitter API v2")

        except Exception as e:
            logger.error(f"Failed to get new followers from {platform}: {e}")

        return followers

    def _classify_mention(self, text: str) -> str:
        """Classify the type of mention"""
        text_lower = text.lower()

        # Question keywords
        if any(word in text_lower for word in ["?", "how", "what", "when", "why", "which"]):
            return "question"

        # Thanks/appreciation
        if any(word in text_lower for word in ["thanks", "thank you", "appreciate", "great", "awesome"]):
            return "thanks"

        # Setup sharing
        if any(word in text_lower for word in ["setup", "entry", "target", "chart"]):
            return "setup_share"

        # Disagreement/critique
        if any(word in text_lower for word in ["disagree", "wrong", "but", "however"]):
            return "disagreement"

        return "general"

    def _generate_reply(self, mention_type: str, mention: Dict[str, Any]) -> Optional[str]:
        """Generate a reply based on mention type"""
        import random

        templates = self.reply_templates.get(mention_type)
        if not templates:
            return None

        # Select random template
        template = random.choice(templates)

        # For questions, add a generic helpful response
        if mention_type == "question":
            response = "Check out my recent posts for examples and explanations. DM me if you need specific guidance!"
            return template.format(response=response)

        return template

    async def _execute_reply(self, engagement_id: int):
        """Execute a reply to a mention or comment"""
        engagement = self.db.query(CommunityEngagement).filter(
            CommunityEngagement.id == engagement_id
        ).first()

        if not engagement:
            return

        try:
            if engagement.platform == "twitter" and self.social_poster.twitter_client:
                self.social_poster.twitter_client.update_status(
                    status=f"@{engagement.target_user} {engagement.content}",
                    in_reply_to_status_id=engagement.target_post_id
                )

            elif engagement.platform == "reddit" and self.social_poster.reddit_client:
                comment = self.social_poster.reddit_client.comment(id=engagement.target_post_id)
                comment.reply(engagement.content)

            engagement.status = "completed"
            engagement.executed_at = datetime.now()
            logger.info(f"Executed reply for engagement {engagement_id}")

        except Exception as e:
            logger.error(f"Failed to execute reply {engagement_id}: {e}")
            engagement.status = "failed"
            engagement.error_message = str(e)

        self.db.commit()

    async def _execute_follow(self, engagement_id: int):
        """Execute a follow action"""
        engagement = self.db.query(CommunityEngagement).filter(
            CommunityEngagement.id == engagement_id
        ).first()

        if not engagement:
            return

        try:
            if engagement.platform == "twitter" and self.social_poster.twitter_client:
                self.social_poster.twitter_client.create_friendship(screen_name=engagement.target_user)

            engagement.status = "completed"
            engagement.executed_at = datetime.now()
            logger.info(f"Followed user: {engagement.target_user}")

        except Exception as e:
            logger.error(f"Failed to follow {engagement.target_user}: {e}")
            engagement.status = "failed"
            engagement.error_message = str(e)

        self.db.commit()

    async def _send_welcome_dm(self, platform: str, username: str):
        """Send welcome DM to new follower"""
        try:
            message = self.dm_templates["welcome_follower"].format(username=username)

            engagement = CommunityEngagement(
                platform=platform,
                engagement_type="dm",
                target_user=username,
                content=message,
                status="pending"
            )
            self.db.add(engagement)
            self.db.commit()

            # Execute DM
            if platform == "twitter" and self.social_poster.twitter_client:
                self.social_poster.twitter_client.send_direct_message(
                    screen_name=username,
                    text=message
                )
                engagement.status = "completed"
                engagement.executed_at = datetime.now()

            self.db.commit()

        except Exception as e:
            logger.error(f"Failed to send welcome DM to {username}: {e}")

    def _is_quality_follower(self, follower: Dict[str, Any]) -> bool:
        """Check if follower meets quality criteria"""
        # Avoid spam accounts
        min_followers = self.engagement_rules["min_follower_count_for_reply"]

        follower_count = follower.get("follower_count", 0)
        following_count = follower.get("following_count", 0)

        # Check for suspicious ratios (following >> followers could be spam)
        if following_count > 0:
            ratio = follower_count / following_count
            if ratio < 0.1 and follower_count < 100:  # Likely spam
                return False

        return follower_count >= min_followers

    async def _has_replied_to(self, platform: str, post_id: str) -> bool:
        """Check if we've already replied to a post"""
        existing = self.db.query(CommunityEngagement).filter(
            CommunityEngagement.platform == platform,
            CommunityEngagement.target_post_id == post_id,
            CommunityEngagement.engagement_type == "reply"
        ).first()

        return existing is not None

    def get_engagement_stats(self, days: int = 7) -> Dict[str, Any]:
        """Get engagement statistics"""
        cutoff_date = datetime.now() - timedelta(days=days)

        engagements = self.db.query(CommunityEngagement).filter(
            CommunityEngagement.created_at >= cutoff_date
        ).all()

        stats = {
            "total_engagements": len(engagements),
            "replies": sum(1 for e in engagements if e.engagement_type == "reply"),
            "follows": sum(1 for e in engagements if e.engagement_type == "follow"),
            "dms": sum(1 for e in engagements if e.engagement_type == "dm"),
            "completed": sum(1 for e in engagements if e.status == "completed"),
            "failed": sum(1 for e in engagements if e.status == "failed"),
            "pending": sum(1 for e in engagements if e.status == "pending")
        }

        return stats
