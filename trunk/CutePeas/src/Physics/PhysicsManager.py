from Vector import Vector
from Surface import Surface
from PhysPea import PhysPea
import math

GRAVITY = -9.8

class PhysicsManager:
    def __init__(self):
        self.surfaces = []
        self.frameTime = 0
        self.gravity = 9.8
        
        
    def update(self, pea):
        self.frameTime = pygame.time.Clock.get_time
        if pea.state == 'jumping':
            pea.physPea = PhysPea(pea.translation)
            calculateTrajectory(pea)
            pea.state = 'falling'
        elif pea.state == 'falling':
            checkForIntersection(pea)
        
    def render(self, screen):
        #Debug surface rendering
        for surface in self.surfaces:
            surface.render(screen)
            
    def addSurface(self, newSurface):
        surfaces.append(newSurface)
        
    def addSurfaces(self, newSurfaces):
        for surface in newSurfaces:
            surfaces.append(surface)
        
    def removeSurface(self, delSurface):
        surfaces.remove(delSurface)
        
    def removeSurfaces(self, delSurfaces):
        for surface in delSurfaces:
            surfaces.remove(surface)
            
    #Physics Calculations
    def calculateTrajectory(self, pea):
        #Calculate new Pea position
        phPea = pea.physPea 
        currPos = phPea.currentCoord
        
        newX = phPea.xvelocity + currPos.x
        newY = (1/2) * GRAVITY * self.frameTime + phPea.yvelocity + currPos.y
        
        phPea.currentCoord = Vector(newX, newY)
        
    def checkForIntersection(self, pea):
        for surface in self._surfaces:
            surface.checkForIntersection(pea)
        
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
        
    
        
            
        
        
        