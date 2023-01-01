import Shapes, random, Piece, Board, pygame, sys
from pygame.locals import *
from queue import Queue
pygame.init()

# screen = pygame.display.set_mode((600, 400))
# pixel_font = pygame.font.Font('fonts/PixelatedRegular.ttf', 50)
# text = pixel_font.render('This text for testing purpose!', 1, 'orange')
font_size = 40
    
font_surface = pygame.display.set_mode((font_size* 5, font_size * 3))
while 1:
    for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()    
                sys.exit()

    font_surface.fill('white')
    pixel_font = pygame.font.Font('fonts/PixelatedRegular.ttf', font_size)
    labels = []
    texts = ['Score', 'Level', 'Next level']

    for line in range(len(texts)):
        labels.append(pixel_font.render(texts[line], 1, 'orange'))

    font_surface.blit(labels[0], (10, 10))
    font_surface.blit(labels[1], (10, 50))
    font_surface.blit(labels[2], (10, 90))

    pygame.display.update()
