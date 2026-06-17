export default function TicTacToeBoard({ currentState, highlightCell }) {
  const board = currentState || [
    [' ', ' ', ' '],
    [' ', ' ', ' '],
    [' ', ' ', ' '],
  ]

  return (
    <div className="flex flex-col items-center gap-3">
      <div className="grid grid-cols-3 gap-2">
        {board.map((row, r) =>
          row.map((cell, c) => {
            const isHighlight = highlightCell && highlightCell[0] === r && highlightCell[1] === c
            let color = 'text-text-muted'
            if (cell === 'X') color = 'text-blue-500'
            if (cell === 'O') color = 'text-red-400'

            return (
              <div
                key={`${r},${c}`}
                className={`w-20 h-20 sm:w-24 sm:h-24 flex items-center justify-center text-3xl sm:text-4xl font-bold rounded-xl cell-transition ${
                  isHighlight ? 'bg-yellow-400/20 ring-2 ring-yellow-400' : 'bg-surface-alt border border-border'
                } ${color}`}
              >
                {cell !== ' ' ? cell : ''}
              </div>
            )
          })
        )}
      </div>
      <div className="flex gap-5 text-xs mt-2">
        <span className="flex items-center gap-1.5"><span className="text-blue-500 font-bold">X</span> <span className="text-text-muted">(Maximiza)</span></span>
        <span className="flex items-center gap-1.5"><span className="text-red-400 font-bold">O</span> <span className="text-text-muted">(Minimiza)</span></span>
        <span className="flex items-center gap-1.5"><span className="w-3 h-3 bg-yellow-400/20 ring-1 ring-yellow-400 rounded inline-block" /><span className="text-text-muted">Evaluando</span></span>
      </div>
    </div>
  )
}
