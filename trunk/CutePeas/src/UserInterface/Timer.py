from Images import images
import Text

class Timer:
    def __init__(self, pixelPos):
        self.time = 0
        self.pixelPos = pixelPos
        
    def update(self, timeD):
        self.time = self.time + timeD*3
        
    def render(self, screen):
        screen.blit(images["Icon-Time"], self.pixelPos)
        Text.renderText(self.getFormattedTime(), (self.pixelPos[0]+30, self.pixelPos[1]), screen)
        
    def getFormattedTime(self):
        return str(self.getMinutes()) + ":" + self.formatSeconds(self.getSeconds())
    
    def formatSeconds(self, seconds):
        if seconds < 10:
            return "0"+str(seconds)
        return str(seconds)
    
    def getSeconds(self):
        return int((self.time/1000) % 60)
    
    def getMinutes(self):
        return int((self.time/60000))