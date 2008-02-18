from Images import images
import Scenery
from Block import Block



class Tool:
    def __init__(self, cursorIcon):
        self.cursorIcon = cursorIcon
        self.listeners = []
        self.slot = None
    
    def invokeTool(self, target):
        pass
    
    def render(self, screen):
        pass
    
    def setPos(self, x, y):
        pass
    
class DeleteTool(Tool):
    def __init__(self):
        self.cursorIcon = images["Pointer-Delete"]
    
    def invokeTool(self, target):
        if self.slot:
            self.slot.deleteBlock()
        
class BlockTool(Tool):
    def __init__(self):
        self.cursorIcon = images["Pointer-Standard"]
        self.block = self.newBlock()
    
    def invokeTool(self, target):
        if self.slot:
            self.slot.block = self.block
            self.block = self.newBlock()
    
    def render(self, screen):
        if self.block:
            self.block.render(screen)
    
    def setPos(self, x, y):
        self.block.x = x
        self.block.y = y
    
class GelBlockTool(BlockTool):
    def __init__(self):
        BlockTool.__init__(self)
    
    def newBlock(self):
        return Block("Block-Place-Gel")
    
class NormalBlockTool(BlockTool):
    def __init__(self):
        BlockTool.__init__(self)
    
    def newBlock(self):
        return Block("Block-Place-Normal")
        
class LeftRampTool(BlockTool):
    def __init__(self):
        BlockTool.__init__(self)
    
    def newBlock(self):
        return Block("Block-Place-LeftRamp")
    
class RightRampTool(BlockTool):
    def __init__(self):
        BlockTool.__init__(self)

    def newBlock(self):
        return Block("Block-Place-RightRamp")
    
class SpringTool(BlockTool):
    def __init__(self):
        BlockTool.__init__(self)        

    def newBlock(self):
        return Block("Block-Place-Spring")
    