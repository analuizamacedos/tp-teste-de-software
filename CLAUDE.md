# CLAUDE.md — Tracker+

Guia de boas práticas para o Claude Code trabalhar neste projeto.
Leia este arquivo inteiro antes de criar ou editar qualquer código.

---

## Visão Geral do Projeto

Tracker+ é um **Habit Tracker** web com:
- **Backend:** Python 3.11 + Flask, banco SQLite via SQLAlchemy
- **Frontend:** React 18 + Vite
- **Testes:** Pytest (unitários + integração) + Playwright (E2E)

```
tracker-plus/
├── backend/
│   ├── app/
│   │   ├── __init__.py       # Flask application factory
│   │   ├── database.py       # instância do SQLAlchemy
│   │   ├── models.py         # Habit, HabitLog, Score
│   │   ├── routes/           # blueprints Flask
│   │   └── services/         # lógica de negócio pura (sem Flask)
│   ├── tests/
│   │   ├── conftest.py
│   │   ├── unit/
│   │   └── integration/
│   └── run.py
└── frontend/
    ├── src/
    │   ├── components/
    │   ├── pages/
    │   └── services/api.js
    └── e2e/
```

---

## Comandos Essenciais

```bash
# Backend
cd backend
pip install -r requirements.txt
python run.py                          # inicia em localhost:5000

# Testes backend
pytest                                 # todos os testes
pytest tests/unit/ -v                  # só unitários
pytest tests/integration/ -v          # só integração
pytest --cov=app --cov-report=term    # com cobertura

# Frontend
cd frontend
npm install
npm run dev                            # inicia em localhost:5173
npm run test:e2e                       # testes Playwright
```

---

## Arquitetura e Camadas

Este projeto segue uma separação estrita de responsabilidades. Respeite sempre:

```
Request HTTP
    │
    ▼
Routes (blueprints)      ← valida input HTTP, chama services/models, retorna JSON
    │
    ▼
Services (streak, scoring) ← lógica de negócio pura, sem Flask, sem DB
    │
    ▼
Models (SQLAlchemy)      ← validação de domínio no __init__, persistência
    │
    ▼
Database (SQLite)
```

### Regra de ouro: onde colocar cada coisa

| Tipo de código | Onde fica | Exemplo |
|---|---|---|
| Validação de domínio | `models.py` (`__init__`) | nome vazio → `ValueError` |
| Lógica de negócio pura | `services/` | cálculo de streak, pontuação |
| Orquestração HTTP | `routes/` | ler body, chamar service, retornar JSON |
| Chamadas à API | `frontend/src/services/api.js` | `fetch('/habits')` |
| Estado e render | Componentes React | `useState`, `useEffect` |

**Nunca coloque lógica de negócio diretamente nas rotas Flask.**
**Nunca coloque lógica de negócio nos componentes React.**

---

## Backend — Convenções Python/Flask

### Application Factory

Sempre use `create_app(testing=False)` de `app/__init__.py`. Nunca instancie o app diretamente fora da factory.

```python
# CORRETO
app = create_app()

# ERRADO
app = Flask(__name__)
```

### Configuração de banco por ambiente

| Ambiente | URI |
|---|---|
| Produção/dev | `sqlite:///tracker.db` |
| Testes | `sqlite:///:memory:` |

A factory recebe `testing=True` para usar banco em memória. Nunca use o banco de arquivo nos testes.

### Models — Regras obrigatórias

1. Todo model deve ter um método `to_dict()` que retorna apenas tipos serializáveis (str, int, bool) — sem objetos Python.
2. Validações de campo ficam no `__init__` do model, levantando `ValueError` com mensagem clara.
3. Datas e datetimes sempre exportados via `.isoformat()`.
4. A constraint `UNIQUE(habit_id, date)` em `HabitLog` é garantida no banco — trate `IntegrityError` nas rotas.

```python
# Padrão de validação no model
class Habit(db.Model):
    def __init__(self, name: str, description: str = ""):
        if not name or not name.strip():
            raise ValueError("Habit name cannot be empty")
        self.name = name.strip()
        self.description = description
```

### Rotas — Padrão de resposta

Todo endpoint retorna JSON. Use este padrão:

```python
# Sucesso
return jsonify(data), 200  # ou 201

# Erro de validação
return jsonify({"error": "mensagem descritiva"}), 400

# Não encontrado
return jsonify({"error": "Habit not found"}), 404

# Conflito (ex: duplicata)
return jsonify({"error": "Habit already completed for this date"}), 409
```

