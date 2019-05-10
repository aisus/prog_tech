from board import Board, Color
from ui import *
from tkinter import Tk
import socket
import json
import socket_events as events
import threading

PORT = 8000


class Application:
    def __init__(self, sock: socket):
        self.root = Tk()
        self.sock = sock
        self.game_state = Board.from_array([[''] * 8] * 8)
        self.ui = ChessUI(self.root, self)

    def set_color(self, obj):
        color = obj["color"]
        self.game_state.color = Color[color]
        self.ui.update_helper_text()

    def set_game_state(self, obj):
        board = obj['board']
        self.game_state.grid = board
        self.ui.redraw()

    def do_move(self, target_cell):
        response = {
            "color": self.game_state.color.name,
            "event": events.DO_MOVE,
            "selected": self.game_state.selected_cell,
            "target": target_cell
        }
        msg = json.dumps(response, sort_keys=True, indent=3)
        sock.send(msg.encode('utf-8'))

    def stop(self):
        self.sock.close()


def message_handle_thread(sock: socket, app: Application):
    sock.connect((host, PORT))

    get_color(sock)
    proceed_server_message(sock, app)
    get_game_state(sock)

    while True:
        proceed_server_message(sock, app)


def get_color(sock: socket):
    response = {
        "event": events.GET_COLOR
    }
    msg = json.dumps(response, sort_keys=True, indent=3)
    sock.send(msg.encode('utf-8'))


def get_game_state(sock: socket):
    response = {
        "event": events.GET_GAME_STATE
    }
    msg = json.dumps(response, sort_keys=True, indent=3)
    sock.send(msg.encode('utf-8'))


def proceed_server_message(sock: socket, app: Application):
    msg = sock.recv(8192).decode('utf-8')
    print(msg)
    obj = json.loads(msg)
    event = obj['event']
    if event == events.SET_COLOR:
        app.set_color(obj)
    elif event == events.SET_GAME_STATE:
        app.set_game_state(obj)
    elif event == events.VALIDATE_MOVE:
        app.set_game_state(obj)


if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = socket.gethostname()
    app = Application(sock)
    reciever_thread = threading.Thread(target=message_handle_thread, args=(sock, app))
    reciever_thread.start()
    app.root.mainloop()

