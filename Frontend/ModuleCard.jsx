export default function ModuleCard({ module }) {
  const typeColors = {
    service: 'bg-blue-900 text-blue-300 border-blue-700',
    route: 'bg-green-900 text-green-300 border-green-700',
    model: 'bg-purple-900 text-purple-300 border-purple-700',
    config: 'bg-yellow-900 text-yellow-300 border-yellow-700',
    utility: 'bg-orange-900 text-orange-300 border-orange-700',
    component: 'bg-pink-900 text-pink-300 border-pink-700',
    unknown: 'bg-gray-800 text-gray-300 border-gray-700',
  }

  const color = typeColors[module.type?.toLowerCase()] || typeColors.unknown

  return (
    <div className="card hover:border-primary-700 transition-colors">
      <div className="flex items-start justify-between gap-4 mb-3">
        <div>
          <h3 className="font-semibold text-white text-sm font-mono">{module.path}</h3>
          <p className="text-gray-400 text-xs mt-0.5">{module.language}</p>
        </div>
        <span className={`badge border ${color} shrink-0`}>{module.type || 'unknown'}</span>
      </div>
      <p className="text-gray-300 text-sm leading-relaxed">{module.summary}</p>

      {module.functions && module.functions.length > 0 && (
        <div className="mt-3 pt-3 border-t border-gray-800">
          <p className="text-xs text-gray-500 mb-2">Key functions / classes:</p>
          <div className="flex flex-wrap gap-1">
            {module.functions.slice(0, 6).map((fn, i) => (
              <span key={i} className="px-2 py-0.5 bg-gray-800 rounded text-xs font-mono text-gray-300">
                {fn}
              </span>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}
