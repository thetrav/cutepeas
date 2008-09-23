import Images
import Text
import Event

SCORE_AWARDED_EVENT = "score awarded event"
SCORE_TEXT_X_OFFSET = 30

class Score:
    def __init__(self, pixelPos):
        self.score = 0
        self.toAdd = 0
        self.addRate = 1
        self.pixelPos = pixelPos
        Event.addListener(SCORE_AWARDED_EVENT, self)
        
    def addScore(self, newPoints):
        self.toAdd += newPoints
        
    def update(self, timeD):
        self.addRate = 1 + self.toAdd/100
        add = int(timeD * self.addRate)
        if add > self.toAdd:
            add = self.toAdd
        self.toAdd = self.toAdd - add
        self.score = self.score + add
        
    def eventFired(self, id, source):
        if id == SCORE_AWARDED_EVENT:
            self.addScore(source)
    
    def render(self, screen):
        screen.blit(Images.images["Happy-Points"], self.pixelPos)
        Text.renderText(str(self.score), (self.pixelPos[0]+SCORE_TEXT_X_OFFSET, self.pixelPos[1]), screen)