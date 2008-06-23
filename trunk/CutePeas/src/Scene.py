import Coordinates
import Event
import Objects.Block
from Constants import *

def toKey(pos):
    return str(pos)
   
class Scene:
    def __init__(self, nodeGraph, physicsManager):
        self.blocks = []
        self.createGrid()
        self.flags = {}
        self.peas = []
        self.nodeGraph = nodeGraph
        self.physicsManager = physicsManager
        Event.addListener(Objects.Block.DONE_GHOSTING_IN_EVENT, self)
        Event.addListener(Objects.Block.DONE_GHOSTING_OUT_EVENT, self)
    
    def getBlock(self, index):
        return self.blocks[index[X]][index[Y]]
    
    def setBlock(self, index, block):
        self.blocks[index[X]][index[Y]] = block
    
    def createGrid(self):
        for x in xrange(9):
            self.blocks.append([])
            for y in xrange(9):
                self.blocks[x].append(None)
    
    def render(self, screen):
        for column in self.blocks:
            for block in reversed(column):
                if block != None:
                    block.render(screen)
        self.nodeGraph.render(screen)
        for pea in self.peas:
            pea.render(screen)
    
    def dispose(self):
        for pea in self.peas:
            pea.dispose()
        for column in self.blocks:
            for block in column:
                if block != None:
                    block.dispose()
        self.physicsManager.dispose()
        Event.removeListener(Objects.Block.DONE_GHOSTING_IN_EVENT, self)
        Event.removeListener(Objects.Block.DONE_GHOSTING_OUT_EVENT, self)
    
    def inBlockArea(self, pos):
        return pos[X] >= 0 and pos[Y] >= 0 and pos[X] < len(self.blocks) and pos[Y] < len(self.blocks[pos[X]])
    
    def canPlaceBlock(self, pixelPos):
        pos = Coordinates.pixelPosToBoxIndex(pixelPos)
        print 'can place at:',pixelPos,' index:',pos
        return self.inBlockArea(pos) and self.getBlock(pos) == None 
    
    def placeBlock(self, pos, block):
        block.pos = pos
        index = Coordinates.pixelPosToBoxIndex(pos)
        self.setBlock(index, block)
        block.ghostIn()
        
    def canRemoveBlock(self, pixelPos):
        pos = Coordinates.pixelPosToBoxIndex(pixelPos)
        return self.inBlockArea(pos) and self.getBlock(pos) != None and not self.getBlock(pos).isGhosting()
    
    def removeBlock(self, pixelPos):
        pos = Coordinates.pixelPosToBoxIndex(pixelPos)
        self.getBlock(pos).ghostOut()
        
    def eventFired(self, id, block):
        if id == Objects.Block.DONE_GHOSTING_IN_EVENT:
            self.nodeGraph.placeBlock(block)
            self.physicsManager.placeBlock(block)
        elif id == Objects.Block.DONE_GHOSTING_OUT_EVENT:
            index = Coordinates.pixelPosToBoxIndex(block.pos)
            self.nodeGraph.removeBlock(block)
            self.physicsManager.removeBlock(block)
            self.setBlock(index, None)
    
    def canPlaceFlag(self, pos):
        return not self.flags.has_key(toKey(pos))
    
    def placeFlag(self, pos, flag):
        self.flags[toKey(pos)] = flag
        self.nodeGraph.placeFlag(flag)
    
    def addPea(self, pea):
        self.peas.append(pea)
    