# Quick Start - Engagement Features

Get started with Legend AI's new engagement and onboarding features in 5 minutes!

## Step 1: Install Dependencies

The engagement features use the existing dependencies. No additional packages required!

```bash
# If you haven't already
pip install -r requirements.txt
```

## Step 2: Initialize Database

Run the initialization script to create tables and seed data:

```bash
python scripts/init_engagement.py
```

This will:
- Create all engagement-related database tables
- Seed 7 achievements
- Add 7 learning articles
- Set up the gamification system

## Step 3: Start the Server

```bash
uvicorn app.main:app --reload
```

## Step 4: Try It Out!

### Option A: Interactive Dashboard (Recommended)

Open your browser and visit:
```
http://localhost:8000/static/engagement.html
```

You'll see:
- User stats (scans, patterns, streaks)
- XP progress bar with level
- Achievement showcase
- Community statistics
- Demo controls to test features

**Try the demo controls:**
1. Click "Run Scan (+10 XP)" multiple times
2. Watch your XP increase
3. Unlock your first achievement!

### Option B: API Testing

#### 1. Get User Stats
```bash
curl http://localhost:8000/api/engagement/stats/demo-user
```

#### 2. Track an Activity
```bash
curl -X POST http://localhost:8000/api/engagement/track/demo-user \
  -H "Content-Type: application/json" \
  -d '{"activity_type": "scan"}'
```

#### 3. Start Onboarding Tutorial
```bash
curl -X POST http://localhost:8000/api/engagement/tutorials/demo-user/start \
  -H "Content-Type: application/json" \
  -d '{"tutorial_key": "onboarding"}'
```

#### 4. Browse Learning Content
```bash
curl http://localhost:8000/api/engagement/learning
```

#### 5. Get Community Stats
```bash
curl http://localhost:8000/api/engagement/community/stats
```

## Features Overview

### 🎯 Achievements
Track user milestones:
- First Pattern Detected
- 10 Stocks Analyzed
- First Profitable Trade Idea
- Watchlist Master (50+ stocks)
- Pattern Expert (100 scans)
- Week Warrior (7-day streak)
- Month Master (30-day streak)

### 📈 Progress Tracking
- User levels (1-10+)
- XP system with activity rewards
- Daily streak counter
- Comprehensive stats dashboard

### 📚 Learning Center
Educational content:
- VCP Pattern Deep Dive
- Cup & Handle Guide
- Relative Strength Analysis
- SEPA Trading Method
- Position Sizing
- Trading Glossary

### 🎓 Interactive Tutorials
- Onboarding walkthrough (6 steps)
- Pattern education tutorials
- Risk management guide
- Skip/replay functionality

### 👥 Social Proof
Community statistics:
- Patterns detected today
- Top pattern this week
- Most watched ticker
- Active users

## Integration with Your App

### Track User Activities

Whenever a user performs an action, track it:

```python
from app.services.engagement import EngagementService

# After pattern scan
result = await EngagementService.track_activity(
    db, user_id, "scan",
    metadata={"symbols_scanned": 100}
)

# Check for level ups and achievements
if result["level_up"]:
    notify_user(f"Level up! Now level {result['level']}")

if result["new_achievements"]:
    for ach in result["new_achievements"]:
        show_achievement_toast(ach)
```

### Show Onboarding to New Users

```python
from app.services.tutorial import TutorialService

# Check if user needs onboarding
should_show = await TutorialService.should_show_onboarding(db, user_id)

if should_show:
    # Start onboarding tutorial
    tutorial = await TutorialService.start_tutorial(db, user_id, "onboarding")
    return tutorial
```

### Display Learning Content

```python
from app.services.learning_center import LearningCenterService

# Get pattern education content
content = await LearningCenterService.get_all_content(
    db, category="pattern"
)

# Get specific article
article = await LearningCenterService.get_content(
    db, "vcp_deep_dive"
)
```

## Activity Types & XP Rewards

| Activity | XP | When to Track |
|----------|----|--------------|
| `scan` | +10 | Pattern scan completed |
| `analyze` | +20 | Stock analyzed |
| `watchlist_add` | +15 | Stock added to watchlist |
| `pattern_detect` | +25 | Pattern detected |
| `profitable_idea` | +50 | Profitable trade idea |
| `tutorial_complete` | +100 | Tutorial completed |
| `learning_complete` | +30 | Learning content completed |
| `daily_login` | +5 | User logs in |

## Testing Checklist

- [ ] Database initialized successfully
- [ ] Server starts without errors
- [ ] Engagement dashboard loads at `/static/engagement.html`
- [ ] Demo controls work and update stats
- [ ] Achievements unlock properly
- [ ] XP increases and level ups work
- [ ] Tutorials can be started and navigated
- [ ] Learning content loads
- [ ] Community stats display
- [ ] API endpoints return valid data

## Troubleshooting

### "Module not found" Error
Make sure you're in the project root directory:
```bash
cd /path/to/legend-ai-python
python scripts/init_engagement.py
```

### Database Connection Error
Check your `DATABASE_URL` in `.env`:
```bash
# SQLite (default)
DATABASE_URL=sqlite:///./legend_ai.db

# PostgreSQL
DATABASE_URL=postgresql://user:pass@localhost/legendai
```

### Static Files Not Loading
Ensure the `static` directory exists:
```bash
mkdir -p static
```

### API Returns Empty Data
Initialize the engagement system:
```bash
curl -X POST http://localhost:8000/api/engagement/admin/init
```

## What's Next?

1. **Customize Achievements**: Edit `app/services/engagement.py`
2. **Add Learning Content**: Update `app/services/learning_center.py`
3. **Create New Tutorials**: Add to `app/services/tutorial.py`
4. **Integrate with Authentication**: Replace `demo-user` with real user IDs
5. **Add Notifications**: Implement achievement notifications
6. **Track More Activities**: Add tracking to your existing endpoints

## API Documentation

Full API docs available at:
```
http://localhost:8000/docs#tag/engagement
```

Features interactive testing of all engagement endpoints!

## Support

Questions? Check out:
- Full documentation: `docs/ENGAGEMENT_FEATURES.md`
- API reference: `/docs#tag/engagement`
- Example dashboard: `/static/engagement.html`

Happy coding! 🚀
