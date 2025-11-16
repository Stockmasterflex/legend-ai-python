from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
from typing import Optional


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False, extra="ignore")
    # App
    app_name: str = "Legend AI"
    debug: bool = False
    secret_key: str = "dev-secret-key-change-in-production"

    # Telegram
    telegram_bot_token: str = "dev-token"
    telegram_chat_id: Optional[str] = None
    telegram_webhook_url: Optional[str] = None

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

    # AI Services
    openrouter_api_key: str = "dev-key"
    openai_api_key: Optional[str] = None

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
