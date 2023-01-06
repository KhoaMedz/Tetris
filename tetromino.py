from game_settings import *
from block import *

class Tetromino():
    def __init__(self, tetris):
        """
        Input: Đối tượng Tetris. Để class này có thể truy cập vào đối tượng Tetris.
        Process: Khởi tạo các giá trị cho đối tượng Tetromino
        Ouput: Không.
        """
        self.tetris = tetris
        self.create_tetromino(self.tetris.is_first_tetromino)
        self.landing = False
        

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

        self.tetromino_name = random.choice(list(TETROMINOS.keys()))
        self.tetromino_rotation = random.randint(0, len(TETROMINOS[self.tetromino_name]) - 1)
        tetromino_shape = TETROMINOS[self.tetromino_name][self.tetromino_rotation]
        blocks_pos = []
        for x in range(SHAPE_TEMPLATE_COLS):
            for y in range(SHAPE_TEMPLATE_ROWS):
                if tetromino_shape[y][x] == 'o':
                    blocks_pos.append(vector(x, y) + self.core_pos)
        image_path = os.path.join(SOURCES_FILE_DIRECTORY, f'images/blocks/block_{TETROMINOS_IMAGE_NUMBER[self.tetromino_name]}.png')
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
        self.tetromino_rotation = (self.tetromino_rotation + rotation_direction) % len(TETROMINOS[self.tetromino_name])
        tetromino_shape = TETROMINOS[self.tetromino_name][self.tetromino_rotation]
        list_new_pos = []
        for x in range(SHAPE_TEMPLATE_COLS):
            for y in range(SHAPE_TEMPLATE_ROWS):
                if tetromino_shape[y][x] == 'o':
                    list_new_pos.append(vector(x, y) + self.core_pos)
        if self.is_collide(list_new_pos):
            self.tetris.play_sound('music/sound_effects/blocking_sound.mp3')
            self.tetromino_rotation = (self.tetromino_rotation - rotation_direction) % len(TETROMINOS[self.tetromino_name])
        else:
            self.tetris.play_sound('music/sound_effects/rotate_sound.wav')
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
        self.landing = True


    def update(self):
        """
        Input: Không.
        Process: Sau một khoảng thời gian thì di chuyển khối tetromino xuống một ô (rơi tự do).
        Ouput: Không.
        """
        if time.time() - self.tetris.last_fall_down_time > self.tetris.fall_frequency:
            self.move('down')
            self.tetris.last_fall_down_time = time.time()


    def draw_piece(self, surface, block_size, core_pos_X = 0, core_pos_Y = 0): # core_pos của hàm này là tọa độ thực (dựa theo resolution), ko phải tọa độ trong matrix
        """
        Input: Surface, kích thước khối vuông, tọa độ gốc x, y (Tọa độ pixel, không phải tọa độ trên ma trận).
        Process: Vẽ khối tetromino dựa vào tọa độ truyền vào.
        Ouput: Không.
        """
        tetromino_shape = TETROMINOS[self.tetromino_name][self.tetromino_rotation]
        for x in range(5):
                for y in range(5):
                    if  tetromino_shape[y][x] == 'o':
                        coor_to_draw_X = (x * block_size) +  core_pos_X
                        coor_to_draw_Y = (y * block_size) + core_pos_Y
                        Block.draw_block(self.blocks[0], surface, coor_to_draw_X, coor_to_draw_Y, block_size)