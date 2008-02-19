

class Particles:
    def __init__(self):
        self.emitters = []
    
    def addEmitter(self, pos, emitter):
        self.emitters.append(emitter)
        emitter.addEndListener(self)
    
    def update(self, timeD):
        for emitter in self.emitters:
            emitter.update(timeD)
    
    def render(self, screen):
        for emitter in self.emitters:
            emitter.render(screen)
    
class Particle:
    def __init__(self, image):
        pass
    
    def update(self, timeD):
        pass
    
    def render(self, screen):
        pass
    
class Emitter:
    def __init__(self, maxParticles=5, maxEmitTime = 5, minEmitTime = 0, runTime=0):
        self.listeners = []
        self.particles = []
        self.runTime = runTime
        self.maxParticles = maxParticles
        self.maxEmitTime = maxEmitTime
        self.minEmitTime = minEmitTime
    
    def update(self, timeD):
        for particle in self.particles:
            particle.update(timeD)
        #spawn more?
        #time to die?
            #notify listeners
            
    def render(self, screen):
        for particle in self.particles:
            particle.render(screen)
    
    def addEndListener(self, listener):
        self.listeners.append(listener)