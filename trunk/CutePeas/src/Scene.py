import Coordinates
import Event
import Objects.Block
from Constants import *

def toKey(pos):
    return str((pos[X], pos[Y]))

# note, this is deliberately backwards because we want a reversed list
def compareBlockKeys(a, b):
    posA = a[1:-1].split(',')
    posB = b[1:-1].split(',')
    return int(float(posB[Y])-float(posA[Y]))
   
class Scene:
    def __init__(self, nodeGraph, physicsManager):
        self.blocks = {}
        self.flags = {}
        self.peas = []
        self.nodeGraph = nodeGraph
        self.physicsManager = physicsManager
        Event.addListener(Objects.Block.DONE_GHOSTING_IN_EVENT, self)
        Event.addListener(Objects.Block.DONE_GHOSTING_OUT_EVENT, self)
    
    def getBlock(self, odePos):
        return self.blocks[toKey(odePos)]
    
    def hasBlockAt(self, odePos):
        return self.blocks.has_key(toKey(odePos))
        
    def setBlock(self, odePos, block):
        self.blocks[toKey(odePos)] = block
    
    def render(self, screen):
        for key in sorted(self.blocks.keys(), compareBlockKeys):
            self.blocks[key].render(screen)
        self.nodeGraph.render(screen)
        for pea in self.peas:
            pea.render(screen)
    
    def dispose(self):
        for pea in self.peas:
            pea.dispose()
            for key in self.blocks.keys():
                self.blocks[key].dispose()
        self.physicsManager.dispose()
        Event.removeListener(Objects.Block.DONE_GHOSTING_IN_EVENT, self)
        Event.removeListener(Objects.Block.DONE_GHOSTING_OUT_EVENT, self)
    
    def canPlaceBlock(self, odePos):
        return not self.hasBlockAt(odePos)
                                                                                    
    def placeBlock(self, odePos, block):
        block.odePos = odePos
        self.setBlock(odePos, block)
        block.ghostIn()
        
    def canRemoveBlock(self, odePos):
        return self.hasBlockAt(odePos) and not self.getBlock(odePos).isGhosting()
    
    def removeBlock(self, odePos):
        self.getBlock(odePos).ghostOut()
        
    def eventFired(self, id, block):
        if id == Objects.Block.DONE_GHOSTING_IN_EVENT:
            self.nodeGraph.placeBlock(block)
            self.physicsManager.placeBlock(block)
        elif id == Objects.Block.DONE_GHOSTING_OUT_EVENT:
            self.nodeGraph.removeBlock(block)
            self.physicsManager.removeBlock(block)
            self.blocks.pop(toKey(block.odePos))
    
    def addPea(self, pea):
        self.peas.append(pea)
    