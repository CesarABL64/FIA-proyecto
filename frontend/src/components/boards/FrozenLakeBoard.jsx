export default function FrozenLakeBoard({ grid, current, explored, frontier, solutionPath, showSolution }) {
  const exploredSet = new Set((explored || []).map(([r, c]) => `${r},${c}`))
  const frontierSet = new Set((frontier || []).map(([r, c]) => `${r},${c}`))
  const pathSet = showSolution
    ? new Set((solutionPath || []).map(([r, c]) => `${r},${c}`))
    : new Set()

  return (
    <div className="flex flex-col items-center gap-3">
      <div className="grid gap-1" style={{ gridTemplateColumns: `repeat(${grid[0].length}, 1fr)` }}>
        {grid.map((row, r) =>
          row.map((cell, c) => {
            const key = `${r},${c}`
            let bg = 'bg-slate-300'
            let label = ''
            let textColor = ''

            if (cell === 'H') {
              bg = 'bg-red-500'
              label = '●'
              textColor = 'text-red-200'
            } else if (cell === 'S') {
              bg = pathSet.has(key) ? 'bg-green-500' : 'bg-blue-400'
              label = 'S'
              textColor = 'text-white'
            } else if (cell === 'G') {
              bg = pathSet.has(key) ? 'bg-green-500' : 'bg-green-400'
              label = 'G'
              textColor = 'text-white'
            } else if (pathSet.has(key)) {
              bg = 'bg-green-500'
              label = '★'
              textColor = 'text-white'
            } else if (current && current[0] === r && current[1] === c) {
              bg = 'bg-yellow-400'
              label = '●'
              textColor = 'text-yellow-900'
            } else if (frontierSet.has(key)) {
              bg = 'bg-yellow-600'
            } else if (exploredSet.has(key)) {
              bg = 'bg-blue-700'
            }

            return (
              <div
                key={key}
                className={`w-14 h-14 flex items-center justify-center rounded-lg text-sm font-bold cell-transition ${bg} ${textColor || 'text-slate-700'}`}
              >
                {label}
              </div>
            )
          })
        )}
      </div>
      <div className="flex flex-wrap gap-4 text-xs mt-2 justify-center">
        <span className="flex items-center gap-1.5"><span className="w-3 h-3 bg-blue-400 rounded inline-block" /><span className="text-text-muted">Inicio</span></span>
        <span className="flex items-center gap-1.5"><span className="w-3 h-3 bg-green-400 rounded inline-block" /><span className="text-text-muted">Meta</span></span>
        <span className="flex items-center gap-1.5"><span className="w-3 h-3 bg-red-500 rounded inline-block" /><span className="text-text-muted">Hoyo</span></span>
        <span className="flex items-center gap-1.5"><span className="w-3 h-3 bg-yellow-400 rounded inline-block" /><span className="text-text-muted">Actual</span></span>
        <span className="flex items-center gap-1.5"><span className="w-3 h-3 bg-blue-700 rounded inline-block" /><span className="text-text-muted">Explorado</span></span>
        <span className="flex items-center gap-1.5"><span className="w-3 h-3 bg-yellow-600 rounded inline-block" /><span className="text-text-muted">Frontera</span></span>
        <span className="flex items-center gap-1.5"><span className="w-3 h-3 bg-green-500 rounded inline-block" /><span className="text-text-muted">Camino solución</span></span>
      </div>
    </div>
  )
}
