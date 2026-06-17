import copy


class Sokoban:
    LEVELS = {
        1: {
            "walls": [
                (0, 0), (0, 1), (0, 2), (0, 3), (0, 4),
                (1, 0), (1, 4),
                (2, 0), (2, 4),
                (3, 0), (3, 1), (3, 4),
            ],
            "player": (1, 1),
            "boxes": [(2, 2)],
            "goals": [(2, 1)],
            "rows": 4,
            "cols": 5,
        },
        2: {
            "walls": [
                (0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5),
                (1, 0), (1, 5),
                (2, 0), (2, 5),
                (3, 0), (3, 3), (3, 5),
                (4, 0), (4, 1), (4, 2), (4, 3), (4, 4), (4, 5),
            ],
            "player": (1, 1),
            "boxes": [(2, 2), (2, 3)],
            "goals": [(2, 1), (3, 4)],
            "rows": 5,
            "cols": 6,
        },
        3: {
            "walls": [
                (0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6),
                (1, 0), (1, 6),
                (2, 0), (2, 6),
                (3, 0), (3, 6),
                (4, 0), (4, 6),
                (5, 0), (5, 1), (5, 2), (5, 3), (5, 4), (5, 5), (5, 6),
            ],
            "player": (1, 1),
            "boxes": [(2, 2), (3, 3), (3, 4)],
            "goals": [(2, 3), (3, 1), (4, 5)],
            "rows": 6,
            "cols": 7,
        },
    }

    def __init__(self, level=1):
        config = self.LEVELS.get(level, self.LEVELS[1])
        self.walls = set(config["walls"])
        self.rows = config["rows"]
        self.cols = config["cols"]
        self.goals = set(config["goals"])
        self.initial_player = config["player"]
        self.initial_boxes = frozenset(config["boxes"])

    def get_start_state(self):
        return (self.initial_player, self.initial_boxes)

    def is_goal(self, state):
        _, boxes = state
        return boxes == self.goals

    def get_actions(self, state):
        actions = []
        player, boxes = state
        r, c = player
        moves = {
            "up": (r - 1, c),
            "down": (r + 1, c),
            "left": (r, c - 1),
            "right": (r, c + 1),
        }
        for action, (nr, nc) in moves.items():
            if (nr, nc) in self.walls:
                continue
            if (nr, nc) not in boxes:
                actions.append((action, ((nr, nc), boxes)))
            else:
                br, bc = nr, nc
                push_moves = {
                    "up": (br - 1, bc),
                    "down": (br + 1, bc),
                    "left": (br, bc - 1),
                    "right": (br, bc + 1),
                }
                box_dest = push_moves[action]
                if box_dest not in self.walls and box_dest not in boxes:
                    new_boxes = frozenset((boxes - {(nr, nc)}) | {box_dest})
                    actions.append((action, ((nr, nc), new_boxes)))
        return actions

    def result(self, state, action, next_state):
        return next_state

    def step_cost(self, state, action, next_state):
        return 1

    def heuristic(self, state):
        _, boxes = state
        total = 0
        for box in boxes:
            min_dist = min(
                abs(box[0] - g[0]) + abs(box[1] - g[1]) for g in self.goals
            )
            total += min_dist
        return total

    def get_grid_for_display(self, state=None):
        grid = []
        for r in range(self.rows):
            row = []
            for c in range(self.cols):
                if (r, c) in self.walls:
                    row.append("W")
                else:
                    row.append(" ")
            grid.append(row)
        if state:
            player, boxes = state
            for g in self.goals:
                if g not in boxes:
                    grid[g[0]][g[1]] = "G"
            for b in boxes:
                if b in self.goals:
                    grid[b[0]][b[1]] = "B"
                else:
                    grid[b[0]][b[1]] = "B"
            pr, pc = player
            grid[pr][pc] = "P"
        return grid
