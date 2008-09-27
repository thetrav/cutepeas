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
    if minMaxNode.isEndPoint():
        return currentPath
    for node in minMaxNode.linkedNodes:
        if node.score == minMaxNode.score:
            return buildPath(node, currentPath)
    return currentPath

def printTree(node, depth):
    print " "*depth, node.gate.odePos, " score:" , node.score, ' jump dir:', node.gate.getJumpDirection()
    for linked in node.linkedNodes:
        printTree(linked, depth+1)

class MinMaxNode:
    def __init__(self, inboundLink, gate):
        self.gate = gate
        self.link= inboundLink
        self.score = gate.odePos[Y] if gate.isJumpable() else SCREEN_HEIGHT_ODE
        self.linkedNodes = []
        self.trueScore = self.score
        
    def isEndPoint(self):
        if self.score == self.trueScore:
            if self.gate.isJumpable():
                return True
        return False
        
    def render(self, screen):
        UserInterface.Scroll.globalViewPort.drawCircle(screen, (255,0,255) , (self.gate.odePos[X], self.gate.odePos[Y]), 15, 3)
        if self.link:
            self.link.render(screen, (255,0,255))