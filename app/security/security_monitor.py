"""
Security Monitoring and Alerting System
Real-time security event detection and Telegram notifications
"""
import logging
import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from redis.asyncio import Redis
import json

from app.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


class SecurityMonitor:
    """
    Real-time security monitoring and alerting.

    Features:
    - Failed authentication tracking
    - Suspicious activity detection
    - Brute force detection
    - Security event logging
    - Telegram alerts for critical events
    """

    # Alert thresholds
    FAILED_AUTH_THRESHOLD = 5  # Failed attempts before alert
    FAILED_AUTH_WINDOW = 300  # 5 minutes
    BRUTE_FORCE_THRESHOLD = 10  # Attempts before considering brute force
    BRUTE_FORCE_WINDOW = 600  # 10 minutes
    SUSPICIOUS_ACTIVITY_THRESHOLD = 3  # Different suspicious events

    # Event severity levels
    SEVERITY_LOW = "low"
    SEVERITY_MEDIUM = "medium"
    SEVERITY_HIGH = "high"
    SEVERITY_CRITICAL = "critical"

    def __init__(self):
        self.redis: Optional[Redis] = None

    async def _get_redis(self) -> Redis:
        """Get Redis connection (lazy initialization)"""
        if self.redis is None:
            self.redis = Redis.from_url(settings.redis_url, decode_responses=True)
        return self.redis

    async def log_security_event(
        self,
        event_type: str,
        severity: str,
        details: Dict,
        ip_address: Optional[str] = None
    ):
        """
        Log a security event and trigger alerts if needed.

        Args:
            event_type: Type of security event
            severity: Event severity (low, medium, high, critical)
            details: Event details dictionary
            ip_address: Source IP address
        """
        redis = await self._get_redis()

        # Create event record
        event = {
            "type": event_type,
            "severity": severity,
            "timestamp": datetime.utcnow().isoformat(),
            "ip_address": ip_address,
            "details": details
        }

        try:
            # Store event in time series
            event_key = f"security:events:{datetime.utcnow().strftime('%Y%m%d')}"
            await redis.lpush(event_key, json.dumps(event))
            await redis.expire(event_key, 86400 * 30)  # Keep 30 days

            # Store by IP for pattern detection
            if ip_address:
                ip_key = f"security:ip:{ip_address}"
                await redis.lpush(ip_key, json.dumps(event))
                await redis.expire(ip_key, 86400)  # Keep 24 hours

            # Log to application logger
            log_msg = f"🔒 Security Event: {event_type} | Severity: {severity} | IP: {ip_address}"
            if severity == self.SEVERITY_CRITICAL:
                logger.critical(log_msg)
            elif severity == self.SEVERITY_HIGH:
                logger.error(log_msg)
            elif severity == self.SEVERITY_MEDIUM:
                logger.warning(log_msg)
            else:
                logger.info(log_msg)

            # Send alert for high/critical events
            if severity in [self.SEVERITY_HIGH, self.SEVERITY_CRITICAL]:
                await self._send_security_alert(event)

            # Check for patterns that indicate attacks
            if ip_address:
                await self._check_attack_patterns(ip_address)

        except Exception as e:
            logger.error(f"Failed to log security event: {e}")

    async def log_failed_authentication(
        self,
        ip_address: str,
        username: Optional[str] = None,
        reason: str = "invalid_credentials"
    ):
        """
        Log failed authentication attempt.

        Args:
            ip_address: Source IP
            username: Attempted username
            reason: Failure reason
        """
        await self.log_security_event(
            event_type="failed_authentication",
            severity=self.SEVERITY_MEDIUM,
            details={
                "username": username,
                "reason": reason
            },
            ip_address=ip_address
        )

        # Check for brute force
        await self._check_brute_force(ip_address)

    async def log_suspicious_activity(
        self,
        ip_address: str,
        activity_type: str,
        details: Dict
    ):
        """
        Log suspicious activity.

        Args:
            ip_address: Source IP
            activity_type: Type of suspicious activity
            details: Activity details
        """
        await self.log_security_event(
            event_type="suspicious_activity",
            severity=self.SEVERITY_HIGH,
            details={
                "activity_type": activity_type,
                **details
            },
            ip_address=ip_address
        )

    async def log_rate_limit_violation(
        self,
        ip_address: str,
        endpoint: str,
        limit: int
    ):
        """
        Log rate limit violation.

        Args:
            ip_address: Source IP
            endpoint: Endpoint that was rate limited
            limit: Rate limit that was exceeded
        """
        await self.log_security_event(
            event_type="rate_limit_violation",
            severity=self.SEVERITY_LOW,
            details={
                "endpoint": endpoint,
                "limit": limit
            },
            ip_address=ip_address
        )

    async def _check_brute_force(self, ip_address: str):
        """
        Check if IP is attempting brute force attack.

        Args:
            ip_address: IP to check
        """
        redis = await self._get_redis()

        try:
            # Count failed auth attempts in window
            ip_key = f"security:ip:{ip_address}"
            events = await redis.lrange(ip_key, 0, -1)

            # Count failed auth events in last 10 minutes
            cutoff_time = datetime.utcnow() - timedelta(seconds=self.BRUTE_FORCE_WINDOW)
            failed_auth_count = 0

            for event_json in events:
                event = json.loads(event_json)
                event_time = datetime.fromisoformat(event["timestamp"])

                if event_time > cutoff_time and event["type"] == "failed_authentication":
                    failed_auth_count += 1

            # Alert if threshold exceeded
            if failed_auth_count >= self.BRUTE_FORCE_THRESHOLD:
                await self.log_security_event(
                    event_type="brute_force_detected",
                    severity=self.SEVERITY_CRITICAL,
                    details={
                        "failed_attempts": failed_auth_count,
                        "window_seconds": self.BRUTE_FORCE_WINDOW
                    },
                    ip_address=ip_address
                )

                logger.critical(
                    f"🚨 BRUTE FORCE ATTACK DETECTED from {ip_address} "
                    f"({failed_auth_count} failed attempts in {self.BRUTE_FORCE_WINDOW}s)"
                )

        except Exception as e:
            logger.error(f"Brute force check error: {e}")

    async def _check_attack_patterns(self, ip_address: str):
        """
        Check for attack patterns from an IP.

        Args:
            ip_address: IP to check
        """
        redis = await self._get_redis()

        try:
            # Get recent events from this IP
            ip_key = f"security:ip:{ip_address}"
            events = await redis.lrange(ip_key, 0, 99)

            if len(events) < self.SUSPICIOUS_ACTIVITY_THRESHOLD:
                return

            # Analyze event types
            event_types = set()
            recent_events = []

            cutoff_time = datetime.utcnow() - timedelta(seconds=300)  # Last 5 minutes

            for event_json in events:
                event = json.loads(event_json)
                event_time = datetime.fromisoformat(event["timestamp"])

                if event_time > cutoff_time:
                    event_types.add(event["type"])
                    recent_events.append(event)

            # Check for multiple different suspicious events
            suspicious_types = {
                "failed_authentication",
                "rate_limit_violation",
                "suspicious_activity",
                "sql_injection_attempt",
                "xss_attempt",
                "path_traversal_attempt"
            }

            suspicious_event_count = len(event_types & suspicious_types)

            if suspicious_event_count >= self.SUSPICIOUS_ACTIVITY_THRESHOLD:
                logger.critical(
                    f"🚨 ATTACK PATTERN DETECTED from {ip_address} "
                    f"({suspicious_event_count} different attack types)"
                )

                await self.log_security_event(
                    event_type="attack_pattern_detected",
                    severity=self.SEVERITY_CRITICAL,
                    details={
                        "attack_types": list(event_types & suspicious_types),
                        "event_count": len(recent_events)
                    },
                    ip_address=ip_address
                )

        except Exception as e:
            logger.error(f"Attack pattern check error: {e}")

    async def _send_security_alert(self, event: Dict):
        """
        Send security alert via Telegram.

        Args:
            event: Security event to alert on
        """
        try:
            # Import here to avoid circular dependency
            from app.infra.telegram import send_message

            # Format alert message
            severity_emoji = {
                self.SEVERITY_LOW: "ℹ️",
                self.SEVERITY_MEDIUM: "⚠️",
                self.SEVERITY_HIGH: "🚨",
                self.SEVERITY_CRITICAL: "🔥"
            }

            emoji = severity_emoji.get(event["severity"], "🔔")

            message = f"""{emoji} **SECURITY ALERT**

**Type:** {event['type'].replace('_', ' ').title()}
**Severity:** {event['severity'].upper()}
**Time:** {event['timestamp']}
**IP:** {event.get('ip_address', 'N/A')}

**Details:**
{json.dumps(event['details'], indent=2)}
"""

            # Send to Telegram (non-blocking)
            asyncio.create_task(send_message(message))

        except Exception as e:
            logger.error(f"Failed to send security alert: {e}")

    async def get_security_summary(self, hours: int = 24) -> Dict:
        """
        Get security summary for the last N hours.

        Args:
            hours: Number of hours to summarize

        Returns:
            Security summary dictionary
        """
        redis = await self._get_redis()

        try:
            # Get events from the last N hours
            summary = {
                "total_events": 0,
                "by_severity": {
                    self.SEVERITY_LOW: 0,
                    self.SEVERITY_MEDIUM: 0,
                    self.SEVERITY_HIGH: 0,
                    self.SEVERITY_CRITICAL: 0
                },
                "by_type": {},
                "top_ips": {},
                "period_hours": hours,
                "generated_at": datetime.utcnow().isoformat()
            }

            # Get today's events
            event_key = f"security:events:{datetime.utcnow().strftime('%Y%m%d')}"
            events = await redis.lrange(event_key, 0, -1)

            cutoff_time = datetime.utcnow() - timedelta(hours=hours)

            for event_json in events:
                event = json.loads(event_json)
                event_time = datetime.fromisoformat(event["timestamp"])

                if event_time > cutoff_time:
                    summary["total_events"] += 1

                    # Count by severity
                    severity = event.get("severity", self.SEVERITY_LOW)
                    summary["by_severity"][severity] = summary["by_severity"].get(severity, 0) + 1

                    # Count by type
                    event_type = event.get("type", "unknown")
                    summary["by_type"][event_type] = summary["by_type"].get(event_type, 0) + 1

                    # Track IPs
                    ip = event.get("ip_address")
                    if ip:
                        summary["top_ips"][ip] = summary["top_ips"].get(ip, 0) + 1

            # Sort top IPs
            summary["top_ips"] = dict(
                sorted(summary["top_ips"].items(), key=lambda x: x[1], reverse=True)[:10]
            )

            return summary

        except Exception as e:
            logger.error(f"Failed to generate security summary: {e}")
            return {"error": str(e)}

    async def generate_daily_security_report(self):
        """
        Generate and send daily security report via Telegram.
        Should be called via cron/scheduler.
        """
        try:
            summary = await self.get_security_summary(hours=24)

            # Format report
            report = f"""📊 **DAILY SECURITY REPORT**

**Period:** Last 24 hours
**Generated:** {summary['generated_at']}

**Overview:**
• Total Events: {summary['total_events']}
• Critical: {summary['by_severity']['critical']}
• High: {summary['by_severity']['high']}
• Medium: {summary['by_severity']['medium']}
• Low: {summary['by_severity']['low']}

**Event Types:**
"""

            for event_type, count in sorted(summary['by_type'].items(), key=lambda x: x[1], reverse=True):
                report += f"• {event_type.replace('_', ' ').title()}: {count}\n"

            if summary['top_ips']:
                report += "\n**Top Source IPs:**\n"
                for ip, count in list(summary['top_ips'].items())[:5]:
                    report += f"• {ip}: {count} events\n"

            # Send report
            from app.infra.telegram import send_message
            await send_message(report)

            logger.info("✅ Daily security report sent")

        except Exception as e:
            logger.error(f"Failed to generate daily report: {e}")


# Global instance
security_monitor = SecurityMonitor()
