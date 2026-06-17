export default function AlgorithmSelector({ algorithms, algorithmNames, selected, onSelect }) {
  return (
    <div className="flex flex-wrap gap-2">
      {algorithms.map((algo) => (
        <button
          key={algo}
          onClick={() => onSelect(algo)}
          className={`px-4 py-2 rounded-xl text-sm font-medium transition-all duration-200 border ${
            selected === algo
              ? 'bg-primary text-white border-primary shadow-sm'
              : 'bg-surface-alt text-text-secondary border-border hover:bg-primary-light hover:text-primary hover:border-primary'
          }`}
        >
          {algorithmNames[algo]}
        </button>
      ))}
    </div>
  )
}
