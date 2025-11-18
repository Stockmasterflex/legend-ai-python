"""
NLP-based Stock Search Service
Provides natural language query parsing for stock pattern searches
"""

import re
import json
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime
from fuzzywuzzy import fuzz, process
import logging

logger = logging.getLogger(__name__)


class NLPSearchService:
    """
    Natural Language Processing service for parsing stock search queries
    Handles intent classification, entity extraction, and intelligent filtering
    """

    # Pattern name mappings with synonyms and variations
    PATTERN_MAPPINGS = {
        "vcp": ["vcp", "volatility contraction", "volatility contraction pattern",
                "vol contraction", "minervini", "mark minervini"],
        "cup_and_handle": ["cup and handle", "cup & handle", "cup handle", "cup-and-handle",
                          "cup with handle", "cup+handle"],
        "ascending_triangle": ["ascending triangle", "asc triangle", "bullish triangle",
                              "upward triangle", "ascending tri"],
        "descending_triangle": ["descending triangle", "desc triangle", "bearish triangle",
                               "downward triangle", "descending tri"],
        "symmetrical_triangle": ["symmetrical triangle", "symmetrical tri", "symmetric triangle",
                                "neutral triangle"],
        "rising_wedge": ["rising wedge", "ascending wedge", "upward wedge"],
        "falling_wedge": ["falling wedge", "descending wedge", "downward wedge"],
        "head_and_shoulders": ["head and shoulders", "head & shoulders", "h&s", "hs",
                              "head-and-shoulders"],
        "inverse_head_and_shoulders": ["inverse head and shoulders", "inverse h&s",
                                       "inverted head and shoulders", "reverse h&s"],
        "double_top": ["double top", "double-top", "twin peaks"],
        "double_bottom": ["double bottom", "double-bottom", "twin valleys"],
        "channel_up": ["channel up", "ascending channel", "upward channel", "bullish channel"],
        "channel_down": ["channel down", "descending channel", "downward channel", "bearish channel"],
        "channel_sideways": ["channel sideways", "horizontal channel", "sideways channel",
                            "ranging channel"],
        "sma50_pullback": ["50 sma pullback", "50 sma", "50 day moving average", "50ma pullback",
                          "pullback to 50", "50 day pullback"],
        "breakout": ["breakout", "break out", "breaking out", "breakthrough"],
    }

    # Intent keywords for classification
    INTENT_KEYWORDS = {
        "scan": ["scan", "find", "search", "show", "look for", "discover", "identify",
                "locate", "which stocks", "what stocks", "any stocks"],
        "analyze": ["analyze", "analysis", "check", "look at", "review", "examine",
                   "evaluate", "assess", "study"],
        "compare": ["compare", "vs", "versus", "difference between", "contrast",
                   "comparison", "better than", "vs."],
        "chart": ["chart", "graph", "show me", "display", "plot", "visualize"],
        "watchlist": ["watchlist", "add to", "track", "monitor", "watch", "follow"],
        "market": ["market", "spy", "indices", "overall market", "market condition",
                  "how is the market", "market status"],
        "plan": ["trading plan", "position size", "how much", "risk", "trade setup",
                "entry", "exit", "stop loss"],
    }

    # Sector keywords
    SECTOR_KEYWORDS = {
        "technology": ["tech", "technology", "software", "saas", "cloud", "semiconductor",
                      "hardware", "it", "cyber", "ai", "artificial intelligence"],
        "healthcare": ["healthcare", "health", "pharma", "biotech", "medical", "drug"],
        "financial": ["financial", "finance", "bank", "fintech", "insurance", "investment"],
        "energy": ["energy", "oil", "gas", "renewable", "solar", "wind"],
        "consumer": ["consumer", "retail", "ecommerce", "shopping", "discretionary", "staples"],
        "industrial": ["industrial", "manufacturing", "construction", "machinery"],
        "materials": ["materials", "mining", "metals", "commodities", "chemicals"],
        "utilities": ["utilities", "electric", "water", "power"],
        "real_estate": ["real estate", "reit", "property", "housing"],
        "communication": ["communication", "telecom", "media", "entertainment"],
    }

    # Timeframe keywords
    TIMEFRAME_KEYWORDS = {
        "daily": ["daily", "1d", "day", "today"],
        "weekly": ["weekly", "1w", "week"],
        "monthly": ["monthly", "1m", "month"],
        "intraday": ["intraday", "15m", "30m", "1h", "hourly"],
    }

    # Common ticker symbols for quick recognition
    COMMON_TICKERS = [
        "AAPL", "MSFT", "GOOGL", "GOOG", "AMZN", "META", "TSLA", "NVDA", "BRK.B", "V",
        "JPM", "JNJ", "WMT", "PG", "MA", "UNH", "DIS", "HD", "BAC", "ADBE",
        "CRM", "NFLX", "CMCSA", "XOM", "PFE", "CSCO", "VZ", "ABT", "INTC", "KO",
        "PEP", "NKE", "MRK", "T", "CVX", "AVGO", "ORCL", "TMO", "LLY", "MCD",
        "COST", "DHR", "NEE", "MDT", "UNP", "TXN", "BMY", "QCOM", "HON", "PM",
        "SPY", "QQQ", "IWM", "DIA",  # ETFs
    ]

    def __init__(self):
        """Initialize the NLP search service"""
        self._pattern_lookup = self._build_pattern_lookup()
        self._sector_lookup = self._build_sector_lookup()

    def _build_pattern_lookup(self) -> Dict[str, str]:
        """Build reverse lookup from pattern variations to canonical names"""
        lookup = {}
        for canonical, variations in self.PATTERN_MAPPINGS.items():
            for variation in variations:
                lookup[variation.lower()] = canonical
        return lookup

    def _build_sector_lookup(self) -> Dict[str, str]:
        """Build reverse lookup from sector keywords to canonical sector names"""
        lookup = {}
        for sector, keywords in self.SECTOR_KEYWORDS.items():
            for keyword in keywords:
                lookup[keyword.lower()] = sector
        return lookup

    def parse_query(self, query: str, user_id: str = "default") -> Dict[str, Any]:
        """
        Parse a natural language query and extract structured information

        Args:
            query: Natural language search query
            user_id: User identifier for context

        Returns:
            Dictionary with parsed query information:
            {
                "original_query": str,
                "intent": str,
                "confidence": float,
                "tickers": List[str],
                "patterns": List[str],
                "sectors": List[str],
                "price_filters": Dict,
                "timeframe": str,
                "comparison": bool,
                "suggestions": List[str]
            }
        """
        query_lower = query.lower().strip()

        # Extract components
        intent, confidence = self._classify_intent(query_lower)
        tickers = self._extract_tickers(query)
        patterns = self._extract_patterns(query_lower)
        sectors = self._extract_sectors(query_lower)
        price_filters = self._extract_price_filters(query_lower)
        timeframe = self._extract_timeframe(query_lower)

        # Determine if this is a comparison query
        is_comparison = self._is_comparison_query(query_lower) or len(tickers) > 1

        # Generate suggestions based on context
        suggestions = self._generate_suggestions(intent, patterns, sectors, tickers)

        result = {
            "original_query": query,
            "intent": intent,
            "confidence": confidence,
            "tickers": tickers,
            "patterns": patterns,
            "sectors": sectors,
            "price_filters": price_filters,
            "timeframe": timeframe or "daily",
            "comparison": is_comparison,
            "suggestions": suggestions,
            "parsed_at": datetime.utcnow().isoformat(),
        }

        logger.info(f"Parsed query: {query[:50]}... -> Intent: {intent} ({confidence:.2f}), "
                   f"Tickers: {tickers}, Patterns: {patterns}")

        return result

    def _classify_intent(self, query: str) -> Tuple[str, float]:
        """
        Classify the intent of the query

        Returns:
            Tuple of (intent_name, confidence_score)
        """
        scores = {}

        for intent, keywords in self.INTENT_KEYWORDS.items():
            score = 0
            for keyword in keywords:
                if keyword in query:
                    # Exact phrase match gets higher score
                    score += 10
                elif any(word in query.split() for word in keyword.split()):
                    # Individual word match gets lower score
                    score += 3
            scores[intent] = score

        if not scores or max(scores.values()) == 0:
            return "scan", 0.5  # Default intent

        best_intent = max(scores, key=scores.get)
        max_score = scores[best_intent]

        # Normalize confidence to 0-1 range
        confidence = min(max_score / 20, 1.0)

        return best_intent, confidence

    def _extract_tickers(self, query: str) -> List[str]:
        """
        Extract stock ticker symbols from query
        Uses pattern matching and fuzzy matching against known tickers
        """
        tickers = []

        # Pattern 1: All caps words 2-5 characters (likely tickers)
        caps_pattern = r'\b[A-Z]{2,5}\b'
        caps_matches = re.findall(caps_pattern, query)

        # Pattern 2: Dollar sign followed by ticker (e.g., $AAPL)
        dollar_pattern = r'\$([A-Z]{2,5})\b'
        dollar_matches = re.findall(dollar_pattern, query)

        # Pattern 3: Ticker with dot (e.g., BRK.B)
        dot_pattern = r'\b([A-Z]{2,4}\.[A-Z])\b'
        dot_matches = re.findall(dot_pattern, query)

        # Combine all matches
        potential_tickers = set(caps_matches + dollar_matches + dot_matches)

        # Fuzzy match against known tickers
        for potential in potential_tickers:
            # Direct match
            if potential in self.COMMON_TICKERS:
                tickers.append(potential)
            else:
                # Fuzzy match with high threshold
                match = process.extractOne(
                    potential,
                    self.COMMON_TICKERS,
                    scorer=fuzz.ratio,
                    score_cutoff=85
                )
                if match:
                    tickers.append(match[0])

        return list(set(tickers))  # Remove duplicates

    def _extract_patterns(self, query: str) -> List[str]:
        """
        Extract pattern names from query using fuzzy matching
        """
        patterns = []

        # Direct lookup
        for pattern_text, canonical in self._pattern_lookup.items():
            if pattern_text in query:
                if canonical not in patterns:
                    patterns.append(canonical)

        # Fuzzy matching for typos
        if not patterns:
            all_variations = list(self._pattern_lookup.keys())
            # Try to find fuzzy matches in chunks of the query
            words = query.split()
            for i in range(len(words)):
                for j in range(i + 1, min(i + 5, len(words) + 1)):
                    phrase = " ".join(words[i:j])
                    match = process.extractOne(
                        phrase,
                        all_variations,
                        scorer=fuzz.token_sort_ratio,
                        score_cutoff=80
                    )
                    if match:
                        canonical = self._pattern_lookup[match[0]]
                        if canonical not in patterns:
                            patterns.append(canonical)

        return patterns

    def _extract_sectors(self, query: str) -> List[str]:
        """Extract sector filters from query"""
        sectors = []

        for sector_keyword, canonical_sector in self._sector_lookup.items():
            if sector_keyword in query:
                if canonical_sector not in sectors:
                    sectors.append(canonical_sector)

        return sectors

    def _extract_price_filters(self, query: str) -> Dict[str, float]:
        """
        Extract price-related filters from query
        Examples: "above $100", "under 50", "between $20 and $30"
        """
        filters = {}

        # Pattern: "above/over/greater than $X"
        above_pattern = r'(?:above|over|greater than|>\s*)\$?(\d+(?:\.\d+)?)'
        above_match = re.search(above_pattern, query)
        if above_match:
            filters["min_price"] = float(above_match.group(1))

        # Pattern: "below/under/less than $X"
        below_pattern = r'(?:below|under|less than|<\s*)\$?(\d+(?:\.\d+)?)'
        below_match = re.search(below_pattern, query)
        if below_match:
            filters["max_price"] = float(below_match.group(1))

        # Pattern: "between $X and $Y"
        between_pattern = r'between\s+\$?(\d+(?:\.\d+)?)\s+and\s+\$?(\d+(?:\.\d+)?)'
        between_match = re.search(between_pattern, query)
        if between_match:
            filters["min_price"] = float(between_match.group(1))
            filters["max_price"] = float(between_match.group(2))

        # Pattern: "around/near $X"
        around_pattern = r'(?:around|near|approximately)\s+\$?(\d+(?:\.\d+)?)'
        around_match = re.search(around_pattern, query)
        if around_match:
            price = float(around_match.group(1))
            filters["min_price"] = price * 0.9  # 10% range
            filters["max_price"] = price * 1.1

        return filters

    def _extract_timeframe(self, query: str) -> Optional[str]:
        """Extract timeframe from query"""
        for timeframe, keywords in self.TIMEFRAME_KEYWORDS.items():
            for keyword in keywords:
                if keyword in query:
                    return timeframe
        return None

    def _is_comparison_query(self, query: str) -> bool:
        """Check if query is asking for comparison"""
        comparison_indicators = ["compare", "vs", "versus", "vs.", "difference between",
                                "better than", "or", "versus"]
        return any(indicator in query for indicator in comparison_indicators)

    def _generate_suggestions(
        self,
        intent: str,
        patterns: List[str],
        sectors: List[str],
        tickers: List[str]
    ) -> List[str]:
        """
        Generate contextual query suggestions based on parsed components
        """
        suggestions = []

        if intent == "scan":
            if patterns:
                suggestions.append(f"Show {patterns[0]} patterns in top stocks")
            if sectors:
                suggestions.append(f"Find breakouts in {sectors[0]} sector")
            suggestions.append("Show me today's best setups")
            suggestions.append("Which stocks are pulling back to support?")

        elif intent == "analyze":
            if tickers:
                suggestions.append(f"Show {tickers[0]} chart")
                suggestions.append(f"Compare {tickers[0]} to sector leaders")
            suggestions.append("Analyze recent breakouts")

        elif intent == "compare":
            if len(tickers) >= 2:
                suggestions.append(f"Which has better RS rating?")
                suggestions.append(f"Show charts side by side")
            suggestions.append("Compare FAANG stocks")

        elif intent == "watchlist":
            suggestions.append("Show my watchlist")
            suggestions.append("Add today's best setups to watchlist")

        # Add popular queries
        if not suggestions:
            suggestions = [
                "Find VCP patterns in tech stocks",
                "Show me breakouts above $100",
                "Which stocks are pulling back to 21 EMA?",
                "Compare AAPL and MSFT patterns",
            ]

        return suggestions[:5]  # Limit to 5 suggestions

    def correct_typos(self, query: str) -> str:
        """
        Auto-correct common typos in stock-related queries
        """
        corrections = {}

        # Check for pattern name typos
        words = query.lower().split()
        for i in range(len(words)):
            for j in range(i + 1, min(i + 4, len(words) + 1)):
                phrase = " ".join(words[i:j])
                all_patterns = list(self._pattern_lookup.keys())
                match = process.extractOne(
                    phrase,
                    all_patterns,
                    scorer=fuzz.ratio,
                    score_cutoff=75
                )
                if match and match[1] < 100:  # Not exact match
                    corrections[phrase] = match[0]

        corrected_query = query.lower()
        for typo, correction in corrections.items():
            corrected_query = corrected_query.replace(typo, correction)

        return corrected_query

    def autocomplete(self, partial_query: str, limit: int = 5) -> List[str]:
        """
        Provide autocomplete suggestions for partial queries
        """
        suggestions = []
        partial_lower = partial_query.lower()

        # Pattern name completions
        for pattern_text in self._pattern_lookup.keys():
            if pattern_text.startswith(partial_lower):
                canonical = self._pattern_lookup[pattern_text]
                suggestions.append(f"Find {pattern_text} patterns")

        # Ticker completions
        for ticker in self.COMMON_TICKERS:
            if ticker.lower().startswith(partial_lower):
                suggestions.append(f"Analyze {ticker}")

        # Sector completions
        for sector in self.SECTOR_KEYWORDS.keys():
            if sector.startswith(partial_lower):
                suggestions.append(f"Scan {sector} stocks")

        # Common query templates
        templates = [
            "Find VCP patterns in tech stocks",
            "Show me breakouts above $100",
            "Which stocks are pulling back to 21 EMA?",
            "Compare AAPL and MSFT",
            "Analyze NVDA daily chart",
            "Show top setups today",
        ]

        for template in templates:
            if template.lower().startswith(partial_lower):
                suggestions.append(template)

        return suggestions[:limit]

    def get_query_type(self, parsed_query: Dict[str, Any]) -> str:
        """
        Determine the type of query based on parsed components
        """
        if parsed_query["comparison"]:
            return "comparison"
        elif parsed_query["tickers"]:
            return "ticker"
        elif parsed_query["patterns"]:
            return "pattern"
        elif parsed_query["intent"] == "market":
            return "market"
        else:
            return "general"
