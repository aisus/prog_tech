from tkinter import *
from tkinter import messagebox

from app import Application
from board import TurnState

CELLS_COUNT = 8
MARGIN = 5
CELL_SIZE = 50
BOARD_WIDTH = BOARD_HEIGHT = MARGIN * 2 + CELL_SIZE * CELLS_COUNT

WHITE_CELL_COLOR = 'AntiqueWhite1'
BLACK_CELL_COLOR = 'AntiqueWhite3'
CURSOR_COLOR = 'MidnightBlue'
CURSOR_ON_FIGURE_COLOR = 'SeaGreen1'
SELECTION_COLOR = 'SeaGreen1'
CANT_SELECT_COLOR = 'red'
FIGURES_SIZE = 24


class ChessUI(Frame):
    def __init__(self, parent, application: Application):
        #parent.resizable(False, False)
        parent.geometry("%dx%d" % (BOARD_WIDTH, BOARD_HEIGHT + 40))
        Frame.__init__(self, parent)
        self.parent = parent
        self.app = application

        self.parent.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.cursor_row, self.cursor_col = -1, -1

        self.canvas = Canvas(
            self, width=BOARD_WIDTH, height=BOARD_HEIGHT,
            highlightthickness=0
        )

        self.textbox = Text(width=25, height=20, bg="gray", fg='white', wrap=WORD)
        self.color_box = Text(width=10, height=20, bg="gray", fg='white', wrap=WORD)

        self.init_ui()

    def init_ui(self):
        self.parent.title("Pawns")
        self.pack(fill=BOTH, expand=1)
        self.canvas.pack(fill=BOTH, side=TOP)
        self.textbox.pack()
        self.color_box.pack(side=LEFT)

        self.draw_grid()
        self.draw_figures()

        self.canvas.bind("<Button-1>", self.cell_clicked)
        self.canvas.bind("<Return>", self.return_pressed)
        self.update_helper_text()

    # _RENDERING________________________________________________________________________________
    def redraw(self):
        self.draw_figures()

    def update_helper_text(self):
        self.textbox.delete(1.0, END)
        self.textbox.insert(1.0, f"You're {self.app.game_state.color} \n but still nigger")

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
                if self.app.game_state.grid[i][j] != '':
                    self.canvas.create_text(
                        MARGIN + j * CELL_SIZE + CELL_SIZE / 2,
                        MARGIN + i * CELL_SIZE + CELL_SIZE / 2,
                        text=self.app.game_state.grid[i][j], tags="figures", font=('Purisa', FIGURES_SIZE)
                    )

    def draw_cursor(self):

        def get_cell_color():
            if self.app.game_state.turn == TurnState.WAITING:
                return CURSOR_ON_FIGURE_COLOR if self.app.game_state.validate_selection(self.cursor_row,
                                                                                        self.cursor_col) \
                    else CURSOR_COLOR
            elif self.app.game_state.turn == TurnState.SELECTED:
                return SELECTION_COLOR if self.app.game_state.validate_move(self.cursor_row, self.cursor_col) \
                    else CANT_SELECT_COLOR

        self.canvas.delete("cursor")
        if self.app.game_state.turn == TurnState.OPPONENT_TURN:
            return

        if self.cursor_row >= 0 and self.cursor_col >= 0:
            color = get_cell_color()
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
        self.update_helper_text()

    def return_pressed(self, event):
        if self.app.game_state.turn == TurnState.OPPONENT_TURN:
            return

        if self.app.game_state.turn != TurnState.SELECTED:
            if self.app.game_state.grid[self.cursor_row][self.cursor_col] == '':
                return
            if not self.app.game_state.validate_selection(self.cursor_row, self.cursor_col):
                return
            self.app.game_state.turn = TurnState.SELECTED
            self.app.game_state.selected_cell = [self.cursor_row, self.cursor_col]
            self.draw_selection()
        else:
            if not self.app.game_state.validate_move(self.cursor_row, self.cursor_col):
                return
            self.app.do_move([self.cursor_row, self.cursor_col])
            self.canvas.delete('cursor')
            self.reset_selection()
            self.draw_figures()
            self.update_helper_text()

    # _UTILITY_______________________________________________________________________________________
    def reset_selection(self):
        self.cursor_row, self.cursor_col = -1, -1
        self.canvas.delete("selection")
        self.app.game_state.turn = TurnState.WAITING

    def on_closing(self):
        #if messagebox.askokcancel("Quit", "Do you want to quit?"):
        self.app.stop()
        self.parent.destroy()
