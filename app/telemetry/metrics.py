from prometheus_client import Counter, Gauge, Histogram, Info, Summary

# ==================== Request Metrics ====================

HTTP_REQUESTS_TOTAL = Counter(
    "http_requests_total",
    "Total HTTP requests by method, endpoint, and status code.",
    ["method", "endpoint", "status_code"],
)

HTTP_REQUEST_DURATION_SECONDS = Histogram(
    "http_request_duration_seconds",
    "HTTP request latency in seconds.",
    ["method", "endpoint", "status_code"],
    buckets=(
        0.005,
        0.01,
        0.025,
        0.05,
        0.075,
        0.1,
        0.25,
        0.5,
        0.75,
        1.0,
        2.5,
        5.0,
        7.5,
        10.0,
    ),
)

HTTP_REQUEST_SIZE_BYTES = Summary(
    "http_request_size_bytes",
    "HTTP request size in bytes.",
    ["method", "endpoint"],
)

HTTP_RESPONSE_SIZE_BYTES = Summary(
    "http_response_size_bytes",
    "HTTP response size in bytes.",
    ["method", "endpoint"],
)

# ==================== Pattern Analysis Metrics ====================

ANALYZE_REQUEST_DURATION_SECONDS = Histogram(
    "analyze_request_duration_seconds",
    "Duration of /api/analyze requests.",
    ["interval"],
)

SCAN_REQUEST_DURATION_SECONDS = Histogram(
    "scan_request_duration_seconds",
    "Duration of /api/scan requests.",
    ["status", "universe_size"],
)

DETECTOR_RUNTIME_SECONDS = Summary(
    "detector_runtime_seconds",
    "Runtime of pattern detectors.",
    ["pattern"],
)

ANALYZE_ERRORS_TOTAL = Counter(
    "analyze_errors_total",
    "Total errors encountered while serving /api/analyze.",
)

SCAN_ERRORS_TOTAL = Counter(
    "scan_errors_total",
    "Total errors encountered while serving /api/scan.",
)

# ==================== External Service Metrics ====================

CHARTIMG_POST_STATUS_TOTAL = Counter(
    "chartimg_post_status_total",
    "Chart-IMG render attempts by result.",
    ["status"],
)

API_QUOTA_USED = Gauge(
    "api_quota_used",
    "Current API quota usage for external services.",
    ["service"],
)

API_QUOTA_LIMIT = Gauge(
    "api_quota_limit",
    "API quota limit for external services.",
    ["service"],
)

API_QUOTA_REMAINING = Gauge(
    "api_quota_remaining",
    "Remaining API quota for external services.",
    ["service"],
)

EXTERNAL_API_ERRORS_TOTAL = Counter(
    "external_api_errors_total",
    "Total errors from external API calls.",
    ["service", "error_type"],
)

EXTERNAL_API_DURATION_SECONDS = Histogram(
    "external_api_duration_seconds",
    "External API call duration in seconds.",
    ["service", "endpoint"],
    buckets=(0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0, 30.0),
)

# ==================== Cache Metrics ====================

CACHE_HITS_TOTAL = Counter(
    "cache_hits_total",
    "Number of cache hits observed for each service.",
    ["name"],
)

CACHE_MISSES_TOTAL = Counter(
    "cache_misses_total",
    "Number of cache misses observed for each service.",
    ["name"],
)

CACHE_SIZE_BYTES = Gauge(
    "cache_size_bytes",
    "Current size of cache in bytes.",
    ["name"],
)

CACHE_EVICTIONS_TOTAL = Counter(
    "cache_evictions_total",
    "Total number of cache evictions.",
    ["name"],
)

# ==================== Database Metrics ====================

DB_CONNECTIONS_TOTAL = Gauge(
    "db_connections_total",
    "Total number of database connections.",
    ["state"],  # active, idle, total
)

DB_CONNECTIONS_POOL_SIZE = Gauge(
    "db_connections_pool_size",
    "Configured database connection pool size.",
)

DB_CONNECTIONS_POOL_OVERFLOW = Gauge(
    "db_connections_pool_overflow",
    "Number of connections in overflow pool.",
)

DB_QUERY_DURATION_SECONDS = Histogram(
    "db_query_duration_seconds",
    "Database query duration in seconds.",
    ["operation"],
    buckets=(0.001, 0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5),
)

DB_QUERY_ERRORS_TOTAL = Counter(
    "db_query_errors_total",
    "Total database query errors.",
    ["operation", "error_type"],
)

# ==================== Health Check Metrics ====================

HEALTH_CHECK_STATUS = Gauge(
    "health_check_status",
    "Health check status (1 = healthy, 0 = unhealthy).",
    ["component"],
)

HEALTH_CHECK_DURATION_SECONDS = Histogram(
    "health_check_duration_seconds",
    "Health check duration in seconds.",
    ["component"],
)

# ==================== Application Info ====================

APP_INFO = Info(
    "app_info",
    "Application version and build information.",
)

UPTIME_SECONDS = Gauge(
    "uptime_seconds",
    "Application uptime in seconds.",
)

# ==================== Error Rate Metrics ====================

ERROR_RATE_TOTAL = Counter(
    "error_rate_total",
    "Total application errors by type and severity.",
    ["error_type", "severity", "endpoint"],
)

# ==================== Alert Metrics ====================

ALERTS_SENT_TOTAL = Counter(
    "alerts_sent_total",
    "Total alerts sent by type and channel.",
    ["alert_type", "channel", "status"],
)

__all__ = [
    # Request metrics
    "HTTP_REQUESTS_TOTAL",
    "HTTP_REQUEST_DURATION_SECONDS",
    "HTTP_REQUEST_SIZE_BYTES",
    "HTTP_RESPONSE_SIZE_BYTES",
    # Pattern analysis
    "ANALYZE_REQUEST_DURATION_SECONDS",
    "SCAN_REQUEST_DURATION_SECONDS",
    "DETECTOR_RUNTIME_SECONDS",
    "ANALYZE_ERRORS_TOTAL",
    "SCAN_ERRORS_TOTAL",
    # External services
    "CHARTIMG_POST_STATUS_TOTAL",
    "API_QUOTA_USED",
    "API_QUOTA_LIMIT",
    "API_QUOTA_REMAINING",
    "EXTERNAL_API_ERRORS_TOTAL",
    "EXTERNAL_API_DURATION_SECONDS",
    # Cache
    "CACHE_HITS_TOTAL",
    "CACHE_MISSES_TOTAL",
    "CACHE_SIZE_BYTES",
    "CACHE_EVICTIONS_TOTAL",
    # Database
    "DB_CONNECTIONS_TOTAL",
    "DB_CONNECTIONS_POOL_SIZE",
    "DB_CONNECTIONS_POOL_OVERFLOW",
    "DB_QUERY_DURATION_SECONDS",
    "DB_QUERY_ERRORS_TOTAL",
    # Health checks
    "HEALTH_CHECK_STATUS",
    "HEALTH_CHECK_DURATION_SECONDS",
    # App info
    "APP_INFO",
    "UPTIME_SECONDS",
    # Errors
    "ERROR_RATE_TOTAL",
    # Alerts
    "ALERTS_SENT_TOTAL",
]
