from enum import Enum


class FigureColor(Enum):
    WHITE = 0,
    BLACK = 1


class PlayerState:

    def __init__(self):
        self.color = FigureColor.WHITE
