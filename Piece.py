import random, Board, Shapes

class Piece():
    def __init__(self):
        shapes = Shapes.Shapes().get_shapes()
        shape_name = str(random.choice(list(shapes.keys())))
        self.piece = {'piece_shape_name': shape_name,
                      'piece_x': 3,
                      'piece_y': 0,
                      'piece_picture': shapes[shape_name][1],
                      'piece_rotation': random.randint(0, len(shapes[shape_name][0]) - 1)}
    
    def get_piece(self):
        return self.piece

    def is_valid_position(self, board, adjacent_X = 0, adjacent_Y = 0):
        shapes = Shapes.Shapes().get_shapes()
        piece_shape = shapes[self.piece['piece_shape_name']][0][self.piece['piece_rotation']]
        for x in range(5):
            for y in range(5):
                is_above_board = self.piece['piece_y'] + y + adjacent_Y < 0
                if is_above_board or piece_shape[y][x] == '.':
                    continue
                if not board.is_on_board(self.piece['piece_x'] + x + adjacent_X, self.piece['piece_y'] + y + adjacent_Y):
                    return False
                if board.board_value[self.piece['piece_x'] + x + adjacent_X][self.piece['piece_y'] + y + adjacent_Y] != '.':
                    return False
        return True
                