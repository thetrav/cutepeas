import pygame.transform as xform
import pygame.draw
import PathFinding.NodeGraph
import Constants
from Constants import *
import Event
import Physics.OdePhysics


NODE_TIMER = 200
FALL_END_TIMER = 2000
MIN_VEL = 0.001
FALLING_MODE = "falling"
JUMPING_MODE = "jumping"
CLIMBING_MODE = "climbing"

class Pea:
    def __init__(self, img, pos, nodeGraph, physics):
        self.image = img
        self.body = None
        self.nodeGraph = nodeGraph
        self.pos = pos
        self.setNode(self.nodeGraph.findNearestNode(self.pos))
        self.path = PathFinding.NodeGraph.findPath(self.currentNode)
        Event.addListener(EVENT_NODE_GRAPH_UPDATED, self)
        self.rect = self.__getRect()
        self.rotateAngle = 0
        self.rotateIncrement = 90
        self.rotated = False
        self.listeners = []
        self.reverse = False
        self.timeStandingStill = FALL_END_TIMER
        self.timeUntilNextNode = 0
        self.mode = FALLING_MODE
        self.physicsManager = physics
    
    def dispose(self):
        Event.removeListener(EVENT_NODE_GRAPH_UPDATED, self)

    def getNode(self):
        return self.currentNode
    
    def setNode(self, node):
        self.reverse = False
        self.currentNode = node
        self.pos = self.currentNode.pos
        self.timeUntilNextNode = NODE_TIMER
    
    def __getRect(self):
        return self.image.get_rect().move(self.pos)
        
    def __restoreImage(self):
        if self.rotated:
            self.image = self.originalImage
            self.rect = self.__getRect()
            self.rotated = False
    
    """Traverses the nodes"""
    def __switchNode(self):
        prev, next = self.__getPrevAndNextNodes()
        if next is None and prev is None:
            self.pos = self.currentNode.getPos() # nowhere new to move, poor claustrophobic pea :(
            return
        elif next is None:
            self.currentNode = prev
            self.__toggleReverse() # swap reversal altering next/prev semantics
        else:
            self.currentNode = next
        self.pos = self.currentNode.getPos()
    
    """
    returns a tuple of (prev, next) nodes.
    """
    def __getPrevAndNextNodes(self):
        next = self.currentNode.nextNode()
        prev = self.currentNode.prevNode()
        if self.reverse:
            return (next, prev) # swap order - moving backwards, next is referring to previous node.
        return (prev, next)
        
    def __toggleReverse(self):
        if self.reverse:
            self.reverse = False
        else:
            self.reverse = True
        
    def __animate(self):
        self.__rotate()
        #self.__switchNode()
        self.rect = self.rect.move(self.pos)
    
    def __rotate(self):
        center = self.rect.center
        self.originalImage = self.image
        self.rotateAngle += self.__getRotateIncrement()
        self.image = xform.rotate(self.image, self.rotateAngle)
        if self.rotateAngle >= 360 or self.rotateAngle <= -360:
            self.rotateAngle = 0
        self.rect = self.image.get_rect(center=center)
        self.rotated = True
        
    def __getRotateIncrement(self):
        if self.reverse:
            return self.rotateIncrement
        return -(self.rotateIncrement)
        
    def render(self, screen):
        screen.blit(self.image, (self.pos[X] - PEA_RADIUS, self.pos[Y] - PEA_RADIUS))
        # Restoring is needed for rotations
        self.__restoreImage()
        
        if Constants.DRAW_PATH:
            for node in self.path:
                node.render(screen, (255,255,0))
        
    def jump(self):
        self.pos = (self.pos[0], self.pos[1] - PEA_RADIUS+5)
        self.physicsManager.addPea(self)
        self.body.setLinearVel((1, -1, 0.0))
        self.mode = JUMPING_MODE
        self.timeStandingStill = FALL_END_TIMER
        
    def update(self, timeD):
        if self.mode == CLIMBING_MODE :
            self.timeUntilNextNode -= timeD
            if self.timeUntilNextNode < 0:
                self.setNode(self.path.pop(0))
                if len(self.path) == 0:
                    self.jump()
        else:
            self.pos = Physics.OdePhysics.getPixelPos(self.body.getPosition())
            vel = self.body.getLinearVel()
            if vel[0] + vel[1] > MIN_VEL:
                self.timeStandingStill = FALL_END_TIMER
            else:
                self.timeStandingStill -= timeD
            
            if self.timeStandingStill <= 0:
                self.mode = CLIMBING_MODE
                self.physicsManager.removePea(self)
                self.setNode(self.nodeGraph.findNearestNode(self.pos))
                self.path = PathFinding.NodeGraph.findPath(self.currentNode)
                
        #physics updates are now handled by a third party library that does all entities at once
        #pea update still exists for non physics related animations
        #self.physics.update(self, timeD)
        
        #self.timeUntilNextNode -= timeD
        #if self.timeUntilNextNode < 0:
        #    self.setNode(self.path.pop(0))
        #    if len(self.path) == 0:
        #        self.path = PathFinding.NodeGraph.findPath(self.currentNode)
        #self.__animate()
        #To Kamal.  In case I don't see you again the update function is called on every member of the Animation.animations list once per frame with the elapsed time since the previous frame.
        # this allows for very smooth animations regardless of the users actual frame rate.  It is important to keep it all synched to the one timer for a number of reasons best not discussed here
        # --Trav 
        
    def eventFired(self, eventId, source):
        if eventId == EVENT_NODE_GRAPH_UPDATED:
            if not source.hasNodeAt(self.currentNode.pos):
                self.currentNode = source.findNearestNode(self.currentNode.pos)
            self.path = PathFinding.NodeGraph.findPath(self.currentNode)
    
    def fireDeath(self):
        for listener in self.listeners:
            listener.deathFired(self)
    
    def fireTrap(self):
        for listener in self.listeners:
            listener.trapFired(self)
        
    def fireJump(self):
        for listener in self.listeners:
            listener.jumpFired(self)
        
    def fireLanded(self):
        for listener in self.listeners:
            listener.landedFired(self)
            
    def addListener(self, listener):
        self.listeners.append(listener)
        
        