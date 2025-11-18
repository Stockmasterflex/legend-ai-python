"""
Search History Management Service
Handles storage, retrieval, and analytics for NLP search queries
"""

import json
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from sqlalchemy import select, func, and_, or_, desc
from sqlalchemy.ext.asyncio import AsyncSession
import logging

from app.models import SearchHistory, QuerySuggestion

logger = logging.getLogger(__name__)


class SearchHistoryService:
    """
    Service for managing search history and query templates
    Provides search analytics, popular queries, and personalized suggestions
    """

    def __init__(self, db_session: AsyncSession):
        """Initialize service with database session"""
        self.db = db_session

    async def save_search(
        self,
        query: str,
        parsed_data: Dict[str, Any],
        user_id: str = "default",
        results_count: int = 0,
        execution_time: float = 0.0,
        voice_query: bool = False,
        language: str = "en"
    ) -> SearchHistory:
        """
        Save a search query to history

        Args:
            query: Original natural language query
            parsed_data: Parsed query data from NLPSearchService
            user_id: User identifier
            results_count: Number of results returned
            execution_time: Query execution time in seconds
            voice_query: Whether this was a voice query
            language: Query language code

        Returns:
            Created SearchHistory record
        """
        search_record = SearchHistory(
            user_id=user_id,
            query=query,
            query_type=self._determine_query_type(parsed_data),
            extracted_tickers=json.dumps(parsed_data.get("tickers", [])),
            extracted_patterns=json.dumps(parsed_data.get("patterns", [])),
            extracted_filters=json.dumps({
                "sectors": parsed_data.get("sectors", []),
                "price": parsed_data.get("price_filters", {}),
                "timeframe": parsed_data.get("timeframe"),
            }),
            intent=parsed_data.get("intent", "unknown"),
            confidence=parsed_data.get("confidence", 0.0),
            results_count=results_count,
            execution_time=execution_time,
            voice_query=voice_query,
            language=language,
        )

        self.db.add(search_record)
        await self.db.commit()
        await self.db.refresh(search_record)

        logger.info(f"Saved search query: {query[:50]}... for user {user_id}")

        # Update query suggestions based on this search
        await self._update_suggestions(parsed_data)

        return search_record

    async def get_user_history(
        self,
        user_id: str,
        limit: int = 50,
        offset: int = 0,
        query_type: Optional[str] = None,
        intent: Optional[str] = None
    ) -> List[SearchHistory]:
        """
        Retrieve user's search history

        Args:
            user_id: User identifier
            limit: Maximum number of records to return
            offset: Number of records to skip
            query_type: Filter by query type
            intent: Filter by intent

        Returns:
            List of SearchHistory records
        """
        query = select(SearchHistory).where(SearchHistory.user_id == user_id)

        if query_type:
            query = query.where(SearchHistory.query_type == query_type)

        if intent:
            query = query.where(SearchHistory.intent == intent)

        query = query.order_by(desc(SearchHistory.created_at)).limit(limit).offset(offset)

        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def get_recent_searches(
        self,
        user_id: str,
        hours: int = 24,
        limit: int = 10
    ) -> List[SearchHistory]:
        """Get recent searches within specified hours"""
        cutoff_time = datetime.utcnow() - timedelta(hours=hours)

        query = (
            select(SearchHistory)
            .where(
                and_(
                    SearchHistory.user_id == user_id,
                    SearchHistory.created_at >= cutoff_time
                )
            )
            .order_by(desc(SearchHistory.created_at))
            .limit(limit)
        )

        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def get_popular_queries(
        self,
        limit: int = 10,
        days: int = 7,
        min_results: int = 1
    ) -> List[Dict[str, Any]]:
        """
        Get most popular queries across all users

        Args:
            limit: Maximum number of queries to return
            days: Look back this many days
            min_results: Only include queries that returned at least this many results

        Returns:
            List of popular queries with usage count
        """
        cutoff_time = datetime.utcnow() - timedelta(days=days)

        query = (
            select(
                SearchHistory.query,
                SearchHistory.intent,
                func.count(SearchHistory.id).label("usage_count"),
                func.avg(SearchHistory.results_count).label("avg_results"),
                func.avg(SearchHistory.confidence).label("avg_confidence")
            )
            .where(
                and_(
                    SearchHistory.created_at >= cutoff_time,
                    SearchHistory.results_count >= min_results
                )
            )
            .group_by(SearchHistory.query, SearchHistory.intent)
            .order_by(desc("usage_count"))
            .limit(limit)
        )

        result = await self.db.execute(query)
        rows = result.all()

        return [
            {
                "query": row.query,
                "intent": row.intent,
                "usage_count": row.usage_count,
                "avg_results": float(row.avg_results) if row.avg_results else 0,
                "avg_confidence": float(row.avg_confidence) if row.avg_confidence else 0,
            }
            for row in rows
        ]

    async def save_template(
        self,
        search_id: int,
        template_name: str,
        tags: Optional[List[str]] = None
    ) -> SearchHistory:
        """
        Save a search as a reusable template

        Args:
            search_id: ID of the search to save as template
            template_name: Name for the template
            tags: Optional tags for categorization

        Returns:
            Updated SearchHistory record
        """
        query = select(SearchHistory).where(SearchHistory.id == search_id)
        result = await self.db.execute(query)
        search = result.scalar_one_or_none()

        if not search:
            raise ValueError(f"Search with ID {search_id} not found")

        search.is_template = True
        search.template_name = template_name
        if tags:
            search.tags = json.dumps(tags)

        await self.db.commit()
        await self.db.refresh(search)

        logger.info(f"Saved search template: {template_name}")

        return search

    async def get_templates(
        self,
        user_id: str,
        tags: Optional[List[str]] = None
    ) -> List[SearchHistory]:
        """
        Get saved search templates

        Args:
            user_id: User identifier
            tags: Filter by tags

        Returns:
            List of template searches
        """
        query = select(SearchHistory).where(
            and_(
                SearchHistory.user_id == user_id,
                SearchHistory.is_template == True
            )
        )

        result = await self.db.execute(query)
        templates = list(result.scalars().all())

        # Filter by tags if provided
        if tags:
            templates = [
                t for t in templates
                if t.tags and any(tag in json.loads(t.tags) for tag in tags)
            ]

        return templates

    async def share_template(
        self,
        template_id: int,
        share_with_users: List[str]
    ) -> SearchHistory:
        """
        Share a template with other users

        Args:
            template_id: ID of the template to share
            share_with_users: List of user IDs to share with

        Returns:
            Updated SearchHistory record
        """
        query = select(SearchHistory).where(
            and_(
                SearchHistory.id == template_id,
                SearchHistory.is_template == True
            )
        )
        result = await self.db.execute(query)
        template = result.scalar_one_or_none()

        if not template:
            raise ValueError(f"Template with ID {template_id} not found")

        current_shares = json.loads(template.shared_with) if template.shared_with else []
        updated_shares = list(set(current_shares + share_with_users))
        template.shared_with = json.dumps(updated_shares)

        await self.db.commit()
        await self.db.refresh(template)

        logger.info(f"Shared template {template_id} with {len(share_with_users)} users")

        return template

    async def get_shared_templates(self, user_id: str) -> List[SearchHistory]:
        """Get templates shared with this user"""
        query = select(SearchHistory).where(
            and_(
                SearchHistory.is_template == True,
                SearchHistory.shared_with.isnot(None)
            )
        )

        result = await self.db.execute(query)
        all_templates = list(result.scalars().all())

        # Filter to only templates shared with this user
        shared_templates = [
            t for t in all_templates
            if user_id in json.loads(t.shared_with or "[]")
        ]

        return shared_templates

    async def get_search_analytics(
        self,
        user_id: str,
        days: int = 30
    ) -> Dict[str, Any]:
        """
        Get analytics about user's search patterns

        Args:
            user_id: User identifier
            days: Look back this many days

        Returns:
            Dictionary with analytics data
        """
        cutoff_time = datetime.utcnow() - timedelta(days=days)

        # Total searches
        total_query = select(func.count(SearchHistory.id)).where(
            and_(
                SearchHistory.user_id == user_id,
                SearchHistory.created_at >= cutoff_time
            )
        )
        total_result = await self.db.execute(total_query)
        total_searches = total_result.scalar()

        # Searches by intent
        intent_query = (
            select(
                SearchHistory.intent,
                func.count(SearchHistory.id).label("count")
            )
            .where(
                and_(
                    SearchHistory.user_id == user_id,
                    SearchHistory.created_at >= cutoff_time
                )
            )
            .group_by(SearchHistory.intent)
        )
        intent_result = await self.db.execute(intent_query)
        intent_distribution = {row.intent: row.count for row in intent_result}

        # Most searched tickers
        ticker_query = select(SearchHistory.extracted_tickers).where(
            and_(
                SearchHistory.user_id == user_id,
                SearchHistory.created_at >= cutoff_time,
                SearchHistory.extracted_tickers.isnot(None)
            )
        )
        ticker_result = await self.db.execute(ticker_query)
        all_tickers = []
        for row in ticker_result:
            tickers = json.loads(row.extracted_tickers)
            all_tickers.extend(tickers)

        from collections import Counter
        ticker_counts = Counter(all_tickers)
        top_tickers = dict(ticker_counts.most_common(10))

        # Most searched patterns
        pattern_query = select(SearchHistory.extracted_patterns).where(
            and_(
                SearchHistory.user_id == user_id,
                SearchHistory.created_at >= cutoff_time,
                SearchHistory.extracted_patterns.isnot(None)
            )
        )
        pattern_result = await self.db.execute(pattern_query)
        all_patterns = []
        for row in pattern_result:
            patterns = json.loads(row.extracted_patterns)
            all_patterns.extend(patterns)

        pattern_counts = Counter(all_patterns)
        top_patterns = dict(pattern_counts.most_common(10))

        # Average confidence and results
        avg_query = (
            select(
                func.avg(SearchHistory.confidence).label("avg_confidence"),
                func.avg(SearchHistory.results_count).label("avg_results"),
                func.avg(SearchHistory.execution_time).label("avg_execution_time")
            )
            .where(
                and_(
                    SearchHistory.user_id == user_id,
                    SearchHistory.created_at >= cutoff_time
                )
            )
        )
        avg_result = await self.db.execute(avg_query)
        avg_row = avg_result.one()

        # Voice vs text searches
        voice_query = select(func.count(SearchHistory.id)).where(
            and_(
                SearchHistory.user_id == user_id,
                SearchHistory.created_at >= cutoff_time,
                SearchHistory.voice_query == True
            )
        )
        voice_result = await self.db.execute(voice_query)
        voice_searches = voice_result.scalar()

        return {
            "period_days": days,
            "total_searches": total_searches,
            "voice_searches": voice_searches,
            "text_searches": total_searches - voice_searches,
            "intent_distribution": intent_distribution,
            "top_tickers": top_tickers,
            "top_patterns": top_patterns,
            "avg_confidence": float(avg_row.avg_confidence) if avg_row.avg_confidence else 0,
            "avg_results_per_query": float(avg_row.avg_results) if avg_row.avg_results else 0,
            "avg_execution_time": float(avg_row.avg_execution_time) if avg_row.avg_execution_time else 0,
        }

    async def _update_suggestions(self, parsed_data: Dict[str, Any]):
        """Update query suggestions based on successful searches"""
        # This would be expanded to use ML for better suggestions
        # For now, just track successful patterns

        patterns = parsed_data.get("patterns", [])
        sectors = parsed_data.get("sectors", [])

        for pattern in patterns:
            # Check if suggestion exists
            query = select(QuerySuggestion).where(
                QuerySuggestion.suggestion_text == f"Find {pattern} patterns"
            )
            result = await self.db.execute(query)
            suggestion = result.scalar_one_or_none()

            if suggestion:
                # Increment popularity
                suggestion.popularity_score += 0.1
            else:
                # Create new suggestion
                new_suggestion = QuerySuggestion(
                    suggestion_text=f"Find {pattern} patterns",
                    category="pattern",
                    popularity_score=1.0,
                    context_patterns=json.dumps([pattern]),
                    context_sectors=json.dumps(sectors) if sectors else None,
                )
                self.db.add(new_suggestion)

        await self.db.commit()

    async def get_contextual_suggestions(
        self,
        user_id: str,
        limit: int = 5
    ) -> List[str]:
        """
        Get personalized suggestions based on user's search history

        Args:
            user_id: User identifier
            limit: Maximum number of suggestions

        Returns:
            List of suggested queries
        """
        # Get user's recent search patterns
        recent_searches = await self.get_recent_searches(user_id, hours=72, limit=20)

        # Extract common patterns and tickers
        all_patterns = []
        all_tickers = []

        for search in recent_searches:
            if search.extracted_patterns:
                all_patterns.extend(json.loads(search.extracted_patterns))
            if search.extracted_tickers:
                all_tickers.extend(json.loads(search.extracted_tickers))

        # Get popular suggestions matching user's interests
        query = select(QuerySuggestion).order_by(desc(QuerySuggestion.popularity_score))

        result = await self.db.execute(query)
        all_suggestions = list(result.scalars().all())

        # Score suggestions based on relevance to user
        scored_suggestions = []
        for suggestion in all_suggestions:
            score = suggestion.popularity_score

            # Boost score if matches user's recent patterns
            if suggestion.context_patterns:
                context_patterns = json.loads(suggestion.context_patterns)
                if any(p in all_patterns for p in context_patterns):
                    score *= 2

            scored_suggestions.append((suggestion.suggestion_text, score))

        # Sort by score and return top N
        scored_suggestions.sort(key=lambda x: x[1], reverse=True)
        return [s[0] for s in scored_suggestions[:limit]]

    def _determine_query_type(self, parsed_data: Dict[str, Any]) -> str:
        """Determine the query type from parsed data"""
        if parsed_data.get("comparison"):
            return "comparison"
        elif parsed_data.get("tickers"):
            return "ticker"
        elif parsed_data.get("patterns"):
            return "pattern"
        else:
            return "general"
