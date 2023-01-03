from game_settings import *
from tetris import *

class App():
    def __init__(self):
        pg.init()
        self.tetris = Tetris(self)
        self.display_screen = pg.display.set_mode(WINDOW_RES)
        pg.display.set_caption('Tetris')
        self.fps_clock = pg.time.Clock()

    def terminate_program(self):
        pg.quit()
        sys.exit()
   
    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                self.terminate_program()
            elif event.type == pg.KEYDOWN:
                self.tetris.key_down_handle(pressed_key=event.key)
            elif event.type == pg.KEYUP:
                self.tetris.key_up_handle(release_key=event.key)


    def update(self):
        self.tetris.update()

    def draw(self):
        self.tetris.draw()
        self.display_screen.blit(self.tetris.tetris_surface, TETRIS_SURFACE_POS)
        pg.display.flip()
        self.fps_clock.tick(FPS)

    def run(self):
        while 1:
            self.check_events()
            self.update()
            self.draw()

