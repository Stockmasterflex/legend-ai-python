"""
Pattern recognition training and quiz system
Educational tool for learning to identify chart patterns
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import random
import json
import pandas as pd

from app.models import PatternQuiz, QuizAttempt, Ticker
from app.services.database import DatabaseService
from app.services.market_data import MarketDataService
from app.core.detector_factory import DetectorFactory


class PatternTrainingEngine:
    """
    Pattern recognition training with quiz mode and score tracking
    """

    # Pattern types for quizzes
    PATTERN_TYPES = [
        "VCP",
        "Cup & Handle",
        "Triangle",
        "Channel",
        "Wedge",
        "Head & Shoulders",
        "Double Top",
        "Double Bottom",
        "SMA50 Pullback"
    ]

    DIFFICULTY_LEVELS = {
        "easy": {
            "bars": 50,
            "clear_patterns": True,
            "options_count": 3
        },
        "medium": {
            "bars": 100,
            "clear_patterns": True,
            "options_count": 5
        },
        "hard": {
            "bars": 200,
            "clear_patterns": False,
            "options_count": 7
        }
    }

    def __init__(
        self,
        db_service: DatabaseService,
        market_data_service: MarketDataService,
        detector_factory: DetectorFactory
    ):
        self.db = db_service
        self.market_data = market_data_service
        self.detector_factory = detector_factory

    async def generate_quiz(
        self,
        ticker_symbol: Optional[str] = None,
        difficulty: str = "medium",
        pattern_type: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate a pattern recognition quiz

        Args:
            ticker_symbol: Optional specific ticker (random if None)
            difficulty: "easy", "medium", or "hard"
            pattern_type: Optional specific pattern to quiz on

        Returns:
            Quiz data with question and options
        """
        if difficulty not in self.DIFFICULTY_LEVELS:
            raise ValueError(f"Invalid difficulty. Must be one of: {list(self.DIFFICULTY_LEVELS.keys())}")

        # Select ticker
        if not ticker_symbol:
            ticker_symbol = await self._get_random_ticker()

        # Select date range
        quiz_date = await self._get_random_date_with_pattern(ticker_symbol, pattern_type)

        # Fetch historical data
        bars = self.DIFFICULTY_LEVELS[difficulty]["bars"]
        data = await self._fetch_quiz_data(ticker_symbol, quiz_date, bars)

        # Detect actual pattern
        if pattern_type:
            actual_pattern = pattern_type
        else:
            actual_pattern = await self._detect_pattern_in_data(ticker_symbol, data)

        if not actual_pattern:
            actual_pattern = random.choice(self.PATTERN_TYPES)

        # Generate answer options
        options_count = self.DIFFICULTY_LEVELS[difficulty]["options_count"]
        answer_options = self._generate_answer_options(actual_pattern, options_count)

        # Create quiz question
        question = self._generate_question(ticker_symbol, difficulty)

        # Save quiz to database
        with self.db.get_db() as session:
            ticker = session.query(Ticker).filter(Ticker.symbol == ticker_symbol.upper()).first()
            if not ticker:
                ticker = Ticker(symbol=ticker_symbol.upper(), name=ticker_symbol.upper())
                session.add(ticker)
                session.flush()

            quiz = PatternQuiz(
                ticker_id=ticker.id,
                quiz_date=quiz_date,
                pattern_type=actual_pattern,
                difficulty=difficulty,
                question=question,
                correct_answer=actual_pattern,
                answer_options=json.dumps(answer_options),
                explanation=self._get_pattern_explanation(actual_pattern),
                chart_data=json.dumps({
                    'timestamps': data['timestamp'].dt.strftime('%Y-%m-%d').tolist(),
                    'open': data['open'].tolist(),
                    'high': data['high'].tolist(),
                    'low': data['low'].tolist(),
                    'close': data['close'].tolist(),
                    'volume': data['volume'].tolist()
                })
            )
            session.add(quiz)
            session.commit()
            session.refresh(quiz)

            return {
                "quiz_id": quiz.id,
                "ticker": ticker_symbol,
                "difficulty": difficulty,
                "question": question,
                "options": answer_options,
                "chart_data": {
                    'timestamps': data['timestamp'].dt.strftime('%Y-%m-%d').tolist(),
                    'open': data['open'].tolist(),
                    'high': data['high'].tolist(),
                    'low': data['low'].tolist(),
                    'close': data['close'].tolist(),
                    'volume': data['volume'].tolist()
                },
                "bars_shown": len(data)
            }

    async def submit_answer(
        self,
        quiz_id: int,
        user_id: str,
        user_answer: str,
        time_taken_seconds: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Submit and grade a quiz answer

        Args:
            quiz_id: Quiz ID
            user_id: User identifier
            user_answer: User's answer
            time_taken_seconds: Time taken to answer

        Returns:
            Results with correct answer and explanation
        """
        with self.db.get_db() as session:
            quiz = session.get(PatternQuiz, quiz_id)
            if not quiz:
                raise ValueError(f"Quiz {quiz_id} not found")

            is_correct = user_answer.lower() == quiz.correct_answer.lower()

            # Calculate score (100 points for correct, bonus for speed)
            score = 100.0 if is_correct else 0.0

            if is_correct and time_taken_seconds:
                # Bonus points for quick answers (up to 20 points)
                if time_taken_seconds < 10:
                    score += 20
                elif time_taken_seconds < 20:
                    score += 15
                elif time_taken_seconds < 30:
                    score += 10
                elif time_taken_seconds < 60:
                    score += 5

            # Save attempt
            attempt = QuizAttempt(
                quiz_id=quiz_id,
                user_id=user_id,
                user_answer=user_answer,
                is_correct=is_correct,
                time_taken_seconds=time_taken_seconds,
                score=score
            )
            session.add(attempt)
            session.commit()
            session.refresh(attempt)

            return {
                "attempt_id": attempt.id,
                "quiz_id": quiz_id,
                "is_correct": is_correct,
                "correct_answer": quiz.correct_answer,
                "user_answer": user_answer,
                "score": score,
                "time_taken_seconds": time_taken_seconds,
                "explanation": quiz.explanation,
                "feedback": self._get_feedback(is_correct, quiz.difficulty)
            }

    async def get_user_stats(self, user_id: str) -> Dict[str, Any]:
        """
        Get training statistics for a user

        Args:
            user_id: User identifier

        Returns:
            Comprehensive statistics
        """
        with self.db.get_db() as session:
            attempts = session.query(QuizAttempt).filter(
                QuizAttempt.user_id == user_id
            ).all()

            if not attempts:
                return {
                    "user_id": user_id,
                    "total_attempts": 0,
                    "message": "No quiz attempts yet"
                }

            # Overall stats
            total_attempts = len(attempts)
            correct_attempts = sum(1 for a in attempts if a.is_correct)
            accuracy = (correct_attempts / total_attempts) * 100

            total_score = sum(a.score for a in attempts)
            avg_score = total_score / total_attempts

            # Time stats
            timed_attempts = [a for a in attempts if a.time_taken_seconds]
            avg_time = sum(a.time_taken_seconds for a in timed_attempts) / len(timed_attempts) if timed_attempts else None

            # Pattern-specific stats
            pattern_stats = {}
            for attempt in attempts:
                quiz = session.get(PatternQuiz, attempt.quiz_id)
                if quiz:
                    pattern = quiz.pattern_type
                    if pattern not in pattern_stats:
                        pattern_stats[pattern] = {"total": 0, "correct": 0}
                    pattern_stats[pattern]["total"] += 1
                    if attempt.is_correct:
                        pattern_stats[pattern]["correct"] += 1

            # Calculate per-pattern accuracy
            for pattern in pattern_stats:
                total = pattern_stats[pattern]["total"]
                correct = pattern_stats[pattern]["correct"]
                pattern_stats[pattern]["accuracy"] = (correct / total) * 100

            # Difficulty stats
            difficulty_stats = {}
            for attempt in attempts:
                quiz = session.get(PatternQuiz, attempt.quiz_id)
                if quiz:
                    diff = quiz.difficulty
                    if diff not in difficulty_stats:
                        difficulty_stats[diff] = {"total": 0, "correct": 0}
                    difficulty_stats[diff]["total"] += 1
                    if attempt.is_correct:
                        difficulty_stats[diff]["correct"] += 1

            # Recent performance (last 10)
            recent_attempts = sorted(attempts, key=lambda a: a.attempted_at, reverse=True)[:10]
            recent_accuracy = (sum(1 for a in recent_attempts if a.is_correct) / len(recent_attempts)) * 100

            # Streaks
            current_streak = self._calculate_current_streak(attempts)
            best_streak = self._calculate_best_streak(attempts)

            return {
                "user_id": user_id,
                "total_attempts": total_attempts,
                "correct_attempts": correct_attempts,
                "accuracy": accuracy,
                "average_score": avg_score,
                "average_time_seconds": avg_time,
                "pattern_stats": pattern_stats,
                "difficulty_stats": difficulty_stats,
                "recent_accuracy": recent_accuracy,
                "current_streak": current_streak,
                "best_streak": best_streak,
                "strengths": self._identify_strengths(pattern_stats),
                "weaknesses": self._identify_weaknesses(pattern_stats)
            }

    async def get_leaderboard(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get top performers leaderboard"""
        with self.db.get_db() as session:
            # Get all users with attempts
            attempts = session.query(QuizAttempt).all()

            user_scores = {}
            for attempt in attempts:
                user_id = attempt.user_id
                if user_id not in user_scores:
                    user_scores[user_id] = {
                        "total_score": 0,
                        "attempts": 0,
                        "correct": 0
                    }
                user_scores[user_id]["total_score"] += attempt.score
                user_scores[user_id]["attempts"] += 1
                if attempt.is_correct:
                    user_scores[user_id]["correct"] += 1

            # Calculate averages and sort
            leaderboard = []
            for user_id, stats in user_scores.items():
                avg_score = stats["total_score"] / stats["attempts"]
                accuracy = (stats["correct"] / stats["attempts"]) * 100
                leaderboard.append({
                    "user_id": user_id,
                    "average_score": avg_score,
                    "total_attempts": stats["attempts"],
                    "accuracy": accuracy,
                    "total_score": stats["total_score"]
                })

            # Sort by average score
            leaderboard.sort(key=lambda x: x["average_score"], reverse=True)

            return leaderboard[:limit]

    async def get_practice_recommendations(self, user_id: str) -> List[str]:
        """Get personalized practice recommendations"""
        stats = await self.get_user_stats(user_id)

        if stats.get("total_attempts", 0) == 0:
            return [
                "Start with easy difficulty quizzes",
                "Focus on common patterns like VCP and Cup & Handle",
                "Take your time to study each chart carefully"
            ]

        recommendations = []

        # Recommend based on weaknesses
        if "weaknesses" in stats and stats["weaknesses"]:
            for pattern in stats["weaknesses"][:2]:
                recommendations.append(f"Practice identifying {pattern} patterns")

        # Recommend difficulty adjustment
        if "difficulty_stats" in stats:
            for diff, data in stats["difficulty_stats"].items():
                if data["total"] >= 5:
                    accuracy = (data["correct"] / data["total"]) * 100
                    if accuracy > 80 and diff == "easy":
                        recommendations.append("Try moving up to medium difficulty")
                    elif accuracy > 80 and diff == "medium":
                        recommendations.append("Challenge yourself with hard difficulty")
                    elif accuracy < 50:
                        recommendations.append(f"Practice more {diff} level quizzes before advancing")

        # Recommend based on accuracy
        if stats.get("accuracy", 0) < 60:
            recommendations.append("Review pattern characteristics before each quiz")

        if not recommendations:
            recommendations.append("Keep up the great work! Try harder difficulty levels")

        return recommendations[:5]

    # Helper methods

    async def _get_random_ticker(self) -> str:
        """Get a random ticker from the database"""
        with self.db.get_db() as session:
            # Get random ticker
            tickers = session.query(Ticker).limit(100).all()
            if tickers:
                return random.choice(tickers).symbol
            else:
                # Fallback to common tickers
                return random.choice(["AAPL", "MSFT", "GOOGL", "TSLA", "NVDA"])

    async def _get_random_date_with_pattern(
        self,
        ticker: str,
        pattern_type: Optional[str] = None
    ) -> datetime:
        """Get a random historical date (simplified)"""
        # For quiz purposes, use dates from 6 months to 2 years ago
        days_ago = random.randint(180, 730)
        return datetime.utcnow() - timedelta(days=days_ago)

    async def _fetch_quiz_data(
        self,
        ticker: str,
        quiz_date: datetime,
        bars: int
    ) -> pd.DataFrame:
        """Fetch historical data for quiz"""
        data = await self.market_data.get_time_series(
            ticker=ticker,
            interval="1day",
            outputsize=bars + 50
        )

        df = pd.DataFrame({
            'timestamp': pd.to_datetime(data['t'], unit='s'),
            'open': data['o'],
            'high': data['h'],
            'low': data['l'],
            'close': data['c'],
            'volume': data['v']
        })

        # Filter around quiz date
        df = df[df['timestamp'] <= quiz_date]
        df = df.tail(bars).reset_index(drop=True)

        return df

    async def _detect_pattern_in_data(self, ticker: str, data: pd.DataFrame) -> Optional[str]:
        """Attempt to detect pattern in data (simplified)"""
        # This would use the actual detector factory in production
        # For now, return random pattern
        return random.choice(self.PATTERN_TYPES)

    def _generate_answer_options(self, correct_answer: str, count: int) -> List[str]:
        """Generate answer options including the correct one"""
        options = [correct_answer]

        # Add wrong answers
        other_patterns = [p for p in self.PATTERN_TYPES if p != correct_answer]
        random.shuffle(other_patterns)
        options.extend(other_patterns[:count - 1])

        # Shuffle final options
        random.shuffle(options)

        return options

    def _generate_question(self, ticker: str, difficulty: str) -> str:
        """Generate quiz question"""
        questions = [
            f"What chart pattern is forming in {ticker}?",
            f"Identify the primary pattern in this {ticker} chart:",
            f"Which pattern best describes the price action in {ticker}?",
            f"What setup is {ticker} showing?"
        ]
        return random.choice(questions)

    def _get_pattern_explanation(self, pattern: str) -> str:
        """Get explanation for a pattern"""
        explanations = {
            "VCP": "Volatility Contraction Pattern (VCP) shows a series of contractions with declining volatility, indicating consolidation before a potential breakout.",
            "Cup & Handle": "Cup and Handle pattern shows a rounded bottom (cup) followed by a small consolidation (handle) before breakout.",
            "Triangle": "Triangle patterns show converging trendlines indicating consolidation and potential breakout direction.",
            "Channel": "Channel patterns show price moving between parallel support and resistance lines.",
            "Wedge": "Wedge patterns show converging trendlines with narrowing price action, signaling potential reversal.",
            "Head & Shoulders": "Head and Shoulders is a reversal pattern with three peaks, the middle one being highest.",
            "Double Top": "Double Top is a bearish reversal pattern with two peaks at similar levels.",
            "Double Bottom": "Double Bottom is a bullish reversal pattern with two troughs at similar levels.",
            "SMA50 Pullback": "SMA50 Pullback shows price pulling back to the 50-day moving average in an uptrend, offering entry opportunity."
        }
        return explanations.get(pattern, "Classic chart pattern used in technical analysis.")

    def _get_feedback(self, is_correct: bool, difficulty: str) -> str:
        """Generate feedback message"""
        if is_correct:
            messages = [
                "Excellent! You correctly identified the pattern.",
                "Great job! Your pattern recognition skills are improving.",
                "Correct! Keep up the good work.",
                "Well done! You nailed it."
            ]
        else:
            messages = [
                "Not quite. Review the explanation and try again.",
                "Incorrect. Study the pattern characteristics more closely.",
                "That's not the right pattern. Check the explanation to learn more.",
                "Keep practicing! Pattern recognition improves with experience."
            ]
        return random.choice(messages)

    def _calculate_current_streak(self, attempts: List[QuizAttempt]) -> int:
        """Calculate current streak of correct answers"""
        if not attempts:
            return 0

        sorted_attempts = sorted(attempts, key=lambda a: a.attempted_at, reverse=True)
        streak = 0

        for attempt in sorted_attempts:
            if attempt.is_correct:
                streak += 1
            else:
                break

        return streak

    def _calculate_best_streak(self, attempts: List[QuizAttempt]) -> int:
        """Calculate best streak of correct answers"""
        if not attempts:
            return 0

        sorted_attempts = sorted(attempts, key=lambda a: a.attempted_at)
        max_streak = 0
        current_streak = 0

        for attempt in sorted_attempts:
            if attempt.is_correct:
                current_streak += 1
                max_streak = max(max_streak, current_streak)
            else:
                current_streak = 0

        return max_streak

    def _identify_strengths(self, pattern_stats: Dict) -> List[str]:
        """Identify patterns user is good at"""
        strengths = []
        for pattern, stats in pattern_stats.items():
            if stats["total"] >= 3 and stats["accuracy"] >= 80:
                strengths.append(pattern)
        return strengths

    def _identify_weaknesses(self, pattern_stats: Dict) -> List[str]:
        """Identify patterns user needs to practice"""
        weaknesses = []
        for pattern, stats in pattern_stats.items():
            if stats["total"] >= 3 and stats["accuracy"] < 60:
                weaknesses.append(pattern)
        return weaknesses
