from game_settings import *

class Drop_Light(pg.sprite.Sprite):
    def __init__(self, tetris, tetromino_center_pos):
        self.tetris = tetris
        super().__init__(self.tetris.drop_light_group)
        self.current_sprite = 1
        self.image = self.tetris.load_image(f'assets/images/effect/drop_light_effect/frame ({self.current_sprite}).png', 150, 556)
        self.rect = self.image.get_rect()
        self.rect.midbottom = tetromino_center_pos + (BLOCK_SIZE // 2, 0)


    def update(self):
        self.image = self.tetris.load_image(f'assets/images/effect/drop_light_effect/frame ({int(self.current_sprite)}).png', 150, 556)
        self.current_sprite += 0.8
        if self.current_sprite >= 8:
            self.kill()
