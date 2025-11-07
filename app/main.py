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
from app.api.dashboard import router as dashboard_router
from app.api.alerts import router as alerts_router
from app.api.multitimeframe import router as multitf_router
from app.api.risk import router as risk_router
from app.api.trades import router as trades_router

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

settings = get_settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    # Startup
    logger.info("Starting Legend AI Bot...")

    # Set webhook automatically
    await setup_telegram_webhook()

    logger.info("Bot started successfully!")

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

# Add CORS middleware to allow dashboard JavaScript to call APIs
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for dashboard
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

# Mount static files if they exist
static_path = Path(__file__).parent.parent / "static"
if static_path.exists():
    app.mount("/static", StaticFiles(directory=str(static_path)), name="static")
    logger.info(f"📁 Static files mounted from {static_path}")

@app.get("/")
async def root():
    """Root endpoint - redirects to dashboard"""
    return {
        "status": "running",
        "service": "Legend AI",
        "version": "1.0.0",
        "dashboard": "/dashboard",
        "docs": "/docs"
    }

@app.get("/health")
async def health():
    """Detailed health check - resilient to missing services"""
    # Test Telegram connectivity (non-blocking)
    telegram_status = "unknown"
    try:
        if settings.telegram_bot_token and settings.telegram_bot_token != "dev-token":
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(
                    f"https://api.telegram.org/bot{settings.telegram_bot_token}/getMe"
                )
                telegram_status = "connected" if response.status_code == 200 else "error"
        else:
            telegram_status = "not_configured"
    except Exception as e:
        logger.debug(f"Telegram health check failed: {e}")
        telegram_status = "disconnected"

    # Test Redis connectivity (non-blocking)
    redis_status = "unknown"
    try:
        from app.services.cache import get_cache_service
        cache = get_cache_service()
        health_check = await cache.health_check()
        redis_status = health_check.get("status", "unknown")
    except Exception as e:
        logger.debug(f"Redis health check failed: {e}")
        redis_status = "disconnected"

    # Always return healthy status - individual services can be down
    return {
        "status": "healthy",
        "telegram": telegram_status,
        "redis": redis_status,
        "version": "1.0.0",
        "webhook_url": settings.telegram_webhook_url if settings.telegram_webhook_url else None
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
