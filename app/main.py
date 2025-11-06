from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import logging
import httpx

from app.config import get_settings
from app.api.telegram import router as telegram_router
from app.api.patterns import router as patterns_router
from app.api.charts import router as charts_router
from app.api.universe import router as universe_router

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

settings = get_settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    # Startup
    logger.info("Starting Legend AI Bot...")

    # Set webhook if URL provided (Phase 1.2)
    if settings.telegram_webhook_url:
        await setup_telegram_webhook()
        logger.info(f"Webhook URL configured: {settings.telegram_webhook_url}")

    logger.info("Bot started successfully!")

    yield

    # Shutdown
    logger.info("Shutting down...")

async def setup_telegram_webhook():
    """Set up Telegram webhook - non-blocking if not configured"""
    try:
        # Only set webhook if both URL and token are properly configured
        if not settings.telegram_webhook_url:
            logger.info("Telegram webhook URL not configured - skipping webhook setup")
            return
        
        if not settings.telegram_bot_token or settings.telegram_bot_token == "dev-token":
            logger.info("Telegram bot token not configured - skipping webhook setup")
            return

        webhook_url = f"{settings.telegram_webhook_url}/api/webhook/telegram"

        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(
                f"https://api.telegram.org/bot{settings.telegram_bot_token}/setWebhook",
                json={"url": webhook_url}
            )

            if response.status_code == 200:
                logger.info(f"✅ Telegram webhook set to: {webhook_url}")
            else:
                logger.warning(f"⚠️ Failed to set webhook: {response.status_code} - {response.text}")

    except Exception as e:
        logger.warning(f"⚠️ Error setting up webhook (non-critical): {e}")

# Create FastAPI app
app = FastAPI(
    title="Legend AI",
    description="Professional Trading Pattern Scanner",
    version="1.0.0",
    lifespan=lifespan
)

# Include API routers
app.include_router(telegram_router, prefix="/api", tags=["telegram"])
app.include_router(patterns_router)
app.include_router(charts_router)
app.include_router(universe_router)

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "running",
        "service": "Legend AI Bot",
        "version": "1.0.0",
        "phase": "1.1 - Project Setup"
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
