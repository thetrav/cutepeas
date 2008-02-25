from Images import images
from UserInterface import Text

class TitleScreen:
    def __init__(self, userInterface):
        self.userInterface = userInterface
        self.highScoreList = HighScoreList((100,100))
    
    def render(self, screen):
        screen.blit(images["Background"], (0,0))
        screen.blit(images["Logo"], (10,10))
        screen.blit(images["Plate"], (5, 520))
        self.highScoreList.render(screen)

LINE_WIDTH = 30
LINE_SPACING = 20
        
class HighScoreList:
    def __init__(self, pos):
        self.scores = [("The Trav","6:33"),("Kamal", "7:00"), ("Rory", "7:01"), ("Scott", "7:15")]
        self.pos = pos
        
    def render(self, screen):
        Text.renderText("High Scores", self.pos, screen, (250,220,0), "TITLE_FONT")
        xPos = self.pos[0]
        yPos = self.pos[1] + 60
        for score in self.scores:
            renderString = score[0] + ((LINE_WIDTH - len(score[0]) - len(score[1])) * ".") + score[1]
            Text.renderText(renderString, (xPos, yPos), screen, (0,100,0))
            yPos = yPos + LINE_SPACING