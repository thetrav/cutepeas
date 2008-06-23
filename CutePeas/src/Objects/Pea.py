from Constants import *
import pygame.transform as xform
import pygame.draw
import PathFinding.NodeGraph
import Constants
import Event
import Coordinates
import Animation
import Images
import Particles

NODE_TIMER = 200
FALL_END_TIMER = 2000
MIN_VEL = 0.001
CELEBRATION_TIMER = 5000

def workOutJumpDirection(node):
    for linkedNode in node.linkedNodes:
        if node.pos[0] != linkedNode.pos[0]:
            return -1 if node.pos[0] < linkedNode.pos[0] else 1

def climbAnimation(pea, timeD):
    pea.timeUntilNextNode -= timeD
    if pea.timeUntilNextNode < 0:
        pea.previousNode = pea.currentNode
        pea.setNode(pea.path.pop(0))
        if len(pea.path) == 0:
            if pea.currentNode.isJumpable():
                pea.jump()
            else:
                pea.path = PathFinding.NodeGraph.findPath(pea.currentNode)
            
def jumpAnimation(pea, timeD):
    pea.pos = Coordinates.odePosToPixelPos(pea.body.getPosition())
    vel = pea.body.getLinearVel()
    if vel[0] + vel[1] > MIN_VEL:
        pea.timeStandingStill = FALL_END_TIMER
    else:
        pea.timeStandingStill -= timeD
    
    if pea.timeStandingStill <= 0:
        pea.endJump()
        
def celebrateAnimation(pea, timeD):
    pea.timeCelebrating -= timeD
    
    if pea.timeCelebrating <= 0:
        pea.endCelebration()

class Pea:
    def __init__(self, pos, nodeGraph, physics):
        self.image = Images.images["Pea-Standard"]
        self.body = None
        self.nodeGraph = nodeGraph
        self.pos = pos
        self.setNode(self.nodeGraph.findNearestNode(self.pos))
        self.path = PathFinding.NodeGraph.findPath(self.currentNode)
        Event.addListener(EVENT_NODE_GRAPH_UPDATED, self)
        self.rotateAngle = 0
        self.rotateIncrement = 90
        self.rotated = False
        self.listeners = []
        self.reverse = False
        self.timeStandingStill = FALL_END_TIMER
        self.timeUntilNextNode = 0
        self.timeCelebrating = CELEBRATION_TIMER
        self.physicsManager = physics
        self.playAnimation = climbAnimation
        self.flags = []
        self.currentFlag = None
        self.previousNode = None
        Animation.animations.append(self)
        self.particleSystem = Particles.ParticleSystem()
    
    def dispose(self):
        Event.removeListener(EVENT_NODE_GRAPH_UPDATED, self)
        Animation.animations.remove(self)

    def getNode(self):
        return self.currentNode
    
    def setNode(self, node):
        self.reverse = False
        self.currentNode = node
        self.pos = self.currentNode.pos
        self.timeUntilNextNode = NODE_TIMER
            
    def render(self, screen):
        if Constants.DRAW_PATH:
            for node in self.path:
                node.render(screen, (255,255,0))
        if self.playAnimation == celebrateAnimation:
            self.renderCelebration(screen)
        self.particleSystem.render(screen)
        screen.blit(self.image, (self.pos[X] - PEA_RADIUS, self.pos[Y] - PEA_RADIUS))
        
    def renderCelebration(self, screen):
        ninjaPos = (self.pos[X] - 36, self.pos[Y] - 60)
        screen.blit(Images.images["Alert-Ninja"], ninjaPos)
        
    def jump(self):
        if self.currentNode.flag != None:
            self.currentFlag = self.currentNode.flag 
        else :
            self.currentFlag = PathFinding.NodeGraph.Flag(self.pos, 5)
            self.nodeGraph.placeFlag(self.currentFlag, self.currentNode)
        self.pos = (self.pos[0], self.pos[1] - PEA_RADIUS+5)
        self.physicsManager.addPea(self)
        self.body.setLinearVel((workOutJumpDirection(self.currentNode), -1, 0.0))
        self.playAnimation = jumpAnimation
        self.timeStandingStill = FALL_END_TIMER
        
    def update(self, timeD):
        self.playAnimation(self, timeD)
        self.particleSystem.update(timeD)
                
    def eventFired(self, eventId, source):
        if eventId == EVENT_NODE_GRAPH_UPDATED:
            if not source.hasNodeAt(self.currentNode.pos):
                self.currentNode = source.findNearestNode(self.currentNode.pos)
            self.path = PathFinding.NodeGraph.findPath(self.currentNode)
            
    def endJump(self):
        self.physicsManager.removePea(self)
        self.currentFlag.jumpDone(self)
        self.currentFlag = None
        self.beginCelebration()
        
    def beginCelebration(self):
        self.timeCelebrating = CELEBRATION_TIMER
        self.playAnimation = celebrateAnimation
        self.image = Images.images["Pea-Happy"]
        self.particleSystem.addEmitter(Particles.ExplodeEmitter(self.pos, CELEBRATION_TIMER))
    
    def endCelebration(self):
        self.image = Images.images["Pea-Standard"]
        self.beginClimb()
        
    def beginClimb(self):
        self.playAnimation = climbAnimation
        self.setNode(self.nodeGraph.findNearestNode(self.pos))
        self.path = PathFinding.NodeGraph.findPath(self.currentNode)
