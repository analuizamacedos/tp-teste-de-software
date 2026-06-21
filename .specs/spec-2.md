# SPEC-02 — Models e Banco de Dados

**Dependência:** 🟡 DEPENDE DE: SPEC-01
**Pode ser executada em paralelo com:** SPEC-03, SPEC-05
**Bloqueia:** SPEC-04, SPEC-06

---

## Objetivo

Implementar os três modelos SQLAlchemy (`Habit`, `HabitLog`, `Score`) com todas as restrições de integridade e validações de domínio. Os modelos devem ser instanciáveis como objetos Python puro, sem contexto Flask, para viabilizar os testes unitários.

---

## Arquivos a Implementar

### `backend/app/models.py`

#### Modelo `Habit`

| Campo         | Tipo SQLAlchemy | Restrições                              |
|---------------|-----------------|-----------------------------------------|
| `id`          | `Integer`, PK   | autoincrement                           |
| `name`        | `String(120)`   | `nullable=False`                        |
| `description` | `String(300)`   | `nullable=True`, default `""`           |
| `created_at`  | `DateTime`      | default = `datetime.utcnow`             |

**Regras de negócio no `__init__`:**
- Levanta `ValueError("Habit name cannot be empty")` se `name` for vazio ou só espaços.
- Levanta `ValueError("Habit name is too long")` se `len(name.strip()) > 120`.
- Levanta `ValueError("Habit description is too long")` se `len(description) > 300`.
- Armazena `self.name = name.strip()`.
- Atribui `self.created_at = datetime.utcnow()` diretamente no `__init__` (não só como default de coluna), para que o campo esteja disponível em objetos não-persistidos.

**Método `to_dict()`:**
```python
{
    "id": self.id,
    "name": self.name,
    "description": self.description,
    "created_at": self.created_at.isoformat()
}
```

**Relacionamento:**
```python
logs = relationship("HabitLog", backref="habit", cascade="all, delete-orphan")
score = relationship("Score", backref="habit", cascade="all, delete-orphan", uselist=False)
```

---

#### Modelo `HabitLog`

| Campo      | Tipo SQLAlchemy    | Restrições                             |
|------------|--------------------|----------------------------------------|
| `id`       | `Integer`, PK      | autoincrement                          |
| `habit_id` | `Integer`, FK      | `Habit.id`, `nullable=False`           |
| `date`     | `Date`             | `nullable=False`                       |
| `completed`| `Boolean`          | default `True`                         |
| *(unique)* | `UniqueConstraint` | `('habit_id', 'date')`                 |

**Regra no `__init__`:**
- Aceita `habit_id` e `date` como parâmetros posicionais e os atribui imediatamente a `self`.
- Isso permite instanciar o objeto sem banco para fins de teste unitário.

**Método `to_dict()`:**
```python
{
    "id": self.id,
    "habit_id": self.habit_id,
    "date": self.date.isoformat(),
    "completed": self.completed
}
```

---

#### Modelo `Score`

| Campo       | Tipo SQLAlchemy | Restrições                                         |
|-------------|-----------------|----------------------------------------------------|
| `id`        | `Integer`, PK   | autoincrement                                      |
| `habit_id`  | `Integer`, FK   | `Habit.id`, `nullable=False`                       |
| `points`    | `Integer`       | default `0`                                        |
| `updated_at`| `DateTime`      | default = `datetime.utcnow`, `onupdate=datetime.utcnow` |

**Método `to_dict()`:**
```python
{
    "habit_id": self.habit_id,
    "points": self.points
}
```

---

## Testes

### Arquivo: `backend/tests/unit/test_habit_model.py`

> Testes unitários — **sem banco de dados, sem contexto Flask**. Testam apenas a lógica do construtor e dos métodos da classe `Habit`.

| # | Nome do teste | Cenário | Resultado esperado |
|---|---|---|---|
| U-01 | `test_habit_created_with_valid_name_and_description` | `Habit(name="Beber água", description="8 copos")` | `habit.name == "Beber água"` e `habit.description == "8 copos"` |
| U-02 | `test_habit_name_cannot_be_empty_string` | `Habit(name="")` | Levanta `ValueError` |
| U-03 | `test_habit_name_cannot_be_whitespace_only` | `Habit(name="   ")` | Levanta `ValueError` |
| U-04 | `test_habit_name_exceeding_max_length_raises_error` | `Habit(name="x" * 121)` | Levanta `ValueError` |
| U-05 | `test_habit_description_is_optional` | `Habit(name="Meditar")` sem `description` | Não levanta exceção |
| U-06 | `test_habit_name_is_stripped_on_creation` | `Habit(name="  Correr  ")` | `habit.name == "Correr"` |
| U-07 | `test_habit_to_dict_contains_required_keys` | `Habit(name="Ler").to_dict()` | Dict contém `id`, `name`, `description`, `created_at` |
| U-08 | `test_habit_created_at_is_iso_format_string` | `Habit(name="Ler").to_dict()["created_at"]` | É uma string no formato ISO 8601 (contém `T`) |

