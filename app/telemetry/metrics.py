from prometheus_client import Counter, Histogram, Summary

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

CHARTIMG_POST_STATUS_TOTAL = Counter(
    "chartimg_post_status_total",
    "Chart-IMG render attempts by result.",
    ["status"],
)

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

ANALYZE_ERRORS_TOTAL = Counter(
    "analyze_errors_total",
    "Total errors encountered while serving /api/analyze.",
)

SCAN_ERRORS_TOTAL = Counter(
    "scan_errors_total",
    "Total errors encountered while serving /api/scan.",
)

__all__ = [
    "ANALYZE_REQUEST_DURATION_SECONDS",
    "SCAN_REQUEST_DURATION_SECONDS",
    "DETECTOR_RUNTIME_SECONDS",
    "CHARTIMG_POST_STATUS_TOTAL",
    "CACHE_HITS_TOTAL",
    "CACHE_MISSES_TOTAL",
    "ANALYZE_ERRORS_TOTAL",
    "SCAN_ERRORS_TOTAL",
]
