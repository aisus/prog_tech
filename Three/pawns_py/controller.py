from enum import Enum

from board import Board
from ui import ChessUI


class TurnState(Enum):
    OPPONENT_TURN = 0
    WAITING = 1,
    SELECTED = 2


class Controller:

    def __init__(self):
        self.game_state = Board([[''] * 8] * 8)
        self.turn = TurnState.OPPONENT_TURN
        self.ui = None

    def register_ui(self, ui: ChessUI):
        self.ui = ui
