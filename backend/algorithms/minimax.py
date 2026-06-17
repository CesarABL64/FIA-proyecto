import time


class MiniMax:
    def __init__(self, problem, max_depth=6):
        self.problem = problem
        self.max_depth = max_depth

    def search(self):
        start_time = time.time()
        steps = []
        state = self.problem.get_start_state()
        nodes_expanded = [0]

        best_move, best_value = self._minimax(
            state, 0, True, steps, nodes_expanded
        )

        path = self._reconstruct_game_path(state, best_move)
        elapsed = (time.time() - start_time) * 1000

        return {
            "steps": steps,
            "solution": {
                "path": path,
                "best_move": best_move,
                "best_value": best_value,
            },
            "metrics": {
                "nodes_expanded": nodes_expanded[0],
                "path_cost": 0,
                "execution_time_ms": round(elapsed, 2),
                "path_length": len(path),
            },
        }

    def _minimax(self, state, depth, is_maximizing, steps, nodes_expanded, record=True):
        nodes_expanded[0] += 1

        winner = self.problem.get_winner(state)
        if winner == "X":
            return None, 1
        elif winner == "O":
            return None, -1
        elif self.problem.is_full(state):
            return None, 0

        if depth >= self.max_depth:
            h = self.problem.heuristic(state)
            return None, h

        actions = self.problem.get_actions(state)
        if not actions:
            return None, 0

        should_record = record and depth <= 2

        if is_maximizing:
            best_value = float("-inf")
            best_move = None
            for action in actions:
                next_state = self.problem.result(state, action)
                _, value = self._minimax(
                    next_state, depth + 1, False, steps, nodes_expanded,
                    record=should_record
                )
                if should_record:
                    steps.append({
                        "current": state,
                        "action": action,
                        "next_state": next_state,
                        "value": value,
                        "player": "X",
                        "depth": depth,
                        "type": "max",
                        "description": f"X evalúa ({action[1]},{action[2]}) → valor={value}",
                    })
                if value > best_value:
                    best_value = value
                    best_move = action
            return best_move, best_value
        else:
            best_value = float("inf")
            best_move = None
            for action in actions:
                next_state = self.problem.result(state, action)
                _, value = self._minimax(
                    next_state, depth + 1, True, steps, nodes_expanded,
                    record=should_record
                )
                if should_record:
                    steps.append({
                        "current": state,
                        "action": action,
                        "next_state": next_state,
                        "value": value,
                        "player": "O",
                        "depth": depth,
                        "type": "min",
                        "description": f"O evalúa ({action[1]},{action[2]}) → valor={value}",
                    })
                if value < best_value:
                    best_value = value
                    best_move = action
            return best_move, best_value

    def _reconstruct_game_path(self, initial_state, first_move):
        path = [initial_state]
        state = initial_state
        move = first_move
        depth = 0
        while move is not None and depth < 9:
            state = self.problem.result(state, move)
            path.append(state)
            winner = self.problem.get_winner(state)
            if winner is not None or self.problem.is_full(state):
                break
            actions = self.problem.get_actions(state)
            if not actions:
                break
            best_value = float("-inf") if self.problem.current_player(state) == "X" else float("inf")
            best_move = None
            for action in actions:
                next_state = self.problem.result(state, action)
                winner_next = self.problem.get_winner(next_state)
                if winner_next == "X":
                    val = 1
                elif winner_next == "O":
                    val = -1
                elif self.problem.is_full(next_state):
                    val = 0
                else:
                    val = self.problem.heuristic(next_state)
                if self.problem.current_player(state) == "X":
                    if val > best_value:
                        best_value = val
                        best_move = action
                else:
                    if val < best_value:
                        best_value = val
                        best_move = action
            move = best_move
            depth += 1
        return path