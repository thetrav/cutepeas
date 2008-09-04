from Constants import *
import UserInterface.Scroll

def findPath(targetGate):
    root = MinMaxNode(None, targetGate)
    buildTree(root, [targetGate])
    #printTree(root, 1)
    path = buildPath(root, [])
    return path

def buildTree(parent, gatesInTree):
    for link in parent.gate.getOpenLinks(parent.link):
        gate = link.other(parent.gate)
        if gate not in gatesInTree:
            newNode = MinMaxNode(link, gate)
            gatesInTree.append(gate)
            score = buildTree(newNode, gatesInTree)
            parent.linkedNodes.append(newNode)
            if score < parent.score:
                parent.score = score
    parent.gate.score = parent.score
    return parent.score

def buildPath(minMaxNode, currentPath):
    currentPath.append(minMaxNode)
    for node in minMaxNode.linkedNodes:
        if node.score == minMaxNode.score:
            return buildPath(node, currentPath)
    return currentPath

def printTree(node, depth):
    print " "*depth, node.gate.pos, " score:" , node.score, ' jump dir:', node.gate.getJumpDirection()
    for linked in node.linkedNodes:
        printTree(linked, depth+1)

class MinMaxNode:
    def __init__(self, inboundLink, gate):
        self.gate = gate
        self.link= inboundLink
        self.score = gate.pos[Y] if gate.getJumpDirection() else SCREEN_HEIGHT
        self.linkedNodes = []
        
    def render(self, screen):
        UserInterface.Scroll.globalViewPort.drawCircle(screen, (255,0,255) , (self.gate.pos[X], self.gate.pos[Y]), 15, 3)
        if self.link:
            self.link.render(screen, (255,0,255))