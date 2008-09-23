from Constants import *
from PathFinding.GateAndLink.PackageConstants import *
import UserInterface.Scroll
import PathFinding.GateAndLink.Corner



class Link:
    def __init__(self, cornerBottomOrLeft, cornerTopOrRight):
        # subclasses will most likely only use two out of these four variables 
        self.bottom = cornerBottomOrLeft
        self.left = cornerBottomOrLeft
        self.top = cornerTopOrRight
        self.right = cornerTopOrRight
        #make relationship bidirectional
        cornerBottomOrLeft.links.append(self)
        cornerTopOrRight.links.append(self)
        self.openColor = (255,255,255)
        self.closedColor = (255,0,0)
        
    def isJumpTransition(self):
        return False
    
    def render(self, screen, color=None):
            drawColor = color if color else self.openColor if self.isOpen() else self.closedColor
            UserInterface.Scroll.globalViewPort.drawLine(screen, drawColor, self.left.odePos, self.right.odePos, 3)
            
    def other(self, gate):
        return self.left.gate if gate != self.left.gate else self.right.gate

    def isOpen(self):
        pass

class LeftLink(Link):
    def __init__(self, bottom, top):
        Link.__init__(self, bottom, top)
    
    def isOpen(self):
        return not (self.top.gate.get(TOP_LEFT) or self.top.gate.get(BOTTOM_LEFT))

class RightLink(Link):
    def __init__(self, bottom, top):
        Link.__init__(self, bottom, top)
    
    def isOpen(self):
        return not (self.top.gate.get(TOP_RIGHT) or self.top.gate.get(BOTTOM_RIGHT))

class TopLink(Link):
    def __init__(self, left, right):
        Link.__init__(self, left, right)
    
    def isOpen(self):
        return not (self.left.gate.get(TOP_RIGHT) and self.right.gate.get(TOP_LEFT))
    
class LeftRampLink(Link):
    def __init__(self, bottom, top):
        Link.__init__(self, bottom, top)
    
    def isOpen(self):
        return not self.top.gate.get(TOP_LEFT)
    
class RightRampLink(Link):
    def __init__(self, bottom, top):
        Link.__init__(self, bottom, top)
    
    def isOpen(self):
        return not self.top.gate.get(TOP_RIGHT) 
    
class JumpTraversalLink(Link):
    def __init__(self, origin, destination):
        self.origin = PathFinding.GateAndLink.Corner.Corner(origin.odePos, JUMP)
        self.origin.gate = origin
        self.destination = PathFinding.GateAndLink.Corner.Corner(destination.odePos, JUMP)
        self.destination.gate = destination
        self.openColor=(180,180,180)
        self.closedColor=(180,0,0)
    
    def isOpen(self):
        return True
    
    def other(self, gate):
        return self.origin.gate if gate != self.origin.gate else self.destination.gate
    
    def render(self, screen, color=None):
        UserInterface.Scroll.globalViewPort.drawLine(screen, self.openColor if self.isOpen() else self.closedColor, self.origin.odePos, self.destination.odePos, 3)
        
    def isJumpTransition(self):
        return True