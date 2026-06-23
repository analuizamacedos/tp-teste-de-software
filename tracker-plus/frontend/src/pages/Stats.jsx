import { useState, useEffect } from 'react'
import ScoreBoard from '../components/ScoreBoard'
import { getLeaderboard } from '../services/api'

export default function Stats() {
  const [leaderboard, setLeaderboard] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    getLeaderboard()
      .then(setLeaderboard)
      .catch(() => setError('Erro ao carregar leaderboard'))
      .finally(() => setLoading(false))
  }, [])

  if (loading) return <p>Carregando...</p>
  if (error) return <p>{error}</p>

  return (
    <div>
      <h1>Estatísticas</h1>
      <ScoreBoard leaderboard={leaderboard} />
    </div>
  )
}
