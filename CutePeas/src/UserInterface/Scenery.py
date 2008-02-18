from Images import images
import math

BLOCK_WIDTH = 71
BLOCK_HEIGHT = 61

NUM_BLOCKS = 9

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
        for x in xrange(NUM_BLOCKS):
            for y in xrange(NUM_BLOCKS):
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
        self.block.ghostOut(self)
    
    def ghostedOut(self, block):
        self.block = None
