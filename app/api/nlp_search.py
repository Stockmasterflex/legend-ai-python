"""
NLP Search API Endpoints
Provides natural language search capabilities for stock patterns
"""

import time
from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, Query, Body
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession
import logging

from app.services.nlp_search import NLPSearchService
from app.services.search_history import SearchHistoryService
from app.services.voice_search import VoiceSearchService
from app.services.database import get_db
from app.services.scanner import ScannerService
from app.core.detector_registry import detector_registry

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/nlp", tags=["NLP Search"])


# Pydantic models for request/response
class NLPQueryRequest(BaseModel):
    """Request model for NLP query parsing"""
    query: str = Field(..., description="Natural language search query", min_length=1)
    user_id: str = Field(default="default", description="User identifier")
    execute_search: bool = Field(default=True, description="Execute the search or just parse")
    save_history: bool = Field(default=True, description="Save to search history")


class NLPQueryResponse(BaseModel):
    """Response model for NLP query results"""
    original_query: str
    intent: str
    confidence: float
    tickers: List[str]
    patterns: List[str]
    sectors: List[str]
    price_filters: Dict[str, float]
    timeframe: str
    comparison: bool
    suggestions: List[str]
    results: Optional[List[Dict[str, Any]]] = None
    results_count: int = 0
    execution_time: float = 0.0


class VoiceSearchRequest(BaseModel):
    """Request model for voice search metadata"""
    user_id: str = Field(default="default", description="User identifier")
    language: str = Field(default="en", description="Language code (en, es, fr, etc.)")
    enhance_audio: bool = Field(default=True, description="Enhance audio quality")


class VoiceSearchResponse(BaseModel):
    """Response model for voice search results"""
    success: bool
    text: str
    alternatives: List[str]
    confidence: float
    language: str
    duration: float
    query_result: Optional[NLPQueryResponse] = None


class SearchHistoryResponse(BaseModel):
    """Response model for search history"""
    id: int
    query: str
    intent: str
    query_type: str
    results_count: int
    confidence: float
    created_at: str
    is_template: bool
    template_name: Optional[str]


class SearchTemplateRequest(BaseModel):
    """Request model for saving search templates"""
    search_id: int
    template_name: str
    tags: Optional[List[str]] = None


class SearchAnalyticsResponse(BaseModel):
    """Response model for search analytics"""
    period_days: int
    total_searches: int
    voice_searches: int
    text_searches: int
    intent_distribution: Dict[str, int]
    top_tickers: Dict[str, int]
    top_patterns: Dict[str, int]
    avg_confidence: float
    avg_results_per_query: float
    avg_execution_time: float


# Initialize services
nlp_service = NLPSearchService()
voice_service = VoiceSearchService()


