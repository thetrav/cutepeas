from Images import images
import Text

class Timer:
    def __init__(self):
        self.time = 0
        
    def update(self, timeD):
        self.time = self.time + timeD*3
        
    def render(self, screen, pos):
        screen.blit(images["Icon-Time"], pos)
        Text.renderText(self.getFormattedTime(), (pos[0]+30, pos[1]), screen)
        
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