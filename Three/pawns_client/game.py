from enum import Enum

from board import *


class TurnState(Enum):
    OPPONENT_TURN = 0
    WAITING = 1,
    SELECTED = 2


class Game(object):
    def __init__(self):
        self.color = Color.WHITE
        self.turn = TurnState.WAITING
        self.is_our_move = True
        self.board = Board.empty()
        self.move_idx = 0

    def set_color(self, color):
        self.color = color
        self.board.color = color

    def set_turn(self, color):
        self.is_our_move = color == self.color
