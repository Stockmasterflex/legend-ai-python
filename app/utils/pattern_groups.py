"""Shared utilities for grouping patterns into named buckets."""
from typing import Optional


def bucket_name(pattern_name: str) -> Optional[str]:
    lower = pattern_name.lower()
    if "vcp" in lower or "mmu" in lower or "mmd" in lower:
        return "vcp"
    if "head" in lower and "shoulder" in lower:
        return "h&s"
    if "flag" in lower or "pennant" in lower:
        return "flags"
    if "flat" in lower or "base" in lower:
        return "flat_base"
    if "pullback" in lower or "throwback" in lower:
        return "pullback"
    if "cup" in lower or "triangle" in lower or "rectangle" in lower or "channel" in lower:
        return "breakout"
    return None
