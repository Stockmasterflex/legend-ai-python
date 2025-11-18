"""
Secrets Management System
Handles secret rotation, detection in commits, and audit logging
"""
import re
import logging
import hashlib
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Set
from redis.asyncio import Redis
import json

from app.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


class SecretsManager:
    """
    Secure secrets management.

    Features:
    - Secret rotation reminders
    - Detect secrets in code commits
    - Audit secret access logs
    - Secret strength validation
    """

    # Patterns to detect secrets in code
    SECRET_PATTERNS = {
        "api_key": [
            r"api[_-]?key['\"]?\s*[:=]\s*['\"]([a-zA-Z0-9_-]{20,})['\"]",
            r"apikey['\"]?\s*[:=]\s*['\"]([a-zA-Z0-9_-]{20,})['\"]",
            r"api[_-]?secret['\"]?\s*[:=]\s*['\"]([a-zA-Z0-9_-]{20,})['\"]",
        ],
        "password": [
            r"password['\"]?\s*[:=]\s*['\"]([^'\"]{8,})['\"]",
            r"passwd['\"]?\s*[:=]\s*['\"]([^'\"]{8,})['\"]",
            r"pwd['\"]?\s*[:=]\s*['\"]([^'\"]{8,})['\"]",
        ],
        "token": [
            r"token['\"]?\s*[:=]\s*['\"]([a-zA-Z0-9_-]{20,})['\"]",
            r"auth[_-]?token['\"]?\s*[:=]\s*['\"]([a-zA-Z0-9_-]{20,})['\"]",
            r"bearer['\"]?\s*[:=]\s*['\"]([a-zA-Z0-9_-]{20,})['\"]",
        ],
        "private_key": [
            r"-----BEGIN (RSA |EC )?PRIVATE KEY-----",
            r"private[_-]?key['\"]?\s*[:=]\s*['\"]([a-zA-Z0-9_-]{20,})['\"]",
        ],
        "aws": [
            r"AKIA[0-9A-Z]{16}",  # AWS Access Key
            r"aws[_-]?secret[_-]?access[_-]?key['\"]?\s*[:=]\s*['\"]([a-zA-Z0-9/+=]{40})['\"]",
        ],
        "database": [
            r"(postgres|mysql|mongodb)://[^:]+:[^@]+@",
            r"database[_-]?url['\"]?\s*[:=]\s*['\"]([^'\"]+@[^'\"]+)['\"]",
        ],
    }

    # Rotation periods (days)
    ROTATION_PERIODS = {
        "api_key": 90,
        "password": 90,
        "token": 60,
        "private_key": 365,
        "database": 180,
    }

    def __init__(self):
        self.redis: Optional[Redis] = None

    async def _get_redis(self) -> Redis:
        """Get Redis connection (lazy initialization)"""
        if self.redis is None:
            self.redis = Redis.from_url(settings.redis_url, decode_responses=True)
        return self.redis

    def scan_for_secrets(self, text: str) -> List[Dict]:
        """
        Scan text for potential secrets.

        Args:
            text: Text to scan (code, commit message, etc.)

        Returns:
            List of detected secrets with type and location
        """
        detected_secrets = []

        for secret_type, patterns in self.SECRET_PATTERNS.items():
            for pattern in patterns:
                matches = re.finditer(pattern, text, re.IGNORECASE | re.MULTILINE)
                for match in matches:
                    # Don't include the actual secret value in results
                    detected_secrets.append({
                        "type": secret_type,
                        "pattern": pattern[:50],  # Truncated pattern
                        "line": text[:match.start()].count('\n') + 1,
                        "position": match.start(),
                        "length": len(match.group(0))
                    })

        return detected_secrets

    async def log_secret_access(
        self,
        secret_name: str,
        accessed_by: str,
        purpose: Optional[str] = None
    ):
        """
        Log access to a secret for audit purposes.

        Args:
            secret_name: Name of the secret
            accessed_by: Who/what accessed the secret
            purpose: Optional purpose of access
        """
        redis = await self._get_redis()

        access_log = {
            "secret_name": secret_name,
            "accessed_by": accessed_by,
            "purpose": purpose,
            "timestamp": datetime.utcnow().isoformat(),
            "access_hash": self._hash_access(secret_name, accessed_by)
        }

        try:
            # Store in time series
            log_key = f"secrets:access:{secret_name}"
            await redis.lpush(log_key, json.dumps(access_log))
            await redis.ltrim(log_key, 0, 999)  # Keep last 1000 accesses
            await redis.expire(log_key, 86400 * 365)  # Keep 1 year

            logger.info(f"🔐 Secret accessed: {secret_name} by {accessed_by}")

        except Exception as e:
            logger.error(f"Failed to log secret access: {e}")

    def _hash_access(self, secret_name: str, accessed_by: str) -> str:
        """Create hash of access for integrity"""
        content = f"{secret_name}:{accessed_by}:{datetime.utcnow().isoformat()}"
        return hashlib.sha256(content.encode()).hexdigest()[:16]

    async def track_secret_rotation(
        self,
        secret_name: str,
        secret_type: str,
        last_rotated: Optional[datetime] = None
    ):
        """
        Track when a secret was last rotated.

        Args:
            secret_name: Name of the secret
            secret_type: Type of secret (api_key, password, etc.)
            last_rotated: When it was last rotated (defaults to now)
        """
        redis = await self._get_redis()

        if last_rotated is None:
            last_rotated = datetime.utcnow()

        rotation_data = {
            "secret_name": secret_name,
            "secret_type": secret_type,
            "last_rotated": last_rotated.isoformat(),
            "rotation_period_days": self.ROTATION_PERIODS.get(secret_type, 90),
            "next_rotation": (
                last_rotated + timedelta(days=self.ROTATION_PERIODS.get(secret_type, 90))
            ).isoformat()
        }

        try:
            key = f"secrets:rotation:{secret_name}"
            await redis.set(key, json.dumps(rotation_data))
            await redis.expire(key, 86400 * 400)  # Keep for 400 days

            logger.info(
                f"🔄 Secret rotation tracked: {secret_name} "
                f"(next rotation: {rotation_data['next_rotation']})"
            )

        except Exception as e:
            logger.error(f"Failed to track secret rotation: {e}")

    async def check_rotation_needed(self) -> List[Dict]:
        """
        Check which secrets need rotation.

        Returns:
            List of secrets that need rotation
        """
        redis = await self._get_redis()

        try:
            # Get all rotation tracking keys
            keys = await redis.keys("secrets:rotation:*")
            needs_rotation = []

            for key in keys:
                data_json = await redis.get(key)
                if data_json:
                    data = json.loads(data_json)
                    next_rotation = datetime.fromisoformat(data["next_rotation"])

                    # Check if rotation is due
                    if datetime.utcnow() > next_rotation:
                        days_overdue = (datetime.utcnow() - next_rotation).days
                        needs_rotation.append({
                            **data,
                            "days_overdue": days_overdue,
                            "urgency": "critical" if days_overdue > 30 else "high"
                        })

            return sorted(needs_rotation, key=lambda x: x["days_overdue"], reverse=True)

        except Exception as e:
            logger.error(f"Failed to check rotation status: {e}")
            return []

    async def get_secret_audit_log(
        self,
        secret_name: str,
        limit: int = 100
    ) -> List[Dict]:
        """
        Get audit log for a secret.

        Args:
            secret_name: Name of the secret
            limit: Maximum number of entries to return

        Returns:
            List of access log entries
        """
        redis = await self._get_redis()

        try:
            log_key = f"secrets:access:{secret_name}"
            entries = await redis.lrange(log_key, 0, limit - 1)

            return [json.loads(entry) for entry in entries]

        except Exception as e:
            logger.error(f"Failed to get audit log: {e}")
            return []

    def validate_secret_strength(
        self,
        secret: str,
        secret_type: str
    ) -> Dict[str, any]:
        """
        Validate the strength of a secret.

        Args:
            secret: The secret value
            secret_type: Type of secret

        Returns:
            Validation result with strength score and recommendations
        """
        result = {
            "is_strong": False,
            "score": 0,
            "issues": [],
            "recommendations": []
        }

        # Check length
        min_length = 20 if secret_type in ["api_key", "token"] else 12
        if len(secret) < min_length:
            result["issues"].append(f"Too short (minimum {min_length} characters)")
        else:
            result["score"] += 25

        # Check character diversity
        has_upper = bool(re.search(r'[A-Z]', secret))
        has_lower = bool(re.search(r'[a-z]', secret))
        has_digit = bool(re.search(r'\d', secret))
        has_special = bool(re.search(r'[^A-Za-z0-9]', secret))

        diversity_score = sum([has_upper, has_lower, has_digit, has_special])
        result["score"] += diversity_score * 15

        if diversity_score < 3:
            result["recommendations"].append("Use a mix of uppercase, lowercase, numbers, and special characters")

        # Check for common patterns
        common_patterns = [
            r"123456",
            r"password",
            r"admin",
            r"qwerty",
            r"abc123",
        ]

        for pattern in common_patterns:
            if re.search(pattern, secret, re.IGNORECASE):
                result["issues"].append("Contains common pattern")
                result["score"] = max(0, result["score"] - 30)
                break

        # Check entropy (randomness)
        unique_chars = len(set(secret))
        if unique_chars < len(secret) * 0.5:
            result["recommendations"].append("Increase randomness (too many repeated characters)")
        else:
            result["score"] += 20

        # Final score
        result["score"] = min(100, result["score"])
        result["is_strong"] = result["score"] >= 70

        return result

    async def generate_rotation_reminder_report(self) -> str:
        """
        Generate report of secrets that need rotation.

        Returns:
            Formatted report string
        """
        needs_rotation = await self.check_rotation_needed()

        if not needs_rotation:
            return "✅ All secrets are up to date. No rotation needed."

        report = "🔑 **SECRET ROTATION REMINDER**\n\n"
        report += f"**Secrets needing rotation:** {len(needs_rotation)}\n\n"

        for secret in needs_rotation:
            emoji = "🔴" if secret["urgency"] == "critical" else "🟡"
            report += f"{emoji} **{secret['secret_name']}**\n"
            report += f"   Type: {secret['secret_type']}\n"
            report += f"   Last rotated: {secret['last_rotated']}\n"
            report += f"   Overdue by: {secret['days_overdue']} days\n\n"

        return report


# Global instance
secrets_manager = SecretsManager()
