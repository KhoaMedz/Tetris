from game_settings import *

class Block(pg.sprite.Sprite):
    def __init__(self, tetromino, block_pos):
        self.tetromino = tetromino
        super().__init__(self.tetromino.tetris.sprites_group)
        self.block_pos = vector(block_pos)
        # self.image = pg.Surface((BLOCK_SIZE - 2, BLOCK_SIZE - 2))
        # self.image.fill(WHITE)
        self.image = tetromino.image
        self.rect = self.image.get_rect()
        self.rect.topleft = self.block_pos * BLOCK_SIZE + (1, 1)
        self.alive = True
    
    def is_alive(self):
        if not self.alive:
            self.kill()

    def set_rect_topleft(self):
        self.rect.topleft = self.block_pos * BLOCK_SIZE + (1, 1)

    def set_block_pos(self, block_pos):
        self.block_pos = block_pos

    def is_collide(self, checking_pos):
        x, y = int(checking_pos.x), int(checking_pos.y)
        is_above = y < 0
        if 0 <= x < TETRIS_COLS and y < TETRIS_ROWS and (is_above or not self.tetromino.tetris.tetris_matrix[x][y]):
            return False
        return True

    def update(self):
        self.set_rect_topleft()
        self.is_alive()

    def draw_block(self, surface, coordinate_X, coordinate_Y, block_size):
        pg.draw.rect(surface, WHITE, (coordinate_X, coordinate_Y, block_size, block_size))
