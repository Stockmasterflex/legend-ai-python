"""
Universe scanner that evaluates VCP patterns across the daily universe.
"""
from __future__ import annotations

import asyncio
import logging
import time
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

import pandas as pd

from app.core.classifiers import minervini_trend_template
from app.core.detectors.vcp_detector import VCPDetector
from app.core.detector_base import PatternResult as DetectorPatternResult
from app.core.metrics import (
    compute_atr,
    last_valid,
    percentage_distance,
    relative_strength_metrics,
)
from app.services import universe_data
from app.services.market_data import market_data_service
from app.services.universe_store import universe_store
from app.utils.build_info import resolve_build_sha
from app.telemetry.metrics import (
    CACHE_HITS_TOTAL,
    CACHE_MISSES_TOTAL,
    DETECTOR_RUNTIME_SECONDS,
)

logger = logging.getLogger(__name__)


def _has_prices(payload: Optional[Dict[str, Any]]) -> bool:
    return bool(payload and payload.get("c"))


def _utcnow_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


class ScannerService:
    """Feature-flagged scanner that focuses on daily VCP detection."""

    def __init__(
        self,
        *,
        max_symbols: int = 600,
        bars: int = 320,
        max_concurrency: int = 8,
        min_confidence: float = 0.45,
    ) -> None:
        self.max_symbols = max_symbols
        self.output_bars = bars
        self.max_concurrency = max_concurrency
        self.detector = VCPDetector()
        self.min_confidence = min_confidence

    async def run_daily_vcp_scan(
        self,
        universe: Optional[List[str]] = None,
        limit: int = 50,
        sector: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Scan the universe for VCP patterns."""
        started = time.perf_counter()
        universe_meta = await universe_store.get_all()
        if not universe_meta:
            fallback = universe_data.get_full_universe()
            universe_meta = {symbol: {"symbol": symbol, "universe": "fallback"} for symbol in fallback}

        if sector:
            normalized = sector.strip().lower()
            universe_meta = {
                sym: meta
                for sym, meta in universe_meta.items()
                if meta and meta.get("sector") and meta["sector"].strip().lower() == normalized
            }

        if universe:
            symbols = [sym.upper() for sym in universe if sym.upper() in universe_meta]
        else:
            symbols = list(universe_meta.keys())

        symbols = symbols[: self.max_symbols]
        if not symbols:
            return self._response(started, 0, [])

        spy_series = await market_data_service.get_time_series("SPY", "1day", self.output_bars)
        self._record_cache_metric(spy_series)
        spy_closes = spy_series.get("c", []) if _has_prices(spy_series) else []

        sem = asyncio.Semaphore(self.max_concurrency)
        missing_data_symbols: List[str] = []
        tasks = [
            self._scan_symbol(
                symbol,
                universe_meta.get(symbol, {}),
                spy_closes,
                sem,
                missing_data_symbols,
            )
            for symbol in symbols
        ]
        raw_results = await asyncio.gather(*tasks)
        results = [item for item in raw_results if item]
        results.sort(key=lambda item: item["legend_score"], reverse=True)

        total_hits = len(results)
        limited_hits = results[:limit]
        remaining_slots = max(limit - len(limited_hits), 0)
        placeholders = self._missing_data_results(missing_data_symbols, remaining_slots)
        final_results = limited_hits + placeholders
        duration = time.perf_counter() - started
        logger.info(
            "scan_complete universe=%s hits=%s duration_ms=%.1f",
            len(symbols),
            len(final_results),
            duration * 1000,
        )
        return self._response(started, len(symbols), final_results, total_hits=total_hits)

    async def _scan_symbol(
        self,
        symbol: str,
        metadata: Dict[str, Any],
        spy_closes: List[float],
        sem: asyncio.Semaphore,
        missing_symbols: List[str],
    ) -> Optional[Dict[str, Any]]:
        async with sem:
            price_data = await market_data_service.get_time_series(
                ticker=symbol,
                interval="1day",
                outputsize=self.output_bars,
            )
            self._record_cache_metric(price_data)
            if not _has_prices(price_data):
                missing_symbols.append(symbol)
                return None

            df = self._to_dataframe(price_data)
            with DETECTOR_RUNTIME_SECONDS.labels(pattern="VCP").time():
                detections = self.detector.find(df, "1D", symbol)
            if not detections:
                return None

            best = max(detections, key=lambda d: d.confidence)
            if best.confidence < self.min_confidence:
                return None

            payload = self._build_result(symbol, df, best, spy_closes)
            return payload

    def _build_result(
        self,
        symbol: str,
        df: pd.DataFrame,
        detection: DetectorPatternResult,
        spy_closes: List[float],
    ) -> Dict[str, Any]:
        closes = df["close"].tolist()
        highs = df["high"].tolist()
        lows = df["low"].tolist()
        volumes = df["volume"].tolist()
        last_close = closes[-1]
        ema21_series = df["close"].ewm(span=21, adjust=False).mean().tolist()
        sma50_series = df["close"].rolling(50).mean().tolist()
        sma200_series = df["close"].rolling(200).mean().tolist()
        ema21_val = last_valid(ema21_series)
        sma50_val = last_valid(sma50_series)
        sma200_val = last_valid(sma200_series)
        ma_dist = {
            "ema21": percentage_distance(last_close, ema21_val),
            "sma50": percentage_distance(last_close, sma50_val),
            "sma200": percentage_distance(last_close, sma200_val),
        }

        atr_series = compute_atr(highs, lows, closes, period=14)
        atr_value = atr_series[-1] if atr_series else None

        rs_metrics = relative_strength_metrics(closes, spy_closes)
        rs_rank = rs_metrics.get("rank")

        trend = minervini_trend_template(closes)
        trend_pass = bool(trend.get("pass"))

        score = self._legend_score(detection.confidence, rs_rank, trend_pass)
        grade = self._grade(score)
        reasons = self._reasons(detection, rs_rank, trend_pass)
        contractions = len(detection.evidence.get("contraction_sequence", [])) if detection.evidence else None
        max_pullback = self._max_pullback_pct(detection)
        base_days = self._base_days(detection)
        pivot = self._pivot_price(detection)

        atr_plan = self._atr_plan(pivot, atr_value)

        return {
            "symbol": symbol,
            "timeframe": "1D",
            "pattern": "VCP",
            "legend_score": score,
            "grade": grade,
            "reasons": reasons,
            "signals": {
                "vol_contractions": contractions,
                "max_pullback_pct": max_pullback,
                "base_days": base_days,
                "pivot": pivot,
                "rs_rank": rs_rank,
                "ma_dist": ma_dist,
            },
            "rule_failures": trend.get("failed_rules", []),
            "atr_plan": atr_plan,
            "chart_url": None,
            "sources": {
                "price": price_data.get("source") if isinstance(price_data, dict) else None,
                "spy": "SPY",
                "sector": metadata.get("sector") if metadata else None,
            },
        }

    @staticmethod
    def _max_pullback_pct(detection: DetectorPatternResult) -> Optional[float]:
        evidence = detection.evidence or {}
        contractions = evidence.get("contraction_sequence") or []
        declines = [c.get("decline_pct") for c in contractions if isinstance(c, dict) and c.get("decline_pct")]
        if not declines:
            return None
        return round(max(declines) * 100, 2)

    @staticmethod
    def _base_days(detection: DetectorPatternResult) -> Optional[int]:
        try:
            start = pd.to_datetime(detection.window_start)
            end = pd.to_datetime(detection.window_end)
            delta = (end - start).days
            return max(1, delta)
        except Exception:
            return None

    @staticmethod
    def _pivot_price(detection: DetectorPatternResult) -> Optional[float]:
        if detection.breakout and detection.breakout.get("price"):
            return round(float(detection.breakout.get("price")), 2)
        if detection.lines.get("last_contraction_high"):
            return round(float(detection.lines["last_contraction_high"]), 2)
        return None

    @staticmethod
    def _missing_data_results(symbols: List[str], limit: int) -> List[Dict[str, Any]]:
        results: List[Dict[str, Any]] = []
        seen = set()
        for symbol in symbols:
            if len(results) >= limit:
                break
            upper = symbol.upper()
            if upper in seen:
                continue
            seen.add(upper)
            results.append(
                {
                    "symbol": upper,
                    "timeframe": "1D",
                    "pattern": None,
                    "legend_score": None,
                    "grade": None,
                    "reasons": [],
                    "signals": {
                        "vol_contractions": None,
                        "max_pullback_pct": None,
                        "base_days": None,
                        "pivot": None,
                        "rs_rank": None,
                        "ma_dist": {"ema21": None, "sma50": None, "sma200": None},
                    },
                    "rule_failures": ["missing_ohlcv"],
                    "atr_plan": {"atr": None, "stop": None, "risk_unit": None},
                    "chart_url": None,
                    "sources": {"price": None, "spy": None, "sector": None},
                }
            )
        return results

    @staticmethod
    def _record_cache_metric(payload: Optional[Dict[str, Any]]) -> None:
        if payload and payload.get("cached"):
            CACHE_HITS_TOTAL.labels(name="scan").inc()
        else:
            CACHE_MISSES_TOTAL.labels(name="scan").inc()

    @staticmethod
    def _atr_plan(pivot: Optional[float], atr_value: Optional[float]) -> Dict[str, Optional[float]]:
        if not pivot:
            return {"atr": atr_value if atr_value else None, "stop": None, "risk_unit": None}
        atr_val = round(atr_value, 2) if atr_value else None
        stop_price = None
        risk_unit = None
        if atr_value:
            stop_price = round(pivot - 1.5 * atr_value, 2)
            stop_price = max(0.01, stop_price)
            risk_unit = round(((pivot - stop_price) / pivot) * 100, 2) if pivot else None
        return {
            "atr": atr_val,
            "stop": stop_price,
            "risk_unit": risk_unit,
        }

    @staticmethod
    def _reasons(
        detection: DetectorPatternResult,
        rs_rank: Optional[int],
        trend_pass: bool,
    ) -> List[str]:
        reasons = []
        contractions = detection.evidence.get("contraction_sequence") if detection.evidence else None
        if contractions:
            reasons.append(f"{len(contractions)} clean contractions")
        if rs_rank:
            reasons.append(f"RS rank {rs_rank}")
        reasons.append("Trend template pass" if trend_pass else "Trend template fail")
        return reasons

    @staticmethod
    def _grade(score: int) -> str:
        if score >= 95:
            return "A+"
        if score >= 85:
            return "A"
        if score >= 70:
            return "B"
        return "C"

    @staticmethod
    def _legend_score(confidence: float, rs_rank: Optional[int], trend_pass: bool) -> int:
        base = confidence * 70  # up to 70 points from detector confidence
        rs_bonus = (rs_rank or 50) * 0.2  # up to 20 points
        trend_bonus = 10 if trend_pass else -5
        score = base + rs_bonus + trend_bonus
        return int(max(0, min(100, round(score))))

    @staticmethod
    def _to_dataframe(payload: Dict[str, Any]) -> pd.DataFrame:
        closes = payload.get("c", [])
        opens = payload.get("o", closes)
        highs = payload.get("h", closes)
        lows = payload.get("l", closes)
        volumes = payload.get("v", [0] * len(closes))
        dates = payload.get("t") or []
        df = pd.DataFrame(
            {
                "open": opens,
                "high": highs,
                "low": lows,
                "close": closes,
                "volume": volumes,
            }
        )
        if dates:
            df["datetime"] = pd.to_datetime(dates, errors="coerce")
        else:
            df["datetime"] = pd.date_range(end=datetime.now(), periods=len(df), freq="B")
        return df.dropna(subset=["close"]).reset_index(drop=True)

    def _response(
        self,
        started: float,
        universe_size: int,
        results: List[Dict[str, Any]],
        *,
        total_hits: int = 0,
    ) -> Dict[str, Any]:
        duration_ms = (time.perf_counter() - started) * 1000
        return {
            "as_of": _utcnow_iso(),
            "universe_size": universe_size,
            "results": results,
            "meta": {
                "build_sha": resolve_build_sha(),
                "duration_ms": round(duration_ms, 2),
                "result_count": len(results),
                "total_hits": total_hits,
            },
        }


scan_service = ScannerService()

__all__ = ["ScannerService", "scan_service"]
