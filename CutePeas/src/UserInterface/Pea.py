import pygame.transform as xform

class Pea:
    def __init__(self, img):
        self.image = img
        self.rect = self.__getRect()
        self.rotateAngle = 0
        self.rotateIncrement = 20
        #self.node = initNode
        #self.prevNode = None
        
        self.listeners = []
    
    def switchNode(self, newNode):
        self.node = newNode
    
    def __getRect(self):
        return self.image.get_rect().move((60, 60))
        
    def __restoreImage(self):
        self.image = self.originalImage
        self.rect = self.__getRect()
        
    def __animate(self):
        center = self.rect.center
        self.originalImage = self.image
        self.rotateAngle += self.__getRotateIncrement()
        self.image = xform.rotate(self.image, self.rotateAngle)
        if self.rotateAngle >= 360 or self.rotateAngle <= -360:
            self.rotateAngle = 0
        self.rect = self.image.get_rect(center=center)
        
    def __getRotateIncrement(self):
        # based on node return either positive or negative increment
        # for now just randomise direction
        import random
        if random.randint(-2,2) < 0:
            return -(self.rotateIncrement)
        return self.rotateIncrement
        
    def render(self, screen):
        self.__animate()
        screen.blit(self.image, self.rect)
        # Restoring is needed for rotations (animate)
        self.__restoreImage()
    
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
        
        