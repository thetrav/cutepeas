from pygame.locals import *
import pygame
import ode

keepRunning = True
eventHandlers = {}
world = None
space = None
balls = []
boxes = []
leftRamps = []
contactGroup = None
pos = (0,0)

pixels_in_an_ode_unit = 25
BALL_RADIUS = 20
BALL_COLOR = (255,0,0)
MAX_FPS = 72

BOX_WIDTH = 50
BOX_HEIGHT = 50
BOX_COLOR = (0,0,255)

RAMP_WIDTH = 200
RAMP_HEIGHT = 100
RAMP_COLOR = (0,0,255)

def odeToPixels(ode_units):
    return int(ode_units * pixels_in_an_ode_unit)

def pixelsToOde(pixels):
    return float(pixels) / float(pixels_in_an_ode_unit)

def getOdePos(pos):
    return (pixelsToOde(pos[0]), pixelsToOde(pos[1]), 0)

def placeBox(pos):
    odePos = getOdePos(pos)
    lx = pixelsToOde(BOX_WIDTH)
    ly = pixelsToOde(BOX_HEIGHT)
    geom = ode.GeomBox(space, (lx,ly,1))
    geom.setPosition(odePos)
    boxes.append(geom)

def placeLeftRamp(pos):
    w = pixelsToOde(RAMP_WIDTH)
    h = pixelsToOde(RAMP_HEIGHT)
    odePos = getOdePos(pos)
    triMeshData = ode.TriMeshData()
    
    verts = [(0.0, 0.0, 0.0),#0
             (w  , -h , 0.0),#1
             (w  , -h , 1.0),#2
             (0.0, 0.0, 1.0),#3
             (w  , 0.0, 0.0),#4
             (w  , 0.0, 1.0)]#5
    print "verts:",verts
    faces = [(0,1,2), (0,2,3), (4,5,1), (5,2,1)]
    triMeshData.build(verts, faces)
    print " built"
    geom = ode.GeomTriMesh(triMeshData, space)
    print "geomed"
    geom.setPosition(odePos)
    print "positioned"
    leftRamps.append(geom)
    
def createBoxRect(pos):
    return (pos[0] - BOX_WIDTH/2, pos[1] - BOX_HEIGHT/2, BOX_WIDTH, BOX_HEIGHT)

def dropSphere(pos):
    odePos = getOdePos(pos)
    body = ode.Body(world)
    mass = ode.Mass()
    mass.setSphere(2500, pixelsToOde(BALL_RADIUS))
    body.setMass(mass)

    # Create a box geom for collision detection
    geom = ode.GeomSphere(space, pixelsToOde(BALL_RADIUS))
    geom.setBody(body)
    
    body.setPosition(odePos)
    balls.append(body)

def initPhysics():
    global world, space, contactgroup
    world = ode.World()
    world.setGravity( (0,9.81,0) )
    world.setERP(0.8)
    world.setCFM(1E-5)
    space = ode.Space()
    floor = ode.GeomPlane(space, (0,-1,0), pixelsToOde(-500))
    leftWall = ode.GeomPlane(space, (1,0,0), pixelsToOde(0))
    rightWall = ode.GeomPlane(space, (-1,0,0), pixelsToOde(-800))
    contactgroup = ode.JointGroup()
    
def near_callback(args, geom1, geom2):
    world,contactgroup = args
    contacts = ode.collide(geom1, geom2)
    for c in contacts:
        c.setBounce(0.2)
        c.setMu(5000)
        j = ode.ContactJoint(world, contactgroup, c)
        j.attach(geom1.getBody(), geom2.getBody())
        
def stepPhysics(timeD):
    if timeD > 0:
        #print "timeD=",timeD#/1000.0
        print "colliding"
        space.collide((world,contactgroup), near_callback)
        #print balls[0].getPosition()
        print "Stepping"
        world.step(timeD * 0.003)#/1000.0)
        print "done"
        contactgroup.empty()
        for ball in balls:
            ball_pos = ball.getPosition()
            ball.setPosition((ball_pos[0], ball_pos[1], 0.0)) 

def handleMouseMotion(event):
    global pos
    pos = event.pos

def handleMouseDown(event):
    if event.button == 1:
        dropSphere(pos)
    if event.button == 2:
        placeBox(pos)
    if event.button == 3:
        placeLeftRamp(pos)

eventHandlers[MOUSEMOTION] = handleMouseMotion
eventHandlers[MOUSEBUTTONDOWN] = handleMouseDown

def events():
    global keepRunning
    for event in pygame.event.get():
        if event.type == QUIT:
            keepRunning = False
        elif eventHandlers.has_key(event.type):
            eventHandlers[event.type](event)
        else:
            print "key ", event.type, " not found"

def getPixelPos(odePos):
    return (odeToPixels(odePos[0]), odeToPixels(odePos[1]))

def getRampPoints(pos):
    x = pos[0]
    y = pos[1]
    return (
            (x,y),
            (x+RAMP_WIDTH, y-RAMP_HEIGHT),
            (x+RAMP_WIDTH, y)
            )

def render(screen):
    for ball in balls:
        odePos = ball.getPosition()
        pos = getPixelPos(odePos)
        #print "drawing ball at ",pos
        pygame.draw.circle(screen, BALL_COLOR, pos, BALL_RADIUS)
    
    for box in boxes:
        odePos = box.getPosition()
        pos = getPixelPos(odePos)
        pygame.draw.rect(screen, BOX_COLOR, createBoxRect(pos))
        
    for ramp in leftRamps:
        odePos = ramp.getPosition()
        pos = getPixelPos(odePos)
        print "drawing ramp at:",pos
        pygame.draw.polygon(screen, RAMP_COLOR, getRampPoints(pos))

def animate(timeD):
    stepPhysics(timeD)

def createBackground(screen):
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((240, 240, 240))
    return background

def main():
    initPhysics()
    dropSphere((100,50))
    pygame.display.set_mode((800,600))
    pygame.display.set_caption('Ball Block and Ramp ZOMG!!!')
    screen = pygame.display.get_surface()
    background = createBackground(screen)
    clock = pygame.time.Clock()
    clock.tick() #initialise timer
    while keepRunning:
        events()
        animate(clock.get_time())
        
        screen.blit(background, (0, 0))
        render(screen)
        pygame.display.flip()
        clock.tick(MAX_FPS)
main()