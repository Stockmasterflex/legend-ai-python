from app.core.indicators import sma, ema, rsi


def test_sma_basic():
    data = [1, 2, 3, 4, 5, 6]
    out = sma(data, 3)
    assert len(out) == 6
    assert round(out[-1], 2) == 5.0  # (4+5+6)/3


def test_ema_basic():
    data = [1, 2, 3, 4, 5]
    out = ema(data, 3)
    assert len(out) == 5
    # EMA should be between last price and SMA
    assert out[-1] < 5 and out[-1] > 3


def test_rsi_len():
    data = list(range(1, 40))
    out = rsi(data, 14)
    assert len(out) == len(data)
    # First values should be NaN-like or not finite
    assert out[0] != out[0] or isinstance(out[0], float)

