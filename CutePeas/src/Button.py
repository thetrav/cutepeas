class Button:
    def __init__(self, buttonUpImage, buttonDownImage, x, y, width, height):
        self.listeners = []
        self.buttonDown = False
        self.mouseHover = False
        self.upImage = buttonUpImage
        self.downImage = buttonDownImage
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        
    def render(self, screen):
        screen.blit(self.downImage if self.buttonDown else self.upImage, (self.x, self.y))
    
    def mouseDown(self, event):
        self.buttonDown = True if self.mouseHover else False
        print "mouseDown="+str(self.buttonDown)
    
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
        print "mouse entered"
    
    def mouseExit(self):
        self.mouseHover = False
        print "mouse exited"
    
    def fireEvent(self):
        print "firing event"
        for listener in self.listeners:
            listener.buttonFired(self)
            
    def addListener(self, listener):
        self.listeners.append(listener)
    
    
    