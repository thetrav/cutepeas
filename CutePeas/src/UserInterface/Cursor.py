import pygame.mouse

from Images import images

class Cursor:
    def __init__(self, image, scene):
        self.image = image
        self.x = 0
        self.y = 0
        self.tool = None
        self.slot = None
        self.scene = scene
        pygame.mouse.set_visible(False)
    
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
        if self.tool:
            self.slot = self.scene.pickSlot(event.pos)
            