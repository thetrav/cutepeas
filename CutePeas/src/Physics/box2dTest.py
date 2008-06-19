import Box2D2 as box2d
import math
import pygame
from pygame.locals import *

#gameLoop
keepRunning = True
eventHandlers = {}
#pygame
screen = None
clock = None
background = None
MAX_FPS = 72
#physics
world = None
balls = []
boxes = []
time_step = 1.0 / 60.0
iterations = 10
time_counter = 0

BOX_WIDTH = 100
BOX_HEIGHT = 100

BALL_RADIUS = 25
BALL_COLOR = (255,0,0)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PIXELS_PER_PHYSICS_UNIT = 10

def pixelsToPhysics(pixels):
    return pixels/PIXELS_PER_PHYSICS_UNIT

def physicsToPixels(physics):
    return physics * PIXELS_PER_PHYSICS_UNIT

def initPhysics():
    global world
    world_bounding_box = box2d.b2AABB()
    world_bounding_box.lowerBound.Set(0, 0)
    print pixelsToPhysics(SCREEN_WIDTH), pixelsToPhysics(SCREEN_HEIGHT)
    world_bounding_box.upperBound.Set(pixelsToPhysics(SCREEN_WIDTH), pixelsToPhysics(SCREEN_HEIGHT))

    gravity = box2d.b2Vec2(0, 10)

    doSleep = False
    world = box2d.b2World(world_bounding_box, gravity, doSleep)

    floorWidth = 400
    floorHeight = 10
    floor_def = box2d.b2BodyDef()
    floor_def.position.Set(0,pixelsToPhysics(SCREEN_HEIGHT) - pixelsToPhysics(floorHeight))
    floor = world.CreateBody(floor_def)

    floor_shape_def = box2d.b2PolygonDef()
    floor_shape_def.SetAsBox(pixelsToPhysics(floorWidth),pixelsToPhysics(floorHeight))
    floor.CreateShape(floor_shape_def)

def dropBall(pos):
    body_def = box2d.b2BodyDef()
    body_def.position.Set(pixelsToPhysics(pos[0]), pixelsToPhysics(pos[1]))
    body = world.CreateBody(body_def)
    
    shape_def = box2d.b2CircleDef()
    shape_def.radius = pixelsToPhysics(BALL_RADIUS)
    shape_def.restitution = 0.6 
    shape_def.density = 1
    shape_def.friction = 0.3
    body.CreateShape(shape_def)
    body.SetMassFromShapes()
    balls.append(body)

def stepPhysics(timeD):
    global time_counter
    time_counter += timeD/1000.0
    while time_counter > time_step:
        world.Step(time_step, iterations)
        time_counter -= time_step

def createBackground(screen):
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((240, 240, 240))
    return background
        
def initPyGame():
    global screen, clock, background
    pygame.display.set_mode((800,600))
    pygame.display.set_caption('2dBox ZOMG!!!')
    screen = pygame.display.get_surface()
    background = createBackground(screen)
    clock = pygame.time.Clock()
    clock.tick() #initialise timer

def animate(timeD):
    stepPhysics(timeD)

def squareRect(pos):
    x = physicsToPixels(pos.x)
    y = physicsToPixels(pos.y)
    return (x - BOX_WIDTH/2, y - BOX_HEIGHT/2, BOX_WIDTH, BOX_HEIGHT)

def render(screen):
    for ball in balls:
        pos = ball.GetPosition()
        pygame.draw.circle(screen, BALL_COLOR, (pos.x, pos.y), BALL_RADIUS) 
    
    for box in boxes:
        position = box.GetPosition()
        rect = squareRect(position)
        pygame.draw.rect(screen, (255,0,0), rect)

def events():
    global keepRunning
    pygame.event.pump()
    for event in pygame.event.get():
        if event.type == QUIT:
            keepRunning = False
        elif eventHandlers.has_key(event.type):
            eventHandlers[event.type](event)
        else:
            print "key ", event.type, " not found"

def mainLoop():
    while keepRunning:
        events()
        animate(clock.get_time())
        
        screen.blit(background, (0, 0))
        render(screen)
        pygame.display.flip()
        clock.tick(MAX_FPS)        
        
initPhysics()
dropBall((300,10))
initPyGame()
mainLoop()