from Constants import *
import UserInterface.Scroll
import Images
import Event

JUMPS_PER_FLAG = 3
POLE_OFFSET_X = -Coordinates.pixelsToOde(15)
POLE_OFFSET_Y = -Coordinates.pixelsToOde(60)

FLAG_OFFSET_X = Coordinates.pixelsToOde(-7)
FLAG_OFFSET_Y = -Coordinates.pixelsToOde(25)
FLAG_MAX_HEIGHT = Coordinates.pixelsToOde(30)

class Flag:
    def __init__(self, pos):
        self.poleImage = Images.images["Flag-Pole"]
        self.flagImage = None
        self.pos = pos
        self.jumps = 0
        self.currentPea = None
        
    def render(self, screen):
        polePos = (self.pos[X]+POLE_OFFSET_X, self.pos[Y]+POLE_OFFSET_Y)
        UserInterface.Scroll.globalViewPort.blit(screen, self.poleImage, polePos)
        
        if self.flagImage:
            flagPos = (self.pos[X] + FLAG_OFFSET_X, self.pos[Y] + FLAG_OFFSET_Y + self.flagHeight())
            UserInterface.Scroll.globalViewPort.blit(screen, self.flagImage, flagPos)
    
    def flagHeight(self):
        return -FLAG_MAX_HEIGHT * self.jumps / JUMPS_PER_FLAG
    
    def startJump(self, pea):
        self.currentPea = pea
    
    def endJump(self, safe):
        self.currentPea = None
        if safe:
            self.flagImage = Images.images["Flag-Good"]
            self.jumps += 1
        else:
            self.flagImage = Images.images["Flag-Bad"]
            self.jumps = JUMPS_PER_FLAG
        Event.fireEvent(EVENT_NODE_GRAPH_UPDATED, self)
    
    def isComplete(self):
        return self.jumps >= JUMPS_PER_FLAG
    
    def peaJumping(self):
        return self.currentPea
    
    def isJumpable(self):
        jumpable = not (self.isComplete() or self.peaJumping())
        print 'isComplete',self.isComplete()
        print 'peaJumping', self.peaJumping()
        print 'isjumpable',jumpable
        return jumpable
    
