from Images import images
import math
import Animation
from PathFinding.NodeGraph import *
from Constants import *

GHOST_TIMER_INIT = 2999
DONE_GHOSTING_IN_EVENT = "Done Ghosting In Event"
DONE_GHOSTING_OUT_EVENT = "Done Ghosting Out Event"

class Block:
    def __init__(self, ghostingImage= None, displayImage = None):
        if ghostingImage != None:
            self.ghostingImage = images[ghostingImage]
        if displayImage != None:
            self.image = images[displayImage]
        self.pos = (0,0)
        self.ghostingIn = False
        self.ghostingOut = False
        self.resetTimer()
        self.geom = None
        self.flagPlaced = False
        
    def dispose(self):
        pass
        
    def createNodes(self):
        print "block xy="+str(self.pos[X])+" " +str(self.pos[Y])
        x = self.pos[X]
        y = self.pos[Y] + BLOCK_Y_OVERLAP
        nodes = [
                 CornerNode((x, y), self),
                 FaceNode((x+BLOCK_WIDTH/2, y), self),
                 CornerNode((x+BLOCK_WIDTH, y), self),
                 FaceNode((x+BLOCK_WIDTH, y + BLOCK_HEIGHT/2), self),
                 CornerNode((x+BLOCK_WIDTH, y + BLOCK_HEIGHT), self),
                 FaceNode((x+BLOCK_WIDTH/2, y + BLOCK_HEIGHT), self),
                 CornerNode((x, y + BLOCK_HEIGHT), self),
                 FaceNode((x, y + BLOCK_HEIGHT/2), self)]
        loopNodes(nodes)
        return nodes
    
    def getPoints(self):
        x = self.pos[X]
        y = self.pos[Y] + BLOCK_Y_OVERLAP
        points = [(x,y),
                  (x+BLOCK_WIDTH, y), 
                  (x+BLOCK_WIDTH, y+BLOCK_HEIGHT), 
                  (x, y+BLOCK_HEIGHT)]
        return points
    
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
            screen.blit(self.ghostingImage, (self.pos[X], self.pos[Y]))
            ghostTimerImage = images[str(int(math.floor(self.ghostTimer/1000)+1))]
            screen.blit(ghostTimerImage, (self.pos[X]+35, self.pos[Y]+25))
        else:
            screen.blit(self.image, (self.pos[X], self.pos[Y]))
        
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
    
    def isDeletable(self):
        return self.flagPlaced

class LeftRampBlock(Block):
    def __init__(self, ghostingImage= None, displayImage = None):
        Block.__init__(self, ghostingImage, displayImage)
        
    def createNodes(self):
        print "block xy="+str(self.pos[X])+" " +str(self.pos[Y])
        x = self.pos[X]
        y = self.pos[Y] + BLOCK_Y_OVERLAP
        nodes = [CornerNode((x, y + BLOCK_HEIGHT), self),
                 FaceNode((x+BLOCK_WIDTH/2, y + BLOCK_HEIGHT/2), self),
                 CornerNode((x+BLOCK_WIDTH, y), self),
                 FaceNode((x+BLOCK_WIDTH, y + BLOCK_HEIGHT/2), self),
                 CornerNode((x+BLOCK_WIDTH, y + BLOCK_HEIGHT), self),
                 FaceNode((x+BLOCK_WIDTH/2, y + BLOCK_HEIGHT), self)]
        loopNodes(nodes)
        return nodes
    
    def getPoints(self):
        x = self.pos[X]
        y = self.pos[Y] + BLOCK_Y_OVERLAP
        points = [(x,y+BLOCK_HEIGHT), (x+BLOCK_WIDTH, y+BLOCK_HEIGHT), (x+BLOCK_WIDTH, y) ]
        return points

class RightRampBlock(Block):
    def __init__(self, ghostingImage= None, displayImage = None):
        Block.__init__(self, ghostingImage, displayImage)
        
    def createNodes(self):
        print "block xy="+str(self.pos[X])+" " +str(self.pos[Y])
        x = self.pos[X]
        y = self.pos[Y] + BLOCK_Y_OVERLAP
        nodes = [CornerNode((x, y), self),
                 FaceNode((x+BLOCK_WIDTH/2, y + BLOCK_HEIGHT/2), self),
                 CornerNode((x+BLOCK_WIDTH, y + BLOCK_HEIGHT), self),
                 FaceNode((x+BLOCK_WIDTH/2, y + BLOCK_HEIGHT), self),
                 CornerNode((x, y + BLOCK_HEIGHT), self),
                 FaceNode((x, y + BLOCK_HEIGHT/2), self)]
        loopNodes(nodes)
        return nodes
    
    def getPoints(self):
        x = self.pos[X]
        y = self.pos[Y] + BLOCK_Y_OVERLAP
        points = [(x,y), (x+BLOCK_WIDTH, y+BLOCK_HEIGHT), (x, y+BLOCK_HEIGHT) ]
        return points

def verticalSurface(pos):
    return Physics.QuickPhysics.VerticalSurface(pos)

def horizontalSurface(pos):
    return Physics.QuickPhysics.HorizontalSurface(pos)

def diagonalSurface(left, right):
    return Physics.QuickPhysics.DiagonalSurface(left, right)