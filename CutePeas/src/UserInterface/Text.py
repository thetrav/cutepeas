import pygame.font

pygame.font.init()

FONT_SIZE = 30

font = pygame.font.Font(None, FONT_SIZE)

antiAlias = True

def renderText(text, pos, screen, color=(0,0,0)):
    surface = font.render(text, antiAlias, color)
    screen.blit(surface, pos)
    
