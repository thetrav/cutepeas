import pygame.font

pygame.font.init()

FONT_SIZE = 30
fonts = {
         "DEFAULT_FONT" : pygame.font.Font('freesansbold.ttf', FONT_SIZE),
         "TITLE_FONT" : pygame.font.Font('freesansbold.ttf', 50),
         "NODE_FONT" : pygame.font.Font('freesansbold.ttf', 10),
         "PEA_FONT" : pygame.font.Font('freesansbold.ttf', 8),
         }

antiAlias = True

def renderText(text, pixelPos, screen, color=(0,0,0), font = "DEFAULT_FONT"):
    surface = fonts[font].render(text, antiAlias, color)
    screen.blit(surface, pixelPos)
    
