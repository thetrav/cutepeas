from Images import images

class Cursor:
    def __init__(self, image):
        self.image = image
        self.x = 0
        self.y = 0
        self.tool = None
    
    def render(self, screen):
        if self.tool:
            screen.blit(self.tool.toolImage, (self.x, self.y))
        screen.blit(self.image, (self.x, self.y))
    
    def toolChanged(self, tool):
        self.tool = tool
    
    def toolUsed(self):
        tool.invokeTool()
    
    def mouseMotion(self, event):
        self.x = event.pos[0]
        self.y = event.pos[1]