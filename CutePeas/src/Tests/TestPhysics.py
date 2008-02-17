import pygame, sys
import Physics

from pygame.locals import *

class Game:
    def __init__(self):
        self.window = pygame.display.set_mode((800,600))
        self.screen = pygame.display.get_surface()
        
        self.background = pygame.Surface(self.screen.get_size()).convert()
        
        self.background.fill((50,50,50))
        
        pygame.display.set_caption('Cute Peas - Physics Prototype')
    
    def handleInput(self, events):
        for event in events:
            if event.type == QUIT:
                print 'Goodbye!'
                sys.exit(0)
            #else :
                #self.userInterface.handleEvent(event)
    
    def render(self, screen):
        
        #screen.blit(background, (0,0))
        #self.button.render(screen)
        self.physManager.render(screen)       
        
        pygame.display.flip()
        
    def main(self):
        
        self.physManager = Physics.PhysicsManager()
        position = Physics.Vector(50, 50)         
        self.physManager.addBlock( position , BlockType['standard'])
        
        while True:
            self.handleInput(pygame.event.get())
            self.render(self.screen)
        
Game().main()