# SOCIAL TRADING IMPLEMENTATION - QUICK START GUIDE

## Overview

You have a solid FastAPI platform with pattern detection and trade management. To add social trading features, you need to:

1. **Add user authentication** (JWT + bcrypt)
2. **Create user tables** (User, UserProfile, Follow relationships)
3. **Migrate trades to be user-isolated** (currently in Redis with no persistence)
4. **Add social APIs** (sharing, follows, leaderboards, engagement)
5. **Update frontend** (login, profile, social feed, leaderboards)

---

## File Structure You'll Be Creating/Modifying

### NEW FILES (Phase-by-phase)

```
Phase 1: Authentication
├── app/services/auth.py               ← NEW (JWT + password hashing)
├── app/api/auth.py                    ← NEW (register, login endpoints)

Phase 2: User Management
├── app/api/users.py                   ← NEW (profile endpoints)
└── Update app/services/database.py    ← MODIFY (add user queries)

Phase 3: Follow System
├── app/services/follows.py            ← NEW
└── app/api/follows.py                 ← NEW

Phase 4: Social Trading
├── app/services/social_trades.py      ← NEW
├── app/api/social_trades.py           ← NEW
└── Update app/services/trades.py      ← MODIFY (add user_id isolation)

Phase 5: Leaderboards
├── app/services/leaderboards.py       ← NEW
└── app/api/leaderboards.py            ← NEW

Frontend
├── static/js/auth.js                  ← NEW
├── static/js/social.js                ← NEW
└── Update templates/dashboard.html    ← MODIFY
```

### MODIFIED FILES

```
Core System Files:
├── app/models.py                       ← Add User, UserProfile, Follow tables
├── app/config.py                       ← Add JWT settings
├── app/main.py                         ← Register new routers
├── app/middleware/rate_limit.py        ← Add per-user rate limiting

Trade Management:
├── app/services/trades.py              ← Add user_id parameter
├── app/api/trades.py                   ← Add @require_auth decorator

Database:
└── alembic/versions/                   ← Add migration files

Database Tables:
├── Watchlist.user_id                   ← Change from string to FK
└── AlertLog.user_id                    ← Change from string to FK
```

---

## Database Changes Required

### New Tables (in app/models.py)

```python
# Phase 1
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, indexed)
    email = Column(String(255), unique=True, indexed)
    password_hash = Column(String(255))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())

class UserProfile(Base):
    __tablename__ = "user_profiles"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    display_name = Column(String(100))
    bio = Column(Text)
    avatar_url = Column(String(500))
    total_trades = Column(Integer, default=0)
    win_rate = Column(Float, default=0)
    total_profit_loss = Column(Float, default=0)
    follower_count = Column(Integer, default=0)
    following_count = Column(Integer, default=0)

# Phase 3
class Follow(Base):
    __tablename__ = "follows"
    id = Column(Integer, primary_key=True)
    follower_id = Column(Integer, ForeignKey("users.id"))
    following_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, server_default=func.now())
    UniqueConstraint('follower_id', 'following_id')

# Phase 4
class SharedTrade(Base):
    __tablename__ = "shared_trades"
    id = Column(Integer, primary_key=True)
    trade_id = Column(String(50))  # Reference to original trade
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String(200))
    description = Column(Text)
    visibility = Column(String(20), default="public")  # public, followers_only, private
    likes_count = Column(Integer, default=0)
    comments_count = Column(Integer, default=0)
    copies_count = Column(Integer, default=0)
    created_at = Column(DateTime, server_default=func.now())

class TradeComment(Base):
    __tablename__ = "trade_comments"
    id = Column(Integer, primary_key=True)
    shared_trade_id = Column(Integer, ForeignKey("shared_trades.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    comment_text = Column(Text)
    created_at = Column(DateTime, server_default=func.now())

class TradeLike(Base):
    __tablename__ = "trade_likes"
    id = Column(Integer, primary_key=True)
    shared_trade_id = Column(Integer, ForeignKey("shared_trades.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, server_default=func.now())
    UniqueConstraint('shared_trade_id', 'user_id')

# Phase 5
class TradePerformance(Base):
    __tablename__ = "trade_performance"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    date = Column(Date, indexed)
    total_trades = Column(Integer)
    winning_trades = Column(Integer)
    win_rate = Column(Float)
    profit_loss = Column(Float)
    roi = Column(Float)
    average_r_multiple = Column(Float)
```

### Alembic Migration

```bash
# Generate migration:
alembic revision --autogenerate -m "Add social trading tables"

# Run migration:
alembic upgrade head
```

---

## Implementation Order (Recommended)

### Week 1: Foundation (Phase 1 + 2)
1. Create `User` and `UserProfile` tables in models.py
2. Implement `app/services/auth.py` with JWT + bcrypt
3. Create `app/api/auth.py` with register/login endpoints
4. Create `app/api/users.py` with profile endpoints
5. Run database migrations

### Week 2: Data Migration + Trade Isolation (Phase 2 cont)
6. Update `app/services/trades.py` to add user_id parameter
7. Update `app/api/trades.py` to require authentication
8. Add user-specific database queries
9. Test trade isolation

### Week 3: Social Features (Phase 3-4)
10. Create `Follow` table and `/api/follows` router
11. Create `SharedTrade` tables and `/api/social-trades` router
12. Implement like/comment functionality
13. Add trade copying feature

