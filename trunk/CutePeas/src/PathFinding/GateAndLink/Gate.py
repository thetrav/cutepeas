from Constants import *
from PathFinding.GateAndLink.PackageConstants import *
import PathFinding.GateAndLink.Link
from Utils import *
import UserInterface.Scroll
import UserInterface.Text

def createGate(x, y):
    xPixelPos = toScreenCoords(x)
    return Gate((xPixelPos, y))

def createGateRect(pos):
    return (pos[0] - 10, pos[1] - 10, 20, 20)

def getJumpLink(graph, originGate, destinationPos):
    if graph.hasGateAt(destinationPos):
        destinationGate = graph.grabGate(destinationPos)
        if destinationGate.getJumpDirection():
            return PathFinding.GateAndLink.Link.JumpTraversalLink(originGate, destinationGate)

class Gate:
    def __init__(self, pos):
        self.pos = pos
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
        UserInterface.Scroll.globalViewPort.drawRect(screen, color, createGateRect(self.pos))
        
        UserInterface.Scroll.globalViewPort.renderText(str(self.score), (self.pos[X]+20, self.pos[Y]-20), screen, (255,0,0), "NODE_FONT")
        
        if self.get(TOP_LEFT):
            self.get(TOP_LEFT).render(screen, (-5, -5))
        if self.get(TOP_RIGHT):
            self.get(TOP_RIGHT).render(screen, (5, -5))
        if self.get(BOTTOM_LEFT):
            self.get(BOTTOM_LEFT).render(screen, (-5, 5))
        if self.get(BOTTOM_RIGHT):
            self.get(BOTTOM_RIGHT).render(screen, (5,5))
    
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
            leftGatePos = (self.pos[X] - BLOCK_WIDTH, self.pos[Y])
            link = getJumpLink(self.graph, self, leftGatePos)
        elif self.getJumpDirection() == RIGHT_JUMP:
            rightGatePos = (self.pos[X] + BLOCK_WIDTH, self.pos[Y])
            link = getJumpLink(self.graph, self, rightGatePos)
        if link:
            openLinks.append(link)
        
        for key in self.positions.keys():
            for link in self.get(key).links:
                if link != inboundLink and link.isOpen():
                    openLinks.append(link)
        return openLinks