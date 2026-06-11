import pytest
from app.models import Habit


def test_habit_created_correctly():
    habit = Habit(name="Beber água", description="8 copos")
    assert habit.name == "Beber água"
    assert habit.description == "8 copos"


def test_habit_name_cannot_be_empty():
    with pytest.raises(ValueError):
        Habit(name="")


def test_habit_name_cannot_be_whitespace():
    with pytest.raises(ValueError):
        Habit(name="   ")


def test_habit_description_is_optional():
    habit = Habit(name="Meditar")
    assert habit.name == "Meditar"


def test_habit_to_dict_keys():
    habit = Habit(name="Exercício")
    result = habit.to_dict()
    assert "id" in result
    assert "name" in result
    assert "description" in result
    assert "created_at" in result