### Week 4: Analytics (Phase 5)
14. Create `TradePerformance` table
15. Implement leaderboard calculations (background job)
16. Create `/api/leaderboards` router

### Week 5: Frontend
17. Create `static/js/auth.js` for login/signup
18. Create `static/js/social.js` for social features
19. Update dashboard.html with social UI
20. Test end-to-end

---

## Key Implementation Details

### Authentication Pattern (Copy-Paste Ready)

```python
# app/services/auth.py
from passlib.context import CryptContext
import jwt
from datetime import datetime, timedelta

pwd_context = CryptContext(schemes=["bcrypt"])

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

def create_access_token(user_id: int, expires_delta: timedelta = None):
    if not expires_delta:
        expires_delta = timedelta(minutes=15)
    
    expire = datetime.utcnow() + expires_delta
    data = {"sub": str(user_id), "exp": expire}
    
    token = jwt.encode(
        data,
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm
    )
    return token

def verify_token(token: str) -> int:
    payload = jwt.decode(token, settings.jwt_secret_key, settings.jwt_algorithm)
    user_id = int(payload.get("sub"))
    return user_id
```

### Router Pattern (Copy-Paste Ready)

```python
# app/api/users.py
from fastapi import APIRouter, Depends, HTTPException
from app.services.auth import get_current_user

router = APIRouter(prefix="/api/users", tags=["users"])

async def get_current_user(token: str = Depends(oauth2_scheme)):
    """Dependency to get authenticated user"""
    try:
        user_id = verify_token(token)
        return user_id
    except:
        raise HTTPException(status_code=401, detail="Invalid token")

@router.get("/me")
async def get_profile(user_id: int = Depends(get_current_user)):
    """Get current user profile"""
    # Query database for user data
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404)
    return {"username": user.username, "profile": user.profile}

@router.put("/me")
async def update_profile(profile_data: dict, user_id: int = Depends(get_current_user)):
    """Update profile"""
    # Always use user_id from token, NEVER from request body
    profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
    # Update fields
    db.commit()
    return {"success": True}
```

### Critical Security Rules

1. **NEVER trust user_id from request**
   ```python
   # BAD ❌
   user_id = request.json.get("user_id")
   
   # GOOD ✅
   user_id = get_current_user(token)  # From JWT only
   ```

2. **ALWAYS check ownership before delete/update**
   ```python
   # GOOD ✅
   trade = db.query(SharedTrade).filter(
       SharedTrade.id == trade_id,
       SharedTrade.user_id == current_user_id  # Verify owner
   ).first()
   if not trade:
       raise HTTPException(403, "Forbidden")
   ```

3. **Use database indexes for performance**
   ```python
   Index on: user_id, created_at for most queries
   Index on: follower_id, following_id for social queries
   ```

---

## Testing Quick Checklist

```bash
# Test authentication
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"test","email":"test@test.com","password":"Test123!"}'

curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","password":"Test123!"}'

# Test authenticated endpoint
curl -X GET http://localhost:8000/api/users/me \
  -H "Authorization: Bearer <token>"

# Test social features
curl -X POST http://localhost:8000/api/follows/2 \
  -H "Authorization: Bearer <token>"

curl -X GET http://localhost:8000/api/leaderboards/winrate
```

---

## Environment Variables to Add

```bash
# JWT Settings
JWT_SECRET_KEY=your-super-secret-key-change-in-production
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7

# Social Features
ENABLE_SOCIAL_TRADING=true
MAX_TRADE_SHARES_PER_DAY=10
MAX_FOLLOWS_PER_USER=1000
MAX_COMMENTS_PER_TRADE=100

# Email (for notifications, optional)
SENDGRID_API_KEY=optional
SEND_EMAIL_ALERTS=false
```

---

## Performance Considerations

1. **Query Optimization**
   - Eager load relationships (User -> UserProfile)
   - Paginate leaderboard queries (100-1000 rows max)
   - Cache leaderboards (30 min TTL)

2. **Background Jobs**
   - Calculate leaderboards daily (off-peak hours)
   - Update user stats periodically
   - Cleanup deleted trades/comments

3. **Caching Strategy**
   ```
   user:{user_id}              -> 1 hour TTL
   leaderboard:{period}        -> 30 min TTL
   feed:{user_id}              -> 5 min TTL
   ```

---

## Next Steps

1. Review this document and the detailed architecture guide
2. Create Alembic migration for new tables
3. Implement Phase 1 (auth) first - it's critical for everything else
4. Run tests after each phase
5. Deploy to staging environment for testing
6. Feature flag social features for gradual rollout

---

## Documentation Files Reference

You have 3 detailed documents:

1. **SOCIAL_TRADING_ARCHITECTURE.md** - Full architecture overview
   - System design, existing components, recommendations
   - Database schema details, API patterns
   - Caching strategy, security considerations

2. **IMPLEMENTATION_CHECKLIST.md** - Phase-by-phase checklist
   - Step-by-step tasks for each phase
   - Database queries to implement
   - Frontend changes needed

3. **DATABASE_DIAGRAM.txt** - Visual architecture
   - Entity relationship diagram
   - API routing hierarchy
   - Data isolation & security rules

**Start with the architecture guide, then refer to checklist while implementing, use diagrams for reference.**

