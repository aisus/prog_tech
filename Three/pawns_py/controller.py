from enum import Enum

from socketIO_client import SocketIO

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
        self.socketIo = None
        self.connect_to_server()

    def register_ui(self, ui: ChessUI):
        self.ui = ui

    def connect_to_server(self):
        self.socketIo = SocketIO('localhost', 5000)
        self.socketIo.on('connect', self.on_connect)
        self.socketIo.on('disconnect', self.on_disconnect)
        self.socketIo.connect()
        self.socketIo.wait()

    def on_connect(self, data):
        print(f"data : {data}")

    def on_disconnect(self):
        print('disconnect')
