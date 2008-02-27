from Images import images
import Text

class Score:
    def __init__(self, pos):
        self.score = 0
        self.toAdd = 0
        self.addRate = 1
        self.pos = pos
        
    def addScore(self, newPoints):
        self.toAdd = self.toAdd + newPoints
        
    def update(self, timeD):
        self.addRate = 1 + self.toAdd/100
        add = int(timeD * self.addRate)
        if add > self.toAdd:
            add = self.toAdd
        self.toAdd = self.toAdd - add
        self.score = self.score + add
        
    def render(self, screen):
        screen.blit(images["Happy-Points"], self.pos)
        Text.renderText(str(self.score), (self.pos[0]+30, self.pos[1]), screen)