from Constants import *
import pygame.draw
import Text

def rePos(pos):
    return (pos[X] + globalViewPort.offset[X], pos[Y] + globalViewPort.offset[Y])

class ViewPort:
    def __init__(self):
        self.offset = [0,0]
        self.xVel = 0
        self.yVel = 0
    
    def update(self, timeD):
        self.offset[X] += self.xVel * timeD
        self.offset[Y] += self.yVel * timeD
        if self.offset[Y] < 0:
            self.offset[Y] = 0
        
    def blit(self, screen, image, gameCoords):
        screen.blit(image, rePos(gameCoords))
        
    def drawLine(self, screen, color, gameCoords1, gameCoords2, thickness=0):
        pygame.draw.line(screen, color, rePos(gameCoords1), rePos(gameCoords2), 3)
        
    def drawRect(self, screen, color, rect):
        pygame.draw.rect(screen, color, (rect[X] + self.offset[X], rect[Y] + self.offset[Y], rect[2], rect[3]))
        
    def drawCircle(self, screen, color, pos, radius, thickness = 0):
        pygame.draw.circle(screen, color , rePos(pos), thickness)
    
    def renderText(self, text, pos, screen, color, font):
        Text.renderText(text, pos, screen, color, font)
        
    
globalViewPort = ViewPort()