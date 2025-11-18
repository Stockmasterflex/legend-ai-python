"""
Multi-platform social media posting service
Supports Twitter/X, StockTwits, LinkedIn, and Reddit
"""

import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
import asyncio
from pydantic import BaseModel

logger = logging.getLogger(__name__)


class PostResult(BaseModel):
    """Result of a social media post"""
    success: bool
    platform: str
    post_id: Optional[str] = None
    url: Optional[str] = None
    error: Optional[str] = None
    timestamp: datetime = datetime.now()


class SocialPoster:
    """Multi-platform social media poster"""

    def __init__(
        self,
        twitter_credentials: Optional[Dict[str, str]] = None,
        reddit_credentials: Optional[Dict[str, str]] = None,
        linkedin_credentials: Optional[Dict[str, str]] = None,
        stocktwits_credentials: Optional[Dict[str, str]] = None
    ):
        """Initialize social poster with platform credentials"""
        self.twitter_credentials = twitter_credentials
        self.reddit_credentials = reddit_credentials
        self.linkedin_credentials = linkedin_credentials
        self.stocktwits_credentials = stocktwits_credentials

        self.twitter_client = None
        self.reddit_client = None
        self.linkedin_client = None
        self.stocktwits_client = None

        self._initialize_clients()

    def _initialize_clients(self):
        """Initialize platform API clients"""
        # Twitter/X
        if self.twitter_credentials:
            try:
                import tweepy
                auth = tweepy.OAuthHandler(
                    self.twitter_credentials.get("api_key"),
                    self.twitter_credentials.get("api_secret")
                )
                auth.set_access_token(
                    self.twitter_credentials.get("access_token"),
                    self.twitter_credentials.get("access_token_secret")
                )
                self.twitter_client = tweepy.API(auth)
                logger.info("Twitter client initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize Twitter client: {e}")

        # Reddit
        if self.reddit_credentials:
            try:
                import praw
                self.reddit_client = praw.Reddit(
                    client_id=self.reddit_credentials.get("client_id"),
                    client_secret=self.reddit_credentials.get("client_secret"),
                    user_agent=self.reddit_credentials.get("user_agent", "LegendAI Trading Bot v1.0"),
                    username=self.reddit_credentials.get("username"),
                    password=self.reddit_credentials.get("password")
                )
                logger.info("Reddit client initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize Reddit client: {e}")

        # LinkedIn (using linkedin-api)
        if self.linkedin_credentials:
            try:
                from linkedin_api import Linkedin
                self.linkedin_client = Linkedin(
                    self.linkedin_credentials.get("username"),
                    self.linkedin_credentials.get("password")
                )
                logger.info("LinkedIn client initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize LinkedIn client: {e}")

    async def post_to_twitter(
        self,
        content: str,
        image_path: Optional[str] = None,
        hashtags: Optional[List[str]] = None
    ) -> PostResult:
        """Post content to Twitter/X"""
        if not self.twitter_client:
            return PostResult(
                success=False,
                platform="twitter",
                error="Twitter client not initialized"
            )

        try:
            # Add hashtags if provided
            if hashtags:
                content = f"{content}\n\n{' '.join([f'#{tag}' for tag in hashtags])}"

            # Post with or without image
            if image_path:
                media = self.twitter_client.media_upload(image_path)
                tweet = self.twitter_client.update_status(
                    status=content,
                    media_ids=[media.media_id]
                )
            else:
                tweet = self.twitter_client.update_status(status=content)

            return PostResult(
                success=True,
                platform="twitter",
                post_id=str(tweet.id),
                url=f"https://twitter.com/user/status/{tweet.id}"
            )

        except Exception as e:
            logger.error(f"Failed to post to Twitter: {e}")
            return PostResult(
                success=False,
                platform="twitter",
                error=str(e)
            )

    async def post_to_stocktwits(
        self,
        content: str,
        symbol: str,
        sentiment: str = "bullish"
    ) -> PostResult:
        """Post content to StockTwits"""
        # StockTwits doesn't have an official public API for posting
        # This would require using their web interface or unofficial methods
        # For now, we'll return a placeholder
        logger.warning("StockTwits posting requires manual implementation or web scraping")
        return PostResult(
            success=False,
            platform="stocktwits",
            error="StockTwits API not available - manual posting required"
        )

    async def post_to_reddit(
        self,
        content: str,
        title: str,
        subreddit: str = "algotrading",
        flair: Optional[str] = None
    ) -> PostResult:
        """Post content to Reddit"""
        if not self.reddit_client:
            return PostResult(
                success=False,
                platform="reddit",
                error="Reddit client not initialized"
            )

        try:
            subreddit_obj = self.reddit_client.subreddit(subreddit)
            submission = subreddit_obj.submit(title=title, selftext=content, flair_id=flair)

            return PostResult(
                success=True,
                platform="reddit",
                post_id=submission.id,
                url=f"https://reddit.com{submission.permalink}"
            )

        except Exception as e:
            logger.error(f"Failed to post to Reddit: {e}")
            return PostResult(
                success=False,
                platform="reddit",
                error=str(e)
            )

    async def post_to_linkedin(
        self,
        content: str,
        image_path: Optional[str] = None
    ) -> PostResult:
        """Post content to LinkedIn"""
        if not self.linkedin_client:
            return PostResult(
                success=False,
                platform="linkedin",
                error="LinkedIn client not initialized"
            )

        try:
            # LinkedIn API posting is complex and may require additional setup
            # This is a simplified version
            logger.warning("LinkedIn posting requires additional implementation")
            return PostResult(
                success=False,
                platform="linkedin",
                error="LinkedIn API posting requires additional setup"
            )

        except Exception as e:
            logger.error(f"Failed to post to LinkedIn: {e}")
            return PostResult(
                success=False,
                platform="linkedin",
                error=str(e)
            )

    async def post_to_platforms(
        self,
        platforms: List[str],
        content: Dict[str, str],
        image_path: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> List[PostResult]:
        """Post content to multiple platforms simultaneously"""
        tasks = []

        for platform in platforms:
            platform_content = content.get(platform, content.get("default", ""))

            if platform == "twitter":
                tasks.append(self.post_to_twitter(
                    platform_content,
                    image_path,
                    metadata.get("hashtags") if metadata else None
                ))
            elif platform == "reddit":
                tasks.append(self.post_to_reddit(
                    platform_content,
                    metadata.get("title", "Trading Analysis") if metadata else "Trading Analysis",
                    metadata.get("subreddit", "algotrading") if metadata else "algotrading"
                ))
            elif platform == "linkedin":
                tasks.append(self.post_to_linkedin(platform_content, image_path))
            elif platform == "stocktwits":
                tasks.append(self.post_to_stocktwits(
                    platform_content,
                    metadata.get("symbol", "") if metadata else ""
                ))

        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Convert any exceptions to PostResults
        final_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                final_results.append(PostResult(
                    success=False,
                    platform=platforms[i],
                    error=str(result)
                ))
            else:
                final_results.append(result)

        return final_results

    async def delete_post(self, platform: str, post_id: str) -> bool:
        """Delete a post from a platform"""
        try:
            if platform == "twitter" and self.twitter_client:
                self.twitter_client.destroy_status(post_id)
                return True
            elif platform == "reddit" and self.reddit_client:
                submission = self.reddit_client.submission(id=post_id)
                submission.delete()
                return True
            else:
                logger.warning(f"Delete not supported for platform: {platform}")
                return False
        except Exception as e:
            logger.error(f"Failed to delete post from {platform}: {e}")
            return False

    def get_post_analytics(self, platform: str, post_id: str) -> Optional[Dict[str, Any]]:
        """Get analytics for a specific post"""
        try:
            if platform == "twitter" and self.twitter_client:
                tweet = self.twitter_client.get_status(post_id)
                return {
                    "likes": tweet.favorite_count,
                    "retweets": tweet.retweet_count,
                    "replies": tweet.reply_count if hasattr(tweet, 'reply_count') else 0,
                    "impressions": tweet.impressions if hasattr(tweet, 'impressions') else 0
                }
            elif platform == "reddit" and self.reddit_client:
                submission = self.reddit_client.submission(id=post_id)
                return {
                    "score": submission.score,
                    "upvote_ratio": submission.upvote_ratio,
                    "num_comments": submission.num_comments,
                    "views": submission.view_count if hasattr(submission, 'view_count') else 0
                }
            else:
                logger.warning(f"Analytics not supported for platform: {platform}")
                return None
        except Exception as e:
            logger.error(f"Failed to get analytics from {platform}: {e}")
            return None

    def get_follower_count(self, platform: str) -> Optional[int]:
        """Get current follower count for a platform"""
        try:
            if platform == "twitter" and self.twitter_client:
                user = self.twitter_client.verify_credentials()
                return user.followers_count
            elif platform == "reddit" and self.reddit_client:
                # Reddit uses karma instead of followers
                user = self.reddit_client.user.me()
                return user.link_karma + user.comment_karma
            else:
                logger.warning(f"Follower count not supported for platform: {platform}")
                return None
        except Exception as e:
            logger.error(f"Failed to get follower count from {platform}: {e}")
            return None
