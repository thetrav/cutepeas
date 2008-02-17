import pygame, sys

from pygame.locals import *
from Images import *
from UserInterface.Button import Button
from UserInterface.UserInterface import UserInterface

class Game:
    def __init__(self):
        self.window = pygame.display.set_mode((800,600))
        pygame.display.set_caption('Cute Peas - Peas Animation')
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
        self.userInterface.render(screen)
        pygame.display.flip()
        
    def main(self):
        self.userInterface = UserInterface()
        clock = pygame.time.Clock()
        while True:
            self.handleInput(pygame.event.get())
            clock.tick(50)
            self.render(self.screen)

if __name__ == "__main__":        
    Game().main()
