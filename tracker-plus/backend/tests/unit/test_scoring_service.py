from app.services.scoring import calculate_points


def test_calculate_points_no_streak_returns_base_10():
    assert calculate_points(streak=0) == 10


def test_calculate_points_streak_1_returns_base_10():
    assert calculate_points(streak=1) == 10


def test_calculate_points_streak_6_returns_no_weekly_bonus():
    assert calculate_points(streak=6) == 10


def test_calculate_points_streak_7_returns_weekly_bonus():
    assert calculate_points(streak=7) == 60


def test_calculate_points_streak_30_returns_monthly_bonus():
    assert calculate_points(streak=30) == 160


def test_calculate_points_streak_50_returns_monthly_bonus():
    assert calculate_points(streak=50) == 160


def test_calculate_points_streak_15_returns_weekly_bonus():
    assert calculate_points(streak=15) == 60


def test_calculate_points_at_streak_30_bonuses_are_cumulative():
    result = calculate_points(streak=30)
    assert result == 10 + 50 + 100


def test_calculate_points_with_custom_base_points_returns_custom_value():
    assert calculate_points(streak=0, base_points=20) == 20
