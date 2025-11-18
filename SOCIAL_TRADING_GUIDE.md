# Legend AI Social Trading Features - Complete Implementation Guide

## Quick Navigation

This guide contains everything you need to implement social trading features. Start here!

### Documents Overview

1. **[SOCIAL_TRADING_IMPLEMENTATION.md](SOCIAL_TRADING_IMPLEMENTATION.md)** - START HERE
   - Quick start guide with copy-paste code snippets
   - 5-week implementation timeline
   - Critical security rules
   - Testing checklist

2. **[SOCIAL_TRADING_ARCHITECTURE.md](SOCIAL_TRADING_ARCHITECTURE.md)** - DETAILED REFERENCE
   - Full system architecture overview
   - Existing project structure (how it currently works)
   - Database schema design for social features
   - API routing patterns and recommendations
   - Caching strategy for performance
   - Security considerations
   - Complete implementation roadmap

3. **[SOCIAL_TRADING_CHECKLIST.md](SOCIAL_TRADING_CHECKLIST.md)** - PHASE-BY-PHASE TASKS
   - Phase 1: Authentication & User Foundation
   - Phase 2: User Management & Profiles
   - Phase 3: Social Follow System
   - Phase 4: Social Trading & Trade Sharing
   - Phase 5: Leaderboards & Analytics
   - Phase 6: Frontend Updates
   - Testing, performance, security hardening
   - Deployment checklist

4. **[SOCIAL_TRADING_DIAGRAM.txt](SOCIAL_TRADING_DIAGRAM.txt)** - VISUAL REFERENCE
   - Database entity relationship diagrams
   - API routing hierarchy
   - Data isolation & security model
   - Table relationships visualization

---

## What You're Building

### Current State
- Pattern detection system (9 different patterns)
- Trade tracking in Redis (in-memory, no persistence)
- Watchlist management
- Alert system
- Risk calculator
- Pattern scanner for universes
- NO user authentication
- NO user profiles
- NO social features
- Global data visibility (everyone sees everything)

### End State (After Implementation)
- User authentication with JWT
- User profiles with trading statistics
- Follow/follower system
- Trade sharing with visibility controls
- Trade likes and comments
- Leaderboards (win rate, profit, consistency, ROI, followers)
- Per-user data isolation and access control
- Persistent trade history
- Performance analytics

---

## Implementation at a Glance

```
Week 1: Authentication (Phase 1-2)
  - User registration & login
  - JWT token management
  - User profiles
  
Week 2: Trade Migration (Phase 2 cont)
  - Move trades to database (currently in Redis)
  - Implement per-user isolation
  - Update all trade endpoints
  
Week 3: Social Core (Phase 3-4)
  - Follow/unfollow system
  - Trade sharing
  - Like/comment features
  
Week 4: Analytics (Phase 5)
  - Leaderboard calculations
  - Performance tracking
  - Statistics aggregation
  
Week 5: Frontend
  - Login/signup UI
  - Profile pages
  - Social feed
  - Leaderboard views
```

---

## Key Architectural Changes

### Database
- Add 8 new tables: User, UserProfile, Follow, SharedTrade, TradeComment, TradeLike, TradePerformance, Leaderboard
- Modify existing Watchlist and AlertLog to use User FK instead of string ID
- Use Alembic migrations for versioning

### Authentication
- JWT tokens (15 min expiry) + refresh tokens (7 days)
- bcrypt password hashing
- Per-user rate limiting (100 req/min per user)

### API Changes
- Add `/api/auth/*` endpoints for authentication
- Add `/api/users/*` for profile management
- Add `/api/follows/*` for social relationships
- Add `/api/social-trades/*` for trade sharing
- Add `/api/leaderboards/*` for rankings
- Update `/api/trades/*` to require authentication

### Data Isolation
- All data filtered by current user's ID (from JWT token)
- Ownership validation before all delete/update operations
- Visibility controls for shared trades

---

## Important Security Rules

1. **ALWAYS extract user_id from JWT token, NEVER from request body**
   ```python
   # BAD ❌
   user_id = request.json.get("user_id")
   
   # GOOD ✅
   user_id = verify_token(request.headers.get("Authorization"))
   ```

2. **ALWAYS validate ownership before modification**
   ```python
   # Check user owns the resource
   record = db.query(Model).filter(
       Model.id == record_id,
       Model.user_id == current_user_id
   ).first()
   if not record:
       raise HTTPException(403, "Forbidden")
   ```

