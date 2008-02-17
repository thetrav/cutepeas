import Vector
import math

class Surface:
    def __init__(self, surfaceID, translation, angle, type, length):
        
        #Specifies the direction that the surface faces, with 0Deg vertical.
        self.id = surfaceID
        self.angle = angle
        self.translation = translation
        self.length = length;
        self.normal = Vector(0, 0)    
        self.type = type
                        
        #Setting up the render info
        self.start_pos = Vector(self.translation.x, self.translation.y)
        self.start_pos.x += self.length * (math.sin(self.angle))
        self.start_pos.y += self.length * (math.cos(self.angle))
        
        self.end_pos = Vector(self.translation.x, self.translation.y)
        self.end_pos.x -= self.length * (math.sin(self.angle))
        self.end_pos.y -= self.length * (math.cos(self.angle)) 
        
    def render(self, screen):
        pygame.draw.line(screen, (1, 1 , 1), (self.start_pos.x, self.start_pos.y), (self.end_pos.x, self.end_pos.y), width=1)
    
    def collide(self):
        print('collided with surface')
        
            
        
        