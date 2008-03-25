from Images import images
from UserInterface import Text
from UserInterface.Button import TitleScreenButton
from Level import BasicLevel
from UserInterface.Scenery import Scenery
from UserInterface.Block import *
from UserInterface.Pea import *
from PathFinding.NodeGraph import *
from Physics.QuickPhysics import *

class TitleScreen:
    def __init__(self, userInterface, transitionListener):
        self.userInterface = userInterface
        self.highScoreList = HighScoreList((100,100))
        self.exitButton = self.addButton("Exit-Game", (600, 150), 200, 50)
        self.newGameButton = self.addButton("New-Game", (580, 100), 200, 50)
        self.transitionListener = transitionListener
        scene = Scenery(BLOCKS_WIDE, BLOCKS_HIGH)
        self.nodeGraph = NodeGraph(BLOCKS_WIDE, BLOCKS_HIGH * BLOCK_HEIGHT + Y_OFFSET + BLOCK_Y_OVERLAP)
        self.userInterface.setScene(scene)
        self.addBlock(Block("Block-Place-Normal", "Block-Normal"), scene, 3, 8)
        self.addBlock(Block("Block-Place-Normal", "Block-Normal"), scene, 3, 7)
        self.addBlock(Block("Block-Place-Normal", "Block-Normal"), scene, 3, 6)
        self.addBlock(Block("Block-Place-Normal", "Block-Normal"), scene, 3, 5)
        self.addBlock(Block("Block-Place-RightRamp", "Block-RightRamp"), scene, 4, 7)
        self.addBlock(Block("Block-Place-Normal", "Block-Normal"), scene, 4, 8)
        self.addBlock(Block("Block-Place-Spring", "Block-Spring"), scene, 6, 8)
        self.addBlock(Block("Block-Place-Gel", "Block-Gel"), scene, 8, 8)
        self.physicsManager = PhysicsManager()
        self.pea = Pea(images["Pea-Standard"], self.nodeGraph.grabNode((121, 551)), self.physicsManager)
        Animation.animations.append(self.pea)
        

    def addBlock(self, block, scene, x, y):
        scene.slots[x][y].addBlock(block)
        block.doneGhostingIn()
        self.nodeGraph.addNodes(block.createNodes())
        
    def addButton(self, name, pos, width, height):
        button = TitleScreenButton(name, pos, width, height)
        button.addListener(self)
        self.userInterface.addActiveWidget(button)
        return button
    
    def buttonFired(self, button):
        if button == self.exitButton:
            raise "quit"
        if button == self.newGameButton:
            self.transition()
    
    def render(self, screen):
        screen.blit(images["Background"], (0,0))
        screen.blit(images["Logo"], (10,10))
        screen.blit(images["Plate"], (5, 520))
        self.userInterface.render(screen)
        self.highScoreList.render(screen)
        flagPos = (315, 280)
        screen.blit(images["Flag-Pole"], flagPos)
        screen.blit(images["Flag-Good"], (flagPos[0]+5, flagPos[1]+20))
        self.nodeGraph.render(screen)
        self.pea.render(screen)
        
    def transition(self):
        self.transitionListener.transition(BasicLevel(self.userInterface))
        Animation.animations.remove(self.pea)
        self.pea.dispose()
        
    def dispose(self):
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