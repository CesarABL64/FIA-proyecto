import { useState, useEffect, useRef, useCallback } from 'react'
import ProblemSelector from './components/ProblemSelector'
import AlgorithmSelector from './components/AlgorithmSelector'
import AnimationControls from './components/AnimationControls'
import MetricsPanel from './components/MetricsPanel'
import FrozenLakeBoard from './components/boards/FrozenLakeBoard'
import SokobanBoard from './components/boards/SokobanBoard'
import EightQueensBoard from './components/boards/EightQueensBoard'
import TicTacToeBoard from './components/boards/TicTacToeBoard'
import { getProblems, getFrozenLakeGrids, getSokobanLevels, runSearch } from './services/api'

export default function App() {
  const [problems, setProblems] = useState(null)
  const [selectedProblem, setSelectedProblem] = useState(null)
  const [selectedAlgorithm, setSelectedAlgorithm] = useState(null)
  const [gridSize, setGridSize] = useState(4)
  const [sokobanLevel, setSokobanLevel] = useState(1)
  const [frozenLakeGrids, setFrozenLakeGrids] = useState(null)
  const [sokobanLevels, setSokobanLevels] = useState(null)
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)

  const [currentStep, setCurrentStep] = useState(0)
  const [isPlaying, setIsPlaying] = useState(false)
  const [speed, setSpeed] = useState(500)
  const intervalRef = useRef(null)

  useEffect(() => {
    getProblems().then(setProblems).catch(() => {})
    getFrozenLakeGrids().then(setFrozenLakeGrids).catch(() => {})
    getSokobanLevels().then(setSokobanLevels).catch(() => {})
  }, [])

  useEffect(() => {
    if (isPlaying && result && result.steps) {
      if (intervalRef.current) clearInterval(intervalRef.current)
      intervalRef.current = setInterval(() => {
        setCurrentStep((prev) => {
          if (prev >= result.steps.length - 1) {
            setIsPlaying(false)
            return prev
          }
          return prev + 1
        })
      }, speed)
      return () => {
        if (intervalRef.current) clearInterval(intervalRef.current)
      }
    } else {
      if (intervalRef.current) {
        clearInterval(intervalRef.current)
        intervalRef.current = null
      }
    }
  }, [isPlaying, speed, result])

  const handleRun = useCallback(async () => {
    if (!selectedProblem || !selectedAlgorithm) return
    setLoading(true)
    setError(null)
    setResult(null)
    setCurrentStep(0)

    const params = {}
    if (selectedProblem === 'frozen_lake') params.grid_size = gridSize
    if (selectedProblem === 'sokoban') params.level = sokobanLevel

    try {
      const data = await runSearch(selectedProblem, selectedAlgorithm, params)
      setResult(data)
      setIsPlaying(true)
    } catch (err) {
      setError(err.response?.data?.detail || 'Error al ejecutar la búsqueda')
    } finally {
      setLoading(false)
    }
  }, [selectedProblem, selectedAlgorithm, gridSize, sokobanLevel])

  const handleSpeedChange = useCallback((newSpeed) => {
    setSpeed(newSpeed)
  }, [])

  const stepData = result?.steps?.[currentStep]
  const solution = result?.solution

  const getBoard = () => {
    if (selectedProblem === 'frozen_lake' && frozenLakeGrids) {
      const grid = frozenLakeGrids[String(gridSize)]?.grid
      if (!grid) return null
      return (
        <FrozenLakeBoard
          grid={grid}
          current={stepData?.current}
          explored={stepData?.explored}
          frontier={stepData?.frontier}
          solutionPath={solution?.path}
          showSolution={currentStep >= (result?.steps?.length ?? 0) - 1 && result?.solution}
        />
      )
    }
    if (selectedProblem === 'sokoban' && sokobanLevels) {
      const levelData = sokobanLevels[String(sokobanLevel)]
      if (!levelData) return null
      let current = stepData?.current
      if (!current) {
        current = { player: levelData.player, boxes: levelData.boxes }
      }
      return (
        <SokobanBoard
          grid={levelData.grid}
          rows={levelData.rows}
          cols={levelData.cols}
          current={current}
          walls={levelData.walls}
          goals={levelData.goals}
        />
      )
    }
    if (selectedProblem === 'eight_queens') {
      const queens = stepData?.current || solution?.state || [0, 1, 2, 3, 4, 5, 6, 7]
      return <EightQueensBoard queens={queens} size={8} />
    }
    if (selectedProblem === 'tic_tac_toe') {
      const board = stepData?.current || [
        [' ', ' ', ' '],
        [' ', ' ', ' '],
        [' ', ' ', ' '],
      ]
      let hl = null
      if (stepData?.action) {
        const a = stepData.action
        if (typeof a === 'object' && a.row !== undefined) {
          hl = [a.row, a.col]
        }
      }
      return <TicTacToeBoard currentState={board} highlightCell={hl} />
    }
    return null
  }

  const showBoard = selectedProblem && (
    selectedProblem === 'frozen_lake' && frozenLakeGrids ||
    selectedProblem === 'sokoban' && sokobanLevels ||
    selectedProblem === 'eight_queens' ||
    selectedProblem === 'tic_tac_toe'
  )

  return (
    <div className="min-h-screen bg-surface p-4 sm:p-6">
      <div className="max-w-5xl mx-auto">
        <h1 className="text-3xl sm:text-4xl font-bold text-center mb-3 bg-gradient-to-r from-primary to-accent bg-clip-text text-transparent tracking-tight">
          Visualizador de Algoritmos de Búsqueda
        </h1>
        <p className="text-center text-text-secondary text-sm mb-8 max-w-xl mx-auto">
          Selecciona un problema, elige un algoritmo y observa paso a paso cómo funciona
        </p>

        {problems && (
          <ProblemSelector
            problems={problems}
            selected={selectedProblem}
            onSelect={(key) => {
              setSelectedProblem(key)
              setSelectedAlgorithm(null)
              setResult(null)
              setCurrentStep(0)
              setIsPlaying(false)
            }}
          />
        )}

        {selectedProblem && problems && (
          <div className="mt-4 bg-surface-card rounded-2xl p-5 shadow-sm border border-border">
            <h3 className="text-sm font-semibold text-text-secondary mb-3 uppercase tracking-wide">Algoritmo</h3>
            <AlgorithmSelector
              algorithms={problems[selectedProblem].algorithms}
              algorithmNames={problems[selectedProblem].algorithm_names}
              selected={selectedAlgorithm}
              onSelect={(algo) => {
                setSelectedAlgorithm(algo)
                setResult(null)
                setCurrentStep(0)
                setIsPlaying(false)
              }}
            />
          </div>
        )}

        {selectedProblem === 'frozen_lake' && (
          <div className="mt-4 bg-surface-card rounded-2xl p-5 shadow-sm border border-border flex items-center gap-4">
            <label className="text-sm font-medium text-text">Tamaño de cuadrícula:</label>
            <select
              value={gridSize}
              onChange={(e) => { setGridSize(Number(e.target.value)); setResult(null); setCurrentStep(0) }}
              className="bg-surface-alt border border-border rounded-xl px-4 py-2 text-sm text-text focus:outline-none focus:ring-2 focus:ring-primary/30 transition-all cursor-pointer"
            >
              <option value={4}>4 x 4</option>
              <option value={5}>5 x 5</option>
              <option value={6}>6 x 6</option>
            </select>
          </div>
        )}

        {selectedProblem === 'sokoban' && (
          <div className="mt-4 bg-surface-card rounded-2xl p-5 shadow-sm border border-border flex items-center gap-4">
            <label className="text-sm font-medium text-text">Nivel:</label>
            <select
              value={sokobanLevel}
              onChange={(e) => { setSokobanLevel(Number(e.target.value)); setResult(null); setCurrentStep(0) }}
              className="bg-surface-alt border border-border rounded-xl px-4 py-2 text-sm text-text focus:outline-none focus:ring-2 focus:ring-primary/30 transition-all cursor-pointer"
            >
              <option value={1}>Nivel 1 (Fácil)</option>
              <option value={2}>Nivel 2 (Medio)</option>
              <option value={3}>Nivel 3 (Difícil)</option>
            </select>
          </div>
        )}

        <div className="mt-5 flex justify-center">
          <button
            onClick={handleRun}
            disabled={!selectedAlgorithm || loading}
            className="px-8 py-3 bg-primary hover:bg-primary-hover disabled:bg-surface-alt disabled:text-text-muted disabled:cursor-not-allowed rounded-xl font-semibold transition-all duration-200 shadow-sm hover:shadow-md text-white"
          >
            {loading ? (
              <span className="flex items-center gap-2">
                <svg className="animate-spin h-4 w-4" viewBox="0 0 24 24"><circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none"/><path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"/></svg>
                Ejecutando...
              </span>
            ) : 'Ejecutar búsqueda'}
          </button>
        </div>

        {error && (
          <div className="mt-4 bg-error-light border border-error rounded-xl p-4 text-error text-sm font-medium">
            {error}
          </div>
        )}

        {showBoard && (
          <div className="mt-6 space-y-4">
            <div className="bg-surface-card rounded-2xl p-6 flex justify-center shadow-sm border border-border">
              {getBoard()}
            </div>

            {result && result.steps && result.steps.length > 0 && stepData && (
              <div className="bg-surface-card rounded-xl p-4 shadow-sm border border-border">
                <p className="text-sm text-text">
                  <span className="text-primary font-semibold">Paso {currentStep + 1}/{result.steps.length}:</span>{' '}
                  {stepData.description}
                </p>
                {stepData.h_score !== undefined && (
                  <p className="text-xs text-text-muted mt-1">
                    h(n) = {stepData.h_score}
                    {stepData.g_score !== undefined && ` | g(n) = ${stepData.g_score}`}
                    {stepData.f_score !== undefined && ` | f(n) = ${stepData.f_score}`}
                  </p>
                )}
                {stepData.attacks !== undefined && (
                  <p className="text-xs text-text-muted mt-1">
                    Pares de reinas atacándose: {stepData.attacks}
                  </p>
                )}
                {stepData.value !== undefined && (
                  <p className="text-xs text-text-muted mt-1">
                    Valor MiniMax: {stepData.value}
                  </p>
                )}
              </div>
            )}

            {result && result.steps && result.steps.length > 0 && (
              <>
                <AnimationControls
                  isPlaying={isPlaying}
                  onPlay={() => setIsPlaying(true)}
                  onPause={() => setIsPlaying(false)}
                  onStepForward={() => setCurrentStep((p) => Math.min(p + 1, result.steps.length - 1))}
                  onStepBackward={() => setCurrentStep((p) => Math.max(p - 1, 0))}
                  onGoToStep={(step) => setCurrentStep(step)}
                  onReset={() => { setCurrentStep(0); setIsPlaying(false) }}
                  currentStep={currentStep}
                  totalSteps={result.steps.length}
                  speed={speed}
                  onSpeedChange={handleSpeedChange}
                />

                <MetricsPanel metrics={result.metrics} />

                {result.solution && (
                  <div className="bg-success-light border border-success rounded-xl p-4 text-sm text-success font-medium">
                    ✓ Solución encontrada
                    {result.metrics.path_length > 0 && ` — Longitud del camino: ${result.metrics.path_length}`}
                    {result.metrics.path_cost > 0 && ` — Costo: ${result.metrics.path_cost}`}
                  </div>
                )}
                {!result.solution && (
                  <div className="bg-warning-light border border-warning rounded-xl p-4 text-sm text-warning font-medium">
                    No se encontró solución
                  </div>
                )}
              </>
            )}
          </div>
        )}
      </div>
    </div>
  )
}