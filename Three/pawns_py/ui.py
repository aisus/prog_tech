from tkinter import Tk, Canvas, Frame, BOTH, TOP, WORD, END, Text
from controller import *

CELLS_COUNT = 8
MARGIN = 5
CELL_SIZE = 50
BOARD_WIDTH = BOARD_HEIGHT = MARGIN * 2 + CELL_SIZE * CELLS_COUNT

WHITE_CELL_COLOR = 'AntiqueWhite1'
BLACK_CELL_COLOR = 'AntiqueWhite3'
CURSOR_COLOR = 'MidnightBlue'
CURSOR_ON_FIGURE_COLOR = ''
SELECTION_COLOR = 'SeaGreen1'
CANT_SELECT_COLOR = 'red'
FIGURES_SIZE = 24


class ChessUI(Frame):
    def __init__(self, parent, ctrl):
        Frame.__init__(self, parent)
        self.parent = parent
        self.controller = ctrl
        self.game_state = controller.game_state

        self.cursor_row, self.cursor_col = -1, -1

        self.canvas = Canvas(
            self, width=BOARD_WIDTH, height=BOARD_HEIGHT,
            highlightthickness=0
        )

        self.textbox = Text(width=25, height=20, bg="gray", fg='white', wrap=WORD)

        self.init_ui()

    def init_ui(self):
        self.parent.title("Pawns")
        self.pack(fill=BOTH, expand=1)
        self.canvas.pack(fill=BOTH, side=TOP)
        self.textbox.pack()

        self.draw_grid()
        self.draw_figures()

        self.canvas.bind("<Button-1>", self.cell_clicked)
        self.canvas.bind("<Return>", self.return_pressed)

    # _RENDERING________________________________________________________________________________
    def draw_grid(self):
        for i in range(CELLS_COUNT):
            for j in range(CELLS_COUNT):
                color = [BLACK_CELL_COLOR, WHITE_CELL_COLOR][(i - j) % 2]
                self.canvas.create_rectangle(
                    MARGIN + i * CELL_SIZE, MARGIN + j * CELL_SIZE,
                    MARGIN + (i + 1) * CELL_SIZE, MARGIN + (j + 1) * CELL_SIZE,
                    fill=color
                )

    def draw_figures(self):
        self.canvas.delete("figures")
        for i in range(CELLS_COUNT):
            for j in range(CELLS_COUNT):
                if self.game_state.grid[i][j] != '':
                    self.canvas.create_text(
                        MARGIN + j * CELL_SIZE + CELL_SIZE / 2,
                        MARGIN + i * CELL_SIZE + CELL_SIZE / 2,
                        text=self.game_state.grid[i][j], tags="figures", font=('Purisa', FIGURES_SIZE)
                    )

    def draw_cursor(self):

        def get_color():
            if self.controller.turn != TurnState.SELECTED:
                return CURSOR_ON_FIGURE_COLOR if self.game_state.grid[self.cursor_row][self.cursor_col] != '' \
                    else CURSOR_COLOR
            else:
                return SELECTION_COLOR if self.game_state.validate_move(self.cursor_row, self.cursor_col) \
                    else CANT_SELECT_COLOR

        self.canvas.delete("cursor")
        if self.cursor_row >= 0 and self.cursor_col >= 0:
            color = get_color()
            self.canvas.create_rectangle(
                MARGIN + self.cursor_col * CELL_SIZE + 1,
                MARGIN + self.cursor_row * CELL_SIZE + 1,
                MARGIN + (self.cursor_col + 1) * CELL_SIZE - 1,
                MARGIN + (self.cursor_row + 1) * CELL_SIZE - 1,
                outline=color, width=2, tags="cursor"
            )

    def draw_selection(self):
        self.canvas.delete("selection")
        if self.cursor_row >= 0 and self.cursor_col >= 0:
            color = SELECTION_COLOR
            self.canvas.create_rectangle(
                MARGIN + self.cursor_col * CELL_SIZE + 1,
                MARGIN + self.cursor_row * CELL_SIZE + 1,
                MARGIN + (self.cursor_col + 1) * CELL_SIZE - 1,
                MARGIN + (self.cursor_row + 1) * CELL_SIZE - 1,
                outline=color, width=2, tags="selection"
            )

    # _INPUT HANDLERS___________________________________________________________________________
    def cell_clicked(self, event):
        x, y = event.x, event.y
        if (MARGIN < x < BOARD_WIDTH - MARGIN and
                MARGIN < y < BOARD_HEIGHT - MARGIN):
            self.canvas.focus_set()
            row, col = int((y - MARGIN) / CELL_SIZE), int((x - MARGIN) / CELL_SIZE)
            if (row, col) == (self.cursor_row, self.cursor_col):
                self.reset_selection()
            else:
                self.cursor_row, self.cursor_col = row, col
        else:
            self.reset_selection()

        self.draw_cursor()

    def return_pressed(self, event):
        if self.controller.turn != TurnState.SELECTED:
            if self.game_state.grid[self.cursor_row][self.cursor_col] == '':
                return

            self.controller.turn = TurnState.SELECTED
            self.game_state.selected_cell = [self.cursor_row, self.cursor_col]
            self.draw_selection()
        else:
            if not self.game_state.validate_move(self.cursor_row, self.cursor_col):
                return
            self.game_state.do_move(self.cursor_row, self.cursor_col)
            self.canvas.delete('cursor')
            self.reset_selection()
            self.draw_figures()

    # _UTILITY_______________________________________________________________________________________
    def reset_selection(self):
        self.cursor_row, self.cursor_col = -1, -1
        self.canvas.delete("selection")
        self.controller.turn = TurnState.WAITING


#     self.textbox.delete(1.0, END)
#        self.textbox.insert(1.0, message)


if __name__ == '__main__':
    root = Tk()
    root.resizable(False, False)
    controller = Controller()
    ui = ChessUI(root, controller)
    root.geometry("%dx%d" % (BOARD_WIDTH, BOARD_HEIGHT + 40))
    root.mainloop()
