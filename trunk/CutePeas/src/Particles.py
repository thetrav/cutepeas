import Images
import UserInterface.Scroll
import Coordinates

GRAVITY = 0.008
FRICTION = 1

class ParticleSystem:
    def __init__(self):
        self.emitters = []
    
    def addEmitter(self, emitter):
        self.emitters.append(emitter)
        emitter.addEndListener(self)
    
    def update(self, timeD):
        for emitter in self.emitters:
            emitter.update(timeD)
    
    def render(self, screen):
        for emitter in self.emitters:
            emitter.render(screen)
    
    def emitterEnded(self, emitter):
        self.emitters.remove(emitter)
    
class Particle:
    def __init__(self, image, odePos, odeVel):
        self.image = image
        self.odePos = [odePos[0],odePos[1]]
        self.odeVel = [odeVel[0], odeVel[1]]
    
    def update(self, timeD):
        self.odePos[0] = self.odePos[0] + self.odeVel[0]
        self.odePos[1] = self.odePos[1] + self.odeVel[1]
    
    def render(self, screen):
        UserInterface.Scroll.globalViewPort.blit(screen, self.image, self.odePos)

        
class ExpireParticle(Particle):
    def __init__(self, image, odePos, odeVel, timeToLive, listener):
        Particle.__init__(self, image, odePos, odeVel)
        self.timeToLive = timeToLive
        self.listener = listener
    
    def update(self, timeD):
        Particle.update(self, timeD)
        self.timeToLive = self.timeToLive - timeD
        if self.timeToLive <= 0:
            self.listener.particleExpired(self)
            
class GravityParticle(ExpireParticle):
    def __init__(self, image, odePos, odeVel, timeToLive, listener):
        ExpireParticle.__init__(self, image, odePos, odeVel, timeToLive, listener)
        
    def update(self, timeD):
        self.odeVel[1] = self.odeVel[1] + Coordinates.pixelsToOde(timeD * GRAVITY)
        self.odeVel[0] = self.odeVel[0] * FRICTION
        ExpireParticle.update(self, timeD)
        
class Emitter:
    def __init__(self):
        self.particles = []
        self.listeners = []
    
    def update(self, timeD):
        for particle in self.particles:
            particle.update(timeD)
            
    def render(self, screen):
        for particle in self.particles:
            particle.render(screen)
    
    def addEndListener(self, listener):
        self.listeners.append(listener)
        
class ExplodeEmitter(Emitter):
    def __init__(self, odePos, timeToLive = 5000):
        Emitter.__init__(self)
        self.timeToLive = timeToLive
        self.odePos = [odePos[0],odePos[1]]
        self.emitExplosion()
    
    def emitExplosion(self):
        self.explodeTimer = 1500
        odePos = self.odePos
        img = Images.images["Gold-Ball"]
        for vel in (
                    (-1, -4.3),
                    (-0.4, -3.9),
                    ( 0.1, -4),
                    ( 0.5, -4.5),
                    ( 0.95, -3.8),
                    (-1.2, -3),
                    (-0.7, -3.3),
                    ( 0, -3.4),
                    ( 0.3, -3.2),
                    ( 1.1, -3.1),
                    ):
            self.particles.append(GravityParticle(img, odePos, Coordinates.pixelPosToOdePos(vel), 500, self))
    
    def update(self, timeD):
        Emitter.update(self, timeD)
        
        self.explodeTimer = self.explodeTimer - timeD
        
        if self.explodeTimer <= 0:
            self.emitExplosion()
        
        self.timeToLive = self.timeToLive - timeD
        if self.timeToLive <= 0:
            for listener in self.listeners:
                listener.emitterEnded(self)
                
    def particleExpired(self, particle):
        self.particles.remove(particle)