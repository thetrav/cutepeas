from Images import images
import math
from Animation import animations

BLOCK_WIDTH = 71
BLOCK_HEIGHT = 50

NUM_BLOCKS = 10

X_OFFSET = 15
X_BORDER = X_OFFSET + NUM_BLOCKS * BLOCK_WIDTH

Y_OFFSET = 15
Y_BORDER = Y_OFFSET + NUM_BLOCKS * BLOCK_HEIGHT

def snap(x, y):
    return (math.floor(x-X_OFFSET/BLOCK_WIDTH)*BLOCK_WIDTH + X_OFFSET, math.floor(y-Y_OFFSET/BLOCK_HEIGHT)*BLOCK_HEIGHT + Y_OFFSET)

class Scenery:
    def __init__(self):
        self.hoveredSlot = None
        self.slots = []
        self.mouseHover = False
        
        self.clouds = [Cloud("Cloud1", 10, 20), Cloud("Cloud2", 100, 400), Cloud("Cloud3", 600, 200)]
        
        for cloud in self.clouds:
            animations.append(cloud)
        
        for x in xrange(NUM_BLOCKS):
            self.slots.append([])
            for y in xrange(NUM_BLOCKS):
                self.slots[x].append(Slot(snap(x,y)))
    
    def mouseMotion(self, event, tool):
        x = event.pos[0]
        y = event.pos[1]
        if not self.mouseIsInArea(x,y):
            if self.mouseHover:
                self.mouseLeavesArea()
        else:
            if not self.mouseHover:
                self.mouseEntersArea()
            hoveredSlot = self.slots[self.xToSlotIndex(x)][self.yToSlotIndex(y)]
            if hoveredSlot != self.hoveredSlot:
                if self.hoveredSlot:
                    self.hoveredSlot.mouseLeaves()
                hoveredSlot.mouseEnters(tool)
                self.hoveredSlot = hoveredSlot
    
    def xToSlotIndex(self, x):
        return self.toSlotIndex(x, X_OFFSET, BLOCK_WIDTH)
    
    def yToSlotIndex(self, y):
        return self.toSlotIndex(y, Y_OFFSET, BLOCK_HEIGHT)
        
    def toSlotIndex(self, pos, offset, blockSize):
        return int(math.floor((pos-offset)/blockSize))
    
    def mouseIsInArea(self, x, y):
        return x > X_OFFSET and x < X_BORDER and y > Y_OFFSET and y < Y_BORDER
    
    def mouseLeavesArea(self):
        self.mouseHover = False
        if self.hoveredSlot:
            self.hoveredSlot.mouseLeaves()
            self.hoveredSlot = None
    
    def toolCleared(self):
        if self.hoveredSlot:
            self.hoveredSlot.toolCleared()
    
    def mouseEntersArea(self):
        self.mouseHover = True
    
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
        self.tool = None
        self.mouseHover = False
        self.x = pos[0]
        self.y = pos[1]
        
    def render(self, screen):
        if self.block:
            self.block.render(screen)
        elif self.tool:
            self.tool.render(screen)
        
    def mouseLeaves(self):
        self.toolCleared()
            
    def toolCleared(self):
        if self.tool:
            self.tool.slot = None
            self.tool = None
    
    def mouseEnters(self, tool):
        if tool:
            self.tool = tool
            tool.setPos(self.x, self.y)
            tool.slot = self
    
    def addBlock(self, block):
        self.block = block
        block.ghostIn()
    
    def deleteBlock(self):
        if self.block:
            self.block.ghostOut(self)
    
    def ghostedOut(self, block):
        self.block = None

class Cloud:
    def __init__(self, image, x, y):
        self.image = images[image]
        self.x = x
        self.y = y
        self.maxX = 800
        self.minX = -200
        self.speed = 0
        self.maxSpeed = 0.01
        self.timer = 0
        
    def update(self, timeD):
        self.timer = self.timer - timeD
        if self.timer <= 0 :
            self.timerReached()
        self.x = self.x + timeD * self.speed
        if self.x < self.minX:
            self.x = self.minX
        elif self.x > self.maxX:
            self.x = self.maxX
    
    def timerReached(self):
        #decide whether to pause or to move
        #set new timer and speed 
        pass
    
    def render(self, screen):
        screen.blit(self.image, (self.x, self.y))
