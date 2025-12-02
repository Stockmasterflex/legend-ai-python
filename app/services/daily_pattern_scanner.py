"""
Daily Pattern Scanner Service
Scans universe for specific patterns at market close (6 PM EST)
Stores top 20 results per pattern in Redis (24hr TTL) + PostgreSQL (history)
"""
import asyncio
import logging
from datetime import datetime, timezone, date
from typing import List, Dict, Any, Optional
import httpx
from sqlalchemy import text

from app.services.market_data import market_data_service
from app.services.cache import get_cache_service
from app.services.database import get_database_service
from app.services.charting import get_charting_service
from app.services.universe_data import get_full_universe
from app.core.detector_registry import get_detector_by_name
from app.core.indicators import calculate_ema, calculate_rsi

logger = logging.getLogger(__name__)

# Pattern type constants
PATTERN_VCP = "VCP"
PATTERN_CUP_HANDLE = "Cup & Handle"
PATTERN_FLAT_BASE = "Flat Base"
PATTERN_TRIANGLE = "Triangle"
PATTERN_POWER_PLAY = "Power Play"

# Cache TTL (24 hours)
CACHE_TTL = 86400

# Minimum score threshold
MIN_SCORE = 7.0

# Top N results to store
TOP_N = 20


class DailyPatternScanner:
    """
    Daily batch scanner for specific chart patterns
    """

    def __init__(self):
        self.cache = get_cache_service()
        self.db = get_database_service()
        self.charting = get_charting_service()

    async def scan_pattern(
        self,
        pattern_type: str,
        tickers: Optional[List[str]] = None,
        min_score: float = MIN_SCORE,
        max_results: int = TOP_N
    ) -> Dict[str, Any]:
        """
        Scan universe for a specific pattern type

        Args:
            pattern_type: Pattern name (VCP, Cup & Handle, etc.)
            tickers: List of tickers to scan (defaults to full universe)
            min_score: Minimum score threshold (0-10)
            max_results: Maximum number of results to return

        Returns:
            Dict with scan results, stats, and metadata
        """
        if tickers is None:
            tickers = get_full_universe()

        scan_date = date.today()
        scan_start = datetime.now(timezone.utc)

        logger.info(f"🔍 Starting {pattern_type} scan for {len(tickers)} tickers (min_score={min_score})")

        results = []
        errors = []
        scanned = 0

        # Get pattern detector
        detector = get_detector_by_name(pattern_type)
        if not detector:
            logger.error(f"❌ No detector found for pattern: {pattern_type}")
            return {
                "success": False,
                "error": f"Unknown pattern type: {pattern_type}",
                "pattern_type": pattern_type,
                "scan_date": str(scan_date),
            }

        # Scan in batches to avoid overwhelming APIs
        batch_size = 10
        for i in range(0, len(tickers), batch_size):
            batch = tickers[i:i + batch_size]

            # Process batch concurrently
            batch_tasks = [
                self._scan_ticker(ticker, pattern_type, detector, min_score)
                for ticker in batch
            ]
            batch_results = await asyncio.gather(*batch_tasks, return_exceptions=True)

            for ticker, result in zip(batch, batch_results):
                scanned += 1
                if isinstance(result, Exception):
                    errors.append({"ticker": ticker, "error": str(result)})
                    logger.debug(f"❌ {ticker}: {result}")
                elif result:
                    results.append(result)
                    logger.info(f"✅ {ticker}: {result['pattern']} score={result['score']}")

            # Rate limiting
            if i + batch_size < len(tickers):
                await asyncio.sleep(0.5)

        # Sort by score descending and take top N
        results.sort(key=lambda x: x['score'], reverse=True)
        top_results = results[:max_results]

        scan_duration = (datetime.now(timezone.utc) - scan_start).total_seconds()

        logger.info(
            f"✅ {pattern_type} scan complete: {len(top_results)}/{len(results)} setups "
            f"(scanned {scanned} tickers in {scan_duration:.1f}s)"
        )

        # Store results in Redis + PostgreSQL
        await self._store_results(pattern_type, scan_date, top_results)

        return {
            "success": True,
            "pattern_type": pattern_type,
            "scan_date": str(scan_date),
            "scanned": scanned,
            "found": len(results),
            "top_results": top_results,
            "errors": errors,
            "duration_seconds": round(scan_duration, 2),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    async def _scan_ticker(
        self,
        ticker: str,
        pattern_type: str,
        detector,
        min_score: float
    ) -> Optional[Dict[str, Any]]:
        """Scan a single ticker for a pattern"""
        try:
            # Fetch price data (500 bars for comprehensive analysis)
            price_data = await market_data_service.get_time_series(
                ticker=ticker,
                interval="1day",
                outputsize=500
            )

            if not price_data or not price_data.get("c"):
                return None

            # Convert to DataFrame for detector
            import pandas as pd
            df = pd.DataFrame({
                'datetime': pd.to_datetime(price_data.get('t', []), unit='s'),
                'open': price_data.get('o', []),
                'high': price_data.get('h', []),
                'low': price_data.get('l', []),
                'close': price_data.get('c', []),
                'volume': price_data.get('v', []),
            })

            if len(df) < 100:
                return None

            # Run pattern detection
            pattern_results = detector.find(df, timeframe="1day", symbol=ticker)

            if not pattern_results or len(pattern_results) == 0:
                return None

            # Use best pattern result
            best_pattern = max(pattern_results, key=lambda p: p.confidence * 10)  # Convert confidence to 0-10 score

            # Calculate score (confidence * 10)
            score = round(best_pattern.confidence * 10, 1)

            if score < min_score:
                return None

            # Extract prices from pattern metadata
            entry_price = None
            stop_price = None
            target_price = None

            # Get current price and calculate trade levels
            current_price = float(df['close'].iloc[-1])

            # Pattern-specific level calculation
            if pattern_type == PATTERN_VCP:
                # VCP: Entry at base high, stop below last contraction low
                lines = best_pattern.lines or {}
                entry_price = lines.get('base_high', current_price * 1.02)
                stop_price = lines.get('last_contraction_low', current_price * 0.93)
                target_price = entry_price * 1.10  # 10% target
            elif pattern_type == PATTERN_CUP_HANDLE:
                # Cup & Handle: Entry at rim, stop below handle low
                lines = best_pattern.lines or {}
                entry_price = lines.get('rim', current_price * 1.02)
                stop_price = lines.get('handle_low', current_price * 0.92)
                target_price = entry_price * 1.15  # 15% target
            else:
                # Generic: 2% entry, 7% stop, 12% target
                entry_price = current_price * 1.02
                stop_price = current_price * 0.93
                target_price = current_price * 1.12

            # Calculate indicators
            closes = df['close'].values
            volumes = df['volume'].values

            ema50 = calculate_ema(closes, 50)
            ema200 = calculate_ema(closes, 200)
            rsi = calculate_rsi(closes, 14)

            avg_volume = volumes[-20:].mean()
            current_volume = volumes[-1]
            volume_ratio = current_volume / avg_volume if avg_volume > 0 else 1.0

            indicators = {
                "ema50": round(float(ema50[-1]), 2) if len(ema50) > 0 else None,
                "ema200": round(float(ema200[-1]), 2) if len(ema200) > 0 else None,
                "rsi": round(float(rsi[-1]), 2) if len(rsi) > 0 else None,
                "volume_vs_avg": round(volume_ratio, 2),
                "current_price": round(current_price, 2),
            }

            # Extract pattern reasons
            evidence = best_pattern.evidence or {}
            reasons = []

            if pattern_type == PATTERN_VCP:
                contraction_seq = evidence.get('contraction_sequence', [])
                if len(contraction_seq) >= 3:
                    reasons.append(f"✓ {len(contraction_seq)} contractions detected")
                if volume_ratio < 0.7:
                    reasons.append("✓ Volume drying up")
                if indicators.get('rsi') and 40 <= indicators['rsi'] <= 70:
                    reasons.append(f"✓ RSI healthy at {indicators['rsi']}")
            elif pattern_type == PATTERN_CUP_HANDLE:
                if best_pattern.strong:
                    reasons.append("✓ Strong cup formation")
                reasons.append(f"✓ Confidence {int(best_pattern.confidence * 100)}%")
            else:
                reasons.append(f"✓ Pattern detected with {int(best_pattern.confidence * 100)}% confidence")

            # Generate chart
            chart_url = None
            try:
                chart_url = await self.charting.generate_chart(
                    ticker=ticker,
                    timeframe="1day",
                    entry=entry_price,
                    stop=stop_price,
                    target=target_price,
                    support=stop_price,
                    resistance=None,
                    pattern_name=f"{pattern_type} Setup"
                )
            except Exception as e:
                logger.warning(f"⚠️ Chart generation failed for {ticker}: {e}")

            return {
                "ticker": ticker,
                "pattern": pattern_type,
                "score": score,
                "entry": round(entry_price, 2) if entry_price else None,
                "stop": round(stop_price, 2) if stop_price else None,
                "target": round(target_price, 2) if target_price else None,
                "chart_url": chart_url,
                "reasons": reasons,
                "indicators": indicators,
            }

        except Exception as e:
            logger.debug(f"Error scanning {ticker}: {e}")
            raise

    async def _store_results(
        self,
        pattern_type: str,
        scan_date: date,
        results: List[Dict[str, Any]]
    ):
        """Store scan results in Redis + PostgreSQL"""

        # 1. Store in Redis (24hr cache)
        cache_key = f"patterns:{pattern_type.lower().replace(' ', '_')}:{scan_date}"
        try:
            await self.cache.set(cache_key, results, ttl=CACHE_TTL)
            logger.info(f"📦 Cached {len(results)} {pattern_type} results in Redis (key={cache_key})")
        except Exception as e:
            logger.error(f"❌ Redis cache failed: {e}")

        # 2. Store in PostgreSQL (permanent history)
        try:
            self._persist_results_to_db(pattern_type, scan_date, results)
            logger.info(f"💾 Stored {len(results)} {pattern_type} results in PostgreSQL")
        except Exception as e:
            logger.error(f"❌ Database storage failed: {e}")

    def _persist_results_to_db(
        self,
        pattern_type: str,
        scan_date: date,
        results: List[Dict[str, Any]]
    ) -> None:
        """Persist scan results using SQLAlchemy sessions."""

        if not results:
            return

        insert_stmt = text(
            """
            INSERT INTO pattern_results (
                date, pattern_type, ticker, score, entry_price, stop_price, target_price,
                chart_url, reasons, indicators
            ) VALUES (
                :date, :pattern_type, :ticker, :score, :entry_price, :stop_price, :target_price,
                :chart_url, :reasons, :indicators
            )
            ON CONFLICT (date, pattern_type, ticker)
            DO UPDATE SET
                score = EXCLUDED.score,
                entry_price = EXCLUDED.entry_price,
                stop_price = EXCLUDED.stop_price,
                target_price = EXCLUDED.target_price,
                chart_url = EXCLUDED.chart_url,
                reasons = EXCLUDED.reasons,
                indicators = EXCLUDED.indicators,
                created_at = NOW()
            """
        )

        session = self.db.get_db()
        try:
            for result in results:
                session.execute(
                    insert_stmt,
                    {
                        "date": scan_date,
                        "pattern_type": pattern_type,
                        "ticker": result["ticker"],
                        "score": result["score"],
                        "entry_price": result.get("entry"),
                        "stop_price": result.get("stop"),
                        "target_price": result.get("target"),
                        "chart_url": result.get("chart_url"),
                        "reasons": result.get("reasons"),
                        "indicators": result.get("indicators"),
                    },
                )
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    async def get_cached_results(
        self,
        pattern_type: str,
        scan_date: Optional[date] = None
    ) -> Optional[List[Dict[str, Any]]]:
        """Retrieve cached scan results from Redis"""
        if scan_date is None:
            scan_date = date.today()

        cache_key = f"patterns:{pattern_type.lower().replace(' ', '_')}:{scan_date}"

        try:
            results = await self.cache.get(cache_key)
            if results:
                logger.info(f"✅ Cache hit for {pattern_type} on {scan_date}")
            return results
        except Exception as e:
            logger.error(f"❌ Cache retrieval failed: {e}")
            return None

    async def send_telegram_notification(
        self,
        pattern_type: str,
        scan_result: Dict[str, Any],
        telegram_bot_token: str,
        telegram_chat_id: str
    ):
        """Send Telegram notification about scan completion"""
        try:
            success = scan_result.get("success", False)
            found = scan_result.get("found", 0)
            scanned = scan_result.get("scanned", 0)
            duration = scan_result.get("duration_seconds", 0)
            top_results = scan_result.get("top_results", [])

            if success:
                emoji = "🎯" if found >= 5 else "📊"
                message = f"{emoji} *{pattern_type} Scan Complete*\n\n"
                message += f"✅ Scanned: {scanned} tickers\n"
                message += f"📈 Found: {found} setups (score ≥ {MIN_SCORE})\n"
                message += f"⏱ Duration: {duration}s\n\n"

                if top_results:
                    message += "*🏆 Top 5 Setups:*\n"
                    for i, setup in enumerate(top_results[:5], 1):
                        ticker = setup['ticker']
                        score = setup['score']
                        entry = setup.get('entry', 0)
                        message += f"{i}. {ticker}: {score}/10 @ ${entry:.2f}\n"
            else:
                message = f"❌ *{pattern_type} Scan Failed*\n\n"
                message += f"Error: {scan_result.get('error', 'Unknown error')}"

            # Send via Telegram Bot API
            url = f"https://api.telegram.org/bot{telegram_bot_token}/sendMessage"
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.post(url, json={
                    "chat_id": telegram_chat_id,
                    "text": message,
                    "parse_mode": "Markdown"
                })

                if response.status_code == 200:
                    logger.info(f"📤 Telegram notification sent for {pattern_type} scan")
                else:
                    logger.warning(f"⚠️ Telegram notification failed: {response.status_code}")

        except Exception as e:
            logger.error(f"❌ Telegram notification error: {e}")


# Singleton instance
_daily_scanner: Optional[DailyPatternScanner] = None

def get_daily_scanner() -> DailyPatternScanner:
    """Get singleton instance of daily pattern scanner"""
    global _daily_scanner
    if _daily_scanner is None:
        _daily_scanner = DailyPatternScanner()
    return _daily_scanner
