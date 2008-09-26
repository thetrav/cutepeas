import pygame.mouse
from Constants import *
import Scroll

class Cursor:
    def __init__(self, image):
        self.image = image
        self.pixelPos = (0,0)
        self.tool = None
        self.slot = None
        self.scene = None
        pygame.mouse.set_visible(False)
    
    def setScene(self, scene):
        self.scene = scene
    
    def render(self, screen):
        if self.tool:
            self.tool.render(screen)
            screen.blit(self.tool.cursorIcon, self.pixelPos)
        else:
            screen.blit(self.image, self.pixelPos)
    
    def toolChanged(self, tool):
        self.tool = tool
        tool.positionChanged(Scroll.pixelsPosToOdePos(self.pixelPos))
        
    def toolCleared(self):
        self.tool = None
    
    def toolUsed(self):
        if self.tool:
            self.tool.invokeTool()
    
    def mouseMotion(self, event):
        self.pixelPos = (event.pos[X], event.pos[Y])
        Scroll.globalViewPort.mouseMoved(self.pixelPos[Y])
        if self.tool:
            self.tool.positionChanged(Scroll.pixelsPosToOdePos(self.pixelPos))