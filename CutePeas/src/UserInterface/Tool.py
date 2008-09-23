import Images 
import Objects.Block
from Constants import *
import Coordinates


class Tool:
    def __init__(self, cursorIcon, scene):
        self.cursorIcon = cursorIcon
        self.listeners = []
        self.odePos = (0,0,0)
        self.scene = scene
    
    def positionChanged(self, newPos):
        self.odePos = (newPos[X], newPos[Y], 0)
    
    def invokeTool(self):
        pass
    
    def render(self, screen):
        pass
    
class SnapTool(Tool):
    def __init__(self, image, scene):
        Tool.__init__(self, image, scene)
        
    def positionChanged(self, odePos):
        snappedOdePos = Coordinates.snapOdePosToBoxOdePos(odePos)
        oldY = self.block.odePos[Y]
        newY = snappedOdePos[Y]
        if oldY != newY:
            print 'y pos changed from:',oldY,' to:',newY
        Tool.positionChanged(self, snappedOdePos)
        self.block.odePos = snappedOdePos 
    
class DeleteTool(Tool):
    def __init__(self, scene):
        Tool.__init__(self, Images.images["Pointer-Delete"], scene)
        self.snappedOdePos = (0,0,0)
    
    def invokeTool(self):
        scene = self.scene
        if scene.canRemoveBlock(self.snappedOdePos):
            scene.removeBlock(self.snappedOdePos)
    
    def positionChanged(self, odePos):
        snap = Coordinates.snapOdePosToBoxOdePos(odePos)
        if self.snappedOdePos[Y] != snap[Y]:
            print 'y pos changed from:',self.snappedOdePos[Y],' to:',snap[Y]
        self.snappedOdePos = snap
        Tool.positionChanged(self, odePos)
        
class BlockTool(SnapTool):
    def __init__(self, scene):
        SnapTool.__init__(self, Images.images["Pointer-Standard"], scene)
        self.block = self.newBlock()
    
    def invokeTool(self):
        scene = self.scene
        if scene.canPlaceBlock(self.odePos):
            scene.placeBlock(self.odePos, self.block)
            self.block = self.newBlock()
    
    def render(self, screen):
        if self.scene.canPlaceBlock(self.odePos):
            self.block.render(screen)
    
class GelBlockTool(BlockTool):
    def __init__(self, scene):
        BlockTool.__init__(self, scene)
    
    def newBlock(self):
        return Objects.Block.Block("Block-Place-Gel", "Block-Gel", Objects.Block.GEL_BLOCK_BOUNCE, Objects.Block.GEL_MAX_SURVIVABLE_VELOCITY_MOD)
    
class NormalBlockTool(BlockTool):
    def __init__(self, scene):
        BlockTool.__init__(self, scene)
    
    def newBlock(self):
        return Objects.Block.Block("Block-Place-Normal", "Block-Normal")
        
class LeftRampTool(BlockTool):
    def __init__(self, scene):
        BlockTool.__init__(self, scene)
    
    def newBlock(self):
        return Objects.Block.LeftRampBlock("Block-Place-LeftRamp", "Block-LeftRamp")
    
class RightRampTool(BlockTool):
    def __init__(self, scene):
        BlockTool.__init__(self, scene)

    def newBlock(self):
        return Objects.Block.RightRampBlock("Block-Place-RightRamp", "Block-RightRamp")
    
class SpringTool(BlockTool):
    def __init__(self, scene):
        BlockTool.__init__(self, scene)        

    def newBlock(self):
        return Objects.Block.Block("Block-Place-Spring", "Block-Spring", Objects.Block.SPRING_BLOCK_BOUNCE, Objects.Block.SPRING_MAX_SURVIVABLE_VELOCITY_MOD)
    