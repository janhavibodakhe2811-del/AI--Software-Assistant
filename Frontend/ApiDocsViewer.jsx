import { useState } from 'react'

// Minimal markdown-to-HTML renderer for API docs
function renderMarkdown(text) {
  if (!text) return ''
  return text
    // h3
    .replace(/^### (.+)$/gm, '<h3 class="text-primary-400 font-bold text-base mt-6 mb-2 font-mono">$1</h3>')
    // h2
    .replace(/^## (.+)$/gm, '<h2 class="text-white font-bold text-lg mt-8 mb-3">$2</h2>')
    // bold
    .replace(/\*\*(.+?)\*\*/g, '<strong class="text-gray-200">$1</strong>')
    // inline code
    .replace(/`([^`]+)`/g, '<code class="bg-gray-800 text-primary-300 px-1.5 py-0.5 rounded text-xs font-mono">$1</code>')
    // bullet points
    .replace(/^- (.+)$/gm, '<li class="text-gray-400 text-sm ml-4 list-disc">$1</li>')
    // wrap list items
    .replace(/(<li.*<\/li>\n?)+/g, '<ul class="space-y-1 mb-2">$&</ul>')
    // horizontal rule
    .replace(/^---$/gm, '<hr class="border-gray-800 my-4">')
    // line breaks
    .replace(/\n{2,}/g, '</p><p class="text-gray-400 text-sm mb-2">')
}

export default function ApiDocsViewer({ docs }) {
  const [view, setView] = useState('rendered')   // 'rendered' | 'raw'

  if (!docs) {
    return (
      <div className="card text-center py-12">
        <p className="text-4xl mb-3">📭</p>
        <p className="text-gray-300 font-semibold">No API endpoints detected</p>
        <p className="text-gray-500 text-sm mt-1">This repository doesn't appear to expose HTTP endpoints.</p>
      </div>
    )
  }

  return (
    <div className="card">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-lg font-semibold text-white">Auto-Generated API Documentation</h2>
        <div className="flex gap-1 bg-gray-800 rounded-lg p-1">
          {['rendered', 'raw'].map(v => (
            <button
              key={v}
              onClick={() => setView(v)}
              className={`px-3 py-1 rounded text-xs font-medium transition-colors capitalize ${
                view === v ? 'bg-primary-600 text-white' : 'text-gray-400 hover:text-white'
              }`}
            >
              {v}
            </button>
          ))}
        </div>
      </div>

      {view === 'rendered' ? (
        <div
          className="prose-invert max-w-none"
          dangerouslySetInnerHTML={{ __html: renderMarkdown(docs) }}
        />
      ) : (
        <pre className="text-xs text-gray-300 font-mono whitespace-pre-wrap leading-relaxed bg-gray-950 rounded-xl p-4 overflow-auto max-h-[60vh] border border-gray-800">
          {docs}
        </pre>
      )}
    </div>
  )
}
