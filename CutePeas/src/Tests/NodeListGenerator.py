from PathFinding import Node

# In all cases returns a tuple: (firstnode, [firstnode, secondnode, ...])
# To determine direction of the initial path, use a positive/negative step value accordingly

DEBUG = False

def createHorizontalNodeList(surface, nodeCount, startX, y, stepX, img=None):
    currentX = startX
    startNode = prevNode = currentNode = Node.Node(currentX, y, surface, None, None, img)
    nodes = [startNode]
    for i in range(1, nodeCount):
        currentX += stepX
        currentNode = Node.Node(currentX, y, surface, prevNode, None, img)
        __linkNodesAndAppendToNodeList(nodes, prevNode, currentNode)
        prevNode = currentNode
    __assertStartNodeAndDebug(startNode, nodes)
    return (startNode, nodes)
        
def createVerticalNodeList(surface, nodeCount, x, startY, stepY, img=None):
    currentY = startY
    startNode = prevNode = currentNode = Node.Node(x, startY, surface, None, None, img)
    nodes = [startNode]
    for i in range(1, nodeCount):
        currentY += stepY
        currentNode = Node.Node(x, currentY, surface, prevNode, None, img)
        __linkNodesAndAppendToNodeList(nodes, prevNode, currentNode)
        prevNode = currentNode
    __assertStartNodeAndDebug(startNode, nodes)
    return (startNode, nodes)

def createDiagonalNodeList():
    pass

def __linkNodesAndAppendToNodeList(nodes, prevNode, currentNode):
    Node.nodeDoublyLink(prevNode, currentNode)
    nodes.append(currentNode)
    
def __assertStartNodeAndDebug(startNode, nodes):
    assert startNode is nodes[0]
    __debugTraverse(startNode)
    
def __debugTraverse(node):
    if not DEBUG or node is None:
        return
    print node
    __debugTraverse(node.nextNode())
        

if __name__ == '__main__':
    node, nodelist = createHorizontalNodeList(None, 10, 20, 30, 10)


