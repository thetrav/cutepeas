import Physics.Vector as Vec

def nodeLink(nodeA, nodeB):
    nodeA.addLink(nodeB)
    nodeB.addLink(nodeA)
    
class Node:
    "Pathfinding node"
    def __init__(self, x, y, surface):
        self.position = Vec.Vector(x=x, y=y)
        self.links = []
        self.surface = surface
        
    def addLink(self, node):
        if node in self.links:
            return
        else:
            self.links.append(node)
        
    def delLink(self, node):
        if node in self.links:
            self.links.remove(node)
    
    