Nunca retorne strings cruas, HTML ou status sem body.

### Services — Funções puras

Os services em `app/services/` são funções Python puras — sem imports do Flask, sem acesso ao banco.

```python
# CORRETO — recebe dados já buscados, retorna valor calculado
def calculate_current_streak(logs: list[date]) -> int:
    ...

# ERRADO — service não deve consultar o banco
def calculate_current_streak(habit_id: int) -> int:
    logs = HabitLog.query.filter_by(habit_id=habit_id).all()  # NÃO
    ...
```

Isso garante que os testes unitários dos services rodem sem banco nem contexto Flask.

### Blueprints

Cada arquivo em `routes/` define um Blueprint. Todos são registrados em `routes/__init__.py` via `register_routes(app)`. Nunca importe rotas diretamente no `__init__.py` da app.

---

## Testes — Regras Críticas

### Três níveis, três contratos

| Nível | Localização | Usa banco? | Usa Flask? |
|---|---|---|---|
| Unitário | `tests/unit/` | ❌ Nunca | ❌ Nunca |
| Integração | `tests/integration/` | ✅ SQLite memória | ✅ test client |
| E2E | `frontend/e2e/` | ✅ banco real | ✅ app rodando |

### Fixtures obrigatórias (`conftest.py`)

Sempre use as fixtures definidas em `backend/tests/conftest.py`. Nunca crie conexões de banco manualmente dentro de um teste.

```python
# CORRETO — usa fixtures
def test_create_habit(client):
    response = client.post("/habits", json={"name": "Meditar"})
    assert response.status_code == 201

# ERRADO — cria banco manual
def test_create_habit():
    app = Flask(__name__)  # NÃO
    ...
```

### Isolamento entre testes

- Cada teste de integração recebe um banco limpo (a fixture `app` faz `db.create_all()` e `db.drop_all()` por teste).
- Testes unitários não podem ter efeito colateral — não escrevem arquivos, não modificam estado global.
- Testes E2E devem chamar `DELETE /test/reset` no `beforeEach` para limpar o banco entre cenários.

### Nomenclatura de testes

Use o padrão `test_<o_que_testa>_<condição>`:

```python
test_create_habit_success
test_create_habit_empty_name
test_streak_reset_on_gap
test_complete_habit_duplicate_same_day
```

### Testes unitários de services — helper de datas

Sempre use helpers relativos a `date.today()`, nunca datas hardcoded:

```python
# CORRETO
def days_ago(n):
    return date.today() - timedelta(days=n)

logs = [days_ago(2), days_ago(1), date.today()]

# ERRADO — vai quebrar com o tempo
logs = [date(2024, 1, 13), date(2024, 1, 14), date(2024, 1, 15)]
```

### Cobertura mínima

Rodar `pytest --cov=app` deve resultar em cobertura ≥ 80%. Os services e models são os mais críticos — alvo de 100% neles.

---

## Frontend — Convenções React

### Toda comunicação com API passa por `api.js`

Nunca chame `fetch` diretamente dentro de um componente ou página. Use sempre as funções de `frontend/src/services/api.js`.

```jsx
// CORRETO
import { getHabits } from '../services/api'
const habits = await getHabits()

// ERRADO
const res = await fetch('/habits')  // não no componente
```

### Separação páginas vs componentes

- **Páginas** (`pages/`): gerenciam estado, fazem chamadas à API, montam o layout.
- **Componentes** (`components/`): recebem props, renderizam UI, disparam callbacks — sem chamadas à API.

```jsx
// CORRETO — componente recebe dados via props
function HabitCard({ habit, onComplete, completedToday }) { ... }

// ERRADO — componente buscando dados sozinho
function HabitCard({ habitId }) {
  const [habit, setHabit] = useState(null)
  useEffect(() => fetch(`/habits/${habitId}`), []) // NÃO
}
```

### data-testid obrigatórios

Os atributos abaixo são necessários para os testes E2E. Nunca remova nem renomeie.

| Elemento | `data-testid` |
|---|---|
| Input de nome | `habit-name-input` |
| Botão adicionar | `add-habit-btn` |
| Card do hábito | `habit-card-{id}` |
| Botão concluir | `complete-btn-{id}` |
| Mensagem de erro do form | `form-error` |
| Mensagem já concluído | `already-completed-msg` |
| Container leaderboard | `leaderboard` |

