from Images import images
import math
import Animation

GHOST_TIMER_INIT = 3000

class Block:
    def __init__(self, ghostingImage, displayImage):
        self.ghostingImage = images[ghostingImage]
        self.image = images[displayImage]
        self.x = 0
        self.y = 0
        self.ghostingIn = False
        self.ghostingOut = False
        self.resetTimer()
        self.ghostingInListeners = []
        self.ghostingOutListeners = []
        
    def resetTimer(self):
        self.ghostTimer = GHOST_TIMER_INIT
    
    def ghostIn(self):
        self.resetTimer()
        self.ghostingOut = False
        self.ghostingIn = True
        Animation.animations.append(self)
        
    def ghostOut(self, listener):
        self.resetTimer()
        self.ghostingIn = False
        self.ghostingOut = True
        Animation.animations.append(self)
        self.ghostingOutListeners.append(listener)
    
    def render(self, screen):
        if self.isGhosting():
            screen.blit(self.ghostingImage, (self.x, self.y))
            ghostTimerImage = images[str(int(math.floor(self.ghostTimer/1000)+1))]
            screen.blit(ghostTimerImage, (self.x+35, self.y+25))
        else:
            screen.blit(self.image, (self.x, self.y))
        
    def isGhosting(self):
        return self.ghostingIn or self.ghostingOut
        
    def update(self, timeD):
        if self.isGhosting():
            self.ghostTimer = self.ghostTimer - timeD
            if self.ghostTimer <= 0:
                if self.ghostingIn:
                    self.doneGhostingIn()
                else:
                    self.doneGhostingOut()
    
    def doneGhostingIn(self):
        Animation.animations.remove(self)
        self.ghostingIn = False
        for listener in self.ghostingInListeners:
            listener.ghostedIn(self)
    
    def doneGhostingOut(self):
        self.ghostingOut = False
        Animation.animations.remove(self)
        for listener in self.ghostingOutListeners:
            listener.ghostedOut(self)
    