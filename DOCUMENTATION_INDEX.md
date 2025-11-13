# Documentation Index

**All documentation for Legend AI - Find what you need quickly**

---

## 🎯 Start Here

**New to the project?** Start with these in order:

1. **[GETTING_STARTED.md](./GETTING_STARTED.md)** ← Start here
   - 45-minute quick start guide
   - Architecture overview
   - What each file does
   - Basic troubleshooting

2. **[LOCAL_SETUP.md](./LOCAL_SETUP.md)** 
   - Step-by-step local development setup
   - Docker configuration
   - Running the API locally
   - Testing endpoints

3. **[DEPLOYMENT_STATUS.md](./DEPLOYMENT_STATUS.md)**
   - Current project state
   - Immediate next steps (3 steps)
   - Phase 1.2 enhancements
   - Security checklist

---

## 📚 Reference Guides

### API Documentation
- **[API_REFERENCE.md](./API_REFERENCE.md)** - Complete API documentation
  - All 44+ endpoints documented
  - Request/response examples
  - Curl command examples
  - Rate limiting info

### Deployment & Infrastructure
- **[DEPLOYMENT_STATUS.md](./DEPLOYMENT_STATUS.md)** - Deployment guide
  - Railway setup instructions
  - Environment variables
  - Production verification
  - Troubleshooting

### Project Planning
- **[ROADMAP.md](./ROADMAP.md)** - Full development roadmap
  - Phase 1, 2, 3, 4 breakdown
  - Timeline and milestones
  - Success metrics
  - Resource planning

### Advanced Topics
- **[docs/TRADINGVIEW_WIDGETS.md](./docs/TRADINGVIEW_WIDGETS.md)** - Dashboard widgets
  - Embedding TradingView charts
  - Widget configuration
  - HTML templates
  - JavaScript integration

---

## 📁 Project Structure

```
legend-ai-python/
│
├── 📖 Documentation
│   ├── GETTING_STARTED.md         ← Start here
│   ├── LOCAL_SETUP.md              Step-by-step setup
│   ├── API_REFERENCE.md            All endpoints
│   ├── DEPLOYMENT_STATUS.md        Current state & next steps
│   ├── ROADMAP.md                  Phase 1-4 plan
│   ├── DOCUMENTATION_INDEX.md      This file
│   ├── README.md                   Project overview
│   └── docs/
│       └── TRADINGVIEW_WIDGETS.md  Widget integration
│
├── 🔧 Configuration
│   ├── .env                        Local config (KEEP SECRET)
│   ├── .env.example                Template for others
│   ├── railway.toml                Railway deployment config
│   ├── Dockerfile                  Container config
│   ├── docker-compose.yml          Local services config
│   └── requirements.txt            Python dependencies
│
├── 💻 Application Code
│   ├── app/
│   │   ├── main.py                 FastAPI entry point
│   │   ├── config.py               Settings management
│   │   ├── models.py               Pydantic models
│   │   ├── api/                    14 routers, 44+ endpoints
│   │   │   ├── patterns.py         Pattern detection
│   │   │   ├── market.py           Market analysis
│   │   │   ├── charts.py           Chart generation
│   │   │   ├── universe.py         Universe scanning
│   │   │   ├── risk.py             Risk calculations
│   │   │   ├── trades.py           Trade management
│   │   │   ├── telegram_enhanced.py Bot webhook
│   │   │   ├── alerts.py           Alert system
│   │   │   ├── multitimeframe.py   Multi-TF analysis
│   │   │   ├── watchlist.py        Watchlist
│   │   │   ├── analytics.py        Performance tracking
│   │   │   ├── trade_plan.py       Trade planning
│   │   │   └── dashboard.py        Web dashboard
│   │   ├── core/                   Business logic
│   │   │   ├── pattern_detector.py Core algorithm
│   │   │   └── chart_generator.py  Chart generation
│   │   └── services/               External integrations
│   │       ├── market_data.py      Data fetching
│   │       ├── cache.py            Redis caching
│   │       ├── database.py         PostgreSQL ORM
│   │       └── [+7 more services]
│   │
│   └── tests/                      Test suite (future)
│
└── 📋 Meta Files
    ├── .gitignore
    ├── .claude-branch              Development branch name
    ├── CLAUDE_CODE_WORKFLOW.md     Claude Code specific setup
    └── LICENSE
```

