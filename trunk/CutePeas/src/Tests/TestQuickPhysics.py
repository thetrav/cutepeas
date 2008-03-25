import pygame, sys
from Physics.QuickPhysics import *
from Constants import *
from pygame.locals import *

class Game:
    def __init__(self):
        self.window = pygame.display.set_mode((800,600))
        self.screen = pygame.display.get_surface()
        
        self.background = pygame.Surface(self.screen.get_size()).convert()
        
        self.background.fill((50,50,50))
        
        pygame.display.set_caption('Cute Peas - Physics Prototype')

        self.physManager = PhysicsManager()
        surfaces = [
                    #VerticalSurface([200,200]),
                    #VerticalSurface([240,200]),
                    HorizontalSurface([160,280]),
                    HorizontalSurface([200,200])]
        self.physManager.addSurfaces(surfaces)
        
        self.pea = TestPea([210,100], [0, 0], self.physManager)
    
    def handleInput(self, events):
        for event in events:
            if event.type == QUIT:
                print 'Goodbye!'
                sys.exit(0)
    
    def render(self, screen):
        
        screen.blit(self.background, (0,0))
        self.physManager.render(screen)       
        self.pea.render(screen)
        pygame.display.flip()
        
    def main(self):
        clock = pygame.time.Clock()
        clock.tick() #initialise timer
        while True:
            self.handleInput(pygame.event.get())
            
            self.render(self.screen)
            self.pea.update(clock.get_time())
            clock.tick(MAX_FPS)
            
        
Game().main()