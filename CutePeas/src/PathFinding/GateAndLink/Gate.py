from Constants import *
from PathFinding.GateAndLink.PackageConstants import *
import PathFinding.GateAndLink.Link
from Utils import *
import UserInterface.Scroll
import UserInterface.Text
import Coordinates

TEXT_OFFSET_X = Coordinates.pixelsToOde(20)
TEXT_OFFSET_Y = Coordinates.pixelsToOde(20)

def createGate(x, y):
    xOdePos = toScreenCoords(x)
    return Gate((xOdePos, y))

def createGateRect(odePos):
    return (odePos[0] - Coordinates.pixelsToOde(10), odePos[1] - Coordinates.pixelsToOde(10), Coordinates.pixelsToOde(20), Coordinates.pixelsToOde(20))

def getJumpLink(graph, originGate, destinationOdePos):
    if graph.hasGateAt(destinationOdePos):
        destinationGate = graph.grabGate(destinationOdePos)
        if destinationGate.getJumpDirection():
            return PathFinding.GateAndLink.Link.JumpTraversalLink(originGate, destinationGate)

class Gate:
    def __init__(self, odePos):
        self.odePos = odePos
        self.positions = {}
        self.score = SCREEN_HEIGHT
        self.pea = None
        self.graph = None
    
    def render(self, screen):
        jumpDir = self.getJumpDirection()
        color = (0,0,255)
        if jumpDir == LEFT_JUMP:
            color = (255,255,0)
        elif jumpDir == RIGHT_JUMP:
            color = (0, 255, 255)
        UserInterface.Scroll.globalViewPort.drawRect(screen, color, createGateRect(self.odePos))
        
        UserInterface.Scroll.globalViewPort.renderText(str(self.score), (self.odePos[X]+TEXT_OFFSET_X, self.odePos[Y]-TEXT_OFFSET_Y), screen, (255,0,0), "NODE_FONT")
        
        if self.get(TOP_LEFT):
            self.get(TOP_LEFT).render(screen, Coordinates.pixelPosToOdePos((-5, -5)))
        if self.get(TOP_RIGHT):
            self.get(TOP_RIGHT).render(screen, Coordinates.pixelPosToOdePos((5, -5)))
        if self.get(BOTTOM_LEFT):
            self.get(BOTTOM_LEFT).render(screen, Coordinates.pixelPosToOdePos((-5, 5)))
        if self.get(BOTTOM_RIGHT):
            self.get(BOTTOM_RIGHT).render(screen, Coordinates.pixelPosToOdePos((5,5)))
    
    def get(self, key):
        if self.positions.has_key(key):
            return self.positions[key]
        return None
    
    def set(self, corner):
        self.positions[corner.position] = corner
    
    def getJumpDirection(self):
        if len(self.positions) == 1:
            if self.get(BOTTOM_LEFT):
                return RIGHT_JUMP
            if self.get(BOTTOM_RIGHT):
                return LEFT_JUMP
    
    def getOpenLinks(self, inboundLink):
        openLinks = []
        link = None
        if self.getJumpDirection() == LEFT_JUMP:
            leftGatePos = (self.odePos[X] - BLOCK_WIDTH_ODE, self.odePos[Y])
            link = getJumpLink(self.graph, self, leftGatePos)
        elif self.getJumpDirection() == RIGHT_JUMP:
            rightGatePos = (self.odePos[X] + BLOCK_WIDTH_ODE, self.odePos[Y])
            link = getJumpLink(self.graph, self, rightGatePos)
        if link:
            openLinks.append(link)
        
        for key in self.positions.keys():
            for link in self.get(key).links:
                if link != inboundLink and link.isOpen():
                    openLinks.append(link)
        return openLinks