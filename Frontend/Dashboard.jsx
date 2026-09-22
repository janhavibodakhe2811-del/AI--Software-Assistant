import { useEffect, useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { listRepos, deleteRepo } from '../api'
import Loader from '../components/Loader'

export default function Dashboard() {
  const [repos, setRepos] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const navigate = useNavigate()

  const fetchRepos = async () => {
    try {
      const data = await listRepos()
      setRepos(data.repos || [])
    } catch {
      setError('Could not load repositories. Make sure the backend is running.')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => { fetchRepos() }, [])

  const handleDelete = async (repoId, e) => {
    e.preventDefault()
    if (!window.confirm('Delete this analysis?')) return
    try {
      await deleteRepo(repoId)
      setRepos(r => r.filter(x => x.repo_id !== repoId))
    } catch {
      alert('Failed to delete.')
    }
  }

  if (loading) return <Loader message="Loading dashboard..." />

  return (
    <div className="max-w-4xl mx-auto">
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-2xl font-bold text-white">Dashboard</h1>
          <p className="text-gray-400 text-sm mt-1">All analyzed repositories</p>
        </div>
        <button onClick={() => navigate('/')} className="btn-primary text-sm py-2">
          + Analyze New Repo
        </button>
      </div>

      {error && (
        <div className="card border-red-800 bg-red-950 mb-6">
          <p className="text-red-400 text-sm">⚠️ {error}</p>
        </div>
      )}

      {repos.length === 0 && !error ? (
        <div className="card text-center py-16">
          <p className="text-4xl mb-4">📭</p>
          <p className="text-gray-300 font-semibold">No repositories analyzed yet</p>
          <p className="text-gray-500 text-sm mt-2 mb-6">Go to Home and paste a GitHub URL to get started.</p>
          <Link to="/" className="btn-primary inline-block text-sm py-2">
            Analyze a Repository
          </Link>
        </div>
      ) : (
        <div className="space-y-4">
          {repos.map(repo => (
            <Link
              key={repo.repo_id}
              to={`/results/${repo.repo_id}`}
              className="card flex items-center justify-between hover:border-primary-700 transition-colors group"
            >
              <div className="flex items-center gap-4 min-w-0">
                <div className="w-10 h-10 bg-primary-900 rounded-xl flex items-center justify-center shrink-0">
                  <span className="text-primary-300 font-bold text-sm">
                    {repo.name?.charAt(0)?.toUpperCase() || 'R'}
                  </span>
                </div>
                <div className="min-w-0">
                  <p className="text-white font-semibold truncate">{repo.name}</p>
                  <p className="text-gray-500 text-xs font-mono truncate">{repo.url}</p>
                  <div className="flex items-center gap-3 mt-1">
                    <span className="text-gray-600 text-xs">{repo.file_count} files</span>
                    <span className="text-gray-600 text-xs">•</span>
                    <span className="text-gray-600 text-xs">{repo.analyzed_at}</span>
                  </div>
                </div>
              </div>
              <div className="flex items-center gap-2 shrink-0 ml-4">
                <span className={`badge border ${
                  repo.status === 'completed'
                    ? 'bg-green-950 text-green-300 border-green-800'
                    : repo.status === 'processing'
                    ? 'bg-yellow-950 text-yellow-300 border-yellow-800'
                    : 'bg-red-950 text-red-300 border-red-800'
                }`}>
                  {repo.status}
                </span>
                <button
                  onClick={(e) => handleDelete(repo.repo_id, e)}
                  className="p-2 text-gray-600 hover:text-red-400 hover:bg-red-950 rounded-lg transition-colors opacity-0 group-hover:opacity-100"
                  title="Delete"
                >
                  🗑️
                </button>
              </div>
            </Link>
          ))}
        </div>
      )}
    </div>
  )
}
