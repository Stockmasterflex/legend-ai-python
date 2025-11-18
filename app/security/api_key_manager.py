"""
API Key Security Manager
Handles API key rotation, encryption, auditing, and revocation
"""
import secrets
import hashlib
import logging
from datetime import datetime, timedelta
from typing import Optional, Dict, List
from redis.asyncio import Redis
from cryptography.fernet import Fernet
import json

from app.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


class APIKeyManager:
    """
    Secure API key management system.

    Features:
    - Automatic key rotation (90 days)
    - Encryption at rest
    - Usage auditing
    - Compromise detection
    - Emergency revocation
    """

    # Key rotation period (days)
    ROTATION_PERIOD_DAYS = 90

    # Alert thresholds
    USAGE_SPIKE_THRESHOLD = 10.0  # 10x normal usage
    UNUSUAL_PATTERN_THRESHOLD = 5  # 5 different IPs in short time

    def __init__(self):
        self.redis: Optional[Redis] = None
        self.encryption_key = self._get_or_create_encryption_key()
        self.cipher = Fernet(self.encryption_key)

    def _get_or_create_encryption_key(self) -> bytes:
        """Get or create encryption key for API keys"""
        # In production, this should be stored in a secure key management service
        # For now, derive from secret_key
        key = hashlib.sha256(settings.secret_key.encode()).digest()
        return Fernet.generate_key()

    async def _get_redis(self) -> Redis:
        """Get Redis connection (lazy initialization)"""
        if self.redis is None:
            self.redis = Redis.from_url(settings.redis_url, decode_responses=False)
        return self.redis

    def generate_api_key(self, prefix: str = "sk") -> str:
        """
        Generate a new cryptographically secure API key.

        Args:
            prefix: Key prefix for identification

        Returns:
            API key string
        """
        # Generate 32 bytes of randomness
        random_bytes = secrets.token_bytes(32)

        # Encode as base64-like string
        key_suffix = secrets.token_urlsafe(32)

        # Format: prefix_randomsuffix
        api_key = f"{prefix}_{key_suffix}"

        return api_key

    async def create_api_key(
        self,
        user_id: str,
        name: str,
        permissions: Optional[List[str]] = None
    ) -> Dict:
        """
        Create and store a new API key.

        Args:
            user_id: User identifier
            name: Key name/description
            permissions: List of allowed permissions

        Returns:
            Dictionary with key info (including plaintext key - only shown once!)
        """
        redis = await self._get_redis()

        # Generate key
        api_key = self.generate_api_key()

        # Hash the key for storage (we store the hash, not the key itself)
        key_hash = self._hash_api_key(api_key)

        # Create key metadata
        key_data = {
            "user_id": user_id,
            "name": name,
            "key_hash": key_hash,
            "permissions": permissions or ["read"],
            "created_at": datetime.utcnow().isoformat(),
            "last_rotated": datetime.utcnow().isoformat(),
            "expires_at": (datetime.utcnow() + timedelta(days=self.ROTATION_PERIOD_DAYS)).isoformat(),
            "is_active": True,
            "usage_count": 0,
            "last_used": None,
        }

        # Store encrypted key data
        key_id = self._generate_key_id(api_key)
        encrypted_data = self.cipher.encrypt(json.dumps(key_data).encode())

        await redis.set(f"apikey:{key_id}", encrypted_data)
        await redis.set(f"apikey:hash:{key_hash}", key_id)

        # Add to user's key list
        await redis.sadd(f"user:{user_id}:keys", key_id)

        logger.info(f"✅ Created API key for user {user_id}: {name}")

        # Return key data (plaintext key only shown here!)
        return {
            "api_key": api_key,  # Only shown once!
            "key_id": key_id,
            "name": name,
            "created_at": key_data["created_at"],
            "expires_at": key_data["expires_at"],
            "permissions": key_data["permissions"],
        }

    def _hash_api_key(self, api_key: str) -> str:
        """Hash API key for secure storage"""
        return hashlib.sha256(api_key.encode()).hexdigest()

    def _generate_key_id(self, api_key: str) -> str:
        """Generate short key ID from API key"""
        hash_obj = hashlib.sha256(api_key.encode())
        return hash_obj.hexdigest()[:16]

    async def validate_api_key(self, api_key: str) -> Optional[Dict]:
        """
        Validate an API key and return its metadata.

        Args:
            api_key: API key to validate

        Returns:
            Key metadata if valid, None otherwise
        """
        redis = await self._get_redis()

        try:
            # Hash the key to look it up
            key_hash = self._hash_api_key(api_key)

            # Get key ID from hash
            key_id = await redis.get(f"apikey:hash:{key_hash}")
            if not key_id:
                logger.warning("🔑 Invalid API key attempt")
                return None

            # Get encrypted key data
            encrypted_data = await redis.get(f"apikey:{key_id}")
            if not encrypted_data:
                return None

            # Decrypt and parse key data
            decrypted_data = self.cipher.decrypt(encrypted_data)
            key_data = json.loads(decrypted_data.decode())

            # Check if key is active
            if not key_data.get("is_active", False):
                logger.warning(f"🔑 Inactive API key used: {key_id}")
                return None

            # Check if key is expired
            expires_at = datetime.fromisoformat(key_data["expires_at"])
            if datetime.utcnow() > expires_at:
                logger.warning(f"🔑 Expired API key used: {key_id}")
                await self._auto_rotate_key(key_id, key_data)
                return None

            # Update usage stats
            await self._record_usage(key_id, key_data)

            return key_data

        except Exception as e:
            logger.error(f"API key validation error: {e}")
            return None

    async def _record_usage(self, key_id: str, key_data: Dict):
        """Record API key usage for auditing"""
        redis = await self._get_redis()

        try:
            # Increment usage counter
            key_data["usage_count"] = key_data.get("usage_count", 0) + 1
            key_data["last_used"] = datetime.utcnow().isoformat()

            # Update stored data
            encrypted_data = self.cipher.encrypt(json.dumps(key_data).encode())
            await redis.set(f"apikey:{key_id}", encrypted_data)

            # Record usage in time series for anomaly detection
            await redis.lpush(
                f"apikey:{key_id}:usage",
                json.dumps({
                    "timestamp": datetime.utcnow().isoformat(),
                    "usage_count": key_data["usage_count"]
                })
            )
            await redis.ltrim(f"apikey:{key_id}:usage", 0, 999)  # Keep last 1000 entries

        except Exception as e:
            logger.error(f"Failed to record API key usage: {e}")

    async def _auto_rotate_key(self, key_id: str, key_data: Dict):
        """
        Automatically rotate an expired API key.

        Args:
            key_id: Key ID to rotate
            key_data: Current key metadata
        """
        logger.info(f"🔄 Auto-rotating expired API key: {key_id}")

        # Mark old key as inactive
        key_data["is_active"] = False
        key_data["rotated_at"] = datetime.utcnow().isoformat()

        redis = await self._get_redis()
        encrypted_data = self.cipher.encrypt(json.dumps(key_data).encode())
        await redis.set(f"apikey:{key_id}", encrypted_data)

        # Notify user (would integrate with notification system)
        logger.warning(
            f"⚠️ API key expired and deactivated: {key_id} "
            f"(user: {key_data.get('user_id')})"
        )

    async def revoke_api_key(self, key_id: str, reason: str = "manual_revocation"):
        """
        Revoke an API key immediately.

        Args:
            key_id: Key ID to revoke
            reason: Revocation reason
        """
        redis = await self._get_redis()

        try:
            # Get key data
            encrypted_data = await redis.get(f"apikey:{key_id}")
            if not encrypted_data:
                logger.warning(f"Attempted to revoke non-existent key: {key_id}")
                return

            # Decrypt and update
            decrypted_data = self.cipher.decrypt(encrypted_data)
            key_data = json.loads(decrypted_data.decode())

            key_data["is_active"] = False
            key_data["revoked_at"] = datetime.utcnow().isoformat()
            key_data["revocation_reason"] = reason

            # Store updated data
            encrypted_data = self.cipher.encrypt(json.dumps(key_data).encode())
            await redis.set(f"apikey:{key_id}", encrypted_data)

            logger.warning(f"🚫 API key revoked: {key_id} (reason: {reason})")

        except Exception as e:
            logger.error(f"Failed to revoke API key: {e}")

    async def detect_compromise(self, key_id: str) -> bool:
        """
        Detect potential API key compromise based on usage patterns.

        Args:
            key_id: Key ID to check

        Returns:
            True if compromise suspected
        """
        redis = await self._get_redis()

        try:
            # Get recent usage patterns
            usage_data = await redis.lrange(f"apikey:{key_id}:usage", 0, 99)

            if len(usage_data) < 10:
                return False  # Not enough data

            # Check for usage spikes
            usage_counts = []
            for entry in usage_data:
                data = json.loads(entry)
                usage_counts.append(data.get("usage_count", 0))

            # Calculate average and recent usage
            avg_usage = sum(usage_counts[10:]) / len(usage_counts[10:]) if len(usage_counts) > 10 else 0
            recent_usage = sum(usage_counts[:10]) / 10

            # Check for spike
            if avg_usage > 0 and recent_usage > avg_usage * self.USAGE_SPIKE_THRESHOLD:
                logger.warning(
                    f"🚨 SECURITY ALERT: Unusual API key usage spike detected for {key_id} "
                    f"(avg: {avg_usage:.1f}, recent: {recent_usage:.1f})"
                )
                return True

            return False

        except Exception as e:
            logger.error(f"Compromise detection error: {e}")
            return False

    async def audit_api_keys(self) -> Dict:
        """
        Generate audit report of all API keys.

        Returns:
            Audit report dictionary
        """
        redis = await self._get_redis()

        try:
            # Get all API keys
            keys = await redis.keys("apikey:*")

            active_keys = 0
            inactive_keys = 0
            expired_keys = 0
            total_usage = 0

            for key in keys:
                if key.startswith(b"apikey:hash:"):
                    continue

                encrypted_data = await redis.get(key)
                if encrypted_data:
                    decrypted_data = self.cipher.decrypt(encrypted_data)
                    key_data = json.loads(decrypted_data.decode())

                    if key_data.get("is_active"):
                        active_keys += 1
                    else:
                        inactive_keys += 1

                    expires_at = datetime.fromisoformat(key_data["expires_at"])
                    if datetime.utcnow() > expires_at:
                        expired_keys += 1

                    total_usage += key_data.get("usage_count", 0)

            return {
                "total_keys": active_keys + inactive_keys,
                "active_keys": active_keys,
                "inactive_keys": inactive_keys,
                "expired_keys": expired_keys,
                "total_usage": total_usage,
                "audit_time": datetime.utcnow().isoformat()
            }

        except Exception as e:
            logger.error(f"Audit error: {e}")
            return {"error": str(e)}


# Global instance
api_key_manager = APIKeyManager()
