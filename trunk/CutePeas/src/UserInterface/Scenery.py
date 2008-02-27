from Images import images
import math
from Animation import animations
import random

BLOCK_WIDTH = 71
BLOCK_HEIGHT = 50
BLOCK_HEIGHT_REAL = 61
BLOCK_Y_OVERLAP = BLOCK_HEIGHT_REAL - BLOCK_HEIGHT

NUM_BLOCKS = 9

X_OFFSET = 50
X_BORDER = X_OFFSET + NUM_BLOCKS * BLOCK_WIDTH

Y_OFFSET = 90
Y_BORDER = Y_OFFSET + NUM_BLOCKS * BLOCK_HEIGHT

def posToIndex(x, y, slots):
    i = singlePosToIndex(x, X_OFFSET, BLOCK_WIDTH)
    j = singlePosToIndex(y, Y_OFFSET, BLOCK_HEIGHT)
    # check for overlap
    distanceFromTop = y - singleIndexToPos(j, Y_OFFSET, BLOCK_HEIGHT)
    if distanceFromTop < BLOCK_Y_OVERLAP  and j > 0 and slots[i][j-1].block:
        j = j-1
    return (i,j)

def singlePosToIndex(pos, offset, gap):
    return int((pos - offset)/gap)

def indexToPos(x, y):
    i = singleIndexToPos(x, X_OFFSET, BLOCK_WIDTH)
    j = singleIndexToPos(y, Y_OFFSET, BLOCK_HEIGHT)
    return (i,j)

def singleIndexToPos(pos, offset, gap):
    return pos * gap + offset

class Scenery:
    def __init__(self):
        self.hoveredSlot = None
        self.slots = []
        self.mouseHover = False
        
        self.clouds = [Cloud("Cloud1", 10, 20), Cloud("Cloud2", 100, 350), Cloud("Cloud3", 600, 200)]
        
        for cloud in self.clouds:
            animations.append(cloud)
        
        for x in xrange(NUM_BLOCKS):
            self.slots.append([])
            for y in xrange(NUM_BLOCKS):
                self.slots[x].append(Slot(indexToPos(x,y)))
    
    def pickSlot(self, pos):
        x = pos[0]
        y = pos[1]
        if not self.mouseIsInArea(x,y):
            return None
        else:
            index = posToIndex(x, y, self.slots)
            return self.slots[index[0]][index[1]]
    
    def mouseIsInArea(self, x, y):
        return x > X_OFFSET and x < X_BORDER and y > Y_OFFSET and y < Y_BORDER
    
    def render(self, screen):
        for cloud in self.clouds:
            cloud.render(screen)
        for x in xrange(NUM_BLOCKS):
            for yMin in xrange(NUM_BLOCKS):
                y = NUM_BLOCKS - yMin -1
                if self.slots[x][y]:
                    self.slots[x][y].render(screen) 

class Slot:
    def __init__(self, pos):
        self.block = None
        self.x = pos[0]
        self.y = pos[1]
        
    def render(self, screen):
        if self.block:
            self.block.render(screen)
        
    def addBlock(self, block):
        block.x = self.x
        block.y = self.y
        self.block = block
        block.ghostIn()
    
    def deleteBlock(self):
        if self.block and not self.block.isGhosting():
            self.block.ghostOut(self)
    
    def ghostedOut(self, block):
        self.block = None

MIN_TIME = 1000
MAX_TIME = 4000
WIND_SPEED = 0.00001

class Cloud:
    def __init__(self, image, x, y):
        self.image = images[image]
        self.x = x
        self.y = y
        self.maxX = 800
        self.minX = -300
        self.xVel = 0
        self.maxSpeed = 0.01
        self.timer = 0
        self.windForce = 0
        
    def update(self, timeD):
        self.timer = self.timer - timeD
        if self.timer <= 0 :
            self.timerReached()
        
        self.xVel = self.xVel + self.windForce
        if self.xVel > self.maxSpeed:
            self.xVel = self.maxSpeed
        elif self.xVel < -self.maxSpeed:
            self.xVel = -self.maxSpeed
        
        self.x = self.x + timeD * self.xVel
        if self.x < self.minX:
            self.x = self.maxX
        elif self.x > self.maxX:
            self.x = self.minX
    
    def timerReached(self):
        rand = random.random()
        if rand >0.66:
            self.windForce = WIND_SPEED
        elif rand < 0.33:
            self.windForce = -WIND_SPEED
        else :
            self.windForce = 0
        
        self.timer = random.randint(MIN_TIME, MAX_TIME)
    
    def render(self, screen):
        screen.blit(self.image, (self.x, self.y))
