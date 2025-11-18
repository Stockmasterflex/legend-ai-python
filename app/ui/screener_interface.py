"""
Gradio UI Interface for Advanced Stock Screener

Provides a web interface for:
- Running custom screens
- Using pre-built templates
- Viewing and exporting results
- Managing saved screens
"""
import gradio as gr
import pandas as pd
import asyncio
from typing import List, Dict, Any

from app.services.advanced_screener import FilterCriteria, advanced_screener_service
from app.services.screen_templates import screen_templates
from app.services.saved_screen_service import get_saved_screen_service


def run_template_screen(template_name: str, limit: int = 50) -> pd.DataFrame:
    """Run a pre-built template screen"""
    try:
        # Map display name to template type
        template_map = {
            "Minervini SEPA": "MINERVINI_SEPA",
            "O'Neil CAN SLIM": "CANSLIM",
            "Momentum Leaders": "MOMENTUM_LEADERS",
            "Breakout Candidates": "BREAKOUT_CANDIDATES",
            "Gap-Up Today": "GAP_UP_TODAY",
            "High Tight Flag": "HIGH_TIGHT_FLAG",
            "Pullback to Support": "PULLBACK_TO_SUPPORT",
            "Pocket Pivot": "POCKET_PIVOT",
            "Strong Foundation": "STRONG_FOUNDATION",
            "Post-IPO Base": "POST_IPO_BASE",
        }

        template_type = template_map.get(template_name)
        if not template_type:
            return pd.DataFrame({"Error": ["Invalid template selected"]})

        # Get criteria
        criteria = screen_templates.get_template(template_type)

        # Run screen
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        results = loop.run_until_complete(
            advanced_screener_service.run_screen(
                filter_criteria=criteria,
                limit=limit
            )
        )
        loop.close()

        # Convert to DataFrame
        if results.get("results"):
            df = pd.DataFrame(results["results"])
            df = df[["symbol", "name", "sector", "price", "volume", "rs_rating", "score"]]
            return df
        else:
            return pd.DataFrame({"Message": ["No matches found"]})

    except Exception as e:
        return pd.DataFrame({"Error": [str(e)]})


def run_custom_screen(
    min_price: float = None,
    max_price: float = None,
    min_volume: float = None,
    min_rs_rating: float = None,
    above_sma_50: bool = False,
    above_sma_200: bool = False,
    minervini_template: bool = False,
    limit: int = 50
) -> pd.DataFrame:
    """Run a custom screen with user-specified criteria"""
    try:
        # Build criteria
        criteria = FilterCriteria(
            min_price=min_price if min_price and min_price > 0 else None,
            max_price=max_price if max_price and max_price > 0 else None,
            min_volume=min_volume if min_volume and min_volume > 0 else None,
            min_rs_rating=min_rs_rating if min_rs_rating and min_rs_rating > 0 else None,
            above_sma_50=above_sma_50 if above_sma_50 else None,
            above_sma_200=above_sma_200 if above_sma_200 else None,
            minervini_template=minervini_template if minervini_template else None,
        )

        # Run screen
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        results = loop.run_until_complete(
            advanced_screener_service.run_screen(
                filter_criteria=criteria,
                limit=limit
            )
        )
        loop.close()

        # Convert to DataFrame
        if results.get("results"):
            df = pd.DataFrame(results["results"])
            df = df[["symbol", "name", "sector", "price", "volume", "rs_rating", "score"]]
            return df
        else:
            return pd.DataFrame({"Message": ["No matches found"]})

    except Exception as e:
        return pd.DataFrame({"Error": [str(e)]})


