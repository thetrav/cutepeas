import pygame.draw
import Constants
from Constants import *
from UserInterface.Text import *
import Event
import Objects.Block
import math
import Images
import Coordinates

NODE_X_GAP = BLOCK_WIDTH/2
NODE_Y_GAP = BLOCK_HEIGHT/2
FLAG_MAX_HEIGHT = 30
FLAG_HEIGHT = 68



def distance(pos, posStrings):
    xDistance = pos[0] - int(posStrings[0])
    yDistance = pos[1] - int(posStrings[1])
    return xDistance * xDistance + yDistance * yDistance

class NodeGraph:
    def __init__(self, numFloorBlocks, yPos):
        self.nodes = {}
        prev = PlateCornerNode((X_OFFSET,yPos))
        self.storeNode(prev)
        self.flags = []
        
        for x in xrange(numFloorBlocks * 2):
            node = createNode(x+1, yPos)
            prev.linkNode(node)
            node.linkNode(prev)
            self.storeNode(node)
            prev = node
            
    def placeFlag(self, flag, node):
        print "placing flag at ", flag.pos
        self.flags.append(flag)
        node.placeFlag(flag)
            
    def findNearestNode(self, pos):
        print "finding node at ", pos, " in ", self.nodes.keys()
        bestNode = None
        bestDistance = None
        for key in self.nodes.keys():
            nodePos = key.strip('()').split(', ')
            if bestNode == None or distance(pos, nodePos) < bestDistance:
                bestNode = self.nodes.get(key)
                bestDistance = distance(pos, nodePos)
        if bestNode == None:
            raise(" could not find a node")
        return bestNode
        #snapped = str(Coordinates.pixelPosToNearestNode(pos))
        #haven't gotten this working yet.  Is theoretically more efficient
        #best = None
        #for key in self.nodes.keys():
        #    current = self.nodes.get(key)
        #    if best == None or current.pos[X] == snapped[X] and current.pos[Y] < best.pos[Y]:
        #        best = current
        #if best == None:
        #    raise "pea could not find node nearest to:  " + str(pos) + " which translated to snapped position of: " + str(snapped)
        #return best
    
    def checkCircle(self, center, radius):
        #radius is in block nodes, and by circle I mean square
        pass
    
    def storeNode(self, node):
        self.nodes[str(node.pos)] = node
        
    def hasNodeAt(self, pos):
        return self.nodes.has_key(str(pos))
    
    def grabNode(self, pos):
        return self.nodes[str(pos)]
    
    def removeNode(self, pos):
        self.nodes.pop(str(pos))
    
    def render(self, screen):
        for flag in self.flags:
            flag.render(screen)
        if Constants.DRAW_NODES:
            for key in self.nodes:
                    self.nodes[key].render(screen)
    
    def placeBlock(self, block):
        self.addNodes(block.createNodes())
    
    def addNodes(self, toAdd):
        for node in toAdd:
            if self.hasNodeAt(node.pos):
                self.nodes[str(node.pos)].merge(node)
            else:
                self.storeNode(node)
        Event.fireEvent(EVENT_NODE_GRAPH_UPDATED, self)
    
    def removeBlock(self, block):
        self.removeNodes(block.createNodes())
    
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
    root = MinMaxNode(currentNode)
    buildTree(root, [currentNode])
    #printTree(root, 0)
    path = buildPath(root, [])
    return path

def buildPath(minMaxNode, currentPath):
    currentPath.append(minMaxNode.node)
    for node in minMaxNode.linkedNodes:
        if node.score == minMaxNode.score:
            return buildPath(node, currentPath)
    return currentPath

def printTree(node, depth):
    print " "*depth + str(node.node.pos) + " score:" + str(node.score)
    for linked in node.linkedNodes:
        printTree(linked, depth+1)

def buildTree(minMaxNode, nodesInTree):
    for linked in minMaxNode.node.linkedNodes:
        if linked.canTraverse() and linked not in nodesInTree:
            newNode = MinMaxNode(linked)
            minMaxNode.linkedNodes.append(newNode)
            nodesInTree.append(linked)
            score = buildTree(newNode, nodesInTree)
            if score < minMaxNode.score:
                minMaxNode.score = score 
    return minMaxNode.score
        
class MinMaxNode:
    def __init__(self, node):
        self.node = node
        self.score = node.pos[Y]
        self.linkedNodes = []
    
class Node:
    def __init__(self, pos, block):
        self.pos = pos
        self.linkedNodes = set()
        self.nodeCount = 1
        self.flag = None
        self.block = block
        
    def isJumpable(self):
        if self.flag == None:
            return True
        else:
            return not self.flag.isComplete()
    
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
        
    def placeFlag(self, flag):
        self.flag = flag
        self.block.flagPlaced = True

class PlateNode(Node):
    def __init__(self, pos):
        Node.__init__(self, pos, None)
        
    def canTraverse(self):
        return self.nodeCount == 1
    
    def isJumpable(self):
        return False
    
class PlateCornerNode(Node):
    def __init__(self, pos):
        Node.__init__(self, pos, None)
        
    def canTraverse(self):
        return self.nodeCount < 3
    
    def isJumpable(self):
        return False
    
class FaceNode(Node):
    def __init__(self, pos, block):
        Node.__init__(self, pos, block)
    
    def canTraverse(self):
        return self.nodeCount == 1
    
class CornerNode(Node):
    def __init__(self, pos, block):
        Node.__init__(self, pos, block)
        
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
    
class Flag:
    def __init__(self, pos, maxJumps):
        self.pos = (pos[0]-10, pos[1]-FLAG_HEIGHT)
        self.jumps = 0
        self.maxJumps = maxJumps
        self.flagPos = [pos[0], pos[1] - FLAG_MAX_HEIGHT]
        self.peas = set()
    
    def render(self, surface):
        surface.blit(Images.images["Flag-Pole"], self.pos)
        if self.jumps > 0:
            surface.blit(Images.images["Flag-Good"], self.flagPos)
    
    def jumpDone(self, pea):
        if pea not in self.peas:
            self.jumps += 1
            self.flagPos[1] -= FLAG_MAX_HEIGHT / self.maxJumps
        
    def isComplete(self):
        return self.jumps == self.maxJumps
