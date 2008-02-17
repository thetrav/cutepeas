import Vector
import Surface
import BlockRef
import math

class PhysicsManager:
    def __init__(self):
        self.surfaces = []
        
        self.blocks = []
        self.nextBlockID = 0
    
    def getNextBlockID(self):
        if self.nextBlockID != 0:
            self.nextBlockID += 1
        return self.nextBlockID           
        
        
    def render(self, screen):
        for block in self.blocks:
            block.render(screen)
            
    def addSurface(self, newSurface):
        surfaces.append(newSurface)
        
    def removeSurface(self, delSurface):
        surfaces.remove(delSurface)
            
    def addBlock(self, position, type ):
        
        newBlock = BlockRef(getNextBlockID)
        
        if BlockType[type] == BlockType['standard'] or \
           BlockType[type] == BlockType['spring'] or \
           BlockType[type] == BlockType['gel'] :
                       
            #Top
            newSurface = createTopSurface(position, type)
            newBlock.surfaces.append(newSurface)
            
            #Bottom
            newSurface = createBottomSurface(position, type)
            newBlock.surfaces.append(newSurface)
            
            #Left
            newSurface = createLeftSurface(position, type)
            newBlock.surfaces.append(newSurface)
            
            #Right
            newSurface = createRightSurface(position, type)
            newBlock.surfaces.append(newSurface)
        
        elif BlockType[type] == BlockType['leftramp'] :
            
            #LeftRamp
            newSurface = createLeftRamp(position, type)
            newBlock.surfaces.append(newSurface)
                        
            #Right
            newSurface = createRightSurface(position, type)
            newBlock.surfaces.append(newSurface)
            
            #Bottom
            newSurface = createBottomSurface(position, type)
            newBlock.surfaces.append(newSurface)
            
            
        elif BlockType[type] == BlockType['rightramp'] :
            #RightRamp
            newSurface = createRightRamp(position, type)
            newBlock.surfaces.append(newSurface)
                        
            #Right
            newSurface = createRightSurface(position, type)
            newBlock.surfaces.append(newSurface)
            
            #Bottom
            newSurface = createBottomSurface(position, type)
            newBlock.surfaces.append(newSurface)
        
        self.blocks.append(newBlock)
        
        #End of addBlock
        
    def removeBlock(self, deleteBlockID):
        print('removing Block')
        
    
    def createTopSurface(self, position, blockType):
        xPos =  position.x;
        yPos =  position.y + (BlockHeight / 2)
        
        newSurface = Surface(Vector(xPos, yPos),
                             0,
                             Vector(0, 1),
                             blockType,
                             BlockWidth
                             )        
        return newSurface
    
    def createBottomSurface(self, position, blockType):
        xPos =  position.x;
        yPos =  position.y - (BlockHeight / 2)
        
        newSurface = Surface(Vector(xPos, yPos),
                             180,
                             Vector(0, -1),
                             blockType,
                             BlockWidth
                             )        
        return newSurface
        
    def createLeftSurface(self, position):
        xPos =  position.x - (BlockWidth / 2) 
        yPos =  position.y;
        
        newSurface = Surface(Vector(xPos, yPos),
                             270,
                             Vector(-1, 0),
                             blockType,
                             BlockWidth
                             )        
        return newSurface
            
    def createRightSurface(self, position):
        xPos =  position.x + (BlockWidth / 2) 
        yPos =  position.y;
        
        newSurface = Surface(Vector(xPos, yPos),
                             90,
                             Vector(1, 0),
                             blockType,
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
        
        newSurface = Surface(Vector(xPos, yPos),
                             315,
                             Vector(-1, 1),
                             blockType,
                             length
                             )        
        return newSurface
        
    def createRightRamp(self, position):
        xPos =  position.x + (BlockWidth / 2) 
        yPos =  position.y; 
        
        tlX = position.x - (BlockWidth/2)
        brX = position.x + (BlockWidth/2)
        tlY = position.y - (BlockHeight/2)
        brY = position.y + (BlockHeight/2)
        
        length = math.sqrt( math.pow( (brX - tlX), 2), math.pow( (brY - tlY), 2) )       
        
        newSurface = Surface(Vector(xPos, yPos),
                             45,
                             Vector(1, 1),
                             blockType,
                             BlockWidth
                             )        
        return newSurface
        
    
        
            
        
        
        