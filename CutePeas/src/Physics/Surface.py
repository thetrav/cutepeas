import Vector
import math
from Physics import BlockType
from Physics import BlockHeight

# Physical Constants
MAX_BOUNCES = 5          # determines bounces on same surface before trap is triggered.
SPRING_MOMENTUM = 1.5    # increase in velocity
RAMP_ABSORB = 0.2        # decrease in velocity

class Surface:
    def __init__(self, translation, angle, normal, type, length):
        
        #Specifies the direction that the surface faces, with 0Deg vertical.        
        #angle of the surface
        self.angle = angle
        self.translation = translation
        self.length = length;
        self.normal = normal    
        self.type = type
                        
        #Setting up the render info
        self.start_pos = Vector(self.translation.x, self.translation.y)
        self.start_pos.x += self.length * (math.sin(self.angle))
        self.start_pos.y += self.length * (math.cos(self.angle))
        
        self.end_pos = Vector(self.translation.x, self.translation.y)
        self.end_pos.x -= self.length * (math.sin(self.angle))
        self.end_pos.y -= self.length * (math.cos(self.angle))
        
        increment = Vector( ( ( self.start_pos.x - self.translation.x ) / 2 ), ( ( self.start_pos.y - self.translation.y ) / 2 ) )
        
        self.collision_points = []
        self.collision_points[0] = self.translation
        self.collision_points[1] = self.translation + increment 
        self.collision_points[2] = self.translation - increment 
        
    def render(self, screen):
        pygame.draw.line(screen, (1, 1 , 1), (self.start_pos.x, self.start_pos.y), (self.end_pos.x, self.end_pos.y), width=1)        
    
    def checkForCollision(self, pea):
        for count in range(0, 3):
            distToSurface = math.abs(pea.translation - self.collision_points[count])
            if ( distToSurface < pea.physPea._radius ):
                pea.physPea.hitCoord = self.collision_points[count]
                collision(pea)
        
    def collision(self, pea):        
        print('pea collided with surface')
        
        phPea = pea.physPea

        # Increment/Add this surface to the PhysPea's hit surfaces dictionary
        if phPea.hitSurfaces.has_key(self):
            phPea.hitSurfaces[self] += 1
            if phPea.hitSurfaces[self] >= MAX_BOUNCES:
                pea.fireTrap()
                
        else:
            phPea.hitSurfaces[self] = 0
                
        # Check for surface type
        # If side
        if (self.angle == 90) or (self.angle == 270):
            # Calculate new Pea bounce direction Vector
            # Invert the x axis velocity component
            phPea.xvelocity *= -1
            
        # If bottom
        elif self.angle == 180:
            # Invert the y axis velocity 
            phPea.yvelocity *= -1
            
        # If top
        elif self.angle == 0:
            # If spring then invert and increase y axis velocity
            if self.type == BlockType['spring']:
                phPea.yvelocity *= -SPRING_MOMENTUM
                phPea.xvelocity *= SPRING_MOMENTUM
            #If gelatin block then land.
            elif self.type == BlockType['gel']:
                pea.fireLanded()
            
            # If Standard Block
            elif self.type == BlockType['standard']:
                fallDistance = phPea.startCoord.y - phPea.hitCoord.y
                if fallDistance >= (2 * BlockHeight):
                    # If death, then send death event.
                    pea.fireDeath()
                else:
                    # If landed, send landed event.
                    pea.fireLanded() 
                   
        elif self.type == BlockType['leftramp']:
            fallDistance = phPea.startCoord.y - phPea.hitCoord.y
            if fallDistance >= (3 * BlockHeight):
                # If death, then send death event.
                pea.fireDeath()
            else:
                # Transferring a percentage of the y velocity component to the x
                # Not physically accurate, but meh, I can't be bothered modeling realistic pea
                # physics at 2am
                phPea.yvelocity *= ( 1 - RAMP_ABSORB)
                phPea.xvelocity += phPea.yvelocity * -RAMP_ABSORB
                
        elif self.type == BlockType['rightramp']:
            fallDistance = phPea.startCoord.y - phPea.hitCoord.y
            if fallDistance >= (3 * BlockHeight):
                # If death, then send death event.
                pea.fireDeath()
            else:
                phPea.yvelocity *= ( 1 - RAMP_ABSORB)
                phPea.xvelocity += phPea.yvelocity * RAMP_ABSORB    
        
        