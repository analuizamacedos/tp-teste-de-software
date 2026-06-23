export default function StreakBadge({ streak }) {
  if (streak >= 30) return <span>🏆 Mês invicto</span>
  if (streak >= 7) return <span>⚡ Semana perfeita</span>
  if (streak >= 3) return <span>🔥 Em chamas</span>
  if (streak >= 1) return <span>✅ {streak} dias</span>
  return null
}
