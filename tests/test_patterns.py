from app.core.classifiers import minervini_trend_template, weinstein_stage


def test_minervini_pass_and_fail():
    # Construct an uptrend with clear SMA ordering
    closes_pass = [i * 1.01 for i in range(1, 230)]  # 229 bars increasing
    res_pass = minervini_trend_template(closes_pass)
    assert isinstance(res_pass, dict)
    assert res_pass.get("pass") is True
    assert isinstance(res_pass.get("failed_rules"), list)

    # Construct a downtrend to fail template
    closes_fail = [300 - i * 0.5 for i in range(230)]
    res_fail = minervini_trend_template(closes_fail)
    assert res_fail.get("pass") is False
    assert any(
        "SMA200" in r or "not rising" in r for r in res_fail.get("failed_rules", [])
    )


def test_weinstein_stage_2_and_4():
    # Stage 2: price above rising 30W SMA
    # Build weekly closes that rise steadily
    weekly_rising = [i * 1.02 for i in range(1, 80)]
    w2 = weinstein_stage(weekly_rising)
    assert w2.get("stage") == 2

    # Stage 4: price below falling 30W SMA
    weekly_falling = [200 - i * 1.5 for i in range(80)]
    w4 = weinstein_stage(weekly_falling)
    assert w4.get("stage") == 4
