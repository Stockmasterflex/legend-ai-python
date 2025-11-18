from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import logging
from pathlib import Path

from app.config import get_settings
from app.lifecycle import lifespan
from app.docs_config import tags_metadata, openapi_custom_info
from app.api.telegram_enhanced import router as telegram_router
from app.api.patterns import router as patterns_router
from app.api.charts import router as charts_router
from app.api.universe import router as universe_router
from app.api.watchlist import router as watchlist_router
from app.api.trade_plan import router as trade_router
from app.api.analytics import router as analytics_router
from app.api.market import router as market_router
from app.api.analyze import router as analyze_router
from app.api.dashboard import router as dashboard_router
from app.api.alerts import router as alerts_router
from app.api.multitimeframe import router as multitf_router
from app.api.risk import router as risk_router
from app.api.trades import router as trades_router
from app.api import analyze as analyze_pkg, watchlist as watchlist_pkg
from app.api.version import router as version_router
from app.api.metrics import router as metrics_router
from app.api.scan import router as scan_router
from app.api.tv import router as tv_router
from app.api.errors import router as errors_router
from app.api.cache_mgmt import router as cache_mgmt_router
from app.api.api_usage import router as api_usage_router
from app.api.docs import router as docs_router
from app.api.crypto import router as crypto_router
from app.routers.ai_chat import router as ai_chat_router
from app.routers.advanced_analysis import router as advanced_analysis_router
from app.middleware.structured_logging import StructuredLoggingMiddleware
from app.middleware.rate_limit import RateLimitMiddleware
from app.utils.build_info import resolve_build_sha

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

settings = get_settings()

# Create FastAPI app with enhanced documentation
app = FastAPI(
    title=openapi_custom_info["title"],
    description=openapi_custom_info["description"],
    version=openapi_custom_info["version"],
    contact=openapi_custom_info["contact"],
    license_info=openapi_custom_info["license_info"],
    openapi_tags=tags_metadata,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,
    swagger_ui_parameters={
        "defaultModelsExpandDepth": -1,  # Hide schemas section by default
        "docExpansion": "list",  # Expand tag lists by default
        "filter": True,  # Enable search filter
        "showCommonExtensions": True,
        "syntaxHighlight.theme": "monokai",  # Beautiful syntax highlighting
        "tryItOutEnabled": True,  # Enable "Try it out" by default
    }
)

# Metrics middleware sits at the top to capture all HTTP metrics
from app.middleware.metrics_middleware import MetricsMiddleware
app.add_middleware(MetricsMiddleware)
logger.info("📊 Metrics middleware enabled")

# Structured logging sits at the top of the stack to capture everything
app.add_middleware(StructuredLoggingMiddleware)

# Add rate limiting middleware to protect against abuse
# 60 requests per minute per IP for public endpoints
app.add_middleware(RateLimitMiddleware, requests_per_minute=60)
logger.info("🛡️ Rate limiting enabled: 60 requests/minute per IP")

