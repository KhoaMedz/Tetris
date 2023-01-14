from game_settings import *

class Dust(pg.sprite.Sprite):
    def __init__(self, tetris, dirt_tetromino_center_pos):
        self.tetris = tetris
        super().__init__(self.tetris.dirt_group)
        self.current_sprite = 1
        self.image = self.tetris.load_image(f'assets/images/effect/dirt_landed_effect/frame ({self.current_sprite}).png', 100, 100)
        self.rect = self.image.get_rect()
        self.rect.midbottom = dirt_tetromino_center_pos + (BLOCK_SIZE // 2, BLOCK_SIZE)


    def update(self):
        self.image = self.tetris.load_image(f'assets/images/effect/dirt_landed_effect/frame ({int(self.current_sprite)}).png', 100, 100)
        self.current_sprite += 0.5
        if self.current_sprite >= 5:
            self.kill()
