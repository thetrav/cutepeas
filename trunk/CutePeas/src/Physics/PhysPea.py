from Vector import Vector
class PhysPea:
    
    def __init__(self, startVec):
        print('Creating Pea Physics Properties')
        self.state = 'walking'
        self.startCoord = startVec
        self.xvelocity = 0
        self.yvelocity = 0
        self.hitCoord = Vector()
        self.radius = 17
        self.currentCoord = startVec
        
        self.numNormalBounces = 0
        self.numSpringBounces = 0
        self.numGelBounces = 0
        
        self.hitSurfaces = {}