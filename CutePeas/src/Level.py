import Animation
import Event
import Images
import Objects.Block
import Objects.Pea
import Physics.OdePhysics
import PathFinding.NodeGraph
import Scene
from Constants import *
from UserInterface.Button import *
from UserInterface.Tool import *
from UserInterface.Score import *
from UserInterface.Timer import *

def newButton(image, yPos, tool):
    return ToolButton(image, tool, (725, yPos), 47, 47)

class BasicLevel:
    def __init__(self, userInterface):
        self.userInterface = userInterface
        
        self.score = self.createScoreWidget()
        self.timer = self.createTimerWidget()
        self.nodeGraph = self.createNodeGraph()
        self.physicsManager = self.createPhysicsManager()
        self.scene = self.createScene()
        self.buttonPanel = self.createToolPanel()
        self.scene.addPea(Objects.Pea.Pea((0, 600), self.nodeGraph, self.physicsManager))
        #self.scene.addPea(Objects.Pea.Pea((100, 600), self.nodeGraph, self.physicsManager))
        #self.scene.addPea(Objects.Pea.Pea((200, 600), self.nodeGraph, self.physicsManager))
        #self.scene.addPea(Objects.Pea.Pea((300, 600), self.nodeGraph, self.physicsManager))
        #self.scene.addPea(Objects.Pea.Pea((400, 600), self.nodeGraph, self.physicsManager))
        
    def render(self, screen):
        screen.blit(Images.images["Background"], (0,0))
        screen.blit(Images.images["Plate"], (5, 520))
        self.scene.render(screen)
        self.userInterface.render(screen)
        
    def dispose(self):
        self.scene.dispose()
        self.buttonPanel.dispose()
        self.timer.dispose()
        self.score.dispose()
        
    def createScene(self):
        scene = Scene.Scene(self.nodeGraph, self.physicsManager)
        self.userInterface.setScene(scene)
        return scene

    def createPhysicsManager(self):
        physicsManager = Physics.OdePhysics.OdePhysicsManager()
        Animation.animations.append(physicsManager)
        return physicsManager
    
    def createNodeGraph(self):
        nodeGraph = PathFinding.NodeGraph.NodeGraph(BLOCKS_WIDE, BLOCKS_HIGH * BLOCK_HEIGHT + Y_OFFSET + BLOCK_Y_OVERLAP)
        return nodeGraph
    
    def createToolPanel(self):
        buttonPanel = ButtonPanel((720, 10))
        self.userInterface.addActiveWidget(buttonPanel)
        buttonPanel.addListener(self.userInterface)
        yStart = 15
        spacing = 50
        for button in (newButton("Delete", yStart, DeleteTool(self.scene)),
                        newButton("Gel", yStart + spacing, GelBlockTool(self.scene)),
                        newButton("Normal", yStart + spacing*2, NormalBlockTool(self.scene)),
                        newButton("LeftRamp", yStart + spacing*3, LeftRampTool(self.scene)),
                        newButton("RightRamp", yStart + spacing*4, RightRampTool(self.scene)),
                        newButton("Spring", yStart + spacing*5, SpringTool(self.scene))
                        ):
            buttonPanel.addButton(button)
        return buttonPanel
    
    def createScoreWidget(self):
        score = Score((300, 10))
        Animation.animations.append(score)
        self.userInterface.addPassiveWidget(score)
        return score
    
    def createTimerWidget(self):
        timer = Timer((600, 10))
        Animation.animations.append(timer)
        self.userInterface.addPassiveWidget(timer)
        return timer
    
        