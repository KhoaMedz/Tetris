import pygame, sys, time, Shapes
from pygame.locals import *
WHITE = (255,255,255)

class Draw():
    def __init__(self):
         pass
        
    
    def draw_block(self, surface, board_x, board_y, block_size):
        pygame.draw.rect(surface, WHITE, ( board_x , board_y, block_size - 1, block_size - 1))

   
    def draw_piece(self, surface, piece, block_size, custom_coor = False, coordinate_X = 0, coordinate_Y = 0):
        shapes = Shapes.Shapes().get_shapes()
        shape_to_draw = shapes[piece.piece['piece_shape_name']][0][piece.piece['piece_rotation']]
        coor_to_draw_X = piece.piece['piece_x']
        coor_to_draw_Y = piece.piece['piece_y']

        if custom_coor == True:
            coor_to_draw_X = coordinate_X
            coor_to_draw_Y = coordinate_Y

        for x in range(5):
                for y in range(5):
                    if  shape_to_draw[y][x] == 'o':
                        board_x = x * block_size + coor_to_draw_X * block_size
                        board_y = y * block_size + coor_to_draw_Y * block_size
                        self.draw_block(surface, board_x, board_y, block_size)

   
    def draw_board(self, surface, board, block_size):
        for x in range(board.board_cols):
            for y in range(board.board_rows):
                if board.board_value[x][y] != '.':
                    board_x = x * block_size
                    board_y = y * block_size
                    self.draw_block(surface, board_x, board_y, block_size)