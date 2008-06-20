import pygame.draw
import Constants
from Constants import *
import Objects.Block

COLLISION_RESOLUTION = 5
VERTICAL_SURFACE_HEIGHT = BLOCK_HEIGHT
HORIZONTAL_SURFACE_WIDTH = BLOCK_WIDTH
DIAGONAL_SURFACE_WIDTH = BLOCK_WIDTH
DIAGONAL_SURFACE_HEIGHT = BLOCK_HEIGHT

X_FRICTION = 0.98
Y_FRICTION = 0.95

GRAVITY = 0.0008
WIND_FRICTION = 0.005
MIN_Y_VELOCITY = 0.02

PHYSICS_RESOLUTION = 2

def positive(number):
    return number if number > 0 else -number
    
def underDistance(first, second, distance):
    return positive(positive(first) - positive(second)) < distance
    
def inRange(point, surface, index):
    return point[index] > surface.start[index] - PEA_RADIUS and point[index] < surface.end[index] + PEA_RADIUS

def leftRampSurface(topLeft):
    return DiagonalSurface([topLeft[X], topLeft[Y] + DIAGONAL_SURFACE_HEIGHT],
                           [topLeft[X] + DIAGONAL_SURFACE_WIDTH, topLeft[Y]])
    
def rightRampSurface(topLeft):
    return DiagonalSurface([topLeft[X], topLeft[Y]],
                           [topLeft[X] + DIAGONAL_SURFACE_WIDTH, topLeft[Y] + DIAGONAL_SURFACE_HEIGHT])

class PhysicsManager:
    def __init__(self):
        self.surfaces = []
        self.timeBuffer = 0
        
    def render(self, screen):
        if Constants.DRAW_HIT_BOXES:
            for surface in self.surfaces:
                surface.render(screen)
    
    def addSurfaces(self, surfaces):
        for surface in surfaces:
            self.surfaces.append(surface)
    
    def removeSurfaces(self, surfaces):
        for surface in surfaces:
            self.surfaces.remove(surface)
    
    def update(self, pea, timeD):
        self.timeBuffer += timeD
        while self.timeBuffer > PHYSICS_RESOLUTION:
            self.play(pea, PHYSICS_RESOLUTION)
    
    def play(self, pea, timeD):
        self.timeBuffer -= timeD
        newVelocity = calculateNewVelocity(pea.velocity, timeD)
        newPos = calculateNewPos(pea.pos, newVelocity, timeD)
        for surface in self.surfaces:
            if surface.isCollide(newPos):
                newVelocity = surface.applyCollision(newVelocity)
                newPos = calculateNewPos(pea.pos, newVelocity, timeD)
        pea.velocity = newVelocity
        pea.pos = newPos
    
    def eventFired(self, id, block):
        if id == Objects.Block.Block.DONE_GHOSTING_IN_EVENT:
            self.addSurfaces(block.createSurfaces())
        elif id == Objects.Block.Block.DONE_GHOSTING_OUT_EVENT:
            self.removeSurfaces(block.surfaces)

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
        pygame.draw.line(screen, self.color, self.start, self.end, 1)
        
    def applyCollision(self, velocity):
        return [velocity[X] * X_FRICTION, velocity[Y] * Y_FRICTION]
        
class VerticalSurface(Surface):
    def __init__(self, topLeft):
        Surface.__init__(self, topLeft, [topLeft[X], topLeft[Y]+VERTICAL_SURFACE_HEIGHT], (0,0,180))
    
    def isCollide(self, point):
        if inRange(point, self, Y):
            return underDistance(point[X], self.start[X], PEA_RADIUS)
        return False
    
    def applyCollision(self, velocity):
        return Surface.applyCollision(self, [-velocity[X], velocity[Y]])

class HorizontalSurface(Surface):
    def __init__(self, topLeft):
        Surface.__init__(self, topLeft, [topLeft[X] + HORIZONTAL_SURFACE_WIDTH, topLeft[Y]], (0,0,180))
    
    def isCollide(self, point):
        if inRange(point, self, X):
            return underDistance(point[Y], self.start[Y], PEA_RADIUS)
        return False
    
    def applyCollision(self, velocity):
        return Surface.applyCollision(self, [velocity[X], -velocity[Y] if positive(velocity[Y]) > MIN_Y_VELOCITY else 0])

class DiagonalSurface(Surface):
    def __init__(self, leftPoint, rightPoint):
        Surface.__init__(self, 
                       leftPoint,
                       rightPoint, 
                       (0,0,180))
        self.gradient = (rightPoint[Y] - leftPoint[Y]) / (rightPoint[X] - leftPoint[X]) #rise over run
        self.yOffset = leftPoint[Y] - (self.gradient * leftPoint[X])
     
    # draws collision path in steps, was using it for debug, will probably want to delete this method later   
    def render(self, screen):
        Surface.render(self, screen)
        steps = (self.end[X] - self.start[X]) / 5
        for x in xrange(5):
            xPos = self.start[X] + (steps * x)
            yPos = self.gradient * xPos + self.yOffset
            pygame.draw.circle(screen, (130, 0, 0), [xPos, yPos], 2)
         
    def isCollide(self, point):
        if inRange(point, self, X):
            lineY = self.gradient * point[X] + self.yOffset
            return underDistance(point[Y], self.start[Y], PEA_RADIUS)
    
    def applyCollision(self, velocity):
        return Surface.applyCollision(self, [-velocity[X], -velocity[Y]])
    
class TestPea:
    def __init__(self, pos, vel, physics):
        self.pos = pos
        self.velocity = vel
        self.physics = physics
    
    def render(self, screen):
        pygame.draw.circle(screen, (0,150,0) , self.pos, PEA_RADIUS, 1)
    
    def update(self, timeD):
        self.physics.update(self, timeD)
        
def physicsManagerWithBorders():
    physicsManager = PhysicsManager()
    bottom = Y_BORDER + BLOCK_Y_OVERLAP
    surfaces = [VerticalSurface([10,10]),
                VerticalSurface([790,10]),
                HorizontalSurface([10,10]),
                HorizontalSurface([10, bottom])]
    surfaces[0].end = [10 , bottom]
    surfaces[1].end = [790, bottom]
    surfaces[2].end = [790, 10]
    surfaces[3].end = [790, bottom]
    physicsManager.addSurfaces(surfaces)
    return physicsManager