---

## 🔍 Finding What You Need

### "I want to..."

#### Learn About the Project
- **Understand what Legend AI does**: [README.md](./README.md)
- **Get a quick overview**: [GETTING_STARTED.md](./GETTING_STARTED.md)
- **See the full plan**: [ROADMAP.md](./ROADMAP.md)

#### Set Up Locally
- **Step-by-step setup**: [LOCAL_SETUP.md](./LOCAL_SETUP.md)
- **Troubleshoot issues**: [LOCAL_SETUP.md](./LOCAL_SETUP.md#troubleshooting)
- **Understand configuration**: `.env` and `.env.example`

#### Deploy to Production
- **Deploy to Railway**: [DEPLOYMENT_STATUS.md](./DEPLOYMENT_STATUS.md) → Step 3
- **View deployment config**: `railway.toml`
- **Build Docker image**: `Dockerfile`

#### Use the API
- **Find an endpoint**: [API_REFERENCE.md](./API_REFERENCE.md)
- **See examples**: Curl commands in [API_REFERENCE.md](./API_REFERENCE.md)
- **Understand response format**: [API_REFERENCE.md](./API_REFERENCE.md#response-format)

#### Customize the Dashboard
- **Add TradingView widgets**: [docs/TRADINGVIEW_WIDGETS.md](./docs/TRADINGVIEW_WIDGETS.md)
- **Change dashboard HTML**: `app/api/dashboard.py` → `HTML_DASHBOARD` variable

#### Develop New Features
- **Add new API endpoint**: Create file in `app/api/` following pattern in existing files
- **Add business logic**: Add to `app/core/` or `app/services/`
- **Understand architecture**: [GETTING_STARTED.md](./GETTING_STARTED.md#-understanding-the-architecture)

#### Debug Issues
- **Something isn't working**: [LOCAL_SETUP.md](./LOCAL_SETUP.md#troubleshooting)
- **Production errors**: [DEPLOYMENT_STATUS.md](./DEPLOYMENT_STATUS.md) → Troubleshooting
- **API not responding**: [API_REFERENCE.md](./API_REFERENCE.md#rate-limits)

---

## 📈 Phase-Based Documentation

### Phase 1.1 (Setup) - COMPLETE ✅
- Project structure and code
- All documentation created
- Ready for Phase 1.2

**Key files**: Everything in this repo

### Phase 1.2 (Bot & Refinement) - IN PROGRESS 🔄
- Telegram bot commands enhancement
- Pattern detection refinement
- Cache optimization

**Read**: [ROADMAP.md](./ROADMAP.md#phase-12-telegram-bot--pattern-refinement-days-2-3)

### Phase 2 (Gradio Dashboard) - UPCOMING
- MVP web dashboard
- Pattern scanner UI
- Trade journal viewer

**Read**: [ROADMAP.md](./ROADMAP.md#phase-2-gradio-mvp-dashboard-week-2)

### Phase 3 (HTMX UI) - UPCOMING
- Professional web interface
- User authentication
- Advanced features

**Read**: [ROADMAP.md](./ROADMAP.md#phase-3-professional-htmx-ui-week-3)

### Phase 4 (Testing & Launch) - UPCOMING
- Comprehensive testing
- Production hardening
- Public launch

**Read**: [ROADMAP.md](./ROADMAP.md#phase-4-testing-docs--launch-week-4)

---

## 🎓 Learning Paths

### For Traders
1. [GETTING_STARTED.md](./GETTING_STARTED.md) - What is this?
2. [LOCAL_SETUP.md](./LOCAL_SETUP.md) - Get it running
3. [API_REFERENCE.md](./API_REFERENCE.md) - Use the endpoints
4. [ROADMAP.md](./ROADMAP.md) → Phase 2 - Upcoming dashboard

### For Developers
1. [GETTING_STARTED.md](./GETTING_STARTED.md#-understanding-the-architecture) - Architecture
2. [API_REFERENCE.md](./API_REFERENCE.md) - API structure
3. Review code in `app/api/` and `app/core/`
4. [ROADMAP.md](./ROADMAP.md) - What to build next
5. [docs/TRADINGVIEW_WIDGETS.md](./docs/TRADINGVIEW_WIDGETS.md) - Dashboard customization

### For DevOps
1. `Dockerfile` - Container setup
2. `docker-compose.yml` - Local services
3. `railway.toml` - Deployment config
4. [DEPLOYMENT_STATUS.md](./DEPLOYMENT_STATUS.md) - Production setup
5. [ROADMAP.md](./ROADMAP.md) → Phase 4 - Monitoring

---

## 🔄 Git & Version Control

**Claude Code Development Branch**:
- Check current branch: `cat .claude-branch`
- All development happens here: `claude/initial-repo-review-011CUsBeQ3RGbnNF3EMZgqJ2`
- Never commit to `main` directly
- See [CLAUDE_CODE_WORKFLOW.md](./CLAUDE_CODE_WORKFLOW.md) for details

---

## 📊 Quick Reference

### Critical Commands

**Start Local Development**:
```bash
source venv/bin/activate
docker compose up -d
uvicorn app.main:app --reload
```

**Test API**:
```bash
curl http://localhost:8000/health
curl -X POST http://localhost:8000/api/patterns/detect \
  -H "Content-Type: application/json" \
  -d '{"ticker": "NVDA"}'
```

**Deploy to Railway**:
```bash
railway login
railway deploy
railway logs --follow
```

### Key Files to Know

| File | Purpose |
|------|---------|
| `app/main.py` | FastAPI entry point |
| `.env` | Your secrets (DON'T commit) |
| `requirements.txt` | Python dependencies |
| `railway.toml` | Deployment configuration |
| `docker-compose.yml` | Local services |

---

## 💡 Pro Tips

1. **Use API_REFERENCE.md** when you need to call an endpoint
2. **Check LOCAL_SETUP.md** before trying something new
3. **Review ROADMAP.md** to understand what comes next
4. **Read GETTING_STARTED.md** if you're confused about overall architecture
5. **Monitor Railway logs** when deploying: `railway logs --follow`

---

## 🆘 Getting Help

1. **Can't get it running locally?** → [LOCAL_SETUP.md#troubleshooting](./LOCAL_SETUP.md#troubleshooting)
2. **API endpoint not working?** → [API_REFERENCE.md](./API_REFERENCE.md)
3. **Deployment issues?** → [DEPLOYMENT_STATUS.md](./DEPLOYMENT_STATUS.md)
4. **What should I build next?** → [ROADMAP.md](./ROADMAP.md)
5. **Confused about architecture?** → [GETTING_STARTED.md](./GETTING_STARTED.md)

---

## 📝 Documentation Status

| Document | Status | Last Updated |
|----------|--------|--------------|
| GETTING_STARTED.md | ✅ Complete | Nov 6, 2025 |
| LOCAL_SETUP.md | ✅ Complete | Nov 6, 2025 |
| API_REFERENCE.md | ✅ Complete | Nov 6, 2025 |
| DEPLOYMENT_STATUS.md | ✅ Complete | Nov 6, 2025 |
| ROADMAP.md | ✅ Complete | Nov 6, 2025 |
| TRADINGVIEW_WIDGETS.md | ✅ Updated | Nov 6, 2025 |
| README.md | ✅ Current | Nov 6, 2025 |

---

## 🎯 Next Steps

1. **Read**: [GETTING_STARTED.md](./GETTING_STARTED.md) (5 min)
2. **Follow**: [LOCAL_SETUP.md](./LOCAL_SETUP.md) (15 min)
3. **Deploy**: [DEPLOYMENT_STATUS.md](./DEPLOYMENT_STATUS.md) (20 min)
4. **Explore**: [API_REFERENCE.md](./API_REFERENCE.md) (10 min)
5. **Plan**: [ROADMAP.md](./ROADMAP.md) (ongoing)

---

**Happy building! 🚀**
