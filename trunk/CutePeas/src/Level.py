from Images import images
from UserInterface.Button import *
from UserInterface.Tool import *
from UserInterface.Scenery import *
import Animation
from UserInterface.Score import *
from UserInterface.Timer import *
import PathFinding.NodeGraph
from Constants import *
import Objects.Block
import Objects.Pea
import Physics.OdePhysics

def newButton(image, yPos, tool):
    return ToolButton(image, tool, (725, yPos), 47, 47)

class BasicLevel:
    def __init__(self, userInterface):
        self.userInterface = userInterface
        self.buttonPanel = ButtonPanel((720, 10))
        
        userInterface.addActiveWidget(self.buttonPanel)
        self.buttonPanel.addListener(self.userInterface)
        
        yStart = 15
        spacing = 50
        for button in (newButton("Delete", yStart, DeleteTool()),
                        newButton("Gel", yStart + spacing, GelBlockTool()),
                        newButton("Normal", yStart + spacing*2, NormalBlockTool()),
                        newButton("LeftRamp", yStart + spacing*3, LeftRampTool()),
                        newButton("RightRamp", yStart + spacing*4, RightRampTool()),
                        newButton("Spring", yStart + spacing*5, SpringTool())
                        ):
            self.buttonPanel.addButton(button)
        
        self.userInterface.setScene(Scenery(BLOCKS_WIDE, BLOCKS_HIGH))
        
        self.score = Score((300, 10))
        Animation.animations.append(self.score)
        self.userInterface.addPassiveWidget(self.score)
        
        self.timer = Timer((600, 10))
        Animation.animations.append(self.timer)
        self.userInterface.addPassiveWidget(self.timer)
        
        self.nodeGraph = PathFinding.NodeGraph.NodeGraph(BLOCKS_WIDE, BLOCKS_HIGH * BLOCK_HEIGHT + Y_OFFSET + BLOCK_Y_OVERLAP)
        
        Event.addListener(Objects.Block.DONE_GHOSTING_IN_EVENT, self.nodeGraph)
        Event.addListener(Objects.Block.DONE_GHOSTING_OUT_EVENT, self.nodeGraph)
        
        
        self.physicsManager = Physics.OdePhysics.OdePhysicsManager()
        
        Event.addListener(Objects.Block.DONE_GHOSTING_IN_EVENT, self.physicsManager)
        Event.addListener(Objects.Block.DONE_GHOSTING_OUT_EVENT, self.physicsManager)
        
        self.pea = Objects.Pea.Pea(images["Pea-Standard"], (121, 50), self.nodeGraph, self.physicsManager)
        Animation.animations.append(self.pea)
        Animation.animations.append(self.physicsManager)
        
    
    def render(self, screen):
        screen.blit(images["Background"], (0,0))
        screen.blit(images["Plate"], (5, 520))
        self.userInterface.render(screen)
        self.nodeGraph.render(screen)
        self.pea.render(screen)
        self.physicsManager.render(screen)
        