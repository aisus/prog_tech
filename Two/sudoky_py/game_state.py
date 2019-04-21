from itertools import chain


class GameState:
    def __init__(self, data):
        self.grid = data

    @classmethod
    def from_array(cls, grid):
        return cls(grid)

    @classmethod
    def empty(cls):
        grid = [[0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0]]
        return cls(grid)

    def validate_sudoku_solution(self):

        def validate_rows(grid):
            for i in range(len(grid)):
                if sum(grid[i]) != sum(set(grid[i])):
                    return False
            return True

        def validate_columns(grid):
            t_grid = list(zip(*grid))
            return validate_rows(t_grid)

        def validate_squares(grid):
            for i in range(0, 4, 2):
                for j in range(0, 4, 2):
                    square = list(chain(*(row[j:j + 2] for row in grid[i:i + 2])))
                    if sum(square) != sum(set(square)):
                        return False
            return True

        rows_status = validate_rows(self.grid)
        columns_status = validate_columns(self.grid)
        squares_status = validate_squares(self.grid)

        valid = rows_status and columns_status and squares_status

        if valid:
            return 'Solution valid!'

        message = 'Failed: '
        if not rows_status:
            message += 'rows '
        if not columns_status:
            message += 'columns '
        if not squares_status:
            message += 'squares '

        return message
