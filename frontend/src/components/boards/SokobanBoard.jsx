export default function SokobanBoard({ grid, rows, cols, current, walls, goals }) {
  const wallSet = new Set((walls || []).map(([r, c]) => `${r},${c}`))
  const goalSet = new Set((goals || []).map(([r, c]) => `${r},${c}`))

  let playerPos = null
  let boxSet = new Set()

  if (current) {
    if (current.player) {
      playerPos = `${current.player[0]},${current.player[1]}`
      if (current.boxes) {
        current.boxes.forEach((b) => boxSet.add(`${b[0]},${b[1]}`))
      }
    } else if (Array.isArray(current) && current.length === 2) {
      if (Array.isArray(current[0])) {
        playerPos = `${current[0][0]},${current[0][1]}`
        if (Array.isArray(current[1])) {
          current[1].forEach((b) => boxSet.add(`${b[0]},${b[1]}`))
        }
      }
    }
  }

  const displayRows = rows || (grid ? grid.length : 5)
  const displayCols = cols || (grid && grid[0] ? grid[0].length : 5)

  return (
    <div className="flex flex-col items-center gap-3">
      <div className="grid gap-1" style={{ gridTemplateColumns: `repeat(${displayCols}, 1fr)` }}>
        {Array.from({ length: displayRows }, (_, r) =>
          Array.from({ length: displayCols }, (_, c) => {
            const key = `${r},${c}`
            let bg = 'bg-slate-300'
            let label = ''
            let textColor = ''

            if (wallSet.has(key)) {
              bg = 'bg-slate-800'
            } else if (playerPos === key && boxSet.has(key)) {
              bg = 'bg-blue-500'
              label = 'P'
              textColor = 'text-white'
            } else if (playerPos === key) {
              bg = 'bg-blue-500'
              label = 'P'
              textColor = 'text-white'
            } else if (boxSet.has(key) && goalSet.has(key)) {
              bg = 'bg-green-600'
              label = '★'
              textColor = 'text-white'
            } else if (boxSet.has(key)) {
              bg = 'bg-orange-400'
              label = 'B'
              textColor = 'text-white'
            } else if (goalSet.has(key)) {
              bg = 'bg-green-300'
              label = 'G'
              textColor = 'text-green-800'
            } else if (grid && grid[r] && grid[r][c] === 'W') {
              bg = 'bg-slate-800'
            }

            return (
              <div
                key={key}
                className={`w-12 h-12 flex items-center justify-center rounded-lg text-xs font-bold cell-transition ${bg} ${textColor}`}
              >
                {label}
              </div>
            )
          })
        )}
      </div>
      <div className="flex flex-wrap gap-4 text-xs mt-2 justify-center">
        <span className="flex items-center gap-1.5"><span className="w-3 h-3 bg-blue-500 rounded inline-block" /><span className="text-text-muted">Jugador</span></span>
        <span className="flex items-center gap-1.5"><span className="w-3 h-3 bg-orange-400 rounded inline-block" /><span className="text-text-muted">Caja</span></span>
        <span className="flex items-center gap-1.5"><span className="w-3 h-3 bg-green-300 rounded inline-block" /><span className="text-text-muted">Meta</span></span>
        <span className="flex items-center gap-1.5"><span className="w-3 h-3 bg-green-600 rounded inline-block" /><span className="text-text-muted">Caja en meta</span></span>
        <span className="flex items-center gap-1.5"><span className="w-3 h-3 bg-slate-800 rounded inline-block" /><span className="text-text-muted">Pared</span></span>
      </div>
    </div>
  )
}
