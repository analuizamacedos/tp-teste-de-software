import pytest
from datetime import date
from app.models import HabitLog


def test_habit_log_create_stores_habit_id_and_date():
    today = date.today()
    log = HabitLog(habit_id=1, date=today)
    assert log.habit_id == 1
    assert log.date == today


def test_habit_log_create_defaults_completed_to_true():
    log = HabitLog(habit_id=1, date=date.today())
    assert log.completed is True


def test_habit_log_to_dict_contains_all_required_keys():
    log = HabitLog(habit_id=1, date=date.today())
    result = log.to_dict()
    assert "id" in result
    assert "habit_id" in result
    assert "date" in result
    assert "completed" in result


def test_habit_log_to_dict_date_is_iso_format_string():
    log = HabitLog(habit_id=1, date=date.today())
    result = log.to_dict()
    assert isinstance(result["date"], str)
    assert len(result["date"]) == 10


def test_habit_log_create_none_habit_id_raises_error():
    with pytest.raises((ValueError, TypeError)):
        HabitLog(habit_id=None, date=date.today())


def test_habit_log_create_none_date_raises_error():
    with pytest.raises((ValueError, TypeError)):
        HabitLog(habit_id=1, date=None)
