class BlockRef:
    def __init__(self, blockID):
        self.blockID = blockID
        self.surfaces = []  
    
    def render(self, screen):
        for surface in self.surfaces:
            surface.render(screen)           