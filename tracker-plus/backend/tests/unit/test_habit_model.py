import pytest
from app.models import Habit


def test_habit_create_stores_name():
    habit = Habit(name="Beber água")
    assert habit.name == "Beber água"


def test_habit_create_stores_description():
    habit = Habit(name="Beber água", description="8 copos")
    assert habit.description == "8 copos"


def test_habit_create_empty_name_raises_value_error():
    with pytest.raises(ValueError):
        Habit(name="")


def test_habit_create_whitespace_name_raises_value_error():
    with pytest.raises(ValueError):
        Habit(name="   ")


def test_habit_create_without_description_defaults_to_empty():
    habit = Habit(name="Meditar")
    assert habit.description == ""


def test_habit_to_dict_contains_all_required_keys():
    habit = Habit(name="Exercício")
    result = habit.to_dict()
    assert "id" in result
    assert "name" in result
    assert "description" in result
    assert "created_at" in result
