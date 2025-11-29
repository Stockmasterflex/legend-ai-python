"""
Market Dashboard View - TradingView widgets
"""
from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from pathlib import Path

router = APIRouter(prefix="/dashboard", tags=["dashboard"])

@router.get("", response_class=HTMLResponse)
async def get_dashboard():
    """Serve market dashboard with TradingView widgets"""
    dashboard_path = Path(__file__).parent.parent.parent / "templates" / "dashboard.html"
    
    if dashboard_path.exists():
        return HTMLResponse(content=dashboard_path.read_text())
    else:
        return HTMLResponse(
            content="<h1>Dashboard not found</h1>",
            status_code=404
        )

