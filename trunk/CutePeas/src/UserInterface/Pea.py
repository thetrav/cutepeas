import pygame.transform as xform
from PathFinding import Node

class Pea:
    def __init__(self, img, initnode):
        self.image = img
        self.setNode(initnode)
        self.pos = initnode.getPos()
        self.rect = self.__getRect()
        self.rotateAngle = 0
        self.rotateIncrement = 90
        self.rotated = False
        self.listeners = []
        self.reverse = False

    def getNode(self):
        return self.currentNode
    
    def setNode(self, node):
        self.reverse = False
        self.currentNode = node
        self.pos = self.currentNode.getPos()
    
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
        self.__switchNode()
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
        self.__animate()
        screen.blit(self.image, self.pos)
        # Restoring is needed for rotations
        self.__restoreImage()
        
    def update(self, timeD):
        #self.__animate()
        #self.__restoreImage()
        # to the.trav - if you're messing with events and what not, could you please also update
        # PeaAnimateAndPathFindingScreen.Screen (which is basically a much simpler test harness
        # version of the TitleScreen) so it works with the new update() mechanism, or let me 
        # know the idea behind it - I reverted the pea's animation back (to render()) temporarily
        # - was too lazy to understand the new mechanism :P.
        pass
    
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
        
        