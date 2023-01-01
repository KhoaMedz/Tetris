import pygame
pygame.init()


class Score():
    def __init__(self, original_fall_frequency):
        self.score = 0
        self.level = 1
        self.score_to_reach_next_level = 2000
        self.original_fall_frequency = original_fall_frequency
        self.fall_frequency = self.original_fall_frequency

    def calculate_score(self, removed_line_num):
        num = 0
        for i in range(removed_line_num):
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
        if self.level > 1:
            self.fall_frequency = self.original_fall_frequency - (self.level * 0.075)


    def draw_score(self, surface_to_draw, coordinate_X, coordinate_Y, font_size, margin_x = 0, margin_y = 0):
        font_surface = pygame.Surface((font_size * 7, font_size * 4))
        font_surface.fill('white')
        pixel_font = pygame.font.Font('fonts/PixelatedRegular.ttf', font_size)
        labels = []
        texts = [f'Score:    {self.score}', f'Level:    {self.level}', f'Next level:    {self.score_to_reach_next_level}', f'Fall frequency:    {self.fall_frequency} s']

        for line in range(len(texts)):
            labels.append(pixel_font.render(texts[line], 1, 'orange'))

        font_surface.blit(labels[0], (margin_x, margin_y + font_size * 0))
        font_surface.blit(labels[1], (margin_x, margin_y + font_size * 1))
        font_surface.blit(labels[2], (margin_x, margin_y + font_size * 2))
        font_surface.blit(labels[3], (margin_x, margin_y + font_size * 3))

        surface_to_draw.blit(font_surface, (coordinate_X, coordinate_Y))


    def get_score(self):
        return self.score


    def get_level(self):
        return self.level


    def set_score(self, score, is_added = False):
        if is_added == True:
            self.score += score
        else:
            self.score = score


    def set_level(self, level, is_added = False):
        if is_added == True:
            self.level += level
        else:
            self.level = level

    def get_fall_frequency(self):
        return self.fall_frequency