from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

from problems.frozen_lake import FrozenLake
from problems.sokoban import Sokoban
from problems.eight_queens import EightQueens
from problems.tic_tac_toe import TicTacToe
from algorithms.bfs import BFS
from algorithms.dfs import DFS
from algorithms.a_star import AStar
from algorithms.gbfs import GBFS
from algorithms.hill_climbing import HillClimbing
from algorithms.minimax import MiniMax

router = APIRouter()

PROBLEM_ALGORITHMS = {
    "frozen_lake": {
        "name": "Frozen Lake",
        "type": "Búsqueda no informada",
        "algorithms": ["bfs", "dfs"],
        "algorithm_names": {"bfs": "BFS", "dfs": "DFS"},
    },
    "sokoban": {
        "name": "Sokoban",
        "type": "Búsqueda informada",
        "algorithms": ["a_star", "gbfs"],
        "algorithm_names": {"a_star": "A*", "gbfs": "GBFS"},
    },
    "eight_queens": {
        "name": "8 Reinas",
        "type": "Búsqueda local",
        "algorithms": ["hill_climbing"],
        "algorithm_names": {"hill_climbing": "Hill Climbing"},
    },
    "tic_tac_toe": {
        "name": "Tic-Tac-Toe",
        "type": "Búsqueda adversaria",
        "algorithms": ["minimax"],
        "algorithm_names": {"minimax": "MiniMax"},
    },
}


class SearchRequest(BaseModel):
    problem: str
    algorithm: str
    params: Optional[dict] = None


def serialize_state(state):
    if isinstance(state, tuple):
        if all(isinstance(x, tuple) for x in state):
            return [list(row) for row in state]
        return list(state)
    return state


def serialize_step(step, problem_name):
    serialized = {}
    for key, value in step.items():
        if key == "current":
            serialized[key] = serialize_state(value)
        elif key in ("explored", "frontier"):
            serialized[key] = [serialize_state(s) for s in value]
        elif key == "next_state" and value is not None:
            serialized[key] = serialize_state(value)
        elif key == "action":
            if problem_name == "tic_tac_toe" and value is not None:
                player, r, c = value
                serialized[key] = {"player": player, "row": r, "col": c}
            else:
                serialized[key] = value
        else:
            serialized[key] = value
    return serialized


@router.get("/problems")
def get_problems():
    return PROBLEM_ALGORITHMS


@router.get("/problems/frozen-lake/grids")
def get_frozen_lake_grids():
    lake = FrozenLake(4)
    configs = {}
    for size in [4, 5, 6]:
        fl = FrozenLake(size)
        configs[str(size)] = {
            "size": size,
            "grid": fl.get_grid_for_display(),
            "start": list(fl.start),
            "goal": list(fl.goal),
            "holes": [list(h) for h in fl.holes],
        }
    return configs


@router.get("/problems/sokoban/levels")
def get_sokoban_levels():
    levels = {}
    for level in Sokoban.LEVELS:
        s = Sokoban(level)
        state = s.get_start_state()
        player, boxes = state
        levels[str(level)] = {
            "level": level,
            "rows": s.rows,
            "cols": s.cols,
            "walls": [list(w) for w in s.walls],
            "goals": [list(g) for g in s.goals],
            "player": list(player),
            "boxes": [list(b) for b in boxes],
            "grid": s.get_grid_for_display(state),
        }
    return levels


@router.post("/search")
def run_search(request: SearchRequest):
    problem_name = request.problem
    algorithm_name = request.algorithm
    params = request.params or {}

    if problem_name not in PROBLEM_ALGORITHMS:
        raise HTTPException(status_code=400, detail=f"Problema desconocido: {problem_name}")

    if algorithm_name not in PROBLEM_ALGORITHMS[problem_name]["algorithms"]:
        raise HTTPException(status_code=400, detail=f"Algoritmo {algorithm_name} no disponible para {problem_name}")

    if problem_name == "frozen_lake":
        grid_size = params.get("grid_size", 4)
        problem = FrozenLake(grid_size)
    elif problem_name == "sokoban":
        level = params.get("level", 1)
        problem = Sokoban(level)
    elif problem_name == "eight_queens":
        problem = EightQueens()
    elif problem_name == "tic_tac_toe":
        problem = TicTacToe()
    else:
        raise HTTPException(status_code=400, detail="Problema no implementado")

    if algorithm_name == "bfs":
        algorithm = BFS(problem)
    elif algorithm_name == "dfs":
        algorithm = DFS(problem)
    elif algorithm_name == "a_star":
        algorithm = AStar(problem)
    elif algorithm_name == "gbfs":
        algorithm = GBFS(problem)
    elif algorithm_name == "hill_climbing":
        algorithm = HillClimbing(problem)
    elif algorithm_name == "minimax":
        algorithm = MiniMax(problem)
    else:
        raise HTTPException(status_code=400, detail="Algoritmo no implementado")

    result = algorithm.search()

    serialized_steps = [serialize_step(step, problem_name) for step in result["steps"]]

    serialized_solution = None
    if result["solution"]:
        sol = result["solution"]
        if problem_name == "frozen_lake":
            serialized_solution = {
                "path": [serialize_state(p) for p in sol["path"]],
                "actions": sol.get("actions", []),
            }
        elif problem_name == "sokoban":
            path = sol["path"]
            serialized_path = []
            for p in path:
                player, boxes = p
                serialized_path.append({
                    "player": list(player),
                    "boxes": [list(b) for b in boxes],
                })
            serialized_solution = {
                "path": serialized_path,
                "actions": sol.get("actions", []),
            }
        elif problem_name == "eight_queens":
            state = sol.get("state") or sol["path"][0]
            serialized_solution = {
                "state": list(state),
            }
        elif problem_name == "tic_tac_toe":
            path = sol["path"]
            serialized_solution = {
                "path": [serialize_state(p) for p in path],
                "best_move": sol.get("best_move"),
                "best_value": sol.get("best_value"),
            }
    elif problem_name == "eight_queens":
        pass

    return {
        "steps": serialized_steps,
        "solution": serialized_solution,
        "metrics": result["metrics"],
    }