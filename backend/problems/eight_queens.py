class EightQueens:
    def __init__(self):
        self.size = 8

    def get_start_state(self):
        return tuple(range(8))

    def is_goal(self, state):
        return self.count_attacks(state) == 0

    def count_attacks(self, state):
        attacks = 0
        for i in range(self.size):
            for j in range(i + 1, self.size):
                if state[i] == state[j]:
                    attacks += 1
                elif abs(state[i] - state[j]) == abs(i - j):
                    attacks += 1
        return attacks

    def get_neighbors(self, state):
        neighbors = []
        for row in range(self.size):
            for col in range(self.size):
                if state[row] != col:
                    new_state = list(state)
                    new_state[row] = col
                    neighbors.append(tuple(new_state))
        return neighbors

    def heuristic(self, state):
        return self.count_attacks(state)

    def get_board_for_display(self, state):
        board = []
        for r in range(self.size):
            row = []
            for c in range(self.size):
                row.append("Q" if state[r] == c else " ")
            board.append(row)
        return board

    def get_attacked_cells(self, state):
        attacked = set()
        for r in range(self.size):
            c = state[r]
            for cc in range(self.size):
                if cc != c:
                    attacked.add((r, cc))
            for rr in range(self.size):
                if rr != r:
                    attacked.add((rr, c))
            for d in range(1, self.size):
                for dr, dc in [(d, d), (d, -d), (-d, d), (-d, -d)]:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < self.size and 0 <= nc < self.size:
                        attacked.add((nr, nc))
        conflict_cells = set()
        for i in range(self.size):
            for j in range(i + 1, self.size):
                if state[i] == state[j]:
                    conflict_cells.add((i, state[i]))
                    conflict_cells.add((j, state[j]))
                elif abs(state[i] - state[j]) == abs(i - j):
                    conflict_cells.add((i, state[i]))
                    conflict_cells.add((j, state[j]))
        return attacked, conflict_cells
