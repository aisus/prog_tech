import json

from flask import Flask
from flask_socketio import SocketIO, send, emit

from game import *

app = Flask(__name__)
socketIo = SocketIO(app)
game = Game()


@socketIo.on('connect')
def connect():
    result = {
        "color": "",
    }
    if game.state == ServerState.WAITING:
        game.state = ServerState.FIRST_CLIENT_CONNECTED
        result = {
            "color": "white",
        }
    elif game.state == ServerState.FIRST_CLIENT_CONNECTED:
        game.state = ServerState.GAME_RUNNING
        result = {
            "color": "black",
        }
    response = json.dumps(result, sort_keys=True, indent=3)
    while True:
        send(response)


@socketIo.on("move", namespace="/socket")
def handle_move(json_data):
    data = json.loads(json_data)
    result = {
        "status": False,
        "turn": game.current_turn,
        "board": game.board.grid
    }
    if data.color == game.current_turn:
        is_valid = validate_positions_and_do_move(data)
        result = {
            "status": is_valid,
            "turn": game.current_turn,
            "board": game.board.grid
        }
    # if check_win_conditions finds no winner, it returns ''
    result["winner"] = game.board.check_win_conditions()
    response = json.dumps(result, sort_keys=True, indent=3)
    emit(response, namespace="/socket", broadcast=True)


def validate_positions_and_do_move(data):
    selected = data.selected
    t_i, t_j = data.target
    game.board.selected_cell = selected
    if game.board.validate_move(t_i, t_j):
        game.board.do_move(t_i, t_j)
        game.current_turn = Color(not game.current_turn)
        return True
    else:
        return False


if __name__ == "__main__":
    socketIo.run(app)
