from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import logging
import httpx
import os
from pathlib import Path

from app.config import get_settings
from app.api.telegram_enhanced import router as telegram_router
from app.api.patterns import router as patterns_router
from app.api.charts import router as charts_router
from app.api.universe import router as universe_router
from app.api.watchlist import router as watchlist_router
from app.api.trade_plan import router as trade_router
from app.api.analytics import router as analytics_router
from app.api.market import router as market_router
from app.api.analyze import router as analyze_router
from app.api.dashboard import router as dashboard_router
from app.api.alerts import router as alerts_router
from app.api.multitimeframe import router as multitf_router
from app.api.risk import router as risk_router
from app.api.trades import router as trades_router
from app.api import analyze as analyze_pkg, watchlist as watchlist_pkg
from app.api.version import router as version_router
from app.api.metrics import router as metrics_router
from app.api.scan import router as scan_router
from app.api.tv import router as tv_router
from app.services.universe_store import universe_store
from app.middleware.structured_logging import StructuredLoggingMiddleware
from app.utils.build_info import resolve_build_sha

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    # Startup
    logger.info("Starting Legend AI Bot...")
    logger.info("API_ANALYZE_ENABLED=True")
    # Report presence of Chart-IMG API key (boolean only)
    try:
        logger.info(
            "key_presence chartimg=%s twelvedata=%s finnhub=%s alpha_vantage=%s redis=%s",
            bool(settings.chart_img_api_key),
            bool(settings.twelvedata_api_key),
            bool(settings.finnhub_api_key),
            bool(settings.alpha_vantage_api_key),
            bool(settings.redis_url),
        )
    except Exception as exc:
        logger.info("key_presence_error %s", exc)
    # Compute and expose short build SHA for cache-busting and header
    try:
        sha = resolve_build_sha()
    except Exception:
        sha = "unknown"
    os.environ["GIT_COMMIT"] = sha

    try:
        await universe_store.seed()
        logger.info("✅ Universe store seeded successfully")
    except Exception as exc:
        logger.warning("⚠️ Universe seed skipped (non-critical): %s", exc)

    # Set webhook automatically (non-critical, won't block startup)
    try:
        await setup_telegram_webhook()
    except Exception as exc:
        logger.warning("⚠️ Telegram webhook setup failed (non-critical): %s", exc)

    logger.info("✅ Bot started successfully!")

    yield

    # Shutdown
    logger.info("Shutting down...")

async def setup_telegram_webhook():
    """Set up Telegram webhook - auto-configures from Railway"""
    try:
        # Get bot token
        bot_token = settings.telegram_bot_token
        if not bot_token or bot_token == "dev-token":
            logger.warning("⚠️ Telegram bot token not configured - webhook not set")
            return

        # Get webhook URL (auto-detect from Railway or use configured)
        webhook_base = settings.auto_webhook_url
        webhook_url = f"{webhook_base}/api/webhook/telegram"  # /api prefix added by router registration

        logger.info(f"📡 Setting Telegram webhook to: {webhook_url}")

        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(
                f"https://api.telegram.org/bot{bot_token}/setWebhook",
                json={"url": webhook_url}
            )

            if response.status_code == 200:
                logger.info(f"✅ Telegram webhook successfully configured!")
                logger.info(f"   URL: {webhook_url}")
            else:
                logger.error(f"❌ Failed to set webhook: {response.status_code}")
                logger.error(f"   Response: {response.text}")

    except Exception as e:
        logger.error(f"❌ Error setting up webhook: {e}")

# Create FastAPI app
app = FastAPI(
    title="Legend AI",
    description="Professional Trading Pattern Scanner",
    version="1.0.0",
    lifespan=lifespan
)

# Structured logging sits at the top of the stack to capture everything
app.add_middleware(StructuredLoggingMiddleware)

# Add CORS middleware with environment-aware origin restrictions
# In production (Railway): only allows requests from the app's own domain
# In development: allows all origins for easier testing
allowed_origins = settings.allowed_origins
logger.info(f"🔒 CORS configured with allowed origins: {allowed_origins}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(telegram_router, prefix="/api", tags=["telegram"])
app.include_router(patterns_router)
app.include_router(charts_router)
app.include_router(universe_router)
app.include_router(watchlist_router)
app.include_router(trade_router)
app.include_router(analytics_router)
app.include_router(market_router)
app.include_router(alerts_router)
app.include_router(multitf_router)
app.include_router(risk_router)
app.include_router(trades_router)
app.include_router(dashboard_router, tags=["dashboard"])
app.include_router(analyze_router)
app.include_router(version_router)
app.include_router(metrics_router)
app.include_router(scan_router)
app.include_router(tv_router)

# Mount static files if they exist
static_path = Path(__file__).parent.parent / "static"
if static_path.exists():
    app.mount("/static", StaticFiles(directory=str(static_path)), name="static")
    logger.info(f"📁 Static files mounted from {static_path}")

@app.get("/")
async def root(request: Request):
    """Root endpoint - redirects to dashboard"""
    request.state.telemetry = {"event": "root", "status": 200}
    return {
        "status": "running",
        "service": "Legend AI",
        "version": "1.0.0",
        "dashboard": "/dashboard",
        "docs": "/docs"
    }

@app.get("/health")
async def health(request: Request):
    """
    Respond with a lightweight health payload.
    CRITICAL: This endpoint must NEVER fail - it's used for Railway healthchecks.
    All operations wrapped in try-except to ensure we always return 200 OK.
    """
    try:
        telegram_status = (
            "configured"
            if settings.telegram_bot_token and settings.telegram_bot_token != "dev-token"
            else "not_configured"
        )
    except Exception:
        telegram_status = "unknown"

    try:
        redis_status = (
            "configured"
            if settings.redis_url and not settings.redis_url.startswith("redis://localhost")
            else "not_configured"
        )
    except Exception:
        redis_status = "unknown"

    try:
        universe_status = {
            "seeded": bool(universe_store._memory),
            "cached_symbols": len(universe_store._memory),
        }
    except Exception:
        universe_status = {"seeded": False, "cached_symbols": 0}

    try:
        key_presence = {
            "chartimg": bool(settings.chart_img_api_key),
            "twelvedata": bool(settings.twelvedata_api_key),
            "finnhub": bool(settings.finnhub_api_key),
            "alpha_vantage": bool(settings.alpha_vantage_api_key),
        }
    except Exception:
        key_presence = {}

    try:
        version = resolve_build_sha()
    except Exception:
        version = "unknown"

    try:
        webhook_url = settings.telegram_webhook_url
    except Exception:
        webhook_url = None

    payload = {
        "status": "healthy",
        "telegram": telegram_status,
        "redis": redis_status,
        "version": version,
        "webhook_url": webhook_url,
        "universe": universe_status,
        "keys": key_presence,
        "analyze": {"cache_ttl": 3600},
    }

    try:
        request.state.telemetry = {
            "event": "health",
            "status": payload["status"],
            "symbol": None,
            "interval": None,
        }
    except Exception:
        pass  # Telemetry is not critical for health check

    return payload

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
