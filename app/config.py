from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
from typing import Optional


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False, extra="ignore")
    # App
    app_name: str = "Legend AI"
    debug: bool = False
    secret_key: str = "dev-secret-key-change-in-production"

    # CORS Origins (comma-separated list)
    cors_origins: str = "*"  # Default to allow all for development

    # Telegram
    telegram_bot_token: str = "dev-token"
    telegram_chat_id: Optional[str] = None
    telegram_webhook_url: Optional[str] = None

    # Discord
    discord_bot_token: Optional[str] = None
    discord_guild_id: Optional[str] = None
    discord_channel_market_updates: Optional[str] = None
    discord_channel_signals: Optional[str] = None
    discord_channel_daily_picks: Optional[str] = None

    @property
    def auto_webhook_url(self) -> str:
        """Auto-generate webhook URL from Railway domain"""
        import os
        # Try to get from Railway environment
        railway_domain = os.getenv("RAILWAY_PUBLIC_DOMAIN")
        if railway_domain:
            return f"https://{railway_domain}"
        # Fallback to explicitly set URL
        if self.telegram_webhook_url:
            return self.telegram_webhook_url
        # Default for local development
        return "http://localhost:8000"

    @property
    def allowed_origins(self) -> list[str]:
        """Get list of allowed CORS origins, auto-detecting Railway domain"""
        import os

        # In production (Railway), restrict to the app's own domain
        railway_domain = os.getenv("RAILWAY_PUBLIC_DOMAIN")
        if railway_domain:
            return [
                f"https://{railway_domain}",
                f"http://{railway_domain}",
            ]

        # If CORS_ORIGINS is explicitly set, use that
        if self.cors_origins != "*":
            return [origin.strip() for origin in self.cors_origins.split(",")]

        # In development, allow all origins
        return ["*"]

    # AI Services
    openrouter_api_key: Optional[str] = None
    openai_api_key: Optional[str] = None
    ai_model: str = "anthropic/claude-3.5-sonnet"  # Default to Claude (best value)
    ai_temperature: float = 0.7

    # Chart-IMG
    chartimg_api_key: Optional[str] = None

    @property
    def chart_img_api_key(self) -> Optional[str]:
        """Get Chart-IMG API key from multiple possible environment variable names"""
        import os
        return (
            os.getenv("CHART_IMG_API_KEY")
            or os.getenv("CHARTIMG_API_KEY")
            or os.getenv("CHART_IMG_APIKEY")
            or os.getenv("CHARTIMG_APIKEY")
            or self.chartimg_api_key
        )

    # Market Data APIs
    twelvedata_api_key: Optional[str] = None
    finnhub_api_key: Optional[str] = None
    alpha_vantage_api_key: Optional[str] = None

    # API Rate Limits (daily)
    twelvedata_daily_limit: int = 800
    finnhub_daily_limit: int = 60
    alpha_vantage_daily_limit: int = 500
    chartimg_daily_limit: int = 500

    # Redis
    redis_url: str = "redis://localhost:6379"

    # Database (optional for Phase 1)
    database_url: Optional[str] = None

    # Google Sheets
    google_sheets_id: Optional[str] = None

    # N8N Integration
    n8n_api_key: Optional[str] = None
    n8n_api_url: Optional[str] = None
    n8n_chart_webhook: Optional[str] = None

    # Feature Flags
    legend_flags_enable_scanner: int = 1

    # Cost Optimization Settings
    cache_ttl_patterns: int = 3600  # 1 hour
    cache_ttl_market_data: int = 900  # 15 minutes
    cache_ttl_charts: int = 7200  # 2 hours
    cache_ttl_ai_responses: int = 1800  # 30 minutes

    rate_limit_per_minute: int = 60
    ai_rate_limit_per_minute: int = 20
    market_data_rate_limit: int = 30

    data_source_priority: str = "twelvedata,finnhub,alphavantage"

    # Multi-Tier Cache Settings
    cache_hot_ttl_min: int = 300  # 5 minutes (Redis hot tier)
    cache_hot_ttl_max: int = 900  # 15 minutes (Redis hot tier)
    cache_warm_ttl: int = 3600  # 1 hour (Database warm tier)
    cache_cdn_ttl: int = 86400  # 24 hours (CDN/static files)
    cache_promotion_threshold: int = 3  # Access count to promote from warm to hot
    cache_hot_max_size: int = 10000  # Max keys in hot tier before eviction
    cache_enable_warming: bool = True  # Enable cache warming on startup
    cache_cdn_path: str = "/tmp/legend-ai-cdn"  # Path for CDN static cache

    # Email & Alerts (optional for Phase 4)
    sendgrid_api_key: Optional[str] = None
    alert_email: Optional[str] = None

    # Security
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60



@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    import os
    import logging

    logger = logging.getLogger(__name__)

    # Debug environment variables
    chartimg_key = os.getenv('CHARTIMG_API_KEY')
    logger.info(f"🔍 Environment CHARTIMG_API_KEY present: {bool(chartimg_key)}")
    if chartimg_key:
        logger.info(f"🔍 CHARTIMG_API_KEY length: {len(chartimg_key)}")

    settings = Settings()
    logger.info(f"🔍 Settings chart_img_api_key present: {bool(settings.chart_img_api_key)}")
    logger.info(f"🔍 Settings chartimg_api_key present: {bool(settings.chartimg_api_key)}")

    return settings
