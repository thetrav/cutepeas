import pygame.mouse

from Images import images

class Cursor:
    def __init__(self, image):
        self.image = image
        self.x = 0
        self.y = 0
        self.tool = None
        self.slot = None
        self.scene = None
        pygame.mouse.set_visible(False)
    
    def setScene(self, scene):
        self.scene = scene
    
    def render(self, screen):
        if self.tool:
            if self.slot:
                self.tool.render(screen, self.slot)
            screen.blit(self.tool.cursorIcon, (self.x, self.y))
        else:
            screen.blit(self.image, (self.x, self.y))
    
    def toolChanged(self, tool):
        self.tool = tool
        
    def toolCleared(self):
        self.tool = None
    
    def toolUsed(self):
        if self.tool:
            self.tool.invokeTool(self.slot)
    
    def mouseMotion(self, event):
        self.x = event.pos[0]
        self.y = event.pos[1]
        if self.tool and self.scene:
            self.slot = self.scene.pickSlot(event.pos)
            