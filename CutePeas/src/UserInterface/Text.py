import pygame.font

pygame.font.init()

FONT_SIZE = 30
fonts = {
         "DEFAULT_FONT" : pygame.font.Font(None, FONT_SIZE),
         "TITLE_FONT" : pygame.font.Font(None, 50),
         "NODE_FONT" : pygame.font.Font(None, 20)
         }

antiAlias = True

def renderText(text, pos, screen, color=(0,0,0), font = "DEFAULT_FONT"):
    surface = fonts[font].render(text, antiAlias, color)
    screen.blit(surface, pos)
    
