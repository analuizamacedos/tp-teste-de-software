function scoreBadge(points) {
  if (points >= 500) return '💎 Consistência diamante'
  if (points >= 100) return '⭐ Iniciante dedicado'
  return null
}

export default function ScoreBoard({ leaderboard }) {
  return (
    <div data-testid="leaderboard">
      {leaderboard.length === 0 && <p>Nenhum dado disponível ainda.</p>}
      {leaderboard.map((entry, i) => (
        <div key={entry.habit_id}>
          <span>{i + 1}. {entry.name}</span>
          <span> — {entry.points} pts</span>
          {scoreBadge(entry.points) && <span> {scoreBadge(entry.points)}</span>}
        </div>
      ))}
    </div>
  )
}
