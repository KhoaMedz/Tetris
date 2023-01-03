from game_settings import *
from block import *

class Tetromino():
    def __init__(self, tetris):
        self.tetris = tetris
        self.create_tetromino(self.tetris.is_first_tetromino)
        self.landing = False


    def create_tetromino(self, is_first_tetromino):
        if is_first_tetromino == True:
            self.core_pos = vector(INITIAL_TETROMINO_POS) # Tọa độ gốc
        else:
            self.core_pos = vector(NEXT_TETROMINO_POS)
        self.tetromino_name = random.choice(list(TETROMINOS.keys()))
        self.tetromino_rotation = random.randint(0, len(TETROMINOS[self.tetromino_name]) - 1)
        tetromino_shape = TETROMINOS[self.tetromino_name][self.tetromino_rotation]
        blocks_pos = []
        for x in range(SHAPE_TEMPLATE_COLS):
            for y in range(SHAPE_TEMPLATE_ROWS):
                if tetromino_shape[y][x] == 'o':
                    blocks_pos.append(vector(x, y) + self.core_pos)
        self.blocks = [Block(self, pos) for pos in blocks_pos]


    def move(self, direction):
        move_direction = MOVE_DIRECTIONS[direction]
        new_tetromino_pos = [block.block_pos + move_direction for block in self.blocks]
        is_collide = self.is_collide(new_tetromino_pos)

        if not is_collide:
            for block in self.blocks:
                block.block_pos += move_direction
            self.core_pos += move_direction # Sau khi di chuyển khối tetromino thì cập nhật lại tọa độ gốc
        elif direction == 'down':
            self.landing = True    
         
        
    def is_collide(self, tetromino_pos):
        for pos in tetromino_pos:
            if Block.is_collide(self.blocks[0], pos):
                return True
        return False
    
    def rotate(self):
        self.tetromino_rotation = (self.tetromino_rotation + 1) % len(TETROMINOS[self.tetromino_name])
        tetromino_shape = TETROMINOS[self.tetromino_name][self.tetromino_rotation]
        list_new_pos = []
        for x in range(SHAPE_TEMPLATE_COLS):
            for y in range(SHAPE_TEMPLATE_ROWS):
                if tetromino_shape[y][x] == 'o':
                    list_new_pos.append(vector(x, y) + self.core_pos)
        if not self.is_collide(list_new_pos):
            for i in range(len(self.blocks)):
                self.blocks[i].set_block_pos(list_new_pos[i])
        

    def update(self):
        if time.time() - self.tetris.last_fall_down_time > self.tetris.fall_frequency:
            self.move('down')
            self.tetris.last_fall_down_time = time.time()


    def draw_piece(self, surface, block_size, core_pos_X = 0, core_pos_Y = 0):
        tetromino_shape = TETROMINOS[self.tetromino_name][self.tetromino_rotation]
        for x in range(5):
                for y in range(5):
                    if  tetromino_shape[y][x] == 'o':
                        coor_to_draw_X = (x + core_pos_X) * block_size
                        coor_to_draw_Y = (y + core_pos_Y) * block_size
                        Block.draw_block(self.blocks[0], surface, coor_to_draw_X, coor_to_draw_Y, block_size)