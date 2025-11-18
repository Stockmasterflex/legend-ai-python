# Quick Implementation Checklist for Social Trading Features

## Phase 1: Authentication & User Foundation (Priority: CRITICAL)

### Database Schema
- [ ] Create `User` table (SQLAlchemy model)
  - id (PK)
  - username (unique, indexed)
  - email (unique, indexed)
  - password_hash
  - created_at / updated_at
  - is_active (boolean)

- [ ] Create `UserProfile` table
  - user_id (FK) → User
  - display_name
  - bio / description
  - avatar_url
  - total_trades
  - win_rate
  - total_profit_loss
  - follower_count / following_count
  - created_at / updated_at

### Authentication Service
- [ ] Create `app/services/auth.py`
  - hash_password() using bcrypt
  - verify_password()
  - create_access_token() using JWT
  - create_refresh_token()
  - verify_token()
  - get_current_user() dependency

- [ ] Create `app/api/auth.py` router
  - POST /api/auth/register
  - POST /api/auth/login
  - POST /api/auth/refresh
  - POST /api/auth/logout
  - POST /api/auth/verify

### Configuration Updates
- [ ] Update `app/config.py`
  - Add JWT_SECRET_KEY
  - Add JWT_ALGORITHM
  - Add ACCESS_TOKEN_EXPIRE_MINUTES
  - Add REFRESH_TOKEN_EXPIRE_DAYS

### Middleware Updates
- [ ] Update middleware/rate_limit.py to support per-user rate limiting

---

## Phase 2: User Management & Profiles

### User Profile API
- [ ] Create `app/api/users.py` router
  - GET /api/users/me → Current user profile
  - PUT /api/users/me → Update profile
  - GET /api/users/{user_id} → Public profile (read-only)
  - DELETE /api/users/me → Delete account

### Update Trade Service
- [ ] Modify `app/services/trades.py`
  - Add user_id parameter to all Trade methods
  - Add user isolation to all queries
  - Update Redis keys: trade:{user_id}:{trade_id}

- [ ] Modify `app/api/trades.py`
  - Add @require_auth decorator to all endpoints
  - Extract user_id from JWT token
  - Filter trades by user_id

### Database Queries
- [ ] Add user-specific queries to `app/services/database.py`
  - get_user_trades(user_id, limit)
  - get_user_watchlist(user_id)
  - get_user_stats(user_id)

---

## Phase 3: Social Follow System

### Database Schema
- [ ] Create `Follow` table
  - id (PK)
  - follower_id (FK) → User
  - following_id (FK) → User
  - created_at
  - (Unique constraint: follower_id + following_id)

### Follow API
- [ ] Create `app/api/follows.py` router
  - POST /api/follows/{user_id} → Follow user
  - DELETE /api/follows/{user_id} → Unfollow
  - GET /api/follows/followers → My followers
  - GET /api/follows/following → Who I follow
  - GET /api/users/{user_id}/followers → User's followers count
  - GET /api/users/{user_id}/following → User's following count

### Follow Service
- [ ] Create `app/services/follows.py`
  - follow_user(follower_id, following_id)
  - unfollow_user(follower_id, following_id)
  - get_followers(user_id)
  - get_following(user_id)
  - is_following(follower_id, following_id)

---

## Phase 4: Social Trading & Trade Sharing

### Database Schema
- [ ] Create `SharedTrade` table
  - id (PK)
  - trade_id (FK) → Trade data
  - user_id (FK) → User
  - title (string)
  - description (text)
  - visibility ("public", "followers_only", "private")
  - likes_count (integer)
  - comments_count (integer)
  - copies_count (integer)
  - created_at / updated_at

- [ ] Create `TradeComment` table
  - id (PK)
  - shared_trade_id (FK) → SharedTrade
  - user_id (FK) → User
  - comment_text (text)
  - created_at / updated_at

- [ ] Create `TradeLike` table
  - id (PK)
  - shared_trade_id (FK) → SharedTrade
  - user_id (FK) → User
  - created_at
  - (Unique constraint: shared_trade_id + user_id)

- [ ] Create `TradePerformance` table
  - id (PK)
  - user_id (FK) → User
  - date (date, indexed)
  - total_trades
  - winning_trades
  - win_rate
  - profit_loss
  - roi
  - average_r_multiple

### Trade Sharing API
- [ ] Create `app/api/social_trades.py` router
  - POST /api/social-trades/create → Share a trade
  - GET /api/social-trades/feed → Get social feed
  - GET /api/social-trades/{trade_id} → View shared trade
  - POST /api/social-trades/{trade_id}/copy → Copy trade
  - DELETE /api/social-trades/{trade_id} → Delete shared trade
  - POST /api/social-trades/{trade_id}/like → Like trade
  - DELETE /api/social-trades/{trade_id}/like → Unlike trade
  - GET /api/social-trades/{trade_id}/likes → Get like count
  - POST /api/social-trades/{trade_id}/comments → Add comment
  - GET /api/social-trades/{trade_id}/comments → Get comments
  - DELETE /api/social-trades/{trade_id}/comments/{comment_id} → Delete comment

