import Constants
import Event
from Constants import *
from Utils import *
from PathFinding.GateAndLink.Gate import *
from PathFinding.GateAndLink.Corner import *
from PathFinding.GateAndLink.PackageConstants import *
from PathFinding.GateAndLink.Link import *



def linkFloorGates(prev, current):
    bottomRight = Corner(prev.odePos, BOTTOM_RIGHT)
    bottomRight.gate = prev
    prev.set(bottomRight)
    bottomLeft = Corner(current.odePos, BOTTOM_LEFT)
    bottomLeft.gate = current
    current.set(bottomLeft)
    link = TopLink(bottomRight, bottomLeft)
    
def distance(odePos, posStrings):
    xDistance = odePos[0] - float(posStrings[0])
    yDistance = odePos[1] - float(posStrings[1])
    return xDistance * xDistance + yDistance * yDistance

class NodeGraph:
    def __init__(self, numFloorBlocks, yOdePos):
        self.gates = {}
        
        prev = Gate((X_OFFSET_ODE, yOdePos))
        self.storeGate(prev)
        for x in xrange(numFloorBlocks):
            gate = createGate(x+1, yOdePos)
            self.storeGate(gate)
            linkFloorGates(prev, gate)
            prev = gate
        
    def placeBlock(self, block):
        self.addCorners(block.createCorners())
        Event.fireEvent(EVENT_NODE_GRAPH_UPDATED, self)
    
    def removeBlock(self, block):
        self.removeCorners(block.createCorners())
        Event.fireEvent(EVENT_NODE_GRAPH_UPDATED, self)
        
    def addCorners(self, corners):
        for corner in corners:
            self.storeCorner(corner)
        
            
    def removeCorners(self, corners):
        for corner in corners:
            self.removeCorner(corner)
    
    def removeCorner(self, corner):
        gate = self.grabGate(corner.odePos)
        gate.positions.pop(corner.position)
        if len(gate.positions) == 0 :
            self.removeGate(gate.odePos)
    
    def storeCorner(self, corner):
        key = str(corner.odePos)
        if not self.gates.has_key(key):
            self.storeGate(Gate(corner.odePos))
        self.gates[key].positions[corner.position] = corner
        corner.gate = self.gates[key]
    
    def storeGate(self, gate):
        self.gates[str(gate.odePos)] = gate
        gate.graph = self
        
    def hasGateAt(self, odePos):
        return self.gates.has_key(str(odePos))
    
    def grabGate(self, odePos):
        return self.gates[str(odePos)]
    
    def removeGate(self, odePos):
        gate = self.gates.pop(str(odePos))
        gate.graph = None
        
    def render(self, screen):
        if Constants.DRAW_NODES:
            for key in self.gates:
                self.gates[key].render(screen)

    def findNearestNode(self, odePos):
        bestNode = None
        bestDistance = None
        for key in self.gates.keys():
            nodePos = key.strip('()').split(', ')
            if bestNode == None or distance(odePos, nodePos) < bestDistance:
                bestNode = self.gates.get(key)
                bestDistance = distance(odePos, nodePos)
        if bestNode == None:
            raise(" could not find a node")
        return bestNode