# Add CORS middleware with environment-aware origin restrictions
# In production (Railway): only allows requests from the app's own domain
# In development: allows all origins for easier testing
allowed_origins = settings.allowed_origins
logger.info(f"🔒 CORS configured with allowed origins: {allowed_origins}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(telegram_router, prefix="/api", tags=["telegram"])
app.include_router(patterns_router)
app.include_router(charts_router)
app.include_router(universe_router)
app.include_router(watchlist_router)
app.include_router(trade_router)
app.include_router(analytics_router)
app.include_router(market_router)
app.include_router(alerts_router)
app.include_router(multitf_router)
app.include_router(risk_router)
app.include_router(trades_router)
app.include_router(dashboard_router, tags=["dashboard"])
app.include_router(analyze_router)
app.include_router(version_router)
app.include_router(metrics_router)
app.include_router(scan_router)
app.include_router(tv_router)
app.include_router(errors_router)
app.include_router(cache_mgmt_router)
app.include_router(api_usage_router)
app.include_router(docs_router)
app.include_router(crypto_router)
app.include_router(ai_chat_router)
app.include_router(advanced_analysis_router)

# Mount static files if they exist
static_path = Path(__file__).parent.parent / "static"
if static_path.exists():
    app.mount("/static", StaticFiles(directory=str(static_path)), name="static")
    logger.info(f"📁 Static files mounted from {static_path}")

@app.get("/")
async def root(request: Request):
    """
    🏠 **API Root Endpoint**

    Welcome to Legend AI Trading Pattern Scanner API!

    Navigate to `/docs` for interactive API documentation.
    """
    request.state.telemetry = {"event": "root", "status": 200}
    return {
        "status": "running",
        "service": "Legend AI - Trading Pattern Scanner",
        "version": "1.0.0",
        "message": "Welcome to Legend AI API! Visit /docs for interactive documentation.",
        "documentation": {
            "swagger_ui": "/docs",
            "redoc": "/redoc",
            "openapi_schema": "/openapi.json",
            "error_codes": "/api/docs/errors",
            "getting_started": "/api/docs/getting-started"
        },
        "endpoints": {
            "dashboard": "/dashboard",
            "health": "/health",
            "pattern_detection": "/api/patterns/detect",
            "ai_chat": "/api/ai/chat",
            "ai_analysis": "/api/ai/analyze"
        },
        "features": [
            "🎯 AI-Powered Pattern Detection",
            "🤖 Trading Assistant Chatbot",
            "📊 Professional Chart Generation",
            "🔍 Market Scanner",
            "📈 Real-time Market Data",
            "⚡ Smart Caching (Redis)"
        ]
    }

@app.get("/healthz")
async def healthz():
    """
    Simple health check for Railway/K8s
    Always returns 200 OK if app is running
    """
    return {"status": "ok"}


@app.get("/health")
async def health(request: Request):
    """
    Fast health check for Railway deployment.
    Always returns 200 OK immediately without blocking connectivity tests.
    Use /health/detailed for full diagnostics.
    """
    issues = []
    warnings = []
    overall_status = "healthy"

    # Telegram configuration (non-blocking check)
    try:
        telegram_status = (
            "configured"
            if settings.telegram_bot_token and settings.telegram_bot_token != "dev-token"
            else "not_configured"
        )
        if telegram_status == "not_configured":
            warnings.append("Telegram bot not configured")
    except Exception as e:
        telegram_status = "unknown"
        issues.append(f"Telegram check failed: {str(e)}")

    # Redis status (config check only - no actual connection test for speed)
    try:
        redis_status = "configured" if settings.redis_url else "not_configured"
        if redis_status == "not_configured":
            warnings.append("Redis not configured - caching disabled")
            if overall_status == "healthy":
                overall_status = "degraded"
    except Exception as e:
        redis_status = "unknown"
        warnings.append(f"Redis check failed: {str(e)}")

    try:
        universe_status = {
            "seeded": bool(universe_store._memory),
            "cached_symbols": len(universe_store._memory),
        }
    except Exception:
        universe_status = {"seeded": False, "cached_symbols": 0}

    # API Keys presence (not the actual keys, just boolean)
    try:
        key_presence = {
            "chartimg": bool(settings.chart_img_api_key),
            "twelvedata": bool(settings.twelvedata_api_key),
            "finnhub": bool(settings.finnhub_api_key),
            "alpha_vantage": bool(settings.alpha_vantage_api_key),
        }
        # Warn if Chart-IMG is not configured (critical for charts)
        if not key_presence["chartimg"]:
            warnings.append("Chart-IMG API key not configured - charts will not load")
            if overall_status == "healthy":
                overall_status = "degraded"
    except Exception as e:
        key_presence = {}
        issues.append(f"API keys check failed: {str(e)}")

    try:
        version = resolve_build_sha()
    except Exception:
        version = "unknown"

    try:
        webhook_url = settings.telegram_webhook_url
    except Exception:
        webhook_url = None

    payload = {
        "status": overall_status,
        "telegram": telegram_status,
        "redis": redis_status,
        "version": version,
        "webhook_url": webhook_url,
        "universe": universe_status,
        "keys": key_presence,
        "analyze": {"cache_ttl": 3600},
        "issues": issues,
        "warnings": warnings,
    }

    try:
        request.state.telemetry = {
            "event": "health",
            "status": payload["status"],
            "symbol": None,
            "interval": None,
        }
    except Exception:
        pass  # Telemetry is not critical for health check

    return payload

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
