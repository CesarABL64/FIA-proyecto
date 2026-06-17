import random
import time


class HillClimbing:
    def __init__(self, problem, max_restarts=20):
        self.problem = problem
        self.max_restarts = max_restarts

    def search(self):
        start_time = time.time()
        steps = []

        best_state = None
        best_attacks = float("inf")
        total_restarts = 0
        nodes_expanded = 0

        for restart in range(self.max_restarts):
            if restart == 0:
                current = self.problem.get_start_state()
            else:
                current = tuple(random.randint(0, 7) for _ in range(8))

            current_attacks = self.problem.heuristic(current)

            steps.append({
                "current": current,
                "attacks": current_attacks,
                "type": "restart" if restart > 0 else "start",
                "description": f"{'Reinicio' if restart > 0 else 'Inicio'}: {current}, ataques={current_attacks}",
            })

            if current_attacks == 0:
                elapsed = (time.time() - start_time) * 1000
                return {
                    "steps": steps,
                    "solution": {"path": [current], "state": current},
                    "metrics": {
                        "nodes_expanded": nodes_expanded,
                        "path_cost": 0,
                        "execution_time_ms": round(elapsed, 2),
                        "path_length": 1,
                        "restarts": total_restarts,
                    },
                }

            if current_attacks < best_attacks:
                best_state = current
                best_attacks = current_attacks

            improving = True
            while improving:
                improving = False
                neighbors = self.problem.get_neighbors(current)
                nodes_expanded += len(neighbors)

                best_neighbor = None
                best_neighbor_attacks = current_attacks

                for neighbor in neighbors:
                    neighbor_attacks = self.problem.heuristic(neighbor)
                    if neighbor_attacks < best_neighbor_attacks:
                        best_neighbor = neighbor
                        best_neighbor_attacks = neighbor_attacks
                        improving = True

                if improving and best_neighbor is not None:
                    current = best_neighbor
                    current_attacks = best_neighbor_attacks

                    steps.append({
                        "current": current,
                        "attacks": current_attacks,
                        "type": "move",
                        "description": f"Movimiento a {current}, ataques={current_attacks}",
                    })

                    if current_attacks == 0:
                        elapsed = (time.time() - start_time) * 1000
                        return {
                            "steps": steps,
                            "solution": {"path": [current], "state": current},
                            "metrics": {
                                "nodes_expanded": nodes_expanded,
                                "path_cost": 0,
                                "execution_time_ms": round(elapsed, 2),
                                "path_length": 1,
                                "restarts": total_restarts,
                            },
                        }

                    if current_attacks < best_attacks:
                        best_state = current
                        best_attacks = current_attacks

            total_restarts += 1

        elapsed = (time.time() - start_time) * 1000
        return {
            "steps": steps,
            "solution": {"path": [best_state], "state": best_state} if best_state else None,
            "metrics": {
                "nodes_expanded": nodes_expanded,
                "path_cost": 0,
                "execution_time_ms": round(elapsed, 2),
                "path_length": 1,
                "restarts": total_restarts,
                "best_attacks": best_attacks,
            },
        }