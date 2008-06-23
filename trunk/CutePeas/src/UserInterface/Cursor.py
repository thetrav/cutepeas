import pygame.mouse
from Constants import *

class Cursor:
    def __init__(self, image):
        self.image = image
        self.pos = (0,0)
        self.tool = None
        self.slot = None
        self.scene = None
        pygame.mouse.set_visible(False)
    
    def setScene(self, scene):
        self.scene = scene
    
    def render(self, screen):
        if self.tool:
            self.tool.render(screen)
            screen.blit(self.tool.cursorIcon, self.pos)
        else:
            screen.blit(self.image, self.pos)
    
    def toolChanged(self, tool):
        self.tool = tool
        tool.positionChanged(self.pos)
        
    def toolCleared(self):
        self.tool = None
    
    def toolUsed(self):
        if self.tool:
            self.tool.invokeTool()
    
    def mouseMotion(self, event):
        self.pos = (event.pos[X], event.pos[Y])
        if self.tool:
            self.tool.positionChanged(self.pos)
            