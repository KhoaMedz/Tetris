from game_settings import *
from tetromino import *

class Tetris():
    def __init__(self, app):
        self.app = app
        self.sprites_group = pg.sprite.Group()
        self.is_first_tetromino = True
        self.tetromino = Tetromino(self)
        self.tetris_surface = pg.Surface(TETRIS_RES)
        self.score_surface = pg.Surface((FONT_SIZE_SCORE * 7, FONT_SIZE_SCORE * 4))
        self.tetromino_queue_surface = pg.Surface(TETROMINO_QUEUE_RES)
        self.create_last_action_time()
        self.create_moving_action()
        self.create_tetris_matrix()
        self.create_tetromino_queue()
        self.create_score_attributes()
        
        
    def create_last_action_time(self):
        self.last_fall_down_time = time.time()
        self.last_move_sideways_time = time.time()
        self.last_move_down_time =time.time()


    def create_moving_action(self):
        self.moving_left = False
        self.moving_right = False
        self.moving_down = False


    def create_tetris_matrix(self):
        self.tetris_matrix = [[0] * TETRIS_HEIGHT for x in range(TETRIS_COLS)]


    def create_tetromino_queue(self):
        self.tetromino_queue = queue.Queue(maxsize=5) # Tetromino queue gồm 5 khối tetromino
        self.is_first_tetromino = False
        for i in range(self.tetromino_queue.maxsize):
            self.tetromino_queue.put(Tetromino(self))


    def create_score_attributes(self):
        self.score = 0
        self.level = 1
        self.score_to_reach_next_level = 2000
        self.fall_frequency = ORIGINAL_FALL_FREQUENCY


    def put_tetromino_blocks_into_matrix(self):
        for block in self.tetromino.blocks:
            x, y = int(block.block_pos.x), int(block.block_pos.y)
            self.tetris_matrix[x][y] = block


    def draw_grid(self):
        for x in range(TETRIS_COLS):
            for y in range(TETRIS_ROWS):
                pg.draw.rect(self.tetris_surface, GREY, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)


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
        self.tetromino_queue_surface.fill(LIGHT_BROWN)
        tetromino_queue_grid_rects = [pg.Rect(x * TETROMINO_QUEUE_BLOCK_SIZE, y * TETROMINO_QUEUE_BLOCK_SIZE, TETROMINO_QUEUE_BLOCK_SIZE, TETROMINO_QUEUE_BLOCK_SIZE) for x in range(TETROMINO_QUEUE_COLS) for y in range(TETROMINO_QUEUE_ROWS)]
        [pg.draw.rect(self.tetromino_queue_surface, GREY, i, 1) for i in tetromino_queue_grid_rects]
        tetronimo_queue_y = 1

        for tetromino in self.tetromino_queue.queue:
            tetromino.draw_piece(self.tetromino_queue_surface, TETROMINO_QUEUE_BLOCK_SIZE, 1, tetronimo_queue_y)
            tetronimo_queue_y += 5

        self.app.display_screen.blit(self.tetromino_queue_surface, TETROMINO_QUEUE_SURFACE_POS)


    def draw_score(self, margin_x = 0, margin_y = 0):
        self.score_surface.fill('white')
        pixel_font = pg.font.Font('fonts/PixelatedRegular.ttf', FONT_SIZE_SCORE)
        labels = []
        texts = [f'Score:    {self.score}', f'Level:    {self.level}', f'Next level:    {self.score_to_reach_next_level}', f'Fall frequency:    {self.fall_frequency} s']

        for line in range(len(texts)):
            labels.append(pixel_font.render(texts[line], 1, 'orange'))

        self.score_surface.blit(labels[0], (margin_x, margin_y + FONT_SIZE_SCORE * 0))
        self.score_surface.blit(labels[1], (margin_x, margin_y + FONT_SIZE_SCORE * 1))
        self.score_surface.blit(labels[2], (margin_x, margin_y + FONT_SIZE_SCORE * 2))
        self.score_surface.blit(labels[3], (margin_x, margin_y + FONT_SIZE_SCORE * 3))

        self.app.display_screen.blit(self.score_surface, DRAW_SCORE_POS)


    def update(self):
        self.tetromino.update()
        self.hold_key_handle()
        self.landed_tetromino_handle()
        self.sprites_group.update()


    def draw(self):
        self.tetris_surface.fill(BROWN)
        self.draw_grid()
        self.draw_tetromino_queue()
        self.sprites_group.draw(self.tetris_surface) # Vẽ ra các sprite có trong group (các khối gạch)
        self.draw_score(10, 10)
    

