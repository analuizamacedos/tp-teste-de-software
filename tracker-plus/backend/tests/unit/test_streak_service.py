from datetime import date, timedelta
from app.services.streak import calculate_current_streak, calculate_max_streak


def today():
    return date.today()


def days_ago(n):
    return today() - timedelta(days=n)


def test_streak_empty_logs():
    assert calculate_current_streak([]) == 0


def test_streak_only_today():
    assert calculate_current_streak([today()]) == 1


def test_streak_consecutive_5_days():
    logs = [days_ago(4), days_ago(3), days_ago(2), days_ago(1), today()]
    assert calculate_current_streak(logs) == 5


def test_streak_reset_on_gap():
    # days_ago(5) e days_ago(4) formam um bloco, days_ago(1) e today() formam outro
    logs = [days_ago(5), days_ago(4), days_ago(1), today()]
    assert calculate_current_streak(logs) == 2


def test_streak_not_including_today():
    # Opção B: ontem é ponto de partida válido — streak ainda "vivo"
    logs = [days_ago(3), days_ago(2), days_ago(1)]
    assert calculate_current_streak(logs) == 3


def test_streak_unordered_input():
    logs = [today(), days_ago(2), days_ago(1)]
    assert calculate_current_streak(logs) == 3


def test_max_streak_empty():
    assert calculate_max_streak([]) == 0


def test_max_streak_single():
    assert calculate_max_streak([days_ago(0)]) == 1


def test_max_streak_with_gap():
    # bloco de 3 + bloco de 7
    block_a = [days_ago(20 + i) for i in range(3)]
    block_b = [days_ago(5 + i) for i in range(7)]
    assert calculate_max_streak(block_a + block_b) == 7


def test_max_streak_all_consecutive():
    logs = [days_ago(9 - i) for i in range(10)]
    assert calculate_max_streak(logs) == 10
