"""
Automated alerting service for monitoring metrics
Monitors error rates, response times, and system health
Sends Telegram alerts when thresholds are breached
"""
import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
from collections import defaultdict
import time

from prometheus_client import REGISTRY
from app.telemetry.monitoring import get_monitoring_service

logger = logging.getLogger(__name__)


class MonitoringAlerter:
    """Service for monitoring metrics and sending alerts"""

    def __init__(self):
        self.monitoring_service = get_monitoring_service()
        self._alerter_task: Optional[asyncio.Task] = None
        self._last_alerts: Dict[str, float] = {}  # Track when we last sent each alert
        self._alert_cooldown = 300  # 5 minutes between same alerts

        # Alert thresholds
        self.thresholds = {
            "error_rate_5xx": 10,  # More than 10 5xx errors in a minute
            "error_rate_4xx": 50,  # More than 50 4xx errors in a minute
            "response_time_p95": 5.0,  # 95th percentile > 5 seconds
            "db_connections_high": 0.8,  # 80% of pool used
            "health_check_failed": 2,  # 2 consecutive failures
            "api_quota_low": 0.9,  # 90% of quota used
        }

        # Tracking for consecutive failures
        self._health_failures: Dict[str, int] = defaultdict(int)
        self._last_metric_values: Dict[str, Any] = {}

    async def start_alerting(self):
        """Start background alerting tasks"""
        logger.info("🚨 Starting monitoring alerter...")
        self._alerter_task = asyncio.create_task(self._alerter_loop())

    async def stop_alerting(self):
        """Stop background alerting tasks"""
        if self._alerter_task:
            self._alerter_task.cancel()
            try:
                await self._alerter_task
            except asyncio.CancelledError:
                pass
        logger.info("🛑 Monitoring alerter stopped")

    async def _alerter_loop(self):
        """Main alerter loop - runs every 60 seconds"""
        await asyncio.sleep(60)  # Wait 1 minute before first check

        while True:
            try:
                await self._check_metrics_and_alert()
                await asyncio.sleep(60)  # Check every minute
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error in alerter loop: {e}")
                await asyncio.sleep(60)

    async def _check_metrics_and_alert(self):
        """Check all metrics and send alerts if thresholds are breached"""
        try:
            # Check error rates
            await self._check_error_rates()

            # Check response times
            await self._check_response_times()

            # Check database connections
            await self._check_database_connections()

            # Check health status
            await self._check_health_status()

            # Check API quotas
            await self._check_api_quotas()

        except Exception as e:
            logger.error(f"Error checking metrics: {e}")

    async def _check_error_rates(self):
        """Monitor error rates and alert if too high"""
        try:
            # Get error rate metrics from Prometheus registry
            for metric in REGISTRY.collect():
                if metric.name == "error_rate_total":
                    for sample in metric.samples:
                        if sample.name == "error_rate_total":
                            labels = sample.labels
                            value = sample.value

                            # Track rate of change
                            key = f"error_rate_{labels.get('severity', 'unknown')}"
                            last_value = self._last_metric_values.get(key, 0)
                            rate = value - last_value
                            self._last_metric_values[key] = value

                            # Check thresholds
                            severity = labels.get("severity", "unknown")
                            endpoint = labels.get("endpoint", "unknown")

                            if severity == "error" and rate > self.thresholds["error_rate_5xx"]:
                                await self._send_alert(
                                    alert_type="high_error_rate",
                                    message=f"⚠️ *High Error Rate Alert*\n\n"
                                            f"*Severity:* {severity}\n"
                                            f"*Endpoint:* {endpoint}\n"
                                            f"*Rate:* {rate:.0f} errors/min\n"
                                            f"*Threshold:* {self.thresholds['error_rate_5xx']}/min\n\n"
                                            f"*Time:* {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                                )

                            elif severity == "warning" and rate > self.thresholds["error_rate_4xx"]:
                                await self._send_alert(
                                    alert_type="high_4xx_rate",
                                    message=f"⚠️ *High 4xx Error Rate*\n\n"
                                            f"*Endpoint:* {endpoint}\n"
                                            f"*Rate:* {rate:.0f} errors/min\n"
                                            f"*Threshold:* {self.thresholds['error_rate_4xx']}/min\n\n"
                                            f"*Time:* {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                                )

        except Exception as e:
            logger.error(f"Error checking error rates: {e}")

    async def _check_response_times(self):
        """Monitor response times and alert if too slow"""
        try:
            for metric in REGISTRY.collect():
                if metric.name == "http_request_duration_seconds":
                    for sample in metric.samples:
                        # Check 95th percentile (0.95 quantile)
                        if "quantile" in sample.labels and sample.labels["quantile"] == "0.95":
                            endpoint = sample.labels.get("endpoint", "unknown")
                            p95 = sample.value

                            if p95 > self.thresholds["response_time_p95"]:
                                await self._send_alert(
                                    alert_type="slow_response_time",
                                    message=f"🐌 *Slow Response Time Alert*\n\n"
                                            f"*Endpoint:* {endpoint}\n"
                                            f"*P95 Latency:* {p95:.2f}s\n"
                                            f"*Threshold:* {self.thresholds['response_time_p95']}s\n\n"
                                            f"*Time:* {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                                )

        except Exception as e:
            logger.error(f"Error checking response times: {e}")

    async def _check_database_connections(self):
        """Monitor database connection pool usage"""
        try:
            pool_size = 0
            active_connections = 0

            for metric in REGISTRY.collect():
                if metric.name == "db_connections_pool_size":
                    for sample in metric.samples:
                        pool_size = sample.value

                elif metric.name == "db_connections_total":
                    for sample in metric.samples:
                        if sample.labels.get("state") == "active":
                            active_connections = sample.value

            if pool_size > 0:
                usage_ratio = active_connections / pool_size

                if usage_ratio > self.thresholds["db_connections_high"]:
                    await self._send_alert(
                        alert_type="high_db_connections",
                        message=f"🗄️ *Database Connection Pool Alert*\n\n"
                                f"*Active Connections:* {active_connections:.0f}\n"
                                f"*Pool Size:* {pool_size:.0f}\n"
                                f"*Usage:* {usage_ratio:.1%}\n"
                                f"*Threshold:* {self.thresholds['db_connections_high']:.0%}\n\n"
                                f"*Action:* Consider increasing pool size or investigating connection leaks\n\n"
                                f"*Time:* {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                    )

        except Exception as e:
            logger.error(f"Error checking database connections: {e}")

    async def _check_health_status(self):
        """Monitor health check status"""
        try:
            for metric in REGISTRY.collect():
                if metric.name == "health_check_status":
                    for sample in metric.samples:
                        component = sample.labels.get("component", "unknown")
                        status = sample.value

                        if status == 0:
                            # Increment failure counter
                            self._health_failures[component] += 1

                            if self._health_failures[component] >= self.thresholds["health_check_failed"]:
                                await self._send_alert(
                                    alert_type=f"health_check_failed_{component}",
                                    message=f"❌ *Health Check Failed*\n\n"
                                            f"*Component:* {component}\n"
                                            f"*Status:* Unhealthy\n"
                                            f"*Consecutive Failures:* {self._health_failures[component]}\n\n"
                                            f"*Action:* Investigate {component} connectivity and configuration\n\n"
                                            f"*Time:* {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                                )
                        else:
                            # Reset failure counter if healthy
                            if component in self._health_failures:
                                self._health_failures[component] = 0

        except Exception as e:
            logger.error(f"Error checking health status: {e}")

    async def _check_api_quotas(self):
        """Monitor API quota usage"""
        try:
            for metric in REGISTRY.collect():
                if metric.name == "api_quota_used":
                    for sample in metric.samples:
                        service = sample.labels.get("service", "unknown")
                        used = sample.value

                        # Find the limit for this service
                        limit = None
                        for limit_metric in REGISTRY.collect():
                            if limit_metric.name == "api_quota_limit":
                                for limit_sample in limit_metric.samples:
                                    if limit_sample.labels.get("service") == service:
                                        limit = limit_sample.value
                                        break

                        if limit and limit > 0:
                            usage_ratio = used / limit

                            if usage_ratio > self.thresholds["api_quota_low"]:
                                await self._send_alert(
                                    alert_type=f"api_quota_low_{service}",
                                    message=f"📊 *API Quota Alert*\n\n"
                                            f"*Service:* {service}\n"
                                            f"*Used:* {used:.0f}\n"
                                            f"*Limit:* {limit:.0f}\n"
                                            f"*Usage:* {usage_ratio:.1%}\n"
                                            f"*Remaining:* {limit - used:.0f}\n\n"
                                            f"*Action:* Monitor usage or upgrade quota\n\n"
                                            f"*Time:* {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                                )

        except Exception as e:
            logger.error(f"Error checking API quotas: {e}")

    async def _send_alert(self, alert_type: str, message: str):
        """Send alert with cooldown to avoid spam"""
        # Check cooldown
        last_alert = self._last_alerts.get(alert_type, 0)
        now = time.time()

        if now - last_alert < self._alert_cooldown:
            logger.debug(f"Skipping alert {alert_type} (cooldown)")
            return

        # Send the alert
        success = await self.monitoring_service.send_telegram_alert(message, alert_type)

        if success:
            self._last_alerts[alert_type] = now


# Global alerter instance
_alerter: Optional[MonitoringAlerter] = None


def get_alerter() -> MonitoringAlerter:
    """Get or create alerter singleton"""
    global _alerter
    if _alerter is None:
        _alerter = MonitoringAlerter()
    return _alerter
