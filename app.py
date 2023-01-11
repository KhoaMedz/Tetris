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
            if event.type == pg.KEYDOWN:
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
        self.tetris.play_music('assets/music/background_music/play_game_theme_0.mp3', -1, custom_volume= True, volume= 0.7)
        while 1:
            self.check_events()
            self.update()
            self.draw()


    def main_menu(self):
        self.tetris.play_music('assets/music/background_music/main_menu_theme.mp3', -1, 3.7, True, 0.5)
        logo_image = self.tetris.load_image('assets/images/background/main_logo.png', 790, 300)
        main_menu_background_image = self.tetris.load_image('assets/images/background/main_menu_background.png', 1920, 1080)
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
            self.display_screen.blit(main_menu_background_image, (0, 0))
            self.display_screen.blit(logo_image, (550, 60))
            for button in [play_button, game_mode_button, option_button, quit_button]:
                if button.is_mouse_collide():
                    button.hover()
                button.blit_to_surface(self.display_screen)
            pg.display.flip()
            self.fps_clock.tick()


    def pause_menu(self):
        pause_logo_image = self.tetris.load_image('assets/images/background/pause_logo.png', 1920, 90)
        while True:
            mouse_pos = pg.mouse.get_pos()
            resume_button = Button('assets/images/button/resume_button.png', 300, 75, mouse_pos, (WINDOW_WIDTH // 2, 610))
            option_button = Button('assets/images/button/option_button.png', 300, 75, mouse_pos, (WINDOW_WIDTH // 2, 720))
            main_menu_button = Button('assets/images/button/main_menu_button.png', 300, 75, mouse_pos, (WINDOW_WIDTH // 2, 830))
            quit_button = Button('assets/images/button/quit_button.png', 300, 75, mouse_pos, (WINDOW_WIDTH // 2, 940))

            #Event handle
            for event in pg.event.get():
                if event.type == pg.MOUSEBUTTONDOWN:
                    if resume_button.is_mouse_collide():
                        self.tetris.last_fall_down_time = time.time()
                        self.tetris.last_move_down_time = time.time()
                        self.tetris.last_move_sideways_time = time.time()
                        return
                    if option_button.is_mouse_collide():
                        self.setting_menu()
                    if main_menu_button.is_mouse_collide():
                        self.main_menu()
                    if quit_button.is_mouse_collide():
                        self.terminate_program()

            #Draw
            pause_menu_background_image = self.tetris.load_image('assets/images/background/pause_background.jpg', 1920, 1080)
            self.display_screen.blit(pause_menu_background_image, (0, 0))
            self.display_screen.blit(pause_logo_image, (0, 40))
            for button in [resume_button, option_button, main_menu_button, quit_button]:
                if button.is_mouse_collide():
                    button.hover()
                button.blit_to_surface(self.display_screen)
            pg.display.flip()
            self.fps_clock.tick()


    def setting_menu(self):
        # Tạo surface popup và load ảnh
        setting_pop_up_surface = pg.Surface((1000, 300), pg.SRCALPHA, 32).convert_alpha()
        tutorial_pop_up_surface = pg.Surface((1000, 550), pg.SRCALPHA, 32).convert_alpha()
        setting_popup_background_image = self.tetris.load_image('assets/images/background/setting_popup_background.png', 1000, 300)
        tutorial_popup_background_image = self.tetris.load_image('assets/images/background/tutorial_popup_background.png', 1000, 435)
        option_menu_background_image = self.tetris.load_image('assets/images/background/option_background.png', 1920, 1080)
        option_logo_image = self.tetris.load_image('assets/images/background/option_logo.png', 1920, 90)

        while True:
            mouse_pos = pg.mouse.get_pos()
            if self.show_grid == True:
                grid_check_button = Button('assets/images/button/check_button.png', 50, 50, mouse_pos, (1350, 330))
            else:
                grid_check_button = Button('assets/images/button/uncheck_button.png', 50, 50, mouse_pos, (1350, 330))

            if self.show_tetromino_shadow == True:
                shadow_check_button = Button('assets/images/button/check_button.png', 50, 50, mouse_pos, (1350, 410))
            else:
                shadow_check_button = Button('assets/images/button/uncheck_button.png', 50, 50, mouse_pos, (1350, 410))
            back_button = Button('assets/images/button/back_button.png', 300, 75, mouse_pos, (200 ,960))

            # Load fonts
            quaver_font_size_50 = pg.font.Font('assets/fonts/quaver.ttf', 50)
            quaver_font_size_40 = pg.font.Font('assets/fonts/quaver.ttf', 40)

            # Setting_popup_texts
            setting_popup_name_text = quaver_font_size_50.render('Setting', 1, (86, 52, 42))
            show_grid_text = quaver_font_size_40.render('Show grid: ', 1, 'white')
            show_tetromino_shadow_text = quaver_font_size_40.render('Show tetromino shadow: ', 1, 'white')

            # Tutorial texts
            tutorial_popup_name_text = quaver_font_size_50.render('Tutorial', 1, (86, 52, 42))

            #Event handle
            for event in pg.event.get():
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

            #Setting popup
            setting_pop_up_surface.blit(setting_popup_background_image, (0, 0))
            setting_pop_up_surface.blit(setting_popup_name_text, (50, 15))
            setting_pop_up_surface.blit(show_grid_text, (40, 120))
            setting_pop_up_surface.blit(show_tetromino_shadow_text, (40, 200))
            
            #Turtorial_popup
            tutorial_pop_up_surface.blit(tutorial_popup_background_image, (0, 0))
            tutorial_pop_up_surface.blit(tutorial_popup_name_text, (35, 15))

            #Display screen
            self.display_screen.blit(option_menu_background_image, (0, 0))
            self.display_screen.blit(option_logo_image, (0, 40))
            self.display_screen.blit(setting_pop_up_surface, (460, 200))
            self.display_screen.blit(tutorial_pop_up_surface, (460, 550))
            for button in [grid_check_button, shadow_check_button, back_button]:
                if button.is_mouse_collide():
                    button.hover()
                button.blit_to_surface(self.display_screen)

            pg.display.flip()
            self.fps_clock.tick()


    def game_over_menu(self):
        game_over_popup_background_image = self.tetris.load_image('assets/images/background/game_over_popup_background.png', 400, 450)
        while True:
            mouse_pos = pg.mouse.get_pos()
            restart_button = Button('assets/images/button/restart_button.png', 250, 62, mouse_pos, (WINDOW_WIDTH // 2, 450))
            main_menu_button = Button('assets/images/button/main_menu_button.png', 250, 62, mouse_pos, (WINDOW_WIDTH // 2, 540))
            quit_button = Button('assets/images/button/quit_button.png', 250, 62, mouse_pos, (WINDOW_WIDTH // 2, 630))

            #Event handle
            for event in pg.event.get():
                if event.type == pg.MOUSEBUTTONDOWN:
                    if restart_button.is_mouse_collide():
                        self.tetris.last_fall_down_time = time.time()
                        self.tetris.last_move_down_time = time.time()
                        self.tetris.last_move_sideways_time = time.time()
                        self.play_game()
                    if main_menu_button.is_mouse_collide():
                        self.main_menu()
                    if quit_button.is_mouse_collide():
                        self.terminate_program()

            #Draw
            self.display_screen.blit(game_over_popup_background_image, (762, 290))
            for button in [restart_button, main_menu_button, quit_button]:
                if button.is_mouse_collide():
                    button.hover()
                button.blit_to_surface(self.display_screen)
            pg.display.flip()
            self.fps_clock.tick()

    def run(self):
        self.main_menu()