### Estado de loading e erro

Toda página que faz chamada assíncrona deve ter estados `loading` e `error`:

```jsx
const [loading, setLoading] = useState(true)
const [error, setError] = useState(null)

useEffect(() => {
  getHabits()
    .then(setHabits)
    .catch(() => setError("Erro ao carregar hábitos"))
    .finally(() => setLoading(false))
}, [])

if (loading) return <p>Carregando...</p>
if (error) return <p>{error}</p>
```

### Proxy do Vite

O `vite.config.js` já está configurado com proxy para `/habits` e `/leaderboard` apontando para `localhost:5000`. Não adicione o host base nas chamadas do `api.js`:

```js
// CORRETO
fetch('/habits')

// ERRADO
fetch('http://localhost:5000/habits')
```

---

## Decisões de Design Documentadas

### Comportamento do streak sem conclusão hoje

**Decisão tomada:** *(preencher quando o grupo decidir)*

- **Opção A (estrito):** streak atual = 0 se hoje não foi concluído.
- **Opção B (flexível):** streak conta o último bloco consecutivo mesmo sem hoje.

Documente a decisão aqui e em um comentário no topo de `app/services/streak.py`.

### Pontuação

| streak | pontos |
|---|---|
| qualquer | +10 (base) |
| ≥ 7 dias | +50 (bônus) |
| ≥ 30 dias | +100 (bônus adicional) |

Bônus são **cumulativos**: streak=30 dá 10+50+100 = 160 pts.

### Cascade de deleção

Deletar um `Habit` remove automaticamente todos os `HabitLog`s e o `Score` associados (via `cascade="all, delete-orphan"` no relacionamento SQLAlchemy).

---

## O que Nunca Fazer

**Backend:**
- Nunca commitar o arquivo `tracker.db` (adicionar ao `.gitignore`).
- Nunca usar `db.session` fora de um contexto de app Flask.
- Nunca retornar objetos SQLAlchemy diretamente nas rotas — sempre chamar `.to_dict()`.
- Nunca colocar lógica de negócio (streak, pontuação) nas rotas.
- Nunca importar Flask ou SQLAlchemy dentro dos arquivos de `services/`.

**Testes:**
- Nunca usar datas hardcoded nos testes de streak.
- Nunca criar um fixture de banco fora do `conftest.py`.
- Nunca fazer teste de integração sem usar o `client` fixture.
- Nunca misturar assert de banco com assert HTTP no mesmo teste.

**Frontend:**
- Nunca fazer `fetch` dentro de um componente — use `api.js`.
- Nunca remover `data-testid` de elementos existentes.
- Nunca colocar lógica de cálculo (streak, badge) fora dos componentes dedicados (`StreakBadge`, `ScoreBoard`).

---

## Fluxo de PR por Task

Ao concluir a implementação de qualquer task, abra um Pull Request **antes** de reportar a task como concluída.

### Regras do PR

- **Branch:** crie uma branch com o padrão `task/<id>-<slug>`, ex: `task/02-habit-model`.
- **Título:** `[TASK-XX] Título resumido da task`.
- **Body:** use o template abaixo, preenchendo com base na spec da task:

```
## O que foi implementado
<bullet points do que foi feito — extraído diretamente da spec>

## Decisões relevantes
<qualquer escolha não óbvia feita durante a implementação>

## Como testar
<passos mínimos para verificar que a task funciona>

## Checklist
- [ ] pytest passa sem erros
- [ ] cobertura ≥ 80%
- [ ] npm run dev abre sem erros
```

- Nunca faça squash dos commits antes do PR ser revisado.
- O PR deve ser aberto **mesmo que não haja reviewer** — serve como registro da spec implementada.

---

## Checklist Antes de Considerar uma Task Concluída

- [ ] `pytest` passa sem erros ou warnings inesperados
- [ ] `pytest --cov=app` mostra cobertura ≥ 80%
- [ ] Nenhum import de Flask/SQLAlchemy em `tests/unit/` ou em `services/`
- [ ] Todos os endpoints retornam `Content-Type: application/json`
- [ ] Todos os `data-testid` listados acima estão presentes no HTML renderizado
- [ ] `npm run dev` abre sem erros no console do browser
- [ ] `tracker.db` está no `.gitignore`
- [ ] PR aberto com título `[TASK-XX] ...` e body seguindo o template da seção **Fluxo de PR por Task**