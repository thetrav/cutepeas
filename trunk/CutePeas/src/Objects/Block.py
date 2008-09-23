import Event
import math
import Animation
import PathFinding.GateAndLink.Corner
import UserInterface.Scroll
from Images import images
from Constants import *
import Coordinates

GHOST_TIMER_INIT = 2999
DONE_GHOSTING_IN_EVENT = "Done Ghosting In Event"
DONE_GHOSTING_OUT_EVENT = "Done Ghosting Out Event"
NORMAL_BLOCK_BOUNCE = 2
SPRING_BLOCK_BOUNCE = 10
GEL_BLOCK_BOUNCE = 0.5

GEL_MAX_SURVIVABLE_VELOCITY_MOD = 4
SPRING_MAX_SURVIVABLE_VELOCITY_MOD = 1.8

TIMER_OFFSET_X = Coordinates.pixelsToOde(35)
TIMER_OFFSET_Y = Coordinates.pixelsToOde(25)

class Block:
    def __init__(self, ghostingImage= None, displayImage = None, bounce=NORMAL_BLOCK_BOUNCE, maxSurvivableVelocityMod = 1):
        if ghostingImage != None:
            self.ghostingImage = images[ghostingImage]
        if displayImage != None:
            self.image = images[displayImage]
        self.odePos = (0.0,0.0)
        self.ghostingIn = False
        self.ghostingOut = False
        self.resetTimer()
        self.geom = None
        self.flagPlaced = False
        self.bounce = bounce
        self.bouncePoints = 1000
        self.maxSurvivableVelocityMod = maxSurvivableVelocityMod
        
    def dispose(self):
        pass
    
    def getBouncePoints(self):
        return self.bouncePoints
        
    def createCorners(self):
        return PathFinding.GateAndLink.Corner.createBoxLinkedCorners(self.odePos)
        
    #points are used for creating trimeshes in ode physics manager
    def getPoints(self):
        x = self.odePos[X]
        y = self.odePos[Y] + BLOCK_Y_OVERLAP_ODE
        points = [(x,y,0),
                  (x+BLOCK_WIDTH_ODE, y,0), 
                  (x+BLOCK_WIDTH_ODE, y+BLOCK_HEIGHT_ODE,0), 
                  (x, y+BLOCK_HEIGHT_ODE,0)]
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
            UserInterface.Scroll.globalViewPort.blit(screen, self.ghostingImage, (self.odePos[X], self.odePos[Y]))
            ghostTimerImage = images[str(int(math.floor(self.ghostTimer/1000)+1))]
            UserInterface.Scroll.globalViewPort.blit(screen, ghostTimerImage, (self.odePos[X]+TIMER_OFFSET_X, self.odePos[Y]+TIMER_OFFSET_Y))
        else:
            UserInterface.Scroll.globalViewPort.blit(screen, self.image, self.odePos)
        
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
        
    def createCorners(self):
        return PathFinding.GateAndLink.Corner.createLeftRampLinkedCorners(self.odePos)

    #points are used for creating trimeshes in ode physics manager
    def getPoints(self):
        x = self.odePos[X]
        y = self.odePos[Y] + BLOCK_Y_OVERLAP_ODE
        points = [(x,y+BLOCK_HEIGHT_ODE,0), (x+BLOCK_WIDTH_ODE, y+BLOCK_HEIGHT_ODE,0), (x+BLOCK_WIDTH_ODE, y,0) ]
        return points

class RightRampBlock(Block):
    def __init__(self, ghostingImage= None, displayImage = None):
        Block.__init__(self, ghostingImage, displayImage)
        
    def createCorners(self):
        return PathFinding.GateAndLink.Corner.createRightRampLinkedCorners(self.odePos)
    
    #points are used for creating trimeshes in ode physics manager
    def getPoints(self):
        x = self.odePos[X]
        y = self.odePos[Y] + BLOCK_Y_OVERLAP_ODE
        points = [(x,y,0), (x+BLOCK_WIDTH_ODE, y+BLOCK_HEIGHT_ODE,0), (x, y+BLOCK_HEIGHT_ODE,0)]
        return points
