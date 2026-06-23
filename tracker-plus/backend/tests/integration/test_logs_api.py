import pytest
from datetime import date, timedelta


def create_habit(client, name="Hábito teste"):
    res = client.post("/habits", json={"name": name})
    return res.get_json()["id"]


def complete(client, habit_id, days_ago=0):
    d = (date.today() - timedelta(days=days_ago)).isoformat()
    return client.post(f"/habits/{habit_id}/complete", json={"date": d})


def test_complete_habit_success(client):
    habit_id = create_habit(client)
    res = client.post(f"/habits/{habit_id}/complete", json={})
    assert res.status_code == 201
    data = res.get_json()
    assert data["habit_id"] == habit_id
    assert "date" in data


def test_complete_habit_with_explicit_date(client):
    habit_id = create_habit(client)
    res = client.post(f"/habits/{habit_id}/complete", json={"date": "2024-01-15"})
    assert res.status_code == 201
    assert res.get_json()["date"] == "2024-01-15"


def test_complete_habit_duplicate_returns_conflict(client):
    habit_id = create_habit(client)
    client.post(f"/habits/{habit_id}/complete", json={"date": "2024-01-15"})
    res = client.post(f"/habits/{habit_id}/complete", json={"date": "2024-01-15"})
    assert res.status_code == 409


def test_complete_habit_on_different_days_succeeds(client):
    habit_id = create_habit(client)
    r1 = client.post(f"/habits/{habit_id}/complete", json={"date": "2024-01-14"})
    r2 = client.post(f"/habits/{habit_id}/complete", json={"date": "2024-01-15"})
    assert r1.status_code == 201
    assert r2.status_code == 201


def test_complete_nonexistent_habit(client):
    res = client.post("/habits/9999/complete", json={})
    assert res.status_code == 404


def test_get_logs_when_empty(client):
    habit_id = create_habit(client)
    res = client.get(f"/habits/{habit_id}/logs")
    assert res.status_code == 200
    assert res.get_json() == []


def test_get_logs_returns_all_completions(client):
    habit_id = create_habit(client)
    for days in [2, 1, 0]:
        complete(client, habit_id, days_ago=days)
    res = client.get(f"/habits/{habit_id}/logs")
    assert res.status_code == 200
    assert len(res.get_json()) == 3


def test_complete_three_consecutive_days_updates_streak(client):
    habit_id = create_habit(client)
    for days in [2, 1, 0]:
        complete(client, habit_id, days_ago=days)
    res = client.get(f"/habits/{habit_id}/streak")
    assert res.status_code == 200
    assert res.get_json()["current_streak"] == 3


def test_first_completion_awards_base_points(client):
    habit_id = create_habit(client)
    complete(client, habit_id)
    res = client.get(f"/habits/{habit_id}/score")
    assert res.status_code == 200
    assert res.get_json()["points"] == 10


def test_leaderboard_orders_by_points_descending(client):
    id_a = create_habit(client, "Hábito A")
    id_b = create_habit(client, "Hábito B")
    complete(client, id_b, days_ago=1)
    complete(client, id_b, days_ago=0)
    res = client.get("/leaderboard")
    assert res.status_code == 200
    board = res.get_json()
    assert board[0]["habit_id"] == id_b


def test_streak_endpoint_with_no_completions(client):
    habit_id = create_habit(client)
    res = client.get(f"/habits/{habit_id}/streak")
    assert res.status_code == 200
    data = res.get_json()
    assert data["current_streak"] == 0
    assert data["max_streak"] == 0
