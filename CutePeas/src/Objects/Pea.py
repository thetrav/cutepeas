from Constants import *
import PathFinding.GateAndLink.Path
import Constants
import Event
import Coordinates
import Animation
import Images
import Particles
import Physics.OdePhysics
import UserInterface.Score
import UserInterface.Scroll
import math

NODE_TIMER = 200
FALL_END_TIMER = 2000
MIN_VEL = 0.001
CELEBRATION_TIMER = 5000
GHOST_Y_VEL = Coordinates.pixelsToOde(-0.1)
TIME_HURT = 3000
MAX_SURVIVABLE_Y_VELOCITY = 20
TRANSITION_JUMP_TIMER = 400
GHOST_MAX_HEIGHT = Coordinates.pixelsToOde(-100)

PEA_RENDER_OFFSET_X = Coordinates.pixelsToOde(PEA_RADIUS)
PEA_RENDER_OFFSET_Y = Coordinates.pixelsToOde(PEA_RADIUS)

NINJA_RENDER_OFFSET_X = Coordinates.pixelsToOde(36)
NINJA_RENDER_OFFSET_Y = Coordinates.pixelsToOde(60)

PEA_HITBOX_COLOR = (0,255,0)
PEA_POS_COLOR = (150,0,0)

def climbAnimation(pea, timeD):
    if pea.currentNode == None:
        pea.findNewNodeAndPath()
        pea.timer = NODE_TIMER
    if pea.timer < 0:
        node = pea.path.pop(0)
        pea.setNode(node.gate)
        if node.link and node.link.isJumpTransition():
            pea.jumpTransition(node.link)
        if len(pea.path) == 0:
            if pea.currentNode.isJumpable():
                pea.jump()
            else:
                pea.path = PathFinding.GateAndLink.Path.findPath(pea.currentNode)
                
def transitionJumpAnimation(pea, timeD):
    pea.odePos = pea.body.getPosition()
    if pea.timer < 0:
        pea.endTransitionJump()
        
            
def jumpAnimation(pea, timeD):
    pea.odePos = pea.body.getPosition()
    vel = pea.body.getLinearVel()
    
    #test for fall death
    if pea.hitThisFrame != None and not pea.oneFreeCollision:
        geom = pea.hitThisFrame[0]
        yVel = pea.hitThisFrame[1][Y]
        if yVel > MAX_SURVIVABLE_Y_VELOCITY * (1 if not geom.isBlock() else geom.block.maxSurvivableVelocityMod):
            pea.jumpDeath() 
    pea.hitThisFrame = None
    
    #test for end of jump
    if vel[X] + vel[Y] > MIN_VEL:
        pea.timer = FALL_END_TIMER
    if pea.timer <= 0:
        pea.endScoredJump()
        
def celebrateAnimation(pea, timeD):
    if pea.timer <= 0:
        pea.endCelebration()
        
def deathAnimation(pea, timeD):
    if pea.timer <= 0:
        pea.image = Images.images["Pea-Ghost"]
        pea.odePos = (pea.odePos[X], pea.odePos[Y] + GHOST_Y_VEL * timeD)
        if pea.odePos[Y] < GHOST_MAX_HEIGHT:
            pea.odePos = Coordinates.pixelPosToOdePos((0, 0))
            pea.currentNode = None
            pea.previousNode = None
            pea.findNewNodeAndPath()
            pea.playAnimation = climbAnimation
            pea.image = Images.images["Pea-Standard"]
            
