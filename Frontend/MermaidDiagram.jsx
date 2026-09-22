import { useEffect, useRef } from 'react'
import mermaid from 'mermaid'

mermaid.initialize({
  startOnLoad: false,
  theme: 'dark',
  themeVariables: {
    primaryColor: '#4f46e5',
    primaryTextColor: '#e2e8f0',
    primaryBorderColor: '#6366f1',
    lineColor: '#6b7280',
    sectionBkgColor: '#1e1b4b',
    altSectionBkgColor: '#1e1e2e',
    sectionBkgColor2: '#1e1b4b',
    taskBkgColor: '#4f46e5',
    taskTextColor: '#ffffff',
    taskTextLightColor: '#ffffff',
    taskTextOutsideColor: '#e2e8f0',
    gridColor: '#374151',
    fillType0: '#1e1b4b',
    background: '#11111b',
  },
})

export default function MermaidDiagram({ chart }) {
  const ref = useRef(null)

  useEffect(() => {
    if (!chart || !ref.current) return
    const id = `mermaid-${Date.now()}`
    mermaid.render(id, chart).then(({ svg }) => {
      if (ref.current) ref.current.innerHTML = svg
    }).catch(err => {
      if (ref.current) ref.current.innerHTML = `<p class="text-red-400 text-sm">Diagram render error: ${err.message}</p>`
    })
  }, [chart])

  if (!chart) return <p className="text-gray-500 text-sm">No diagram available.</p>

  return (
    <div
      ref={ref}
      className="bg-gray-950 rounded-xl border border-gray-800 p-4 overflow-auto min-h-40 flex items-center justify-center"
    />
  )
}
