import pygame.draw
from Constants import *
from UserInterface.Text import *
import Event
import UserInterface.Block
import math

NODE_X_GAP = BLOCK_WIDTH/2
NODE_Y_GAP = BLOCK_HEIGHT/2

def snapToPos(pos):
    return [snap(pos[0], X_OFFSET, NODE_X_GAP), snap(pos[1], Y_OFFSET, NODE_Y_GAP)]

def snap(pos, offset, gap):
    return math.round((pos - offset) / gap) * gap + offset

class NodeGraph:
    def __init__(self, numFloorBlocks, yPos):
        self.nodes = {}
        prev = PlateCornerNode((X_OFFSET,yPos))
        self.storeNode(prev)
        
        for x in xrange(numFloorBlocks * 2):
            node = createNode(x+1, yPos)
            prev.linkNode(node)
            node.linkNode(prev)
            self.storeNode(node)
            prev = node
            
    def findNearestNode(self, pos):
        snapped = snapToPos(pos)
        if self.hasNodeAt(snapped):
            return self.grabNode(snapped)
        else:
            radius = 1
            while radius < NUM_BLOCKS * 2 + 1:
                node = self.checkCircle(snapped, radius)
                if node:
                    return node
        raise "pea could not find node nearest to:  " + str(pos) + " which translated to snapped position of: " + str(snapped)
    
    def checkCircle(self, center, radius):
        #radius is in block nodes, and by circle I mean square
        pass
    
    def eventFired(self, id, block):
        if id == UserInterface.Block.DONE_GHOSTING_IN_EVENT:
            self.addNodes(block.createNodes())
        elif id == UserInterface.Block.DONE_GHOSTING_OUT_EVENT:
            self.removeNodes(block.createNodes())
    
    def storeNode(self, node):
        self.nodes[str(node.pos)] = node
        
    def hasNodeAt(self, pos):
        return self.nodes.has_key(str(pos))
    
    def grabNode(self, pos):
        return self.nodes[str(pos)]
    
    def removeNode(self, pos):
        self.nodes.pop(str(pos))
    
    def render(self, screen):
        for key in self.nodes:
                self.nodes[key].render(screen)
    
    def addNodes(self, toAdd):
        for node in toAdd:
            if self.hasNodeAt(node.pos):
                self.nodes[str(node.pos)].merge(node)
            else:
                self.storeNode(node)
        Event.fireEvent(EVENT_NODE_GRAPH_UPDATED, self)
                
    def removeNodes(self, toRemove):
        for node in toRemove:
            if self.hasNodeAt(node.pos):
                self.remove(self.grabNode(node.pos))
        Event.fireEvent(EVENT_NODE_GRAPH_UPDATED, self)
    
    def remove(self, node):
        node.nodeCount -= 1
        if node.nodeCount < 1:
            for linked in node.linkedNodes:
                linked.unLinkNode(node)
            node.linkedNodes.clear()
            self.removeNode(node.pos)
    
def findPath(currentNode):
    nodeCount = 0
    nodes = []
    traverseNode(nodes, currentNode)
    return nodes
        
def traverseNode(currentPath, currentNode):
    if len(currentPath) < 5:
        for linked in currentNode.linkedNodes:
            if linked not in currentPath and linked.canTraverse() and len(currentPath) < 5:
                currentPath.append(linked)
                traverseNode(currentPath, linked)
                return
                
class Node:
    def __init__(self, pos):
        self.pos = pos
        self.linkedNodes = set()
        self.nodeCount = 1
    
    def linkNode(self, node):
        assert node is not self
        self.linkedNodes.add(node)
        
    def unLinkNode(self, node):
        self.linkedNodes.remove(node)

    def getValidLinkedNodes(self):
        validNodes = []
        for node in self.linkedNodes:
            if node.canTraverse():
                validNodes.append(node)
        return validNodes
        
    def render(self, screen, traversableNodeColor=(0,200,0), blockedNodeColor=(250,0,0),linkColor=(0,0,200)):
        pos = self.pos
        renderText(str(self.nodeCount), pos, screen, (0,0,200))
        pygame.draw.circle(screen, traversableNodeColor if self.canTraverse() else blockedNodeColor , pos, 8)
        for node in self.linkedNodes:
            pygame.draw.line(screen, linkColor, pos, node.pos)
    
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
        
def toScreenCoords(x):
    return x*BLOCK_WIDTH/2 + X_OFFSET

def createNode(x, y):
    xPixelPos = toScreenCoords(x)
    if x % 2 == 0:
        return PlateCornerNode((xPixelPos, y))
    else:
        return PlateNode((xPixelPos, y))

def loopNodes(nodeList):
    prev = None
    for node in nodeList:
        if prev:
            prev.linkNode(node)
            node.linkNode(prev)
        prev = node
    prev.linkNode(nodeList[0])
    nodeList[0].linkNode(prev)


graph = NodeGraph(9,10)
for key in graph.nodes:
    node = graph.nodes[key]
    print "node at:"+key+" count="+str(len(node.linkedNodes)) + " nodes:"+str([linked.pos for linked in node.linkedNodes])

path = findPath(graph.nodes['(156, 10)'])
print str([node.pos for node in path])