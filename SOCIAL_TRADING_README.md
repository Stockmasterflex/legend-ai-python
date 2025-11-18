# 👥 Social Trading Community

A comprehensive social trading platform that enables users to share trade ideas, follow successful traders, engage in discussions, and track community performance through leaderboards and analytics.

## 🌟 Features

### 1. User Profiles & Following
- **Public Trading Profiles**: Showcase your trading performance, win rate, and total returns
- **Follow Successful Traders**: Follow top performers and get notified of their trades
- **Copy Trading**: Automatically replicate trades from traders you follow
- **Leaderboards**: Compete and compare performance with the community

### 2. Trade Sharing
- **Post Trade Ideas**: Share your trade setups, entry points, and strategies
- **Chart Annotations**: Attach annotated charts to your posts
- **Trade Plans**: Include detailed trade plans with entry, stop, and target prices
- **Success/Fail Updates**: Update your community on trade outcomes

### 3. Community Features
- **Comments & Discussions**: Engage in threaded discussions on trade posts
- **Reactions**: React to posts with likes, bullish/bearish sentiment
- **Pattern Debates**: Discuss pattern validity and setups
- **Tips & Tricks**: Share trading wisdom with the community

### 4. Social Analytics
- **Most-Followed Tickers**: See what the community is watching
- **Crowd Sentiment**: Gauge bullish/bearish sentiment on any ticker
- **Popular Patterns**: Discover which patterns are trending
- **Trending Strategies**: Learn what strategies are working

## 📚 API Documentation

### Authentication

#### Register a New User
```bash
POST /api/social/auth/register
Content-Type: application/json

{
  "username": "trader123",
  "email": "trader@example.com",
  "password": "secure_password123",
  "full_name": "John Trader"
}
```

