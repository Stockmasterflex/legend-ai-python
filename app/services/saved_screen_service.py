"""
Saved Screen Management Service

Handles database operations for saved screens, scheduled scans, and screen results.
"""
import json
import logging
from datetime import datetime, timezone, timedelta
from typing import List, Dict, Any, Optional
from sqlalchemy import select, delete, update
from sqlalchemy.orm import Session

from app.models import SavedScreen, ScreenResult, ScheduledScan, Ticker
from app.services.database import DatabaseService
from app.services.advanced_screener import FilterCriteria, advanced_screener_service
from app.services.screen_templates import screen_templates
from app.config import get_settings

logger = logging.getLogger(__name__)


class SavedScreenService:
    """Service for managing saved screens and scheduled scans"""

    def __init__(self, db_service: DatabaseService):
        self.db_service = db_service

    def create_screen(
        self,
        name: str,
        filter_criteria: FilterCriteria,
        user_id: str = "default",
        description: Optional[str] = None,
        is_template: bool = False,
        template_type: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Create a new saved screen"""
        session = self.db_service.get_session()
        try:
            screen = SavedScreen(
                user_id=user_id,
                name=name,
                description=description,
                filter_criteria=json.dumps(filter_criteria.to_dict()),
                is_template=is_template,
                template_type=template_type,
            )
            session.add(screen)
            session.commit()
            session.refresh(screen)

            return self._screen_to_dict(screen)
        except Exception as e:
            session.rollback()
            logger.error(f"Failed to create screen: {e}")
            raise
        finally:
            session.close()

    def get_screen(self, screen_id: int) -> Optional[Dict[str, Any]]:
        """Get a saved screen by ID"""
        session = self.db_service.get_session()
        try:
            screen = session.query(SavedScreen).filter(SavedScreen.id == screen_id).first()
            if not screen:
                return None
            return self._screen_to_dict(screen)
        finally:
            session.close()

    def list_screens(
        self,
        user_id: str = "default",
        include_templates: bool = True
    ) -> List[Dict[str, Any]]:
        """List all saved screens for a user"""
        session = self.db_service.get_session()
        try:
            query = session.query(SavedScreen).filter(SavedScreen.user_id == user_id)

            if not include_templates:
                query = query.filter(SavedScreen.is_template == False)

            screens = query.order_by(SavedScreen.created_at.desc()).all()
            return [self._screen_to_dict(screen) for screen in screens]
        finally:
            session.close()

    def update_screen(
        self,
        screen_id: int,
        name: Optional[str] = None,
        description: Optional[str] = None,
        filter_criteria: Optional[FilterCriteria] = None,
    ) -> Optional[Dict[str, Any]]:
        """Update a saved screen"""
        session = self.db_service.get_session()
        try:
            screen = session.query(SavedScreen).filter(SavedScreen.id == screen_id).first()
            if not screen:
                return None

            if name:
                screen.name = name
            if description is not None:
                screen.description = description
            if filter_criteria:
                screen.filter_criteria = json.dumps(filter_criteria.to_dict())

            screen.updated_at = datetime.now(timezone.utc)
            session.commit()
            session.refresh(screen)

            return self._screen_to_dict(screen)
        except Exception as e:
            session.rollback()
            logger.error(f"Failed to update screen: {e}")
            raise
        finally:
            session.close()

    def delete_screen(self, screen_id: int) -> bool:
        """Delete a saved screen"""
        session = self.db_service.get_session()
        try:
            screen = session.query(SavedScreen).filter(SavedScreen.id == screen_id).first()
            if not screen:
                return False

            # Delete associated results and scheduled scans
            session.query(ScreenResult).filter(ScreenResult.screen_id == screen_id).delete()
            session.query(ScheduledScan).filter(ScheduledScan.screen_id == screen_id).delete()
            session.delete(screen)
            session.commit()

            return True
        except Exception as e:
            session.rollback()
            logger.error(f"Failed to delete screen: {e}")
            raise
        finally:
            session.close()

    def schedule_screen(
        self,
        screen_id: int,
        frequency: str,
        time: str,
        email_results: bool = False,
        alert_on_match: bool = False,
    ) -> Optional[Dict[str, Any]]:
        """Schedule a screen to run automatically"""
        session = self.db_service.get_session()
        try:
            screen = session.query(SavedScreen).filter(SavedScreen.id == screen_id).first()
            if not screen:
                return None

            screen.is_scheduled = True
            screen.schedule_frequency = frequency
            screen.schedule_time = time
            screen.email_results = email_results
            screen.alert_on_match = alert_on_match

            session.commit()
            session.refresh(screen)

            return self._screen_to_dict(screen)
        except Exception as e:
            session.rollback()
            logger.error(f"Failed to schedule screen: {e}")
            raise
        finally:
            session.close()

    def unschedule_screen(self, screen_id: int) -> Optional[Dict[str, Any]]:
        """Remove schedule from a screen"""
        session = self.db_service.get_session()
        try:
            screen = session.query(SavedScreen).filter(SavedScreen.id == screen_id).first()
            if not screen:
                return None

            screen.is_scheduled = False
            screen.schedule_frequency = None
            screen.schedule_time = None

            session.commit()
            session.refresh(screen)

            return self._screen_to_dict(screen)
        except Exception as e:
            session.rollback()
            logger.error(f"Failed to unschedule screen: {e}")
            raise
        finally:
            session.close()

    async def run_screen(
        self,
        screen_id: int,
        limit: int = 50,
        save_results: bool = True
    ) -> Dict[str, Any]:
        """Run a saved screen and optionally save results"""
        session = self.db_service.get_session()
        try:
            screen = session.query(SavedScreen).filter(SavedScreen.id == screen_id).first()
            if not screen:
                raise ValueError(f"Screen {screen_id} not found")

            # Parse filter criteria
            criteria_dict = json.loads(screen.filter_criteria)
            criteria = FilterCriteria.from_dict(criteria_dict)

            # Run the screen
            results = await advanced_screener_service.run_screen(
                filter_criteria=criteria,
                limit=limit
            )

            # Save results if requested
            if save_results and results.get("results"):
                self._save_screen_results(session, screen_id, results["results"])

            # Update last run time
            screen.last_run_at = datetime.now(timezone.utc)
            session.commit()

            return results

        finally:
            session.close()

    def get_screen_results(
        self,
        screen_id: int,
        limit: int = 100,
        since: Optional[datetime] = None
    ) -> List[Dict[str, Any]]:
        """Get historical results for a screen"""
        session = self.db_service.get_session()
        try:
            query = session.query(ScreenResult, Ticker).join(
                Ticker, ScreenResult.ticker_id == Ticker.id
            ).filter(ScreenResult.screen_id == screen_id)

            if since:
                query = query.filter(ScreenResult.executed_at >= since)

            results = query.order_by(
                ScreenResult.executed_at.desc(),
                ScreenResult.score.desc()
            ).limit(limit).all()

            return [
                {
                    "symbol": ticker.symbol,
                    "name": ticker.name,
                    "sector": ticker.sector,
                    "score": result.score,
                    "price": result.price,
                    "volume": result.volume,
                    "rs_rating": result.rs_rating,
                    "match_data": json.loads(result.match_data) if result.match_data else {},
                    "executed_at": result.executed_at.isoformat(),
                }
                for result, ticker in results
            ]
        finally:
            session.close()

    def get_scheduled_screens(self) -> List[Dict[str, Any]]:
        """Get all scheduled screens"""
        session = self.db_service.get_session()
        try:
            screens = session.query(SavedScreen).filter(
                SavedScreen.is_scheduled == True
            ).all()
            return [self._screen_to_dict(screen) for screen in screens]
        finally:
            session.close()

    def create_template_screens(self):
        """Create pre-built template screens in the database"""
        templates = screen_templates.get_all_templates()

        for template_type, template_info in templates.items():
            try:
                self.create_screen(
                    name=template_info["name"],
                    description=template_info["description"],
                    filter_criteria=template_info["criteria"],
                    is_template=True,
                    template_type=template_type,
                    user_id="system"
                )
                logger.info(f"Created template screen: {template_info['name']}")
            except Exception as e:
                logger.warning(f"Template {template_type} may already exist or failed: {e}")

    def _save_screen_results(
        self,
        session: Session,
        screen_id: int,
        results: List[Dict[str, Any]]
    ):
        """Save screen results to database"""
        for result in results:
            try:
                # Get or create ticker
                ticker = session.query(Ticker).filter(
                    Ticker.symbol == result["symbol"]
                ).first()

                if not ticker:
                    ticker = Ticker(
                        symbol=result["symbol"],
                        name=result.get("name"),
                        sector=result.get("sector"),
                        industry=result.get("industry")
                    )
                    session.add(ticker)
                    session.flush()

                # Create screen result
                screen_result = ScreenResult(
                    screen_id=screen_id,
                    ticker_id=ticker.id,
                    score=result.get("score", 0),
                    match_data=json.dumps(result.get("match_data", {})),
                    price=result.get("price"),
                    volume=result.get("volume"),
                    rs_rating=result.get("rs_rating"),
                )
                session.add(screen_result)

            except Exception as e:
                logger.error(f"Failed to save result for {result.get('symbol')}: {e}")

        session.commit()

    def _screen_to_dict(self, screen: SavedScreen) -> Dict[str, Any]:
        """Convert SavedScreen model to dictionary"""
        return {
            "id": screen.id,
            "user_id": screen.user_id,
            "name": screen.name,
            "description": screen.description,
            "filter_criteria": json.loads(screen.filter_criteria) if screen.filter_criteria else {},
            "is_template": screen.is_template,
            "template_type": screen.template_type,
            "is_scheduled": screen.is_scheduled,
            "schedule_frequency": screen.schedule_frequency,
            "schedule_time": screen.schedule_time,
            "email_results": screen.email_results,
            "alert_on_match": screen.alert_on_match,
            "last_run_at": screen.last_run_at.isoformat() if screen.last_run_at else None,
            "created_at": screen.created_at.isoformat() if screen.created_at else None,
            "updated_at": screen.updated_at.isoformat() if screen.updated_at else None,
        }


# Global service instance - will be initialized with db_service
_saved_screen_service: Optional[SavedScreenService] = None


def get_saved_screen_service() -> SavedScreenService:
    """Get the global SavedScreenService instance"""
    global _saved_screen_service
    if _saved_screen_service is None:
        from app.services.database import get_db_service
        _saved_screen_service = SavedScreenService(get_db_service())
    return _saved_screen_service
