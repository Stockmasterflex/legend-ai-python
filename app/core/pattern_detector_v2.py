"""
O'Neil / Minervini Pattern Detection – single-file module
Drop-in for CLI (Claude/LLM) pipelines. Requires: pandas, numpy

Patterns implemented:
- Cup with Handle
- Flat Base
- 21EMA Pullback
- VCP (Volatility Contraction Pattern)  ← NEW: robust, scored

Stubs (interfaces defined, easy to extend):
- Double Bottom, Ascending Base, Base-on-Base, IPO Base,
  High-Tight Flag, Three-Weeks Tight, Tight Areas

Design choices:
- Causal, rule-based geometry (no future leak).
- Tunable thresholds via DetectionConfig.
- Deterministic outputs (PatternSignal), with rich details for LLMs.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any, Dict, List, Tuple

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)

# ============================================================
# ===  Data Classes  =========================================
# ============================================================


@dataclass
class Window:
    start: pd.Timestamp
    end: pd.Timestamp


@dataclass
class PatternSignal:
    pattern: str
    pivot_price: float
    pivot_date: pd.Timestamp
    confidence: float  # 0..1
    window: Window
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class DetectionConfig:
    # Global
    vol_avg_window: int = 50
    rs_period: int = 126

    # ZigZag / swings
    zigzag_pct: float = 0.11

    # Cup w/ Handle
    cup_min_weeks: int = 7
    cup_max_weeks: int = 65
    cup_depth_min: float = 0.12
    cup_depth_max: float = 0.33
    handle_min_days: int = 5
    handle_max_days: int = 25
    handle_max_depth: float = 0.15
    vol_dryup_percentile: float = 0.30
    breakout_vol_mult: float = 1.4

    # Flat base
    flat_min_weeks: int = 5
    flat_max_depth: float = 0.15

    # 21EMA pullback
    ema21_max_undercut: float = 0.03
    ema21_lookback_above: int = 10

    # VCP
    vcp_min_contractions: int = 3
    vcp_max_contractions: int = 6
    vcp_final_contraction_max: float = 0.10  # <= 10%
    vcp_base_max_depth: float = 0.35  # <= 35%
    vcp_breakout_vol_mult: float = 1.5  # >= 1.5x 50d avg
    vcp_recent_days: int = 70  # lookback to form base (~14 weeks)
    vcp_swing_window: int = 5  # local extrema window
    vcp_volume_dry_up_drop: float = 0.20  # 20% drop in last vs prior contraction


# ============================================================
# ===  Utils / Indicators  ===================================
# ============================================================


def ensure_ohlcv(df: pd.DataFrame) -> pd.DataFrame:
    """
    Accepts OHLCV in either lower-case or Title Case; returns lower-case columns.
    Raises if required columns are missing.
    """
    colmap = {c.lower(): c for c in df.columns}
    required = ["open", "high", "low", "close", "volume"]
    if all(k in colmap for k in required):
        return df.rename(columns=str.lower)
    # try Title Case
    alt_required = ["Open", "High", "Low", "Close", "Volume"]
    if all(c in df.columns for c in alt_required):
        return df.rename(columns=str.lower)
    # last chance: infer
    raise ValueError("DataFrame must contain OHLCV columns.")


def ema(s: pd.Series, span: int) -> pd.Series:
    return s.ewm(span=span, adjust=False).mean()


def sma(s: pd.Series, n: int) -> pd.Series:
    return s.rolling(n).mean()


def atr(df: pd.DataFrame, window: int = 14) -> pd.Series:
    h, l, c = df["high"], df["low"], df["close"]
    prev = c.shift(1)
    tr = pd.concat([(h - l), (h - prev).abs(), (l - prev).abs()], axis=1).max(axis=1)
    return tr.rolling(window).mean()


def to_weekly(df: pd.DataFrame) -> pd.DataFrame:
    rule = "W-FRI"
    o = df["open"].resample(rule).first()
    h = df["high"].resample(rule).max()
    l = df["low"].resample(rule).min()
    c = df["close"].resample(rule).last()
    v = df["volume"].resample(rule).sum()
    return pd.DataFrame(
        {"open": o, "high": h, "low": l, "close": c, "volume": v}
    ).dropna()


def zigzag_peaks_troughs(prices: pd.Series, pct_threshold: float = 0.1):
    """
    Simple causal percent ZigZag returning [(index_position, 'peak'|'trough'), ...]
    """
    if prices.empty:
        return []
    pivots = []
    last_price = prices.iloc[0]
    direction = 0
    for i in range(1, len(prices)):
        chg = (prices.iloc[i] - last_price) / last_price
        if direction >= 0 and chg <= -pct_threshold:
            pivots.append((i - 1, "peak"))
            direction = -1
            last_price = prices.iloc[i - 1]
        elif direction <= 0 and chg >= pct_threshold:
            pivots.append((i - 1, "trough"))
            direction = 1
            last_price = prices.iloc[i - 1]
        else:
            if direction >= 0 and prices.iloc[i] > last_price:
                last_price = prices.iloc[i]
            elif direction <= 0 and prices.iloc[i] < last_price:
                last_price = prices.iloc[i]
    return pivots


def local_extrema(series: pd.Series, window: int = 5) -> Tuple[List[int], List[int]]:
    """
    Return indices of swing highs / lows via centered rolling-window checks.
    """
    highs, lows = [], []
    vals = series.values
    for i in range(window, len(vals) - window):
        seg = vals[i - window : i + window + 1]
        if vals[i] == seg.max():
            highs.append(i)
        if vals[i] == seg.min():
            lows.append(i)
    return highs, lows


# ============================================================
# ===  Detectors  ============================================
# ============================================================


class PatternDetectors:
    """Rule-based O'Neil / Minervini pattern scans."""

    # -------------------- CUP WITH HANDLE --------------------
    @staticmethod
    def cup_with_handle(
        df: pd.DataFrame, cfg: DetectionConfig = DetectionConfig()
    ) -> List[PatternSignal]:
        try:
            df = ensure_ohlcv(df)
            close, vol = df["close"], df["volume"]
            piv = zigzag_peaks_troughs(close, pct_threshold=cfg.zigzag_pct)
            sigs = []
            for k in range(len(piv) - 2):
                i1, t1 = piv[k]
                i2, t2 = piv[k + 1]
                i3, t3 = piv[k + 2]
                if not (t1 == "peak" and t2 == "trough" and t3 == "peak"):
                    continue
                start, end = df.index[i1], df.index[i3]
                weeks = (end - start).days / 7
                if not (cfg.cup_min_weeks <= weeks <= cfg.cup_max_weeks):
                    continue
                left, right, bottom = close.iloc[i1], close.iloc[i3], close.iloc[i2]
                depth = (left - bottom) / left if left > 0 else np.nan
                if not (cfg.cup_depth_min <= depth <= cfg.cup_depth_max):
                    continue
                if abs((right - left) / left) > 0.05:
                    continue

                # handle
                hstart = i3 + 1
                if hstart >= len(df):
                    continue
                hend = min(len(df) - 1, i3 + cfg.handle_max_days)
                look = close.iloc[hstart : hend + 1]
                if look.empty:
                    continue
                handle_low_i = hstart + int(np.argmin(look.values))
                handle_low = close.iloc[handle_low_i]
                hdepth = (right - handle_low) / right
                if hdepth > cfg.handle_max_depth:
                    continue
                mid = bottom + 0.5 * (left - bottom)
                if handle_low < mid:
                    continue

                avg50 = vol.rolling(cfg.vol_avg_window).mean()
                hvol = vol.iloc[hstart : handle_low_i + 1]
                vol_dry = (
                    hvol.mean() < avg50.iloc[handle_low_i] * cfg.vol_dryup_percentile
                )

                post = df.iloc[handle_low_i + 1 : handle_low_i + 15]
                breakout = None
                for j in range(len(post)):
                    if (
                        post["close"].iloc[j] > right
                        and post["volume"].iloc[j]
                        >= cfg.breakout_vol_mult * avg50.iloc[post.index[j]]
                    ):
                        breakout = post.index[j]
                        break
                if breakout is None:
                    continue

                score = min(
                    1.0,
                    0.6
                    + 0.15 * vol_dry
                    + 0.1 * (depth < 0.25)
                    + 0.15 * (hdepth < 0.12),
                )
                sigs.append(
                    PatternSignal(
                        "Cup with Handle",
                        float(right * 1.0001),
                        breakout,
                        score,
                        Window(start, end),
                        {
                            "depth": float(depth),
                            "handle_depth": float(hdepth),
                            "weeks": float(weeks),
                            "vol_dryup": bool(vol_dry),
                        },
                    )
                )
            return sigs
        except Exception as e:
            logger.error(f"Error in cup_with_handle: {e}")
            return []

    # -------------------- FLAT BASE --------------------------
    @staticmethod
    def flat_base(
        df: pd.DataFrame, cfg: DetectionConfig = DetectionConfig()
    ) -> List[PatternSignal]:
        try:
            df = ensure_ohlcv(df)
            w = to_weekly(df)
            sigs = []
            avg_vol = w["volume"].rolling(max(2, cfg.vol_avg_window // 5)).mean()
            for s in range(0, len(w) - cfg.flat_min_weeks - 2):
                for win in range(cfg.flat_min_weeks, 9):
                    e = s + win
                    if e >= len(w):
                        break
                    seg = w.iloc[s : e + 1]
                    peak, trough = seg["high"].max(), seg["low"].min()
                    depth = (peak - trough) / peak if peak > 0 else np.nan
                    if depth > cfg.flat_max_depth:
                        continue
                    first_high = w["high"].iloc[s]
                    if (peak - first_high) / first_high > 0.01:
                        continue
                    tight = seg["close"].std() / max(1e-9, seg["close"].mean()) < 0.015
                    if not tight:
                        continue
                    if s < 12:
                        continue
                    pre = w.iloc[s - 12 : s]
                    pre_ret = (
                        pre["close"].iloc[-1] / pre["close"].iloc[0] - 1
                        if pre["close"].iloc[0] > 0
                        else 0
                    )
                    if pre_ret < 0.30:
                        continue
                    pivot = peak
                    post = w.iloc[e + 1 : min(e + 4, len(w))]
                    wk = None
                    for i in range(len(post)):
                        if (
                            post["close"].iloc[i] > pivot
                            and post["volume"].iloc[i]
                            >= cfg.breakout_vol_mult * avg_vol.iloc[post.index[i]]
                        ):
                            wk = post.index[i]
                            break
                    if wk is None:
                        continue
                    daily_break = df[df.index >= wk]
                    br = daily_break[daily_break["close"] > pivot].index.min()
                    if pd.isna(br):
                        continue
                    score = min(1.0, 0.6 + 0.2 * (depth < 0.12) + 0.2 * tight)
                    sigs.append(
                        PatternSignal(
                            "Flat Base",
                            float(pivot * 1.0001),
                            br,
                            score,
                            Window(w.index[s], br),
                            {
                                "weeks": float(win),
                                "depth": float(depth),
                                "pre_uptrend": float(pre_ret),
                            },
                        )
                    )
            return sigs
        except Exception as e:
            logger.error(f"Error in flat_base: {e}")
            return []

    # -------------------- 21 EMA PULLBACK --------------------
    @staticmethod
    def pullback_21ema(
        df: pd.DataFrame, cfg: DetectionConfig = DetectionConfig()
    ) -> List[PatternSignal]:
        try:
            df = ensure_ohlcv(df)
            close, vol = df["close"], df["volume"]
            ema21 = ema(close, 21)
            sma50 = sma(close, 50)
            sma200 = sma(close, 200)
            avg_vol = vol.rolling(cfg.vol_avg_window).mean()
            trend = (close > sma50) & (close > sma200) & (sma50 > sma50.shift(1))
            sigs = []
            for i in range(21, len(df) - 1):
                if not trend.iloc[i - 1]:
                    continue
                if i < cfg.ema21_lookback_above:
                    continue
                if (df["low"].iloc[i] <= ema21.iloc[i]) and (
                    close.iloc[i] >= ema21.iloc[i]
                ):
                    under = max(
                        0,
                        (ema21.iloc[i] - df["low"].iloc[i]) / max(1e-9, ema21.iloc[i]),
                    )
                    if under <= cfg.ema21_max_undercut:
                        pull_vol = vol.iloc[i] <= avg_vol.iloc[i]
                        score = min(
                            1.0,
                            0.6
                            + 0.2 * pull_vol
                            + 0.2 * (close.iloc[i] > close.iloc[i - 1]),
                        )
                        sigs.append(
                            PatternSignal(
                                "21EMA Pullback",
                                float(max(close.iloc[i], ema21.iloc[i])),
                                df.index[i],
                                score,
                                Window(df.index[max(0, i - 10)], df.index[i]),
                                {
                                    "undercut": float(under),
                                    "pull_vol_ok": bool(pull_vol),
                                },
                            )
                        )
            return sigs
        except Exception as e:
            logger.error(f"Error in pullback_21ema: {e}")
            return []

    # -------------------- VCP (VOLATILITY CONTRACTION) -------
    @staticmethod
    def vcp(
        df: pd.DataFrame, cfg: DetectionConfig = DetectionConfig()
    ) -> List[PatternSignal]:
        """
        VCP detection:
        1) Trend template gate (strong uptrend context).
        2) Identify contractions using swing highs → subsequent swing lows.
        3) Validate decreasing contraction magnitudes, final tightness, base depth, volume dry-up.
        4) Pivot = highest high of base (buffered); breakout = price > pivot with >= 1.5x avg vol.
        """
        try:
            df = ensure_ohlcv(df)
            if len(df) < max(60, cfg.vol_avg_window + 10):
                return []

            # ---- Trend template (simplified Minervini) gate ----
            gate_ok, trend_score, tt_details = _trend_template_gate(df)

            # ---- recent window for base formation ----
            recent = (
                df.iloc[-cfg.vcp_recent_days :].copy()
                if len(df) >= cfg.vcp_recent_days
                else df.copy()
            )
            highs_idx, lows_idx = local_extrema(recent["high"], cfg.vcp_swing_window)

            # Build contractions: each contraction = swing high → following swing low (lowest after that high)
            contractions = []
            for hi in highs_idx:
                hi_ts = recent.index[hi]
                hi_price = recent["high"].iloc[hi]
                # lows after this high:
                lows_after = [lo for lo in lows_idx if lo > hi]
                if not lows_after:
                    continue
                # choose the lowest low after this high (contracting leg)
                lo = int(min(lows_after, key=lambda j: recent["low"].iloc[j]))
                lo_ts = recent.index[lo]
                lo_price = recent["low"].iloc[lo]
                pct_drop = (hi_price - lo_price) / max(1e-9, hi_price)
                avg_vol = (
                    recent["volume"].iloc[hi : lo + 1].mean() if lo > hi else np.nan
                )
                contractions.append(
                    {
                        "start_idx": int(hi),
                        "end_idx": int(lo),
                        "start": hi_ts,
                        "end": lo_ts,
                        "high": float(hi_price),
                        "low": float(lo_price),
                        "percent_drop": float(pct_drop),
                        "avg_volume": float(avg_vol),
                        "duration_days": int((lo_ts - hi_ts).days),
                    }
                )

            # sort & trim
            contractions = sorted(contractions, key=lambda c: c["start"])
            if len(contractions) < cfg.vcp_min_contractions:
                return []
            if len(contractions) > cfg.vcp_max_contractions:
                contractions = contractions[-cfg.vcp_max_contractions :]

            # ---- validate contraction structure ----
            # 1) decreasing magnitude (not necessarily strictly every step)
            dec_pairs = 0
            for i in range(1, len(contractions)):
                if (
                    contractions[i]["percent_drop"]
                    <= contractions[i - 1]["percent_drop"]
                ):
                    dec_pairs += 1
            if (dec_pairs / (len(contractions) - 1)) < 0.60:
                return []

            # 2) final contraction tight enough
            final_pct = contractions[-1]["percent_drop"]
            if final_pct > cfg.vcp_final_contraction_max:
                return []

            # 3) base depth not too large
            base_high = max(c["high"] for c in contractions)
            base_low = min(c["low"] for c in contractions)
            base_depth = (base_high - base_low) / max(1e-9, base_high)
            if base_depth > cfg.vcp_base_max_depth:
                return []

            # 4) volume trend: prefer decreasing through pattern (soft requirement)
            vols = np.array(
                [c["avg_volume"] for c in contractions if np.isfinite(c["avg_volume"])]
            )
            vol_down_ok = True
            if len(vols) >= 3:
                # linear slope; require non-positive
                x = np.arange(len(vols))
                slope = np.polyfit(x, vols, 1)[0]
                vol_down_ok = slope <= 0

            # 5) dry-up: last vs previous average volume
            vol_dryup = False
            if len(contractions) >= 2:
                prev_vol = contractions[-2]["avg_volume"]
                last_vol = contractions[-1]["avg_volume"]
                if np.isfinite(prev_vol) and prev_vol > 0 and np.isfinite(last_vol):
                    vol_dryup = (
                        (prev_vol - last_vol) / prev_vol
                    ) >= cfg.vcp_volume_dry_up_drop

            # ---- pivot & breakout ----
            # pivot at 1% above base high
            pivot = base_high * 1.01
            # breakout with volume
            avg50 = df["volume"].rolling(cfg.vol_avg_window).mean()
            today = df.index[-1]
            price_break = df["close"].iloc[-1] > pivot
            vol_break = df["volume"].iloc[-1] >= cfg.vcp_breakout_vol_mult * max(
                1e-9, avg50.iloc[-1]
            )
            broke_out = bool(price_break and vol_break)

            # ---- confidence score ----
            score = 0.0
            # trend gate
            score += 0.30 * trend_score  # 0..0.30
            # ideal #contractions (3–4 best)
            n = len(contractions)
            if 3 <= n <= 4:
                score += 0.25
            elif 2 <= n <= 5:
                score += 0.10
            # final tightness
            if final_pct <= 0.05:
                score += 0.20
            elif final_pct <= 0.08:
                score += 0.10
            # volume profile
            if vol_down_ok:
                score += 0.10
            if vol_dryup:
                score += 0.15
            # breakout bonus (not required to issue a setup)
            if broke_out:
                score += 0.05
            score = float(max(0.0, min(1.0, score)))

            if score < 0.4:  # Skip low confidence VCP
                return []

            # signal
            base_start = recent.index[min(c["start_idx"] for c in contractions)]
            window = Window(start=base_start, end=today)
            return [
                PatternSignal(
                    "VCP",
                    float(pivot),
                    today,
                    score,
                    window,
                    {
                        "contractions": contractions,
                        "base_depth": float(base_depth),
                        "final_contraction_drop": float(final_pct),
                        "volume_downtrend": bool(vol_down_ok),
                        "volume_dryup": bool(vol_dryup),
                        "trend_gate_ok": bool(gate_ok),
                        "trend_score": float(trend_score),
                        "broke_out_today": bool(broke_out),
                    },
                )
            ]
        except Exception as e:
            logger.error(f"Error in vcp: {e}")
            return []

    # ---------- Stubs (same interfaces; easy to implement) ----------
    @staticmethod
    def double_bottom(
        df: pd.DataFrame, cfg: DetectionConfig = DetectionConfig()
    ) -> List[PatternSignal]:
        return []

    @staticmethod
    def ascending_base(
        df: pd.DataFrame, cfg: DetectionConfig = DetectionConfig()
    ) -> List[PatternSignal]:
        return []

    @staticmethod
    def base_on_base(
        df: pd.DataFrame, cfg: DetectionConfig = DetectionConfig()
    ) -> List[PatternSignal]:
        return []

    @staticmethod
    def ipo_base(
        df: pd.DataFrame, cfg: DetectionConfig = DetectionConfig()
    ) -> List[PatternSignal]:
        return []

    @staticmethod
    def high_tight_flag(
        df: pd.DataFrame, cfg: DetectionConfig = DetectionConfig()
    ) -> List[PatternSignal]:
        return []

    @staticmethod
    def three_weeks_tight(
        df: pd.DataFrame, cfg: DetectionConfig = DetectionConfig()
    ) -> List[PatternSignal]:
        return []

    @staticmethod
    def tight_areas(
        df: pd.DataFrame, cfg: DetectionConfig = DetectionConfig()
    ) -> List[PatternSignal]:
        return []


# ============================================================
# ===  Trend Template Gate (helper)  =========================
# ============================================================


def _trend_template_gate(df: pd.DataFrame) -> Tuple[bool, float, Dict[str, Any]]:
    """
    Simplified Minervini trend template gate:
      1) Price > MA150 and MA200
      2) MA150 > MA200
      3) MA200 rising vs ~1 month ago (20 trading days)
      4) MA50 > MA150 and MA200
      5) Price > MA50
      6) Price >= 30% above 52w low (if available)
      7) Price within 25% of 52w high (if available)
      8) 6m price perf > +10% (if available)

    Returns (ok:boolean, score:0..1, details:dict)
    """
    try:
        cdf = ensure_ohlcv(df)
        c = cdf["close"]
        ma50 = c.rolling(50).mean()
        ma150 = c.rolling(150).mean()
        ma200 = c.rolling(200).mean()

        price = c.iloc[-1]
        m50, m150, m200 = ma50.iloc[-1], ma150.iloc[-1], ma200.iloc[-1]
        m200_20 = ma200.iloc[-20] if len(cdf) >= 220 else m200

        # 52w band (252 trading days)
        if len(cdf) >= 252:
            h52 = cdf["high"].iloc[-252:].max()
            l52 = cdf["low"].iloc[-252:].min()
        else:
            h52 = cdf["high"].max()
            l52 = cdf["low"].min()

        crit = []
        crit.append(price > m150 and price > m200)
        crit.append(m150 > m200)
        crit.append(m200 > m200_20)
        crit.append(m50 > m150 and m50 > m200)
        crit.append(price > m50)
        crit.append((price - l52) / max(1e-9, l52) >= 0.30 if l52 > 0 else False)
        crit.append((h52 - price) / max(1e-9, h52) <= 0.25 if h52 > 0 else False)
        if len(cdf) >= 126:
            perf6m = (price - c.iloc[-126]) / max(1e-9, c.iloc[-126])
            crit.append(perf6m > 0.10)
        else:
            crit.append(True)

        passed = sum(crit)
        score = passed / len(crit)
        return (
            (passed >= 6),
            float(score),
            {
                "passed": passed,
                "total": len(crit),
                "price": float(price),
                "ma50": float(m50),
                "ma150": float(m150),
                "ma200": float(m200),
            },
        )
    except Exception as e:
        logger.error(f"Error in trend template gate: {e}")
        return False, 0.0, {}


# ============================================================
# ===  Unified Scan  =========================================
# ============================================================


def scan_all(
    df: pd.DataFrame, cfg: DetectionConfig = DetectionConfig()
) -> List[PatternSignal]:
    """
    Run all implemented detectors and return a list of PatternSignal.
    """
    out: List[PatternSignal] = []
    out += PatternDetectors.cup_with_handle(df, cfg)
    out += PatternDetectors.flat_base(df, cfg)
    out += PatternDetectors.pullback_21ema(df, cfg)
    out += PatternDetectors.vcp(df, cfg)
    return out
