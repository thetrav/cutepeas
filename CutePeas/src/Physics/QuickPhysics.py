import pygame.draw
from Constants import *

COLLISION_RESOLUTION = 10
VERTICAL_SURFACE_HEIGHT = 40
HORIZONTAL_SURFACE_WIDTH = 40

GRAVITY = 0.008
WIND_FRICTION = 0.005

class PhysicsManager:
    def __init__(self):
        self.surfaces = []
        
    def render(self, screen):
        for surface in self.surfaces:
            surface.render(screen)
    
    def addSurfaces(self, surfaces):
        for surface in surfaces:
            self.surfaces.append(surface)
            
    def removeSurfaces(self, surfaces):
        for surface in surfaces:
            self.surfaces.remove(surface)
            
    def update(self, pea, timeD):
        newVelocity = calculateNewVelocity(pea.velocity, timeD)
        newPos = calculateNewPos(pea.pos, newVelocity, timeD)
        
        for surface in self.surfaces:
            if surface.isCollide(newPos):
                print "collision"
                elapsed = 0
                lastPos = [pea.pos[X], pea.pos[Y]]
                lastVelocity = [pea.velocity[X], pea.velocity[Y]]
                timeSliceSize = timeD / COLLISION_RESOLUTION
                for n in xrange(COLLISION_RESOLUTION):
                    vel = calculateNewVelocity(lastVelocity, timeSliceSize)
                    pos = calculateNewPos(lastPos, lastVelocity, timeD)
                    if surface.isCollide(pos):
                        pea.velocity = surface.applyCollision(lastVelocity)
                        pea.pos = lastPos
                        #recurse to animate pea for remaining time
                        if elapsed == 0:
                            raise "Pea began update already collided with surface at pos:" + str(pea.pos) + " vel:"+str(pea.velocity)
                        return self.update(pea, timeD - elapsed)
                    elapsed += timeSliceSize
                    lastPos = pos
                    lastVelocity = velocity
        pea.velocity = newVelocity
        pea.pos = newPos
        print "time="+str(timeD)+" vel="+str(newVelocity)+" pos="+str(newPos)

def calculateNewVelocity(oldVelocity, timeD):
    return [oldVelocity[X], oldVelocity[Y] + GRAVITY * timeD ]

def calculateNewPos(oldPos, velocity, timeD):
    return [oldPos[X] + timeD * velocity[X], 
            oldPos[Y] + timeD * velocity[Y]]
            
class Surface:
    def __init__(self, start, end, color):
        self.start = start
        self.end = end
        self.color = color
        
    def render(self, screen):
        pygame.draw.line(screen, self.color, self.start, self.end, 3)

def positive(number):
    return number if number > 0 else -number

def underDistance(first, second, distance):
    print "distance = "+ str(positive(first) - positive(second)) + " target="+str(distance)
    return positive(positive(first) - positive(second)) < distance
        
class VerticalSurface(Surface):
    def __init__(self, topLeft):
        Surface.__init__(self, topLeft, [topLeft[X], topLeft[Y]+VERTICAL_SURFACE_HEIGHT], (255,255,255))
    
    def isCollide(self, point):
        if point[Y] >= self.start[Y] and point[Y] <= self.end[Y]:
            return underDistance(point[X], self.start[X], PEA_RADIUS)
        return False
    
    def applyCollision(self, velocity):
        print "applying vertical collision"
        return [velocity[X] * -1, velocity[Y]]

class HorizontalSurface(Surface):
    def __init__(self, topLeft):
        Surface.__init__(self, topLeft, [topLeft[X] + HORIZONTAL_SURFACE_WIDTH, topLeft[Y]], (255,255,255))
    
    def isCollide(self, point):
        if point[X] >= self.start[X] and point[X] <= self.end[X]:
            print "in X zone"
            return underDistance(point[Y], self.start[Y], PEA_RADIUS)
        return False
    
    def applyCollision(self, velocity):
        print "applying horizontal collision"
        return [velocity[X], velocity[Y] * -1]
    
class TestPea:
    def __init__(self, pos, vel, physics):
        self.pos = pos
        self.velocity = vel
        self.physics = physics
        
    def render(self, screen):
        pygame.draw.circle(screen, (0,150,0) , self.pos, PEA_RADIUS, 3)
        pygame.draw.circle(screen, (0,150,0) , self.pos, PEA_RADIUS/2, 3)
        
    def update(self, timeD):
        self.physics.update(self, timeD)