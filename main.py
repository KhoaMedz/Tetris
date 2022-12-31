import pygame, sys, time, random, queue
import Draw, Shapes, Piece, Board
from pygame.locals import *

pygame.init()

# Thiết lập kích thước
WINDOW_WIDTH = 1600
WINDOW_HEIGHT = 900
WINDOW_RES = WINDOW_WIDTH, WINDOW_HEIGHT
BLOCK_SIZE = 42
PIECE_QUEUE_BLOCK_SIZE = 15
BOARD_COLS = 10
BOARD_ROWS = 20
BOARD_WIDTH = BOARD_COLS * BLOCK_SIZE
BOARD_HEIGHT = BOARD_ROWS * BLOCK_SIZE
BOARD_RES = BOARD_WIDTH, BOARD_HEIGHT
PIECE_QUEUE_COLS = 7
PIECE_QUEUE_ROWS = 27
PIECE_QUEUE_WIDTH = PIECE_QUEUE_COLS * PIECE_QUEUE_BLOCK_SIZE
PIECE_QUEUE_HEIGHT = PIECE_QUEUE_ROWS * PIECE_QUEUE_BLOCK_SIZE
PIECE_QUEUE_RES = PIECE_QUEUE_WIDTH, PIECE_QUEUE_HEIGHT
TEMP_WIDTH = 5
TEMP_HEIGHT = 5

