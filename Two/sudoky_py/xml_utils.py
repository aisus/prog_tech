from game_state import GameState
from lxml import etree, objectify
from os import path


def load_game_state(uri, expected_size, expected_values):
    def create_default():
        print('Creating empty board')
        return GameState.empty()

    if not path.isfile(uri):
        print('Can\'t load {} !'.format(uri))
        return create_default()

    try:
        with open(uri) as f:
            xml = f.read()
        parser = etree.XMLParser(ns_clean=True, recover=True, encoding='utf-8')
        root = objectify.fromstring(xml, parser)
    except Exception:
        print('Xml file is invalid!')
        return create_default()

    rows = root.getchildren()[0]
    if len(rows) != expected_size:
        print('Incorrect number of rows!')
        return create_default()

    cells = [[]]
    for i in range(expected_size):
        row = rows[i].text.split()
        if len(row) != expected_size:
            print('Incorrect number of elements in a row!')
            return create_default()
        cells.append([])
        for ch in row:
            if ch not in expected_values:
                print('Incorrect element {}!'.format(ch))
                return create_default()
            cells[i].append(int(ch))

    cells.remove(cells[-1])
    print('Xml parse successful')
    return GameState.from_array(cells)


def save_game_state(path, game_state):
    def create_board_structure(grid):
        board = objectify.Element('board')
        grid = game_state.grid
        lines = []
        for i in range(len(grid)):
            lines.append('')
            for j in range(len(grid[i])):
                lines[i] += ('{} '.format(grid[i][j]))

        board.row = lines
        return board

    parser = etree.XMLParser(ns_clean=True, recover=True, encoding='utf-8')
    xml = '''<data></data>'''
    root = objectify.fromstring(xml, parser=parser)
    board = create_board_structure(game_state.grid)
    root.append(board)

    objectify.deannotate(root)
    etree.cleanup_namespaces(root)

    obj_xml = etree.tostring(root,
                             pretty_print=True,
                             xml_declaration=False
                             )

    try:
        with open(path, "wb") as xml_writer:
            xml_writer.write(obj_xml)
    except IOError:
        pass

    print('Saved!')
