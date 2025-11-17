"""
Application lifecycle management - startup and shutdown events
"""
import logging
import os
from contextlib import asynccontextmanager
from typing import AsyncIterator

import httpx
from fastapi import FastAPI

from app.config import get_settings
from app.services.universe_store import universe_store
from app.utils.build_info import resolve_build_sha

logger = logging.getLogger(__name__)
settings = get_settings()


async def setup_telegram_webhook() -> None:
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


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Startup and shutdown events"""
    # === STARTUP ===
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

    # Seed universe store
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

    # === SHUTDOWN ===
    logger.info("Shutting down...")
