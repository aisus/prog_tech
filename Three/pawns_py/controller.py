import json

from socketIO_client import SocketIO

import ui
import logging
logger = logging.getLogger("Main")
logging.basicConfig(
    level=logging.INFO
)
sio = SocketIO('http://localhost:5000')


def do_move(selected, target):
    pass


def __set_color(data):
    obj = json.loads(data)
    color = obj["color"]
    print(f"color : {color}")


def __set_game_state(data):
    # print(f"data : {data}")
    obj = json.loads(data)
    board = obj['board']
    # print(board)
    ui.redraw(board)


if __name__ == '__main__':
    logger.info("Started")
    ui_thread = ui.UiThread()
    ui_thread.start()

    sio.connect('http://localhost:5000')
    sio.on('set_color', __set_color)
    sio.on('set_game_state', __set_game_state)
    sio.emit('get_color')
    sio.emit('get_game_state')
    sio.wait(1)
