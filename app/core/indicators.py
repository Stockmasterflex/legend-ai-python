from typing import Any, Dict, List


def sma(values: List[float], period: int) -> List[float]:
    if not values or period <= 0:
        return []
    out: List[float] = []
    window_sum = 0.0
    for i, v in enumerate(values):
        window_sum += float(v)
        if i >= period:
            window_sum -= float(values[i - period])
        if i + 1 >= period:
            out.append(window_sum / period)
        else:
            out.append(float("nan"))
    return out


def ema(values: List[float], period: int) -> List[float]:
    if not values or period <= 0:
        return []
    k = 2 / (period + 1)
    out: List[float] = []
    ema_prev = None
    for i, v in enumerate(values):
        price = float(v)
        if ema_prev is None:
            ema_prev = price
        else:
            ema_prev = price * k + ema_prev * (1 - k)
        out.append(ema_prev)
    return out


def rsi(values: List[float], period: int = 14) -> List[float]:
    if not values or len(values) < 2:
        return []
    gains: List[float] = [0.0]
    losses: List[float] = [0.0]
    for i in range(1, len(values)):
        change = float(values[i]) - float(values[i - 1])
        gains.append(max(change, 0.0))
        losses.append(max(-change, 0.0))

    avg_gain = sum(gains[1 : period + 1]) / period if len(gains) > period else 0.0
    avg_loss = sum(losses[1 : period + 1]) / period if len(losses) > period else 0.0
    out: List[float] = [float("nan")] * len(values)

    if period < len(values):
        rs = (avg_gain / avg_loss) if avg_loss != 0 else float("inf")
        out[period] = 100 - (100 / (1 + rs))

    for i in range(period + 1, len(values)):
        avg_gain = (avg_gain * (period - 1) + gains[i]) / period
        avg_loss = (avg_loss * (period - 1) + losses[i]) / period
        rs = (avg_gain / avg_loss) if avg_loss != 0 else float("inf")
        out[i] = 100 - (100 / (1 + rs))

    return out


def detect_rsi_divergences(
    closes: List[float], rsi_values: List[float]
) -> List[Dict[str, Any]]:
    """Very simple swing-based divergence detector.
    - Bullish: price makes lower low while RSI makes higher low
    - Bearish: price makes higher high while RSI makes lower high
    Returns list of {type: 'bullish'|'bearish', index: int}
    """
    if not closes or not rsi_values or len(closes) != len(rsi_values):
        return []

    def is_local_min(i: int) -> bool:
        if i <= 0 or i >= len(closes) - 1:
            return False
        return closes[i] < closes[i - 1] and closes[i] < closes[i + 1]

    def is_local_max(i: int) -> bool:
        if i <= 0 or i >= len(closes) - 1:
            return False
        return closes[i] > closes[i - 1] and closes[i] > closes[i + 1]

    lows = [i for i in range(1, len(closes) - 1) if is_local_min(i)]
    highs = [i for i in range(1, len(closes) - 1) if is_local_max(i)]
    out: List[Dict[str, Any]] = []

    # Check last two swing lows/highs only to keep it fast and deterministic
    if len(lows) >= 2:
        i1, i2 = lows[-2], lows[-1]
        if closes[i2] < closes[i1] and rsi_values[i2] > rsi_values[i1]:
            out.append({"type": "bullish", "index": i2})
    if len(highs) >= 2:
        i1, i2 = highs[-2], highs[-1]
        if closes[i2] > closes[i1] and rsi_values[i2] < rsi_values[i1]:
            out.append({"type": "bearish", "index": i2})

    return out
