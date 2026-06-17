from collections import deque
import time


class BFS:
    def __init__(self, problem):
        self.problem = problem

    def search(self):
        start_time = time.time()
        start = self.problem.get_start_state()
        steps = []

        frontier = deque([start])
        visited = {start}
        came_from = {start: None}
        action_from = {start: None}

        if self.problem.is_goal(start):
            path = self._reconstruct_path(came_from, action_from, start)
            elapsed = (time.time() - start_time) * 1000
            return {
                "steps": steps,
                "solution": {"path": path, "actions": action_from},
                "metrics": {
                    "nodes_expanded": 0,
                    "path_cost": len(path) - 1,
                    "execution_time_ms": round(elapsed, 2),
                    "path_length": len(path),
                },
            }

        nodes_expanded = 0

        while frontier:
            current = frontier.popleft()
            steps.append({
                "current": current,
                "explored": list(visited),
                "frontier": list(frontier),
                "description": f"Expandiendo nodo {current}",
            })

            nodes_expanded += 1

            if self.problem.is_goal(current):
                path = self._reconstruct_path(came_from, action_from, current)
                elapsed = (time.time() - start_time) * 1000
                return {
                    "steps": steps,
                    "solution": {"path": path, "actions": [action_from[p] for p in path[1:]]},
                    "metrics": {
                        "nodes_expanded": nodes_expanded,
                        "path_cost": len(path) - 1,
                        "execution_time_ms": round(elapsed, 2),
                        "path_length": len(path),
                    },
                }

            for action, next_state in self.problem.get_actions(current):
                if next_state not in visited:
                    visited.add(next_state)
                    frontier.append(next_state)
                    came_from[next_state] = current
                    action_from[next_state] = action

        elapsed = (time.time() - start_time) * 1000
        return {
            "steps": steps,
            "solution": None,
            "metrics": {
                "nodes_expanded": nodes_expanded,
                "path_cost": 0,
                "execution_time_ms": round(elapsed, 2),
                "path_length": 0,
            },
        }

    def _reconstruct_path(self, came_from, action_from, goal):
        path = []
        current = goal
        while current is not None:
            path.append(current)
            current = came_from[current]
        path.reverse()
        return path