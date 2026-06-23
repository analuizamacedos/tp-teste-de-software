# SPEC-07 — Testes End-to-End com Playwright

**Dependência:** 🔴 DEPENDE DE: SPEC-04, SPEC-05, SPEC-06
**Última task — não bloqueia nenhuma outra**

---

## Objetivo

Configurar o Playwright e implementar os 5 testes E2E que simulam o fluxo completo do usuário com o sistema rodando (backend + frontend).

---

## Pré-requisitos

- Backend rodando em `http://localhost:4321`
- Frontend rodando em `http://localhost:5173`
- Todos os `data-testid` da TASK-05 presentes no HTML

---

## Configuração

### Instalar dependências

```bash
cd frontend
npm install --save-dev @playwright/test
npx playwright install chromium
```

### `frontend/playwright.config.js`

```js
import { defineConfig } from '@playwright/test'

export default defineConfig({
  testDir: './e2e',
  timeout: 30_000,
  use: {
    baseURL: 'http://localhost:5173',
    headless: true,
  },
  webServer: [
    {
      command: 'cd ../backend && python run.py',
      url: 'http://localhost:4321/habits',
      reuseExistingServer: true,
      timeout: 10_000,
    },
    {
      command: 'npm run dev',
      url: 'http://localhost:5173',
      reuseExistingServer: true,
    },
  ],
})
```

### Endpoint de reset no backend (obrigatório para isolamento)

Adicionar em `backend/app/routes/habits.py`:

```python
@habits_bp.route("/test/reset", methods=["DELETE"])
def reset_db():
    from flask import current_app
    from app.models import HabitLog, Score, Habit
    db.session.query(HabitLog).delete()
    db.session.query(Score).delete()
    db.session.query(Habit).delete()
    db.session.commit()
    return {"message": "Database reset"}, 200
```

---

## Testes

### Arquivo: `frontend/e2e/habits.spec.js`

> Testes E2E — simulam interação real do usuário no browser. O `beforeEach` limpa o banco via API para garantir isolamento.

```js
import { test, expect } from '@playwright/test'

test.beforeEach(async ({ request }) => {
  await request.delete('http://localhost:4321/test/reset')
})
```

---

#### E-01 — Criar hábito aparece na lista

**Requisito:** RE-01

| Passo | Ação | Verificação |
|---|---|---|
| 1 | Navega para `/` | — |
| 2 | Preenche `[data-testid="habit-name-input"]` com `"Meditar"` | — |
| 3 | Clica em `[data-testid="add-habit-btn"]` | — |
| 4 | — | Elemento `[data-testid^="habit-card-"]` está visível |
| 5 | — | Texto "Meditar" está presente na página |

```js
test('E-01: criar hábito aparece na lista', async ({ page }) => {
  await page.goto('/')
  await page.getByTestId('habit-name-input').fill('Meditar')
  await page.getByTestId('add-habit-btn').click()
  await expect(page.locator('[data-testid^="habit-card-"]')).toBeVisible()
  await expect(page.getByText('Meditar')).toBeVisible()
})
```

---

#### E-02 — Formulário bloqueia nome vazio

**Requisito:** RE-02

| Passo | Ação | Verificação |
|---|---|---|
| 1 | Navega para `/` | — |
| 2 | Deixa o input vazio | — |
| 3 | Clica em `[data-testid="add-habit-btn"]` | — |
| 4 | — | `[data-testid="form-error"]` está visível |
| 5 | — | Nenhum `[data-testid^="habit-card-"]` foi adicionado |

```js
test('E-02: formulário bloqueia nome vazio', async ({ page }) => {
  await page.goto('/')
  await page.getByTestId('add-habit-btn').click()
  await expect(page.getByTestId('form-error')).toBeVisible()
  await expect(page.locator('[data-testid^="habit-card-"]')).toHaveCount(0)
})
```

---

#### E-03 — Marcar hábito como concluído desabilita o botão

