import json
import socket

from flask import Flask
from flask_socketio import SocketIO, emit

from game import *

app = Flask(__name__)
socketio = SocketIO(app)
game = Game()


@app.route("/api/game_state", methods=['GET'])
def api_get_game_state():
    result = {
        "turn": game.current_turn.name,
        "board": game.board.grid,
        "winner": game.board.check_win_conditions()
    }
    return json.dumps(result, sort_keys=True, indent=3), 200


@socketio.on('get_game_state')
def get_game_state():
    result = {
        "turn": game.current_turn.name,
        "board": game.board.grid,
        "winner": game.board.check_win_conditions()
    }
    response = json.dumps(result, sort_keys=True, indent=3)
    socketio.emit('set_game_state', response)


@socketio.on('disconnect')
def handle_disconnect():
    print('====== DISCONNECTED')


@socketio.on('connect')
def handle_connect():
    print('======= CONNECTED')


@socketio.on('get_color')
def get_color():
    result = {
        "color": "",
    }
    if game.state == ServerState.WAITING:
        game.state = ServerState.FIRST_CLIENT_CONNECTED
        result = {
            "color": "WHITE",
        }
    elif game.state == ServerState.FIRST_CLIENT_CONNECTED:
        game.state = ServerState.GAME_RUNNING
        result = {
            "color": "BLACK",
        }
    response = json.dumps(result, sort_keys=True, indent=3)
    print(response)
    socketio.emit('set_color', response)


@socketio.on('do_move')
def handle_move(json_data):
    data = json.loads(json_data)
    result = {
        "status": False,
        "turn": game.current_turn.name,
        "board": game.board.grid
    }
    if data.color == game.current_turn:
        is_valid = validate_positions_and_do_move(data["selected"], data["target"])
        result = {
            "status": is_valid,
            "turn": game.current_turn.name,
            "board": game.board.grid
        }
    # if check_win_conditions finds no winner, it returns ''
    result["winner"] = game.board.check_win_conditions()
    response = json.dumps(result, sort_keys=True, indent=3)
    emit(response, namespace="/socket", broadcast=True)


def validate_positions_and_do_move(selected, target):
    t_i, t_j = target
    game.board.selected_cell = selected
    if game.board.validate_move(t_i, t_j):
        game.board.do_move(t_i, t_j)
        game.current_turn = Color(not game.current_turn)
        return True
    else:
        return False


if __name__ == "__main__":
    socketio.run(app, debug=True)
