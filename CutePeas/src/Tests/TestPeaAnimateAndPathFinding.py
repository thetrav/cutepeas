import pygame, sys, os
import Animation, PeaAnimateAndPathFindingScreen

from pygame.locals import *
import Images
from UserInterface.Button import Button
from UserInterface.UserInterface import UserInterface

MAX_FPS = 20

class Game:
    def __init__(self):
        self.window = pygame.display.set_mode((800,600))
        pygame.display.set_caption('Cute Peas')
        self.screen = pygame.display.get_surface()
        Images.IMAGE_BASE_DIR = os.path.join('..', '..', 'data', 'images')
        Images.loadImages()
    
    def handleInput(self, events):
        for event in events:
            if event.type == QUIT:
                print 'Goodbye!'
                sys.exit(0)
            else :
                self.userInterface.handleEvent(event)
    
    def render(self, screen):
        self.level.render(screen)
        pygame.display.flip()
        
    def transition(self, newLevel):
        self.level.dispose()
        self.level = newLevel
        
    def main(self):
        self.userInterface = UserInterface()
        self.level = PeaAnimateAndPathFindingScreen.Screen(self.userInterface, self)
        clock = pygame.time.Clock()
        clock.tick() #initialise timer
        while True:
            self.handleInput(pygame.event.get())
            for animation in Animation.animations:
                animation.update(clock.get_time())
            self.render(self.screen)
            clock.tick(MAX_FPS)
        
Game().main()