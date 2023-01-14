from game_settings import *

class Big_Bomb_Explosion(pg.sprite.Sprite):
    def __init__(self, tetris, big_bomb_tetromino_center_pos):
        self.tetris = tetris
        super().__init__(self.tetris.big_bomb_group)
        self.current_sprite = 1
        self.image = self.tetris.load_image(f'assets/images/effect/big_bomb_explosion_effect/frame ({self.current_sprite}).png', 400, 400)
        self.rect = self.image.get_rect()
        self.rect.center = big_bomb_tetromino_center_pos + (BLOCK_SIZE // 2, BLOCK_SIZE // 2)


    def update(self):
        self.image = self.tetris.load_image(f'assets/images/effect/big_bomb_explosion_effect/frame ({int(self.current_sprite)}).png', 400, 400)
        self.current_sprite += 1
        if self.current_sprite >= 83:
            self.kill()
