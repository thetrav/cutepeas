import pygame, sys
from pygame.locals import *
from PathFinding.GateAndLink.Graph import *
from PathFinding.GateAndLink.Corner import *
from PathFinding.GateAndLink.Path import *
from Constants import *
import Constants

window = pygame.display.set_mode((800,600))
pygame.display.set_caption('Cute Peas')
        
screen = pygame.display.get_surface()

graph = NodeGraph(9, 500)

def transPos(pos):
    return (X_OFFSET + pos[X] * BLOCK_WIDTH, 500-BLOCK_HEIGHT - pos[Y] * BLOCK_HEIGHT)

def addBox(pos):
    graph.addCorners(createBoxLinkedCorners(transPos(pos)))

def addLeftRamp(pos):
    graph.addCorners(createLeftRampLinkedCorners(transPos(pos)))    

def addRightRamp(pos):
    graph.addCorners(createRightRampLinkedCorners(transPos(pos)))  
    
addBox((0,0))
addLeftRamp((1,0))
addLeftRamp((1,1))
addBox((2,0))
addRightRamp((3,0))

addLeftRamp((4,3))
addRightRamp((5,3))
addLeftRamp((6,3))

addBox((7,4))
addBox((8,3))

def handleInput(events):
    for event in events:
        if event.type == QUIT:
            print 'Goodbye!'
            sys.exit(0)

clock = pygame.time.Clock()
clock.tick() #initialise timer
Constants.DRAW_NODES = True

gate = graph.findNearestNode((400,250))
path = findPath(gate)
print path
print SCREEN_HEIGHT

while True:
    handleInput(pygame.event.get())
    
    graph.render(screen)
    for node in path:
        pygame.draw.circle(screen, (255,0,255) , (node.gate.pos[X], node.gate.pos[Y]), 15, 3)
    pygame.draw.circle(screen, (0,255,0) , (gate.pos[X], gate.pos[Y]), 18, 3)
    pygame.display.flip()
    
    clock.tick(MAX_FPS)
            
print graph 