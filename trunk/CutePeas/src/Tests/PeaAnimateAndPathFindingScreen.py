from Images import images
from UserInterface import Text
from UserInterface.Button import TitleScreenButton
from Level import BasicLevel
from UserInterface.Scenery import Scenery
from UserInterface.Block import *
from UserInterface.Pea import *
from PathFinding import Node

# Modified from TitleScreen
class Screen:
    def __init__(self, userInterface, transitionListener):
        self.nodeImage = images["nodeview"]
        self.userInterface = userInterface
        self.exitButton = self.addButton("Exit-Game", (600, 150), 200, 50)
        self.transitionListener = transitionListener
        #scene = Scenery()
        #self.userInterface.setScene(scene)
        self.node = self.__createSquareNodeStructure()
        self.pea = Pea(images["Pea-Standard"], self.node)
    
    def __createSquareNodeStructure(self):
        import NodeListGenerator as ng
        hnode1, hnodelist1 = ng.createHorizontalNodeList(None, 25, 30, 50, 7, self.nodeImage)
        lasthnode1 = hnodelist1[len(hnodelist1)-1]
        pos1 = hnode1.getPos()
        vnode1, vnodelist1 = ng.createVerticalNodeList(None, 25, pos1[0], pos1[1], 7, self.nodeImage)
        hnode1 = hnode1.nextNode()
        hnode1.setPrevNode(vnode1)
        # need to swap direction of links so that traversal is consistent.. I've never had to worry
        # about direction on a regular list before wow... - this stuff only makes sense when you draw it.
        # need to optimise this if possible...
        # Alternatively drawing it in a different order may work w/o swapDirection.. too sleepy to think..
        Node.swapDirection(vnode1) 
        vnode1.setNextNode(hnode1)
        lastvnode1 = vnodelist1[len(vnodelist1)-1]
        pos2 = lastvnode1.getPos()
        hnode2, hnodelist2 = ng.createHorizontalNodeList(None, 25, pos2[0], pos2[1], 7, self.nodeImage)
        lastvnode1 = lastvnode1.nextNode()
        lastvnode1.setPrevNode(hnode2)
        Node.swapDirection(hnode2) 
        hnode2.setNextNode(lastvnode1)
        lasthnode2 = hnodelist2[len(hnodelist2)-1]
        #return lasthnode2
        pos3 = lasthnode2.getPos()
        vnode2, vnodelist2 = ng.createVerticalNodeList(None, 25, pos3[0], pos3[1], -7, self.nodeImage)
        lasthnode2 = lasthnode2.nextNode()
        lasthnode2.setPrevNode(vnode2)
        Node.swapDirection(vnode2)
        vnode2.setNextNode(lasthnode2)
        lastvnode2 = vnodelist2[len(vnodelist2)-1]
        # Complete the circle
        print lasthnode1
        print lastvnode2
        lasthnode1 = lasthnode1.prevNode()
        lasthnode1.setNextNode(lastvnode2)
        lastvnode2.setPrevNode(lasthnode1)
        print lasthnode1
        print lastvnode2
        return lastvnode2
        #return vnodelist1[len(vnodelist1)-1]
    
    def addBlock(self, block, scene, x, y):
        scene.slots[x][y].addBlock(block)
        block.doneGhostingIn()
        
    def addButton(self, name, pos, width, height):
        button = TitleScreenButton(name, pos, width, height)
        button.addListener(self)
        self.userInterface.addActiveWidget(button)
        return button
    
    def buttonFired(self, button):
        if button == self.exitButton:
            import sys
            sys.exit(0)
    
    def render(self, screen):
        screen.blit(images["Background"], (0,0))
        screen.blit(images["Logo"], (10,10))
        screen.blit(images["Plate"], (5, 520))
        self.userInterface.render(screen)
        flagPos = (315, 280)
        screen.blit(images["Flag-Pole"], flagPos)
        screen.blit(images["Flag-Good"], (flagPos[0]+5, flagPos[1]+20))
        self.node.render(screen)
        self.renderPea(screen)
    
    def renderPea(self, screen):
        self.pea.render(screen)
        
    def transition(self):
        self.transitionListener.transition(BasicLevel(self.userInterface))
        
    def dispose(self):
        self.userInterface.removeActiveWidget(self.exitButton)
        self.userInterface.removeActiveWidget(self.newGameButton)
