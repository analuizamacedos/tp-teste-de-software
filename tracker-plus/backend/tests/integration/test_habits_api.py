def test_create_habit_success(client):
    res = client.post("/habits", json={"name": "Beber água", "description": "8 copos"})
    assert res.status_code == 201
    data = res.get_json()
    assert data["name"] == "Beber água"
    assert "id" in data


def test_create_habit_only_name(client):
    res = client.post("/habits", json={"name": "Meditar"})
    assert res.status_code == 201


def test_create_habit_empty_name(client):
    res = client.post("/habits", json={"name": ""})
    assert res.status_code == 400


def test_create_habit_whitespace_name(client):
    res = client.post("/habits", json={"name": "   "})
    assert res.status_code == 400


def test_create_habit_missing_name_field(client):
    res = client.post("/habits", json={})
    assert res.status_code == 400


def test_list_habits_when_empty(client):
    res = client.get("/habits")
    assert res.status_code == 200
    assert res.get_json() == []


def test_list_habits_returns_all_created(client):
    client.post("/habits", json={"name": "Hábito A"})
    client.post("/habits", json={"name": "Hábito B"})
    res = client.get("/habits")
    assert res.status_code == 200
    assert len(res.get_json()) == 2


def test_get_habit_by_id(client):
    created = client.post("/habits", json={"name": "Ler"}).get_json()
    res = client.get(f"/habits/{created['id']}")
    assert res.status_code == 200
    assert res.get_json()["name"] == "Ler"


def test_get_habit_not_found(client):
    res = client.get("/habits/9999")
    assert res.status_code == 404


def test_delete_habit_removes_it(client):
    created = client.post("/habits", json={"name": "Deletar"}).get_json()
    habit_id = created["id"]
    assert client.delete(f"/habits/{habit_id}").status_code == 200
    assert client.get(f"/habits/{habit_id}").status_code == 404


def test_delete_habit_not_found(client):
    res = client.delete("/habits/9999")
    assert res.status_code == 404
