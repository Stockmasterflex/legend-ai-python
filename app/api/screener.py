"""
Advanced Stock Screener API Endpoints

Provides comprehensive screening capabilities with:
- Custom filter criteria
- Pre-built screen templates
- Save & schedule functionality
- CSV export
- Screen result history
"""
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
from fastapi import APIRouter, HTTPException, Query, Response
from pydantic import BaseModel, Field

from app.services.advanced_screener import FilterCriteria, advanced_screener_service
from app.services.screen_templates import screen_templates
from app.services.saved_screen_service import get_saved_screen_service
from app.services.screen_scheduler import screen_scheduler_service

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/screener", tags=["screener"])


# Pydantic Models
class FilterCriteriaRequest(BaseModel):
    """Request model for filter criteria"""
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    min_volume: Optional[float] = None
    min_avg_volume: Optional[float] = None
    min_rs_rating: Optional[float] = None
    max_rs_rating: Optional[float] = None
    patterns: Optional[List[str]] = None
    min_pattern_confidence: float = 0.6
    above_sma_50: Optional[bool] = None
    above_sma_200: Optional[bool] = None
    above_ema_21: Optional[bool] = None
    sma_50_above_sma_200: Optional[bool] = None
    min_pct_above_sma_50: Optional[float] = None
    max_pct_above_sma_50: Optional[float] = None
    min_price_change_pct: Optional[float] = None
    max_price_change_pct: Optional[float] = None
    price_change_period: int = 20
    min_atr: Optional[float] = None
    max_atr: Optional[float] = None
    sectors: Optional[List[str]] = None
    exclude_sectors: Optional[List[str]] = None
    minervini_template: Optional[bool] = None
    gap_up_today: Optional[bool] = None
    min_gap_pct: Optional[float] = None
    in_consolidation: Optional[bool] = None
    max_consolidation_days: Optional[int] = None


class ScreenRequest(BaseModel):
    """Request to run a custom screen"""
    filter_criteria: FilterCriteriaRequest
    universe: Optional[List[str]] = None
    limit: int = Field(default=50, ge=1, le=200)


class SavedScreenRequest(BaseModel):
    """Request to create a saved screen"""
    name: str
    description: Optional[str] = None
    filter_criteria: FilterCriteriaRequest
    user_id: str = "default"


class ScheduleRequest(BaseModel):
    """Request to schedule a screen"""
    frequency: str = Field(..., pattern="^(daily|weekly|hourly)$")
    time: str = Field(..., pattern="^([0-1][0-9]|2[0-3]):[0-5][0-9]$")
    email_results: bool = False
    alert_on_match: bool = False


# Endpoints
@router.post("/run")
async def run_custom_screen(request: ScreenRequest):
    """
    Run a custom screen with specified filter criteria

    Args:
        request: Screen request with filter criteria

    Returns:
        Screen results with matches
    """
    try:
        # Convert request to FilterCriteria
        criteria = FilterCriteria(**request.filter_criteria.dict(exclude_none=True))

        # Run the screen
        results = await advanced_screener_service.run_screen(
            filter_criteria=criteria,
            universe=request.universe,
            limit=request.limit
        )

        return results

    except Exception as e:
        logger.error(f"Failed to run screen: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/templates")
async def get_templates():
    """
    Get all available pre-built screen templates

    Returns:
        Dictionary of available templates with metadata
    """
    try:
        templates = screen_templates.get_all_templates()

        # Convert FilterCriteria to dict for serialization
        result = {}
        for key, template in templates.items():
            result[key] = {
                "name": template["name"],
                "description": template["description"],
                "category": template["category"],
                "difficulty": template["difficulty"],
                "criteria": template["criteria"].to_dict()
            }

        return result

    except Exception as e:
        logger.error(f"Failed to get templates: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/templates/{template_type}/run")
async def run_template_screen(
    template_type: str,
    limit: int = Query(50, ge=1, le=200),
    universe: Optional[List[str]] = None
):
    """
    Run a pre-built template screen

    Args:
        template_type: Template type (e.g., MINERVINI_SEPA, CANSLIM)
        limit: Maximum results to return
        universe: Optional list of symbols to screen

    Returns:
        Screen results
    """
    try:
        # Get template criteria
        criteria = screen_templates.get_template(template_type)

        if not criteria:
            raise HTTPException(status_code=404, detail=f"Template {template_type} not found")

        # Run the screen
        results = await advanced_screener_service.run_screen(
            filter_criteria=criteria,
            universe=universe,
            limit=limit
        )

        return results

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to run template screen: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/saved")
async def create_saved_screen(request: SavedScreenRequest):
    """
    Create a new saved screen

    Args:
        request: Saved screen request

    Returns:
        Created screen details
    """
    try:
        screen_service = get_saved_screen_service()

        criteria = FilterCriteria(**request.filter_criteria.dict(exclude_none=True))

        screen = screen_service.create_screen(
            name=request.name,
            description=request.description,
            filter_criteria=criteria,
            user_id=request.user_id
        )

        return screen

    except Exception as e:
        logger.error(f"Failed to create saved screen: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/saved")
