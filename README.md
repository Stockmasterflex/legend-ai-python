# Legend AI - Python FastAPI Conversion

**Status:** Phase 1.1 - Project Setup ✅
**Conversion Progress:** 0%
**Target Completion:** November 30, 2025

Professional trading pattern scanner converting from n8n workflows to Python FastAPI backend.

---

## ⚠️ IMPORTANT: Claude Code Development Branch

> **Always read `.claude-branch` file before starting work!**

This repository uses a dedicated development branch for Claude Code:
- **Development Branch**: `claude/initial-repo-review-011CUsBeQ3RGbnNF3EMZgqJ2` ✅ **USE THIS**
- **Production Branch**: `main` (merges only, no direct commits)

**Quick Check:**
```bash
cat .claude-branch                                    # Read branch name
git checkout $(cat .claude-branch)                   # Switch if needed
git status                                           # Verify correct branch
```

**CRITICAL**: All Claude Code commits MUST go to the claude branch, not main. See [`CLAUDE_CODE_WORKFLOW.md`](./CLAUDE_CODE_WORKFLOW.md) for complete instructions.

---

## 🚀 Quick Start

### 1. Setup Environment

```bash
# Clone or navigate to project
cd legend-ai

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your API keys
nano .env
```

**Required Environment Variables:**
- `TELEGRAM_BOT_TOKEN` - From BotFather
- `OPENROUTER_API_KEY` - From OpenRouter
- `CHARTIMG_API_KEY` - From Chart-IMG
- `TWELVEDATA_API_KEY` - From TwelveData
- `SECRET_KEY` - Generate a random string

### 3. Run Development Server

```bash
# Start FastAPI server
uvicorn app.main:app --reload

# Check health endpoint
curl http://localhost:8000/health
```

## 📋 Project Structure

```
legend-ai/
├── README.md                    # This file
├── requirements.txt             # Python dependencies
├── .env.example                 # Environment template
├── .gitignore                   # Git ignore rules
├── app/
│   ├── __init__.py
│   ├── main.py                  # FastAPI application
│   ├── config.py                # Settings management
│   ├── api/                     # API endpoints
│   │   ├── __init__.py
│   │   └── telegram.py          # Telegram webhook (Phase 1.2)
│   ├── core/                    # Business logic
│   │   ├── __init__.py
│   │   └── pattern_detector.py  # Pattern algorithms (Phase 1.3)
│   ├── services/                # External services
│   │   ├── __init__.py
│   │   └── telegram_service.py  # Telegram bot (Phase 1.2)
│   └── utils/                   # Utilities
│       └── __init__.py
├── tests/                       # Test suite
└── docs/                        # Documentation (future)
```

## 🎯 Current Phase: 1.1 - Project Setup

### ✅ Completed
- [x] Project directory structure
- [x] requirements.txt with dependencies
- [x] .env.example with all variables
- [x] .gitignore configuration
- [x] Basic FastAPI app with health endpoints
- [x] Pydantic settings configuration

### 🔄 Next Steps (Phase 1.2)
- [ ] Telegram webhook endpoint
- [ ] Bot command handling
- [ ] AI intent classification
- [ ] Basic pattern detection skeleton

## 🔑 Key Features

### Phase 1: Backend Foundation (Week 1)
- **Telegram Bot** - All commands working (/start, /scan, /pattern, /chart)
- **Pattern Scanner** - Fast async scanning of NASDAQ universe
- **Redis Caching** - 1-hour TTL, reduce API calls by 80%
- **Error Handling** - Robust, no silent failures

### Phase 2: Gradio MVP Dashboard (Week 2)
- **Web Interface** - Pattern scanning dashboard
- **Bulk Analysis** - Scan multiple tickers
- **Charts** - TradingView integration
- **Export** - CSV download functionality

### Phase 3: Professional UI (Week 3)
- **HTMX Interface** - No JavaScript complexity
- **Real-time Updates** - Live scanning progress
- **User Management** - Authentication system
- **Trade Journal** - Position tracking

### Phase 4: Polish & Launch (Week 4)
- **Testing** - Comprehensive test suite
- **Documentation** - API docs and user guide
- **Monitoring** - Health checks and alerts
- **Railway Deployment** - Production ready

## 🔧 Technical Stack

### Backend
- **FastAPI** - Modern async web framework
- **Pydantic** - Data validation and settings
- **Redis** - High-performance caching
- **httpx** - Async HTTP client

### Services
- **TwelveData** - Stock market data (800 calls/day)
- **OpenRouter** - AI models (GPT-4o-mini)
- **Chart-IMG** - TradingView charts (unlimited)
- **Telegram** - Bot interface (free)

### Deployment
- **Railway** - One-click deploy with PostgreSQL + Redis
- **Docker** - Containerized deployment
- **GitHub Actions** - CI/CD pipeline

## 📚 Additional Guides

- [`docs/TRADINGVIEW_WIDGETS.md`](docs/TRADINGVIEW_WIDGETS.md) – embed TradingView widgets (ticker tapes, advanced charts, heatmaps, etc.) inside Python dashboards using reusable HTML + tv.js.

## 📊 Performance Goals

| Metric | n8n Current | Python Target | Improvement |
|--------|-------------|---------------|-------------|
| Response Time | 20-30s | <5s | 6x faster |
| Cost/Month | $50+ | $5-10 | 80% savings |
| Reliability | ~90% | >99% | Much more stable |
| API Calls | 400/day limit | Unlimited | No limits |

## 🚨 Critical Notes

1. **DO NOT DELETE** n8n workflows until Python version is validated
2. **CACHE EVERYTHING** - We have strict API limits
3. **ERROR HANDLING** - Must be robust, this is production
4. **SECURITY** - Validate all webhook signatures
5. **PERFORMANCE** - Target <5s response times

## 📞 Support

- **Issues:** Check Railway logs first
- **API Keys:** Verify in Railway dashboard
- **Bot Problems:** Test with Telegram API directly
- **Performance:** Monitor Redis cache hit rates

## 🎯 Success Criteria

By November 30, 2025:
- [ ] All n8n features working in Python
- [ ] Web dashboard operational
- [ ] Deployed and running 24/7
- [ ] Costs under $10/month
- [ ] Response time under 5 seconds
- [ ] Zero downtime migration

## 📝 Development Log

### Phase 1.1 - Project Setup (Today)
- Created complete FastAPI project structure
- Configured all dependencies and environment variables
- Set up basic health endpoints
- Ready for Phase 1.2: Telegram Bot Logic

---

**Let's build something great! 🚀**
