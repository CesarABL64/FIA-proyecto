export default function MetricsPanel({ metrics }) {
  if (!metrics) return null

  const items = [
    { label: 'Nodos expandidos', value: metrics.nodes_expanded ?? '-' },
    { label: 'Longitud del camino', value: metrics.path_length ?? '-' },
    { label: 'Costo del camino', value: metrics.path_cost ?? '-' },
    { label: 'Tiempo (ms)', value: metrics.execution_time_ms ?? '-' },
  ]

  if (metrics.restarts !== undefined) {
    items.push({ label: 'Reinicios', value: metrics.restarts })
  }
  if (metrics.best_attacks !== undefined) {
    items.push({ label: 'Mejor ataques', value: metrics.best_attacks })
  }

  return (
    <div className="bg-surface-card rounded-2xl p-5 shadow-sm border border-border">
      <h3 className="text-sm font-semibold text-text-secondary mb-4 uppercase tracking-wide">Métricas</h3>
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
        {items.map(({ label, value }) => (
          <div key={label} className="bg-surface-alt rounded-xl p-4 text-center border border-border">
            <div className="text-xl font-bold text-primary">{value}</div>
            <div className="text-xs text-text-muted mt-1">{label}</div>
          </div>
        ))}
      </div>
    </div>
  )
}
