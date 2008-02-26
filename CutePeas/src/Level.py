from Images import images
from UserInterface.Button import *
from UserInterface.Tool import *


def newButton(image, yPos, tool):
    return ToolButton(image, tool, (725, yPos), 47, 47)

class BasicLevel:
    def __init__(self, userInterface):
        self.userInterface = userInterface
        self.buttonPanel = ButtonPanel((720, 10))
        
        userInterface.addActiveWidget(self.buttonPanel)
        
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
    
    def render(self, screen):
        screen.blit(images["Background"], (0,0))
        screen.blit(images["Plate"], (5, 520))