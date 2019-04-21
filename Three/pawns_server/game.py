from enum import Enum
from board import *


class Color(Enum):
    WHITE = True,
    BLACK = False


class ServerState(Enum):
    WAITING = 0
    FIRST_CLIENT_CONNECTED = 1,
    BOTH_CLIENTS_CONNECTED = 2,
    GAME_RUNNING = 3,
    CONNECTION_FAIL = 4,
    GAME_FINISHED = 5


class Game(object):
    def __init__(self):
        self.state = ServerState.WAITING
        self.current_turn = Color.WHITE
        self.board = Board.initial_positions()
