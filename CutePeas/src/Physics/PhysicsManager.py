from Vector import Vector
from Surface import Surface
from PhysPea import PhysPea
import math
from Constants import *

GRAVITY = -9.8

class PhysicsManager:
    def __init__(self):
        self.surfaces = []
        self.frameTime = 0
        self.gravity = 9.8
        
        
    def update(self, pea):
        self.frameTime = pygame.time.Clock.get_time
        if pea.physPea != None:
            if pea.physPea.state == 'falling':
                calculateTrajectory(pea)
                checkForIntersection(pea)
                
    def jumpFired(self, pea):
        # Respond to jump event.
        pea.physPea = PhysPea(pea.translation)
        calculateTrajectory(pea)
        pea.physPea.state = 'falling'            
        
    def render(self, screen):
        #Debug surface rendering
        for surface in self.surfaces:
            surface.render(screen)
            
    def addSurface(self, newSurface):
        self.surfaces.append(newSurface)
        
    def addSurfaces(self, newSurfaces):
        for surface in newSurfaces:
            self.surfaces.append(surface)
        
    def removeSurface(self, delSurface):
        self.surfaces.remove(delSurface)
        
    def removeSurfaces(self, delSurfaces):
        for surface in delSurfaces:
            self.surfaces.remove(surface)
            
    #Physics Calculations
    def calculateTrajectory(self, pea):
        #Calculate new Pea position
        phPea = pea.physPea 
        currPos = phPea.currentCoord
        
        newX = phPea.xvelocity + currPos.x
        newY = (1/2) * GRAVITY * self.frameTime + phPea.yvelocity + currPos.y
        
        phPea.currentCoord = Vector(newX, newY)
        # Need to possibly pass this coordinate back into the rendered parts of the Pea?
        
    def checkForIntersection(self, pea):
        for surface in self.surfaces:
            surface.checkForIntersection(pea)        
    
    def createTopSurface(self, position, blockType):
        xPos =  position.x;
        yPos =  position.y + (BLOCK_HEIGHT / 2)
        
        newSurface = Surface(Vector(xPos, yPos),
                             0,
                             Vector(0, 1),
                             blockType,
                             BLOCK_WIDTH
                             )        
        return newSurface
    
    def createBottomSurface(self, position, blockType):
        xPos =  position.x;
        yPos =  position.y - (BLOCK_HEIGHT / 2)
        
        newSurface = Surface(Vector(xPos, yPos),
                             180,
                             Vector(0, -1),
                             blockType,
                             BLOCK_WIDTH
                             )        
        return newSurface
        
    def createLeftSurface(self, position):
        xPos =  position.x - (BLOCK_WIDTH / 2) 
        yPos =  position.y;
        
        newSurface = Surface(Vector(xPos, yPos),
                             270,
                             Vector(-1, 0),
                             blockType,
                             BLOCK_WIDTH
                             )        
        return newSurface
            
    def createRightSurface(self, position):
        xPos =  position.x + (BLOCK_WIDTH / 2) 
        yPos =  position.y;
        
        newSurface = Surface(Vector(xPos, yPos),
                             90,
                             Vector(1, 0),
                             blockType,
                             BLOCK_WIDTH
                             )        
        return newSurface
        
        
    def createLeftRamp(self, position):
        xPos =  position.x; 
        yPos =  position.y;
        
        tlX = position.x - (BLOCK_WIDTH/2)
        brX = position.x + (BLOCK_WIDTH/2)
        tlY = position.y - (BLOCK_HEIGHT/2)
        brY = position.y + (BLOCK_HEIGHT/2)
        
        length = math.sqrt( math.pow( (brX - tlX), 2), math.pow( (brY - tlY), 2) )
        
        newSurface = Surface(Vector(xPos, yPos),
                             315,
                             Vector(-1, 1),
                             blockType,
                             length
                             )        
        return newSurface
        
    def createRightRamp(self, position):
        xPos =  position.x + (BLOCK_WIDTH / 2) 
        yPos =  position.y; 
        
        tlX = position.x - (BLOCK_WIDTH/2)
        brX = position.x + (BLOCK_WIDTH/2)
        tlY = position.y - (BLOCK_HEIGHT/2)
        brY = position.y + (BLOCK_HEIGHT/2)
        
        length = math.sqrt( math.pow( (brX - tlX), 2), math.pow( (brY - tlY), 2) )       
        
        newSurface = Surface(Vector(xPos, yPos),
                             45,
                             Vector(1, 1),
                             blockType,
                             BLOCK_WIDTH
                             )        
        return newSurface
        
    
        
            
        
        
        