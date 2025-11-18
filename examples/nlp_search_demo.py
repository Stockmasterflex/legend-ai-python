"""
NLP Search Demo
Demonstrates all features of the NLP-based stock search system
"""

import asyncio
import httpx
import json
from pathlib import Path


BASE_URL = "http://localhost:8000"
USER_ID = "demo_user"


class NLPSearchDemo:
    """Demo class for NLP Search features"""

    def __init__(self, base_url: str = BASE_URL):
        self.base_url = base_url
        self.client = httpx.AsyncClient(base_url=base_url, timeout=30.0)

    async def close(self):
        """Close the HTTP client"""
        await self.client.aclose()

    def print_section(self, title: str):
        """Print a formatted section header"""
        print("\n" + "=" * 70)
        print(f"  {title}")
        print("=" * 70 + "\n")

    async def demo_basic_search(self):
        """Demo 1: Basic natural language search"""
        self.print_section("Demo 1: Basic Natural Language Search")

        queries = [
            "Find VCP patterns in tech stocks",
            "Show me breakouts above $100",
            "Which stocks are pulling back to 21 EMA?",
            "Compare AAPL and MSFT patterns",
        ]

        for query in queries:
            print(f"Query: {query}")

            response = await self.client.post(
                "/api/nlp/search",
                json={
                    "query": query,
                    "user_id": USER_ID,
                    "execute_search": False,  # Just parse, don't execute
                    "save_history": True
                }
            )

            if response.status_code == 200:
                result = response.json()
                print(f"  Intent: {result['intent']} (confidence: {result['confidence']:.2f})")
                print(f"  Tickers: {result['tickers']}")
                print(f"  Patterns: {result['patterns']}")
                print(f"  Sectors: {result['sectors']}")
                print(f"  Price Filters: {result['price_filters']}")
                print(f"  Timeframe: {result['timeframe']}")
                print(f"  Comparison: {result['comparison']}")
                print()
            else:
                print(f"  Error: {response.status_code}")
                print()

    async def demo_price_filters(self):
        """Demo 2: Price filter extraction"""
        self.print_section("Demo 2: Price Filter Extraction")

        queries = [
            "Find stocks above $100",
            "Show me stocks under $50",
            "Stocks between $20 and $30",
            "Find patterns around $75",
        ]

        for query in queries:
            print(f"Query: {query}")

            response = await self.client.post(
                "/api/nlp/search",
                json={
                    "query": query,
                    "user_id": USER_ID,
                    "execute_search": False
                }
            )

            if response.status_code == 200:
                result = response.json()
                filters = result['price_filters']
                print(f"  Extracted filters: {filters}")
                if 'min_price' in filters and 'max_price' in filters:
                    print(f"  Range: ${filters['min_price']:.2f} - ${filters['max_price']:.2f}")
                elif 'min_price' in filters:
                    print(f"  Minimum: ${filters['min_price']:.2f}")
                elif 'max_price' in filters:
                    print(f"  Maximum: ${filters['max_price']:.2f}")
                print()

    async def demo_autocomplete(self):
        """Demo 3: Autocomplete suggestions"""
        self.print_section("Demo 3: Autocomplete")

        partial_queries = [
            "find",
            "find vcp",
            "compare",
            "analyze",
        ]

        for partial in partial_queries:
            print(f"Partial query: '{partial}'")

            response = await self.client.get(
                "/api/nlp/autocomplete",
                params={"query": partial, "limit": 3}
            )

            if response.status_code == 200:
                result = response.json()
                suggestions = result['suggestions']
                for i, suggestion in enumerate(suggestions, 1):
                    print(f"  {i}. {suggestion}")
                print()

    async def demo_typo_correction(self):
        """Demo 4: Typo correction"""
        self.print_section("Demo 4: Typo Correction")

        queries_with_typos = [
            "find cupp and handl patern",
            "show me hed and shulders",
            "dobble botom patterns",
        ]

        for query in queries_with_typos:
            print(f"Original: {query}")

            response = await self.client.post(
                "/api/nlp/correct",
                json={"query": query}
            )

            if response.status_code == 200:
                result = response.json()
                print(f"Corrected: {result['corrected']}")
                print(f"Changed: {result['changed']}")
                print()

    async def demo_search_history(self):
        """Demo 5: Search history"""
        self.print_section("Demo 5: Search History")

        # Get recent searches
        response = await self.client.get(
            "/api/nlp/history",
            params={"user_id": USER_ID, "limit": 5}
        )

        if response.status_code == 200:
            history = response.json()
            print(f"Found {len(history)} recent searches:\n")

            for i, search in enumerate(history, 1):
                print(f"{i}. {search['query']}")
                print(f"   Intent: {search['intent']} | "
                      f"Confidence: {search['confidence']:.2f} | "
                      f"Results: {search['results_count']}")
                print(f"   Date: {search['created_at']}")
                print()

    async def demo_analytics(self):
        """Demo 6: Search analytics"""
        self.print_section("Demo 6: Search Analytics")

        response = await self.client.get(
            "/api/nlp/analytics",
            params={"user_id": USER_ID, "days": 30}
        )

        if response.status_code == 200:
            analytics = response.json()

            print(f"Search Analytics (Last {analytics['period_days']} days)")
            print(f"\nTotal Searches: {analytics['total_searches']}")
            print(f"  - Voice: {analytics['voice_searches']}")
            print(f"  - Text: {analytics['text_searches']}")

            print(f"\nIntent Distribution:")
            for intent, count in analytics['intent_distribution'].items():
                print(f"  - {intent}: {count}")

            print(f"\nTop Tickers:")
            for ticker, count in list(analytics['top_tickers'].items())[:5]:
                print(f"  - {ticker}: {count}")

            print(f"\nTop Patterns:")
            for pattern, count in list(analytics['top_patterns'].items())[:5]:
                print(f"  - {pattern}: {count}")

            print(f"\nAverages:")
            print(f"  - Confidence: {analytics['avg_confidence']:.2f}")
            print(f"  - Results per query: {analytics['avg_results_per_query']:.1f}")
            print(f"  - Execution time: {analytics['avg_execution_time']:.3f}s")
            print()

    async def demo_suggestions(self):
        """Demo 7: Contextual suggestions"""
        self.print_section("Demo 7: Contextual Suggestions")

        response = await self.client.get(
            "/api/nlp/suggestions",
            params={"user_id": USER_ID, "limit": 5}
        )

        if response.status_code == 200:
            result = response.json()
            suggestions = result['suggestions']

            print("Personalized suggestions based on your search history:\n")
            for i, suggestion in enumerate(suggestions, 1):
                print(f"{i}. {suggestion}")
            print()

    async def demo_popular_queries(self):
        """Demo 8: Popular queries"""
        self.print_section("Demo 8: Popular Queries")

        response = await self.client.get(
            "/api/nlp/history/popular",
            params={"limit": 10, "days": 7}
        )

        if response.status_code == 200:
            result = response.json()
            popular = result['popular_queries']

            print(f"Most popular queries (Last 7 days):\n")
            for i, query in enumerate(popular, 1):
                print(f"{i}. {query['query']}")
                print(f"   Used {query['usage_count']} times | "
                      f"Avg results: {query['avg_results']:.1f} | "
                      f"Intent: {query['intent']}")
                print()

    async def demo_complex_queries(self):
        """Demo 9: Complex multi-criteria queries"""
        self.print_section("Demo 9: Complex Multi-Criteria Queries")

        complex_queries = [
            "Find cup and handle patterns in healthcare stocks between $50 and $150 on the weekly chart",
            "Show me tech stocks breaking out above $100 with high RS rating",
            "Which financial stocks are forming VCP patterns near their 50 day moving average",
        ]

        for query in complex_queries:
            print(f"Query: {query}\n")

            response = await self.client.post(
                "/api/nlp/search",
                json={
                    "query": query,
                    "user_id": USER_ID,
                    "execute_search": False
                }
            )

            if response.status_code == 200:
                result = response.json()
                print(f"Parsed components:")
                print(f"  Intent: {result['intent']}")
                print(f"  Patterns: {result['patterns']}")
                print(f"  Sectors: {result['sectors']}")
                print(f"  Price range: {result['price_filters']}")
                print(f"  Timeframe: {result['timeframe']}")
                print(f"  Confidence: {result['confidence']:.2f}")
                print()

    async def demo_supported_languages(self):
        """Demo 10: Supported languages for voice"""
        self.print_section("Demo 10: Supported Languages for Voice Search")

        response = await self.client.get("/api/nlp/voice/languages")

        if response.status_code == 200:
            result = response.json()
            languages = result['languages']

            print("Supported languages for voice search:\n")
            for code, name in languages.items():
                print(f"  {code}: {name}")
            print()

    async def run_all_demos(self):
        """Run all demos in sequence"""
        print("\n" + "=" * 70)
        print("  NLP SEARCH SYSTEM - COMPREHENSIVE DEMO")
        print("=" * 70)

        try:
            await self.demo_basic_search()
            await self.demo_price_filters()
            await self.demo_autocomplete()
            await self.demo_typo_correction()
            await self.demo_complex_queries()
            await self.demo_search_history()
            await self.demo_analytics()
            await self.demo_suggestions()
            await self.demo_popular_queries()
            await self.demo_supported_languages()

            print("\n" + "=" * 70)
            print("  DEMO COMPLETE!")
            print("=" * 70 + "\n")

        except Exception as e:
            print(f"\n❌ Error during demo: {str(e)}")
            import traceback
            traceback.print_exc()

        finally:
            await self.close()


async def main():
    """Main entry point"""
    demo = NLPSearchDemo()

    print("\nStarting NLP Search Demo...")
    print(f"Base URL: {BASE_URL}")
    print(f"User ID: {USER_ID}\n")

    # Check if server is running
    try:
        response = await demo.client.get("/health")
        if response.status_code != 200:
            print("❌ Server is not responding properly.")
            print(f"Health check returned: {response.status_code}")
            await demo.close()
            return
    except Exception as e:
        print(f"❌ Cannot connect to server at {BASE_URL}")
        print(f"Error: {str(e)}")
        print("\nMake sure the server is running:")
        print("  uvicorn app.main:app --reload")
        await demo.close()
        return

    print("✅ Server is running!\n")

    # Run all demos
    await demo.run_all_demos()


if __name__ == "__main__":
    asyncio.run(main())
