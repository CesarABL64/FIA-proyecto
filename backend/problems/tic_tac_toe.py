class TicTacToe:
    def __init__(self):
        self.size = 3

    def get_start_state(self):
        return tuple(tuple(" " for _ in range(3)) for _ in range(3))

    def is_goal(self, state):
        return self.get_winner(state) is not None or self.is_full(state)

    def get_winner(self, state):
        lines = []
        for r in range(3):
            lines.append([(r, 0), (r, 1), (r, 2)])
        for c in range(3):
            lines.append([(0, c), (1, c), (2, c)])
        lines.append([(0, 0), (1, 1), (2, 2)])
        lines.append([(0, 2), (1, 1), (2, 0)])
        for line in lines:
            vals = [state[r][c] for r, c in line]
            if vals[0] != " " and vals[0] == vals[1] == vals[2]:
                return vals[0]
        return None

    def is_full(self, state):
        return all(state[r][c] != " " for r in range(3) for c in range(3))

    def current_player(self, state):
        x_count = sum(1 for r in range(3) for c in range(3) if state[r][c] == "X")
        o_count = sum(1 for r in range(3) for c in range(3) if state[r][c] == "O")
        return "X" if x_count <= o_count else "O"

    def get_actions(self, state):
        if self.get_winner(state) is not None:
            return []
        player = self.current_player(state)
        actions = []
        for r in range(3):
            for c in range(3):
                if state[r][c] == " ":
                    actions.append((player, r, c))
        return actions

    def result(self, state, action):
        player, r, c = action
        new_state = [list(row) for row in state]
        new_state[r][c] = player
        return tuple(tuple(row) for row in new_state)

    def evaluate(self, state):
        winner = self.get_winner(state)
        if winner == "X":
            return 1
        elif winner == "O":
            return -1
        if self.is_full(state):
            return 0
        return None

    def heuristic(self, state):
        ev = self.evaluate(state)
        if ev is not None:
            return ev
        score = 0
        lines = []
        for r in range(3):
            lines.append([(r, 0), (r, 1), (r, 2)])
        for c in range(3):
            lines.append([(0, c), (1, c), (2, c)])
        lines.append([(0, 0), (1, 1), (2, 2)])
        lines.append([(0, 2), (1, 1), (2, 0)])
        for line in lines:
            vals = [state[r][c] for r, c in line]
            x_count = vals.count("X")
            o_count = vals.count("O")
            if o_count == 0:
                score += x_count
            if x_count == 0:
                score -= o_count
        return score

    def get_board_for_display(self, state):
        return [list(row) for row in state]
