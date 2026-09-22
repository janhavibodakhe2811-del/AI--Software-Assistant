export default function StatCard({ icon, label, value, sub, color = 'text-primary-400' }) {
  return (
    <div className="card flex items-center gap-4">
      <div className={`text-3xl ${color}`}>{icon}</div>
      <div>
        <p className="text-gray-400 text-xs uppercase tracking-wide">{label}</p>
        <p className={`text-2xl font-bold ${color}`}>{value}</p>
        {sub && <p className="text-gray-500 text-xs mt-0.5">{sub}</p>}
      </div>
    </div>
  )
}
