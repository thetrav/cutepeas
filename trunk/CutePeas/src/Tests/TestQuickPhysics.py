import pygame, sys
from Physics.QuickPhysics import *
import Constants
from Constants import *
from pygame.locals import *
from UserInterface.Block import Block, LeftRampBlock, RightRampBlock

class Game:
    def __init__(self):
        self.window = pygame.display.set_mode((800,600))
        self.screen = pygame.display.get_surface()
        
        self.background = pygame.Surface(self.screen.get_size()).convert()
        
        self.background.fill((50,50,50))
        
        pygame.display.set_caption('Cute Peas - Physics Prototype')

        self.physManager = physicsManagerWithBorders()
        block = Block()
        block.x = 400
        block.y = 400
        self.physManager.addSurfaces(block.createSurfaces())
        
        leftRamp = LeftRampBlock()
        leftRamp.x = 100
        leftRamp.y = 400
        self.physManager.addSurfaces(leftRamp.createSurfaces())
        
        rightRamp = RightRampBlock()
        rightRamp.x = 600
        rightRamp.y = 400
        self.physManager.addSurfaces(rightRamp.createSurfaces())
        
        self.pea = TestPea([210,100], [0.5, 0], self.physManager)
        Constants.DRAW_HIT_BOXES = True
    
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