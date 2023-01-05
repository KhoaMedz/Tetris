from game_settings import *
from tetromino import *

class Tetris():
    def __init__(self, app):
        self.app = app
        self.sprites_group = pg.sprite.Group()
        self.is_first_tetromino = True
        self.tetromino = Tetromino(self)
        self.tetris_surface = pg.Surface(TETRIS_RES)
        self.score_surface = pg.Surface((300, 175), pg.SRCALPHA, 32).convert_alpha()
        self.next_level_surface = pg.Surface((300, 175), pg.SRCALPHA, 32).convert_alpha()
        self.level_surface = pg.Surface((175, 175), pg.SRCALPHA, 32).convert_alpha()
        self.speed_surface = pg.Surface((175, 175), pg.SRCALPHA, 32).convert_alpha()
        self.tetromino_queue_surface = pg.Surface((123, 550), pg.SRCALPHA, 32).convert_alpha()
        self.tetris_background_image = self.load_image('images/background/tetris_background.png', TETRIS_WIDTH, TETRIS_HEIGHT)
        self.tetris_border_image = self.load_image('images/background/tetris_border.png', TETRIS_WIDTH + 38, TETRIS_HEIGHT + 118)
        self.create_last_action_time()
        self.create_moving_action()
        self.create_tetris_matrix()
        self.create_tetromino_queue()
        self.create_score_attributes()

        
    def create_last_action_time(self):
        self.last_fall_down_time = time.time()
        self.last_move_sideways_time = time.time()
        self.last_move_down_time = time.time()


    def create_moving_action(self):
        self.moving_left = False
        self.moving_right = False
        self.moving_down = False


    def create_tetris_matrix(self):
        self.tetris_matrix = [[0] * TETRIS_HEIGHT for x in range(TETRIS_COLS)]


    def create_tetromino_queue(self):
        self.tetromino_queue = queue.Queue(maxsize=4) # Tetromino queue gồm 5 khối tetromino
        self.is_first_tetromino = False
        for i in range(self.tetromino_queue.maxsize):
            self.tetromino_queue.put(Tetromino(self))


    def create_score_attributes(self):
        self.score = 0
        self.level = 1
        self.score_to_reach_next_level = 2000
        self.fall_frequency = ORIGINAL_FALL_FREQUENCY


    def load_image(self, image_path, image_width, image_height):
        # Nối tên file với thư mục chứa mã nguồn, để load ảnh ko bị lỗi
        image_path = os.path.join(SOURCES_FILE_DIRECTORY, image_path)
        return pg.transform.scale(pg.image.load(image_path).convert_alpha(), (image_width, image_height))


    def put_tetromino_blocks_into_matrix(self):
        for block in self.tetromino.blocks:
            x, y = int(block.block_pos.x), int(block.block_pos.y)
            self.tetris_matrix[x][y] = block

    def is_out_of_index(self, x, y):
        if 0 <= x < TETRIS_COLS and 0 <= y < TETRIS_HEIGHT:
            return False
        return True

    def is_game_over(self):
        for block in self.tetromino.blocks:
            x, y = int(block.block_pos.x), int(block.block_pos.y)
            if self.is_out_of_index(x ,y):
                return True
        return False

    def draw_grid(self):
        for x in range(TETRIS_COLS):
            for y in range(TETRIS_ROWS):
                pg.draw.rect(self.tetris_surface, GREY, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)


    def draw_background(self, pos):
        self.tetris_surface.blit(self.tetris_background_image, pos)


    def draw_tetris_border(self, pos):
        self.app.display_screen.blit(self.tetris_border_image, pos)


    def key_up_handle(self, release_key):
        if release_key == pg.K_LEFT:
            self.moving_left = False
        elif release_key == pg.K_RIGHT:
            self.moving_right = False
        elif release_key == pg.K_DOWN:
            self.moving_down = False


    def key_down_handle(self, pressed_key):
        if pressed_key == pg.K_LEFT:
            self.moving_left = True
            self.moving_right = False
            self.tetromino.move('left')
            self.last_move_sideways_time = time.time()
        elif pressed_key == pg.K_RIGHT:
            self.moving_right = True
            self.moving_left = False
            self.tetromino.move('right')
            self.last_move_sideways_time = time.time()
        elif pressed_key == pg.K_DOWN:
            self.moving_down = True
            self.tetromino.move('down')
            self.last_move_down_time = time.time()
        elif pressed_key == pg.K_z: # Xoay theo chiều kim đồng hồ
            self.tetromino.rotate(1)
        elif pressed_key == pg.K_x: # Xoay ngược chiều kim đồng hồ
            self.tetromino.rotate(-1)
        elif pressed_key == pg.K_c:
            self.moving_left = False
            self.moving_right = False
            self.moving_down = False
            self.tetromino.move_all_the_way_down()
        elif pressed_key == pg.K_p:
            self.draw_text_on_screen('PAUSE')
            self.last_fall_down_time = time.time()
            self.last_move_down_time = time.time()
            self.last_move_sideways_time = time.time()


    def hold_key_handle(self):
        if (self.moving_left or self.moving_right) and time.time() - self.last_move_sideways_time > MOVE_SIDEAWAYS_FREQUENCY:
            if self.moving_left:
                self.tetromino.move('left')
                self.last_move_sideways_time = time.time()
            else:
                self.tetromino.move('right')
                self.last_move_sideways_time = time.time()
        if self.moving_down and time.time() - self.last_move_down_time > MOVE_DOWN_FREQUENCY:
                self.tetromino.move('down')
                self.last_move_down_time = time.time()
        

    def landed_tetromino_handle(self):
        if self.tetromino.landing:
            if self.is_game_over():
                self.draw_text_on_screen('Game Over')
                self.__init__(self.app) # game over handle
            else:
                self.play_sound('music/sound_effects/brick_drop.mp3')
                self.put_tetromino_blocks_into_matrix()
                removed_lines_num = self.removed_completed_lines()
                self.calculate_score(removed_lines_num)
                self.calculate_level()
                self.calculate_fall_frequency()
                self.tetromino = self.tetromino_queue.get()
                self.tetromino_queue.put(Tetromino(self))


    def is_completed_line(self, line):
        for x in range(TETRIS_COLS):
            if not self.tetris_matrix[x][line]:
                return False
        return True


    def removed_completed_lines(self):
        line = TETRIS_ROWS - 1
        removed_lines_num = 0
        while line >= 0: 
            if self.is_completed_line(line):
                for x in range(TETRIS_COLS):
                    self.tetris_matrix[x][line].alive = False # Đặt về False để xóa block ra khỏi group
                for y in range(line, 0, -1):
                    for x in range(TETRIS_COLS):
                        self.tetris_matrix[x][y] = self.tetris_matrix[x][y - 1]
                        if self.tetris_matrix[x][y]:
                            self.tetris_matrix[x][y].block_pos = vector(x, y)
                for x in range(TETRIS_COLS):
                    self.tetris_matrix[x][0] = 0
                removed_lines_num += 1
            else:
                line -= 1
        if removed_lines_num > 0:
            self.app.time_stop = True
        return removed_lines_num


    def calculate_score(self, removed_lines_num):
            num = 0
            for i in range(removed_lines_num):
                num += i + 1
            self.score += 100 * num
            

    def calculate_level(self):
        score_step = 2000 
        score_temp = 0
        lv = 0

        while score_temp <= self.score:
            lv += 1
            score_temp += score_step
            score_step += 1000

        self.level = lv
        self.score_to_reach_next_level = score_temp


    def calculate_fall_frequency(self):
        if self.level > 1: # bắt đầu tính chu kỳ rơi từ level 2
            self.fall_frequency = ORIGINAL_FALL_FREQUENCY - (self.level * 0.075)
            if self.fall_frequency < 0.1:
                self.fall_frequency = 0.1


    def draw_tetromino_queue(self):
        tetromino_queue_background_image = self.load_image('images/background/tetromino_queue_background.png', 123, 550)
        self.tetromino_queue_surface.blit(tetromino_queue_background_image, (0, 0))
        tetronimo_queue_y = 73
        for tetromino in self.tetromino_queue.queue:
            tetromino.draw_piece(self.tetromino_queue_surface, TETROMINO_QUEUE_BLOCK_SIZE, 29, tetronimo_queue_y)
            tetronimo_queue_y += 129
        self.app.display_screen.blit(self.tetromino_queue_surface, (TETROMINO_QUEUE_SURFACE_POS))


    def draw_score(self):
        score_background_image = self.load_image('images/background/sign_0.png', 300, 175)
        pixel_font = pg.font.Font('fonts/PixelatedRegular.ttf', FONT_SIZE_SCORE)
        score_text = pixel_font.render('SCORE', 1, 'white')
        score_number_text = pixel_font.render(str(self.score), 1, 'white')
        self.score_surface.blit(score_background_image, (0, 0))
        self.score_surface.blit(score_text, (100, 20))
        self.score_surface.blit(score_number_text, (70, 100))
        self.app.display_screen.blit(self.score_surface, (DRAW_SCORE_POS))


    def draw_next_level(self):
        next_level_background_image = self.load_image('images/background/sign_0.png', 300, 175)
        pixel_font = pg.font.Font('fonts/PixelatedRegular.ttf', FONT_SIZE_SCORE)
        next_level_text = pixel_font.render('NEXT   LV', 1, 'white')
        next_level_number_text = pixel_font.render(str(self.score_to_reach_next_level), 1, 'white')
        self.next_level_surface.blit(next_level_background_image, (0, 0))
        self.next_level_surface.blit(next_level_text, (80, 20))
        self.next_level_surface.blit(next_level_number_text, (70, 100))
        self.app.display_screen.blit(self.next_level_surface, (DRAW_NEXT_LEVEL_POS))


    def draw_level(self):
        level_background_image = self.load_image('images/background/sign_0.png', 175, 175)
        pixel_font = pg.font.Font('fonts/PixelatedRegular.ttf', FONT_SIZE_SCORE)
        level_text = pixel_font.render('LEVEL', 1, 'white')
        level_number_text = pixel_font.render(str(self.level), 1, 'white')
        self.level_surface.blit(level_background_image, (0, 0))
        self.level_surface.blit(level_text, (42, 20))
        self.level_surface.blit(level_number_text, (50, 100))
        self.app.display_screen.blit(self.level_surface, (DRAW_LEVEL_POS))


    def draw_speed(self):
        speed_background_image = self.load_image('images/background/sign_0.png', 175, 175)
        pixel_font = pg.font.Font('fonts/PixelatedRegular.ttf', FONT_SIZE_SCORE)
        speed_text = pixel_font.render('SPEED', 1, 'white')
        speed_number_text = pixel_font.render(f'drop/{str(self.fall_frequency)} s', 1, 'white')
        self.speed_surface.blit(speed_background_image, (0, 0))
        self.speed_surface.blit(speed_text, (42, 20))
        self.speed_surface.blit(speed_number_text, (20, 100))
        self.app.display_screen.blit(self.speed_surface, (DRAW_SPEED_POS))


    def draw_text_on_screen(self, text):
        # Tạo text
        font_path = os.path.join(SOURCES_FILE_DIRECTORY, 'fonts/PixelatedRegular.ttf')
        pixel_font = pg.font.Font(font_path, 100)
        text_surface = pixel_font.render(text, 1, 'red')
        text_rect = text_surface.get_rect()
        text_rect.center = (TETRIS_WIDTH // 2, TETRIS_HEIGHT // 2)
        # Tạo 'press any key to continue or ESC to exit'
        pixel_font = pg.font.Font(font_path, 35)
        text_surface_2 = pixel_font.render('Press any key to continue or ESC to exit', 1, 'red')
        text_2_rect = text_surface_2.get_rect()
        text_2_rect.center = (TETRIS_WIDTH // 2, TETRIS_HEIGHT // 2 + 50)
        # Vẽ text lên tetris surface
        self.tetris_surface.blit(text_surface, text_rect)
        self.tetris_surface.blit(text_surface_2, text_2_rect)
        # Vẽ tetris surface lên main surface
        self.app.display_screen.blit(self.tetris_surface, TETRIS_SURFACE_POS)
        self.draw_tetris_border(TETRIS_SURFACE_POS + (-17, -87)) # Vẽ khung lên main surface (display_screen)
        while not self.is_pressed():
            pg.display.flip()
            self.app.fps_clock.tick()


    def is_pressed(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                self.app.terminate_program()
            elif event.type == pg.KEYDOWN:
                return True
        return False


    def play_sound(self, sound_path):
        sound_path = os.path.join(SOURCES_FILE_DIRECTORY, sound_path)
        sound_to_play = pg.mixer.Sound(sound_path)
        sound_to_play.play()



    def update(self):
        self.tetromino.update()
        self.hold_key_handle()
        self.landed_tetromino_handle()
        self.sprites_group.update()


    def draw(self):
        self.draw_background(vector(0, 0))
        #self.draw_grid()
        self.draw_tetromino_queue()
        self.sprites_group.draw(self.tetris_surface) # Vẽ ra các sprite có trong group (các khối gạch)
        self.draw_score()
        self.draw_next_level()
        self.draw_level()
        self.draw_speed()
    

