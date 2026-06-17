import { Play, Pause, SkipBack, SkipForward, RotateCcw } from 'lucide-react'

export default function AnimationControls({
  isPlaying,
  onPlay,
  onPause,
  onStepForward,
  onStepBackward,
  onReset,
  onGoToStep,
  currentStep,
  totalSteps,
  speed,
  onSpeedChange,
}) {
  return (
    <div className="bg-surface-card rounded-2xl p-5 shadow-sm border border-border flex flex-col gap-4">
      <div className="flex items-center justify-center gap-3">
        <button
          onClick={onReset}
          className="p-2.5 rounded-xl bg-surface-alt border border-border hover:bg-primary-light hover:text-primary hover:border-primary transition-all duration-200 text-text-secondary"
          title="Reiniciar"
        >
          <RotateCcw size={18} />
        </button>
        <button
          onClick={onStepBackward}
          disabled={currentStep === 0}
          className="p-2.5 rounded-xl bg-surface-alt border border-border hover:bg-primary-light hover:text-primary hover:border-primary transition-all duration-200 text-text-secondary disabled:opacity-30 disabled:hover:bg-surface-alt disabled:hover:text-text-secondary disabled:hover:border-border"
          title="Retroceder"
        >
          <SkipBack size={18} />
        </button>
        {isPlaying ? (
          <button
            onClick={onPause}
            className="p-3 rounded-xl bg-primary hover:bg-primary-hover transition-all duration-200 shadow-sm text-white"
            title="Pausar"
          >
            <Pause size={20} />
          </button>
        ) : (
          <button
            onClick={onPlay}
            disabled={totalSteps === 0 || (currentStep >= totalSteps - 1 && totalSteps > 0)}
            className="p-3 rounded-xl bg-primary hover:bg-primary-hover transition-all duration-200 shadow-sm text-white disabled:opacity-30"
            title="Reproducir"
          >
            <Play size={20} />
          </button>
        )}
        <button
          onClick={onStepForward}
          disabled={currentStep >= totalSteps - 1}
          className="p-2.5 rounded-xl bg-surface-alt border border-border hover:bg-primary-light hover:text-primary hover:border-primary transition-all duration-200 text-text-secondary disabled:opacity-30 disabled:hover:bg-surface-alt disabled:hover:text-text-secondary disabled:hover:border-border"
          title="Avanzar"
        >
          <SkipForward size={18} />
        </button>
      </div>

      <div className="flex items-center gap-3">
        <span className="text-xs text-text-muted w-8 text-right font-medium">{currentStep + 1}</span>
        <input
          type="range"
          min={0}
          max={Math.max(totalSteps - 1, 0)}
          value={currentStep}
          onChange={(e) => onGoToStep(parseInt(e.target.value))}
          className="flex-1"
          style={{ accentColor: 'var(--color-primary)' }}
        />
        <span className="text-xs text-text-muted w-8 font-medium">{totalSteps}</span>
      </div>

      <div className="flex items-center gap-3">
        <span className="text-xs text-text-muted font-medium">Velocidad:</span>
        <input
          type="range"
          min={50}
          max={2000}
          value={2300 - speed}
          onChange={(e) => onSpeedChange(2300 - parseInt(e.target.value))}
          className="flex-1"
          style={{ accentColor: 'var(--color-accent)' }}
        />
        <span className="text-xs text-text-muted w-16 font-medium">{speed < 300 ? 'Rápido' : speed < 800 ? 'Medio' : 'Lento'}</span>
      </div>
    </div>
  )
}
