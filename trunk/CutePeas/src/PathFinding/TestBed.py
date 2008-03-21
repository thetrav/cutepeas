from NodeGraph import *
from UserInterface.Block import *
from Images import *

graph = NodeGraph(9,10)
images["test"] = "test"
block = Block("test", "test")
block.x = 263
block.y = -1
blockNodes = block.createNodes()
graph.addNodes(blockNodes)


for key in graph.nodes:
    node = graph.nodes[key]
    print "node at:"+key+" count="+str(len(node.linkedNodes)) + " nodes:"+str([linked.pos for linked in node.linkedNodes])

path = findPath(graph.nodes['(156, 10)'])

