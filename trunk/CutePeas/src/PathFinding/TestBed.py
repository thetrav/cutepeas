from Node import *
from Images import *

nodes = []

def createNodes():
    global nodes
    one = Node(38, 20, None)
    two = Node(74, 20, None)
    three = Node(109, 20, None)
    
    four = Node(127, 38, None)
    five = Node(127, 69, None)
    six = Node(127, 99, None)
    
    one.addLink(two)
    two.addLink(one)
    two.addLink(three)
    three.addLink(two)

    nodes = [one, two, three, four, five, six]
    
    return;
    
def drawNodes(screen):
    for i in nodes:
        screen.blit(images["Gold-Ball"], (i.position.x, i.position.y))