#### Login
```bash
POST /api/social/auth/login
Content-Type: application/json

{
  "username": "trader123",
  "password": "secure_password123"
}

Response:
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

#### Get Current User Profile
```bash
GET /api/social/auth/me
Authorization: Bearer {access_token}
```

### User Profiles

#### Get User Profile
```bash
GET /api/social/users/{username}
```

#### Update Profile
```bash
PUT /api/social/profile
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "bio": "Swing trader focused on VCP patterns",
  "trading_since": "2020-01-01T00:00:00Z",
  "preferred_strategies": ["VCP", "Cup & Handle"],
  "preferred_tickers": ["AAPL", "TSLA", "NVDA"],
  "is_public": true,
  "show_stats": true,
  "allow_copy_trading": true
}
```

### Following System

#### Follow a User
```bash
POST /api/social/follow
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "following_id": 123,
  "copy_trading_enabled": true,
  "copy_percentage": 10.0,
  "max_position_size": 5000.0
}
```

#### Unfollow a User
```bash
DELETE /api/social/follow/{user_id}
Authorization: Bearer {access_token}
```

#### Get Following List
```bash
GET /api/social/following
Authorization: Bearer {access_token}
```

#### Get Followers List
```bash
GET /api/social/followers
Authorization: Bearer {access_token}
```

### Trade Posts

#### Create Trade Post
```bash
POST /api/social/posts
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "title": "AAPL VCP Setup - Potential Breakout",
  "content": "Apple showing a tight VCP pattern with volume contraction. Entry at $175, stop at $170, target $190.",
  "ticker_symbol": "AAPL",
  "post_type": "idea",
  "entry_price": 175.0,
  "stop_price": 170.0,
  "target_price": 190.0,
  "pattern_type": "VCP",
  "is_public": true
}
```

#### Get Trade Posts (with filtering)
```bash
GET /api/social/posts?page=1&page_size=20&post_type=idea&ticker_symbol=AAPL
```

Query Parameters:
- `page`: Page number (default: 1)
- `page_size`: Items per page (default: 20, max: 100)
- `post_type`: Filter by type (idea, entry, exit, update, analysis)
- `ticker_symbol`: Filter by ticker
- `username`: Filter by author
- `following_only`: Show only posts from followed users (true/false)

#### Get Single Trade Post
```bash
GET /api/social/posts/{post_id}
```

#### Update Trade Post
```bash
PUT /api/social/posts/{post_id}
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "exit_price": 188.0,
  "profit_loss": 13.0,
  "profit_loss_percent": 7.4,
  "trade_status": "closed"
}
```

#### Delete Trade Post
```bash
DELETE /api/social/posts/{post_id}
Authorization: Bearer {access_token}
```

### Comments

#### Add Comment
```bash
POST /api/social/posts/{post_id}/comments
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "content": "Great setup! I'm watching this one too.",
  "parent_comment_id": null
}
```

#### Get Comments
```bash
GET /api/social/posts/{post_id}/comments
```

#### Update Comment
```bash
PUT /api/social/comments/{comment_id}
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "content": "Updated comment text"
}
```

#### Delete Comment
```bash
DELETE /api/social/comments/{comment_id}
Authorization: Bearer {access_token}
```

### Reactions

#### Add Reaction to Post
```bash
POST /api/social/posts/{post_id}/reactions
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "reaction_type": "bullish"
}
```

Reaction types: `like`, `bullish`, `bearish`, `fire`

#### Remove Reaction
```bash
DELETE /api/social/posts/{post_id}/reactions
Authorization: Bearer {access_token}
```

### Leaderboards

#### Get Leaderboard
```bash
GET /api/social/leaderboard?period=all_time&limit=50
```

Query Parameters:
- `period`: Time period (all_time, monthly, weekly)
- `limit`: Number of entries (default: 50, max: 100)

### Social Analytics

#### Get Trending Tickers
```bash
GET /api/social/analytics/trending-tickers?time_window=24h&limit=10
```

Query Parameters:
- `time_window`: Time window (1h, 24h, 7d, 30d)
- `limit`: Number of results (default: 10, max: 50)

#### Get Trending Patterns
```bash
GET /api/social/analytics/trending-patterns?time_window=7d&limit=10
```

#### Get Community Stats
```bash
GET /api/social/analytics/community-stats
```

#### Get Crowd Sentiment for Ticker
```bash
GET /api/social/analytics/sentiment/{ticker_symbol}
```

Example response:
```json
{
  "ticker_symbol": "AAPL",
  "total_mentions": 45,
  "bullish_count": 30,
  "bearish_count": 10,
  "neutral_count": 5,
  "sentiment_score": 44.4,
  "avg_target_price": 185.5,
  "most_common_pattern": "VCP"
}
```

## 🗄️ Database Schema

### Core Tables

1. **users** - User accounts
   - id, username, email, hashed_password, full_name
   - is_active, is_verified, created_at, updated_at, last_login

2. **user_profiles** - Public trading profiles
   - User stats, bio, avatar, trading preferences
   - Performance metrics (win_rate, avg_return, total_trades)
   - Privacy settings

3. **follows** - Following relationships
   - follower_id, following_id
   - copy_trading settings (enabled, percentage, max_position_size)

4. **trade_posts** - Trade ideas and updates
   - Post content, ticker, trade details
   - Entry, stop, target prices
   - Pattern type, chart annotations
   - Engagement metrics

5. **comments** - Post comments
   - Threaded comments support
   - Edit and delete tracking

6. **reactions** - Likes and sentiment
   - Support for multiple reaction types
   - Bullish/bearish sentiment tracking

7. **leaderboard_stats** - Performance metrics
   - Win rate, returns, risk metrics
   - Social metrics (followers, posts)
   - Rankings by period

8. **trending_tickers** - Ticker popularity
   - Mention counts, sentiment scores
   - Time-windowed trending data

9. **trending_patterns** - Pattern popularity
   - Pattern usage and success rates
   - Community pattern performance

## 🔐 Security

- **JWT Authentication**: Secure token-based authentication
- **Password Hashing**: Bcrypt password hashing
- **Input Validation**: Pydantic schema validation
- **SQL Injection Protection**: SQLAlchemy ORM
- **Rate Limiting**: Built-in rate limiting middleware
- **CORS Protection**: Configurable CORS policies

## 🚀 Getting Started

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set Environment Variables**:
   ```bash
   export DATABASE_URL="postgresql://user:pass@localhost/legend_ai"
   export SECRET_KEY="your-secret-key-here"
   ```

3. **Initialize Database**:
   The tables will be automatically created on first run via SQLAlchemy.

4. **Start Server**:
   ```bash
   uvicorn app.main:app --reload
   ```

5. **Access API Docs**:
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

## 📊 Usage Examples

### Python Example
```python
import requests

