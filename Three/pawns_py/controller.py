from game_state import *
from player_state import *


class GamePhase(Enum):
    WAITING = 0
    PLAYER_TURN = 1
    OPPONENT_TURN = 2
    WIN = 3
    LOSE = 4
    CONNECTION_LOST = 5
    RESTART = 6


class TurnState(Enum):
    WAITING = 0
    SELECTED = 1
    TURN = 2


class Controller:

    def __init__(self):
        self.game_state = GameState.initial_positions()
        self.player_state = PlayerState()
        self.phase = GamePhase.WAITING
        self.turn = TurnState.WAITING
