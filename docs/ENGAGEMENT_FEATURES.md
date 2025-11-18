# Legend AI - Engagement & Onboarding Features

This document describes the new engagement, gamification, and onboarding features added to Legend AI.

## Overview

The engagement system makes Legend AI more interactive and easier to learn through:

1. **Interactive Tutorial System** - First-time user walkthrough with tooltips
2. **Achievement System** - Gamified milestones and rewards
3. **Progress Tracking** - User levels, XP, and daily streaks
4. **Learning Center** - Educational content about patterns and trading
5. **Social Proof** - Community statistics and engagement metrics

## Features

### 1. Interactive Tutorial System

**Tutorials Available:**
- `onboarding` - First-time user walkthrough (6 steps)
- `vcp_pattern` - Understanding VCP patterns (4 steps)
- `cup_handle` - Cup & Handle pattern guide (4 steps)
- `risk_management` - Risk management basics (4 steps)

**Features:**
- Progressive disclosure of features
- Contextual tooltips on hover
- Skip option at any time
- Replay tutorials anytime
- Track completion status

**API Endpoints:**
```
GET    /api/engagement/tutorials                    # List all tutorials
GET    /api/engagement/tutorials/{key}              # Get tutorial definition
POST   /api/engagement/tutorials/{user_id}/start    # Start tutorial
POST   /api/engagement/tutorials/{user_id}/next     # Next step
POST   /api/engagement/tutorials/{user_id}/skip     # Skip tutorial
GET    /api/engagement/onboarding/{user_id}         # Check if show onboarding
GET    /api/engagement/tooltips                     # Get all tooltips
```

### 2. Achievement System

**Available Achievements:**

| Achievement | Icon | Requirement | XP Reward |
|------------|------|-------------|-----------|
| First Pattern Detected | 🎯 | Detect 1 pattern | 50 XP |
| 10 Stocks Analyzed | 📊 | Analyze 10 stocks | 100 XP |
| First Profitable Trade Idea | 💰 | 1 profitable idea | 100 XP |
| Watchlist Master | 📋 | 50+ watchlist items | 200 XP |
| Pattern Expert | 🔍 | 100 scans completed | 250 XP |
| Week Warrior | 🔥 | 7-day streak | 150 XP |
| Month Master | ⭐ | 30-day streak | 500 XP |

**Features:**
- Automatic unlock when criteria met
- XP bonus rewards
- Visual notifications on unlock
- Track unlock timestamps

**API Endpoints:**
```
GET    /api/engagement/achievements/{user_id}       # Get user achievements
```

### 3. Progress Tracking

**User Level System:**
- Start at Level 1
- Earn XP through activities
- Level up at thresholds: 100, 250, 500, 1000, 2000, 3500, 5500, 8000, 12000 XP
- Visual progress bar showing % to next level

**XP Rewards:**
- Scan: +10 XP
- Analyze stock: +20 XP
- Add to watchlist: +15 XP
- Pattern detected: +25 XP
- Profitable idea: +50 XP
- Complete tutorial: +100 XP
- Complete learning content: +30 XP
- Daily login: +5 XP

**Daily Streaks:**
- Tracks consecutive days of activity
- Shows current streak and longest streak
- Achievements for 7-day and 30-day streaks

**API Endpoints:**
```
GET    /api/engagement/stats/{user_id}              # Get user stats
POST   /api/engagement/track/{user_id}              # Track activity
GET    /api/engagement/leaderboard                  # Top users by XP
```

### 4. Learning Center

**Content Categories:**
- **Pattern Education** - Deep dives on VCP, Cup & Handle, etc.
- **Trading Strategies** - SEPA method, relative strength analysis
- **Glossary** - Trading terms and definitions
- **Best Practices** - Position sizing, risk management

**Content Available:**
- VCP Pattern Deep Dive (Intermediate, 15 min)
- Cup & Handle Pattern Guide (Beginner, 10 min)
- Understanding Relative Strength (Intermediate, 12 min)
- Mark Minervini's SEPA Method (Advanced, 20 min)
- What is a Pivot Point? (Beginner, 3 min)
- What is Volume Dry-Up? (Beginner, 3 min)
- Proper Position Sizing (Intermediate, 10 min)

**Features:**
- Markdown-formatted articles
- Video tutorial support (URLs)
- Difficulty levels: Beginner, Intermediate, Advanced
- Progress tracking (0-100%)
- Bookmark functionality
- Estimated reading time

**API Endpoints:**
```
GET    /api/engagement/learning                     # List all content
GET    /api/engagement/learning/{key}               # Get content detail
GET    /api/engagement/learning/categories/list     # Get categories
POST   /api/engagement/learning/{user_id}/progress  # Track progress
GET    /api/engagement/learning/{user_id}/progress  # Get user progress
POST   /api/engagement/learning/{user_id}/bookmark/{key}  # Toggle bookmark
GET    /api/engagement/learning/{user_id}/bookmarks # Get bookmarks
```

