# SPEC-05 — Frontend React

**Dependência:** 🟡 DEPENDE DE: SPEC-01
**Pode ser executada em paralelo com:** SPEC-02, SPEC-03, SPEC-04
**Bloqueia:** SPEC-07

---

## Objetivo

Implementar a interface React com páginas Dashboard e Stats, todos os componentes visuais e o sistema de badges. O frontend pode ser desenvolvido com dados mockados enquanto o backend não estiver pronto — basta trocar para as chamadas reais do `api.js` quando TASK-04 e TASK-06 estiverem prontas.

---

## Páginas a Implementar

### `frontend/src/pages/Dashboard.jsx`

**Responsabilidades:**
- Exibir a lista de hábitos.
- Permitir adicionar hábito via `AddHabitForm`.
- Permitir marcar hábito como concluído.
- Exibir feedback quando uma ação falha.

**Estado local:**
```js
const [habits, setHabits]     = useState([])
const [loading, setLoading]   = useState(true)
const [error, setError]       = useState(null)
```

**Fluxo de dados:**
1. `useEffect` → `getHabits()` → preenche `habits`.
2. Submit do form → `createHabit()` → adiciona à lista.
3. Click "Concluir hoje" → `completeHabit(id)` → atualiza UI.

---

### `frontend/src/pages/Stats.jsx`

**Responsabilidades:**
- Exibir leaderboard via `ScoreBoard`.
- Buscar dados com `getLeaderboard()` no `useEffect`.

---

## Componentes a Implementar

### `frontend/src/components/AddHabitForm.jsx`

**Props:** `onAdd(name, description)`

- Campo `name` obrigatório; campo `description` opcional.
- Submit com `name` vazio: exibe `"O nome do hábito é obrigatório"` em `[data-testid="form-error"]`. Não chama `onAdd`.
- Submit válido: chama `onAdd` e limpa os campos.

### `frontend/src/components/HabitList.jsx`

**Props:** `habits`, `onComplete`, `onDelete`, `completedIds` (Set)

- Renderiza `HabitCard` para cada item.
- Se `habits` vazio: exibe `"Nenhum hábito cadastrado. Adicione um acima!"`.

### `frontend/src/components/HabitCard.jsx`

**Props:** `habit`, `onComplete`, `onDelete`, `completedToday`, `streak`, `points`

- Exibe nome, descrição e `StreakBadge`.
- Botão `[data-testid="complete-btn-{id}"]`: se `completedToday`, fica desabilitado e exibe `[data-testid="already-completed-msg"]`.
- Botão "Excluir" chama `onDelete(habit.id)`.

### `frontend/src/components/StreakBadge.jsx`

**Props:** `streak: number`

| Condição     | Ícone | Texto             |
|--------------|-------|-------------------|
| streak >= 30 | 🏆    | "Mês invicto"     |
| streak >= 7  | ⚡    | "Semana perfeita" |
| streak >= 3  | 🔥    | "Em chamas"       |
| streak >= 1  | ✅    | "{n} dias"        |
| streak == 0  | —     | sem badge         |

### `frontend/src/components/ScoreBoard.jsx`

**Props:** `leaderboard: [{habit_id, name, points, streak}]`

| Condição      | Badge | Texto                   |
|---------------|-------|-------------------------|
| points >= 500 | 💎    | "Consistência diamante" |
| points >= 100 | ⭐    | "Iniciante dedicado"    |

---

## `data-testid` Obrigatórios

Estes atributos são exigidos pelos testes E2E da TASK-07. **Nunca remova nem renomeie.**

| Elemento | `data-testid` |
|---|---|
| Input de nome | `habit-name-input` |
| Botão adicionar | `add-habit-btn` |
| Card do hábito | `habit-card-{id}` |
| Botão concluir | `complete-btn-{id}` |
| Mensagem de erro do form | `form-error` |
| Mensagem já concluído | `already-completed-msg` |
| Container leaderboard | `leaderboard` |

---

## Estratégia para Desenvolver sem Backend

Usar dados mockados no `Dashboard.jsx` enquanto o backend não estiver disponível:

```js
const MOCK_HABITS = [
  { id: 1, name: "Beber água", description: "8 copos por dia", created_at: new Date().toISOString() },
  { id: 2, name: "Meditar", description: "", created_at: new Date().toISOString() },
]
```

Quando TASK-04 e TASK-06 estiverem prontas, substituir pelo `getHabits()` real.

---

## Testes

Esta task não produz testes automatizados próprios. Ela prepara a UI necessária para os testes E2E da TASK-07.

**Para considerar esta task pronta do ponto de vista de testes:**
- Todos os `data-testid` listados acima estão presentes no HTML renderizado (verificar com DevTools).
- O formulário bloqueia submit com nome vazio e exibe `[data-testid="form-error"]` visível.
- Clicar em "Concluir hoje" desabilita o botão e exibe `[data-testid="already-completed-msg"]`.
- A página de Stats renderiza o `[data-testid="leaderboard"]` mesmo que vazio.

---

## Critério de Conclusão

- `npm run dev` abre sem erros de console.
- É possível adicionar hábito, ver na lista e clicar em "Concluir hoje".
- Formulário com nome vazio mostra erro e não adiciona.
- Todos os `data-testid` estão presentes.