from game_settings import *
from tetris import *

class App():
    def __init__(self):
        pg.init()
        self.display_screen = pg.display.set_mode(WINDOW_RES)
        self.tetris = Tetris(self)
        
        pg.display.set_caption('Tetris')
        self.background_image = self.load_image()
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

    
    def load_image(self):
        # Nối tên file với thư mục chứa mã nguồn, để load ảnh ko bị lỗi
        image_path = os.path.join(SOURCES_FILE_DIRECTORY, 'images/background/main_background.png')
        return pg.transform.scale(pg.image.load(image_path), (WINDOW_WIDTH, WINDOW_HEIGHT))


    def draw_main_background(self):
        self.display_screen.blit(self.background_image, (0, 0))

    def update(self):
        self.tetris.update()


    def draw(self):
        self.draw_main_background()
        self.tetris.draw()
        self.display_screen.blit(self.tetris.tetris_surface, TETRIS_SURFACE_POS)
        self.tetris.draw_tetris_border(TETRIS_SURFACE_POS + (-17, -70))
        pg.display.flip()
        self.fps_clock.tick(FPS)


    def run(self):
        while 1:
            self.check_events()
            self.update()
            self.draw()

