import { useState, useEffect } from 'react'
import AddHabitForm from '../components/AddHabitForm'
import HabitList from '../components/HabitList'
import { getHabits, createHabit, completeHabit, deleteHabit } from '../services/api'

export default function Dashboard() {
  const [habits, setHabits] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [completedIds, setCompletedIds] = useState(new Set())

  useEffect(() => {
    getHabits()
      .then(setHabits)
      .catch(() => setError('Erro ao carregar hábitos'))
      .finally(() => setLoading(false))
  }, [])

  async function handleAdd(name, description) {
    const result = await createHabit(name, description)
    if (result.ok) {
      setHabits(prev => [result.data, ...prev])
    } else {
      setError(result.data.error || 'Erro ao criar hábito')
    }
  }

  async function handleComplete(id) {
    const result = await completeHabit(id)
    if (result.ok || result.status === 409) {
      setCompletedIds(prev => new Set([...prev, id]))
    }
  }

  async function handleDelete(id) {
    await deleteHabit(id)
    setHabits(prev => prev.filter(h => h.id !== id))
    setCompletedIds(prev => {
      const next = new Set(prev)
      next.delete(id)
      return next
    })
  }

  if (loading) return <p>Carregando...</p>
  if (error) return <p>{error}</p>

  return (
    <div>
      <h1>Tracker+</h1>
      <AddHabitForm onAdd={handleAdd} />
      <HabitList
        habits={habits}
        onComplete={handleComplete}
        onDelete={handleDelete}
        completedIds={completedIds}
      />
    </div>
  )
}
