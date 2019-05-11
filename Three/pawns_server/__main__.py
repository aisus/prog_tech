import json

import socket
import socket_events as events
from threading import Thread

from game import *

PORT = 8000

game = Game()
connected_sockets = []


class SocketThread(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self, clientsocket, addr):
        proceed_client(clientsocket, addr)


def do_broadcast(message):
    for s in connected_sockets:
        s.send(message.encode('utf-8'))


def get_game_state():
    result = {
        "event": events.SET_GAME_STATE,
        "turn": game.current_turn.name,
        "board": game.board.grid,
        "winner": game.board.check_win_conditions()
    }
    response = json.dumps(result, sort_keys=True, indent=3)
    return response


def get_color():
    result = {
        "event": events.SET_COLOR,
        "color": "",
    }
    if game.state == ServerState.FIRST_CLIENT_CONNECTED:
        result["color"] = Color.WHITE.name
    elif game.state == ServerState.BOTH_CLIENTS_CONNECTED:
        game.state = ServerState.GAME_RUNNING
        result["color"] = Color.BLACK.name
    response = json.dumps(result, sort_keys=True, indent=3)
    return response


def handle_move(json_data):
    result = {
        "event": events.SET_GAME_STATE,
        "status": False,
        "turn": game.current_turn.name,
        "board": game.board.grid
    }
    # if json_data["color"] == game.current_turn:
    if True:
        is_valid = validate_positions_and_do_move(json_data["selected"], json_data["target"])
        result = {
            "event": events.SET_GAME_STATE,
            "status": is_valid,
            "turn": game.current_turn.name,
            "board": game.board.grid
        }
    # if check_win_conditions finds no winner, it returns ''
    result["winner"] = game.board.check_win_conditions()
    response = json.dumps(result, sort_keys=True, indent=3)
    return response


def validate_positions_and_do_move(selected, target):
    t_i, t_j = target
    game.board.selected_cell = selected
    if game.board.validate_move(t_i, t_j):
        game.board.do_move(t_i, t_j)
        kek = game.current_turn.value
        game.current_turn = Color.BLACK if kek else Color.WHITE
        return True
    else:
        return False


def proceed_client_message(msg):
    obj = json.loads(msg)
    event = obj['event']
    response = ''
    if event == events.GET_COLOR:
        response = get_color()
    elif event == events.GET_GAME_STATE:
        response = get_game_state()
    elif event == events.DO_MOVE:
        response = handle_move(obj)
        do_broadcast(response)
        pass
    return response


def proceed_client(clientsocket, addr, idx):
    def read_message():
        msg = clientsocket.recv(8192).decode('utf-8')
        print('------>')
        print(msg)
        return msg

    while True:
        msg = read_message()
        response = proceed_client_message(msg)
        print('<------')
        print(response)
        clientsocket.send(response.encode('utf-8'))


def init_socket():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = socket.gethostname()
    sock.bind((host, PORT))
    sock.listen(1)
    print(f'Server started on {host}:{PORT}')
    connected_clients = 0
    while True:
        c, addr = sock.accept()
        connected_sockets.append(c)
        connected_clients += 1
        if connected_clients == 1:
            game.state = ServerState.FIRST_CLIENT_CONNECTED
        elif connected_clients == 2:
            game.state = ServerState.BOTH_CLIENTS_CONNECTED
        else:
            # TODO handle attempt to connect where there are two clients already
            game.state = ServerState.WAITING

        client_thread = Thread(target=proceed_client, args=(c, addr, connected_clients))
        client_thread.start()


if __name__ == "__main__":
    init_socket()
