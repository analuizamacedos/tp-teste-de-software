import { useState } from 'react'

export default function AddHabitForm({ onAdd }) {
  const [name, setName] = useState('')
  const [description, setDescription] = useState('')
  const [error, setError] = useState('')

  function handleSubmit(e) {
    e.preventDefault()
    if (!name.trim()) {
      setError('O nome do hábito é obrigatório')
      return
    }
    setError('')
    onAdd(name.trim(), description.trim())
    setName('')
    setDescription('')
  }

  return (
    <form onSubmit={handleSubmit}>
      <input
        data-testid="habit-name-input"
        value={name}
        onChange={e => setName(e.target.value)}
        placeholder="Nome do hábito"
      />
      <input
        value={description}
        onChange={e => setDescription(e.target.value)}
        placeholder="Descrição (opcional)"
      />
      {error && <span data-testid="form-error">{error}</span>}
      <button data-testid="add-habit-btn" type="submit">Adicionar</button>
    </form>
  )
}
