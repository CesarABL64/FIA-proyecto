export default function EightQueensBoard({ currentState, queens, size = 8 }) {
  const state = currentState || queens || Array(8).fill(0)
  const attacked = new Set()
  const conflicts = new Set()

  for (let i = 0; i < size; i++) {
    for (let j = i + 1; j < size; j++) {
      if (state[i] === state[j]) {
        conflicts.add(`${i},${state[i]}`)
        conflicts.add(`${j},${state[j]}`)
      }
      if (Math.abs(state[i] - state[j]) === Math.abs(i - j)) {
        conflicts.add(`${i},${state[i]}`)
        conflicts.add(`${j},${state[j]}`)
      }
    }
  }

  return (
    <div className="flex flex-col items-center gap-3">
      <div className="grid gap-0.5" style={{ gridTemplateColumns: `repeat(${size}, 1fr)` }}>
        {Array.from({ length: size }, (_, r) =>
          Array.from({ length: size }, (_, c) => {
            const isQueen = state[r] === c
            const isConflict = conflicts.has(`${r},${c}`)
            const isLight = (r + c) % 2 === 0
            let bg = isLight ? 'bg-amber-100' : 'bg-amber-800'

            if (isQueen && isConflict) {
              bg = 'bg-red-500'
            } else if (isQueen) {
              bg = 'bg-purple-500'
            }

            return (
              <div
                key={`${r},${c}`}
                className={`w-10 h-10 sm:w-12 sm:h-12 flex items-center justify-center text-lg cell-transition rounded-sm ${bg}`}
              >
                {isQueen && <span className="text-white font-bold">♛</span>}
              </div>
            )
          })
        )}
      </div>
      <div className="flex gap-5 text-xs mt-2 items-center">
        <span className="flex items-center gap-1.5"><span className="w-3 h-3 bg-purple-500 rounded inline-block" /><span className="text-text-muted">Reina (sin conflicto)</span></span>
        <span className="flex items-center gap-1.5"><span className="w-3 h-3 bg-red-500 rounded inline-block" /><span className="text-text-muted">Reina (en conflicto)</span></span>
        <span className="text-text-muted">Ataques: {conflicts.size / 2}</span>
      </div>
    </div>
  )
}