### Social Trading Service
- [ ] Create `app/services/social_trades.py`
  - share_trade(user_id, trade_data, visibility)
  - get_social_feed(user_id, limit)
  - copy_trade(user_id, shared_trade_id)
  - like_trade(user_id, shared_trade_id)
  - unlike_trade(user_id, shared_trade_id)
  - add_comment(user_id, shared_trade_id, comment)
  - get_trade_comments(shared_trade_id)

---

## Phase 5: Leaderboards & Analytics

### Database Schema
- [ ] Create `Leaderboard` table (materialized view or denormalized)
  - id (PK)
  - user_id (FK) → User
  - period ("day", "week", "month", "all_time")
  - rank (integer)
  - metric_type ("winrate", "profitability", "consistency", "roi", "followers")
  - metric_value (float)
  - calculated_at (datetime)

### Leaderboard API
- [ ] Create `app/api/leaderboards.py` router
  - GET /api/leaderboards/winrate → Top by win rate
  - GET /api/leaderboards/profitability → Top by profit
  - GET /api/leaderboards/consistency → Top by consistency (low std dev)
  - GET /api/leaderboards/roi → Top by ROI
  - GET /api/leaderboards/followers → Top by followers
  - Query params: period (day|week|month|all_time), limit (default 100)

### Leaderboard Service
- [ ] Create `app/services/leaderboards.py`
  - calculate_leaderboards() → Background job
  - get_leaderboard(metric_type, period, limit)
  - get_user_rank(user_id, metric_type, period)
  - calculate_consistency(user_id, period)
  - calculate_roi(user_id, period)

### Analytics Service Enhancement
- [ ] Extend `app/services/database.py`
  - calculate_user_stats(user_id, period)
  - batch_calculate_performance()

---

## Phase 6: Frontend Updates

### Templates
- [ ] Update `templates/dashboard.html`
  - Add login/registration modal
  - Add user profile dropdown
  - Add social trading feed section
  - Add leaderboard view
  - Add follow/unfollow buttons

### JavaScript
- [ ] Create `static/js/auth.js`
  - register(username, email, password)
  - login(email, password)
  - logout()
  - refreshToken()
  - getAuthHeaders() → Include JWT in requests

- [ ] Create `static/js/social.js`
  - followUser(userId)
  - unfollowUser(userId)
  - shareTrade(tradeData)
  - likeTrade(tradeId)
  - commentOnTrade(tradeId, comment)
  - copyTrade(sharedTradeId)

- [ ] Update `static/js/dashboard.js`
  - Initialize auth on page load
  - Redirect to login if not authenticated
  - Display user profile in header
  - Add social feed fetching

### Styles
- [ ] Update `static/css/dashboard.css`
  - Add login form styles
  - Add profile dropdown styles
  - Add social feed layout
  - Add leaderboard table styles

---

## Testing Implementation

- [ ] Write tests for `app/services/auth.py`
  - Test password hashing/verification
  - Test JWT token generation/validation
  - Test token expiration

- [ ] Write tests for `app/api/auth.py`
  - Test registration validation
  - Test login success/failure
  - Test token refresh

- [ ] Write tests for `app/api/users.py`
  - Test profile CRUD
  - Test authorization

- [ ] Write tests for `app/api/follows.py`
  - Test follow/unfollow
  - Test follower lists
  - Test self-follow prevention

- [ ] Write tests for `app/api/social_trades.py`
  - Test trade sharing
  - Test visibility settings
  - Test trade copying
  - Test like/comment functionality

- [ ] Write tests for `app/api/leaderboards.py`
  - Test leaderboard calculation
  - Test ranking correctness
  - Test period filtering

---

## Performance Optimization

- [ ] Implement caching strategy
  - Cache user profiles (1 hour TTL)
  - Cache leaderboards (30 min TTL)
  - Cache social feeds (5 min TTL)

- [ ] Add database indexes
  - Index on Follow.follower_id
  - Index on Follow.following_id
  - Index on SharedTrade.user_id
  - Index on SharedTrade.created_at
  - Index on TradePerformance.user_id
  - Index on TradePerformance.date

- [ ] Add query optimizations
  - Use eager loading for related data
  - Implement pagination for all lists
  - Add query timeouts

---

## Security Hardening

- [ ] Implement rate limiting
  - 10 login attempts per 15 minutes
  - 100 API calls per minute per user
  - 1000 social actions per day per user

- [ ] Add input validation
  - Username: 3-30 chars, alphanumeric + underscore
  - Bio: max 500 chars
  - Trade title: max 100 chars
  - Comment: max 1000 chars

- [ ] Add authorization checks
  - Users can only edit their own data
  - Users can only delete their own trades/comments
  - Users cannot follow themselves

- [ ] Implement CORS correctly
  - Only allow requests from frontend origin

---

## Deployment Checklist

- [ ] Add environment variables to Railway
  - JWT_SECRET_KEY
  - JWT_ALGORITHM
  - ACCESS_TOKEN_EXPIRE_MINUTES
  - REFRESH_TOKEN_EXPIRE_DAYS

- [ ] Run database migrations
  - Create User table
  - Create UserProfile table
  - Create Follow table
  - Create SharedTrade table
  - Create other tables

- [ ] Backup existing data
  - Before any schema changes
  - Test migration scripts locally

- [ ] Deploy in stages
  - 1. Auth system (non-breaking)
  - 2. New tables (with feature flags)
  - 3. User isolation (gradual rollout)
  - 4. Social features (behind feature flag)

