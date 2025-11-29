"""
Monitoring service for collecting and exposing system metrics
Tracks database pools, API quotas, health checks, and application info
"""

import asyncio
import logging
import os
import time
from typing import Optional

import httpx

from app.config import get_settings
from app.telemetry.metrics import (ALERTS_SENT_TOTAL, API_QUOTA_LIMIT,
                                   APP_INFO, DB_CONNECTIONS_POOL_OVERFLOW,
                                   DB_CONNECTIONS_POOL_SIZE,
                                   DB_CONNECTIONS_TOTAL,
                                   HEALTH_CHECK_DURATION_SECONDS,
                                   HEALTH_CHECK_STATUS, UPTIME_SECONDS)

logger = logging.getLogger(__name__)
settings = get_settings()


class MonitoringService:
    """Service for collecting system monitoring metrics"""

    def __init__(self):
        self.start_time = time.time()
        self.settings = settings
        self._monitoring_task: Optional[asyncio.Task] = None

        # Initialize app info
        build_sha = os.getenv("RAILWAY_GIT_COMMIT_SHA", "dev")[:7]
        APP_INFO.info(
            {
                "version": "1.0.0",
                "build_sha": build_sha,
                "environment": (
                    "production"
                    if os.getenv("RAILWAY_PUBLIC_DOMAIN")
                    else "development"
                ),
            }
        )

    async def start_monitoring(self):
        """Start background monitoring tasks"""
        logger.info("🔍 Starting monitoring service...")
        self._monitoring_task = asyncio.create_task(self._monitor_loop())

    async def stop_monitoring(self):
        """Stop background monitoring tasks"""
        if self._monitoring_task:
            self._monitoring_task.cancel()
            try:
                await self._monitoring_task
            except asyncio.CancelledError:
                pass
        logger.info("🛑 Monitoring service stopped")

    async def _monitor_loop(self):
        """Main monitoring loop - runs every 60 seconds"""
        while True:
            try:
                await self.collect_metrics()
                await asyncio.sleep(60)  # Collect metrics every minute
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error in monitoring loop: {e}")
                await asyncio.sleep(60)

    async def collect_metrics(self):
        """Collect all system metrics"""
        try:
            # Update uptime
            uptime = time.time() - self.start_time
            UPTIME_SECONDS.set(uptime)

            # Collect database metrics
            await self._collect_db_metrics()

            # Collect API quota metrics
            await self._collect_api_quota_metrics()

            # Run health checks
            await self._run_health_checks()

        except Exception as e:
            logger.error(f"Error collecting metrics: {e}")

    async def _collect_db_metrics(self):
        """Collect database connection pool metrics"""
        try:
            from app.services.database import get_database_service

            db_service = get_database_service()

            if db_service and db_service.engine:
                pool = db_service.engine.pool

                # Get pool stats
                pool_size = pool.size()
                checked_out = pool.checkedout()
                overflow = pool.overflow()

                # Update metrics
                DB_CONNECTIONS_POOL_SIZE.set(pool_size)
                DB_CONNECTIONS_TOTAL.labels(state="total").set(pool_size)
                DB_CONNECTIONS_TOTAL.labels(state="active").set(checked_out)
                DB_CONNECTIONS_TOTAL.labels(state="idle").set(pool_size - checked_out)
                DB_CONNECTIONS_POOL_OVERFLOW.set(overflow)

                logger.debug(
                    f"DB Pool: size={pool_size}, active={checked_out}, idle={pool_size - checked_out}, overflow={overflow}"
                )

        except Exception as e:
            logger.warning(f"Could not collect DB metrics: {e}")

    async def _collect_api_quota_metrics(self):
        """Track API quota usage for external services"""
        try:
            # TwelveData quota
            if self.settings.twelvedata_api_key:
                API_QUOTA_LIMIT.labels(service="twelvedata").set(
                    self.settings.twelvedata_daily_limit
                )
                # Note: Actual usage tracking would require persistent storage
                # For now, we just set the limit

            # Finnhub quota
            if self.settings.finnhub_api_key:
                API_QUOTA_LIMIT.labels(service="finnhub").set(
                    self.settings.finnhub_daily_limit
                )

            # Alpha Vantage quota
            if self.settings.alpha_vantage_api_key:
                API_QUOTA_LIMIT.labels(service="alpha_vantage").set(
                    self.settings.alpha_vantage_daily_limit
                )

            # Chart-IMG quota
            if self.settings.chart_img_api_key:
                API_QUOTA_LIMIT.labels(service="chartimg").set(
                    self.settings.chartimg_daily_limit
                )

        except Exception as e:
            logger.warning(f"Could not collect API quota metrics: {e}")

    async def _run_health_checks(self):
        """Run health checks for all components"""
        # Database health check
        await self._check_database_health()

        # Redis health check
        await self._check_redis_health()

        # External APIs health check
        await self._check_external_apis_health()

    async def _check_database_health(self):
        """Check database connection health"""
        start_time = time.perf_counter()

        try:
            from app.services.database import get_database_service

            db_service = get_database_service()
            health = db_service.health_check()

            status = 1 if health.get("status") == "healthy" else 0
            HEALTH_CHECK_STATUS.labels(component="database").set(status)

            duration = time.perf_counter() - start_time
            HEALTH_CHECK_DURATION_SECONDS.labels(component="database").observe(duration)

        except Exception as e:
            HEALTH_CHECK_STATUS.labels(component="database").set(0)
            logger.warning(f"Database health check failed: {e}")

    async def _check_redis_health(self):
        """Check Redis connection health"""
        start_time = time.perf_counter()

        try:
            from app.services.cache import get_cache_service

            cache_service = get_cache_service()

            # Try to ping Redis
            # Use the internal redis client if available, or initialize it
            redis = await cache_service._get_redis()
            if redis:
                await redis.ping()
                HEALTH_CHECK_STATUS.labels(component="redis").set(1)
            else:
                HEALTH_CHECK_STATUS.labels(component="redis").set(0)

            duration = time.perf_counter() - start_time
            HEALTH_CHECK_DURATION_SECONDS.labels(component="redis").observe(duration)

        except Exception as e:
            HEALTH_CHECK_STATUS.labels(component="redis").set(0)
            logger.warning(f"Redis health check failed: {e}")

    async def _check_external_apis_health(self):
        """Check external API connectivity"""
        # Check market data APIs
        for api_name in ["twelvedata", "finnhub", "alpha_vantage"]:
            start_time = time.perf_counter()

            try:
                # Simple connectivity check (timeout after 5 seconds)
                async with httpx.AsyncClient(timeout=5) as client:
                    if api_name == "twelvedata":
                        url = "https://api.twelvedata.com/time_series"
                    elif api_name == "finnhub":
                        url = "https://finnhub.io/api/v1/quote"
                    else:  # alpha_vantage
                        url = "https://www.alphavantage.co/query"

                    # Just check if the endpoint is reachable
                    response = await client.get(url, params={"symbol": "AAPL"})

                    # Consider any response (even 401/403) as "API is up"
                    if response.status_code < 500:
                        HEALTH_CHECK_STATUS.labels(component=f"api_{api_name}").set(1)
                    else:
                        HEALTH_CHECK_STATUS.labels(component=f"api_{api_name}").set(0)

                duration = time.perf_counter() - start_time
                HEALTH_CHECK_DURATION_SECONDS.labels(
                    component=f"api_{api_name}"
                ).observe(duration)

            except Exception as e:
                HEALTH_CHECK_STATUS.labels(component=f"api_{api_name}").set(0)
                logger.debug(f"{api_name} health check failed: {e}")

    async def send_telegram_alert(
        self, message: str, alert_type: str = "system"
    ) -> bool:
        """Send a monitoring alert via Telegram"""
        try:
            if (
                not self.settings.telegram_bot_token
                or not self.settings.telegram_chat_id
            ):
                logger.warning("Telegram credentials not configured")
                return False

            url = f"https://api.telegram.org/bot{self.settings.telegram_bot_token}/sendMessage"

            payload = {
                "chat_id": self.settings.telegram_chat_id,
                "text": message,
                "parse_mode": "Markdown",
            }

            async with httpx.AsyncClient(timeout=10) as client:
                response = await client.post(url, json=payload)
                response.raise_for_status()

            ALERTS_SENT_TOTAL.labels(
                alert_type=alert_type, channel="telegram", status="success"
            ).inc()
            logger.info(f"Telegram alert sent successfully: {alert_type}")
            return True

        except Exception as e:
            ALERTS_SENT_TOTAL.labels(
                alert_type=alert_type, channel="telegram", status="failed"
            ).inc()
            logger.error(f"Failed to send Telegram alert: {e}")
            return False


# Global monitoring service instance
_monitoring_service: Optional[MonitoringService] = None


def get_monitoring_service() -> MonitoringService:
    """Get or create monitoring service singleton"""
    global _monitoring_service
    if _monitoring_service is None:
        _monitoring_service = MonitoringService()
    return _monitoring_service
