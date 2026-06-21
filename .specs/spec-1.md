# SPEC-01 — Project Setup

**Dependência:** 🟢 INDEPENDENTE — deve ser a primeira task executada
**Bloqueia:** SPEC-02, SPEC-03, SPEC-05

---

## Objetivo

Criar a estrutura de pastas do monorepo, arquivos de configuração e garantir que tanto o backend Flask quanto o frontend React inicializam sem erros.

---

## Estrutura de Diretórios a Criar

```
tracker-plus/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── database.py
│   │   └── routes/
│   │       └── __init__.py
│   ├── tests/
│   │   ├── conftest.py
│   │   ├── unit/
│   │   │   └── .gitkeep
│   │   └── integration/
│   │       └── .gitkeep
│   ├── requirements.txt
│   └── run.py
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   ├── components/
│   │   │   └── .gitkeep
│   │   ├── pages/
│   │   │   └── .gitkeep
│   │   └── services/
│   │       └── api.js
│   ├── e2e/
│   │   └── .gitkeep
│   ├── package.json
│   ├── vite.config.js
│   └── index.html
├── .gitignore
└── CLAUDE.md
```

---

## Arquivos a Implementar

### `.gitignore`

```
backend/tracker.db
backend/__pycache__/
backend/.pytest_cache/
backend/.coverage
frontend/node_modules/
frontend/dist/
frontend/playwright-report/
```

### `backend/requirements.txt`

```
flask>=3.0
flask-sqlalchemy>=3.1
flask-cors>=4.0
pytest>=8.0
pytest-cov>=5.0
pytest-flask>=1.3
```

### `backend/app/__init__.py` — Flask Application Factory

```python
from flask import Flask
from flask_cors import CORS
from .database import db

def create_app(testing: bool = False) -> Flask:
    app = Flask(__name__)

    if testing:
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        app.config["TESTING"] = True
    else:
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tracker.db"

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    CORS(app)
    db.init_app(app)

    from .routes import register_routes
    register_routes(app)

    return app
```

### `backend/app/database.py`

```python
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
```

### `backend/app/routes/__init__.py`

```python
def register_routes(app):
    pass  # rotas serão registradas nas tasks seguintes
```

### `backend/run.py`

```python
from app import create_app
from app.database import db

app = create_app()

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)
```

### `backend/tests/conftest.py`

```python
import pytest
from app import create_app
from app.database import db as _db

@pytest.fixture(scope="function")
def app():
    app = create_app(testing=True)
    with app.app_context():
        _db.create_all()
        yield app
        _db.session.remove()
        _db.drop_all()

@pytest.fixture(scope="function")
def client(app):
    return app.test_client()

@pytest.fixture(scope="function")
def db(app):
    return _db
```

### `frontend/package.json`

```json
{
  "name": "tracker-plus-frontend",
  "version": "0.1.0",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview",
    "test:e2e": "playwright test",
    "test:e2e:ui": "playwright test --ui"
  },
  "dependencies": {
    "react": "^18.3.0",
    "react-dom": "^18.3.0",
    "react-router-dom": "^6.22.0"
  },
  "devDependencies": {
    "@vitejs/plugin-react": "^4.2.0",
    "@playwright/test": "^1.44.0",
    "vite": "^5.2.0"
  }
}
```

### `frontend/vite.config.js`

```js
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      '/habits': 'http://localhost:5000',
      '/leaderboard': 'http://localhost:5000',
    }
  }
})
```

### `frontend/src/services/api.js`

```js
const BASE_URL = '/habits'

export async function getHabits() {
  const res = await fetch(BASE_URL)
  return res.json()
}

export async function createHabit(name, description = '') {
  const res = await fetch(BASE_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ name, description }),
  })
  return { ok: res.ok, status: res.status, data: await res.json() }
}

export async function deleteHabit(id) {
  const res = await fetch(`${BASE_URL}/${id}`, { method: 'DELETE' })
  return res.json()
}

export async function completeHabit(id, date = null) {
  const body = date ? { date } : {}
  const res = await fetch(`${BASE_URL}/${id}/complete`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  })
  return { ok: res.ok, status: res.status, data: await res.json() }
}

export async function getStreak(id) {
  const res = await fetch(`${BASE_URL}/${id}/streak`)
  return res.json()
}

export async function getScore(id) {
  const res = await fetch(`${BASE_URL}/${id}/score`)
  return res.json()
}

export async function getLeaderboard() {
  const res = await fetch('/leaderboard')
  return res.json()
}
```

### `frontend/src/App.jsx`

```jsx
import { BrowserRouter, Routes, Route } from 'react-router-dom'

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<div>Dashboard (a implementar)</div>} />
        <Route path="/stats" element={<div>Stats (a implementar)</div>} />
      </Routes>
    </BrowserRouter>
  )
}
```

---

## Testes

Esta task não produz testes próprios. Ela cria a infraestrutura que viabiliza todos os testes das tasks seguintes:

- O `conftest.py` define as fixtures `app`, `client` e `db` usadas por todos os testes de integração.
- O banco SQLite em memória (`sqlite:///:memory:`) garante isolamento entre testes.
- A `create_app(testing=True)` é o ponto de entrada de toda suíte de testes do backend.

**Verificação:** `cd backend && pytest` deve rodar sem erros (zero testes coletados é aceitável neste ponto).

---

## Critério de Conclusão

- `cd backend && pip install -r requirements.txt && python run.py` inicia sem erros.
- `cd frontend && npm install && npm run dev` abre o React em `localhost:5173`.
- `tracker.db` não aparece no controle de versão (`.gitignore` configurado).
- `cd backend && pytest` roda sem erros.