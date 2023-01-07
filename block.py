from game_settings import *

class Block(pg.sprite.Sprite):
    def __init__(self, tetromino, block_pos):
        """
        Input: Đối tượng tetromino, tọa độ của khối vuông.
        Process: Khởi tạo các giá trị của đối tượng Block.
        Ouput: Không.
        """
        self.tetromino = tetromino
        super().__init__(self.tetromino.tetris.sprites_group)
        self.block_pos = vector(block_pos)
        self.image = tetromino.image
        self.rect = self.image.get_rect()
        self.rect.topleft = self.block_pos * BLOCK_SIZE
        self.alive = True
        self.create_block_sfx()


    def create_block_sfx(self):
        """
        Input: Không.
        Process: Tạo các giá trị cho hiệu ứng xóa hàng.
        Ouput: Không.
        """
        img_index = random.randint(0, 16)
        image_path = os.path.join(SOURCES_FILE_DIRECTORY, f'images/effect/star_{img_index}.png')
        self.sfx_image = pg.image.load(image_path).convert_alpha()
        # self.sfx_image.set_alpha(160)
        self.sfx_speed = random.uniform(0.1, 0.8)
        self.sfx_cycles = random.randrange(6, 12)
        self.cycle_counter = 0


    def sfx_end_time(self):
        """
        Input: Không.
        Process: Tính toán thời gian kết thúc hiệu ứng.
        Ouput: Giá trị boolean.
        """
        if self.tetromino.tetris.app.effect_trigger:
            self.cycle_counter += 1
            if self.cycle_counter > self.sfx_cycles:
                self.cycle_counter = 0
                return True


    def sfx_run(self):
        """
        Input: Không.
        Process: Chạy hiệu ứng bằng cách gán các giá trị mới cho Block bao gồm hình ảnh và tọa độ.
        Ouput: Không.
        """
        self.image = self.sfx_image
        self.block_pos.y -= self.sfx_speed
        self.image = pg.transform.rotate(self.image, pg.time.get_ticks() * self.sfx_speed)


    def is_alive(self):
        """
        Input: Không.
        Process: Kiểm tra xem đối tượng còn hoạt động không (Tức là còn nằm trong ma trận không).
        Ouput: Không.
        """
        if not self.alive:
            if not self.sfx_end_time():
                self.sfx_run()
            else:
                self.kill()


    def set_rect_topleft(self):
        """
        Input: Không.
        Process: Gán giá trị tọa độ của block vào cho group.
        Ouput: Không.
        """
        self.rect.topleft = self.block_pos * BLOCK_SIZE


    def set_block_pos(self, block_pos):
        """
        Input: Tọa độ block.
        Process: Cập nhật giá trị tọa độ của block.
        Ouput: Không.
        """
        self.block_pos = block_pos


    def is_collide(self, checking_pos):
        """
        Input: Tọa độ block.
        Process: Kiểm tra xem tọa độ của block có hợp lệ không.
        Ouput: Giá trị boolean
        """
        x, y = int(checking_pos.x), int(checking_pos.y)
        is_above = y < 0
        if 0 <= x < TETRIS_COLS and y < TETRIS_ROWS and (is_above or not self.tetromino.tetris.tetris_matrix[x][y]):
            return False
        return True


    def update(self):
        """
        Input: Không.
        Process: Cập nhật lại tọa độ của block trong group và kiểm tra xem block còn hoạt động không.
        Ouput: Không.
        """
        self.set_rect_topleft()
        self.is_alive()


    # Chỉ dùng để vẽ hàng chờ tetromino
    def draw_block(self, surface, coordinate_X, coordinate_Y, block_size):
        """
        Input: Surface, tọa độ x, y (tọa độ pixel, không phải tọa độ trên ma trận), kích thước khối vuông.
        Process: Vẽ ra một khối vuông vào surface được truyền vào.
        Ouput: Không.
        """
        pg.draw.rect(surface, WHITE, (coordinate_X, coordinate_Y, block_size, block_size))


    # Chỉ dùng để vẽ bóng đổ cho tetromino
    def draw_block_image(self, surface, image_path, coordinate_X, coordinate_Y, image_size_width, image_size_height):
        """
        Input: Surface, đường dẫn ảnh, tọa độ x, y (tọa độ pixel, không phải tọa độ trên ma trận), chiều rộng ảnh, chiều cao ảnh.
        Process: Vẽ ra hình ảnh đã được làm mờ của một khối vuông.
        Ouput: Không.
        """
        block_image = self.tetromino.tetris.load_image(image_path, image_size_width, image_size_height)
        block_image.set_alpha(150)
        surface.blit(block_image, (coordinate_X, coordinate_Y))

    