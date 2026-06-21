# SPEC-03 — Services (StreakService e ScoringService)

**Dependência:** 🟡 DEPENDE DE: SPEC-01
**Pode ser executada em paralelo com:** SPEC-02, SPEC-05
**Bloqueia:** SPEC-06

---

## Objetivo

Implementar os dois serviços de lógica de negócio pura (`streak.py` e `scoring.py`). São funções Python simples, sem dependência do Flask ou do banco de dados — o que permite testá-las de forma completamente isolada.

---

## Arquivos a Implementar

### `backend/app/services/__init__.py`

```python
# vazio
```

### `backend/app/services/streak.py`

```python
from datetime import date, timedelta

def calculate_current_streak(logs: list[date]) -> int:
    """
    Recebe lista de objetos date em que o hábito foi concluído.
    Retorna o número de dias consecutivos contados a partir de hoje
    (ou de ontem, se hoje não estiver na lista).

    Regras:
    - Lista vazia retorna 0.
    - Ordena internamente antes de calcular.
    - Um gap de 1 ou mais dias zera o streak.
    - Se o dia mais recente for anterior a ontem, retorna 0.
    """

def calculate_max_streak(logs: list[date]) -> int:
    """
    Retorna o maior bloco consecutivo de dias já registrado no histórico.

    Regras:
    - Lista vazia retorna 0.
    - Ordena internamente antes de calcular.
    """
```

**Lógica de `calculate_current_streak`:**
1. Se `logs` vazio → retorna `0`.
2. Converte para `set` e ordena em ordem decrescente.
3. `today = date.today()`. Se `today` não está na lista e `today - 1 day` também não → retorna `0`.
4. Ponto de partida: `today` se estiver na lista, senão `today - 1 day`.
5. Itera para trás enquanto o dia esperado estiver no conjunto. Retorna o contador.

**Lógica de `calculate_max_streak`:**
1. Se `logs` vazio → retorna `0`.
2. Ordena em ordem crescente.
3. Percorre a lista comparando `logs[i+1] == logs[i] + timedelta(days=1)`. Mantém `current` e `max_seen`. Retorna `max_seen`.

---

### `backend/app/services/scoring.py`

```python
def calculate_points(streak: int, base_points: int = 10) -> int:
    """
    Retorna os pontos a conceder por uma conclusão com o streak atual.

    Tabela de bônus (cumulativos):
    - Base:          10 pts  (sempre)
    - streak >= 7:  +50 pts
    - streak >= 30: +100 pts (acumula com o de 7)

    Exemplos:
    - streak=0  → 10
    - streak=6  → 10
    - streak=7  → 60
    - streak=29 → 60
    - streak=30 → 160
    """
```

---

## Testes

### Arquivo: `backend/tests/unit/test_streak_service.py`

> Testes unitários — **sem banco, sem Flask**. Usam `date` objects diretamente.

**Helper obrigatório** (usar datas relativas, nunca hardcoded):
```python
from datetime import date, timedelta

def days_ago(n):
    return date.today() - timedelta(days=n)
```

| # | Nome do teste | Cenário | Resultado esperado |
|---|---|---|---|
| U-15 | `test_current_streak_with_empty_logs` | `calculate_current_streak([])` | `0` |
| U-16 | `test_current_streak_with_only_today` | `[days_ago(0)]` | `1` |
| U-17 | `test_current_streak_with_five_consecutive_days` | `[days_ago(4), days_ago(3), days_ago(2), days_ago(1), days_ago(0)]` | `5` |
| U-18 | `test_current_streak_resets_after_gap` | `[days_ago(5), days_ago(4), days_ago(1), days_ago(0)]` — falta dias_ago(3) e dias_ago(2) | `2` |
| U-19 | `test_current_streak_accepts_unordered_dates` | `[days_ago(0), days_ago(2), days_ago(1)]` fora de ordem | `3` |
| U-20 | `test_current_streak_with_today_and_yesterday` | `[days_ago(1), days_ago(0)]` | `2` |
| U-21 | `test_max_streak_with_empty_logs` | `calculate_max_streak([])` | `0` |
| U-22 | `test_max_streak_with_single_day` | `[days_ago(0)]` | `1` |
| U-23 | `test_max_streak_returns_longest_block` | Bloco de 3 dias + bloco de 7 dias com gap entre eles | `7` |
| U-24 | `test_max_streak_with_all_consecutive_days` | `[days_ago(i) for i in range(9, -1, -1)]` (10 dias) | `10` |

