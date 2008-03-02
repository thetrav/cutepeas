from UserInterface import Text

class NodeGraph:
    def __init__(self, blocksWide, blocksHigh):
        self.slots = []
        for x in xrange(blocksWide*2+1):
            self.slots.append([])
            for y in xrange(blocksHigh*2):
                self.slots[x].append(createSlot(x,y))
            self.slots[x].append(BottomNodeSlot([x,y+1]))
    
    def render(self, screen):
        for slots in self.slots:
            for slot in slots:
                slot.render(screen)
    
class NodeSlot:
    def __init__(self, pos):
        self.blocks = []
        self.blockCount = 0
        self.pos = pos
        self.symbol = "BROKEN!"
    
    def render(self, screen):
        drawNode(self.symbol, self.pos, screen)

class CenterNodeSlot(NodeSlot):
    def __init__(self, pos):
        NodeSlot.__init__(self, pos)
        self.symbol = "0"
    
    def isTraversible(self):
        # Centre slots can only ever be traversed via ramps
        return self.blockCount > 0 and self.blocks[0].type == "ramp"

# as far as path finding goes there's little difference between vertical and horizontal slots
class FaceNodeSlot(NodeSlot):
    def __init__(self, pos):
        NodeSlot.__init__(self, pos)
        self.symbol = "[]"
        
    def isTraversible(self):
        # Face slots can only ever be traversed via single blocks.
        return  self.blockCount == 1
    
class CornerNodeSlot(NodeSlot):
    def __init__(self, pos):
        NodeSlot.__init__(self, pos)
        self.symbol = "+"
        
    def isTraversible(self):
        return self.blockCount < 0
    
        
class BottomNodeSlot(NodeSlot):
    def __init__(self, pos):
        NodeSlot.__init__(self, pos)
        self.symbol = "_"
        
    def isTraversible(self):
        return self.BlockCount == 0
    
def createSlot(xIndex, yIndex):
    pos = [xIndex, yIndex]
    if isEven(xIndex):
        if isEven(yIndex):
            return CornerNodeSlot(pos)
        else:
            return FaceNodeSlot(pos)
    else:
        if isEven(yIndex):
            return FaceNodeSlot(pos)
        else:
            return CenterNodeSlot(pos)
    
def drawNode(text, pos, screen):
    aPos = (pos[0]*50, pos[1]*50)
    Text.renderText(text, aPos, screen, (255,0,0), "NODE_FONT")
    
def isEven(num):
    return num % 2 == 0 