```python
# backend/tests/unit/test_habit_model.py
import pytest
from app.models import Habit

def test_habit_created_with_valid_name_and_description():
    habit = Habit(name="Beber água", description="8 copos")
    assert habit.name == "Beber água"
    assert habit.description == "8 copos"

def test_habit_name_cannot_be_empty_string():
    with pytest.raises(ValueError):
        Habit(name="")

def test_habit_name_cannot_be_whitespace_only():
    with pytest.raises(ValueError):
        Habit(name="   ")

def test_habit_name_exceeding_max_length_raises_error():
    with pytest.raises(ValueError):
        Habit(name="x" * 121)

def test_habit_description_is_optional():
    habit = Habit(name="Meditar")
    assert habit.name == "Meditar"

def test_habit_name_is_stripped_on_creation():
    habit = Habit(name="  Correr  ")
    assert habit.name == "Correr"

def test_habit_to_dict_contains_required_keys():
    habit = Habit(name="Ler")
    result = habit.to_dict()
    assert "id" in result
    assert "name" in result
    assert "description" in result
    assert "created_at" in result

def test_habit_created_at_is_iso_format_string():
    habit = Habit(name="Ler")
    result = habit.to_dict()
    assert isinstance(result["created_at"], str)
    assert "T" in result["created_at"]
```

---

### Arquivo: `backend/tests/unit/test_habit_log_model.py`

> Testes unitários — **sem banco de dados, sem contexto Flask**. Testam apenas a lógica do construtor e dos métodos da classe `HabitLog`.

| # | Nome do teste | Cenário | Resultado esperado |
|---|---|---|---|
| U-09 | `test_habit_log_created_with_valid_data` | `HabitLog(habit_id=1, date=date.today())` | `log.habit_id == 1` e `log.date == date.today()` |
| U-10 | `test_habit_log_completed_defaults_to_true` | `HabitLog(habit_id=1, date=date.today())` sem `completed` | `log.completed == True` |
| U-11 | `test_habit_log_to_dict_contains_required_keys` | `HabitLog(...).to_dict()` | Dict contém `id`, `habit_id`, `date`, `completed` |
| U-12 | `test_habit_log_date_is_iso_format_string` | `HabitLog(...).to_dict()["date"]` | É uma string no formato `YYYY-MM-DD` |
| U-13 | `test_habit_log_requires_habit_id` | `HabitLog(habit_id=None, date=date.today())` | Levanta `ValueError` ou `TypeError` |
| U-14 | `test_habit_log_requires_date` | `HabitLog(habit_id=1, date=None)` | Levanta `ValueError` ou `TypeError` |

```python
# backend/tests/unit/test_habit_log_model.py
import pytest
from datetime import date
from app.models import HabitLog

def test_habit_log_created_with_valid_data():
    today = date.today()
    log = HabitLog(habit_id=1, date=today)
    assert log.habit_id == 1
    assert log.date == today

def test_habit_log_completed_defaults_to_true():
    log = HabitLog(habit_id=1, date=date.today())
    assert log.completed == True

def test_habit_log_to_dict_contains_required_keys():
    log = HabitLog(habit_id=1, date=date.today())
    result = log.to_dict()
    assert "id" in result
    assert "habit_id" in result
    assert "date" in result
    assert "completed" in result

def test_habit_log_date_is_iso_format_string():
    log = HabitLog(habit_id=1, date=date.today())
    result = log.to_dict()
    assert isinstance(result["date"], str)
    assert len(result["date"]) == 10  # YYYY-MM-DD

def test_habit_log_requires_habit_id():
    with pytest.raises((ValueError, TypeError)):
        HabitLog(habit_id=None, date=date.today())

def test_habit_log_requires_date():
    with pytest.raises((ValueError, TypeError)):
        HabitLog(habit_id=1, date=None)
```

---

## Critério de Conclusão

- `pytest backend/tests/unit/test_habit_model.py -v` → 8 testes passam.
- `pytest backend/tests/unit/test_habit_log_model.py -v` → 6 testes passam.
- Nenhum import de Flask ou SQLAlchemy nos arquivos de teste.
- `python run.py` cria `tracker.db` com as três tabelas ao iniciar.