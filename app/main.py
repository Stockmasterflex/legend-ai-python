from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import logging
import httpx

from app.config import get_settings
from app.api.telegram import router as telegram_router
from app.api.patterns import router as patterns_router
from app.api.charts import router as charts_router

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
    """Set up Telegram webhook"""
    try:
        webhook_url = f"{settings.telegram_webhook_url}/webhook/telegram"

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"https://api.telegram.org/bot{settings.telegram_bot_token}/setWebhook",
                json={"url": webhook_url}
            )

            if response.status_code == 200:
                logger.info(f"Telegram webhook set to: {webhook_url}")
            else:
                logger.error(f"Failed to set webhook: {response.text}")

    except Exception as e:
        logger.error(f"Error setting up webhook: {e}")

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
    """Detailed health check"""
    # Test Telegram connectivity
    telegram_status = "unknown"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"https://api.telegram.org/bot{settings.telegram_bot_token}/getMe"
            )
            telegram_status = "connected" if response.status_code == 200 else "error"
    except Exception:
        telegram_status = "disconnected"

    # Test Redis connectivity
    redis_status = "unknown"
    try:
        from app.services.cache import get_cache_service
        cache = get_cache_service()
        health_check = await cache.health_check()
        redis_status = health_check["status"]
    except Exception:
        redis_status = "disconnected"

    return {
        "status": "healthy",
        "telegram": telegram_status,
        "redis": redis_status,
        "version": "1.0.0",
        "webhook_url": settings.telegram_webhook_url
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
