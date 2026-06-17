from collections import deque
import copy


class FrozenLake:
    GRID_CONFIGS = {
        4: [
            ["S", "F", "F", "F"],
            ["F", "H", "F", "H"],
            ["F", "F", "F", "H"],
            ["H", "F", "F", "G"],
        ],
        5: [
            ["S", "F", "F", "F", "H"],
            ["F", "H", "F", "F", "F"],
            ["F", "F", "F", "H", "F"],
            ["H", "F", "H", "F", "F"],
            ["F", "F", "F", "F", "G"],
        ],
        6: [
            ["S", "F", "F", "H", "F", "F"],
            ["F", "H", "F", "F", "F", "H"],
            ["F", "F", "F", "H", "F", "F"],
            ["H", "F", "H", "F", "F", "F"],
            ["F", "F", "F", "F", "H", "F"],
            ["H", "F", "F", "F", "F", "G"],
        ],
    }

    def __init__(self, grid_size=4):
        self.grid_size = grid_size
        self.grid = self.GRID_CONFIGS.get(grid_size, self.GRID_CONFIGS[4])
        self.start = self._find_cell("S")
        self.goal = self._find_cell("G")
        self.holes = self._find_all_cells("H")

    def _find_cell(self, cell_type):
        for r in range(len(self.grid)):
            for c in range(len(self.grid[r])):
                if self.grid[r][c] == cell_type:
                    return (r, c)
        return None

    def _find_all_cells(self, cell_type):
        cells = []
        for r in range(len(self.grid)):
            for c in range(len(self.grid[r])):
                if self.grid[r][c] == cell_type:
                    cells.append((r, c))
        return cells

    def get_start_state(self):
        return self.start

    def is_goal(self, state):
        return state == self.goal

    def is_hole(self, state):
        return state in self.holes

    def get_actions(self, state):
        actions = []
        r, c = state
        moves = {
            "up": (r - 1, c),
            "down": (r + 1, c),
            "left": (r, c - 1),
            "right": (r, c + 1),
        }
        for action, (nr, nc) in moves.items():
            if 0 <= nr < self.grid_size and 0 <= nc < self.grid_size:
                if not self.is_hole((nr, nc)):
                    actions.append((action, (nr, nc)))
        return actions

    def result(self, state, action, next_state):
        return next_state

    def step_cost(self, state, action, next_state):
        return 1

    def heuristic(self, state):
        return abs(state[0] - self.goal[0]) + abs(state[1] - self.goal[1])

    def get_grid_for_display(self):
        return copy.deepcopy(self.grid)
