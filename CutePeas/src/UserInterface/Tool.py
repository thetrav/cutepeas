import Images 
import Objects.Block
from Constants import *
import Coordinates


class Tool:
    def __init__(self, cursorIcon, scene):
        self.cursorIcon = cursorIcon
        self.listeners = []
        self.pos = (0,0)
        self.scene = scene
    
    def positionChanged(self, newPos):
        self.pos = (newPos[X], newPos[Y])
    
    def invokeTool(self):
        pass
    
    def render(self, screen):
        pass
    
class DeleteTool(Tool):
    def __init__(self, scene):
        Tool.__init__(self, Images.images["Pointer-Delete"], scene)
    
    def invokeTool(self):
        scene = self.scene
        if scene.canRemoveBlock(self.pos):
            scene.removeBlock(self.pos)
        
class BlockTool(Tool):
    def __init__(self, scene):
        Tool.__init__(self, Images.images["Pointer-Standard"], scene)
        self.block = self.newBlock()
    
    def invokeTool(self):
        scene = self.scene
        if scene.canPlaceBlock(self.pos):
            scene.placeBlock(self.pos, self.block)
            self.block = self.newBlock()
    
    def render(self, screen):
        if self.scene.canPlaceBlock(self.pos):
            self.block.render(screen)
    
    def positionChanged(self, pos):
        snappedPos = Coordinates.snapPixelPosToBoxPixelPos(pos)
        Tool.positionChanged(self, snappedPos)
        self.block.pos = (snappedPos[X], snappedPos[Y])

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
    