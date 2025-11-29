@router.post("/detect", response_model=PatternResponse)
async def detect_pattern(request: PatternRequest):
    """Detect Chart Pattern for Any Stock"""
    import time
    start_time = time.time()
    cache = get_cache_service()

    try:
        # Ticker validation
        if not request.ticker or not request.ticker.strip():
            raise HTTPException(status_code=400, detail="Ticker is required")

        ticker = request.ticker.upper().strip()

        # Validate ticker format
        if not ticker.replace(".", "").replace("-", "").isalnum():
            raise HTTPException(status_code=400, detail="Invalid ticker symbol format")

        logger.info(f"🔍 Analyzing pattern for {ticker}")

        # 1. Try cache first
        cached_result = await cache.get_pattern(ticker=ticker, interval=request.interval)
        if cached_result:
            # Convert cached dict back to PatternResult
            if isinstance(cached_result.get("timestamp"), str):
                cached_result["timestamp"] = datetime.fromisoformat(cached_result["timestamp"])

            # Just return the cached dict directly (it should be clean)
            processing_time = time.time() - start_time
            return PatternResponse(
                success=True,
                data=cached_result,
                error=None,
                cached=True,
                api_used="cache",
                processing_time=round(processing_time, 2)
            )

        # 2. Cache miss - fetch from API
        price_data = await market_data_service.get_time_series(
            ticker=ticker,
            interval=request.interval,
            outputsize=500
        )

        if not price_data:
            raise HTTPException(status_code=404, detail=f"No price data available for {ticker}")

        api_used = price_data.get("source", "unknown")

        # Get SPY data for RS
        spy_data = await market_data_service.get_time_series("SPY", "1day", 500)

        # Run pattern detection
        result = None
        if request.use_advanced_patterns:
            advanced_detector = get_pattern_detector()
            detected_patterns = advanced_detector.detect_all_patterns(price_data, ticker)
            
            if detected_patterns:
                best_pattern = max(detected_patterns, key=lambda p: p.get('confidence', 0))
                result = PatternResult(
                    ticker=ticker,
                    pattern=best_pattern['pattern'],
                    score=best_pattern['score'],
                    entry=best_pattern['entry'],
                    stop=best_pattern['stop'],
                    target=best_pattern['target'],
                    risk_reward=best_pattern['risk_reward'],
                    criteria_met=[
                        f"✓ {best_pattern['pattern']} confirmed" if best_pattern.get('confirmed') else f"⚠ {best_pattern['pattern']} pending confirmation",
                        f"✓ Confidence: {best_pattern['confidence']*100:.1f}%"
                    ],
                    analysis=f"Legend AI detected {best_pattern['pattern']} with {best_pattern['confidence']*100:.0f}% confidence.",
                    timestamp=datetime.now(),
                    current_price=best_pattern.get('current_price'),
                    support_start=best_pattern.get('metadata', {}).get('bottom'),
                    support_end=best_pattern.get('metadata', {}).get('bottom')
                )
            else:
                detector = PatternDetector()
                result = await detector.analyze_ticker(ticker=ticker, price_data=price_data, spy_data=spy_data)
        else:
            detector = PatternDetector()
            result = await detector.analyze_ticker(ticker=ticker, price_data=price_data, spy_data=spy_data)

        if not result:
            raise HTTPException(status_code=500, detail=f"Pattern analysis failed for {ticker}")

        # Generate chart
        try:
            charting = get_charting_service()
            chart_url = await charting.generate_chart(
                ticker=ticker,
                timeframe=request.interval,
                entry=result.entry,
                stop=result.stop,
                target=result.target,
                support=result.support_start,
                resistance=None,
                pattern_name=f"{result.pattern} Entry"
            )
            if chart_url:
                result.chart_url = chart_url
        except Exception:
            pass

        # Convert to dict (sanitizes numpy types)
        result_dict = result.to_dict()

        # Cache result
        await cache.set_pattern(ticker, request.interval, result_dict)

        return PatternResponse(
            success=True,
            data=result_dict,
            error=None,
            cached=False,
            api_used=api_used,
            processing_time=round(time.time() - start_time, 2)
        )

    except HTTPException:
        raise
    except Exception as e:
        processing_time = time.time() - start_time
        logger.error(f"💥 Pattern detection failed for {request.ticker}: {e}")
        # Return 500 for unhandled exceptions to avoid swallowing server errors
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
