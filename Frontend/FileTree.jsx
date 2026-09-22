import { useState } from 'react'

function TreeNode({ node, depth = 0 }) {
  const [open, setOpen] = useState(depth < 2)
  const isDir = node.type === 'directory'

  return (
    <div style={{ paddingLeft: `${depth * 16}px` }}>
      <div
        className={`flex items-center gap-2 py-1 px-2 rounded-lg text-sm cursor-pointer transition-colors ${
          isDir ? 'text-primary-300 hover:bg-gray-800' : 'text-gray-300 hover:bg-gray-800'
        }`}
        onClick={() => isDir && setOpen(o => !o)}
      >
        {isDir ? (
          <span className="text-yellow-400 text-xs">{open ? '📂' : '📁'}</span>
        ) : (
          <span className="text-blue-400 text-xs">📄</span>
        )}
        <span className="font-mono">{node.name}</span>
        {node.size && (
          <span className="ml-auto text-gray-600 text-xs">{formatSize(node.size)}</span>
        )}
      </div>
      {isDir && open && node.children?.map((child, i) => (
        <TreeNode key={i} node={child} depth={depth + 1} />
      ))}
    </div>
  )
}

function formatSize(bytes) {
  if (bytes < 1024) return `${bytes}B`
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)}KB`
  return `${(bytes / 1024 / 1024).toFixed(1)}MB`
}

export default function FileTree({ tree }) {
  if (!tree) return <p className="text-gray-500 text-sm">No file tree available.</p>
  return (
    <div className="bg-gray-950 rounded-xl border border-gray-800 p-4 overflow-auto max-h-96 font-mono text-sm">
      <TreeNode node={tree} depth={0} />
    </div>
  )
}
