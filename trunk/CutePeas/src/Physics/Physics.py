import Vector
import Surface
import BlockRef
import math

class SurfaceManager:
    def __init__(self):
        self.surfaces = []
        self.nextSurfaceID = 0
        
        self.blocks = []
        self.nextBlockID = 0
        
    def render(self, screen):
        for surface in surfaces
            surface.render(screen)
        
    
    def addBlock(self, position, type ):
        
        if BlockType[type] == BlockType['normal'] :
            

    def createTopSurface(self, position):
        xPos =  position.x;
        yPos =  position.y + (BlockHeight / 2)
        
        newSurface = Surface(self.nextSurfaceID,
                             Vector(xPos, yPos),
                             0,
                             BlockType['normal']
                             BlockWidth
                             )        
        return newSurface
    
    def createBottomSurface(self, position, blockType):
        xPos =  position.x;
        yPos =  position.y - (BlockHeight / 2)
        
        newSurface = Surface(self.nextSurfaceID,
                             Vector(xPos, yPos),
                             0,
                             blockType
                             BlockWidth
                             )        
        return newSurface
        
    def createLeftSurface(self, position):
        xPos =  position.x - (BlockWidth / 2) 
        yPos =  position.y;
        
        newSurface = Surface(self.nextSurfaceID,
                             Vector(xPos, yPos),
                             0,
                             blockType
                             BlockWidth
                             )        
        return newSurface
            
    def createRightSurface(self, position):
        xPos =  position.x + (BlockWidth / 2) 
        yPos =  position.y;
        
        newSurface = Surface(self.nextSurfaceID,
                             Vector(xPos, yPos),
                             0,
                             blockType
                             BlockWidth
                             )        
        return newSurface
        
        
    def createLeftRamp(self, position):
        xPos =  position.x; 
        yPos =  position.y;
        
        tlX = position.x - (BlockWidth/2)
        brX = position.x + (BlockWidth/2)
        tlY = position.y - (BlockHeight/2)
        brY = position.y + (BlockHeight/2)
        
        length = math.sqrt( math.pow( (brX - tlX), 2), math.pow( (brY - tlY), 2) )
        
        newSurface = Surface(self.nextSurfaceID,
                             Vector(xPos, yPos),
                             0,
                             blockType
                             length
                             )        
        return newSurface
        
    def createRightRamp(self, position):
        xPos =  position.x + (BlockWidth / 2) 
        yPos =  position.y;
        
        
        newSurface = Surface(self.nextSurfaceID,
                             Vector(xPos, yPos),
                             0,
                             blockType
                             BlockWidth
                             )        
        return newSurface
        
    
        
            
        
        
        