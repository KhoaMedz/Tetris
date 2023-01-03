import pygame as pg
import sys, random, time, queue
vector = pg.math.Vector2

# Thiết lập kích thước
WINDOW_RES = WINDOW_WIDTH, WINDOW_HEIGHT = 1600, 900
BLOCK_SIZE = 42
TETROMINO_QUEUE_BLOCK_SIZE = 15
TETRIS_COLS = 10
TETRIS_ROWS = 20
TETRIS_RES = TETRIS_WIDTH, TETRIS_HEIGHT = TETRIS_COLS * BLOCK_SIZE, TETRIS_ROWS * BLOCK_SIZE

TETROMINO_QUEUE_COLS = 7
TETROMINO_QUEUE_ROWS = 27
TETROMINO_QUEUE_RES = TETROMINO_QUEUE_WIDTH, TETROMINO_QUEUE_HEIGHT = TETROMINO_QUEUE_COLS * TETROMINO_QUEUE_BLOCK_SIZE, TETROMINO_QUEUE_ROWS * TETROMINO_QUEUE_BLOCK_SIZE

# Thiết lập vị trí để vẽ các surface phụ lên surface chính
TETRIS_SURFACE_POS = (WINDOW_WIDTH - TETRIS_WIDTH) // 2, (WINDOW_HEIGHT - TETRIS_HEIGHT) // 2
TETROMINO_QUEUE_SURFACE_POS = ((WINDOW_WIDTH - TETRIS_WIDTH) // 2) + TETRIS_WIDTH + 20, (WINDOW_HEIGHT - TETRIS_HEIGHT) // 2
DRAW_SCORE_POS = ((WINDOW_WIDTH - TETRIS_WIDTH) // 2) + TETRIS_WIDTH + 20, ((WINDOW_HEIGHT - TETRIS_HEIGHT) // 2) + TETROMINO_QUEUE_HEIGHT + 20

# Thiết lập màu sắc
WHITE = (255,255,255)
BROWN = (39, 22, 0)
LIGHT_BROWN = (198, 168, 129)
GREY = (105, 105, 105)

# Time and FPS
ORIGINAL_FALL_FREQUENCY = 1
MOVE_SIDEAWAYS_FREQUENCY = 0.05
MOVE_DOWN_FREQUENCY = 0.07
FPS = 30

# Tọa độ của tetromino
INITIAL_TETROMINO_POS = vector(3, 0) # Tọa độ ban đầu khi bắt đầu game
NEXT_TETROMINO_POS = vector(3, -4) # Tọa độ sinh khối tetromino tiếp theo

# Score font size
FONT_SIZE_SCORE = 50


# Tetromino's Shape
SHAPE_TEMPLATE_COLS = 5
SHAPE_TEMPLATE_ROWS = 5
I_TEMP = [['..o..',
           '..o..',
           '..o..',
           '..o..',
           '.....'],   

          ['.....',
           '.....',
           'oooo.',
           '.....',
           '.....']]

L_TEMP = [['.....',
           '..o..',
           '..o..',
           '..oo.',
           '.....'],    

          ['.....',
           '.....',
           '.ooo.',
           '.o...',
           '.....'],  

          ['.....',
           '.oo..',
           '..o..',
           '..o..',
           '.....'],  

          ['.....',
           '...o.',
           '.ooo.',
           '.....',
           '.....']]

J_TEMP = [['.....',
           '..o..',
           '..o..',
           '.oo..',
           '.....'],  

          ['.....',
           '.o...',
           '.ooo.',
           '.....',
           '.....'],  

          ['.....',
           '..oo.',
           '..o..',
           '..o..',
           '.....'], 

           ['.....',
            '.....',
            '.ooo.',
            '...o.',
            '.....']]

S_TEMP = [['.....',
           '.....',
           '..oo.',
           '.oo..',
           '.....'], 

           ['.....',
           '.o...',
           '.oo..',
           '..o..',
           '.....']]

Z_TEMP = [['.....',
           '.....',
           '.oo..',
           '..oo.',
           '.....'], 

          ['.....',
           '...o.',
           '..oo.',
           '..o..',
           '.....']]

T_TEMP = [['.....',
           '..o..',
           '.ooo.',
           '.....',
           '.....'],

          ['.....',
           '..o..',
           '..oo.',
           '..o..',
           '.....'],

          ['.....',
           '.....',
           '.ooo.',
           '..o..',
           '.....'],

           ['.....',
           '..o..',
           '.oo..',
           '..o..',
           '.....']]

O_TEMP = [['.....',
           '.....',
           '..oo.',
           '..oo.',
           '.....']]


TETROMINOS = {'I': I_TEMP,
              'L': L_TEMP,
              'J': J_TEMP,
              'S': S_TEMP,
              'Z': Z_TEMP,
              'T': T_TEMP,
              'O': O_TEMP}


# Hướng di chuyển
MOVE_DIRECTIONS = {'left': vector(-1, 0),
             'right': vector(1, 0),
             'down': vector(0, 1)}