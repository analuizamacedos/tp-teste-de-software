from app.services.scoring import calculate_points


def test_base_points_no_streak():
    assert calculate_points(streak=0) == 10


def test_base_points_streak_1():
    assert calculate_points(streak=1) == 10


def test_no_bonus_streak_6():
    assert calculate_points(streak=6) == 10


def test_bonus_streak_7():
    assert calculate_points(streak=7) == 60


def test_bonus_streak_10():
    assert calculate_points(streak=10) == 60


def test_bonus_streak_29():
    assert calculate_points(streak=29) == 60


def test_bonus_streak_30():
    assert calculate_points(streak=30) == 160


def test_bonus_streak_50():
    assert calculate_points(streak=50) == 160
