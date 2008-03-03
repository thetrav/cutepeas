from PathFinding.AddNodes import *

import pygame, sys
import Animation, TitleScreen

from pygame.locals import *
from Images import *
from UserInterface.Button import Button
from UserInterface.UserInterface import UserInterface


MAX_FPS = 72

class TestLevel():
    def __init__(self):
        pass
    
    def render(self, screen):
        pass

class Game:
    def __init__(self):
        self.window = pygame.display.set_mode((800,600))
        pygame.display.set_caption('Cute Peas')
        
        self.screen = pygame.display.get_surface()
        loadImages()
        
        
        self.nodes = NodeGraph(5)
        self.toggle = True
        
    def addNodes(self):
        self.toggle = False
        nodes = [
                 CornerNode((2,0)),
                 FaceNode((3,0)),
                 CornerNode((4,0)),
                 FaceNode((4,1)),
                 CornerNode((4,2)),
                 FaceNode((3,2)),
                 CornerNode((2,2)),
                 FaceNode((2,1))]
        prev = None
        for node in nodes:
            if prev:
                prev.linkNode(node)
                node.linkNode(prev)
            prev = node
        nodes[0].linkNode(nodes[7])
        nodes[7].linkNode(nodes[0])
        self.nodes.addNodes(nodes)
    
    def handleInput(self, events):
        for event in events:
            if event.type == KEYDOWN and self.toggle:
                self.addNodes();
            if event.type == QUIT:
                print 'Goodbye!'
                sys.exit(0)
            else :
                self.userInterface.handleEvent(event)
    
    def render(self, screen):
        self.level.render(screen)
        
        screen.blit(images["Background"], (0,0))
        self.nodes.render(screen)
        pygame.display.flip()
        
    def transition(self, newLevel):
        self.level.dispose()
        self.level = newLevel
        
    def main(self):
        self.userInterface = UserInterface()
        self.level = TestLevel()
        clock = pygame.time.Clock()
        clock.tick() #initialise timer
        while True:
            self.handleInput(pygame.event.get())
            for animation in Animation.animations:
                animation.update(clock.get_time())
            self.render(self.screen)
            clock.tick(MAX_FPS)
        
Game().main()