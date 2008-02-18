from Images import images

class Block:
    def __init__(self, image):
        self.image = images[image]
        self.x = 0
        self.y = 0
    
    def render(self, screen):
        screen.blit(self.image, (self.x, self.y))
    
    