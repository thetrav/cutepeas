import Images
import Text
import Event

SCORE_AWARDED_EVENT = "score awarded event"

class Score:
    def __init__(self, pos):
        self.score = 0
        self.toAdd = 0
        self.addRate = 1
        self.pos = pos
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
        screen.blit(Images.images["Happy-Points"], self.pos)
        Text.renderText(str(self.score), (self.pos[0]+30, self.pos[1]), screen)