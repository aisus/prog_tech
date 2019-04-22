import json

from flask import Flask
from flask_socketio import SocketIO, emit
import socket_events as events

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


@socketio.on(events.GET_GAME_STATE)
def get_game_state():
    result = {
        "turn": game.current_turn.name,
        "board": game.board.grid,
        "winner": game.board.check_win_conditions()
    }
    response = json.dumps(result, sort_keys=True, indent=3)
    socketio.emit(events.SET_GAME_STATE, response)


@socketio.on(events.DISCONNECT)
def handle_disconnect():
    print('====== DISCONNECTED')
    game.state = ServerState.WAITING


@socketio.on(events.CONNECT)
def handle_connect():
    print('======= CONNECTED')


@socketio.on(events.GET_COLOR)
def get_color():
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
    print(response)
    socketio.emit(events.SET_COLOR, response)


@socketio.on(events.DO_MOVE)
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
    socketio.emit(events.SET_GAME_STATE, response)


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