# Register
response = requests.post(
    'http://localhost:8000/api/social/auth/register',
    json={
        'username': 'trader123',
        'email': 'trader@example.com',
        'password': 'secure_pass123'
    }
)

# Login
response = requests.post(
    'http://localhost:8000/api/social/auth/login',
    json={
        'username': 'trader123',
        'password': 'secure_pass123'
    }
)
token = response.json()['access_token']

# Create trade post
headers = {'Authorization': f'Bearer {token}'}
response = requests.post(
    'http://localhost:8000/api/social/posts',
    headers=headers,
    json={
        'title': 'TSLA Breakout Setup',
        'content': 'Tesla breaking out of consolidation...',
        'ticker_symbol': 'TSLA',
        'entry_price': 250.0,
        'target_price': 280.0,
        'pattern_type': 'Cup & Handle'
    }
)

# Get trending tickers
response = requests.get(
    'http://localhost:8000/api/social/analytics/trending-tickers?time_window=24h'
)
trending = response.json()
for ticker in trending:
    print(f"{ticker['ticker_symbol']}: {ticker['sentiment_score']:.1f}")
```

### JavaScript Example
```javascript
// Login
const loginResponse = await fetch('http://localhost:8000/api/social/auth/login', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    username: 'trader123',
    password: 'secure_pass123'
  })
});
const { access_token } = await loginResponse.json();

// Get leaderboard
const leaderboardResponse = await fetch(
  'http://localhost:8000/api/social/leaderboard?period=monthly&limit=10'
);
const leaderboard = await leaderboardResponse.json();
console.log('Top Traders:', leaderboard.leaderboard);

// Get community stats
const statsResponse = await fetch(
  'http://localhost:8000/api/social/analytics/community-stats'
);
const stats = await statsResponse.json();
console.log(`Total Users: ${stats.total_users}`);
console.log(`Total Posts: ${stats.total_posts}`);
```

## 🎯 Best Practices

1. **Authentication**: Always use HTTPS in production
2. **Rate Limiting**: Respect rate limits (60 req/min)
3. **Error Handling**: Check response status codes
4. **Data Validation**: Validate input before sending
5. **Copy Trading**: Start with small percentages
6. **Privacy**: Review privacy settings before posting

## 📈 Future Enhancements

- [ ] Real-time notifications (WebSocket)
- [ ] Advanced copy trading algorithms
- [ ] Portfolio tracking integration
- [ ] Mobile app
- [ ] Email notifications
- [ ] Advanced analytics dashboards
- [ ] Trading competitions
- [ ] Educational content sections

## 🐛 Troubleshooting

### Common Issues

1. **401 Unauthorized**: Token expired or invalid - login again
2. **403 Forbidden**: Insufficient permissions - check user permissions
3. **404 Not Found**: Resource doesn't exist - verify IDs
4. **429 Too Many Requests**: Rate limited - wait and retry

## 📞 Support

- API Documentation: `/docs`
- GitHub Issues: [Report Issues](https://github.com/Stockmasterflex/legend-ai-python/issues)
- Community: Join our trading community

---

**⚠️ Disclaimer**: This platform is for educational and informational purposes only. Not financial advice. Always do your own research and trade responsibly.
