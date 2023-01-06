from game_settings import *

class Block(pg.sprite.Sprite):
    def __init__(self, tetromino, block_pos):
        self.tetromino = tetromino
        super().__init__(self.tetromino.tetris.sprites_group)
        self.block_pos = vector(block_pos)
        self.image = tetromino.image
        self.rect = self.image.get_rect()
        self.rect.topleft = self.block_pos * BLOCK_SIZE
        self.alive = True
        self.create_block_sfx()


    def create_block_sfx(self):
        img_index = random.randint(0, 16)
        image_path = os.path.join(SOURCES_FILE_DIRECTORY, f'images/effect/star_{img_index}.png')
        self.sfx_image = pg.image.load(image_path).convert_alpha()
        # self.sfx_image.set_alpha(160)
        self.sfx_speed = random.uniform(0.1, 0.8)
        self.sfx_cycles = random.randrange(6, 12)
        self.cycle_counter = 0


    def sfx_end_time(self):
        if self.tetromino.tetris.app.effect_trigger:
            self.cycle_counter += 1
            if self.cycle_counter > self.sfx_cycles:
                self.cycle_counter = 0
                return True


    def sfx_run(self):
        self.image = self.sfx_image
        self.block_pos.y -= self.sfx_speed
        self.image = pg.transform.rotate(self.image, pg.time.get_ticks() * self.sfx_speed)


    def is_alive(self):
            if not self.alive:
                if not self.sfx_end_time():
                    self.sfx_run()
                else:
                    self.kill()


    def set_rect_topleft(self):
        self.rect.topleft = self.block_pos * BLOCK_SIZE

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