```python
# backend/tests/unit/test_streak_service.py
import pytest
from datetime import date, timedelta
from app.services.streak import calculate_current_streak, calculate_max_streak

def days_ago(n):
    return date.today() - timedelta(days=n)

def test_current_streak_with_empty_logs():
    assert calculate_current_streak([]) == 0

def test_current_streak_with_only_today():
    assert calculate_current_streak([days_ago(0)]) == 1

def test_current_streak_with_five_consecutive_days():
    logs = [days_ago(i) for i in range(4, -1, -1)]
    assert calculate_current_streak(logs) == 5

def test_current_streak_resets_after_gap():
    logs = [days_ago(5), days_ago(4), days_ago(1), days_ago(0)]
    assert calculate_current_streak(logs) == 2

def test_current_streak_accepts_unordered_dates():
    logs = [days_ago(0), days_ago(2), days_ago(1)]
    assert calculate_current_streak(logs) == 3

def test_current_streak_with_today_and_yesterday():
    assert calculate_current_streak([days_ago(1), days_ago(0)]) == 2

def test_max_streak_with_empty_logs():
    assert calculate_max_streak([]) == 0

def test_max_streak_with_single_day():
    assert calculate_max_streak([days_ago(0)]) == 1

def test_max_streak_returns_longest_block():
    # bloco antigo: 3 dias; bloco recente: 7 dias; gap entre eles
    old_block = [days_ago(20 + i) for i in range(3)]
    new_block = [days_ago(i) for i in range(7)]
    assert calculate_max_streak(old_block + new_block) == 7

def test_max_streak_with_all_consecutive_days():
    logs = [days_ago(i) for i in range(9, -1, -1)]
    assert calculate_max_streak(logs) == 10
```

---

### Arquivo: `backend/tests/unit/test_scoring_service.py`

> Testes unitários — **sem banco, sem Flask**. Testam apenas a função `calculate_points`.

| # | Nome do teste | Cenário | Resultado esperado |
|---|---|---|---|
| U-25 | `test_base_points_with_zero_streak` | `calculate_points(streak=0)` | `10` |
| U-26 | `test_base_points_with_streak_below_seven` | `calculate_points(streak=6)` | `10` |
| U-27 | `test_bonus_points_at_exactly_seven_day_streak` | `calculate_points(streak=7)` | `60` |
| U-28 | `test_bonus_points_with_streak_between_7_and_29` | `calculate_points(streak=15)` | `60` |
| U-29 | `test_bonus_points_at_exactly_thirty_day_streak` | `calculate_points(streak=30)` | `160` |
| U-30 | `test_bonus_points_with_streak_above_thirty` | `calculate_points(streak=50)` | `160` |
| U-31 | `test_bonuses_are_cumulative_at_streak_30` | `calculate_points(streak=30)` | `10 + 50 + 100 == 160` |
| U-32 | `test_custom_base_points_parameter` | `calculate_points(streak=0, base_points=20)` | `20` |

```python
# backend/tests/unit/test_scoring_service.py
import pytest
from app.services.scoring import calculate_points

def test_base_points_with_zero_streak():
    assert calculate_points(streak=0) == 10

def test_base_points_with_streak_below_seven():
    assert calculate_points(streak=6) == 10

def test_bonus_points_at_exactly_seven_day_streak():
    assert calculate_points(streak=7) == 60

def test_bonus_points_with_streak_between_7_and_29():
    assert calculate_points(streak=15) == 60

def test_bonus_points_at_exactly_thirty_day_streak():
    assert calculate_points(streak=30) == 160

def test_bonus_points_with_streak_above_thirty():
    assert calculate_points(streak=50) == 160

def test_bonuses_are_cumulative_at_streak_30():
    result = calculate_points(streak=30)
    assert result == 10 + 50 + 100

def test_custom_base_points_parameter():
    assert calculate_points(streak=0, base_points=20) == 20
```

---

## Critério de Conclusão

- `pytest backend/tests/unit/test_streak_service.py -v` → 10 testes passam.
- `pytest backend/tests/unit/test_scoring_service.py -v` → 8 testes passam.
- Nenhum import de Flask, SQLAlchemy ou qualquer módulo da `app` nos arquivos de serviço.