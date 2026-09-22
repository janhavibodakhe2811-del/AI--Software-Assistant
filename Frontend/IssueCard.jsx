const severityConfig = {
  high:   { color: 'text-red-400',    bg: 'bg-red-950 border-red-800',    dot: 'bg-red-500' },
  medium: { color: 'text-yellow-400', bg: 'bg-yellow-950 border-yellow-800', dot: 'bg-yellow-500' },
  low:    { color: 'text-blue-400',   bg: 'bg-blue-950 border-blue-800',  dot: 'bg-blue-500' },
  info:   { color: 'text-gray-400',   bg: 'bg-gray-900 border-gray-700',  dot: 'bg-gray-500' },
}

export default function IssueCard({ issue }) {
  const cfg = severityConfig[issue.severity?.toLowerCase()] || severityConfig.info

  return (
    <div className={`rounded-xl border p-4 ${cfg.bg}`}>
      <div className="flex items-start gap-3">
        <span className={`mt-1.5 w-2 h-2 rounded-full shrink-0 ${cfg.dot}`}></span>
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 flex-wrap mb-1">
            <span className={`text-xs font-semibold uppercase tracking-wide ${cfg.color}`}>
              {issue.severity}
            </span>
            <span className="text-gray-500 text-xs">•</span>
            <span className="text-gray-400 text-xs font-mono truncate">{issue.file}</span>
            {issue.line && (
              <span className="text-gray-600 text-xs">line {issue.line}</span>
            )}
          </div>
          <p className="text-white text-sm font-medium">{issue.title}</p>
          <p className="text-gray-400 text-sm mt-1 leading-relaxed">{issue.description}</p>
          {issue.suggestion && (
            <p className="text-green-400 text-xs mt-2">
              💡 {issue.suggestion}
            </p>
          )}
        </div>
      </div>
    </div>
  )
}
