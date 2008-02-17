class Button:
    def __init__(self, buttonUpImage, buttonDownImage, selectedImage, tool, x, y, width, height):
        self.listeners = []
        self.buttonDown = False
        self.mouseHover = False
        self.selected = False
        self.upImage = buttonUpImage
        self.downImage = buttonDownImage
        self.selectedImage = selectedImage
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.tool = tool
        
    def render(self, screen):
        screen.blit(self.downImage if self.buttonDown else self.upImage, (self.x+2, self.y+2))
        if self.selected:
            screen.blit(self.selectedImage, (self.x, self.y))
    
    def mouseDown(self, event):
        self.buttonDown = True if self.mouseHover else False
    
    def mouseUp(self, event):
        if self.mouseHover and self.buttonDown :
            self.fireEvent()
        self.buttonDown = False
    
    def mouseMotion(self, event):
        mouse = event.pos
        if self.mouseHover :
            if not self.mouseIsIn(mouse[0], mouse[1]):
                self.mouseExit()
        else :
            if self.mouseIsIn(mouse[0], mouse[1]):
                self.mouseEnter()
    
    def mouseIsIn(self, mouseX, mouseY):
        return mouseX > self.x and mouseX < self.x + self.width and mouseY > self.y and mouseY < self.y + self.height
    
    def mouseEnter(self):
        self.mouseHover = True
    
    def mouseExit(self):
        self.mouseHover = False
    
    def fireEvent(self):
        for listener in self.listeners:
            listener.buttonFired(self)
            
    def addListener(self, listener):
        self.listeners.append(listener)
    
    def deSelect(self):
        self.selected = False
    
    def select(self):
        self.selected = True
    