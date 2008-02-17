import pygame, sys

from pygame.locals import *
from Images import *
from Button import Button

class Game:
    def __init__(self):
        self.window = pygame.display.set_mode((800,600))
        pygame.display.set_caption('Cute Peas - UI Prototype')
        
        self.screen = pygame.display.get_surface()
        
        self.images = {}
        
        cacheImage(self.images, "Background")
        cacheImage(self.images, "Gold-Ball")
        cacheImage(self.images, "Happy-Points")
    
    def handleInput(self, events):
        for event in events:
            if event.type == QUIT:
                print 'Goodbye!'
                sys.exit(0)
            elif event.type == KEYDOWN:
                pass
            elif event.type == MOUSEMOTION:
                self.button.mouseMotion(event)
            elif event.type == MOUSEBUTTONDOWN:
                self.button.mouseDown(event)
            elif event.type == MOUSEBUTTONUP:
                self.button.mouseUp(event)
    
    def render(self, screen):
        screen.blit(self.images["Background"], (0,0))
        self.button.render(screen)
        screen.blit(self.images["Gold-Ball"], (400,500))
        
        pygame.display.flip()
        
    def main(self):
        self.button = Button(loadImage("up"), loadImage("down"), 50, 50, 200, 200)
        
        while True:
            self.handleInput(pygame.event.get())
            self.render(self.screen)
        
Game().main()