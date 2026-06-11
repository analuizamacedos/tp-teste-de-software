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
