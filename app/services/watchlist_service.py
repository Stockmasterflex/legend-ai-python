"""
Professional Watchlist Service
Provides multi-watchlist management, smart organization, analytics, and import/export
"""

import logging
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime
from collections import defaultdict
import csv
import io
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_

from app.models import Watchlist, WatchlistGroup, Ticker, PatternScan
from app.services.database import DatabaseService
from app.services.market_data import MarketDataService

logger = logging.getLogger(__name__)


class WatchlistService:
    """Professional watchlist management with analytics and organization"""

    def __init__(self, db_service: DatabaseService, market_data_service: MarketDataService):
        self.db_service = db_service
        self.market_data_service = market_data_service

    # ==================== Watchlist Group Management ====================

    def create_group(self, user_id: str, name: str, description: str = None,
                     color: str = "#3B82F6", strategy: str = None) -> Dict[str, Any]:
        """Create a new watchlist group"""
        with self.db_service.get_db() as db:
            # Get max position
            max_pos = db.query(func.max(WatchlistGroup.position)).filter(
                WatchlistGroup.user_id == user_id
            ).scalar() or 0

            group = WatchlistGroup(
                user_id=user_id,
                name=name,
                description=description,
                color=color,
                strategy=strategy,
                position=max_pos + 1
            )
            db.add(group)
            db.commit()
            db.refresh(group)

            return self._group_to_dict(group)

    def get_groups(self, user_id: str) -> List[Dict[str, Any]]:
        """Get all watchlist groups for a user, ordered by position"""
        with self.db_service.get_db() as db:
            groups = db.query(WatchlistGroup).filter(
                WatchlistGroup.user_id == user_id
            ).order_by(WatchlistGroup.position).all()

            return [self._group_to_dict(g) for g in groups]

    def update_group(self, group_id: int, **kwargs) -> Dict[str, Any]:
        """Update watchlist group properties"""
        with self.db_service.get_db() as db:
            group = db.query(WatchlistGroup).filter(WatchlistGroup.id == group_id).first()
            if not group:
                raise ValueError(f"Group {group_id} not found")

            for key, value in kwargs.items():
                if hasattr(group, key):
                    setattr(group, key, value)

            db.commit()
            db.refresh(group)
            return self._group_to_dict(group)

    def delete_group(self, group_id: int, move_items_to: int = None) -> bool:
        """Delete a group, optionally moving items to another group"""
        with self.db_service.get_db() as db:
            group = db.query(WatchlistGroup).filter(WatchlistGroup.id == group_id).first()
            if not group:
                return False

            # Move or delete items
            items = db.query(Watchlist).filter(Watchlist.group_id == group_id).all()
            for item in items:
                if move_items_to:
                    item.group_id = move_items_to
                else:
                    db.delete(item)

            db.delete(group)
            db.commit()
            return True

    def reorder_groups(self, user_id: str, group_ids: List[int]) -> bool:
        """Reorder groups (drag-and-drop)"""
        with self.db_service.get_db() as db:
            for position, group_id in enumerate(group_ids):
                db.query(WatchlistGroup).filter(
                    and_(WatchlistGroup.id == group_id, WatchlistGroup.user_id == user_id)
                ).update({"position": position})
            db.commit()
            return True

    # ==================== Watchlist Item Management ====================

    def add_item(self, user_id: str, symbol: str, group_id: int = None, **kwargs) -> Dict[str, Any]:
        """Add ticker to watchlist with optional properties"""
        with self.db_service.get_db() as db:
            # Get or create ticker
            ticker = self.db_service.get_or_create_ticker(symbol)

            # Check if already exists
            existing = db.query(Watchlist).filter(
                and_(
                    Watchlist.user_id == user_id,
                    Watchlist.ticker_id == ticker.id,
                    Watchlist.group_id == group_id if group_id else True
                )
            ).first()

            if existing:
                # Update existing
                for key, value in kwargs.items():
                    if hasattr(existing, key):
                        setattr(existing, key, value)
                db.commit()
                db.refresh(existing)
                return self._item_to_dict(existing, ticker)

            # Get max position in group
            max_pos = db.query(func.max(Watchlist.position)).filter(
                and_(
                    Watchlist.user_id == user_id,
                    Watchlist.group_id == group_id if group_id else Watchlist.group_id.is_(None)
                )
            ).scalar() or 0

            # Create new item
            item = Watchlist(
                user_id=user_id,
                ticker_id=ticker.id,
                group_id=group_id,
                position=max_pos + 1,
                **kwargs
            )

            # Auto-categorize by sector if not provided
            if not kwargs.get('category') and ticker.sector:
                item.category = ticker.sector

            db.add(item)
            db.commit()
            db.refresh(item)

            return self._item_to_dict(item, ticker)

    def get_items(self, user_id: str, group_id: int = None, filters: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Get watchlist items with optional filtering"""
        with self.db_service.get_db() as db:
            query = db.query(Watchlist, Ticker).join(Ticker).filter(
                Watchlist.user_id == user_id
            )

            # Filter by group
            if group_id is not None:
                query = query.filter(Watchlist.group_id == group_id)

            # Apply filters
            if filters:
                if 'status' in filters:
                    query = query.filter(Watchlist.status == filters['status'])
                if 'pattern_type' in filters:
                    query = query.filter(Watchlist.pattern_type == filters['pattern_type'])
                if 'category' in filters:
                    query = query.filter(Watchlist.category == filters['category'])
                if 'min_strength' in filters:
                    query = query.filter(Watchlist.strength_score >= filters['min_strength'])

            # Order by position
            query = query.order_by(Watchlist.position)

            results = query.all()
            return [self._item_to_dict(item, ticker) for item, ticker in results]

    def update_item(self, item_id: int, **kwargs) -> Dict[str, Any]:
        """Update watchlist item properties"""
        with self.db_service.get_db() as db:
            item = db.query(Watchlist).filter(Watchlist.id == item_id).first()
            if not item:
                raise ValueError(f"Watchlist item {item_id} not found")

            for key, value in kwargs.items():
                if hasattr(item, key):
                    setattr(item, key, value)

            db.commit()
            db.refresh(item)

            ticker = db.query(Ticker).filter(Ticker.id == item.ticker_id).first()
            return self._item_to_dict(item, ticker)

    def delete_item(self, item_id: int) -> bool:
        """Remove item from watchlist"""
        with self.db_service.get_db() as db:
            item = db.query(Watchlist).filter(Watchlist.id == item_id).first()
            if not item:
                return False
            db.delete(item)
            db.commit()
            return True

    def reorder_items(self, user_id: str, group_id: int, item_ids: List[int]) -> bool:
        """Reorder items within a group (drag-and-drop)"""
        with self.db_service.get_db() as db:
            for position, item_id in enumerate(item_ids):
                db.query(Watchlist).filter(
                    and_(
                        Watchlist.id == item_id,
                        Watchlist.user_id == user_id,
                        Watchlist.group_id == group_id if group_id else Watchlist.group_id.is_(None)
                    )
                ).update({"position": position})
            db.commit()
            return True

    def color_code_item(self, item_id: int, color: str) -> Dict[str, Any]:
        """Set color for a specific ticker"""
        return self.update_item(item_id, color=color)

    # ==================== Smart Organization ====================

    def auto_categorize(self, user_id: str, group_id: int = None) -> int:
        """Auto-categorize items by sector"""
        count = 0
        with self.db_service.get_db() as db:
            query = db.query(Watchlist, Ticker).join(Ticker).filter(
                Watchlist.user_id == user_id
            )
            if group_id is not None:
                query = query.filter(Watchlist.group_id == group_id)

            items = query.all()
            for item, ticker in items:
                if ticker.sector and item.category != ticker.sector:
                    item.category = ticker.sector
                    count += 1

            db.commit()
        return count

    def group_by_pattern(self, user_id: str) -> Dict[str, List[Dict[str, Any]]]:
        """Group items by pattern type"""
        items = self.get_items(user_id)
        grouped = defaultdict(list)
        for item in items:
            pattern = item.get('pattern_type') or 'Unclassified'
            grouped[pattern].append(item)
        return dict(grouped)

    def sort_by_strength(self, user_id: str, group_id: int = None) -> List[Dict[str, Any]]:
        """Get items sorted by strength score"""
        with self.db_service.get_db() as db:
            query = db.query(Watchlist, Ticker).join(Ticker).filter(
                Watchlist.user_id == user_id
            )
            if group_id is not None:
                query = query.filter(Watchlist.group_id == group_id)

            query = query.order_by(Watchlist.strength_score.desc().nullslast())
            results = query.all()
            return [self._item_to_dict(item, ticker) for item, ticker in results]

    # ==================== Analytics ====================

    def get_analytics(self, user_id: str, group_id: int = None) -> Dict[str, Any]:
        """Get comprehensive watchlist analytics"""
        with self.db_service.get_db() as db:
            query = db.query(Watchlist, Ticker, PatternScan).join(Ticker).outerjoin(
                PatternScan,
                Ticker.id == PatternScan.ticker_id
            ).filter(Watchlist.user_id == user_id)

            if group_id is not None:
                query = query.filter(Watchlist.group_id == group_id)

            results = query.all()

            if not results:
                return self._empty_analytics()

            # Calculate metrics
            rs_ratings = [scan.rs_rating for _, _, scan in results if scan and scan.rs_rating]
            avg_rs = sum(rs_ratings) / len(rs_ratings) if rs_ratings else 0

            # Sector distribution
            sector_counts = defaultdict(int)
            for _, ticker, _ in results:
                sector = ticker.sector or "Unknown"
                sector_counts[sector] += 1

            # Pattern breakdown
            pattern_counts = defaultdict(int)
            for item, _, scan in results:
                pattern = item.pattern_type or (scan.pattern_type if scan else "Unclassified")
                pattern_counts[pattern] += 1

            # Status breakdown
            status_counts = defaultdict(int)
            for item, _, _ in results:
                status_counts[item.status] += 1

            # Performance tracking (for completed items)
            completed_items = [item for item, _, _ in results if item.profit_loss_pct is not None]
            avg_performance = sum(i.profit_loss_pct for i in completed_items) / len(completed_items) if completed_items else 0
            win_rate = len([i for i in completed_items if i.profit_loss_pct > 0]) / len(completed_items) * 100 if completed_items else 0

            # Strength distribution
            strength_scores = [item.strength_score for item, _, _ in results if item.strength_score]
            avg_strength = sum(strength_scores) / len(strength_scores) if strength_scores else 0

            return {
                "total_items": len(results),
                "average_rs_rating": round(avg_rs, 2),
                "average_strength": round(avg_strength, 2),
                "sector_distribution": dict(sector_counts),
                "pattern_breakdown": dict(pattern_counts),
                "status_breakdown": dict(status_counts),
                "performance": {
                    "completed_trades": len(completed_items),
                    "average_pnl_pct": round(avg_performance, 2),
                    "win_rate_pct": round(win_rate, 2)
                },
                "strongest_setups": [
                    {
                        "ticker": ticker.symbol,
                        "strength": item.strength_score,
                        "pattern": item.pattern_type
                    }
                    for item, ticker, _ in sorted(
                        [(i, t, s) for i, t, s in results if i.strength_score],
                        key=lambda x: x[0].strength_score or 0,
                        reverse=True
                    )[:5]
                ]
            }

    # ==================== Import/Export ====================

    def export_to_csv(self, user_id: str, group_id: int = None) -> str:
        """Export watchlist to CSV format"""
        items = self.get_items(user_id, group_id)

        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=[
            'ticker', 'name', 'status', 'pattern_type', 'category',
            'target_entry', 'target_stop', 'target_price',
            'strength_score', 'color', 'notes', 'tags'
        ])

        writer.writeheader()
        for item in items:
            writer.writerow({
                'ticker': item['ticker'],
                'name': item['name'],
                'status': item['status'],
                'pattern_type': item.get('pattern_type', ''),
                'category': item.get('category', ''),
                'target_entry': item.get('target_entry', ''),
                'target_stop': item.get('target_stop', ''),
                'target_price': item.get('target_price', ''),
                'strength_score': item.get('strength_score', ''),
                'color': item.get('color', ''),
                'notes': item.get('notes', ''),
                'tags': ','.join(item.get('tags', []) or [])
            })

        return output.getvalue()

    def import_from_csv(self, user_id: str, csv_content: str, group_id: int = None) -> Dict[str, Any]:
        """Import watchlist from CSV"""
        input_stream = io.StringIO(csv_content)
        reader = csv.DictReader(input_stream)

        added = 0
        errors = []

        for row in reader:
            try:
                ticker = row.get('ticker', '').strip().upper()
                if not ticker:
                    continue

                kwargs = {
                    'status': row.get('status', 'Watching'),
                    'pattern_type': row.get('pattern_type') or None,
                    'category': row.get('category') or None,
                    'notes': row.get('notes') or None,
                    'color': row.get('color') or None,
                }

                # Parse numeric fields
                for field in ['target_entry', 'target_stop', 'target_price', 'strength_score']:
                    value = row.get(field, '').strip()
                    if value:
                        try:
                            kwargs[field] = float(value)
                        except ValueError:
                            pass

                # Parse tags
                tags_str = row.get('tags', '').strip()
                if tags_str:
                    kwargs['tags'] = [t.strip() for t in tags_str.split(',') if t.strip()]

                self.add_item(user_id, ticker, group_id, **kwargs)
                added += 1
            except Exception as e:
                errors.append(f"Error importing {row.get('ticker', 'unknown')}: {str(e)}")

        return {
            "success": True,
            "added": added,
            "errors": errors
        }

    def import_symbols_list(self, user_id: str, symbols: List[str], group_id: int = None) -> Dict[str, Any]:
        """Import from simple list of symbols (copy/paste)"""
        added = 0
        errors = []

        for symbol in symbols:
            try:
                symbol = symbol.strip().upper()
                if symbol:
                    self.add_item(user_id, symbol, group_id)
                    added += 1
            except Exception as e:
                errors.append(f"Error adding {symbol}: {str(e)}")

        return {
            "success": True,
            "added": added,
            "errors": errors
        }

    def export_to_tradingview(self, user_id: str, group_id: int = None) -> str:
        """Export to TradingView format (comma-separated symbols)"""
        items = self.get_items(user_id, group_id)
        symbols = [item['ticker'] for item in items]
        return ','.join(symbols)

    def import_from_tradingview(self, user_id: str, symbols_string: str, group_id: int = None) -> Dict[str, Any]:
        """Import from TradingView format (comma or newline separated)"""
        # Handle both comma and newline separation
        symbols = []
        for sep in [',', '\n', ' ']:
            if sep in symbols_string:
                symbols = [s.strip() for s in symbols_string.split(sep)]
                break

        if not symbols:
            symbols = [symbols_string.strip()]

        return self.import_symbols_list(user_id, symbols, group_id)

    # ==================== Helper Methods ====================

    def _group_to_dict(self, group: WatchlistGroup) -> Dict[str, Any]:
        """Convert WatchlistGroup to dict"""
        return {
            "id": group.id,
            "name": group.name,
            "description": group.description,
            "color": group.color,
            "strategy": group.strategy,
            "position": group.position,
            "is_default": group.is_default,
            "created_at": group.created_at.isoformat() if group.created_at else None,
            "updated_at": group.updated_at.isoformat() if group.updated_at else None
        }

    def _item_to_dict(self, item: Watchlist, ticker: Ticker) -> Dict[str, Any]:
        """Convert Watchlist item to dict"""
        return {
            "id": item.id,
            "ticker": ticker.symbol,
            "name": ticker.name,
            "sector": ticker.sector,
            "industry": ticker.industry,
            "group_id": item.group_id,
            "status": item.status,
            "color": item.color,
            "category": item.category,
            "pattern_type": item.pattern_type,
            "position": item.position,
            "strength_score": item.strength_score,
            "target_entry": item.target_entry,
            "target_stop": item.target_stop,
            "target_price": item.target_price,
            "reason": item.reason,
            "notes": item.notes,
            "tags": item.tags,
            "alerts_enabled": item.alerts_enabled,
            "alert_threshold": item.alert_threshold,
            "entry_price": item.entry_price,
            "exit_price": item.exit_price,
            "profit_loss_pct": item.profit_loss_pct,
            "added_at": item.added_at.isoformat() if item.added_at else None,
            "triggered_at": item.triggered_at.isoformat() if item.triggered_at else None,
            "updated_at": item.updated_at.isoformat() if item.updated_at else None
        }

    def _empty_analytics(self) -> Dict[str, Any]:
        """Return empty analytics structure"""
        return {
            "total_items": 0,
            "average_rs_rating": 0,
            "average_strength": 0,
            "sector_distribution": {},
            "pattern_breakdown": {},
            "status_breakdown": {},
            "performance": {
                "completed_trades": 0,
                "average_pnl_pct": 0,
                "win_rate_pct": 0
            },
            "strongest_setups": []
        }


# Global instance
_watchlist_service: Optional[WatchlistService] = None


def get_watchlist_service() -> WatchlistService:
    """Get global watchlist service instance"""
    global _watchlist_service
    if _watchlist_service is None:
        from app.services.database import get_database_service
        from app.services.market_data import get_market_data_service

        db_service = get_database_service()
        market_service = get_market_data_service()
        _watchlist_service = WatchlistService(db_service, market_service)
    return _watchlist_service
