import pygame, sys
import Animation

from pygame.locals import *
from Images import *
from UserInterface.Button import Button
from UserInterface.UserInterface import UserInterface


MAX_FPS = 72



class Game:
    def __init__(self):
        self.window = pygame.display.set_mode((800,600))
        pygame.display.set_caption('Cute Peas - UI Prototype')
        
        self.screen = pygame.display.get_surface()
        loadImages()
    
    def handleInput(self, events):
        for event in events:
            if event.type == QUIT:
                print 'Goodbye!'
                sys.exit(0)
            else :
                self.userInterface.handleEvent(event)
    
    def render(self, screen):
        screen.blit(images["Background"], (0,0))
        screen.blit(images["Plate"], (5, 520))
        self.userInterface.render(screen)
        pygame.display.flip()
        
    def main(self):
        self.userInterface = UserInterface()
        clock = pygame.time.Clock()
        clock.tick() #initialise timer
        while True:
            self.handleInput(pygame.event.get())
            for animation in Animation.animations:
                animation.update(clock.get_time())
            self.render(self.screen)
            clock.tick(MAX_FPS)
        
Game().main()