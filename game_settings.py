import pygame as pg
import sys, random, time, queue, pathlib, os
vector = pg.math.Vector2

# Thiết lập kích thước
WINDOW_RES = WINDOW_WIDTH, WINDOW_HEIGHT = 1920, 1080 # 1600, 900
BLOCK_SIZE = 50
BLOCK_SIZE_FUTURE_SHADOW = 48
TETROMINO_QUEUE_BLOCK_SIZE = 15
TETRIS_COLS = 10
TETRIS_ROWS = 20
TETRIS_RES = TETRIS_WIDTH, TETRIS_HEIGHT = TETRIS_COLS * BLOCK_SIZE, TETRIS_ROWS * BLOCK_SIZE

TETROMINO_QUEUE_COLS = 7
TETROMINO_QUEUE_ROWS = 27
TETROMINO_QUEUE_RES = TETROMINO_QUEUE_WIDTH, TETROMINO_QUEUE_HEIGHT = TETROMINO_QUEUE_COLS * TETROMINO_QUEUE_BLOCK_SIZE, TETROMINO_QUEUE_ROWS * TETROMINO_QUEUE_BLOCK_SIZE

# Thiết lập vị trí để vẽ các surface phụ lên surface chính
TETRIS_SURFACE_POS = vector((WINDOW_WIDTH - TETRIS_WIDTH) // 2, (WINDOW_HEIGHT - TETRIS_HEIGHT) // 2)
TETROMINO_QUEUE_SURFACE_POS = vector(((WINDOW_WIDTH - TETRIS_WIDTH) // 2) + TETRIS_WIDTH + 50, (WINDOW_HEIGHT - TETRIS_HEIGHT) // 2)
DRAW_NEXT_LEVEL_POS = vector(((WINDOW_WIDTH - TETRIS_WIDTH) // 2) + TETRIS_WIDTH + 40, ((WINDOW_HEIGHT - TETRIS_HEIGHT) // 2) + TETRIS_HEIGHT - 175)
DRAW_SCORE_POS = vector(((WINDOW_WIDTH - TETRIS_WIDTH) // 2) + TETRIS_WIDTH + 40, ((WINDOW_HEIGHT - TETRIS_HEIGHT) // 2) + TETRIS_HEIGHT - 175 - 175 - 50)
DRAW_SPEED_POS = vector(((WINDOW_WIDTH - TETRIS_WIDTH) // 2) - 215, ((WINDOW_HEIGHT - TETRIS_HEIGHT) // 2) + TETRIS_HEIGHT - 175)
DRAW_LEVEL_POS = vector(((WINDOW_WIDTH - TETRIS_WIDTH) // 2) - 215, ((WINDOW_HEIGHT - TETRIS_HEIGHT) // 2) + TETRIS_HEIGHT - 175 - 175 - 50)
DRAW_TETRIS_BORDER_POS = TETRIS_SURFACE_POS + (-19, -87)
TETROMINO_CURRENT_HOLD_SURFACE_POS = vector(((WINDOW_WIDTH - TETRIS_WIDTH) // 2) - 250 - 50, ((WINDOW_HEIGHT - TETRIS_HEIGHT) // 2) + 90)
LOGO_SURFACE_POS = vector(1530,50)

# Thiết lập màu sắc
WHITE = (255,255,255)
BROWN = (39, 22, 0)
LIGHT_BROWN = (198, 168, 129)
GREY = (105, 105, 105)
DARK_ORANGE = (255, 140, 0)
LIGHT_GREEN = (158,255,54)
# Time and FPS
ORIGINAL_FALL_FREQUENCY = 1
MOVE_SIDEAWAYS_FREQUENCY = 0.05
MOVE_DOWN_FREQUENCY = 0.07
FPS = 30

# Tọa độ của tetromino
INITIAL_TETROMINO_POS = vector(3, 0) # Tọa độ ban đầu khi bắt đầu game
NEXT_TETROMINO_POS = vector(3, -4) # Tọa độ sinh khối tetromino tiếp theo

# Font size
FONT_SIZE_SCORE = 50
FONT_SIZE_LOGO = 50
# Lấy thư mục hiện tại đang chứa file này
SOURCES_FILE_DIRECTORY = os.path.dirname(os.path.abspath(__file__))

# Hướng di chuyển
MOVE_DIRECTIONS = {'left': vector(-1, 0),
             'right': vector(1, 0),
             'down': vector(0, 1)}

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

DOT_TEMP = [['.....',
             '.....',
             '..o..',
             '.....',
             '.....']]


SMALL_L_TEMP = [['.....',
                 '..o..',
                 '.oo..',
                 '.....',
                 '.....'],

                ['.....',
                 '..o..',
                 '..oo.',
                 '.....',
                 '.....'],
   
                ['.....',
                 '.....',
                 '..oo.',
                 '..o..',
                 '.....'],
   
                ['.....',
                 '.....',
                 '.oo..',
                 '..o..',
                 '.....']]


SMALL_I_TEMP = [['.....',
                 '..o..',
                 '..o..',
                 '.....',
                 '.....'],   

                ['.....',
                 '.....',
                 '.oo..',
                 '.....',
                 '.....']]


CROSS_TEMP = [['.....',
               '.o...',
               '..o..',
               '.....',
               '.....'],

              ['.....',
               '...o.',
               '..o..',
               '.....',
               '.....']]


PLUS_TEMP = [['.....',
              '..o..',
              '.ooo.',
              '..o..',
              '.....']]


V_TEMP =  [['.....',
            '.o.o.',
            '..o..',
            '.....',
            '.....'],

           ['.....',
            '...o.',
            '..o..',
            '...o.',
            '.....'],
   
           ['.....',
            '.....',
            '..o..',
            '.o.o.',
            '.....'],
   
           ['.....',
            '.o...',
            '..o..',
            '.o...',
            '.....']]


BOAT_TEMP =  [['.....',
               '.o.o.',
               '.ooo.',
               '.....',
               '.....'],
   
              ['.....',
               '..oo.',
               '..o..',
               '..oo.',
               '.....'],
      
              ['.....',
               '.....',
               '.ooo.',
               '.o.o.',
               '.....'],
      
              ['.....',
               '.oo..',
               '..o..',
               '.oo..',
               '.....']]


#Classic mode ------------------------------------------------------------------------------------
TETROMINOS_CLASSIC = {'I': I_TEMP,
                      'L': L_TEMP,
                      'J': J_TEMP,
                      'S': S_TEMP,
                      'Z': Z_TEMP,
                      'T': T_TEMP,
                      'O': O_TEMP}


# Số hiệu ảnh theo hình khối tetromino
TETROMINOS_IMAGE_NUMBER_CLASSIC = {'I': 0,
                                   'L': 1,
                                   'J': 2,
                                   'S': 3,
                                   'Z': 4,
                                   'T': 5,
                                   'O': 6}

#Modern mode ------------------------------------------------------------------------------------
TETROMINOS_MODERN = {'I': I_TEMP,
                      'L': L_TEMP,
                      'J': J_TEMP,
                      'S': S_TEMP,
                      'Z': Z_TEMP,
                      'T': T_TEMP,
                      'O': O_TEMP,
                      'DOT': DOT_TEMP,
                      'SMALL_L': SMALL_L_TEMP,
                      'SMALL_I': SMALL_I_TEMP,
                      'CROSS': CROSS_TEMP,
                      'PLUS': PLUS_TEMP,
                      'V': V_TEMP,
                      'BOAT': BOAT_TEMP}


# Số hiệu ảnh theo hình khối tetromino
TETROMINOS_IMAGE_NUMBER_MODERN = {'I': 0,
                                   'L': 1,
                                   'J': 2,
                                   'S': 3,
                                   'Z': 4,
                                   'T': 5,
                                   'O': 6,
                                   'DOT': 7,
                                   'SMALL_L': 8,
                                   'SMALL_I': 9,
                                   'CROSS': 10,
                                   'PLUS': 11,
                                   'V': 12,
                                   'BOAT': 13}