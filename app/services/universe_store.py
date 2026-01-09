import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional

from sqlalchemy import text

from app.config import get_settings
from app.services.cache import get_cache_service

logger = logging.getLogger(__name__)


class UniverseStore:
    """Loads the seeded S&P 500 + NASDAQ 100 universe and syncs it to Redis/Postgres."""

    DATA_PATH = Path("data/universe_seed.json")
    CACHE_KEY = "universe:metadata:v1"
    CACHE_TTL = 24 * 3600

    def __init__(self) -> None:
        self.settings = get_settings()
        self.cache = get_cache_service()
        self._memory: Dict[str, Dict[str, Any]] = {}
        self._seeded = False

    async def seed(self, force: bool = False) -> Dict[str, Dict[str, Any]]:
        """Load universe metadata from disk, push to Redis/Postgres."""
        if self._memory and not force:
            return self._memory

        if not force:
            cached = await self.cache.get(self.CACHE_KEY)
            if isinstance(cached, dict) and cached:
                self._memory = cached
                self._seeded = True
                return self._memory

        payload = self._load_from_disk()
        if not payload:
            logger.warning("universe seed file missing or empty")
            self._memory = {}
            return {}

        try:
            await self.cache.set(self.CACHE_KEY, payload, ttl=self.CACHE_TTL)
        except Exception as exc:
            logger.debug("universe cache seed failed: %s", exc)

        self._persist_to_database(payload)
        self._memory = payload
        self._seeded = True
        logger.info("Seeded universe metadata: %s symbols", len(payload))
        return payload

    async def get_metadata(self, symbol: str) -> Optional[Dict[str, Any]]:
        """Return universe metadata for a ticker, seeding cache if required."""
        if not symbol:
            return None
        uppercase = symbol.upper()
        if uppercase in self._memory:
            return self._memory[uppercase]
        dataset = await self.seed()
        return dataset.get(uppercase)

    async def get_all(self) -> Dict[str, Dict[str, Any]]:
        return await self.seed()

    def _load_from_disk(self) -> Dict[str, Dict[str, Any]]:
        if not self.DATA_PATH.exists():
            return {}
        try:
            entries = json.loads(self.DATA_PATH.read_text())
            return {item["symbol"]: item for item in entries if item.get("symbol")}
        except Exception as exc:
            logger.error("Failed to load universe seed: %s", exc)
            return {}

    def _persist_to_database(self, payload: Dict[str, Dict[str, Any]]) -> None:
        if not self.settings.database_url:
            return
        try:
            from app.services.database import get_database_service

            dbs = get_database_service()
            with dbs.engine.begin() as conn:
                rows = [
                    {
                        "symbol": meta["symbol"],
                        "name": meta.get("name"),
                        "sector": meta.get("sector"),
                        "industry": meta.get("industry"),
                    }
                    for meta in payload.values()
                ]
                stmt = text(
                    """
                    insert into tickers (symbol, name, sector, industry)
                    values (:symbol, :name, :sector, :industry)
                    on conflict(symbol) do update
                    set name=excluded.name,
                        sector=excluded.sector,
                        industry=excluded.industry
                    """
                )
                conn.execute(stmt, rows)

                # Also sync to universe_symbols (used by EODScanner)
                stmt_univ = text(
                    """
                    insert into universe_symbols (symbol, name, sector, industry)
                    values (:symbol, :name, :sector, :industry)
                    on conflict(symbol) do update
                    set name=excluded.name,
                        sector=excluded.sector,
                        industry=excluded.industry,
                        last_updated=now()
                    """
                )
                conn.execute(stmt_univ, rows)
        except Exception as exc:
            logger.warning("Universe DB seed skipped: %s", exc)


universe_store = UniverseStore()
