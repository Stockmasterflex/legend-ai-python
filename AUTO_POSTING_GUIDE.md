# Auto-Posting Trading Analysis Guide

## Overview

The auto-posting feature enables automated social media posting of trading analysis, pattern detections, and performance summaries across multiple platforms including Twitter/X, Reddit, LinkedIn, and StockTwits.

## Features

### 1. Content Generation
- **Auto-generate tweets** with pattern details, entry/target/stop prices
- **Chart annotations** with technical analysis markup
- **Performance summaries** tracking wins, losses, and returns
- **Pattern explanations** for educational content
- **Breakout alerts** for real-time trade setups
- **Daily summaries** of market scans

### 2. Multi-Platform Posting
- **Twitter/X**: Short-form updates with hashtags
- **StockTwits**: Symbol-focused trading content
- **LinkedIn**: Professional technical analysis posts
- **Reddit**: Discussion-style posts for trading communities

### 3. Engagement Analytics
- Track likes, shares, comments, and impressions
- Monitor follower growth over time
- Identify best posting times by platform
- Calculate engagement rates
- Platform-specific metrics

### 4. Community Building
- **Auto-reply** to mentions and comments
- **Auto-follow** quality followers
- **Share community setups** from other traders
- **DM automation** for new followers (optional)
- Smart filtering to avoid spam accounts

### 5. Compliance
- **Automatic disclaimers** on all posts (SEC, risk warnings)
- **Performance disclaimers** for results
- **Compliance logging** for audit trail
- **Manual verification** flags

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Social Media Credentials

Add to your `.env` file:

```bash
# Enable auto-posting
AUTO_POSTING_ENABLED=true
AUTO_POSTING_PLATFORMS=twitter,reddit
AUTO_POSTING_MIN_SCORE=75.0

# Twitter/X API (from developer.twitter.com)
TWITTER_API_KEY=your-api-key
TWITTER_API_SECRET=your-api-secret
TWITTER_ACCESS_TOKEN=your-access-token
TWITTER_ACCESS_TOKEN_SECRET=your-access-token-secret

# Reddit API (from reddit.com/prefs/apps)
REDDIT_CLIENT_ID=your-client-id
REDDIT_CLIENT_SECRET=your-client-secret
REDDIT_USERNAME=your-username
REDDIT_PASSWORD=your-password

# LinkedIn (Note: API access restricted)
LINKEDIN_USERNAME=your-email
LINKEDIN_PASSWORD=your-password
```

### 3. Run Database Migrations

```bash
alembic upgrade head
```

### 4. Start the Scheduler

The auto-posting scheduler starts automatically with the main application. It runs:
- Post processing every minute
- Analytics updates every hour
- Daily summary at 4 PM ET

## API Endpoints

### Schedule a Post

```bash
POST /api/v1/auto-posting/schedule
```

**Request:**
```json
{
  "pattern_scan_id": 123,
  "platforms": ["twitter", "reddit"],
  "scheduled_time": "2025-11-18T14:00:00Z",
  "post_immediately": false
}
```

**Response:**
```json
{
  "id": 1,
  "status": "pending",
  "scheduled_time": "2025-11-18T14:00:00Z",
  "platforms": ["twitter", "reddit"],
  "content_type": "pattern_detection"
}
```

### Get Scheduled Posts

```bash
GET /api/v1/auto-posting/scheduled?status=pending&limit=50
```

### Get Analytics Summary

```bash
GET /api/v1/auto-posting/analytics/summary?platform=twitter&days=7
```

**Response:**
```json
{
  "total_posts": 42,
  "total_likes": 1250,
  "total_shares": 320,
  "total_comments": 180,
  "total_engagement": 1750,
  "avg_engagement_rate": 3.2,
  "follower_growth": 85,
  "platform": "twitter"
}
```

### Get Best Posting Times

```bash
GET /api/v1/auto-posting/analytics/best-times?platform=twitter
```

**Response:**
```json
{
  "platform": "twitter",
  "best_posting_hours": [
    {"hour": 12, "avg_engagement_rate": 4.5},
    {"hour": 16, "avg_engagement_rate": 4.2},
    {"hour": 9, "avg_engagement_rate": 3.8}
  ]
}
```

### Process Mentions

```bash
POST /api/v1/auto-posting/engagement/process-mentions?platform=twitter&limit=50
```

### Get Engagement Stats

```bash
GET /api/v1/auto-posting/engagement/stats?days=7
```

## Usage Examples

### 1. Auto-Post a Pattern Detection

```python
from app.services.auto_posting import AutoPostingService
from app.services.content_generator import ContentGenerator
from app.services.social_poster import SocialPoster

# Initialize services
content_generator = ContentGenerator()
social_poster = SocialPoster(twitter_credentials=credentials)
auto_posting = AutoPostingService(db, content_generator, social_poster)

# Schedule post
scheduled_post = await auto_posting.schedule_pattern_post(
    pattern_scan_id=123,
    platforms=["twitter", "reddit"],
    post_immediately=True
)
```

