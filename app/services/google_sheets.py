"""
Google Sheets Integration Service
Bidirectional sync for watchlist, patterns, trades, portfolio, and dashboards
"""

import logging
import json
import asyncio
from typing import Optional, List, Dict, Any, Tuple
from datetime import datetime, timedelta
from pathlib import Path
import os

import gspread
from gspread_asyncio import AsyncioGspreadClientManager
from google.oauth2.service_account import Credentials

from app.config import get_settings
from app.services.database import get_db_service
from app.models import Watchlist, PatternScan, Trade, Portfolio, SheetSync, Ticker

logger = logging.getLogger(__name__)


class GoogleSheetsService:
    """Service for bidirectional Google Sheets synchronization"""

    # Google Sheets API scopes
    SCOPES = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive.file'
    ]

    def __init__(self):
        self.settings = get_settings()
        self.db_service = get_db_service()
        self.client_manager: Optional[AsyncioGspreadClientManager] = None
        self._initialized = False

    async def initialize(self) -> bool:
        """Initialize Google Sheets client"""
        if self._initialized:
            return True

        if not self.settings.google_sheets_enabled:
            logger.warning("Google Sheets integration is disabled in settings")
            return False

        try:
            # Get credentials from environment
            creds_json = self.settings.google_sheets_credentials_json
            if not creds_json:
                logger.error("Google Sheets credentials not configured")
                return False

            # Parse credentials
            if creds_json.startswith('{'):
                # JSON string
                creds_info = json.loads(creds_json)
            elif Path(creds_json).exists():
                # File path
                with open(creds_json, 'r') as f:
                    creds_info = json.load(f)
            else:
                logger.error("Invalid Google Sheets credentials format")
                return False

            # Create credentials
            creds = Credentials.from_service_account_info(creds_info, scopes=self.SCOPES)

            # Initialize async client manager
            def get_creds():
                return creds

            self.client_manager = AsyncioGspreadClientManager(get_creds)
            self._initialized = True

            logger.info("✅ Google Sheets service initialized successfully")
            return True

        except Exception as e:
            logger.error(f"❌ Failed to initialize Google Sheets service: {e}")
            return False

    async def _get_client(self):
        """Get authenticated gspread client"""
        if not self._initialized:
            await self.initialize()
        if not self.client_manager:
            raise RuntimeError("Google Sheets client not initialized")
        return await self.client_manager.authorize()

    # ==========================================
    # 1. WATCHLIST SYNC
    # ==========================================

    async def sync_watchlist_to_sheet(self, sheet_id: Optional[str] = None) -> Dict[str, Any]:
        """Export watchlist to Google Sheet"""
        try:
            sheet_id = sheet_id or self.settings.google_sheets_watchlist_id
            if not sheet_id:
                raise ValueError("Watchlist sheet ID not configured")

            # Get watchlist from database
            db = await self.db_service.get_session()
            watchlist_items = db.query(Watchlist).join(Ticker).all()

            # Prepare data for sheet
            headers = [
                "Ticker", "Status", "Target Entry", "Target Stop", "Target Price",
                "Reason", "Notes", "Alerts Enabled", "Alert Threshold %",
                "Added At", "Triggered At", "Last Updated"
            ]

            rows = []
            for item in watchlist_items:
                ticker = db.query(Ticker).filter(Ticker.id == item.ticker_id).first()
                rows.append([
                    ticker.symbol if ticker else "N/A",
                    item.status,
                    item.target_entry or "",
                    item.target_stop or "",
                    item.target_price or "",
                    item.reason or "",
                    item.notes or "",
                    "Yes" if item.alerts_enabled else "No",
                    item.alert_threshold or "",
                    item.added_at.strftime("%Y-%m-%d %H:%M") if item.added_at else "",
                    item.triggered_at.strftime("%Y-%m-%d %H:%M") if item.triggered_at else "",
                    item.updated_at.strftime("%Y-%m-%d %H:%M") if item.updated_at else ""
                ])

            # Update sheet
            client = await self._get_client()
            sheet = await client.open_by_key(sheet_id)
            worksheet = await sheet.get_worksheet(0)  # First worksheet

            # Clear and update
            await worksheet.clear()
            await worksheet.update([headers] + rows, 'A1')

            # Format header row
            await worksheet.format('A1:L1', {
                "backgroundColor": {"red": 0.2, "green": 0.2, "blue": 0.8},
                "textFormat": {"bold": True, "foregroundColor": {"red": 1, "green": 1, "blue": 1}}
            })

            # Track sync
            await self._log_sync("watchlist", sheet_id, "to_sheet", len(rows), "success")

            logger.info(f"✅ Synced {len(rows)} watchlist items to sheet")
            return {"status": "success", "records": len(rows), "sheet_id": sheet_id}

        except Exception as e:
            logger.error(f"❌ Failed to sync watchlist to sheet: {e}")
            await self._log_sync("watchlist", sheet_id or "", "to_sheet", 0, "error", str(e))
            return {"status": "error", "error": str(e)}

    async def sync_watchlist_from_sheet(self, sheet_id: Optional[str] = None) -> Dict[str, Any]:
        """Import watchlist from Google Sheet (bidirectional sync)"""
        try:
            sheet_id = sheet_id or self.settings.google_sheets_watchlist_id
            if not sheet_id:
                raise ValueError("Watchlist sheet ID not configured")

            # Read from sheet
            client = await self._get_client()
            sheet = await client.open_by_key(sheet_id)
            worksheet = await sheet.get_worksheet(0)
            data = await worksheet.get_all_records()

            # Update database
            db = await self.db_service.get_session()
            updated = 0

            for row in data:
                ticker_symbol = row.get("Ticker", "").strip().upper()
                if not ticker_symbol:
                    continue

                # Get or create ticker
                ticker = db.query(Ticker).filter(Ticker.symbol == ticker_symbol).first()
                if not ticker:
                    ticker = Ticker(symbol=ticker_symbol)
                    db.add(ticker)
                    db.flush()

                # Update or create watchlist entry
                watchlist_item = db.query(Watchlist).filter(
                    Watchlist.ticker_id == ticker.id
                ).first()

                if not watchlist_item:
                    watchlist_item = Watchlist(ticker_id=ticker.id)
                    db.add(watchlist_item)

                # Update fields
                watchlist_item.status = row.get("Status", "Watching")
                watchlist_item.target_entry = self._parse_float(row.get("Target Entry"))
                watchlist_item.target_stop = self._parse_float(row.get("Target Stop"))
                watchlist_item.target_price = self._parse_float(row.get("Target Price"))
                watchlist_item.reason = row.get("Reason", "")
                watchlist_item.notes = row.get("Notes", "")
                watchlist_item.alerts_enabled = row.get("Alerts Enabled", "Yes").lower() == "yes"
                watchlist_item.alert_threshold = self._parse_float(row.get("Alert Threshold %"))

                updated += 1

            db.commit()
            await self._log_sync("watchlist", sheet_id, "from_sheet", updated, "success")

            logger.info(f"✅ Imported {updated} watchlist items from sheet")
            return {"status": "success", "records": updated, "sheet_id": sheet_id}

        except Exception as e:
            logger.error(f"❌ Failed to sync watchlist from sheet: {e}")
            await self._log_sync("watchlist", sheet_id or "", "from_sheet", 0, "error", str(e))
            return {"status": "error", "error": str(e)}

    # ==========================================
    # 2. PATTERN RESULTS EXPORT
    # ==========================================

    async def export_pattern_results(self, sheet_id: Optional[str] = None, days: int = 7) -> Dict[str, Any]:
        """Export recent pattern scan results to Google Sheet"""
        try:
            sheet_id = sheet_id or self.settings.google_sheets_patterns_id
            if not sheet_id:
                raise ValueError("Patterns sheet ID not configured")

            # Get recent pattern scans
            db = await self.db_service.get_session()
            cutoff_date = datetime.now() - timedelta(days=days)

            scans = db.query(PatternScan).join(Ticker).filter(
                PatternScan.scanned_at >= cutoff_date
            ).order_by(PatternScan.scanned_at.desc()).all()

            # Prepare data
            headers = [
                "Date", "Ticker", "Pattern Type", "Score", "Current Price",
                "Entry Price", "Stop Price", "Target Price", "Risk/Reward",
                "Volume Dry Up", "Consolidation Days", "RS Rating",
                "Analysis", "Chart URL"
            ]

            rows = []
            for scan in scans:
                ticker = db.query(Ticker).filter(Ticker.id == scan.ticker_id).first()
                rows.append([
                    scan.scanned_at.strftime("%Y-%m-%d %H:%M") if scan.scanned_at else "",
                    ticker.symbol if ticker else "N/A",
                    scan.pattern_type,
                    round(scan.score, 2),
                    scan.current_price or "",
                    scan.entry_price or "",
                    scan.stop_price or "",
                    scan.target_price or "",
                    round(scan.risk_reward_ratio, 2) if scan.risk_reward_ratio else "",
                    "Yes" if scan.volume_dry_up else "No",
                    scan.consolidation_days or "",
                    round(scan.rs_rating, 2) if scan.rs_rating else "",
                    scan.analysis or "",
                    scan.chart_url or ""
                ])

            # Update sheet
            client = await self._get_client()
            sheet = await client.open_by_key(sheet_id)
            worksheet = await sheet.get_worksheet(0)

            await worksheet.clear()
            await worksheet.update([headers] + rows, 'A1')

            # Format header
            await worksheet.format('A1:N1', {
                "backgroundColor": {"red": 0.0, "green": 0.5, "blue": 0.0},
                "textFormat": {"bold": True, "foregroundColor": {"red": 1, "green": 1, "blue": 1}}
            })

            # Add conditional formatting for scores
            await self._apply_score_formatting(worksheet, len(rows))

            await self._log_sync("patterns", sheet_id, "to_sheet", len(rows), "success")

            logger.info(f"✅ Exported {len(rows)} pattern results to sheet")
            return {"status": "success", "records": len(rows), "sheet_id": sheet_id}

        except Exception as e:
            logger.error(f"❌ Failed to export pattern results: {e}")
            await self._log_sync("patterns", sheet_id or "", "to_sheet", 0, "error", str(e))
            return {"status": "error", "error": str(e)}

    async def _apply_score_formatting(self, worksheet, num_rows: int):
        """Apply conditional formatting for pattern scores"""
        try:
            # High scores (8-10) - Green
            await worksheet.format(f'D2:D{num_rows + 1}', {
                "backgroundColorStyle": {
                    "rgbColor": {"red": 0.7, "green": 1.0, "blue": 0.7}
                }
            }, fields="userEnteredFormat.backgroundColorStyle")

        except Exception as e:
            logger.warning(f"Could not apply conditional formatting: {e}")

    # ==========================================
    # 3. TRADE JOURNAL INTEGRATION
    # ==========================================

    async def sync_trades_to_sheet(self, sheet_id: Optional[str] = None) -> Dict[str, Any]:
        """Export trade journal to Google Sheet with P&L calculations"""
        try:
            sheet_id = sheet_id or self.settings.google_sheets_trades_id
            if not sheet_id:
                raise ValueError("Trades sheet ID not configured")

            # Get trades from database
            db = await self.db_service.get_session()
            trades = db.query(Trade).join(Ticker).order_by(Trade.entry_date.desc()).all()

            # Prepare headers
            headers = [
                "Trade ID", "Ticker", "Entry Date", "Entry Price", "Stop Loss",
                "Target Price", "Position Size", "Risk Amount", "Status",
                "Exit Date", "Exit Price", "P&L $", "P&L %", "R-Multiple",
                "Win/Loss", "Notes"
            ]

            # Calculate statistics
            total_trades = len(trades)
            closed_trades = [t for t in trades if t.status == "closed"]
            winning_trades = [t for t in closed_trades if t.win]
            losing_trades = [t for t in closed_trades if not t.win]

            win_rate = (len(winning_trades) / len(closed_trades) * 100) if closed_trades else 0
            total_pnl = sum(t.profit_loss or 0 for t in closed_trades)
            avg_r_multiple = sum(t.r_multiple or 0 for t in closed_trades) / len(closed_trades) if closed_trades else 0

            # Prepare rows
            rows = []
            for trade in trades:
                ticker = db.query(Ticker).filter(Ticker.id == trade.ticker_id).first()
                rows.append([
                    trade.trade_id,
                    ticker.symbol if ticker else "N/A",
                    trade.entry_date.strftime("%Y-%m-%d") if trade.entry_date else "",
                    trade.entry_price,
                    trade.stop_loss,
                    trade.target_price,
                    trade.position_size,
                    round(trade.risk_amount, 2),
                    trade.status.upper(),
                    trade.exit_date.strftime("%Y-%m-%d") if trade.exit_date else "",
                    trade.exit_price or "",
                    round(trade.profit_loss, 2) if trade.profit_loss else "",
                    f"{round(trade.profit_loss_pct, 2)}%" if trade.profit_loss_pct else "",
                    round(trade.r_multiple, 2) if trade.r_multiple else "",
                    "WIN" if trade.win else ("LOSS" if trade.win is False else ""),
                    trade.notes or ""
                ])

            # Add summary section
            summary_rows = [
                [],
                ["TRADE STATISTICS"],
                ["Total Trades", total_trades],
                ["Closed Trades", len(closed_trades)],
                ["Winning Trades", len(winning_trades)],
                ["Losing Trades", len(losing_trades)],
                ["Win Rate", f"{round(win_rate, 2)}%"],
                ["Total P&L", f"${round(total_pnl, 2)}"],
                ["Avg R-Multiple", round(avg_r_multiple, 2)]
            ]

            # Update sheet
            client = await self._get_client()
            sheet = await client.open_by_key(sheet_id)
            worksheet = await sheet.get_worksheet(0)

            await worksheet.clear()
            await worksheet.update([headers] + rows + summary_rows, 'A1')

            # Format header
            await worksheet.format('A1:P1', {
                "backgroundColor": {"red": 0.2, "green": 0.6, "blue": 0.8},
                "textFormat": {"bold": True, "foregroundColor": {"red": 1, "green": 1, "blue": 1}}
            })

            # Format statistics section
            stats_start_row = len(rows) + 3
            await worksheet.format(f'A{stats_start_row}:B{stats_start_row}', {
                "backgroundColor": {"red": 1.0, "green": 0.8, "blue": 0.0},
                "textFormat": {"bold": True}
            })

            await self._log_sync("trades", sheet_id, "to_sheet", len(rows), "success")

            logger.info(f"✅ Synced {len(rows)} trades to sheet")
            return {
                "status": "success",
                "records": len(rows),
                "sheet_id": sheet_id,
                "statistics": {
                    "total_trades": total_trades,
                    "win_rate": round(win_rate, 2),
                    "total_pnl": round(total_pnl, 2),
                    "avg_r_multiple": round(avg_r_multiple, 2)
                }
            }

        except Exception as e:
            logger.error(f"❌ Failed to sync trades to sheet: {e}")
            await self._log_sync("trades", sheet_id or "", "to_sheet", 0, "error", str(e))
            return {"status": "error", "error": str(e)}

    # ==========================================
    # 4. PORTFOLIO TRACKING
    # ==========================================

    async def sync_portfolio_to_sheet(self, sheet_id: Optional[str] = None) -> Dict[str, Any]:
        """Export portfolio holdings to Google Sheet with risk metrics"""
        try:
            sheet_id = sheet_id or self.settings.google_sheets_portfolio_id
            if not sheet_id:
                raise ValueError("Portfolio sheet ID not configured")

            # Get portfolio from database
            db = await self.db_service.get_session()
            holdings = db.query(Portfolio).join(Ticker).all()

            # Prepare headers
            headers = [
                "Ticker", "Shares", "Avg Cost", "Current Price", "Market Value",
                "Cost Basis", "Unrealized P&L $", "Unrealized P&L %",
                "Position Size %", "Risk Amount", "Stop Loss", "Target Price",
                "Acquired Date", "Notes"
            ]

            # Calculate portfolio totals
            total_market_value = sum(h.market_value or 0 for h in holdings)
            total_cost_basis = sum(h.cost_basis for h in holdings)
            total_unrealized_pnl = total_market_value - total_cost_basis

            # Prepare rows
            rows = []
            for holding in holdings:
                ticker = db.query(Ticker).filter(Ticker.id == holding.ticker_id).first()
                rows.append([
                    ticker.symbol if ticker else "N/A",
                    holding.shares,
                    round(holding.avg_cost, 2),
                    round(holding.current_price, 2) if holding.current_price else "",
                    round(holding.market_value, 2) if holding.market_value else "",
                    round(holding.cost_basis, 2),
                    round(holding.unrealized_pnl, 2) if holding.unrealized_pnl else "",
                    f"{round(holding.unrealized_pnl_pct, 2)}%" if holding.unrealized_pnl_pct else "",
                    f"{round(holding.position_size_pct, 2)}%" if holding.position_size_pct else "",
                    round(holding.risk_amount, 2) if holding.risk_amount else "",
                    round(holding.stop_loss, 2) if holding.stop_loss else "",
                    round(holding.target_price, 2) if holding.target_price else "",
                    holding.acquired_date.strftime("%Y-%m-%d") if holding.acquired_date else "",
                    holding.notes or ""
                ])

            # Add summary
            summary_rows = [
                [],
                ["PORTFOLIO SUMMARY"],
                ["Total Positions", len(holdings)],
                ["Total Market Value", f"${round(total_market_value, 2)}"],
                ["Total Cost Basis", f"${round(total_cost_basis, 2)}"],
                ["Total Unrealized P&L", f"${round(total_unrealized_pnl, 2)}"],
                ["Portfolio Return %", f"{round((total_unrealized_pnl / total_cost_basis * 100), 2)}%" if total_cost_basis > 0 else "0%"]
            ]

            # Update sheet
            client = await self._get_client()
            sheet = await client.open_by_key(sheet_id)
            worksheet = await sheet.get_worksheet(0)

            await worksheet.clear()
            await worksheet.update([headers] + rows + summary_rows, 'A1')

            # Format header
            await worksheet.format('A1:N1', {
                "backgroundColor": {"red": 0.6, "green": 0.2, "blue": 0.8},
                "textFormat": {"bold": True, "foregroundColor": {"red": 1, "green": 1, "blue": 1}}
            })

            await self._log_sync("portfolio", sheet_id, "to_sheet", len(rows), "success")

            logger.info(f"✅ Synced {len(rows)} portfolio holdings to sheet")
            return {
                "status": "success",
                "records": len(rows),
                "sheet_id": sheet_id,
                "summary": {
                    "total_positions": len(holdings),
                    "total_value": round(total_market_value, 2),
                    "total_pnl": round(total_unrealized_pnl, 2)
                }
            }

        except Exception as e:
            logger.error(f"❌ Failed to sync portfolio to sheet: {e}")
            await self._log_sync("portfolio", sheet_id or "", "to_sheet", 0, "error", str(e))
            return {"status": "error", "error": str(e)}

    async def import_portfolio_from_sheet(self, sheet_id: Optional[str] = None) -> Dict[str, Any]:
        """Import portfolio holdings from Google Sheet"""
        try:
            sheet_id = sheet_id or self.settings.google_sheets_portfolio_id
            if not sheet_id:
                raise ValueError("Portfolio sheet ID not configured")

            # Read from sheet
            client = await self._get_client()
            sheet = await client.open_by_key(sheet_id)
            worksheet = await sheet.get_worksheet(0)
            data = await worksheet.get_all_records()

            # Update database
            db = await self.db_service.get_session()
            updated = 0

            for row in data:
                ticker_symbol = row.get("Ticker", "").strip().upper()
                if not ticker_symbol or ticker_symbol == "PORTFOLIO SUMMARY":
                    continue

                # Get or create ticker
                ticker = db.query(Ticker).filter(Ticker.symbol == ticker_symbol).first()
                if not ticker:
                    ticker = Ticker(symbol=ticker_symbol)
                    db.add(ticker)
                    db.flush()

                # Update or create portfolio entry
                holding = db.query(Portfolio).filter(
                    Portfolio.ticker_id == ticker.id
                ).first()

                if not holding:
                    holding = Portfolio(ticker_id=ticker.id)
                    db.add(holding)

                # Update fields
                holding.shares = int(row.get("Shares", 0))
                holding.avg_cost = self._parse_float(row.get("Avg Cost")) or 0
                holding.cost_basis = holding.shares * holding.avg_cost
                holding.stop_loss = self._parse_float(row.get("Stop Loss"))
                holding.target_price = self._parse_float(row.get("Target Price"))
                holding.notes = row.get("Notes", "")

                updated += 1

            db.commit()
            await self._log_sync("portfolio", sheet_id, "from_sheet", updated, "success")

            logger.info(f"✅ Imported {updated} portfolio holdings from sheet")
            return {"status": "success", "records": updated, "sheet_id": sheet_id}

        except Exception as e:
            logger.error(f"❌ Failed to import portfolio from sheet: {e}")
            await self._log_sync("portfolio", sheet_id or "", "from_sheet", 0, "error", str(e))
            return {"status": "error", "error": str(e)}

    # ==========================================
    # 5. CUSTOM DASHBOARDS
    # ==========================================

    async def create_dashboard(self, sheet_id: Optional[str] = None) -> Dict[str, Any]:
        """Create custom dashboard with formulas and real-time data"""
        try:
            sheet_id = sheet_id or self.settings.google_sheets_dashboard_id
            if not sheet_id:
                raise ValueError("Dashboard sheet ID not configured")

            client = await self._get_client()
            sheet = await client.open_by_key(sheet_id)

            # Create multiple worksheets for different sections
            worksheets = {
                "Overview": 0,
                "Top Patterns": 1,
                "Active Trades": 2,
                "Performance": 3
            }

            # Ensure worksheets exist
            existing_sheets = await sheet.worksheets()
            existing_titles = [ws.title for ws in existing_sheets]

            for title, index in worksheets.items():
                if title not in existing_titles:
                    await sheet.add_worksheet(title=title, rows=100, cols=20)

            # 1. Overview Dashboard
            overview = await sheet.worksheet("Overview")
            overview_data = await self._build_overview_data()
            await overview.clear()
            await overview.update(overview_data, 'A1')
            await self._format_overview(overview)

            # 2. Top Patterns
            top_patterns = await sheet.worksheet("Top Patterns")
            patterns_data = await self._build_top_patterns_data()
            await top_patterns.clear()
            await top_patterns.update(patterns_data, 'A1')

            # 3. Active Trades
            active_trades = await sheet.worksheet("Active Trades")
            trades_data = await self._build_active_trades_data()
            await active_trades.clear()
            await active_trades.update(trades_data, 'A1')

            # 4. Performance Metrics
            performance = await sheet.worksheet("Performance")
            perf_data = await self._build_performance_data()
            await performance.clear()
            await performance.update(perf_data, 'A1')

            await self._log_sync("dashboard", sheet_id, "to_sheet", 4, "success")

            logger.info("✅ Created custom dashboard with 4 worksheets")
            return {"status": "success", "worksheets": 4, "sheet_id": sheet_id}

        except Exception as e:
            logger.error(f"❌ Failed to create dashboard: {e}")
            await self._log_sync("dashboard", sheet_id or "", "to_sheet", 0, "error", str(e))
            return {"status": "error", "error": str(e)}

    async def _build_overview_data(self) -> List[List[Any]]:
        """Build overview dashboard data"""
        db = await self.db_service.get_session()

        # Get counts
        watchlist_count = db.query(Watchlist).count()
        patterns_count = db.query(PatternScan).filter(
            PatternScan.scanned_at >= datetime.now() - timedelta(days=1)
        ).count()
        active_trades = db.query(Trade).filter(Trade.status == "open").count()

        return [
            ["LEGEND AI TRADING DASHBOARD"],
            ["Last Updated:", datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
            [],
            ["QUICK STATS"],
            ["Watchlist Items", watchlist_count],
            ["Patterns (24h)", patterns_count],
            ["Active Trades", active_trades],
            [],
            ["MARKET STATUS"],
            ["Status", "OPEN" if self._is_market_open() else "CLOSED"],
        ]

    async def _build_top_patterns_data(self) -> List[List[Any]]:
        """Build top patterns data"""
        db = await self.db_service.get_session()

        patterns = db.query(PatternScan).join(Ticker).filter(
            PatternScan.scanned_at >= datetime.now() - timedelta(days=7)
        ).order_by(PatternScan.score.desc()).limit(20).all()

        headers = ["Ticker", "Pattern", "Score", "Entry", "Target", "R/R", "Date"]
        rows = [headers]

        for p in patterns:
            ticker = db.query(Ticker).filter(Ticker.id == p.ticker_id).first()
            rows.append([
                ticker.symbol if ticker else "N/A",
                p.pattern_type,
                round(p.score, 2),
                p.entry_price or "",
                p.target_price or "",
                round(p.risk_reward_ratio, 2) if p.risk_reward_ratio else "",
                p.scanned_at.strftime("%Y-%m-%d") if p.scanned_at else ""
            ])

        return rows

    async def _build_active_trades_data(self) -> List[List[Any]]:
        """Build active trades data"""
        db = await self.db_service.get_session()

        trades = db.query(Trade).join(Ticker).filter(
            Trade.status == "open"
        ).all()

        headers = ["Ticker", "Entry", "Stop", "Target", "Size", "Risk $", "Days Open"]
        rows = [headers]

        for t in trades:
            ticker = db.query(Ticker).filter(Ticker.id == t.ticker_id).first()
            days_open = (datetime.now() - t.entry_date).days if t.entry_date else 0
            rows.append([
                ticker.symbol if ticker else "N/A",
                t.entry_price,
                t.stop_loss,
                t.target_price,
                t.position_size,
                round(t.risk_amount, 2),
                days_open
            ])

        return rows

    async def _build_performance_data(self) -> List[List[Any]]:
        """Build performance metrics data"""
        db = await self.db_service.get_session()

        closed_trades = db.query(Trade).filter(Trade.status == "closed").all()

        if not closed_trades:
            return [["No closed trades yet"]]

        winning = [t for t in closed_trades if t.win]
        losing = [t for t in closed_trades if not t.win]

        win_rate = len(winning) / len(closed_trades) * 100
        total_pnl = sum(t.profit_loss or 0 for t in closed_trades)
        avg_win = sum(t.profit_loss or 0 for t in winning) / len(winning) if winning else 0
        avg_loss = sum(t.profit_loss or 0 for t in losing) / len(losing) if losing else 0
        profit_factor = abs(sum(t.profit_loss or 0 for t in winning) / sum(t.profit_loss or 0 for t in losing)) if losing and sum(t.profit_loss or 0 for t in losing) != 0 else 0

        return [
            ["PERFORMANCE METRICS"],
            [],
            ["Total Trades", len(closed_trades)],
            ["Winning Trades", len(winning)],
            ["Losing Trades", len(losing)],
            ["Win Rate", f"{round(win_rate, 2)}%"],
            [],
            ["Total P&L", f"${round(total_pnl, 2)}"],
            ["Avg Win", f"${round(avg_win, 2)}"],
            ["Avg Loss", f"${round(avg_loss, 2)}"],
            ["Profit Factor", round(profit_factor, 2)],
        ]

    async def _format_overview(self, worksheet):
        """Format overview worksheet"""
        try:
            # Title
            await worksheet.format('A1', {
                "backgroundColor": {"red": 0.0, "green": 0.0, "blue": 0.0},
                "textFormat": {
                    "bold": True,
                    "fontSize": 18,
                    "foregroundColor": {"red": 1, "green": 1, "blue": 1}
                }
            })

            # Section headers
            await worksheet.format('A4', {
                "backgroundColor": {"red": 0.2, "green": 0.6, "blue": 0.9},
                "textFormat": {"bold": True, "foregroundColor": {"red": 1, "green": 1, "blue": 1}}
            })

        except Exception as e:
            logger.warning(f"Could not apply dashboard formatting: {e}")

    # ==========================================
    # HELPER METHODS
    # ==========================================

    def _parse_float(self, value: Any) -> Optional[float]:
        """Safely parse float value"""
        try:
            if value is None or value == "":
                return None
            # Remove % sign if present
            if isinstance(value, str):
                value = value.replace('%', '').replace('$', '').strip()
            return float(value)
        except (ValueError, TypeError):
            return None

    def _is_market_open(self) -> bool:
        """Check if market is currently open (simplified)"""
        now = datetime.now()
        # Market open 9:30 AM - 4:00 PM ET, Monday-Friday
        if now.weekday() >= 5:  # Weekend
            return False
        hour = now.hour
        return 9 <= hour < 16

    async def _log_sync(
        self,
        sheet_type: str,
        sheet_id: str,
        direction: str,
        records: int,
        status: str,
        error: Optional[str] = None
    ):
        """Log sync operation to database"""
        try:
            db = await self.db_service.get_session()

            sync_log = db.query(SheetSync).filter(
                SheetSync.sheet_type == sheet_type,
                SheetSync.sheet_id == sheet_id
            ).first()

            if not sync_log:
                sync_log = SheetSync(
                    sheet_type=sheet_type,
                    sheet_id=sheet_id
                )
                db.add(sync_log)

            sync_log.last_sync_at = datetime.now()
            sync_log.last_sync_direction = direction
            sync_log.records_synced = records
            sync_log.sync_status = status
            sync_log.error_message = error

            db.commit()

        except Exception as e:
            logger.error(f"Failed to log sync: {e}")

    async def get_sync_status(self) -> List[Dict[str, Any]]:
        """Get status of all sheet syncs"""
        try:
            db = await self.db_service.get_session()
            syncs = db.query(SheetSync).all()

            return [
                {
                    "sheet_type": s.sheet_type,
                    "sheet_id": s.sheet_id,
                    "last_sync": s.last_sync_at.isoformat() if s.last_sync_at else None,
                    "direction": s.last_sync_direction,
                    "records": s.records_synced,
                    "status": s.sync_status,
                    "error": s.error_message
                }
                for s in syncs
            ]

        except Exception as e:
            logger.error(f"Failed to get sync status: {e}")
            return []


# Singleton instance
_sheets_service: Optional[GoogleSheetsService] = None


def get_sheets_service() -> GoogleSheetsService:
    """Get or create singleton sheets service"""
    global _sheets_service
    if _sheets_service is None:
        _sheets_service = GoogleSheetsService()
    return _sheets_service
