import Images
import Objects.Block
import Objects.Pea
import Physics.OdePhysics
import Animation
import Scene
import sys
import Coordinates
from UserInterface import Text
from UserInterface.Button import TitleScreenButton
from Level import BasicLevel
from PathFinding.NodeGraph import *

class TitleScreen:
    def __init__(self, userInterface, transitionListener):
        self.userInterface = userInterface
        self.transitionListener = transitionListener
        self.highScoreList = HighScoreList((100,100))
        self.exitButton = self.addButton("Exit-Game", (600, 150), 200, 50)
        self.newGameButton = self.addButton("New-Game", (580, 100), 200, 50)
        self.nodeGraph = NodeGraph(BLOCKS_WIDE, BLOCKS_HIGH * BLOCK_HEIGHT + Y_OFFSET + BLOCK_Y_OVERLAP)
        self.physicsManager = Physics.OdePhysics.OdePhysicsManager()
        self.scene = Scene.Scene(self.nodeGraph, self.physicsManager)
        self.userInterface.setScene(self.scene)
        self.addBlock(Objects.Block.Block("Block-Place-Normal", "Block-Normal"), (2, 8))
        self.addBlock(Objects.Block.Block("Block-Place-Normal", "Block-Normal"), (3, 8))
        self.addBlock(Objects.Block.Block("Block-Place-Normal", "Block-Normal"), (3, 7))
        self.addBlock(Objects.Block.Block("Block-Place-Normal", "Block-Normal"), (3, 6))
        self.addBlock(Objects.Block.Block("Block-Place-Normal", "Block-Normal"), (3, 5))
        self.addBlock(Objects.Block.RightRampBlock("Block-Place-RightRamp", "Block-RightRamp"), (4, 7))
        self.addBlock(Objects.Block.Block("Block-Place-Normal", "Block-Normal"), (4, 8))
        self.addBlock(Objects.Block.Block("Block-Place-Spring", "Block-Spring"), (6, 8))
        self.addBlock(Objects.Block.Block("Block-Place-Gel", "Block-Gel"), (8, 8))
        self.scene.addPea(Objects.Pea.Pea((0, 600), self.nodeGraph, self.physicsManager))
        
    def addBlock(self, block, pos):
        pixelPos = Coordinates.boxIndexToPixelPos(pos)
        self.scene.placeBlock(pixelPos, block)
        block.doneGhostingIn()
        
    def addButton(self, name, pos, width, height):
        button = TitleScreenButton(name, pos, width, height)
        button.addListener(self)
        self.userInterface.addActiveWidget(button)
        return button
    
    def buttonFired(self, button):
        if button == self.exitButton:
            sys.exit(0)
        if button == self.newGameButton:
            self.transition()
    
    def render(self, screen):
        screen.blit(Images.images["Background"], (0,0))
        screen.blit(Images.images["Logo"], (10,10))
        screen.blit(Images.images["Plate"], (5, 520))
        self.userInterface.render(screen)
        self.highScoreList.render(screen)
        #flagPos = (315, 280)
        #screen.blit(images["Flag-Pole"], flagPos)
        #screen.blit(images["Flag-Good"], (flagPos[0]+5, flagPos[1]+20))
        self.scene.render(screen)
        
    def transition(self):
        self.transitionListener.transition(BasicLevel(self.userInterface))
        
    def dispose(self):
        self.scene.dispose()
        self.userInterface.removeActiveWidget(self.exitButton)
        self.userInterface.removeActiveWidget(self.newGameButton)

LINE_WIDTH = 30
LINE_SPACING = 20
        
class HighScoreList:
    def __init__(self, pos):
        self.scores = [("The Trav","6:33"),("Kamal", "7:00"), ("Rory", "7:01"), ("Scott", "7:15")]
        self.pos = pos
        
    def render(self, screen):
        Text.renderText("High Scores", self.pos, screen, (250,220,0), "TITLE_FONT")
        xPos = self.pos[0]
        yPos = self.pos[1] + 60
        for score in self.scores:
            renderString = score[0] + ((LINE_WIDTH - len(score[0]) - len(score[1])) * ".") + score[1]
            Text.renderText(renderString, (xPos, yPos), screen, (0,100,0))
            yPos = yPos + LINE_SPACING