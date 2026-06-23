import HabitCard from './HabitCard'

export default function HabitList({ habits, onComplete, onDelete, completedIds }) {
  if (habits.length === 0) {
    return <p>Nenhum hábito cadastrado. Adicione um acima!</p>
  }
  return (
    <div>
      {habits.map(habit => (
        <HabitCard
          key={habit.id}
          habit={habit}
          onComplete={onComplete}
          onDelete={onDelete}
          completedToday={completedIds.has(habit.id)}
        />
      ))}
    </div>
  )
}
