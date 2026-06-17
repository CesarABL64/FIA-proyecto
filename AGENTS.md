# AGENTS.md

## Project: Search Algorithms Visualizer

Two-package project: Python/FastAPI backend + React/Vite/Tailwind frontend.

## Start commands

```bash
# Backend (from project root)
cd backend && pip install -r requirements.txt && python -m uvicorn main:app --port 8000

# Frontend (from project root)
cd frontend && npm install && npm run dev
```

The frontend dev server proxies `/api` to `http://localhost:8000` (see `vite.config.js`). Backend must be running first.

## Architecture

```
backend/
  algorithms/     # Each algorithm is a standalone class with a .search() method
  problems/       # Problem classes expose: get_start_state, is_goal, get_actions, result, heuristic
  routes/         # Single search.py router registered at /api prefix
frontend/
  src/
    App.jsx                       # Main component: selection, execution, animation loop
    components/boards/            # One board component per problem type
    components/AnimationControls  # Play/Pause/Step/Speed slider
    components/MetricsPanel       # nodes_expanded, path_cost, time, path_length
    services/api.js               # axios calls to backend
    hooks/useSearchAnimation.js   # UNUSED — App.jsx inlines its own animation state
```

## Algorithm <-> Problem contract

Every algorithm class receives a `problem` object in its constructor. The problem must expose:
- `get_start_state()` → returns initial state
- `is_goal(state)` → bool
- `get_actions(state)` → list of `(action, next_state)` tuples
- `result(state, action, next_state)` → state (usually just returns `next_state`)
- `step_cost(state, action, next_state)` → number (usually 1)
- `heuristic(state)` → number (used by A*, GBFS, Hill Climbing, MiniMax)

Every algorithm returns from `.search()`: `{ steps: [...], solution: {...} | null, metrics: {...} }`

## State serialization

The API route (`backend/routes/search.py`) serializes states differently per problem:
- **Frozen Lake**: state is `[row, col]` list
- **Sokoban**: state is `{player: [r,c], boxes: [[r,c],...]}`
- **8 Queens**: state is `[col_per_row, ...]` list of 8 ints
- **Tic-Tac-Toe**: state is 2D list `[[cell, ...], ...]`

Frontend board components expect these exact shapes. When adding new problems, update both the route serialization and the corresponding board component.

## MiniMax performance

`MiniMax` defaults to `max_depth=6`. At depth 9 (full Tic-Tac-Toe tree) it takes ~10s. Steps are only recorded for `depth <= 2` to keep response size manageable (~585 steps). Do not increase max_depth without also adjusting the `record` threshold.

## Testing

No formal test suite. Quick backend validation:
```bash
cd backend
python -c "from algorithms.bfs import BFS; from problems.frozen_lake import FrozenLake; r=BFS(FrozenLake(4)).search(); print(len(r['steps']), r['metrics']['path_length'])"
```
Frontend: `npm run build` confirms no import/syntax errors.

## Gotchas

- **Tailwind v4**: Uses `@import "tailwindcss"` in CSS (not `@tailwind` directives) and `@tailwindcss/vite` plugin.
- **No TypeScript**: The Vite template generated `.ts` files initially but they were removed. All files are `.jsx`/`.js`. The old `typecheck` build step (`tsc`) was removed from package.json. Do not reintroduce TS without checking.
- **Hardcoded grids**: Frozen Lake grids are defined in `frozen_lake.py`, not loaded from config. Max size is 6x6.
- **Hardcoded levels**: Sokoban levels are in `sokoban.py` under the `LEVELS` dict. Only 3 levels exist.
- **CORS is wide open**: `allow_origins=["*"]` — production deployments should restrict this.
- **Python imports require being run from `backend/`**: The module paths assume `python` is invoked from the `backend/` directory.
