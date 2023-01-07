from game_settings import *
from tetris import *

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
        self.tetris = Tetris(self)
        pg.display.set_caption('Tetris')
        self.background_image = self.load_image()
        self.fps_clock = pg.time.Clock()
        self.set_timer()
        

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
        image_path = os.path.join(SOURCES_FILE_DIRECTORY, 'images/background/main_background.png')
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


    def run(self):
        """
        Input: Không.
        Process: Chạy vòng lặp chính của game.
        Ouput: Không.
        """
        while 1:
            self.check_events()
            self.update()
            self.draw()

