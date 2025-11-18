"""
Visualization Service
Helper utilities for generating charts, pie charts, and correlation matrices
"""

from typing import List, Dict, Optional
import json


class VisualizationService:
    """Service for generating visualization data"""

    @staticmethod
    def generate_pie_chart_data(labels: List[str], values: List[float], colors: Optional[List[str]] = None) -> Dict:
        """
        Generate data for pie chart visualization

        Args:
            labels: List of labels (e.g., stock symbols)
            values: List of values (e.g., position values)
            colors: Optional list of colors

        Returns:
            Chart.js compatible pie chart data
        """
        if not colors:
            # Default color palette
            colors = [
                '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF',
                '#FF9F40', '#FF6384', '#C9CBCF', '#4BC0C0', '#FF6384'
            ]

        total = sum(values)
        percentages = [(v / total * 100) if total > 0 else 0 for v in values]

        return {
            "type": "pie",
            "data": {
                "labels": labels,
                "datasets": [{
                    "data": values,
                    "backgroundColor": colors[:len(labels)],
                    "borderWidth": 2,
                    "borderColor": "#fff"
                }]
            },
            "options": {
                "responsive": True,
                "plugins": {
                    "legend": {
                        "position": "right"
                    },
                    "tooltip": {
                        "callbacks": {
                            "label": "function(context) { return context.label + ': $' + context.parsed.toFixed(2) + ' (' + context.dataset.percentages[context.dataIndex].toFixed(1) + '%)'; }"
                        }
                    }
                }
            },
            "percentages": percentages
        }

    @staticmethod
    def generate_correlation_heatmap(symbols: List[str], correlation_matrix: List[List[float]]) -> Dict:
        """
        Generate correlation heatmap data

        Args:
            symbols: List of stock symbols
            correlation_matrix: NxN correlation matrix

        Returns:
            Heatmap visualization data
        """
        # Convert correlation matrix to heatmap format
        heatmap_data = []
        for i, row in enumerate(correlation_matrix):
            for j, value in enumerate(row):
                heatmap_data.append({
                    "x": symbols[j],
                    "y": symbols[i],
                    "value": round(value, 3),
                    "color": VisualizationService._get_correlation_color(value)
                })

        return {
            "type": "heatmap",
            "symbols": symbols,
            "data": heatmap_data,
            "matrix": correlation_matrix,
            "colorScale": {
                "-1.0": "#d73027",  # Strong negative correlation (red)
                "-0.5": "#fc8d59",  # Moderate negative
                "0.0": "#ffffbf",   # No correlation (yellow)
                "0.5": "#91bfdb",   # Moderate positive
                "1.0": "#4575b4"    # Strong positive correlation (blue)
            }
        }

    @staticmethod
    def _get_correlation_color(value: float) -> str:
        """Get color for correlation value"""
        if value >= 0.7:
            return "#4575b4"  # Strong positive (blue)
        elif value >= 0.3:
            return "#91bfdb"  # Moderate positive
        elif value >= -0.3:
            return "#ffffbf"  # Neutral (yellow)
        elif value >= -0.7:
            return "#fc8d59"  # Moderate negative
        else:
            return "#d73027"  # Strong negative (red)

    @staticmethod
    def generate_performance_chart(dates: List[str], values: List[float], benchmark_values: Optional[List[float]] = None) -> Dict:
        """
        Generate performance line chart

        Args:
            dates: List of dates
            values: Portfolio values
            benchmark_values: Optional benchmark values for comparison

        Returns:
            Line chart data
        """
        datasets = [{
            "label": "Portfolio",
            "data": values,
            "borderColor": "#4BC0C0",
            "backgroundColor": "rgba(75, 192, 192, 0.2)",
            "tension": 0.4,
            "fill": True
        }]

        if benchmark_values:
            datasets.append({
                "label": "Benchmark (SPY)",
                "data": benchmark_values,
                "borderColor": "#FF6384",
                "backgroundColor": "rgba(255, 99, 132, 0.2)",
                "tension": 0.4,
                "fill": True
            })

        return {
            "type": "line",
            "data": {
                "labels": dates,
                "datasets": datasets
            },
            "options": {
                "responsive": True,
                "plugins": {
                    "legend": {
                        "display": True,
                        "position": "top"
                    },
                    "title": {
                        "display": True,
                        "text": "Portfolio Performance"
                    }
                },
                "scales": {
                    "y": {
                        "beginAtZero": False,
                        "title": {
                            "display": True,
                            "text": "Value ($)"
                        }
                    },
                    "x": {
                        "title": {
                            "display": True,
                            "text": "Date"
                        }
                    }
                }
            }
        }

    @staticmethod
    def generate_bar_chart(labels: List[str], values: List[float], title: str = "Performance") -> Dict:
        """
        Generate bar chart for performance comparison

        Args:
            labels: Bar labels (e.g., stock symbols)
            values: Values (e.g., returns)
            title: Chart title

        Returns:
            Bar chart data
        """
        # Color bars based on positive/negative values
        colors = ['#4BC0C0' if v >= 0 else '#FF6384' for v in values]

        return {
            "type": "bar",
            "data": {
                "labels": labels,
                "datasets": [{
                    "label": title,
                    "data": values,
                    "backgroundColor": colors,
                    "borderColor": colors,
                    "borderWidth": 1
                }]
            },
            "options": {
                "responsive": True,
                "plugins": {
                    "legend": {
                        "display": False
                    },
                    "title": {
                        "display": True,
                        "text": title
                    }
                },
                "scales": {
                    "y": {
                        "beginAtZero": True,
                        "title": {
                            "display": True,
                            "text": "Return (%)"
                        }
                    }
                }
            }
        }

    @staticmethod
    def generate_diversification_gauge(score: int, grade: str) -> Dict:
        """
        Generate gauge chart for diversification score

        Args:
            score: Diversification score (0-100)
            grade: Letter grade

        Returns:
            Gauge chart data
        """
        # Determine color based on score
        if score >= 80:
            color = "#4BC0C0"  # Excellent (teal)
        elif score >= 60:
            color = "#FFCE56"  # Good (yellow)
        else:
            color = "#FF6384"  # Needs improvement (red)

        return {
            "type": "gauge",
            "score": score,
            "grade": grade,
            "color": color,
            "data": {
                "value": score,
                "max": 100,
                "label": f"Diversification: {grade}",
                "color": color
            },
            "ranges": [
                {"min": 0, "max": 50, "color": "#FF6384", "label": "Poor"},
                {"min": 50, "max": 70, "color": "#FFCE56", "label": "Fair"},
                {"min": 70, "max": 85, "color": "#4BC0C0", "label": "Good"},
                {"min": 85, "max": 100, "color": "#36A2EB", "label": "Excellent"}
            ]
        }
