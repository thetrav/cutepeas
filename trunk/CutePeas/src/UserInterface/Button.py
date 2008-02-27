from Images import images

class ButtonPanel:
    def __init__(self, pos):
        self.pos = pos
        self.buttons = []
        self.listeners = []
        self.selectedButton = None
        
    def addButton(self, button):
        self.buttons.append(button)
        button.addListener(self)
        
    def addListener(self, listener):
        self.listeners.append(listener)
        
    def buttonFired(self, button):
        for listener in self.listeners:
            listener.buttonFired(button)
    
    def render(self, screen):
        screen.blit(images["Tool-Background"], self.pos)
        for button in self.buttons:
            button.render(screen)
        
    def mouseMotion(self, event):
        for button in self.buttons:
            button.mouseMotion(event)
    
    def mouseDown(self, event):
        for button in self.buttons:
            button.mouseDown(event)
    
    def mouseUp(self, event):
        for button in self.buttons:
            button.mouseUp(event)
            
    def scrollButton(self, direction):
        buttons = self.buttons
        buttonCount = len(buttons)
        for x in xrange(buttonCount):
            if self.selectedButton == None or buttons[x] == self.selectedButton:
                self.deSelectEvent()
                buttonInd = x + direction
                if buttonInd < 0:
                    buttonInd = buttonCount-1
                elif buttonInd == buttonCount:
                    buttonInd = 0
                buttons[buttonInd].fireEvent()
                return
    
    def deSelectEvent(self):
        if self.selectedButton:
            self.selectedButton.deSelect()
            self.selectedButton = None
            
    def selectEvent(self, button):
        self.selectedButton = button
            

class Button:
    def __init__(self, buttonUpImage, buttonDownImage, buttonHoverImage, pos, width, height):
        self.listeners = []
        self.buttonDown = False
        self.mouseHover = False
        self.upImage = buttonUpImage
        self.downImage = buttonDownImage
        self.hoverImage = buttonHoverImage
        self.x = pos[0]
        self.y = pos[1]
        self.width = width
        self.height = height
        
    def render(self, screen):
        screen.blit(self.downImage if self.buttonDown else self.hoverImage if self.mouseHover else self.upImage, (self.x+2, self.y+2))
    
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
        
    def scrollButton(self, direction):
        pass
    
    def deSelectEvent(self):
        pass
        
class ToolButton (Button):
    def __init__(self, image, tool, pos, width, height):
        Button.__init__(self, images["Tool-"+image], images["Tool-"+image], images["Tool-"+image], pos, width, height)
        self.selectedImage = images["Tool-Selected"]
        self.tool = tool
        self.selected = False
    
    def render(self, screen):
        Button.render(self, screen)
        if self.selected:
            screen.blit(self.selectedImage, (self.x, self.y))
            
    def deSelect(self):
        self.selected = False
    
    def select(self):
        self.selected = True
        for listener in self.listeners:
            listener.selectEvent(self)
    
class TitleScreenButton (Button):
    def __init__(self, imageSetName, pos, width, height):
        Button.__init__(self, images["Button-"+imageSetName], images["Button-"+imageSetName+"-Down"], images["Button-"+imageSetName+"-Hover"], pos, width, height)
    