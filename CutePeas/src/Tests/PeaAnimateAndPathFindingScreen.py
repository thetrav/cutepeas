from Images import images
from UserInterface import Text
from UserInterface.Button import TitleScreenButton
from Level import BasicLevel
from UserInterface.Scenery import Scenery
from UserInterface.Block import *
from UserInterface.Pea import *

# Modified from TitleScreen
class Screen:
    def __init__(self, userInterface, transitionListener):
        self.userInterface = userInterface
        self.exitButton = self.addButton("Exit-Game", (600, 150), 200, 50)
        self.transitionListener = transitionListener
        #scene = Scenery()
        #self.userInterface.setScene(scene)
        self.pea = Pea(images["Pea-Standard"], (0, 515))
        

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
            raise "quit"
    
    def render(self, screen):
        screen.blit(images["Background"], (0,0))
        screen.blit(images["Logo"], (10,10))
        screen.blit(images["Plate"], (5, 520))
        self.userInterface.render(screen)
        flagPos = (315, 280)
        screen.blit(images["Flag-Pole"], flagPos)
        screen.blit(images["Flag-Good"], (flagPos[0]+5, flagPos[1]+20))
        self.pea.render(screen)
        
    def transition(self):
        self.transitionListener.transition(BasicLevel(self.userInterface))
        
    def dispose(self):
        self.userInterface.removeActiveWidget(self.exitButton)
        self.userInterface.removeActiveWidget(self.newGameButton)