**Requisito:** RE-03

| Passo | Ação | Verificação |
|---|---|---|
| 1 | Navega para `/` | — |
| 2 | Cria hábito "Exercício" | — |
| 3 | Aguarda card aparecer | — |
| 4 | Clica no botão `[data-testid^="complete-btn-"]` | — |
| 5 | — | O mesmo botão está desabilitado |

```js
test('E-03: marcar concluído desabilita o botão', async ({ page }) => {
  await page.goto('/')
  await page.getByTestId('habit-name-input').fill('Exercício')
  await page.getByTestId('add-habit-btn').click()
  const completeBtn = page.locator('[data-testid^="complete-btn-"]').first()
  await completeBtn.waitFor({ state: 'visible' })
  await completeBtn.click()
  await expect(completeBtn).toBeDisabled()
})
```

---

#### E-04 — Não permite concluir duas vezes no mesmo dia

**Requisito:** RE-04

| Passo | Ação | Verificação |
|---|---|---|
| 1 | Navega para `/` | — |
| 2 | Cria hábito "Yoga" | — |
| 3 | Aguarda card aparecer | — |
| 4 | Clica em "Concluir hoje" | — |
| 5 | Tenta clicar novamente | — |
| 6 | — | `[data-testid="already-completed-msg"]` está visível OU botão está desabilitado |

```js
test('E-04: não permite concluir duas vezes no mesmo dia', async ({ page }) => {
  await page.goto('/')
  await page.getByTestId('habit-name-input').fill('Yoga')
  await page.getByTestId('add-habit-btn').click()
  const completeBtn = page.locator('[data-testid^="complete-btn-"]').first()
  await completeBtn.waitFor({ state: 'visible' })
  await completeBtn.click()

  // Após primeira conclusão, botão deve estar desabilitado ou msg visível
  const isDisabled = await completeBtn.isDisabled()
  const msgVisible = await page.getByTestId('already-completed-msg').isVisible()
  expect(isDisabled || msgVisible).toBe(true)
})
```

---

#### E-05 — Hábito concluído aparece com pontuação no leaderboard

**Requisito:** RE-05

| Passo | Ação | Verificação |
|---|---|---|
| 1 | Navega para `/` | — |
| 2 | Cria hábito "Ler" | — |
| 3 | Aguarda card aparecer | — |
| 4 | Clica em "Concluir hoje" | — |
| 5 | Navega para `/stats` | — |
| 6 | — | `[data-testid="leaderboard"]` está visível |
| 7 | — | Texto "Ler" está presente no leaderboard |

```js
test('E-05: hábito concluído aparece no leaderboard', async ({ page }) => {
  await page.goto('/')
  await page.getByTestId('habit-name-input').fill('Ler')
  await page.getByTestId('add-habit-btn').click()
  const completeBtn = page.locator('[data-testid^="complete-btn-"]').first()
  await completeBtn.waitFor({ state: 'visible' })
  await completeBtn.click()

  await page.goto('/stats')
  await expect(page.getByTestId('leaderboard')).toBeVisible()
  await expect(page.getByText('Ler')).toBeVisible()
})
```

---

## Resumo dos Testes E2E

| # | Teste | Requisito |
|---|---|---|
| E-01 | `criar hábito aparece na lista` | RE-01 |
| E-02 | `formulário bloqueia nome vazio` | RE-02 |
| E-03 | `marcar concluído desabilita o botão` | RE-03 |
| E-04 | `não permite concluir duas vezes no mesmo dia` | RE-04 |
| E-05 | `hábito concluído aparece no leaderboard` | RE-05 |

---

## Executar

```bash
cd frontend
npm run test:e2e
```

---

## Critério de Conclusão

- `npm run test:e2e` com backend e frontend rodando → 5 testes passam.
- Os testes rodam em modo headless.
- Cada teste começa com banco limpo via `DELETE /test/reset`.