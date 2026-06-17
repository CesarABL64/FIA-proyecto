export default function ProblemSelector({ problems, selected, onSelect }) {
  const problemInfo = {
    frozen_lake: { icon: '🏔️', color: 'from-cyan-600 to-blue-700' },
    sokoban: { icon: '📦', color: 'from-amber-600 to-orange-700' },
    eight_queens: { icon: '♛', color: 'from-purple-600 to-indigo-700' },
    tic_tac_toe: { icon: '✕○', color: 'from-rose-600 to-red-700' },
  }

  return (
    <div className="bg-surface-card rounded-2xl p-5 shadow-sm border border-border">
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
        {Object.entries(problems).map(([key, info]) => {
          const meta = problemInfo[key] || { icon: '?', color: 'from-slate-600 to-slate-700' }
          return (
            <button
              key={key}
              onClick={() => onSelect(key)}
              className={`p-4 rounded-xl text-left transition-all duration-200 border-2 ${
                selected === key
                  ? 'border-primary bg-primary-light shadow-sm scale-[1.02]'
                  : 'border-border bg-surface-alt hover:bg-surface-alt/80 hover:border-border-strong shadow-sm'
              }`}
            >
              <div className="text-2xl mb-2">{meta.icon}</div>
              <div className={`font-semibold text-sm ${selected === key ? 'text-primary' : 'text-text'}`}>{info.name}</div>
              <div className="text-xs text-text-muted mt-0.5">{info.type}</div>
            </button>
          )
        })}
      </div>
    </div>
  )
}
