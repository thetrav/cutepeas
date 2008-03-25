from Images import images
import math
import Animation
from PathFinding.NodeGraph import *
from Constants import *
import Physics.QuickPhysics

GHOST_TIMER_INIT = 2999
DONE_GHOSTING_IN_EVENT = "Done Ghosting In Event"
DONE_GHOSTING_OUT_EVENT = "Done Ghosting Out Event"

class Block:
    def __init__(self, ghostingImage= None, displayImage = None):
        if ghostingImage != None:
            self.ghostingImage = images[ghostingImage]
        if displayImage != None:
            self.image = images[displayImage]
        self.x = 0
        self.y = 0
        self.ghostingIn = False
        self.ghostingOut = False
        self.resetTimer()
        
    def createNodes(self):
        print "block xy="+str(self.x)+" " +str(self.y)
        x = self.x
        y = self.y + BLOCK_Y_OVERLAP
        nodes = [
                 CornerNode((x, y)),
                 FaceNode((x+BLOCK_WIDTH/2, y)),
                 CornerNode((x+BLOCK_WIDTH, y)),
                 FaceNode((x+BLOCK_WIDTH, y + BLOCK_HEIGHT/2)),
                 CornerNode((x+BLOCK_WIDTH, y + BLOCK_HEIGHT)),
                 FaceNode((x+BLOCK_WIDTH/2, y + BLOCK_HEIGHT)),
                 CornerNode((x, y + BLOCK_HEIGHT)),
                 FaceNode((x, y + BLOCK_HEIGHT/2))]
        loopNodes(nodes)
        return nodes
    
    def createSurfaces(self):
        x = self.x
        y = self.y + BLOCK_Y_OVERLAP
        return [verticalSurface([x,y]),
                    verticalSurface(([x+BLOCK_WIDTH,y])),
                    horizontalSurface((x,y)),
                    horizontalSurface((x,y+BLOCK_HEIGHT))
                    ]
        
    
    def resetTimer(self):
        self.ghostTimer = GHOST_TIMER_INIT
    
    def ghostIn(self):
        self.resetTimer()
        self.ghostingOut = False
        self.ghostingIn = True
        Animation.animations.append(self)
        
    def ghostOut(self):
        self.resetTimer()
        self.ghostingIn = False
        self.ghostingOut = True
        Animation.animations.append(self)
    
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
        Event.fireEvent(DONE_GHOSTING_IN_EVENT, self)
    
    def doneGhostingOut(self):
        self.ghostingOut = False
        Animation.animations.remove(self)
        Event.fireEvent(DONE_GHOSTING_OUT_EVENT, self)

def verticalSurface(pos):
    return Physics.QuickPhysics.VerticalSurface(pos)

def horizontalSurface(pos):
    return Physics.QuickPhysics.HorizontalSurface(pos)

