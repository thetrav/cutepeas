# Implementation #

Ok, so now we've got a basic implementation of the NodeGraph down.

The path finding has finally been implemented using a min max tree.  Every find path operation will traverse the connected node graph in its entirety to build the score graph, and then traverse the highest scoring branches to build the path.

The graph looks pretty basic when printed out at the moment because we're almost always dealing with a linear path of nodes, however this is likely to change when jump nodes are added.

The current structure should support the addition of jump nodes, however I've got a nasty feeling I implemented a depth first method of building the graph, when what we really want is breadth first, as that would model distance far more effectively and prevent big loopy paths.

The other thing worthy of note is that there's no attempt to ensure the pea attempts to get to the closest high point, so if there's a stack of two blocks next to it and a stack on the other side of the plate the pea could go for either of them.

## Alternative ##

I've been thinking about an alternative that may simplify the code a lot, GateAndLinkPathFinding