async def list_saved_screens(
    user_id: str = Query("default"),
    include_templates: bool = Query(True)
):
    """
    List all saved screens for a user

    Args:
        user_id: User ID
        include_templates: Include pre-built templates

    Returns:
        List of saved screens
    """
    try:
        screen_service = get_saved_screen_service()
        screens = screen_service.list_screens(
            user_id=user_id,
            include_templates=include_templates
        )
        return {"screens": screens}

    except Exception as e:
        logger.error(f"Failed to list saved screens: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/saved/{screen_id}")
async def get_saved_screen(screen_id: int):
    """
    Get a specific saved screen

    Args:
        screen_id: Screen ID

    Returns:
        Screen details
    """
    try:
        screen_service = get_saved_screen_service()
        screen = screen_service.get_screen(screen_id)

        if not screen:
            raise HTTPException(status_code=404, detail="Screen not found")

        return screen

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get saved screen: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/saved/{screen_id}")
async def update_saved_screen(
    screen_id: int,
    name: Optional[str] = None,
    description: Optional[str] = None,
    filter_criteria: Optional[FilterCriteriaRequest] = None
):
    """
    Update a saved screen

    Args:
        screen_id: Screen ID
        name: New name
        description: New description
        filter_criteria: New filter criteria

    Returns:
        Updated screen details
    """
    try:
        screen_service = get_saved_screen_service()

        criteria = None
        if filter_criteria:
            criteria = FilterCriteria(**filter_criteria.dict(exclude_none=True))

        screen = screen_service.update_screen(
            screen_id=screen_id,
            name=name,
            description=description,
            filter_criteria=criteria
        )

        if not screen:
            raise HTTPException(status_code=404, detail="Screen not found")

        return screen

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to update saved screen: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/saved/{screen_id}")
async def delete_saved_screen(screen_id: int):
    """
    Delete a saved screen

    Args:
        screen_id: Screen ID

    Returns:
        Success message
    """
    try:
        screen_service = get_saved_screen_service()
        success = screen_service.delete_screen(screen_id)

        if not success:
            raise HTTPException(status_code=404, detail="Screen not found")

        return {"message": "Screen deleted successfully"}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to delete saved screen: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/saved/{screen_id}/run")
async def run_saved_screen(
    screen_id: int,
    limit: int = Query(50, ge=1, le=200),
    save_results: bool = Query(True)
):
    """
    Run a saved screen

    Args:
        screen_id: Screen ID
        limit: Maximum results
        save_results: Whether to save results to database

    Returns:
        Screen results
    """
    try:
        screen_service = get_saved_screen_service()
        results = await screen_service.run_screen(
            screen_id=screen_id,
            limit=limit,
            save_results=save_results
        )

        return results

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Failed to run saved screen: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/saved/{screen_id}/schedule")
async def schedule_screen(screen_id: int, request: ScheduleRequest):
    """
    Schedule a screen to run automatically

    Args:
        screen_id: Screen ID
        request: Schedule configuration

    Returns:
        Updated screen details
    """
    try:
        screen_service = get_saved_screen_service()
        screen = screen_service.schedule_screen(
            screen_id=screen_id,
            frequency=request.frequency,
            time=request.time,
            email_results=request.email_results,
            alert_on_match=request.alert_on_match
        )

        if not screen:
            raise HTTPException(status_code=404, detail="Screen not found")

        return screen

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to schedule screen: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/saved/{screen_id}/schedule")
async def unschedule_screen(screen_id: int):
    """
    Remove schedule from a screen

    Args:
        screen_id: Screen ID

    Returns:
        Updated screen details
    """
    try:
        screen_service = get_saved_screen_service()
        screen = screen_service.unschedule_screen(screen_id)

        if not screen:
            raise HTTPException(status_code=404, detail="Screen not found")

        return screen

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to unschedule screen: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/saved/{screen_id}/results")
async def get_screen_results(
    screen_id: int,
    limit: int = Query(100, ge=1, le=500)
):
    """
    Get historical results for a screen

    Args:
        screen_id: Screen ID
        limit: Maximum results

    Returns:
        Historical screen results
    """
    try:
        screen_service = get_saved_screen_service()
        results = screen_service.get_screen_results(
            screen_id=screen_id,
            limit=limit
        )

        return {"results": results}

    except Exception as e:
        logger.error(f"Failed to get screen results: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/saved/{screen_id}/export/csv")
async def export_screen_results_csv(
    screen_id: int,
    limit: int = Query(100, ge=1, le=500)
):
    """
    Export screen results to CSV

    Args:
        screen_id: Screen ID
        limit: Maximum results

    Returns:
        CSV file
    """
    try:
        screen_service = get_saved_screen_service()
        results = screen_service.get_screen_results(
            screen_id=screen_id,
            limit=limit
        )

        # Generate CSV
        csv_content = screen_scheduler_service.generate_csv_export(results)

        return Response(
            content=csv_content,
            media_type="text/csv",
            headers={
                "Content-Disposition": f"attachment; filename=screen_{screen_id}_results.csv"
            }
        )

    except Exception as e:
        logger.error(f"Failed to export screen results: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/initialize-templates")
async def initialize_templates():
    """
    Initialize pre-built template screens in the database

    Returns:
        Success message
    """
    try:
        screen_service = get_saved_screen_service()
        screen_service.create_template_screens()

        return {"message": "Template screens initialized successfully"}

    except Exception as e:
        logger.error(f"Failed to initialize templates: {e}")
        raise HTTPException(status_code=500, detail=str(e))