def create_screener_interface():
    """Create the Gradio interface for the screener"""

    with gr.Blocks(title="Legend AI Stock Screener") as interface:
        gr.Markdown("# 📊 Legend AI Advanced Stock Screener")
        gr.Markdown("Powerful stock screening with proven strategies and custom filters")

        with gr.Tabs():
            # Tab 1: Pre-built Templates
            with gr.Tab("📋 Pre-built Templates"):
                gr.Markdown("### Select a proven screening strategy")

                template_dropdown = gr.Dropdown(
                    choices=[
                        "Minervini SEPA",
                        "O'Neil CAN SLIM",
                        "Momentum Leaders",
                        "Breakout Candidates",
                        "Gap-Up Today",
                        "High Tight Flag",
                        "Pullback to Support",
                        "Pocket Pivot",
                        "Strong Foundation",
                        "Post-IPO Base"
                    ],
                    label="Select Template",
                    value="Minervini SEPA"
                )

                template_limit = gr.Slider(
                    minimum=10,
                    maximum=100,
                    value=50,
                    step=10,
                    label="Maximum Results"
                )

                template_btn = gr.Button("Run Template Screen", variant="primary")
                template_output = gr.DataFrame(label="Screen Results")

                template_btn.click(
                    fn=run_template_screen,
                    inputs=[template_dropdown, template_limit],
                    outputs=template_output
                )

            # Tab 2: Custom Screen
            with gr.Tab("⚙️ Custom Screen"):
                gr.Markdown("### Build your own custom screen")

                with gr.Row():
                    with gr.Column():
                        gr.Markdown("**Price Filters**")
                        custom_min_price = gr.Number(label="Min Price", value=5.0)
                        custom_max_price = gr.Number(label="Max Price", value=0)

                    with gr.Column():
                        gr.Markdown("**Volume & Strength**")
                        custom_min_volume = gr.Number(label="Min Volume", value=500000)
                        custom_min_rs = gr.Number(label="Min RS Rating", value=70.0)

                with gr.Row():
                    with gr.Column():
                        gr.Markdown("**Technical Indicators**")
                        custom_above_sma50 = gr.Checkbox(label="Above SMA 50")
                        custom_above_sma200 = gr.Checkbox(label="Above SMA 200")
                        custom_minervini = gr.Checkbox(label="Minervini Trend Template")

                    with gr.Column():
                        gr.Markdown("**Output**")
                        custom_limit = gr.Slider(
                            minimum=10,
                            maximum=100,
                            value=50,
                            step=10,
                            label="Maximum Results"
                        )

                custom_btn = gr.Button("Run Custom Screen", variant="primary")
                custom_output = gr.DataFrame(label="Screen Results")

                custom_btn.click(
                    fn=run_custom_screen,
                    inputs=[
                        custom_min_price,
                        custom_max_price,
                        custom_min_volume,
                        custom_min_rs,
                        custom_above_sma50,
                        custom_above_sma200,
                        custom_minervini,
                        custom_limit
                    ],
                    outputs=custom_output
                )

            # Tab 3: Documentation
            with gr.Tab("📚 Documentation"):
                gr.Markdown("""
                ## How to Use the Screener

                ### Pre-built Templates
                Choose from 10 proven screening strategies:

                1. **Minervini SEPA** - Mark Minervini's Specific Entry Point Analysis
                2. **O'Neil CAN SLIM** - William O'Neil's growth stock methodology
                3. **Momentum Leaders** - High RS stocks with strong momentum
                4. **Breakout Candidates** - Stocks setting up for breakouts
                5. **Gap-Up Today** - Stocks gapping up with volume
                6. **High Tight Flag** - O'Neil's strongest pattern
                7. **Pullback to Support** - Quality pullbacks to SMA50
                8. **Pocket Pivot** - Volume spikes on up days
                9. **Strong Foundation** - Stocks with aligned moving averages
                10. **Post-IPO Base** - Recent IPOs building first base

                ### Custom Screens
                Build your own screen with these filters:

                - **Price**: Set minimum and maximum price
                - **Volume**: Filter by daily volume
                - **RS Rating**: Relative Strength vs market (0-100)
                - **Technical**: Above SMA50, SMA200, Minervini template
                - **Patterns**: VCP, Cup & Handle, and more

                ### API Endpoints
                Use the REST API for automation:

                - `POST /api/screener/run` - Run custom screen
                - `POST /api/screener/templates/{type}/run` - Run template
                - `POST /api/screener/saved` - Save a screen
                - `POST /api/screener/saved/{id}/schedule` - Schedule a screen

                See `/docs` for full API documentation.

                ### Tips
                - Start with pre-built templates to learn
                - Combine multiple filters for better results
                - Higher RS rating (>80) indicates stronger stocks
                - Save frequently used screens for quick access
                - Schedule screens to run daily for alerts
                """)

        gr.Markdown("---")
        gr.Markdown("Built with Legend AI | Powered by proven trading strategies")

    return interface


if __name__ == "__main__":
    interface = create_screener_interface()
    interface.launch()
