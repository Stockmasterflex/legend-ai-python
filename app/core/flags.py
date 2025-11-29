"""
Feature flag utilities for Legend AI.

Flags are sourced from the LEGEND_FLAGS environment variable, which accepts either
JSON (e.g., {"enable_scanner": true}) or a comma-separated list (e.g., enable_scanner=1).
Individual overrides like LEGEND_FLAGS_ENABLE_SCANNER are also supported.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from functools import lru_cache
from typing import Any, Dict


@dataclass(frozen=True)
class LegendFlags:
    enable_scanner: bool = False


def _to_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if value is None:
        return False
    if isinstance(value, (int, float)):
        return value != 0
    if isinstance(value, str):
        return value.strip().lower() in {"1", "true", "yes", "on"}
    return False


def _load_env_flags() -> Dict[str, Any]:
    flags: Dict[str, Any] = {}
    raw = os.getenv("LEGEND_FLAGS")
    if raw:
        raw = raw.strip()
        if raw.startswith("{"):
            try:
                parsed = json.loads(raw)
                if isinstance(parsed, dict):
                    flags.update(parsed)
            except json.JSONDecodeError:
                pass
        else:
            for token in raw.split(","):
                if not token:
                    continue
                key, _, val = token.partition("=")
                key = key.strip()
                if not key:
                    continue
                flags[key] = val.strip() if val else True
    env_override = os.getenv("LEGEND_FLAGS_ENABLE_SCANNER")
    if env_override is not None:
        flags["enable_scanner"] = env_override
    return flags


@lru_cache()
def _cached_flags() -> LegendFlags:
    data = _load_env_flags()
    return LegendFlags(enable_scanner=_to_bool(data.get("enable_scanner")))


def get_legend_flags() -> LegendFlags:
    """Return cached feature flags."""
    return _cached_flags()


def reload_legend_flags() -> LegendFlags:
    """Force-refresh feature flags (useful in tests)."""
    _cached_flags.cache_clear()
    return _cached_flags()


LEGEND_FLAGS = get_legend_flags()

__all__ = ["LegendFlags", "LEGEND_FLAGS", "get_legend_flags", "reload_legend_flags"]
