from Images import images
from UserInterface.Button import *
from UserInterface.Tool import *
from UserInterface.Scenery import *
from Animation import *
from UserInterface.Score import *
from UserInterface.Timer import *


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
        
        self.userInterface.setScene(Scenery())
        
        self.score = Score((300, 10))
        animations.append(self.score)
        self.userInterface.addPassiveWidget(self.score)
        
        self.timer = Timer((600, 10))
        animations.append(self.timer)
        self.userInterface.addPassiveWidget(self.timer)
    
    def render(self, screen):
        screen.blit(images["Background"], (0,0))
        screen.blit(images["Plate"], (5, 520))
        self.userInterface.render(screen)
        