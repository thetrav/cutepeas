import Physics.Vector as Vec

def nodeLink(nodeA, nodeB):
    nodeA.addLink(nodeB)
    nodeB.addLink(nodeA)

class Node:
    "Pathfinding node"
    def __init__(self, x, y, surface):
        self.__initCommon(x, y, surface)

    def addLink(self, node):
        if node in self.links:
            return
        else:
            self.links.append(node)
        
    def delLink(self, node):
        if node in self.links:
            self.links.remove(node)
    
    def __initCommon(self, x, y, surface):
        self.position = Vec.Vector(x=x, y=y)
        self.links = []
        self.surface = surface

    # Kamal: -- Pea node-traversal testing --
    # Not sure how the phys. stuff works, temporarily assuming that it's safe to use x/y
    # directly off the internal vector instead of caching it locally. 
    def getPos(self):
        return (self.position.x, self.position.y)
        
    # Kamal: Some questions on traversals:  
    #    how do i get the next node? implement some sort of getNext() on a node - similar to the way a linked list is structured?
    #    What are node.links meant to represent exactly? Are we going to have an arbitrary tree of nodes?
    #    Does a pea get a single node supplied to it, or a list of nodes and traverses that list (and then what about node.links :P)? 
    #    Can a pea get a situation where it can choose one node path or another off a current node (i.e. a branching), e.g.
    #        node.getNext() returns a list of possible next nodes?
    #    A pea moves thru nodes, then reverses direction because it's reached the end of it's node list - a doubly-linked list?
    
    # Testing - assuming a doubly linked list structure - sorry to mess with your code Rory - considered making a copy, but thought
    # this might be a good time to start thinking about integrating - you are free to mess with my Pea.py of course :P
    
    def __init__(self, x, y, surface, prevnode=None, nextnode=None, img=None):
        self.__initCommon(x, y, surface)
        self.prev = prevnode
        self.next = nextnode
        self.image = img
        
    def nextNode(self):
        return self.next
    
    def prevNode(self):
        return self.prev
    
    def setNextNode(self, node):
        self.next = node
    
    def setPrevNode(self, node):
        self.prev = node
    
    def __repr__(self):
        pos = self.getPos()
        npos = None
        ppos = None
        if self.nextNode() is not None:
            npos = self.nextNode().getPos()
        if self.prevNode() is not None:
            ppos = self.prevNode().getPos()
        return 'node[pos=%s,prevNode[%s],nextNode[%s]]' % (pos, ppos, npos)

    """
    Generic inorder traversal method:
        node - node to traverse using it's nextNode() method to move forward, prevNode() is NOT used.
        func - func to execute on each node encountered, must be of the form: myfunc(node, data)
        data - whatever data is suitable for the func
    """
    def __traverse(self, node, func, data):
        if node is None:
            return
        func(node, data)
        self.__traverse(node.nextNode(), func, data)

    def __renderNode(self, node, screen):
        if node.image is None:
            return
        node.image.get_rect().move(node.getPos())
        screen.blit(node.image, node.getPos())
        
    def render(self, screen):
        self.__traverse(self, self.__renderNode, screen)

        
"""
Links prevNode's next to nextNode, and nextNode's prev to prevNode
"""
def nodeDoublyLink(prevNode, nextNode):
    prevNode.setNextNode(nextNode)
    assert prevNode.nextNode() is nextNode
    nextNode.setPrevNode(prevNode)
    assert nextNode.prevNode() is prevNode 
