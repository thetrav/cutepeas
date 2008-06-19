import ode
from Constants import *
import UserInterface.Block
import pygame


pixels_in_an_ode_unit = 25
physics_step_size = 0.016
GRAVITY = 9.81
BOUNCE = 0.5

PEA_COLOR = (0,200,0)
BLOCK_COLOR = (200,200,0)
BLOCK_LINE_THICKNESS = 4

def odeToPixels(ode_units):
    return int(ode_units * pixels_in_an_ode_unit)

def pixelsToOde(pixels):
    return float(pixels) / float(pixels_in_an_ode_unit)

def getOdePos(pos):
    return (pixelsToOde(pos[0]), pixelsToOde(pos[1]), 0)

def getPixelPos(odePos):
    return (odeToPixels(odePos[0]), odeToPixels(odePos[1]))

def createBoxRect(pos):
    return (pos[0] - BLOCK_WIDTH/2, pos[1] - BLOCK_HEIGHT/2, BLOCK_WIDTH, BLOCK_HEIGHT)

def near_callback(args, geom1, geom2):
    world,contactgroup = args
    contacts = ode.collide(geom1, geom2)
    for c in contacts:
        c.setBounce(BOUNCE)
        c.setMu(5000)
        j = ode.ContactJoint(world, contactgroup, c)
        j.attach(geom1.getBody(), geom2.getBody())
        
def getNext(ind, max):
    if ind < max - 2:
        return ind + 1
    else:
        return 0

class OdePhysicsManager:
    def __init__(self):
        self.world = ode.World()
        self.world.setGravity( (0,GRAVITY,0) )
        self.world.setERP(0.8)
        self.world.setCFM(1E-5)
        self.space = ode.Space()
        floor = ode.GeomPlane(self.space, (0,-1,0), pixelsToOde(-FLOOR_POS))
        leftWall = ode.GeomPlane(self.space, (1,0,0), pixelsToOde(0))
        rightWall = ode.GeomPlane(self.space, (-1,0,0), pixelsToOde(-SCREEN_WIDTH))
        self.contactgroup = ode.JointGroup()
        self.blocks = []
        self.peas = []
        self.timeCounter = 0.0
        
    def dispose(self):
        pass
    
    def eventFired(self, id, block):
        if id == UserInterface.Block.DONE_GHOSTING_IN_EVENT:
            self.addBlock(block)
        elif id == UserInterface.Block.DONE_GHOSTING_OUT_EVENT:
            self.removeBlock(block)
    
    def removeBlock(self, block):
        raise "how do I do that?"
    
    def addBlock(self, block):
        #adjust pos from top left coord for center coord
        triMeshData = ode.TriMeshData()
        points = block.getPoints()
        verts = []
        faces = []
        #create two vertices for each point
        for point in points:
            frontPoint = getOdePos(point)
            verts.append(frontPoint)
            verts.append((frontPoint[0], frontPoint[1], 1.0))
        #create one triangle for each vertice
        numVerts = len(verts)
        for i in xrange(numVerts):
            if i % 2 == 0:
                faces.append((i, getNext(getNext(i, numVerts), numVerts), getNext(i, numVerts)))
            else :
                faces.append((i, getNext(i, numVerts), getNext(getNext(i, numVerts), numVerts)))
        print "verts:",verts, " faces=", faces
        triMeshData.build(verts, faces)
        block.geom = ode.GeomTriMesh(triMeshData, self.space)
        self.blocks.append(block)
    
    def addPea(self, pea):
        odePos = getOdePos(pea.pos)
        pea.body = ode.Body(self.world)
        mass = ode.Mass()
        mass.setSphere(2500, pixelsToOde(PEA_RADIUS))
        pea.body.setMass(mass)
    
        # Create a box geom for collision detection
        geom = ode.GeomSphere(self.space, pixelsToOde(PEA_RADIUS))
        geom.setBody(pea.body)
        
        pea.body.setPosition(odePos)
        self.peas.append(pea)
        
    def render(self, screen):
        for ball in self.peas:
            odePos = ball.body.getPosition()
            pos = getPixelPos(odePos)
            #print "drawing ball at ",pos
            pygame.draw.circle(screen, PEA_COLOR, pos, PEA_RADIUS)
        
        for block in self.blocks:
            #odePos = box.getPosition()
            #pos = getPixelPos(odePos)
            pygame.draw.polygon(screen, BLOCK_COLOR, block.getPoints(), BLOCK_LINE_THICKNESS)
    
    def update(self, timeD):
        self.timeCounter += (timeD*0.001)#milliseconds to seconds
        while self.timeCounter > physics_step_size:
            self.timeCounter -= physics_step_size
            self.space.collide((self.world,self.contactgroup), near_callback)
            self.world.step(physics_step_size)
            self.contactgroup.empty()
            for pea in self.peas:
                pea_pos = pea.body.getPosition()
                pea.body.setPosition((pea_pos[0], pea_pos[1], 0.0))
    