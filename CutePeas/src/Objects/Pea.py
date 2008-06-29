from Constants import *
import pygame.transform as xform
import pygame.draw
import PathFinding.NodeGraph
import Constants
import Event
import Coordinates
import Animation
import Images
import Particles
import Physics.OdePhysics
import UserInterface.Score

NODE_TIMER = 200
FALL_END_TIMER = 2000
MIN_VEL = 0.001
CELEBRATION_TIMER = 5000
GHOST_Y_VEL = -0.1
TIME_HURT = 3000
MAX_SURVIVABLE_Y_VELOCITY = 12

def workOutJumpDirection(node):
    for linkedNode in node.linkedNodes:
        if node.pos[X] != linkedNode.pos[Y]:
            return -1 if node.pos[X] < linkedNode.pos[X] else 1

def climbAnimation(pea, timeD):
    if pea.currentNode == None:
        pea.findNewNodeAndPath()
        pea.timer = NODE_TIMER
    if pea.timer < 0:
        pea.setNode(pea.path.pop(0))
        if len(pea.path) == 0:
            if pea.currentNode.isJumpable() and (pea.currentNode.flag == None or pea.currentNode.flag not in pea.flags):
                pea.jump()
            else:
                pea.path = PathFinding.NodeGraph.findPath(pea.currentNode)
            
def jumpAnimation(pea, timeD):
    pea.pos = Coordinates.odePosToPixelPos(pea.body.getPosition())
    pos = pea.pos
    vel = pea.body.getLinearVel()
    
    #test for fall death
    if pea.hitThisFrame != None and not pea.oneFreeCollision:
        geom = pea.hitThisFrame[0]
        yVel = pea.hitThisFrame[1][Y]
        print 'hit at ', yVel
        if yVel > MAX_SURVIVABLE_Y_VELOCITY * (1 if not geom.isBlock() else geom.block.maxSurvivableVelocityMod):
            pea.jumpDeath() 
    pea.hitThisFrame = None
    
    #test for end of jump
    if vel[X] + vel[Y] > MIN_VEL:
        pea.timer = FALL_END_TIMER
    if pea.timer <= 0:
        pea.endJump()
        
def celebrateAnimation(pea, timeD):
    if pea.timer <= 0:
        pea.endCelebration()
        
def deathAnimation(pea, timeD):
    if pea.timer <= 0:
        pea.image = Images.images["Pea-Ghost"]
        pea.pos = (pea.pos[X], pea.pos[Y] + GHOST_Y_VEL * timeD)

class Pea:
    def __init__(self, pos, nodeGraph, physics):
        self.image = Images.images["Pea-Standard"]
        self.body = None
        self.pos = pos
        self.initPathFinding(nodeGraph)
        Event.addListener(EVENT_NODE_GRAPH_UPDATED, self)
        Event.addListener(Physics.OdePhysics.PEA_COLLISION_EVENT, self)
        self.listeners = []
        self.timer = 0
        self.physicsManager = physics
        self.playAnimation = climbAnimation
        self.flags = []
        self.currentFlag = None
        
        Animation.animations.append(self)
        self.particleSystem = Particles.ParticleSystem()
        self.blocksHit = []
        self.physicsManager.addPea(self)
        self.physicsManager.removePea(self)
        self.hitThisFrame = None
    
    def initPathFinding(self, nodeGraph):
        self.currentNode = None
        self.nodeGraph = nodeGraph
        self.findNewNodeAndPath()
        self.previousNode = None
    
    def dispose(self):
        Event.removeListener(EVENT_NODE_GRAPH_UPDATED, self)
        Animation.animations.remove(self)

    def getNode(self):
        return self.currentNode
    
    def setNode(self, node):
        self.previousNode = self.currentNode
        self.currentNode = node
        self.pos = self.currentNode.pos
        self.timer = NODE_TIMER
            
    def render(self, screen):
        if Constants.DRAW_PATH:
            for node in self.path:
                node.render(screen, (255,255,0))
        if self.playAnimation == celebrateAnimation:
            self.renderCelebration(screen)
        self.particleSystem.render(screen)
        screen.blit(self.image, (self.pos[X] - PEA_RADIUS, self.pos[Y] - PEA_RADIUS))
        
    def renderCelebration(self, screen):
        ninjaPos = (self.pos[X] - 36, self.pos[Y] - 60)
        screen.blit(Images.images["Alert-Ninja"], ninjaPos)
        
    def jump(self):
        if self.currentNode.flag != None:
            self.currentFlag = self.currentNode.flag 
        else :
            self.currentFlag = PathFinding.NodeGraph.Flag(self.pos, 5)
            self.nodeGraph.placeFlag(self.currentFlag, self.currentNode)
        self.flags.append(self.currentFlag)
        self.pos = (self.pos[X], self.pos[Y] - PEA_RADIUS*1.5)
        self.physicsManager.jumpPea(self, (workOutJumpDirection(self.currentNode)*4, -3.5, 0.0))
        self.playAnimation = jumpAnimation
        self.timer = FALL_END_TIMER
        
    def update(self, timeD):
        self.timer -= timeD
        self.playAnimation(self, timeD)
        self.particleSystem.update(timeD)
        self.oneFreeCollision = False
                
    def eventFired(self, eventId, source):
        if eventId == EVENT_NODE_GRAPH_UPDATED:
            if not source.hasNodeAt(self.currentNode.pos):
                self.currentNode = source.findNearestNode(self.currentNode.pos)
            self.path = PathFinding.NodeGraph.findPath(self.currentNode)
        elif eventId == Physics.OdePhysics.PEA_COLLISION_EVENT:
            self.hitThisFrame = (source[1], self.body.getLinearVel())
            if source[1].isBlock() and source[0] == self.geom and source[1].block not in self.blocksHit:
                self.blocksHit.append(source[1].block)
    
    def beginDeathAnimation(self):
        self.playAnimation = deathAnimation
        self.image = Images.images["Pea-Hurt"]
        self.timer = TIME_HURT
    
    def jumpDeath(self):
        self.physicsManager.removePea(self)
        self.currentFlag.deadlyJump()
        self.currentFlag = None
        self.beginDeathAnimation()
    
    def endJump(self):
        self.physicsManager.removePea(self)
        self.currentFlag.jumpDone(self)
        self.currentFlag = None
        self.beginCelebration()
        
    def beginCelebration(self):
        self.timer = CELEBRATION_TIMER
        self.playAnimation = celebrateAnimation
        self.image = Images.images["Pea-Happy"]
        self.particleSystem.addEmitter(Particles.ExplodeEmitter(self.pos, CELEBRATION_TIMER))
        for block in self.blocksHit:
            Event.fireEvent(UserInterface.Score.SCORE_AWARDED_EVENT, block.getBouncePoints())
        self.blocksHit = []
    
    def endCelebration(self):
        self.image = Images.images["Pea-Standard"]
        self.beginClimb()
        
    def beginClimb(self):
        self.currentNode = None
        self.playAnimation = climbAnimation
        self.findNewNodeAndPath()

    def findNewNodeAndPath(self):
        nearestNode = self.nodeGraph.findNearestNode(self.pos)
        if nearestNode.pea == None: 
            self.setNode(nearestNode)
            self.path = PathFinding.NodeGraph.findPath(self.currentNode)
        else:
            self.currentNode = None