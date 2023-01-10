from game_settings import *
from tetris import *
from button import *

class App():
    def __init__(self):
        """
        Input: Không.
        Process: Khởi tạo các giá trị cần thiết cho đối tượng App.
        Ouput: Không.
        """
        pg.init()
        pg.mixer.set_num_channels(100)
        self.display_screen = pg.display.set_mode(WINDOW_RES)
        self.set_tetrominos_template()
        self.tetris = Tetris(self)
        pg.display.set_caption('Tetris')
        self.background_image = self.load_image()
        self.fps_clock = pg.time.Clock()
        self.set_timer()
        self.create_option_attributes()


    def set_tetrominos_template(self):
        self.tetrominos = TETROMINOS_CLASSIC
        self.tetrominos_image_number = TETROMINOS_IMAGE_NUMBER_CLASSIC


    def update_tetromino_template(self):
        if self.game_mode == 'classic':
            self.tetrominos = TETROMINOS_CLASSIC
            self.tetrominos_image_number = TETROMINOS_IMAGE_NUMBER_CLASSIC
        elif self.game_mode == 'modern':
            self.tetrominos = TETROMINOS_MODERN
            self.tetrominos_image_number = TETROMINOS_IMAGE_NUMBER_MODERN


    def create_option_attributes(self):
        self.show_grid = False
        self.show_tetromino_shadow = True
        self.game_mode = 'classic'


    def set_timer(self):
        """
        Input: Không.
        Process: Tạo sự kiện người dùng effect_event và thiêt đặt kích hoat sự kiện này sau một khoảng thời gian. Hàm này dùng để tạo thời gian chạy hiệu ứng xóa hàng.
        Ouput: Biến effect_trigger và sự kiện người dùng effect_event.
        """
        self.effect_trigger = False
        self.effect_event = pg.USEREVENT + 0
        pg.time.set_timer(self.effect_event, 150)


    def terminate_program(self):
        """
        Input: Không.
        Process: Thoát game.
        Ouput: Không.
        """
        pg.quit()
        sys.exit()
   

    def check_events(self):
        """
        Input: Không.
        Process: Kiểm tra sự kiện và kích hoạt các hàm xử lý sự kiện.
        Ouput: Nếu có sự kiện effect_event trả về True cho biến effect_trigger.
        """
        self.effect_trigger = False
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                self.terminate_program()
            elif event.type == pg.KEYDOWN:
                self.tetris.key_down_handle(pressed_key=event.key)
            elif event.type == pg.KEYUP:
                self.tetris.key_up_handle(release_key=event.key)
            elif event.type == self.effect_event:
                self.effect_trigger = True

    
    def load_image(self):
        """
        Input: String đường dẫn của hình ảnh.
        Process: Tải ảnh lên và scale ảnh theo kích thước của độ phân giải màn hình hiển thị (display_screen)
        Ouput: Trả về ảnh đã scale
        """
        # Nối tên file với thư mục chứa mã nguồn, để load ảnh ko bị lỗi
        image_path = os.path.join(SOURCES_FILE_DIRECTORY, 'assets/images/background/main_background.png')
        return pg.transform.scale(pg.image.load(image_path), (WINDOW_WIDTH, WINDOW_HEIGHT))


    def draw_main_background(self):
        """
        Input: Không.
        Process: Thêm hình nền vào display_screen surface (màn hình hiển thị chính)
        Ouput: Không.
        """
        self.display_screen.blit(self.background_image, (0, 0))


    def update(self):
        """
        Input: Không.
        Process: Hàm thực hiện các hàm update con khác. (Hàm update chính)
        Ouput: Không.
        """
        self.tetris.update()


    def draw(self):
        """
        Input: Không.
        Process: Hiển thị tất cả nội dung trong display_screen lên màn hình, đồng thời chạy clock để đảm bảo chương trình chạy đúng
        với số FPS truyền vào.
        Ouput: Không.
        """
        self.draw_main_background()
        self.tetris.draw()
        self.display_screen.blit(self.tetris.tetris_surface, self.tetris.tetris_surface_pos)
        self.tetris.draw_tetris_border(self.tetris.tetris_border_pos)
        pg.display.flip()
        self.fps_clock.tick(FPS)


    def play_game(self):
        """
        Input: Không.
        Process: Chạy vòng lặp chính của game.
        Ouput: Không.
        """
        while 1:
            self.check_events()
            self.update()
            self.draw()


    def main_menu(self):
        while True:
            mouse_pos = pg.mouse.get_pos()
            play_button = Button('assets/images/button/play_button.png', 300, 75, mouse_pos, (WINDOW_WIDTH // 2, 610))
            if self.game_mode == 'classic':
                game_mode_button = Button('assets/images/button/game_mode_classic_button.png', 300, 75, mouse_pos, (WINDOW_WIDTH // 2, 720))
            elif self.game_mode == 'modern':
                game_mode_button = Button('assets/images/button/game_mode_modern_button.png', 300, 75, mouse_pos, (WINDOW_WIDTH // 2, 720))
            option_button = Button('assets/images/button/option_button.png', 300, 75, mouse_pos, (WINDOW_WIDTH // 2, 830))
            quit_button = Button('assets/images/button/quit_button.png', 300, 75, mouse_pos, (WINDOW_WIDTH // 2, 940))

            #Event handle
            for event in pg.event.get():
                if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                    self.terminate_program()
                if event.type == pg.MOUSEBUTTONDOWN:
                    if play_button.is_mouse_collide():
                        self.tetris.__init__(self)
                        self.play_game()
                    elif game_mode_button.is_mouse_collide():
                        if self.game_mode == 'classic':
                            self.game_mode = 'modern'
                        else:
                            self.game_mode = 'classic'
                        self.update_tetromino_template() # Cập nhật lại tetrominos template của class app
                    elif option_button.is_mouse_collide():
                        self.setting_menu()
                    elif quit_button.is_mouse_collide():
                        self.terminate_program()

            #Draw
            self.display_screen.fill('grey')
            for button in [play_button, game_mode_button, option_button, quit_button]:
                if button.is_mouse_collide():
                    button.hover()
                button.blit_to_surface(self.display_screen)
            pg.display.flip()
            self.fps_clock.tick()


    def pause_menu(self):
         while True:
            mouse_pos = pg.mouse.get_pos()
            resume_button = Button('assets/images/button/resume_button.png', 300, 75, mouse_pos, (WINDOW_WIDTH // 2, 610))
            option_button = Button('assets/images/button/option_button.png', 300, 75, mouse_pos, (WINDOW_WIDTH // 2, 720))
            main_menu_button = Button('assets/images/button/main_menu_button.png', 300, 75, mouse_pos, (WINDOW_WIDTH // 2, 830))
            quit_button = Button('assets/images/button/quit_button.png', 300, 75, mouse_pos, (WINDOW_WIDTH // 2, 940))

            #Event handle
            for event in pg.event.get():
                if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                    self.terminate_program()
                if event.type == pg.MOUSEBUTTONDOWN:
                    if resume_button.is_mouse_collide():
                        self.tetris.last_fall_down_time = time.time()
                        self.tetris.last_move_down_time = time.time()
                        self.tetris.last_move_sideways_time = time.time()
                        self.play_game()
                    if option_button.is_mouse_collide():
                        self.setting_menu()
                    if main_menu_button.is_mouse_collide():
                        self.main_menu()
                    if quit_button.is_mouse_collide():
                        self.terminate_program()

            #Draw
            pause_menu_background_image = self.tetris.load_image('assets/images/background/pause_background.jpg', 1920, 1080)
            self.display_screen.blit(pause_menu_background_image, (0, 0))
            for button in [resume_button, option_button, main_menu_button, quit_button]:
                if button.is_mouse_collide():
                    button.hover()
                button.blit_to_surface(self.display_screen)
            pg.display.flip()
            self.fps_clock.tick()


    def setting_menu(self):
        setting_pop_up_surface = pg.Surface((1000, 300))
        turtorial_pop_up_surface = pg.Surface((1000, 300))
        while True:
            mouse_pos = pg.mouse.get_pos()


            if self.show_grid == True:
                grid_check_button = Button('assets/images/button/check_button.png', 50, 50, mouse_pos, (1350, 440))
            else:
                grid_check_button = Button('assets/images/button/uncheck_button.png', 50, 50, mouse_pos, (1350, 440))


            if self.show_tetromino_shadow == True:
                shadow_check_button = Button('assets/images/button/check_button.png', 50, 50, mouse_pos, (1350, 540))
            else:
                shadow_check_button = Button('assets/images/button/uncheck_button.png', 50, 50, mouse_pos, (1350, 540))
            
            
            back_button = Button('assets/images/button/back_button.png', 300, 75, mouse_pos, (200 ,960))

            # Text
            quaver_font = pg.font.Font('assets/fonts/quaver.ttf', FONT_SIZE_SCORE)
            show_grid_text = quaver_font.render('Show grid: ', 1, 'white')
            show_tetromino_shadow = quaver_font.render('Show tetromino shadow: ', 1, 'white')


            #Event handle
            for event in pg.event.get():
                if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                    self.terminate_program()
                if event.type == pg.MOUSEBUTTONDOWN:
                    if grid_check_button.is_mouse_collide():
                        if self.show_grid == False:
                            self.show_grid = True
                        else:
                             self.show_grid = False
                    elif shadow_check_button.is_mouse_collide():
                        if self.show_tetromino_shadow == False:
                            self.show_tetromino_shadow = True
                        else:
                             self.show_tetromino_shadow = False
                    elif back_button.is_mouse_collide():
                        return

            #Draw
            turtorial_pop_up_surface.fill('orange')
            setting_pop_up_surface.fill('orange')
            setting_pop_up_surface.blit(show_grid_text, (40, 125))
            setting_pop_up_surface.blit(show_tetromino_shadow, (40, 225))
            setting_menu_background_image = self.tetris.load_image('assets/images/background/setting_background.png', 1920, 1080)
            self.display_screen.blit(setting_menu_background_image, (0, 0))
            self.display_screen.blit(setting_pop_up_surface, (460, 300))
            self.display_screen.blit(turtorial_pop_up_surface, (460, 700))
            for button in [grid_check_button, shadow_check_button, back_button]:
                if button.is_mouse_collide():
                    button.hover()
                button.blit_to_surface(self.display_screen)

            # grid_radio_button.blit_to_surface(self.display_screen)
            # shadow_radio_button.blit_to_surface(self.display_screen)
            # back_button.blit_to_surface(self.display_screen)
            pg.display.flip()
            self.fps_clock.tick()


    def run(self):
        self.main_menu()

