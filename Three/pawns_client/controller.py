import json

import ui
import socket_events as events
import socket
import logging

import threading

PORT = 8000
COLOR = ''

logger = logging.getLogger("Main")
logging.basicConfig(
    level=logging.INFO
)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
sock.connect((host, PORT))


def ui_closed():
    quit(0)


def __set_color(obj):
    color = obj["color"]
    ui.set_color(color)


def __set_game_state(obj):
    board = obj['board']
    ui.set_board(board)


def do_move(selected, target):
    result = {
        "event": events.DO_MOVE,
        "color": ui.get_color(),
        "selected": selected,
        "target": target
    }
    response = json.dumps(result, sort_keys=True, indent=3)
    sock.send(response.encode('utf-8'))


def get_color():
    response = {
        "event": events.GET_COLOR
    }
    msg = json.dumps(response, sort_keys=True, indent=3)
    sock.send(msg.encode('utf-8'))


def get_game_state():
    response = {
        "event": events.GET_GAME_STATE
    }
    msg = json.dumps(response, sort_keys=True, indent=3)
    sock.send(msg.encode('utf-8'))


def proceed_server_message():
    msg = sock.recv(8192).decode('utf-8')
    print(msg)
    obj = json.loads(msg)
    event = obj['event']
    if event == events.SET_COLOR:
        __set_color(obj)
    elif event == events.SET_GAME_STATE:
        __set_game_state(obj)
    elif event == events.VALIDATE_MOVE:
        __set_game_state(obj)


if __name__ == '__main__':
    logger.info("Started")
    ui_thread = ui.UiThread()
    threading.Thread.start(ui_thread)

    get_color()
    proceed_server_message()
    get_game_state()

    while True:
        proceed_server_message()

    sock.close()
