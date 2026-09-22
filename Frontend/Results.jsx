import { useEffect, useState } from 'react'
import { useParams, Link } from 'react-router-dom'
import { getResults } from '../api'
import Loader from '../components/Loader'
import FileTree from '../components/FileTree'
import ModuleCard from '../components/ModuleCard'
import IssueCard from '../components/IssueCard'
import DuplicateCard from '../components/DuplicateCard'
import MermaidDiagram from '../components/MermaidDiagram'
import StatCard from '../components/StatCard'
import ApiDocsViewer from '../components/ApiDocsViewer'

const TABS = [
  { key: 'overview',     label: '🗺️ Overview'     },
  { key: 'modules',      label: '📦 Modules'       },
  { key: 'security',     label: '🔐 Security'      },
  { key: 'performance',  label: '⚡ Performance'   },
  { key: 'duplicates',   label: '🔁 Duplicates'    },
  { key: 'apidocs',      label: '📄 API Docs'      },
]

export default function Results() {
  const { repoId } = useParams()
  const [data, setData]         = useState(null)
  const [loading, setLoading]   = useState(true)
  const [error, setError]       = useState('')
  const [activeTab, setActiveTab] = useState('overview')

  useEffect(() => {
    getResults(repoId)
      .then(setData)
      .catch(() => setError('Failed to load results. Make sure the backend is running.'))
      .finally(() => setLoading(false))
  }, [repoId])

  if (loading) return <Loader message="Loading analysis results…" />

  if (error) return (
    <div className="max-w-2xl mx-auto pt-12 text-center">
      <p className="text-5xl mb-4">❌</p>
      <p className="text-red-400 font-semibold text-lg">{error}</p>
      <Link to="/" className="btn-primary inline-block mt-6 text-sm py-2">← Back to Home</Link>
    </div>
  )

  const {
    repo_info, file_tree, modules = [],
    security_issues = [], performance_issues = [],
    duplicates = [], api_docs, diagram,
  } = data || {}

  const highSec  = security_issues.filter(i => i.severity === 'high').length
  const dupFiles = duplicates.reduce((n, d) => n + d.occurrences.length, 0)

  return (
    <div className="max-w-5xl mx-auto pb-16">

      {/* ── Breadcrumb + header ─────────────────────────────── */}
      <div className="flex items-start justify-between mb-6 flex-wrap gap-4">
        <div>
          <div className="flex items-center gap-2 mb-1 text-sm">
            <Link to="/" className="text-gray-500 hover:text-white transition-colors">Home</Link>
            <span className="text-gray-700">/</span>
            <Link to="/dashboard" className="text-gray-500 hover:text-white transition-colors">Dashboard</Link>
            <span className="text-gray-700">/</span>
            <span className="text-white font-mono">{repo_info?.name}</span>
          </div>
          <h1 className="text-2xl font-bold text-white">{repo_info?.name}</h1>
          <a
            href={repo_info?.url} target="_blank" rel="noreferrer"
            className="text-primary-400 hover:text-primary-300 text-sm font-mono transition-colors"
          >
            {repo_info?.url} ↗
          </a>
          {repo_info?.primary_language && (
            <span className="ml-3 badge bg-gray-800 text-gray-300 border border-gray-700 text-xs">
              {repo_info.primary_language}
            </span>
          )}
        </div>
        <Link to={`/chat/${repoId}`} className="btn-primary text-sm py-2 px-5">
          💬 Chat with Codebase
        </Link>
      </div>

      {/* ── Stats row ───────────────────────────────────────── */}
      <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3 mb-8">
        <StatCard icon="📄" label="Files"    value={repo_info?.file_count ?? 0}    color="text-blue-400"   />
        <StatCard icon="📦" label="Modules"  value={modules.length}                color="text-purple-400" />
        <StatCard
          icon="🔐" label="Security"
          value={security_issues.length}
          sub={highSec ? `${highSec} high` : 'All clear'}
          color={highSec ? 'text-red-400' : 'text-green-400'}
        />
        <StatCard icon="⚡" label="Perf Tips"    value={performance_issues.length}  color="text-yellow-400" />
        <StatCard
          icon="🔁" label="Duplicates"
          value={duplicates.length}
          sub={dupFiles ? `across ${dupFiles} files` : ''}
          color={duplicates.length ? 'text-orange-400' : 'text-green-400'}
        />
        <StatCard icon="📝" label="Analyzed" value={repo_info?.analyzed_at?.split(' ')[0] ?? '—'} color="text-gray-400" />
      </div>

      {/* ── Project summary banner ───────────────────────────── */}
      {repo_info?.summary && (
        <div className="card mb-6 border-l-4 border-l-primary-600">
          <p className="text-gray-300 leading-relaxed text-sm">{repo_info.summary}</p>
        </div>
      )}

      {/* ── Tab bar ─────────────────────────────────────────── */}
      <div className="flex gap-1 bg-gray-900 border border-gray-800 rounded-xl p-1 mb-6 overflow-x-auto">
        {TABS.map(tab => (
          <button
            key={tab.key}
            onClick={() => setActiveTab(tab.key)}
            className={`px-3 py-2 rounded-lg text-xs font-medium whitespace-nowrap transition-colors flex-1 ${
              activeTab === tab.key
                ? 'bg-primary-600 text-white'
                : 'text-gray-400 hover:text-white hover:bg-gray-800'
            }`}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {/* ── Tab: Overview ───────────────────────────────────── */}
      {activeTab === 'overview' && (
        <div className="space-y-6">
          <div className="card">
            <h2 className="text-lg font-semibold text-white mb-4">Architecture Diagram</h2>
            <MermaidDiagram chart={diagram} />
          </div>
          <div className="card">
            <h2 className="text-lg font-semibold text-white mb-4">File Tree</h2>
            <FileTree tree={file_tree} />
          </div>
        </div>
      )}

      {/* ── Tab: Modules ────────────────────────────────────── */}
      {activeTab === 'modules' && (
        <div className="space-y-4">
          <p className="text-gray-400 text-sm">{modules.length} modules analysed</p>
          {modules.length > 0
            ? modules.map((m, i) => <ModuleCard key={i} module={m} />)
            : <Empty icon="📦" msg="No modules found." />}
        </div>
      )}

      {/* ── Tab: Security ───────────────────────────────────── */}
      {activeTab === 'security' && (
        <div className="space-y-4">
          <SecuritySummary issues={security_issues} />
          {security_issues.length > 0
            ? security_issues.map((iss, i) => <IssueCard key={i} issue={iss} />)
            : <Empty icon="✅" msg="No security issues detected." color="text-green-400" />}
        </div>
      )}

      {/* ── Tab: Performance ────────────────────────────────── */}
      {activeTab === 'performance' && (
        <div className="space-y-4">
          <p className="text-gray-400 text-sm">{performance_issues.length} suggestions</p>
          {performance_issues.length > 0
            ? performance_issues.map((iss, i) => (
                <IssueCard key={i} issue={{ ...iss, severity: 'medium' }} />
              ))
            : <Empty icon="⚡" msg="No performance issues detected." color="text-yellow-400" />}
        </div>
      )}

      {/* ── Tab: Duplicates ─────────────────────────────────── */}
      {activeTab === 'duplicates' && (
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <p className="text-gray-400 text-sm">{duplicates.length} duplicate groups found</p>
            {duplicates.length > 0 && (
              <span className="badge bg-orange-950 text-orange-300 border border-orange-800">
                {dupFiles} file occurrences
              </span>
            )}
          </div>
          {duplicates.length > 0
            ? duplicates.map((g, i) => <DuplicateCard key={i} group={g} index={i} />)
            : <Empty icon="✅" msg="No duplicate code blocks detected." color="text-green-400" />}
        </div>
      )}

      {/* ── Tab: API Docs ────────────────────────────────────── */}
      {activeTab === 'apidocs' && (
        <ApiDocsViewer docs={api_docs} />
      )}
    </div>
  )
}

// ── Small helpers ─────────────────────────────────────────────────

function Empty({ icon, msg, color = 'text-gray-400' }) {
  return (
    <div className="card text-center py-14">
      <p className="text-4xl mb-3">{icon}</p>
      <p className={`font-semibold ${color}`}>{msg}</p>
    </div>
  )
}

function SecuritySummary({ issues }) {
  const counts = { high: 0, medium: 0, low: 0, info: 0 }
  issues.forEach(i => { counts[i.severity] = (counts[i.severity] || 0) + 1 })

  return (
    <div className="grid grid-cols-4 gap-3 mb-2">
      {[
        { sev: 'high',   color: 'text-red-400',    bg: 'bg-red-950 border-red-800'    },
        { sev: 'medium', color: 'text-yellow-400',  bg: 'bg-yellow-950 border-yellow-800' },
        { sev: 'low',    color: 'text-blue-400',    bg: 'bg-blue-950 border-blue-800'  },
        { sev: 'info',   color: 'text-gray-400',    bg: 'bg-gray-900 border-gray-700'  },
      ].map(({ sev, color, bg }) => (
        <div key={sev} className={`rounded-xl border p-3 text-center ${bg}`}>
          <p className={`text-2xl font-bold ${color}`}>{counts[sev] || 0}</p>
          <p className={`text-xs capitalize ${color}`}>{sev}</p>
        </div>
      ))}
    </div>
  )
}