@router.post("/search", response_model=NLPQueryResponse)
async def nlp_search(
    request: NLPQueryRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Parse and execute a natural language search query

    Examples:
    - "Find VCP patterns in tech stocks"
    - "Show me breakouts above $100"
    - "Which stocks are pulling back to 21 EMA?"
    - "Compare AAPL and MSFT patterns"
    """
    start_time = time.time()

    try:
        # Parse the query
        parsed = nlp_service.parse_query(request.query, request.user_id)

        results = []
        results_count = 0

        # Execute search if requested
        if request.execute_search:
            results, results_count = await _execute_search(parsed, db)

        execution_time = time.time() - start_time

        # Save to search history if requested
        if request.save_history:
            history_service = SearchHistoryService(db)
            await history_service.save_search(
                query=request.query,
                parsed_data=parsed,
                user_id=request.user_id,
                results_count=results_count,
                execution_time=execution_time,
                voice_query=False
            )

        return NLPQueryResponse(
            original_query=parsed["original_query"],
            intent=parsed["intent"],
            confidence=parsed["confidence"],
            tickers=parsed["tickers"],
            patterns=parsed["patterns"],
            sectors=parsed["sectors"],
            price_filters=parsed["price_filters"],
            timeframe=parsed["timeframe"],
            comparison=parsed["comparison"],
            suggestions=parsed["suggestions"],
            results=results if request.execute_search else None,
            results_count=results_count,
            execution_time=execution_time
        )

    except Exception as e:
        logger.error(f"NLP search error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")


@router.post("/voice/search", response_model=VoiceSearchResponse)
async def voice_search(
    audio_file: UploadFile = File(..., description="Audio file (WAV, MP3, OGG, etc.)"),
    user_id: str = Query(default="default"),
    language: str = Query(default="en"),
    enhance_audio: bool = Query(default=True),
    execute_search: bool = Query(default=True),
    db: AsyncSession = Depends(get_db)
):
    """
    Voice-to-text search with automatic query execution

    Upload an audio file with your search query spoken in natural language.
    Supports multiple languages and audio formats.

    Supported formats: WAV, MP3, OGG, FLAC, M4A, WEBM
    Supported languages: en, es, fr, de, it, pt, ja, ko, zh
    """
    try:
        # Read audio data
        audio_data = await audio_file.read()

        # Extract audio format from filename
        audio_format = audio_file.filename.split('.')[-1].lower()
        if audio_format not in voice_service.SUPPORTED_FORMATS:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported audio format: {audio_format}. "
                       f"Supported: {', '.join(voice_service.SUPPORTED_FORMATS)}"
            )

        # Process voice query
        voice_result = await voice_service.process_voice_query(
            audio_data=audio_data,
            audio_format=audio_format,
            language=language,
            enhance=enhance_audio
        )

        if not voice_result["success"]:
            return VoiceSearchResponse(
                success=False,
                text="",
                alternatives=[],
                confidence=0.0,
                language=language,
                duration=0.0,
                error=voice_result.get("error", "Unknown error")
            )

        # If text was successfully transcribed and execute_search is True
        query_result = None
        if voice_result["text"] and execute_search:
            # Parse and execute the query
            query_request = NLPQueryRequest(
                query=voice_result["text"],
                user_id=user_id,
                execute_search=True,
                save_history=True
            )

            query_result = await nlp_search(query_request, db)

            # Update search history to mark as voice query
            history_service = SearchHistoryService(db)
            recent_searches = await history_service.get_recent_searches(user_id, hours=1, limit=1)
            if recent_searches:
                recent_searches[0].voice_query = True
                await db.commit()

        return VoiceSearchResponse(
            success=True,
            text=voice_result["text"],
            alternatives=voice_result.get("alternatives", []),
            confidence=voice_result.get("confidence", 0.0),
            language=voice_result.get("language", language),
            duration=voice_result.get("duration", 0.0),
            query_result=query_result
        )

    except Exception as e:
        logger.error(f"Voice search error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Voice search failed: {str(e)}")


@router.get("/autocomplete")
async def autocomplete(
    query: str = Query(..., description="Partial query text", min_length=1),
    limit: int = Query(default=5, ge=1, le=20)
):
    """
    Get autocomplete suggestions for partial queries

    Returns suggested completions based on common patterns and queries.
    """
    try:
        suggestions = nlp_service.autocomplete(query, limit=limit)

        return {
            "query": query,
            "suggestions": suggestions
        }

    except Exception as e:
        logger.error(f"Autocomplete error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Autocomplete failed: {str(e)}")


@router.post("/correct")
async def correct_typos(
    query: str = Body(..., embed=True, description="Query with potential typos")
):
    """
    Auto-correct typos in search queries

    Corrects common misspellings of pattern names and stock terminology.
    """
    try:
        corrected = nlp_service.correct_typos(query)

        return {
            "original": query,
            "corrected": corrected,
            "changed": query.lower() != corrected.lower()
        }

    except Exception as e:
        logger.error(f"Typo correction error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Correction failed: {str(e)}")


@router.get("/history", response_model=List[SearchHistoryResponse])
async def get_search_history(
    user_id: str = Query(default="default"),
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    query_type: Optional[str] = Query(default=None),
    intent: Optional[str] = Query(default=None),
    db: AsyncSession = Depends(get_db)
):
    """
    Get user's search history

    Retrieve past searches with optional filtering by query type and intent.
    """
    try:
        history_service = SearchHistoryService(db)
        history = await history_service.get_user_history(
            user_id=user_id,
            limit=limit,
            offset=offset,
            query_type=query_type,
            intent=intent
        )

        return [
            SearchHistoryResponse(
                id=h.id,
                query=h.query,
                intent=h.intent,
                query_type=h.query_type,
                results_count=h.results_count,
                confidence=h.confidence,
                created_at=h.created_at.isoformat(),
                is_template=h.is_template,
                template_name=h.template_name
            )
            for h in history
        ]

    except Exception as e:
        logger.error(f"History retrieval error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve history: {str(e)}")


@router.get("/history/popular")
async def get_popular_queries(
    limit: int = Query(default=10, ge=1, le=50),
    days: int = Query(default=7, ge=1, le=90),
    db: AsyncSession = Depends(get_db)
):
    """
    Get most popular search queries

    Returns trending searches across all users within the specified time period.
    """
    try:
        history_service = SearchHistoryService(db)
        popular = await history_service.get_popular_queries(
            limit=limit,
            days=days,
            min_results=1
        )

        return {"popular_queries": popular}

    except Exception as e:
        logger.error(f"Popular queries error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get popular queries: {str(e)}")


@router.post("/template/save", response_model=SearchHistoryResponse)
async def save_search_template(
    request: SearchTemplateRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Save a search as a reusable template

    Templates can be quickly re-run and shared with other users.
    """
    try:
        history_service = SearchHistoryService(db)
        template = await history_service.save_template(
            search_id=request.search_id,
            template_name=request.template_name,
            tags=request.tags
        )

        return SearchHistoryResponse(
            id=template.id,
            query=template.query,
            intent=template.intent,
            query_type=template.query_type,
            results_count=template.results_count,
            confidence=template.confidence,
            created_at=template.created_at.isoformat(),
            is_template=template.is_template,
            template_name=template.template_name
        )

    except Exception as e:
        logger.error(f"Save template error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to save template: {str(e)}")


@router.get("/templates", response_model=List[SearchHistoryResponse])
async def get_templates(
    user_id: str = Query(default="default"),
    tags: Optional[List[str]] = Query(default=None),
    include_shared: bool = Query(default=True),
    db: AsyncSession = Depends(get_db)
):
    """
    Get saved search templates

    Returns user's templates and optionally templates shared by others.
    """
    try:
        history_service = SearchHistoryService(db)

        # Get user's templates
        templates = await history_service.get_templates(user_id=user_id, tags=tags)

        # Include shared templates if requested
        if include_shared:
            shared = await history_service.get_shared_templates(user_id=user_id)
            templates.extend(shared)

        return [
            SearchHistoryResponse(
                id=t.id,
                query=t.query,
                intent=t.intent,
                query_type=t.query_type,
                results_count=t.results_count,
                confidence=t.confidence,
                created_at=t.created_at.isoformat(),
                is_template=t.is_template,
                template_name=t.template_name
            )
            for t in templates
        ]

    except Exception as e:
        logger.error(f"Get templates error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get templates: {str(e)}")


@router.get("/analytics", response_model=SearchAnalyticsResponse)
async def get_search_analytics(
    user_id: str = Query(default="default"),
    days: int = Query(default=30, ge=1, le=365),
    db: AsyncSession = Depends(get_db)
):
    """
    Get search analytics and insights

    Returns analytics about search patterns, popular tickers, and query performance.
    """
    try:
        history_service = SearchHistoryService(db)
        analytics = await history_service.get_search_analytics(
            user_id=user_id,
            days=days
        )

        return SearchAnalyticsResponse(**analytics)

    except Exception as e:
        logger.error(f"Analytics error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get analytics: {str(e)}")


@router.get("/suggestions")
async def get_contextual_suggestions(
    user_id: str = Query(default="default"),
    limit: int = Query(default=5, ge=1, le=20),
    db: AsyncSession = Depends(get_db)
):
    """
    Get personalized query suggestions

    Returns suggestions based on user's search history and popular queries.
    """
    try:
        history_service = SearchHistoryService(db)
        suggestions = await history_service.get_contextual_suggestions(
            user_id=user_id,
            limit=limit
        )

        return {"suggestions": suggestions}

    except Exception as e:
        logger.error(f"Suggestions error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get suggestions: {str(e)}")


@router.get("/voice/languages")
async def get_supported_languages():
    """
    Get list of supported languages for voice search

    Returns language codes and their full names.
    """
    return {
        "languages": voice_service.get_supported_languages()
    }


# Helper function to execute the actual search
async def _execute_search(
    parsed: Dict[str, Any],
    db: AsyncSession
) -> tuple[List[Dict[str, Any]], int]:
    """
    Execute the search based on parsed query

    Args:
        parsed: Parsed query data
        db: Database session

    Returns:
        Tuple of (results list, count)
    """
    results = []
    intent = parsed["intent"]

    try:
        if intent == "scan":
            # Pattern scanning
            scanner = ScannerService()

            # Determine which patterns to scan for
            patterns = parsed["patterns"] if parsed["patterns"] else ["vcp"]

            for pattern in patterns:
                # Get detector for pattern
                detector = detector_registry.get(pattern)
                if detector:
                    # For now, return pattern info
                    # In production, this would trigger actual scanning
                    results.append({
                        "pattern": pattern,
                        "status": "scanning",
                        "message": f"Scanning for {pattern} patterns"
                    })

        elif intent == "analyze" and parsed["tickers"]:
            # Ticker analysis
            for ticker in parsed["tickers"]:
                results.append({
                    "ticker": ticker,
                    "status": "analysis_requested",
                    "message": f"Analysis for {ticker} requested"
                })

        elif intent == "compare" and len(parsed["tickers"]) >= 2:
            # Comparison
            results.append({
                "tickers": parsed["tickers"],
                "status": "comparison_requested",
                "message": f"Comparing {', '.join(parsed['tickers'])}"
            })

        else:
            # Generic response
            results.append({
                "status": "query_understood",
                "intent": intent,
                "message": f"Understood query with intent: {intent}"
            })

        return results, len(results)

    except Exception as e:
        logger.error(f"Search execution error: {str(e)}")
        return [], 0
