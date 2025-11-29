"""
Universe ingestion helper for S&P 500 and NASDAQ 100 lists.
"""
from __future__ import annotations

import asyncio
from datetime import datetime
from typing import Dict, List, Optional

import httpx
import pandas as pd
from sqlalchemy import text

from app.services.cache import get_cache_service
from app.services.database import get_database_service
from app.config import get_settings
import logging

logger = logging.getLogger(__name__)

SCAN_CACHE_KEY = "universe:metadata:latest"


def _parse_market_cap(value: Optional[str]) -> Optional[int]:
    if not value or not isinstance(value, str):
        return None

    normalized = value.strip().upper().replace("$", "").replace(",", "")
    if not normalized:
        return None

    multiplier = 1
    if normalized.endswith("T"):
        multiplier = 1_000_000_000_000
        normalized = normalized[:-1]
    elif normalized.endswith("B"):
        multiplier = 1_000_000_000
        normalized = normalized[:-1]
    elif normalized.endswith("M"):
        multiplier = 1_000_000
        normalized = normalized[:-1]

    try:
        number = float(normalized)
        return int(number * multiplier)
    except ValueError:
        try:
            return int(float(normalized))
        except ValueError:
            return None


class UniverseIngestor:
    """Fetch and persist curated universes."""

    SP500_URL = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    NASDAQ100_URL = "https://en.wikipedia.org/wiki/Nasdaq-100"

    def __init__(self):
        self.db = get_database_service()
        self.cache = get_cache_service()
        self.settings = get_settings()

    async def refresh(self) -> List[Dict[str, Optional[str]]]:
        """Fetch S&P 500 + NASDAQ 100 and persist to Postgres + Redis."""
        raw = await asyncio.to_thread(self._fetch_universe)
        if not raw:
            logger.warning("Universe ingest returned no symbols")
            return []

        self._persist_symbols(raw)
        try:
            await self.cache.set(SCAN_CACHE_KEY, raw, ttl=24 * 3600)
        except Exception as exc:
            logger.warning("Failed to cache universe metadata: %s", exc)
        return raw

    def _fetch_universe(self) -> List[Dict[str, Optional[str]]]:
        entries = []
        entries.extend(self._parse_table(self.SP500_URL, "Symbol", "Security", "GICS Sector", "GICS Sub-Industry", "Market Cap (USD)", "S&P 500"))
        entries.extend(self._parse_table(self.NASDAQ100_URL, "Ticker", "Company", "GICS Sector", "GICS Sub-Industry", "Market Cap", "NASDAQ 100"))
        # Deduplicate by symbol, keep latest entry
        dedup = {}
        for entry in entries:
            dedup[entry["symbol"]] = entry
        return list(dedup.values())

    def _parse_table(
        self,
        url: str,
        symbol_col: str,
        name_col: str,
        sector_col: str,
        industry_col: str,
        market_cap_col: Optional[str],
        source: str,
    ) -> List[Dict[str, Optional[str]]]:
        try:
            with httpx.Client(timeout=15.0) as client:
                response = client.get(url)
                response.raise_for_status()
                tables = pd.read_html(response.text)
        except Exception as exc:
            logger.warning("Failed to fetch universe table %s: %s", url, exc)
            return []

        if not tables:
            return []

        df = tables[0]
        results = []
        for _, row in df.iterrows():
            symbol = row.get(symbol_col)
            if not isinstance(symbol, str):
                continue
            name = row.get(name_col)
            sector = row.get(sector_col) if sector_col in df.columns else None
            industry = row.get(industry_col) if industry_col in df.columns else None
            market_cap = _parse_market_cap(row.get(market_cap_col)) if market_cap_col and market_cap_col in df.columns else None
            results.append({
                "symbol": symbol.upper().strip(),
                "name": str(name).strip() if isinstance(name, str) else None,
                "sector": str(sector).strip() if isinstance(sector, str) else None,
                "industry": str(industry).strip() if isinstance(industry, str) else None,
                "market_cap": market_cap,
                "source": source,
                "last_updated": datetime.utcnow(),
            })
        logger.info("Parsed %s entries from %s", len(results), source)
        return results

    def _persist_symbols(self, symbols: List[Dict[str, Optional[str]]]) -> None:
        if not symbols:
            return

        rows = []
        for entry in symbols:
            rows.append({
                "symbol": entry["symbol"],
                "name": entry.get("name"),
                "sector": entry.get("sector"),
                "industry": entry.get("industry"),
                "market_cap": entry.get("market_cap"),
                "last_updated": entry.get("last_updated") or datetime.utcnow(),
            })

        stmt = text(
            """
            INSERT INTO universe_symbols (symbol, name, sector, industry, market_cap, last_updated)
            VALUES (:symbol, :name, :sector, :industry, :market_cap, :last_updated)
            ON CONFLICT (symbol) DO UPDATE SET
                name = COALESCE(EXCLUDED.name, universe_symbols.name),
                sector = COALESCE(EXCLUDED.sector, universe_symbols.sector),
                industry = COALESCE(EXCLUDED.industry, universe_symbols.industry),
                market_cap = COALESCE(EXCLUDED.market_cap, universe_symbols.market_cap),
                last_updated = EXCLUDED.last_updated
            """
        )
        try:
            with self.db.engine.begin() as conn:
                conn.execute(stmt, rows)
            logger.info("Persisted %s universe symbols", len(rows))
        except Exception as exc:
            logger.error("Failed to persist universe symbols: %s", exc)
