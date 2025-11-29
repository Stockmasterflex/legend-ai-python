from typing import Any, Dict, List

from .indicators import sma


def minervini_trend_template(closes: List[float]) -> Dict[str, Any]:
    """Simplified Minervini 8-point style checks using daily data.
    Uses SMA(50), SMA(150), SMA(200) and slope checks.
    Returns {pass: bool, failed_rules: [str]}
    """
    failed: List[str] = []
    if len(closes) < 200:
        return {"pass": False, "failed_rules": ["insufficient data"]}
    sma50 = sma(closes, 50)
    sma150 = sma(closes, 150)
    sma200 = sma(closes, 200)
    c = closes[-1]
    s50, s150, s200 = sma50[-1], sma150[-1], sma200[-1]

    # Slope checks (compare last vs value 10 bars ago)
    s50_prev = sma50[-11] if len(sma50) > 11 else s50
    s200_prev = sma200[-11] if len(sma200) > 11 else s200

    if not (c > s50):
        failed.append("close <= SMA50")
    if not (s50 > s150 > s200):
        failed.append("SMA50<=SMA150 or SMA150<=SMA200")
    if not (s200 > s200_prev):
        failed.append("SMA200 not rising")
    if not (s50 > s50_prev):
        failed.append("SMA50 not rising")

    return {"pass": len(failed) == 0, "failed_rules": failed}


def weinstein_stage(closes_weekly: List[float]) -> Dict[str, Any]:
    """Classify Stage 1–4 using 30-week SMA trend and price relative to it.
    Returns {stage: int, reason: str}
    """
    if len(closes_weekly) < 30:
        return {"stage": 0, "reason": "insufficient data"}
    sma30 = sma(closes_weekly, 30)
    c = closes_weekly[-1]
    s = sma30[-1]
    s_prev = sma30[-4] if len(sma30) > 4 else s
    rising = s > s_prev
    if c > s and rising:
        return {"stage": 2, "reason": "price above rising 30W SMA"}
    if c < s and not rising:
        return {"stage": 4, "reason": "price below falling 30W SMA"}
    if not rising and abs(c - s) / s if s else 0 < 0.03:
        return {"stage": 3, "reason": "near flattening 30W SMA"}
    return {"stage": 1, "reason": "basing / transition"}
