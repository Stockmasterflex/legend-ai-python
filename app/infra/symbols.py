"""Symbol helpers for Chart-IMG/TradingView.

Small, synchronous helpers only. Keep network checks optional elsewhere.
"""


def to_chartimg_symbol(ticker: str) -> str:
    """Return a best-effort symbol string for Chart-IMG.

    Simple fallback: just uppercase the ticker. Exchange prefixing can be added
    later if needed (e.g., NASDAQ:NVDA, NYSE:IBM) after verifying via a HEAD
    check on a symbol endpoint. For now, keep it deterministic and fast.
    """
    return (ticker or "").upper()
