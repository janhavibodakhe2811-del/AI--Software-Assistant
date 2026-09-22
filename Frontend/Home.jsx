import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { analyzeRepo } from '../api'
import ProgressLoader from '../components/ProgressLoader'

const EXAMPLE_REPOS = [
  'https://github.com/tiangolo/fastapi',
  'https://github.com/pallets/flask',
  'https://github.com/expressjs/express',
]

export default function Home() {
  const [url, setUrl] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const navigate = useNavigate()

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!url.trim()) return

    // Basic GitHub URL validation
    if (!url.includes('github.com')) {
      setError('Please enter a valid GitHub repository URL.')
      return
    }

    setError('')
    setLoading(true)
    try {
      const result = await analyzeRepo(url.trim())
      navigate(`/results/${result.repo_id}`)
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to analyze repository. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  if (loading) return <ProgressLoader repoUrl={url} />

  return (
    <div className="max-w-3xl mx-auto pt-12 pb-24">
      {/* Hero */}
      <div className="text-center mb-12">
        <div className="inline-flex items-center gap-2 bg-primary-900 border border-primary-700 rounded-full px-4 py-1.5 text-primary-300 text-sm mb-6">
          <span className="w-2 h-2 bg-primary-400 rounded-full animate-pulse"></span>
          AI-Powered Code Analysis
        </div>
        <h1 className="text-5xl font-bold text-white leading-tight mb-4">
          Understand Any<br />
          <span className="text-primary-500">Codebase in Seconds</span>
        </h1>
        <p className="text-gray-400 text-lg leading-relaxed">
          Paste a GitHub repository URL and our AI will analyze the entire project —
          architecture diagrams, module explanations, security issues, and more.
        </p>
      </div>

      {/* Input form */}
      <form onSubmit={handleSubmit} className="card mb-6">
        <label className="block text-sm font-medium text-gray-300 mb-2">
          GitHub Repository URL
        </label>
        <div className="flex gap-3">
          <input
            type="url"
            value={url}
            onChange={e => setUrl(e.target.value)}
            placeholder="https://github.com/username/repository"
            className="flex-1 bg-gray-800 border border-gray-700 rounded-xl px-4 py-3 text-white placeholder-gray-500 focus:outline-none focus:border-primary-500 focus:ring-1 focus:ring-primary-500 transition-colors font-mono text-sm"
          />
          <button type="submit" className="btn-primary whitespace-nowrap" disabled={!url.trim()}>
            Analyze →
          </button>
        </div>
        {error && (
          <p className="mt-3 text-red-400 text-sm flex items-center gap-2">
            <span>⚠️</span> {error}
          </p>
        )}
      </form>

      {/* Example repos */}
      <div className="mb-12">
        <p className="text-gray-500 text-xs uppercase tracking-widest mb-3 text-center">Try an example</p>
        <div className="flex flex-wrap gap-2 justify-center">
          {EXAMPLE_REPOS.map(repo => (
            <button
              key={repo}
              onClick={() => setUrl(repo)}
              className="px-3 py-1.5 bg-gray-800 hover:bg-gray-700 border border-gray-700 rounded-lg text-xs font-mono text-gray-300 transition-colors"
            >
              {repo.replace('https://github.com/', '')}
            </button>
          ))}
        </div>
      </div>

      {/* Features grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        {[
          { icon: '🗺️', title: 'Architecture Diagram', desc: 'Visual map of the entire project structure' },
          { icon: '📖', title: 'Module Explanations', desc: 'AI explains every file and what it does' },
          { icon: '🔐', title: 'Security Scanner', desc: 'Detects hardcoded secrets & vulnerabilities' },
          { icon: '⚡', title: 'Performance Tips', desc: 'AI-driven optimization recommendations' },
          { icon: '🔁', title: 'Duplicate Finder', desc: 'Identifies repeated code across files' },
          { icon: '💬', title: 'Q&A Chat', desc: 'Ask anything about the codebase' },
        ].map(f => (
          <div key={f.title} className="card flex items-start gap-3 hover:border-gray-700 transition-colors">
            <span className="text-2xl">{f.icon}</span>
            <div>
              <p className="font-semibold text-white text-sm">{f.title}</p>
              <p className="text-gray-400 text-xs mt-0.5">{f.desc}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
