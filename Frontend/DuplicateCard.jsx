export default function DuplicateCard({ group, index }) {
  return (
    <div className="card hover:border-orange-700 transition-colors">
      <div className="flex items-start justify-between gap-4 mb-3">
        <div className="flex items-center gap-2">
          <span className="w-6 h-6 bg-orange-900 text-orange-300 rounded-full flex items-center justify-center text-xs font-bold shrink-0">
            {index + 1}
          </span>
          <span className="badge bg-orange-950 text-orange-300 border border-orange-800">
            {group.occurrences.length} files
          </span>
          <span className="text-gray-500 text-xs">{group.line_count} lines</span>
        </div>
      </div>

      {/* Code preview */}
      <div className="bg-gray-950 rounded-lg px-4 py-3 mb-3 border border-gray-800 font-mono text-xs text-gray-400 truncate">
        {group.block_preview || 'Code block'}
      </div>

      {/* Occurrences */}
      <div className="space-y-1">
        <p className="text-xs text-gray-500 uppercase tracking-widest mb-2">Found in:</p>
        {group.occurrences.map((occ, i) => (
          <div key={i} className="flex items-center gap-2 text-sm">
            <span className="text-orange-400 text-xs">→</span>
            <span className="font-mono text-gray-300 truncate">{occ.file}</span>
            {occ.start_line && (
              <span className="text-gray-600 text-xs shrink-0">line {occ.start_line}</span>
            )}
          </div>
        ))}
      </div>
    </div>
  )
}
