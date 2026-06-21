# SPEC-04 — Rotas de Hábitos (CRUD)

**Dependência:** 🟡 DEPENDE DE: SPEC-02
**Pode ser executada em paralelo com:** SPEC-03, SPEC-05
**Bloqueia:** SPEC-06

---

## Objetivo

Implementar os endpoints CRUD de hábitos e seus testes de integração. Nesta task não existe lógica de negócio nas rotas — validações ficam nos models, cálculos ficam nos services.

---

## Arquivos a Implementar

### `backend/app/routes/habits.py`

Blueprint `habits_bp` com prefixo `/habits`.

#### `POST /habits`

1. Lê `name` e `description` do body JSON. Se `name` ausente → `400`.
2. Instancia `Habit(name=name, description=description)`.
3. Se o construtor levantar `ValueError` → `400` com `{"error": "<mensagem do ValueError>"}`.
4. Persiste no banco. Cria um `Score(habit_id=habit.id, points=0)` associado.
5. Retorna `201` com `habit.to_dict()`.

#### `GET /habits`

- Retorna todos os hábitos ordenados por `created_at` decrescente.
- Lista vazia é válida: retorna `200` com `[]`.

#### `GET /habits/<int:habit_id>`

- Se não encontrado → `404` com `{"error": "Habit not found"}`.
- Retorna `200` com `habit.to_dict()`.

#### `DELETE /habits/<int:habit_id>`

- Se não encontrado → `404`.
- Remove o hábito (cascade apaga `HabitLog`s e `Score`).
- Retorna `200` com `{"message": "Habit deleted"}`.

---

### `backend/app/routes/__init__.py`

```python
def register_routes(app):
    from .habits import habits_bp
    app.register_blueprint(habits_bp)
```

---

## Testes

### Arquivo: `backend/tests/integration/test_habits_api.py`

> Testes de integração — usam o `client` fixture do `conftest.py` (banco SQLite em memória). Cada teste recebe um banco limpo.

| # | Nome do teste | Ação | Resultado esperado |
|---|---|---|---|
| I-01 | `test_create_habit_success` | `POST /habits` com `{"name": "Beber água", "description": "8 copos"}` | Status `201`; body tem `id` e `name == "Beber água"` |
| I-02 | `test_create_habit_only_name` | `POST /habits` com `{"name": "Meditar"}` | Status `201` |
| I-03 | `test_create_habit_empty_name` | `POST /habits` com `{"name": ""}` | Status `400` |
| I-04 | `test_create_habit_whitespace_name` | `POST /habits` com `{"name": "   "}` | Status `400` |
| I-05 | `test_create_habit_missing_name_field` | `POST /habits` com `{}` | Status `400` |
| I-06 | `test_list_habits_when_empty` | `GET /habits` sem dados | Status `200`; body `== []` |
| I-07 | `test_list_habits_returns_all_created` | Cria 2 hábitos, `GET /habits` | Status `200`; lista com 2 itens |
| I-08 | `test_get_habit_by_id` | Cria hábito, `GET /habits/<id>` | Status `200`; `name` correto |
| I-09 | `test_get_habit_not_found` | `GET /habits/9999` | Status `404` |
| I-10 | `test_delete_habit_removes_it` | Cria hábito, `DELETE /habits/<id>`, depois `GET /habits/<id>` | DELETE → `200`; GET → `404` |
| I-11 | `test_delete_habit_not_found` | `DELETE /habits/9999` | Status `404` |

```python
# backend/tests/integration/test_habits_api.py
import pytest

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
```

---

## Critério de Conclusão

- `pytest backend/tests/integration/test_habits_api.py -v` → 11 testes passam.
- Todos os endpoints retornam `Content-Type: application/json`.
- Deletar um `Habit` remove seus `HabitLog`s e `Score` (cascade).