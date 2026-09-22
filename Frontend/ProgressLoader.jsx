import { useEffect, useState } from 'react'

const STEPS = [
  { label: 'Cloning repository…',         duration: 4000  },
  { label: 'Reading source files…',        duration: 3000  },
  { label: 'Running static analysis…',     duration: 5000  },
  { label: 'Detecting duplicate code…',    duration: 4000  },
  { label: 'Scanning security issues…',    duration: 3000  },
  { label: 'Generating AI summaries…',     duration: 8000  },
  { label: 'Building architecture diagram…', duration: 5000 },
  { label: 'Writing API documentation…',   duration: 4000  },
  { label: 'Saving results…',              duration: 2000  },
]

export default function ProgressLoader({ repoUrl }) {
  const [stepIndex, setStepIndex] = useState(0)
  const [pct, setPct] = useState(0)

  useEffect(() => {
    const total = STEPS.reduce((a, s) => a + s.duration, 0)
    let elapsed = 0
    let si = 0

    const tick = () => {
      if (si >= STEPS.length) return
      elapsed += 200
      setPct(Math.min(Math.round((elapsed / total) * 100), 95))

      let cumulative = 0
      for (let i = 0; i < STEPS.length; i++) {
        cumulative += STEPS[i].duration
        if (elapsed < cumulative) { si = i; break }
      }
      setStepIndex(si)
    }

    const interval = setInterval(tick, 200)
    return () => clearInterval(interval)
  }, [])

  return (
    <div className="flex flex-col items-center justify-center py-20 gap-8 max-w-md mx-auto">
      {/* Animated orb */}
      <div className="relative w-24 h-24">
        <div className="absolute inset-0 rounded-full bg-primary-900 animate-ping opacity-30"></div>
        <div className="absolute inset-2 rounded-full bg-primary-800 animate-pulse"></div>
        <div className="absolute inset-4 rounded-full bg-primary-600 flex items-center justify-center">
          <span className="text-white font-bold text-lg">{pct}%</span>
        </div>
      </div>

      {/* Progress bar */}
      <div className="w-full">
        <div className="flex justify-between text-xs text-gray-500 mb-2">
          <span>Analyzing</span>
          <span>{pct}%</span>
        </div>
        <div className="w-full bg-gray-800 rounded-full h-2">
          <div
            className="bg-primary-500 h-2 rounded-full transition-all duration-300"
            style={{ width: `${pct}%` }}
          />
        </div>
      </div>

      {/* Current step */}
      <div className="text-center">
        <p className="text-white font-semibold">{STEPS[stepIndex]?.label}</p>
        <p className="text-gray-500 text-xs mt-1 font-mono truncate max-w-xs">
          {repoUrl}
        </p>
      </div>

      {/* Step list */}
      <div className="w-full space-y-2">
        {STEPS.map((step, i) => (
          <div key={i} className="flex items-center gap-3 text-sm">
            <span className={`w-5 h-5 rounded-full flex items-center justify-center shrink-0 text-xs ${
              i < stepIndex  ? 'bg-green-700 text-white' :
              i === stepIndex ? 'bg-primary-600 text-white animate-pulse' :
                                'bg-gray-800 text-gray-600'
            }`}>
              {i < stepIndex ? '✓' : i + 1}
            </span>
            <span className={i <= stepIndex ? 'text-gray-200' : 'text-gray-600'}>
              {step.label}
            </span>
          </div>
        ))}
      </div>
    </div>
  )
}
