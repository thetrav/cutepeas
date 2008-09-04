import Constants
import Event
from Constants import *
from Utils import *
from PathFinding.GateAndLink.Gate import *
from PathFinding.GateAndLink.Corner import *
from PathFinding.GateAndLink.PackageConstants import *
from PathFinding.GateAndLink.Link import *



def linkFloorGates(prev, current):
    bottomRight = Corner(prev.pos, BOTTOM_RIGHT)
    bottomRight.gate = prev
    prev.set(bottomRight)
    bottomLeft = Corner(current.pos, BOTTOM_LEFT)
    bottomLeft.gate = current
    current.set(bottomLeft)
    link = TopLink(bottomRight, bottomLeft)
    
def distance(pos, posStrings):
    xDistance = pos[0] - int(posStrings[0])
    yDistance = pos[1] - int(posStrings[1])
    return xDistance * xDistance + yDistance * yDistance

class NodeGraph:
    def __init__(self, numFloorBlocks, yPos):
        self.gates = {}
        
        prev = Gate((X_OFFSET, yPos))
        self.storeGate(prev)
        for x in xrange(numFloorBlocks):
            gate = createGate(x+1, yPos)
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
        gate = self.grabGate(corner.pos)
        gate.positions.pop(corner.position)
        if len(gate.positions) == 0 :
            self.removeGate(gate.pos)
    
    def storeCorner(self, corner):
        key = str(corner.pos)
        if not self.gates.has_key(key):
            self.storeGate(Gate(corner.pos))
        self.gates[key].positions[corner.position] = corner
        corner.gate = self.gates[key]
    
    def storeGate(self, gate):
        self.gates[str(gate.pos)] = gate
        gate.graph = self
        
    def hasGateAt(self, pos):
        return self.gates.has_key(str(pos))
    
    def grabGate(self, pos):
        return self.gates[str(pos)]
    
    def removeGate(self, pos):
        gate = self.gates.pop(str(pos))
        gate.graph = None
        
    def render(self, screen):
        if Constants.DRAW_NODES:
            for key in self.gates:
                self.gates[key].render(screen)

    def findNearestNode(self, pos):
        bestNode = None
        bestDistance = None
        for key in self.gates.keys():
            nodePos = key.strip('()').split(', ')
            if bestNode == None or distance(pos, nodePos) < bestDistance:
                bestNode = self.gates.get(key)
                bestDistance = distance(pos, nodePos)
        if bestNode == None:
            raise(" could not find a node")
        return bestNode
