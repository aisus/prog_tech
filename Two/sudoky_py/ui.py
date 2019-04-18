from tkinter import Tk, Canvas, Frame, BOTH, TOP, WORD, END, Text
from xml_utils import *

CELLS_COUNT = 4
MARGIN = 0
CELL_SIZE = 50
BOARD_WIDTH = BOARD_HEIGHT = MARGIN * 2 + CELL_SIZE * CELLS_COUNT
GAME_STATE_PATH = 'game_state.xml'
VALID_CHARACTERS = '12340'


class SudokuUI(Frame):
    def __init__(self, parent, game_state):
        Frame.__init__(self, parent)
        self.parent = parent
        self.game_state = game_state

        self.selected_row, self.selected_col = -1, -1

        self.canvas = Canvas(
            self, width=BOARD_WIDTH, height=BOARD_HEIGHT,
            highlightthickness=0
        )

        self.textbox = Text(width=25, height=20, bg="gray", fg='white', wrap=WORD)

        self.init_ui()

    def init_ui(self):
        self.parent.title("Sudoku")
        self.pack(fill=BOTH, expand=1)
        self.canvas.pack(fill=BOTH, side=TOP)
        self.textbox.pack()

        self.draw_grid()
        self.draw_numbers()
        self.check_result()

        self.canvas.bind("<Button-1>", self.cell_clicked)
        self.canvas.bind("<Key>", self.key_pressed)

    # _RENDERING________________________________________________________________________________
    def draw_grid(self):
        for i in range(CELLS_COUNT + 1):
            self.canvas.create_line(
                MARGIN + i * CELL_SIZE, MARGIN,
                MARGIN + i * CELL_SIZE, BOARD_HEIGHT - MARGIN,
                fill="blue" if i % 3 == 0 else "gray"
            )

            self.canvas.create_line(
                MARGIN, MARGIN + i * CELL_SIZE, BOARD_WIDTH - MARGIN, MARGIN + i * CELL_SIZE,
                fill="blue" if i % 3 == 0 else "gray"
            )

    def draw_numbers(self):
        self.canvas.delete("numbers")
        for i in range(CELLS_COUNT):
            for j in range(CELLS_COUNT):
                if self.game_state.grid[i][j] != 0:
                    self.canvas.create_text(
                        MARGIN + j * CELL_SIZE + CELL_SIZE / 2,
                        MARGIN + i * CELL_SIZE + CELL_SIZE / 2,
                        text=self.game_state.grid[i][j], tags="numbers",
                    )

    def draw_cursor(self):
        self.canvas.delete("cursor")
        if self.selected_row >= 0 and self.selected_col >= 0:
            self.canvas.create_rectangle(
                MARGIN + self.selected_col * CELL_SIZE + 1,
                MARGIN + self.selected_row * CELL_SIZE + 1,
                MARGIN + (self.selected_col + 1) * CELL_SIZE - 1,
                MARGIN + (self.selected_row + 1) * CELL_SIZE - 1,
                outline="red", tags="cursor"
            )

    # _INPUT HANDLERS___________________________________________________________________________
    def cell_clicked(self, event):
        x, y = event.x, event.y
        if (MARGIN < x < BOARD_WIDTH - MARGIN and
                MARGIN < y < BOARD_HEIGHT - MARGIN):
            self.canvas.focus_set()
            row, col = int((y - MARGIN) / CELL_SIZE), int((x - MARGIN) / CELL_SIZE)
            if (row, col) == (self.selected_row, self.selected_col):
                self.selected_row, self.selected_col = -1, -1
            else:
                self.selected_row, self.selected_col = row, col
        else:
            self.selected_row, self.selected_col = -1, -1

        self.draw_cursor()

    def key_pressed(self, event):
        if self.selected_row >= 0 and self.selected_col >= 0 and event.char in VALID_CHARACTERS:
            self.game_state.grid[self.selected_row][self.selected_col] = int(event.char)
            save_game_state(GAME_STATE_PATH, self.game_state)
            self.selected_col, self.selected_row = -1, -1
            self.draw_numbers()
            self.draw_cursor()
            self.check_result()

    # _UTILITY___________________________________________________________________________________
    def check_result(self):
        message = self.game_state.validate_sudoku_solution()
        # print(message)
        self.textbox.delete(1.0, END)
        self.textbox.insert(1.0, message)


if __name__ == '__main__':
    root = Tk()
    loaded_game_state = load_game_state(GAME_STATE_PATH, 4, VALID_CHARACTERS)
    ui = SudokuUI(root, loaded_game_state)
    root.geometry("%dx%d" % (BOARD_WIDTH, BOARD_HEIGHT + 40))
    root.mainloop()
