# SPEC-06 — Rotas de Logs e Estatísticas

**Dependência:** 🟡 DEPENDE DE: SPEC-02, SPEC-03, SPEC-04
**Pode ser executada em paralelo com:** SPEC-05
**Bloqueia:** SPEC-07

---

## Objetivo

Implementar os endpoints de conclusão de hábito, estatísticas (streak, score) e leaderboard, integrando os services de TASK-03 com o banco de TASK-02. Escrever os testes de integração correspondentes.

---

## Arquivos a Implementar

### `backend/app/routes/logs.py`

Blueprint `logs_bp`.

#### `POST /habits/<int:habit_id>/complete`

1. Busca hábito. Se não encontrado → `404`.
2. Lê `date` do body JSON. Se ausente, usa `date.today()`.
3. Verifica duplicata via query `HabitLog.query.filter_by(habit_id=..., date=...)`. Se existir → `409 {"error": "Habit already completed for this date"}`.
4. Cria `HabitLog` e persiste.
5. Busca todos os logs do hábito, extrai as datas, chama `calculate_current_streak(dates)`.
6. Chama `calculate_points(streak)`.
7. Adiciona os pontos ao `Score` do hábito.
8. Retorna `201` com `log.to_dict()`.

#### `GET /habits/<int:habit_id>/logs`

- Retorna todos os `HabitLog`s do hábito ordenados por `date` decrescente.
- Retorna `200` com lista de `log.to_dict()`.

---

### `backend/app/routes/stats.py`

Blueprint `stats_bp`.

#### `GET /habits/<int:habit_id>/streak`

1. Busca hábito. Se não encontrado → `404`.
2. Extrai datas dos logs.
3. Chama `calculate_current_streak` e `calculate_max_streak`.
4. Retorna `200`:
```json
{ "habit_id": 1, "current_streak": 5, "max_streak": 12 }
```

#### `GET /habits/<int:habit_id>/score`

1. Busca hábito. Se não encontrado → `404`.
2. Busca `Score` do hábito.
3. Retorna `200`:
```json
{ "habit_id": 1, "points": 350 }
```

#### `GET /leaderboard`

1. Faz join de `Habit` com `Score`, ordena por `points` decrescente.
2. Para cada entrada calcula `current_streak`.
3. Retorna `200`:
```json
[
  { "habit_id": 1, "name": "Beber água", "points": 350, "streak": 5 },
  { "habit_id": 2, "name": "Exercício",  "points": 180, "streak": 2 }
]
```

---

### `backend/app/routes/__init__.py`

```python
def register_routes(app):
    from .habits import habits_bp
    from .logs import logs_bp
    from .stats import stats_bp

    app.register_blueprint(habits_bp)
    app.register_blueprint(logs_bp)
    app.register_blueprint(stats_bp)
```

---

## Testes

### Arquivo: `backend/tests/integration/test_logs_api.py`

> Testes de integração — usam o `client` fixture (banco SQLite em memória). Cada teste recebe um banco limpo.

| # | Nome do teste | Ação | Resultado esperado |
|---|---|---|---|
| I-12 | `test_complete_habit_success` | Cria hábito → `POST /habits/<id>/complete` | Status `201`; body tem `habit_id` e `date` |
| I-13 | `test_complete_habit_with_explicit_date` | `POST /habits/<id>/complete` com `{"date": "2024-01-15"}` | Status `201`; `date == "2024-01-15"` |
| I-14 | `test_complete_habit_duplicate_returns_conflict` | `POST /habits/<id>/complete` duas vezes na mesma data | Segundo retorna `409` |
| I-15 | `test_complete_habit_on_different_days_succeeds` | `POST /habits/<id>/complete` em dois dias distintos | Ambos retornam `201` |
| I-16 | `test_complete_nonexistent_habit` | `POST /habits/9999/complete` | Status `404` |
| I-17 | `test_get_logs_when_empty` | Cria hábito sem conclusões, `GET /habits/<id>/logs` | Status `200`; lista `[]` |
| I-18 | `test_get_logs_returns_all_completions` | Completa 3 dias diferentes, `GET /habits/<id>/logs` | Status `200`; lista com 3 itens |
| I-19 | `test_complete_three_consecutive_days_updates_streak` | Completa dias -2, -1 e hoje, `GET /habits/<id>/streak` | `current_streak == 3` |
| I-20 | `test_first_completion_awards_base_points` | Completa 1 vez, `GET /habits/<id>/score` | `points == 10` |
| I-21 | `test_leaderboard_orders_by_points_descending` | Cria 2 hábitos; completa o segundo 2 vezes; `GET /leaderboard` | Segundo hábito aparece primeiro |
| I-22 | `test_streak_endpoint_with_no_completions` | Cria hábito, `GET /habits/<id>/streak` sem completar | `current_streak == 0` e `max_streak == 0` |

```python
# backend/tests/integration/test_logs_api.py
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
```

---

## Critério de Conclusão

- `pytest backend/tests/integration/test_logs_api.py -v` → 11 testes passam.
- `pytest backend/tests/` → todos os testes (unitários + integração) passam juntos.
- Pontuação acumula corretamente a cada conclusão.
- Leaderboard retorna ordenado por pontuação decrescente.