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
        pos1 = hnode1.getPos()
        vnode1, vnodelist1 = ng.createVerticalNodeList(None, 25, pos1[0], pos1[1], 7, self.nodeImage)
        hnode1 = hnode1.nextNode()
        hnode1.setPrevNode(vnode1)
#        pos2 = vnodelist1[len(vnodelist1)-1].getPos()
#        hnode2, hnodelist2 = ng.createHorizontalNodeList(None, 25, pos2[0], pos2[1], 7)
#        pos3 = hnodelist2[len(hnodelist2)-1].getPos()
#        vnode2, vnodelist2 = ng.createVerticalNodeList(None, 25, pos3[0], pos3[1], 7)
        return hnode1
    
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
