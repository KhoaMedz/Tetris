from game_settings import *

class Sparkle(pg.sprite.Sprite):
    def __init__(self, tetris):
        self.tetris = tetris
        super().__init__(self.tetris.sparkle_group)
        self.current_sprite = 1
        self.counter = 0
        self.image = self.tetris.load_image(f'assets/images/effect/four_line_clear_effect/frame ({self.current_sprite}).png', 500, 1020)
        self.rect = self.image.get_rect()
        self.rect.topleft = 0, 0


    def update(self):
        self.image = self.tetris.load_image(f'assets/images/effect/four_line_clear_effect/frame ({self.current_sprite}).png', 500, 1020)
        self.current_sprite += 1
        if self.current_sprite >= 26:
            self.current_sprite = 1
            self.counter += 1
        if self.counter == 2:
            self.kill()
