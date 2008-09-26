import UserInterface.Scroll

class Flag:
    def __init__(self, pos):
        self.poleImage = None
        self.flagImage = None
        self.pos = pos
        self.completion = 0.0
        
    def render(self, screen):
        polePos = None # offset
        UserInterface.Scroll.globalViewPort.blit(screen, self.poleImage, polePos)
        
        if self.flagImage:
            flagPos = None # offset
            UserInterface.Scroll.globalViewPort.blit(screen, self.flagImage, flagPos)
    
    def jumpPea(self, pea):
        pass