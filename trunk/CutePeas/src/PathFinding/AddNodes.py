import pygame.draw
from Constants import *
from UserInterface.Text import *

class NodeGraph:
    def __init__(self, numFloorBlocks, plateIndex):
        self.nodes = {}
        prev = PlateCornerNode((0,plateIndex))
        self.storeNode(prev)
        
        for x in xrange(numFloorBlocks * 2):
            node = createNode(x+1, plateIndex)
            prev.linkNode(node)
            node.linkNode(prev)
            self.storeNode(node)
            pref = node
    
    def storeNode(self, node):
        self.nodes[str(node.pos)] = node
        
    def hasNodeAt(self, pos):
        return self.nodes.has_key(str(pos))
    
    def render(self, screen):
        for key in self.nodes:
                self.nodes[key].render(screen)
    
    def addNodes(self, toAdd):
        for node in toAdd:
            if self.hasNodeAt(node.pos):
                self.nodes[str(node.pos)].merge(node)
            else:
                self.storeNode(node)
                
class Node:
    def __init__(self, pos):
        self.pos = pos
        self.linkedNodes = set()
        self.nodeCount = 1
    
    def linkNode(self, node):
        self.linkedNodes.add(node)
        
    def unLinkNode(self, node):
        self.linkedNodes.remove(node)

    def getValidLinkedNodes(self):
        validNodes = []
        for node in self.linkedNodes:
            if node.canTraverse():
                validNodes.append(node)
        return validNodes
        
    def render(self, screen):
        pos = toScreenCoords(self.pos)
        renderText(str(self.nodeCount), pos, screen, (0,0,200))
        pygame.draw.circle(screen, (0,200,0) if self.canTraverse() else (250,0,0) , pos, 8)
        for node in self.linkedNodes:
            pygame.draw.line(screen, (0,0,200), pos, toScreenCoords(node.pos))
    
    def merge(self, node):
        print "merging"
        for linked in node.linkedNodes:
            linked.unLinkNode(node)
            linked.linkNode(self)
            self.linkNode(linked)
        self.nodeCount += 1
        node.linkedNodes.clear()

class PlateNode(Node):
    def __init__(self, pos):
        Node.__init__(self, pos)
        
    def canTraverse(self):
        return self.nodeCount == 1
    
class PlateCornerNode(Node):
    def __init__(self, pos):
        Node.__init__(self, pos)
        
    def canTraverse(self):
        return self.nodeCount < 3
    
class FaceNode(Node):
    def __init__(self, pos):
        Node.__init__(self, pos)
    
    def canTraverse(self):
        return self.nodeCount == 1
    
class CornerNode(Node):
    def __init__(self, pos):
        Node.__init__(self, pos)
        
    def canTraverse(self):
        return self.nodeCount < 4
        
def toScreenCoords(pos):
    return (pos[0]*BLOCK_WIDTH/2 + X_OFFSET, pos[1] * BLOCK_HEIGHT/2 + Y_OFFSET)

def createNode(x, y):
    if x % 2 == 0:
        return PlateCornerNode((x, y))
    else:
        return PlateNode((x, y))

