import os
import subprocess
from datetime import datetime, timezone
from functools import lru_cache
from typing import Dict


@lru_cache(maxsize=1)
def resolve_build_sha() -> str:
    """Best-effort short git SHA for logging/metrics."""
    for key in ("BUILD_SHA", "GIT_COMMIT", "RAILWAY_GIT_COMMIT_SHA"):
        value = os.getenv(key, "").strip()
        if value:
            return value[:7]
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"],
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
    except Exception:
        return "unknown"


@lru_cache(maxsize=1)
def resolve_branch() -> str:
    """Best-effort current branch name."""
    for key in ("GIT_BRANCH", "RAILWAY_GIT_BRANCH"):
        value = os.getenv(key)
        if value:
            return value
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
    except Exception:
        return "unknown"


def resolve_build_payload() -> Dict[str, str]:
    """Shared payload for version + telemetry surfaces."""
    sha = resolve_build_sha()
    branch = resolve_branch()
    ts = os.getenv("BUILD_TIME")
    if not ts:
        ts = datetime.now(timezone.utc).isoformat()
    return {
        "build_sha": sha,
        "branch": branch,
        "version": os.getenv("APP_VERSION", "1.0.0"),
        "commit": sha,
        "build_time": ts,
    }
