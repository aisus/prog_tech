import json

import socketio

import ui
import socket_events as events
import logging

import threading

logger = logging.getLogger("Main")
logging.basicConfig(
    level=logging.INFO
)
sio = socketio.client.Client()


def do_move(selected, target):
    result = {
        "selected": selected,
        "target": target
    }
    response = json.dumps(result, sort_keys=True, indent=3)
    sio.emit(events.DO_MOVE, response)


def ui_closed():
    sio.disconnect()
    quit(0)


@sio.on(events.SET_COLOR)
def __set_color(data):
    obj = json.loads(data)
    color = obj["color"]
    ui.set_color(color)


@sio.on(events.SET_GAME_STATE)
def __set_game_state(data):
    obj = json.loads(data)
    board = obj['board']
    ui.set_board(board)


def kek(thread: threading.Thread):
    while True:
        if not thread.is_alive():
            ui_closed()


if __name__ == '__main__':
    logger.info("Started")
    ui_thread = ui.UiThread()
    threading.Thread.start(ui_thread)

    sio.connect('http://localhost:5000')
    sio.emit(events.GET_COLOR)
    sio.emit(events.GET_GAME_STATE)

    result = {
        "selected": [7, 1],
        "target": [6, 1]
    }
    response = json.dumps(result, sort_keys=True, indent=3)
    sio.emit(events.DO_MOVE, response)
    sio.emit(events.GET_GAME_STATE)