# Thiết lập vị trí để vẽ các surface phụ lên surface chính
COOR_TO_DRAW_BOARD_SURFACE_X = (WINDOW_WIDTH - BOARD_WIDTH) // 2
COOR_TO_DRAW_BOARD_SURFACE_Y = (WINDOW_HEIGHT - BOARD_HEIGHT) // 2
COOR_TO_DRAW_PIECE_QUEUE_SURFACE_X = ((WINDOW_WIDTH - BOARD_WIDTH) // 2) + BOARD_WIDTH + 20
COOR_TO_DRAW_PIECE_QUEUE_SURFACE_Y = (WINDOW_HEIGHT - BOARD_HEIGHT) // 2

# Thiết lập màu sắc
WHITE = (255,255,255)
BROWN = (39, 22, 0)
LIGHT_BROWN = (198, 168, 129)
GREY = (105, 105, 105)

# Shapes
shapes = Shapes.Shapes().get_shapes()

# FPS và time
FPS = 30
fps_clock = pygame.time.Clock()


def main():
    # Khởi tạo các surface
    display_surface = pygame.display.set_mode(WINDOW_RES)
    board_surface = pygame.Surface(BOARD_RES)
    piece_queue_surface = pygame.Surface(PIECE_QUEUE_RES)
    pygame.display.set_caption('Tetris')
    rects = [pygame.Rect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE) for x in range(BOARD_COLS) for y in range(BOARD_ROWS)]
    
    # Time
    last_fall_down_time = time.time()
    last_move_sideways_time = time.time()
    last_move_down_time =time.time()
    fall_frequency = 1
    move_sideways_frequency = 0.05
    move_down_frequency = 0.07
    
    # Move
    moving_left = False
    moving_right = False
    moving_down = False

    # Tạo board để lưu giá trị các block
    board = Board.Board(BOARD_COLS, BOARD_ROWS)

    #Tạo khối
    piece_queue = queue.Queue(maxsize=5) # Piece queue gồm 5 khối
    
    for i in range(piece_queue.maxsize):
        piece_queue.put(Piece.Piece())

    
    piece = Piece.Piece()

    # Main loop
    while True:
        if piece == None:
            piece = piece_queue.get()
            piece_queue.put(Piece.Piece())
            last_fall_down_time = time.time()

        # Xử lý sự kiện
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()    
                sys.exit()
            # Xử lý KEYUP
            elif event.type == KEYUP:
                if event.key == K_LEFT:
                    moving_left = False
                elif event.key == K_RIGHT:
                    moving_right = False
                elif event.key == K_DOWN:
                    moving_down = False
            # Xử lý KEYDOWN
            elif event.type == KEYDOWN:
                if event.key == K_LEFT and piece.is_valid_position(board, adjacent_X = -1):
                    moving_left = True
                    moving_right = False
                    piece.piece['piece_x'] -= 1
                    last_move_sideways_time = time.time()
                elif event.key == K_RIGHT and piece.is_valid_position(board, adjacent_X = 1):
                    moving_right = True
                    moving_left = False
                    piece.piece['piece_x'] += 1
                    last_move_sideways_time = time.time()
                elif event.key == K_DOWN and piece.is_valid_position(board, adjacent_Y = 1):
                    moving_down = True
                    piece.piece['piece_y'] += 1
                    last_move_down_time = time.time()
                # Xoay theo chiều kim đồng hồ khi nhấn z
                elif event.key == K_z:
                    piece.piece['piece_rotation'] = (piece.piece['piece_rotation'] + 1) % len(shapes[piece.piece['piece_shape_name']][0])
                    if not piece.is_valid_position(board):
                        piece.piece['piece_rotation'] = (piece.piece['piece_rotation'] - 1) % len(shapes[piece.piece['piece_shape_name']][0])
                # Xoay ngược chiều kim đòng hồ khi nhấn x
                elif event.key == K_x:
                    piece.piece['piece_rotation'] = (piece.piece['piece_rotation'] - 1) % len(shapes[piece.piece['piece_shape_name']][0])
                    if not piece.is_valid_position(board):
                        piece.piece['piece_rotation'] = (piece.piece['piece_rotation'] + 1) % len(shapes[piece.piece['piece_shape_name']][0])    
                # elif event.key == K_SPACE:
                #     piece.piece['piece_y'] += BOARD_ROWS - 4

            
        # Xử lý giữ phím
        if moving_left and time.time() - last_move_sideways_time > move_sideways_frequency and piece.is_valid_position(board, adjacent_X=-1):
            piece.piece['piece_x'] -= 1
            last_move_sideways_time = time.time()
        if moving_right and time.time() - last_move_sideways_time > move_sideways_frequency and piece.is_valid_position(board, adjacent_X=1):
            piece.piece['piece_x'] += 1
            last_move_sideways_time = time.time()
        if moving_down and time.time() - last_move_down_time > move_down_frequency and piece.is_valid_position(board, adjacent_Y=1):
            piece.piece['piece_y'] += 1
            last_move_down_time = time.time()
        
        # Landed
        if time.time() - last_fall_down_time > fall_frequency:
            if not piece.is_valid_position(board, adjacent_Y=1):
                board.add_to_board(piece)
                board.remove_completed_lines()
                piece = None
            else:
                piece.piece['piece_y'] += 1
                last_fall_down_time = time.time()
        # Vẽ lên surface
        board_surface.fill(BROWN)
        [pygame.draw.rect(board_surface, GREY, i, 1) for i in rects]
        Draw.Draw().draw_board(board_surface, board, BLOCK_SIZE)
        if piece != None:
            Draw.Draw().draw_piece(board_surface, piece, BLOCK_SIZE)

        piece_queue_surface.fill(LIGHT_BROWN)
        piece_queue_y = 1
        for element in piece_queue.queue:
            Draw.Draw().draw_piece(piece_queue_surface, element, PIECE_QUEUE_BLOCK_SIZE, True, 1, piece_queue_y)
            piece_queue_y += 5
        
        
        display_surface.blit( board_surface, ( COOR_TO_DRAW_BOARD_SURFACE_X, COOR_TO_DRAW_BOARD_SURFACE_Y ) )
        display_surface.blit( piece_queue_surface, ( COOR_TO_DRAW_PIECE_QUEUE_SURFACE_X, COOR_TO_DRAW_PIECE_QUEUE_SURFACE_Y ) )
        # Cập nhật lên màn hình           
        pygame.display.update()
        fps_clock.tick(FPS)


   
   
if __name__ == '__main__':
    main()


