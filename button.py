from game_settings import *

class Button():
    def __init__(self, image_path, image_width, image_height, mouse_pos, draw_pos):
        self.draw_pos_x = draw_pos[0]
        self.draw_pos_y = draw_pos[1]
        self.mouse_pos_x = mouse_pos[0]
        self.mouse_pos_y = mouse_pos[1]
        self.image_width = image_width
        self.image_height = image_height
        image_path = os.path.join(SOURCES_FILE_DIRECTORY, image_path)
        self.button_image = pg.transform.scale(pg.image.load(image_path).convert_alpha(), (self.image_width, self.image_height))
        self.button_rect = self.button_image.get_rect()
        self.button_rect.center = self.draw_pos_x, self.draw_pos_y


    def blit_to_surface(self, surface):
        surface.blit(self.button_image, self.button_rect)

    
    def is_mouse_collide(self):
        if self.mouse_pos_x in range (self.button_rect.left, self.button_rect.right) and self.mouse_pos_y in range(self.button_rect.top, self.button_rect.bottom):
            return True
        return False

    def hover(self):
        self.button_image = pg.transform.scale(self.button_image, (self.image_width + 15, self.image_height + 15))
        self.button_rect = self.button_image.get_rect()
        self.button_rect.center = self.draw_pos_x, self.draw_pos_y