### 2. Generate Custom Content

```python
from app.services.content_generator import ContentGenerator

generator = ContentGenerator()

# Generate a tweet
tweet = generator.generate_tweet(
    symbol="AAPL",
    pattern_type="VCP",
    score=92.5,
    entry_price=175.50,
    target_price=195.00,
    stop_price=168.00,
    rr_ratio=3.2
)

print(tweet)
# Output:
# 🚀 VCP pattern detected in $AAPL!
# 📊 Score: 93/100
# 💰 Entry: $175.50
# 🎯 Target: $195.00 (11.1% upside)
# 🛑 Stop: $168.00
# 📈 R/R Ratio: 3.2
# Not financial advice. For educational purposes only. Trade at your own risk.
# #trading #stockmarket #technicalanalysis
```

### 3. Track Analytics

```python
# Get analytics summary
summary = auto_posting.get_analytics_summary(platform="twitter", days=30)

print(f"Total Posts: {summary['total_posts']}")
print(f"Engagement Rate: {summary['avg_engagement_rate']}%")
print(f"Follower Growth: {summary['follower_growth']}")
```

## Content Templates

### Tweet Pattern
```
🚀 {{ pattern_type }} pattern detected in ${{ symbol }}!

📊 Score: {{ score }}/100
💰 Entry: ${{ entry_price }}
🎯 Target: ${{ target_price }} ({{ upside }}% upside)
🛑 Stop: ${{ stop_price }}
📈 R/R Ratio: {{ rr_ratio }}

{{ disclaimer }}
{{ hashtags }}
```

### Daily Summary
```
📊 Daily Market Scan Results

🔍 Scanned: {{ tickers_scanned }} stocks
🎯 Patterns Found: {{ patterns_found }}
⭐ Top Score: {{ top_score }}/100

Top Setups:
• $AAPL: VCP (92/100)
• $MSFT: Cup & Handle (88/100)
• $NVDA: Breakout (85/100)

{{ hashtags }}
```

## Best Practices

### 1. Posting Schedule
- **Twitter**: 9 AM, 12 PM, 4 PM, 8 PM ET
- **Reddit**: 8 AM, 1 PM, 6 PM ET
- **LinkedIn**: 7 AM, 12 PM, 5 PM ET
- **StockTwits**: 9:30 AM, 12 PM, 3:30 PM ET (market hours)

### 2. Content Strategy
- Mix educational content (40%) with trade setups (60%)
- Include disclaimers on all trading advice
- Use relevant hashtags (3-5 per post)
- Add charts/images when possible
- Engage with community responses

### 3. Engagement Rules
- Auto-reply to genuine questions
- Follow back quality accounts (>50 followers)
- Share community setups that meet criteria
- Limit automated actions to avoid spam flags
- Manual review of DMs recommended

### 4. Compliance
- Always include SEC disclaimers
- Add risk warnings on performance posts
- Log all compliance actions
- Regular compliance audits
- Never guarantee returns

## Rate Limits

### Twitter
- 300 tweets per 3 hours
- 1000 DMs per day
- 400 follows per day

### Reddit
- 1 post per 10 minutes
- 100 comments per day
- Follow subreddit rules

### LinkedIn
- 100 posts per day
- Limited API access

## Troubleshooting

### Posts Not Sending
1. Check credentials in `.env`
2. Verify API access/rate limits
3. Check scheduler is running: `GET /api/v1/auto-posting/health`
4. Review error logs in database

### Low Engagement
1. Analyze best posting times
2. Review content quality
3. Increase hashtag usage
4. Add more images/charts
5. Engage with community more

### Compliance Issues
1. Always include disclaimers
2. Never guarantee returns
3. Clearly mark as educational
4. Follow platform guidelines
5. Maintain audit logs

## Monitoring

### Health Check
```bash
GET /api/v1/auto-posting/health
```

### Key Metrics
- Pending posts count
- Posts last 24 hours
- Failed post rate
- Average engagement rate
- Follower growth rate

## Security

### API Credentials
- Store in environment variables
- Never commit to git
- Use separate accounts for testing
- Rotate credentials regularly
- Monitor for unauthorized access

### Data Privacy
- Don't share user data
- Follow platform privacy policies
- Comply with GDPR if applicable
- Secure API endpoints
- Regular security audits

## Future Enhancements

- [ ] Instagram integration
- [ ] Discord community bot
- [ ] Advanced sentiment analysis
- [ ] AI-powered reply generation
- [ ] A/B testing for content
- [ ] Video/GIF support
- [ ] Cross-platform analytics dashboard
- [ ] Automated performance reporting
- [ ] Community trading competitions
- [ ] NFT badge rewards for top contributors

## Support

For issues or questions:
- GitHub Issues: [github.com/yourrepo/issues](https://github.com/yourrepo/issues)
- Documentation: [docs.yourdomain.com](https://docs.yourdomain.com)
- Email: support@yourdomain.com

## License

This feature is part of Legend AI and follows the same license terms.
