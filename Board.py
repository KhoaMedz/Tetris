import Shapes

class Board():
    def __init__(self, board_cols = 0, board_rows = 0):
        self.board_cols = board_cols
        self.board_rows = board_rows
        self.board_value = [['.'] * self.board_rows for x in range(self.board_cols)]

    def make_board_empty(self):
        for x in range(self.board_cols):
            for y in range(self.board_rows):
                self.board_value[x][y] = '.'

    def print_board_value(self):
        for x in range(self.board_rows):
            for y in range(self.board_cols):
                print(self.board_value[y][x], end = ' ')
            print()
        
    def is_on_board(self, coordinate_X, coordinate_Y):
        return coordinate_X >= 0 and coordinate_X < self.board_cols and coordinate_Y < self.board_rows

    def add_to_board(self, piece):
        shapes = Shapes.Shapes().get_shapes()
        piece_shape = shapes[piece.piece['piece_shape_name']][0][piece.piece['piece_rotation']]
        for x in range(5):
            for y in range(5):
                if piece_shape[y][x] != '.':
                    self.board_value[piece.piece['piece_x'] + x][piece.piece['piece_y'] + y] = piece.piece['piece_picture']

    def is_completed_line(self, line):
        for x in range(self.board_cols):
            if self.board_value[x][line] == '.':
                return False
        return True

    def remove_completed_lines(self):
        k = self.board_rows - 1
        while k >= 0:
            if self.is_completed_line(k):
                for y in range(k, 0, -1):
                    for x in range(self.board_cols):
                        self.board_value[x][y] = self.board_value[x][y - 1]
                    
                for x in range(self.board_cols):
                    self.board_value[x][0] = '.'
            else:
                k -= 1