3. **NEVER return sensitive data**
   - Hide actual account balances
   - Hide email addresses (except own profile)
   - Hide password hashes everywhere
   - Only show aggregate statistics on leaderboards

---

## Getting Started

### Step 1: Read the Quick Start (15 minutes)
- Open [SOCIAL_TRADING_IMPLEMENTATION.md](SOCIAL_TRADING_IMPLEMENTATION.md)
- Understand the 5-phase approach
- Review the database schema

### Step 2: Review the Architecture (30 minutes)
- Open [SOCIAL_TRADING_ARCHITECTURE.md](SOCIAL_TRADING_ARCHITECTURE.md)
- Understand existing components
- See recommended implementation locations
- Review caching strategy

### Step 3: Check the Checklist (reference while coding)
- Open [SOCIAL_TRADING_CHECKLIST.md](SOCIAL_TRADING_CHECKLIST.md)
- Use as your task list
- Check off each phase as you complete it
- Reference database schemas and API endpoints

### Step 4: Use Diagrams When Needed
- Open [SOCIAL_TRADING_DIAGRAM.txt](SOCIAL_TRADING_DIAGRAM.txt)
- Visualize database relationships
- Understand API routing hierarchy
- Review security model

---

## File Locations You'll Be Working With

### Backend Files to Create
```
app/services/auth.py                  # Phase 1
app/api/auth.py                       # Phase 1
app/api/users.py                      # Phase 2
app/services/follows.py               # Phase 3
app/api/follows.py                    # Phase 3
app/services/social_trades.py         # Phase 4
app/api/social_trades.py              # Phase 4
app/services/leaderboards.py          # Phase 5
app/api/leaderboards.py               # Phase 5
```

### Backend Files to Modify
```
app/models.py                         # Add User, UserProfile, Follow tables
app/config.py                         # Add JWT settings
app/main.py                           # Register new routers
app/services/trades.py                # Add user_id parameter
app/api/trades.py                     # Add @require_auth decorator
app/middleware/rate_limit.py          # Add per-user limiting
```

### Frontend Files to Create/Modify
```
static/js/auth.js                     # Login/signup logic
static/js/social.js                   # Follow, share, like features
templates/dashboard.html              # Add social UI components
```

### Database Files
```
alembic/versions/                     # Migration files (auto-generated)
```

---

## Dependencies You'll Need to Add

```bash
pip install python-jose[cryptography]  # JWT
pip install passlib[bcrypt]            # Password hashing
pip install pydantic-extra-types       # Additional validators
```

Update `requirements.txt` with these if not already present.

---

## Success Criteria

Phase 1 Complete: Users can register, login, and get JWT tokens
Phase 2 Complete: Trades are user-isolated and require authentication
Phase 3 Complete: Users can follow/unfollow other traders
Phase 4 Complete: Users can share, like, and comment on trades
Phase 5 Complete: Leaderboards show top traders across different metrics
Frontend Done: Everything works in the browser with new UI

---

## Common Questions

**Q: Can I do this gradually without breaking existing features?**
A: Yes! Deploy auth system first (non-breaking), then feature-flag new tables, gradually migrate data.

**Q: What about existing trades in Redis?**
A: Keep them for now, migrate to database in background jobs. Implement alongside existing system.

**Q: How do I test this locally?**
A: See curl examples in SOCIAL_TRADING_IMPLEMENTATION.md - test each endpoint as you build.

**Q: What about performance?**
A: See caching strategy in SOCIAL_TRADING_ARCHITECTURE.md - cache user data, leaderboards, feeds with appropriate TTLs.

**Q: Should I use database migrations?**
A: Yes! Use Alembic (already configured). Run `alembic revision --autogenerate` to generate migrations automatically.

---

## Next Steps

1. Open [SOCIAL_TRADING_IMPLEMENTATION.md](SOCIAL_TRADING_IMPLEMENTATION.md)
2. Create app/models.py additions for User and UserProfile tables
3. Generate Alembic migration: `alembic revision --autogenerate -m "Add social tables"`
4. Implement app/services/auth.py with JWT and password hashing
5. Build app/api/auth.py with register/login endpoints
6. Test with curl commands provided in the documentation

Good luck! These features will make Legend AI stand out as a true community trading platform.

