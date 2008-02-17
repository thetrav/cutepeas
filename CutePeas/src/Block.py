import Physics.Vector as Vec
import PathFinding.Node as Node

class Block:
    def __init__(self, position):
        self.position = position
        self.nodes = []
        
    def createNodes(self):
        self.nodes = []
        