class Pea:
    def __init__(self, odePos, nodeGraph, physics):
        self.image = Images.images["Pea-Standard"]
        self.body = None
        self.odePos = odePos
        self.initPathFinding(nodeGraph)
        Event.addListener(EVENT_NODE_GRAPH_UPDATED, self)
        Event.addListener(Physics.OdePhysics.PEA_COLLISION_EVENT, self)
        self.listeners = []
        self.timer = 0
        self.physicsManager = physics
        self.playAnimation = climbAnimation
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
        self.odePos = self.currentNode.odePos
        self.timer = NODE_TIMER
            
    def render(self, screen):
        if Constants.DRAW_PATH:
            for node in self.path:
                node.render(screen)
        if self.playAnimation == celebrateAnimation:
            self.renderCelebration(screen)
        self.particleSystem.render(screen)
        UserInterface.Scroll.globalViewPort.blit(screen, self.image, (self.odePos[X] - PEA_RENDER_OFFSET_X, self.odePos[Y] - PEA_RENDER_OFFSET_Y))
        if Constants.DRAW_HIT_BOXES:
            UserInterface.Scroll.globalViewPort.drawCircle(screen, PEA_HITBOX_COLOR, self.odePos, PEA_RADIUS)
            posText = str(math.floor(self.odePos[X])) + ', ' + str(math.floor(self.odePos[Y]))
            UserInterface.Scroll.globalViewPort.renderText(posText, self.odePos, screen, PEA_POS_COLOR, "PEA_FONT")
        
    def renderCelebration(self, screen):
        ninjaPos = (self.odePos[X] - NINJA_RENDER_OFFSET_X, self.odePos[Y] - NINJA_RENDER_OFFSET_Y)
        UserInterface.Scroll.globalViewPort.blit(screen, Images.images["Alert-Ninja"], ninjaPos)
        
    def jumpTransition(self, link):
        originPos = link.origin.odePos
        self.odePos = (originPos[X], originPos[Y] - Coordinates.pixelsToOde(PEA_RADIUS))
        self.physicsManager.jumpPea(self, (link.origin.gate.getJumpDirection()[X]*5.5, -2.0, 0.0))
        self.timer = TRANSITION_JUMP_TIMER
        self.playAnimation = transitionJumpAnimation
        
    def jump(self):
        self.currentFlag = self.currentNode.getFlag()
        self.currentFlag.startJump(self)
        self.odePos = (self.odePos[X], self.odePos[Y] - Coordinates.pixelsToOde(PEA_RADIUS*1.5))
        self.physicsManager.jumpPea(self, (self.currentNode.getJumpDirection()[X]*4.0, -3.5, 0.0))
        self.playAnimation = jumpAnimation
        self.timer = FALL_END_TIMER
        
    def update(self, timeD):
        self.timer -= timeD
        self.playAnimation(self, timeD)
        self.particleSystem.update(timeD)
        self.oneFreeCollision = False
                
    def eventFired(self, eventId, source):
        if eventId == EVENT_NODE_GRAPH_UPDATED:
            if not self.nodeGraph.hasGateAt(self.currentNode.odePos):
                self.currentNode = self.nodeGraph.findNearestNode(self.currentNode.odePos)
            self.path = PathFinding.GateAndLink.Path.findPath(self.currentNode)
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
        self.currentFlag.endJump(False)
        self.currentFlag = None
        self.beginDeathAnimation()
    
    def endTransitionJump(self):
        self.physicsManager.removePea(self)
        self.playAnimation = climbAnimation
        self.timer = NODE_TIMER
        if self.nodeGraph.findNearestNode(self.odePos) != self.currentNode:
            self.beginClimb()
        
    def endScoredJump(self):
        self.physicsManager.removePea(self)
        self.currentFlag.endJump(True)
        self.currentFlag = None
        self.beginCelebration()
        
    def beginCelebration(self):
        self.timer = CELEBRATION_TIMER
        self.playAnimation = celebrateAnimation
        self.image = Images.images["Pea-Happy"]
        self.particleSystem.addEmitter(Particles.ExplodeEmitter(self.odePos, CELEBRATION_TIMER))
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
        nearestNode = self.nodeGraph.findNearestNode(self.odePos)
        if nearestNode.pea == None: 
            self.setNode(nearestNode)
            self.path = PathFinding.GateAndLink.Path.findPath(self.currentNode)
        else:
            self.currentNode = None