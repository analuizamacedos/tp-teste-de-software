from datetime import date, timedelta
from app.services.streak import calculate_current_streak, calculate_max_streak


def today():
    return date.today()


def days_ago(n):
    return today() - timedelta(days=n)


def test_current_streak_empty_logs_returns_0():
    assert calculate_current_streak([]) == 0


def test_current_streak_only_today_returns_1():
    assert calculate_current_streak([today()]) == 1


def test_current_streak_5_consecutive_days_returns_5():
    logs = [days_ago(4), days_ago(3), days_ago(2), days_ago(1), today()]
    assert calculate_current_streak(logs) == 5


def test_current_streak_gap_in_logs_returns_recent_block_count():
    logs = [days_ago(5), days_ago(4), days_ago(1), today()]
    assert calculate_current_streak(logs) == 2


def test_current_streak_ending_yesterday_returns_streak_count():
    logs = [days_ago(3), days_ago(2), days_ago(1)]
    assert calculate_current_streak(logs) == 3


def test_current_streak_unordered_input_returns_correct_count():
    logs = [today(), days_ago(2), days_ago(1)]
    assert calculate_current_streak(logs) == 3


def test_current_streak_with_today_and_yesterday_returns_2():
    assert calculate_current_streak([days_ago(1), days_ago(0)]) == 2


def test_max_streak_empty_logs_returns_0():
    assert calculate_max_streak([]) == 0


def test_max_streak_single_day_returns_1():
    assert calculate_max_streak([days_ago(0)]) == 1


def test_max_streak_two_blocks_returns_longer_block_length():
    block_a = [days_ago(22), days_ago(21), days_ago(20)]
    block_b = [days_ago(11), days_ago(10), days_ago(9), days_ago(8), days_ago(7), days_ago(6), days_ago(5)]
    assert calculate_max_streak(block_a + block_b) == 7


def test_max_streak_all_consecutive_returns_total_count():
    logs = [
        days_ago(9), days_ago(8), days_ago(7), days_ago(6), days_ago(5),
        days_ago(4), days_ago(3), days_ago(2), days_ago(1), days_ago(0),
    ]
    assert calculate_max_streak(logs) == 10
