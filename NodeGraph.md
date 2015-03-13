# Purpose #
The NodeGraph class is responsible for holding the graph of nodes and for adding and removing nodes from that structure.  It is also be responsible for firing events to notify peas of world updates.


# Implementation Notes #

## Graph ##
Currently the NodeGraph implementation holds all nodes in a map indexed by the string representation of the nodes pixel position.  This is done to aid in calculation of jump nodes, which will need to be added and removed when the world updates.

## Nodes ##
In the current implementation, an instant of Node represents a potentially traversable segment, either a corner or a face of a block.

When a second node is attempted to be added to the same position as an existing node, its links are transfered to the existing node, and the existing nodes node count is incremented.

This basically represents the number of blocks that occupy that node.  For faces it will generally be 1 or 2, for corners it will generally be 1, 2, 3 or 4.

Rather than cull non traversable nodes, we're instead implementing a canTraverse function in each node type.  This function queries the node count to determine if it's full or not.

This should make the node removal function a lot easier, as you've just got to decrement the node count until it reaches 0 at which point the node can be unlinked from its neighbors and removed from the graph.

## Ghosting ##
Ghosting nodes are not currently implemented, I'm expecting it to be a royal pain in the ass and involve a few more states and events

## Jump Nodes ##
Jump nodes are not currently implemented.  I anticipate that they will be slightly easier than Ghosting.