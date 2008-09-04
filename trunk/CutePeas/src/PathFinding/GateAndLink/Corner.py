from Constants import *
from PathFinding.GateAndLink.PackageConstants import *
import PathFinding.GateAndLink.Link
import UserInterface.Scroll


def topLeftPos(pos):
    return (pos[X], pos[Y])

def topRightPos(pos):
    return (pos[X] + BLOCK_WIDTH, pos[Y])

def bottomLeftPos(pos):
    return (pos[X], pos[Y] + BLOCK_HEIGHT)

def bottomRightPos(pos):
    return (pos[X] + BLOCK_WIDTH, pos[Y] + BLOCK_HEIGHT)

def createLeftRampLinkedCorners(pos):
    #leftRamp link
        #bottom left gate is top right corner - 1
    bottomLeftGateTopRightCorner = Corner(bottomLeftPos(pos), TOP_RIGHT)
        #top right gate is bottom left corner - 2
    topRightGateBottomLeftCorner = Corner(topRightPos(pos), BOTTOM_LEFT)
    PathFinding.GateAndLink.Link.LeftRampLink(bottomLeftGateTopRightCorner, topRightGateBottomLeftCorner)
    #right Link
        #top right gate is bottom left corner - 2
        #bottom right gate is top left corner - 3
    bottomRightGateTopLeftCorner = Corner(bottomRightPos(pos), TOP_LEFT)
    PathFinding.GateAndLink.Link.RightLink(bottomRightGateTopLeftCorner, topRightGateBottomLeftCorner)
    return (bottomLeftGateTopRightCorner,
            topRightGateBottomLeftCorner,
            bottomRightGateTopLeftCorner)
    
def createRightRampLinkedCorners(pos):
    #left link
        #bottom left gate is top right corner - 1
    bottomLeftGateTopRightCorner = Corner(bottomLeftPos(pos), TOP_RIGHT)
        #top left gate is bottom right corner - 2
    topLeftGateBottomRightCorner = Corner(topLeftPos(pos), BOTTOM_RIGHT)
    PathFinding.GateAndLink.Link.LeftLink(bottomLeftGateTopRightCorner, topLeftGateBottomRightCorner)
    #right Ramp Link
        #top left gate is bottom right corner - 2
        #bottom right gate is top left corner - 3
    bottomRightGateTopLeftCorner = Corner(bottomRightPos(pos), TOP_LEFT)
    PathFinding.GateAndLink.Link.RightRampLink(bottomRightGateTopLeftCorner, topLeftGateBottomRightCorner)
    return (bottomLeftGateTopRightCorner,
            topLeftGateBottomRightCorner,
            bottomRightGateTopLeftCorner)

def createBoxLinkedCorners(pos):
    #left link
        #bottom left gate top right corner - 1
    bottomLeftGateTopRightCorner = Corner(bottomLeftPos(pos), TOP_RIGHT)
        #top left gate bottom right corner - 2
    topLeftGateBottomRightCorner = Corner(topLeftPos(pos), BOTTOM_RIGHT)
    PathFinding.GateAndLink.Link.LeftLink(bottomLeftGateTopRightCorner, topLeftGateBottomRightCorner)
    #top link
        #top left gate bottom right corner - 2
        #top right gate bottom left corner - 3
    topRightGateBottomLeftCorner = Corner(topRightPos(pos), BOTTOM_LEFT)
    PathFinding.GateAndLink.Link.TopLink(topLeftGateBottomRightCorner, topRightGateBottomLeftCorner)
    #right link
        #top right gate bottom left corner - 3
        #bottom right gate top left corner - 4
    bottomRightGateTopLeftCorner = Corner(bottomRightPos(pos), TOP_LEFT)
    PathFinding.GateAndLink.Link.RightLink(bottomRightGateTopLeftCorner, topRightGateBottomLeftCorner)
    return (bottomLeftGateTopRightCorner,
            topLeftGateBottomRightCorner,
            topRightGateBottomLeftCorner,
            bottomRightGateTopLeftCorner)

class Corner:
    def __init__(self, pos, position):
        self.links = []
        self.gate = None
        self.pos = pos
        self.position = position
    
    def render(self, screen, offset):
        UserInterface.Scroll.globalViewPort.drawCircle(screen, (0,255,0) , (self.pos[0] + offset[0], self.pos[1] + offset[1]), 3)
        for link in self.links:
            link.render(screen)
    
