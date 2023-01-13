from game_settings import *
from block import *
from drop_light import *

class Tetromino():
    def __init__(self, tetris):
        """
        Input: Đối tượng Tetris. Để class này có thể truy cập vào đối tượng Tetris.
        Process: Khởi tạo các giá trị cho đối tượng Tetromino
        Ouput: Không.
        """
        self.tetris = tetris
        self.init_tetromino_type()
        self.create_tetromino(self.tetris.is_first_tetromino)
        self.landing = False
        

    def init_tetromino_type(self):
        if self.tetris.app.game_mode == 'modern':
            types = ['normal', 'bomb']
            random_type = random.randint(0, 10)
            if random_type < 8:
                self.tetromino_type = types[0]
            elif random_type >= 8:
                self.tetromino_type = types[1]
        elif self.tetris.app.game_mode == 'classic':
            self.tetromino_type = 'normal'

    def create_tetromino(self, is_first_tetromino):
        """
        Input: Biến is_first_tetromino, dùng để kiểm tra đây có phải là khối tetromino đầu tiên hay không.
        Process: Tạo ra một khối tetromino ngẫu nhiên dựa vào các hình dạng.
        Ouput: Không.
        """
        if is_first_tetromino == True:
            self.core_pos = vector(INITIAL_TETROMINO_POS) # Tọa độ gốc
        else:
            self.core_pos = vector(NEXT_TETROMINO_POS)
        if self.tetromino_type == 'normal':
            self.create_normal_tetromino()
        elif self.tetromino_type == 'bomb':
            self.create_bomb_tetromino()


    def create_normal_tetromino(self):
        self.tetromino_name = random.choice(list(self.tetris.app.tetrominos.keys()))
        self.tetromino_rotation = random.randint(0, len(self.tetris.app.tetrominos[self.tetromino_name]) - 1)
        tetromino_shape = self.tetris.app.tetrominos[self.tetromino_name][self.tetromino_rotation]
        blocks_pos = []
        for x in range(SHAPE_TEMPLATE_COLS):
            for y in range(SHAPE_TEMPLATE_ROWS):
                if tetromino_shape[y][x] == 'o':
                    blocks_pos.append(vector(x, y) + self.core_pos)
        image_path = os.path.join(SOURCES_FILE_DIRECTORY, f'assets/images/blocks/block_{self.tetris.app.tetrominos_image_number[self.tetromino_name]}.png')
        self.image = pg.transform.scale(pg.image.load(image_path), (BLOCK_SIZE, BLOCK_SIZE))
        self.blocks = [Block(self, pos) for pos in blocks_pos]


    def create_bomb_tetromino(self):
        self.tetromino_name = 'DOT'
        self.tetromino_rotation = 0
        tetromino_shape = self.tetris.app.tetrominos[self.tetromino_name][self.tetromino_rotation]
        blocks_pos = []
        for x in range(SHAPE_TEMPLATE_COLS):
            for y in range(SHAPE_TEMPLATE_ROWS):
                if tetromino_shape[y][x] == 'o':
                    blocks_pos.append(vector(x, y) + self.core_pos)
        image_path = os.path.join(SOURCES_FILE_DIRECTORY, 'assets/images/effect/bomb_effect/1.png')
        self.image = pg.transform.scale(pg.image.load(image_path), (BLOCK_SIZE, BLOCK_SIZE))
        self.blocks = [Block(self, pos) for pos in blocks_pos]


    def move(self, direction):
        """
        Input: Hướng di chuyển (một chuỗi string).
        Process: Di chuyển khối tetromino nếu vị trí hợp lệ.
        Ouput: Không.
        """
        move_direction = MOVE_DIRECTIONS[direction]
        new_tetromino_pos = [block.block_pos + move_direction for block in self.blocks]
        is_collide = self.is_collide(new_tetromino_pos)

        if not is_collide:
            for block in self.blocks:
                block.block_pos += move_direction
            self.core_pos += move_direction # Sau khi di chuyển khối tetromino thì cập nhật lại tọa độ gốc
        elif direction == 'down':
            self.landing = True    
         
        
    def is_collide(self, tetromino_pos):
        """
        Input: Tọa độ của khối tetromino (tọa độ ma trận không phải tọa độ pixel).
        Process: Kiểm tra vị trí hiện tại của khối tetromino có hợp lệ không.
        Ouput: Giá trị boolean.
        """
        for pos in tetromino_pos:
            if Block.is_collide(self.blocks[0], pos): # tham số self.blocks[0] chỉ là tham số được thêm vào cho đúng số lượng tham số của hàm, không có tác dụng gì trong hàm này.
                return True
        return False
    
    
    def rotate(self, rotation_direction):
        """
        Input: Hướng xoay (một số nguyên int).
        Process: Xoay khối dựa vào hướng xoay (nếu vị trí xoay hợp lệ).
        Ouput: Không.
        """
        self.tetromino_rotation = (self.tetromino_rotation + rotation_direction) % len(self.tetris.app.tetrominos[self.tetromino_name])
        tetromino_shape = self.tetris.app.tetrominos[self.tetromino_name][self.tetromino_rotation]
        list_new_pos = []
        for x in range(SHAPE_TEMPLATE_COLS):
            for y in range(SHAPE_TEMPLATE_ROWS):
                if tetromino_shape[y][x] == 'o':
                    list_new_pos.append(vector(x, y) + self.core_pos)
        if self.is_collide(list_new_pos):
            self.tetris.play_sound('assets/music/sound_effects/blocking_sound.mp3')
            self.tetromino_rotation = (self.tetromino_rotation - rotation_direction) % len(self.tetris.app.tetrominos[self.tetromino_name])
        else:
            self.tetris.play_sound('assets/music/sound_effects/rotate_sound.wav', custom_volume = True, volume = 0.7)
            for i in range(len(self.blocks)):
                self.blocks[i].set_block_pos(list_new_pos[i])
        
        
    def move_all_the_way_down(self):
        """
        Input: Không.
        Process: Di chuyển khối chạm đất ngay lập tức.
        Ouput: Không.
        """
        for i in range(1, TETRIS_HEIGHT):
            new_tetromino_pos = [block.block_pos + (0, i) for block in self.blocks]
            if self.is_collide(new_tetromino_pos):
                break
        for block in self.blocks:
            block.block_pos += (0, i - 1)
            block.set_rect_topleft() #Sau khi đáp đất thì cập nhật ngay tọa độ của rect để group vẽ (do nếu rơi vào trường hợp game over thì vẫn có thể vẽ khối này)
            self.tetris.sprites_group.draw(self.tetris.tetris_surface) #Vẽ
        self.core_pos += (0, i - 1)
        Drop_Light(self.tetris, (self.core_pos + (2, 2)) * BLOCK_SIZE)
        self.tetris.counter = 0
        self.landing = True


    def draw_tetromino_drop_shadow(self):
        """
        Input: Không
        Process: Tính toán tọa độ khi đáp đất của khối tetromino hiện tại, sau đó vẽ ra bóng của khối tetromino (Tức lúc này khối tetromino vẫn chưa đáp đất, chỉ vẽ ảnh trong tương lai).
        Ouput: Không.
        """
        for i in range(1, TETRIS_HEIGHT):
            new_tetromino_pos = [block.block_pos + (0, i) for block in self.blocks]
            if self.is_collide(new_tetromino_pos):
                break
        future_landing_core_pos = self.core_pos + (0, i - 1)
        x, y = int(future_landing_core_pos.x), int(future_landing_core_pos.y)
        self.draw_tetromino_with_image(self.tetris.tetris_surface, 'assets/images/blocks/empty_block.png', BLOCK_SIZE, x, y)            


    def update(self):
        """
        Input: Không.
        Process: Sau một khoảng thời gian thì di chuyển khối tetromino xuống một ô (rơi tự do).
        Ouput: Không.
        """
        if time.time() - self.tetris.last_fall_down_time > self.tetris.fall_frequency:
            self.move('down')
            self.tetris.last_fall_down_time = time.time()


    # Chỉ dùng để vẽ hàng chờ tetromino
    def draw_tetromino(self, surface, block_size, core_pos_X = 0, core_pos_Y = 0): # core_pos của hàm này là tọa độ thực (dựa theo resolution), ko phải tọa độ trong matrix
        """
        Input: Surface, kích thước khối vuông, tọa độ gốc x, y (Tọa độ pixel, không phải tọa độ trên ma trận).
        Process: Vẽ khối tetromino dựa vào tọa độ truyền vào.
        Ouput: Không.
        """
        tetromino_shape = self.tetris.app.tetrominos[self.tetromino_name][self.tetromino_rotation]
        for x in range(5):
                for y in range(5):
                    if  tetromino_shape[y][x] == 'o':
                        coor_to_draw_X = (x * block_size) +  core_pos_X
                        coor_to_draw_Y = (y * block_size) + core_pos_Y
                        Block.draw_block(self.blocks[0], surface, coor_to_draw_X, coor_to_draw_Y, block_size)

    
    # Chỉ dùng để vẽ bóng đổ cho tetromino
    def draw_tetromino_with_image(self, surface, image_path, block_size, core_pos_X = 0, core_pos_Y = 0): # core_pos của hàm này là tọa độ ma trận ko phải tọa độ thực (tọa độ pixel)
        """
        Input: Surface, đường dẫn ảnh, kích thước khối vuông, tọa độ gốc x, y (Tọa độ pixel, không phải tọa độ trên ma trận).
        Process: Vẽ khối tetromino bằng hình ảnh dựa vào tọa độ truyền vào.
        Ouput: Không.
        """
        tetromino_shape = self.tetris.app.tetrominos[self.tetromino_name][self.tetromino_rotation]
        for x in range(5):
                for y in range(5):
                    if  tetromino_shape[y][x] == 'o':
                        coor_to_draw_X = (x + core_pos_X) * block_size
                        coor_to_draw_Y = (y + core_pos_Y) * block_size
                        Block.draw_block_image(self.blocks[0], surface, image_path, coor_to_draw_X, coor_to_draw_Y, BLOCK_SIZE_FUTURE_SHADOW , BLOCK_SIZE_FUTURE_SHADOW )


    def draw_tetromino_current_hold(self, surface, block_size, core_pos_X = 0, core_pos_Y = 0): # core_pos của hàm này là tọa độ thực (dựa theo resolution), ko phải tọa độ trong matrix
        tetromino_shape = self.tetris.app.tetrominos[self.tetromino_name][self.tetromino_rotation]
        for x in range(5):
                for y in range(5):
                    if  tetromino_shape[y][x] == 'o':
                        coor_to_draw_X = (x * block_size) + core_pos_X
                        coor_to_draw_Y = (y * block_size) + core_pos_Y
                        Block.draw_block_image_for_current_hold(self.blocks[0], surface, coor_to_draw_X, coor_to_draw_Y, block_size , block_size)
