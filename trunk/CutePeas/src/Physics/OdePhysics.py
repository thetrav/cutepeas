import ode
from Constants import *
import Constants
import Objects.Block
import pygame
import Coordinates
import Animation
import Event
import UserInterface.Scroll

physics_step_size = 0.016
GRAVITY = 9.81
BOUNCE = 0.8

PEA_COLOR = (0,200,0)
BLOCK_COLOR = (200,200,0)
SURFACE_LINE_THICKNESS = 4
PEA_COLLISION_EVENT = "pea collision event"

def returnBounceFunction():
    return BOUNCE

def createBoxRect(odePos):
    return (odePos[0] - BLOCK_WIDTH_ODE/2, odePos[1] - BLOCK_HEIGHT_ODE/2, BLOCK_WIDTH_ODE, BLOCK_HEIGHT_ODE)

def near_callback(args, geom1, geom2):
    if geom1.isPea() and geom2.isPea():
        return
    if geom1.isPea():
        closeCollisionTest(geom1, geom2, args)
    elif geom2.isPea():
        closeCollisionTest(geom2, geom1, args)

def closeCollisionTest(peaGeom, geom, args):
    world,contactgroup = args
    contacts = ode.collide(peaGeom, geom)
    collision = False
    for c in contacts:
        collision = True
        bounce = geom.bounce
        c.setBounce(bounce)
        c.setMu(5000)
        j = ode.ContactJoint(world, contactgroup, c)
        j.attach(peaGeom.getBody(), geom.getBody())
    if collision:
        #print ' hit ', geom.name
        Event.fireEvent(PEA_COLLISION_EVENT, (peaGeom, geom))
        
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
        
        #floor
        self.createPlane((0,-1,0), -FLOOR_POS_ODE, "floor")
        #left wall 
        self.createPlane((1,0,0), 0, "left wall")
        #right wall
        self.createPlane((-1,0,0), -SCREEN_WIDTH_ODE, "right wall")
        
        self.contactgroup = ode.JointGroup()
        self.blocks = []
        self.peas = []
        self.timeCounter = 0.0
        Animation.animations.append(self)
    
    def createPlane(self, normal, odeDistance, name):
        plane = ode.GeomPlane(self.space, normal, odeDistance)
        plane.isPea = returnFalseFunction
        plane.isBlock = returnFalseFunction
        plane.bounce = BOUNCE
        plane.name = name
    
    def dispose(self):
        Animation.animations.remove(self)
    
    def removeBlock(self, block):
        self.blocks.remove(block)
        self.space.remove(block.geom)
        block.geom.block = None
        block.geom = None
    
    def placeBlock(self, block):
        triMeshData = ode.TriMeshData()
        points = block.getPoints()
        verts = []
        faces = []
        #create two vertices for each point
        for point in points:
            frontPoint = point
            verts.append(frontPoint)
            verts.append((frontPoint[0], frontPoint[1], 1.0))
        #create one triangle for each vertice
        numVerts = len(verts)
        for i in xrange(numVerts):
            if i % 2 == 0:
                faces.append((i, getNext(getNext(i, numVerts), numVerts), getNext(i, numVerts)))
            else :
                faces.append((i, getNext(i, numVerts), getNext(getNext(i, numVerts), numVerts)))
        triMeshData.build(verts, faces)
        geom = ode.GeomTriMesh(triMeshData, self.space)
        geom.block = block
        geom.isPea = returnFalseFunction
        geom.isBlock = returnTrueFunction
        geom.bounce = block.bounce
        self.blocks.append(block)
        geom.name="block"
        block.geom = geom
        
    
    def addPea(self, pea):
        odePos = pea.odePos
        pea.body = ode.Body(self.world)
        mass = ode.Mass()
        mass.setSphere(2500, Coordinates.pixelsToOde(PEA_RADIUS))
        pea.body.setMass(mass)
    
        # Create a box geom for collision detection
        geom = ode.GeomSphere(self.space, Coordinates.pixelsToOde(PEA_RADIUS))
        geom.setBody(pea.body)
        
        #pea.body.setPosition(odePos)
        self.peas.append(pea)
        geom.pea = pea
        geom.isPea = returnTrueFunction
        geom.isBlock = returnFalseFunction
        geom.name = "pea"
        pea.geom = geom
        
    def removePea(self, pea):
        #self.peas.remove(pea)
        #self.space.remove(pea.geom)
        #pea.body = None
        #pea.geom.pea = None
        #pea.geom = None
        pea.body.disable()
        pea.geom.disable()
        
    def render(self, screen):
        if Constants.DRAW_HIT_BOXES:
            for block in self.blocks:
                UserInterface.Scroll.globalViewPort.drawPolygon(screen, BLOCK_COLOR, block.getPoints(), SURFACE_LINE_THICKNESS)
    
    def update(self, timeD):
        self.timeCounter += (timeD*0.001)#milliseconds to seconds
        while self.timeCounter > physics_step_size:
            self.timeCounter -= physics_step_size
            self.space.collide((self.world,self.contactgroup), near_callback)
            self.world.step(physics_step_size)
            self.contactgroup.empty()
            #nullify any z axis velocity and rotation
            for pea in self.peas:
                pea_pos = pea.body.getPosition()
                pea.body.setPosition((pea_pos[X], pea_pos[Y], 0.0))
                vel = pea.body.getLinearVel()
                pea.body.setLinearVel((vel[X], vel[Y], 0))
                pea.body.setAngularVel((0, 0, 0))#pea.body.getAngularVel()[Z]))
                
    def jumpPea(self, pea, vel):
        odePos = (pea.odePos[X], pea.odePos[Y], 0)
        pea.body.setPosition(odePos)
        pea.body.setLinearVel(vel)
        pea.body.enable()
        pea.geom.enable()
        pea.oneFreeCollision = True #this is a dirty filthy hack.  I believe moving the pea through a heap of stuff wrecks collision detection
    