import pygame.mouse
from Constants import *
import Scroll

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
        tool.positionChanged(Scroll.rePos(self.pos))
        
    def toolCleared(self):
        self.tool = None
    
    def toolUsed(self):
        if self.tool:
            self.tool.invokeTool()
    
    def mouseMotion(self, event):
        self.pos = (event.pos[X], event.pos[Y])
        if self.tool:
            self.tool.positionChanged(Scroll.rePos(self.pos))
        if self.pos[Y] < UP_SCROLL_LINE:
            Scroll.globalViewPort.yVel = Y_SCROLL_SPEED
        elif self.pos[Y] > DOWN_SCROLL_LINE:
            Scroll.globalViewPort.yVel = -Y_SCROLL_SPEED
        else:
            Scroll.globalViewPort.yVel = 0