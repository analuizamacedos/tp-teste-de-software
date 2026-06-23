import StreakBadge from './StreakBadge'

export default function HabitCard({ habit, onComplete, onDelete, completedToday, streak = 0, points = 0 }) {
  return (
    <div data-testid={`habit-card-${habit.id}`}>
      <h3>{habit.name}</h3>
      {habit.description && <p>{habit.description}</p>}
      <StreakBadge streak={streak} />
      <button
        data-testid={`complete-btn-${habit.id}`}
        onClick={() => onComplete(habit.id)}
        disabled={completedToday}
      >
        {completedToday ? 'Concluído hoje' : 'Concluir hoje'}
      </button>
      {completedToday && (
        <span data-testid="already-completed-msg">Já concluído hoje!</span>
      )}
      <button onClick={() => onDelete(habit.id)}>Excluir</button>
    </div>
  )
}
