from Constants import *
import pygame.draw
import Text
import Coordinates

# converts a position in the ODE universe (relative to an arbitrary fixed origin) 
# to a position in the pixel universe (which is relative to the view port)
def odePosToPixelPos(odePos):
    return Coordinates.odePosToPixelPos((odePos[X] + globalViewPort.odeOffset[X], odePos[Y] + globalViewPort.odeOffset[Y]))

# converts a position in the pixel universe (relative to the view port)
# to a position in the ODE universe (which is relative to an arbitrary fixed origin)
def pixelsPosToOdePos(pixelPos):
    unScrolledPixelPos = (pixelPos[X] - Coordinates.odeToPixels(globalViewPort.odeOffset[X]),
                          pixelPos[Y] - Coordinates.odeToPixels(globalViewPort.odeOffset[Y]))
    return Coordinates.pixelPosToOdePos(unScrolledPixelPos)


class ViewPort:
    def __init__(self):
        self.odeOffset = [0,0]
        self.odeVelX = 0
        self.odeVelY = 0
    
    def update(self, timeD):
        self.odeOffset[X] += self.odeVelX * timeD
        self.odeOffset[Y] += self.odeVelY * timeD
        if self.odeOffset[Y] < 0:
            self.odeOffset[Y] = 0
            
    def mouseMoved(self, yPixelPos):
        if yPixelPos < UP_SCROLL_LINE:
            self.odeVelY = Y_SCROLL_SPEED * SCROLL_LINE_HEIGHT / (yPixelPos+1)
        elif yPixelPos > DOWN_SCROLL_LINE:
            distancePastLine = yPixelPos - DOWN_SCROLL_LINE
            self.odeVelY = -Y_SCROLL_SPEED * SCROLL_LINE_HEIGHT / (SCROLL_LINE_HEIGHT - distancePastLine + 1)
        else:
            self.odeVelY = 0
        
    def blit(self, screen, image, gameCoords):
        screen.blit(image, odePosToPixelPos(gameCoords))
        
    def drawLine(self, screen, color, gameCoords1, gameCoords2, thickness=0):
        pygame.draw.line(screen, color, odePosToPixelPos(gameCoords1), odePosToPixelPos(gameCoords2), 3)
        
    def drawRect(self, screen, color, odeRect):
        pixelRect = (Coordinates.odeToPixels(odeRect[X] + self.odeOffset[X]),
                     Coordinates.odeToPixels(odeRect[Y] + self.odeOffset[Y]), 
                     Coordinates.odeToPixels(odeRect[2]), 
                     Coordinates.odeToPixels(odeRect[3]))
        pygame.draw.rect(screen, color, pixelRect)
        
    def drawCircle(self, screen, color, odePos, pixelRadius, pixelThickness = 0):
        pygame.draw.circle(screen, color , odePosToPixelPos(odePos), pixelRadius, pixelThickness)
    
    def renderText(self, text, odePos, screen, color, font="DEFAULT_FONT"):
        Text.renderText(text, odePosToPixelPos(odePos), screen, color, font)
    
    def drawPolygon(self, screen, color, odePoints, thickness):
        pixelPoints = [odePosToPixelPos(point) for point in odePoints]
        pygame.draw.polygon(screen, color, pixelPoints, thickness)
    
globalViewPort = ViewPort()

def graphFinalOutputReport():
    headerString = 'scrollHeight'
    for cursorHeight in xrange(60):
        headerString += '|' + str(cursorHeight*10)
    print headerString
    for scrollHeight in xrange(10):
        rowString = str(scrollHeight)
        for cursorHeight in xrange(60):
            globalViewPort.odeOffset[Y] = scrollHeight*10
            cursorPos = (1,600 - cursorHeight*10)
            rowString += '|' + str(Coordinates.snapOdePosToBoxOdePos(pixelsPosToOdePos(cursorPos))[Y])
        print rowString

def graphOffsetOutputReport():
    headerString = 'scrollHeight'
    for cursorHeight in xrange(60):
        headerString += '|' + str(cursorHeight*10)
    print headerString
    for scrollHeight in xrange(10):
        rowString = str(scrollHeight*10)
        for cursorHeight in xrange(60):
            globalViewPort.odeOffset[Y] = scrollHeight*10
            cursorPos = (1,600 - cursorHeight*10)
            rowString += '|' + str(pixelsPosToOdePos(cursorPos)[Y])
        print rowString
        
def snapReport():
    print 'yPosition|snappedPos'
    for yStep in xrange(120):
        cursorPos = (1,600 - yStep*10)
        snapped = pixelsPosToOdePos(cursorPos)
        print cursorPos[Y], '|', snapped[Y]

def dataPointAnalysis(scroll, cursor):
    print 'analysis for scroll',scroll,' cursor',cursor
    globalViewPort.odeOffset[Y] = scroll
    odePos = pixelsPosToOdePos((1,cursor))
    print 'odePos=',odePos
    snappedPos = Coordinates.snapOdePosToBoxOdePos(odePos)
    print 'snapped=',snappedPos

snapReport()