### 5. Social Proof & Community Stats

**Displayed Stats:**
- Patterns detected today
- Top pattern this week
- Most watched ticker
- Active users today
- Total scans today

**API Endpoints:**
```
GET    /api/engagement/community/stats              # Get community stats
```

## Usage

### Frontend Integration

1. **Check if user needs onboarding:**
```javascript
const response = await fetch(`/api/engagement/onboarding/${userId}`);
const { show_onboarding } = await response.json();

if (show_onboarding) {
    startOnboardingTutorial();
}
```

2. **Track user activities:**
```javascript
// When user performs an action
await fetch(`/api/engagement/track/${userId}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        activity_type: 'scan',
        metadata: { symbol: 'AAPL' }
    })
});
```

3. **Display user stats:**
```javascript
const response = await fetch(`/api/engagement/stats/${userId}`);
const stats = await response.json();

// stats contains:
// - level, xp, level_progress
// - stats: total_scans, patterns_detected, etc.
// - streak: current, longest
// - achievements: array of unlocked achievements
```

4. **Show learning content:**
```javascript
const response = await fetch('/api/engagement/learning?category=pattern');
const { content } = await response.json();

// Display content list
content.forEach(item => {
    console.log(item.title, item.difficulty, item.estimated_time);
});
```

### Database Setup

1. **Run migrations to create tables:**
```bash
alembic revision --autogenerate -m "Add engagement tables"
alembic upgrade head
```

2. **Initialize data:**
```bash
curl -X POST http://localhost:8000/api/engagement/admin/init
```

This will:
- Create all achievement definitions
- Populate learning content
- Initialize community stats

### Engagement Dashboard

Visit the interactive dashboard at:
```
http://localhost:8000/static/engagement.html
```

Features:
- Real-time user stats display
- Progress bar with XP tracking
- Achievement showcase (locked/unlocked)
- Community statistics
- Demo controls for testing

## Database Models

### UserProgress
- User level, XP, and activity counters
- Daily streak tracking
- Last active timestamp

### Achievement
- Achievement definitions (name, icon, requirements)
- XP rewards

### UserAchievement
- User-achievement relationships
- Unlock timestamps

### TutorialProgress
- Tutorial completion tracking
- Current step number
- Skip/complete status

### ActivityLog
- User activity history
- XP earnings log
- Activity metadata

### LearningContent
- Educational articles and videos
- Categories and difficulty levels
- Order and timing information

### UserLearningProgress
- Progress through learning content
- Bookmarks
- Completion tracking

### CommunityStats
- Daily aggregate statistics
- Top patterns and tickers
- Active user counts

## Integration Points

### Pattern Scanner
Track when patterns are detected:
```python
await EngagementService.track_activity(db, user_id, "pattern_detect", {
    "pattern": "VCP",
    "symbol": "AAPL",
    "score": 85
})
```

### Stock Analysis
Track stock analyses:
```python
await EngagementService.track_activity(db, user_id, "analyze", {
    "symbol": "NVDA"
})
```

### Watchlist
Track watchlist additions:
```python
await EngagementService.track_activity(db, user_id, "watchlist_add", {
    "symbol": "TSLA"
})
```

## Testing

### Manual Testing
1. Visit `/static/engagement.html`
2. Use demo controls to simulate activities
3. Watch XP increase and achievements unlock
4. Test tutorial flow with `/api/engagement/tutorials/{user_id}/start`

### API Testing
```bash
# Get user stats
curl http://localhost:8000/api/engagement/stats/test-user

# Track activity
curl -X POST http://localhost:8000/api/engagement/track/test-user \
  -H "Content-Type: application/json" \
  -d '{"activity_type": "scan"}'

# Get learning content
curl http://localhost:8000/api/engagement/learning

# Start tutorial
curl -X POST http://localhost:8000/api/engagement/tutorials/test-user/start \
  -H "Content-Type: application/json" \
  -d '{"tutorial_key": "onboarding"}'
```

## Future Enhancements

Potential additions:
- Weekly/monthly challenges
- Team competitions
- Custom achievement creation
- Video tutorial integration
- Push notifications for achievements
- Social sharing of achievements
- Mentor/mentee system
- Trading journal integration
- Performance-based achievements
- Referral rewards

## Notes

- User ID can come from authentication system
- For demo purposes, uses "demo-user" as default
- XP and level calculations are customizable
- Achievement criteria can be adjusted
- Learning content can be easily added/modified
- Community stats update daily (can be configured)
