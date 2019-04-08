from game_state import GameState
from xml.etree import ElementTree
from os import path


def load_game_state(uri, expected_size):
    def create_default():
        print('Creating empty board')
        return GameState.empty()

    if not path.isfile(uri):
        print('Can\'t load {} !'.format(uri))
        return create_default()

    doc = ElementTree.parse(uri)
    root = doc.find('board')
    print(root)

    rows = doc.findall('row')
    print(rows)

    nodes = root.childNodes
    for node in nodes:
        if node.nodeType == node.TEXT_NODE:
            print(node.data)

    if len(root.childNodes) != expected_size:
        print('Board isn\'t had a length of {}'.format(expected_size))
        return create_default()


def save_game_state(path, game_state):
    pass
