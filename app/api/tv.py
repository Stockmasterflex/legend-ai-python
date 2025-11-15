from fastapi import APIRouter, Query
from fastapi.responses import HTMLResponse
from pathlib import Path
from urllib.parse import quote

from app.utils.build_info import resolve_build_sha

router = APIRouter(tags=["tradingview"])

TEMPLATE_PATH = Path(__file__).resolve().parents[2] / "templates" / "tv_symbol_lab.html"
TV_TEMPLATE_PATH = Path(__file__).resolve().parents[2] / "templates" / "partials" / "tv_widget_templates.html"


def _normalize_symbol(raw_symbol: str | None) -> str:
    """Ensure we always return an uppercase TradingView symbol."""
    if not raw_symbol:
        return "NASDAQ:AAPL"
    symbol = raw_symbol.strip().upper()
    if ":" not in symbol:
        symbol = f"NASDAQ:{symbol}"
    return symbol


def _inject_tv_templates(html: str) -> str:
    if "<!--TV_WIDGET_TEMPLATES-->" not in html:
        return html
    try:
        partial = TV_TEMPLATE_PATH.read_text(encoding="utf-8")
    except FileNotFoundError:
        partial = ""
    return html.replace("<!--TV_WIDGET_TEMPLATES-->", partial)


def _render_symbol_page(symbol: str) -> HTMLResponse:
    html = TEMPLATE_PATH.read_text(encoding="utf-8")
    build_sha = resolve_build_sha()
    html = html.replace("{{ build_sha }}", build_sha)
    html = html.replace("__DEFAULT_TV_SYMBOL__", symbol)
    html = _inject_tv_templates(html)
    return HTMLResponse(content=html)


@router.get("/tv", response_class=HTMLResponse)
async def tv_symbol_lab(tvwidgetsymbol: str = Query(None)):
    """TradingView Symbol Lab page linked from dashboard call-to-actions."""
    symbol = _normalize_symbol(tvwidgetsymbol)
    return _render_symbol_page(symbol)


@router.get("/tv/{symbol}", response_class=HTMLResponse)
async def tv_symbol_lab_path(symbol: str):
    return _render_symbol_page(_normalize_symbol(symbol))
