
from enum import Enum

# White pawn
W = '\u2659'
# Black pawn
B = '\u265F'


class Color(Enum):
    WHITE = True,
    BLACK = False


class Board:

    def __init__(self, data):
        self.grid = data
        self.color = Color.WHITE
        self.selected_cell = []

    @classmethod
    def from_array(cls, grid):
        return cls(grid)

    @classmethod
    def empty(cls):
        return cls([[''] * 8] * 8)

    def get_unicode_figure_symbol(self):
        if self.color == Color.WHITE:
            return W
        else:
            return B

    def validate_selection(self, i, j):
        res = (self.grid[i][j] == W and self.color == Color.WHITE) or (
                    self.grid[i][j] == B and self.color == Color.BLACK)
        # print(f"validate {self.color} : {res}")
        return res

    def validate_move(self, i, j):

        def check_grid(grid, selected, target):
            i, j = selected
            t_i, t_j = target

            # Can't move backwards
            if t_i <= i:
                return False

            # Can go for two cells at first move
            if i == 1:
                if t_i - i > 2:
                    return False
            # Usually move for one cell
            elif t_i - i > 1:
                return False

            # Can move maximum for one cell right and left (while attacking)
            if abs(t_j - j) > 1:
                # print('too far aside')
                return False

            # We already checked that target can't be the same color figure, so
            # if it's not empty - it's enemy
            if grid[t_i][t_j] != '':
                # If enemy stands not in front of pawn
                if abs(t_j - j) == 1:
                    # It can attack!
                    return True
                return False
            # If there is no enemy - we just go forward as usual
            if t_j != j:
                return False
            return True

        # ______________________________________________________________________________
        # Can't go outside of a board
        if i < 0 or i > len(self.grid) or j < 0 or j > len(self.grid[0]):
            # print('outside')
            return False

        # Can't go to a cell with a figure of the same color
        if self.grid[i][j] == self.grid[self.selected_cell[0]][self.selected_cell[1]]:
            return False

        if self.grid[self.selected_cell[0]][self.selected_cell[1]] == W:
            return check_grid([x[::-1] for x in self.grid[::-1]], [len(self.grid) - self.selected_cell[0] - 1,
                                                                   len(self.grid[0]) - self.selected_cell[1] - 1],
                              [len(self.grid) - i - 1, len(self.grid[0]) - j - 1])
        else:
            return check_grid(self.grid, [self.selected_cell[0], self.selected_cell[1]], [i, j])
