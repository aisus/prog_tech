# White pawn
W = '\u2659'
# Black pawn
B = '\u265F'


class GameState:

    def __init__(self, data):
        self.grid = data
        self.selected_cell = []

    @classmethod
    def from_array(cls, grid):
        return cls(grid)

    @classmethod
    def empty(cls):
        grid = [[''] * 8] * 8
        return cls(grid)

    @classmethod
    def initial_positions(cls):
        grid = [
            [B, B, B, B, B, B, B, B],
            ['', '', '', '', '', '', '', ''],
            ['', '', '', '', '', '', '', ''],
            ['', '', '', '', '', '', '', ''],
            ['', '', '', '', '', '', '', ''],
            ['', '', '', '', '', '', '', ''],
            ['', '', '', '', '', '', '', ''],
            [W, W, W, W, W, W, W, W], ]
        return cls(grid)

    def check_win_conditions(self):
        pass

    def do_move(self, i, j):
        f = self.grid[self.selected_cell[0]][self.selected_cell[1]]
        self.grid[i][j] = f
        self.grid[self.selected_cell[0]][self.selected_cell[1]] = ''

    def validate_move(self, i, j):

        def check_grid(grid, selected, target):
            i, j = selected
            t_i, t_j = target
            print(f"recalc. s: {i, j} tar: {t_i, t_j}")

            # Can't move backwards
            if t_i <= i:
                print(f'backwards {t_i} {i}')
                return False

            # Can go for two cells at first move
            if i == 0:
                if t_i - i > 2:
                    print('first move > 2')
                    return False
            # Usually move for one cell
            elif t_i - i > 1:
                print('move > 1')
                return False

            # Can move maximum for one cell right and left (while attacking)
            if abs(t_j - j) > 1:
                print('too far aside')
                return False

            # We already checked that target can't be the same color figure, so
            # if it's not empty - it's enemy
            print(grid)
            if grid[t_i][t_j] != '':
                print('enemy stand')
                # If enemy stands not in front of pawn
                if abs(t_j - j) == 1:
                    # It can attack!
                    print("can attack!")
                    return True
                print('enemy in front')
                return False
            # If there is no enemy - we just go forward as usual
            if t_j != j:
                return False
            print("can go!")
            return True

        # ______________________________________________________________________________
        print(f"sel:{self.selected_cell}, trg:{i, j}")
        # Can't go outside of a board
        if i < 0 or i > len(self.grid) or j < 0 or j > len(self.grid[0]):
            print('outside')
            return False

        # Can't go to a cell with a figure of the same color
        if self.grid[i][j] == self.grid[self.selected_cell[0]][self.selected_cell[1]]:
            print('same color')
            return False

        if self.grid[self.selected_cell[0]][self.selected_cell[1]] == W:
            return check_grid([x[::-1] for x in self.grid[::-1]], [len(self.grid) - self.selected_cell[0] - 1,
                                                                   len(self.grid[0]) - self.selected_cell[1] - 1],
                              [len(self.grid) - i - 1, len(self.grid[0]) - j - 1])
        else:
            return check_grid(self.grid, [self.selected_cell[0], self.selected_cell[1]], [i, j])
