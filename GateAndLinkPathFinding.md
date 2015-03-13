# Introduction #
The first NodeGraph implementation, while functional, is becoming slightly cumbersome to work with.

To solve the problem with peas squeezing between two diagonal blocks, all links that lead to an overhang are marked blocked.
![http://img207.imageshack.us/img207/8119/overhangnz5.gif](http://img207.imageshack.us/img207/8119/overhangnz5.gif)

Each potential corner of a block occupies a corner of a gate, therefore gates can be occupied by a maximum of 4 corners

Each of these gates are linked to a maximum of 4 other gates (out of a potential 8 gates once you account for ramps)

![http://img378.imageshack.us/img378/9129/gatessr7.gif](http://img378.imageshack.us/img378/9129/gatessr7.gif)

# Domain #

The three modeled objects are gates, corners and links.

Gates can have 0 to 4 corners, alternatively 1 to 4 if we only create the gates on demand.  They are, top left, top right, bottom left and bottom right

If we assume peas can't climb along the ceiling of blocks then corners each have 1 or 2 links.  Once placed corners always have exactly 1 gate

Links each have exactly 2 corners, links can either be open or blocked.
There are five kinds of links: left, top, right, left ramp, right ramp.

A pea is going to approach a gate via a link (the inbound link) and want to know what open outbound links there are.

To calculate this the gate is first queried, and it then queries all its links under all its corners to build a list of open links.

# calculating traversable paths #

A left link is open unless the gate of its top corner has either the top left or bottom left positions occupied (indicating an overhang to the left or another block to the left)

![http://img168.imageshack.us/img168/1493/leftbv0.gif](http://img168.imageshack.us/img168/1493/leftbv0.gif)

A right link is open unless the gate of its top corner has either the top right or bottom right positions occupied (indicating either an overhang to the right or another block to the right)

![http://img65.imageshack.us/img65/13/rightss3.gif](http://img65.imageshack.us/img65/13/rightss3.gif)

A top link is open unless the gate of its left corner has the top right position occupied AND the gate of its right corner has the top left position occupied (indicating a block directly on top)

![http://img168.imageshack.us/img168/8782/toplx2.gif](http://img168.imageshack.us/img168/8782/toplx2.gif)

A left ramp is open unless the gate of its top corner has the top left position occupied (indicating an overhang)

![http://img76.imageshack.us/img76/1773/leftrampmt0.gif](http://img76.imageshack.us/img76/1773/leftrampmt0.gif)

A right ramp is open unless the gate of its top corner has the top right position occupied (indicating an overhang)

![http://img76.imageshack.us/img76/1114/rightrampnm5.gif](http://img76.imageshack.us/img76/1114/rightrampnm5.gif)

## jump traversal ##
![http://img389.imageshack.us/img389/9004/pathssu3.gif](http://img389.imageshack.us/img389/9004/pathssu3.gif)

A jump between gates is available where a gate is jumpable and horizontally next to another jumpable gate
This allows peas to jump traverse between ramps, which looks pretty precarious in some situations, but they are ninja's after all :)

# Calculating jump positions #
Only gates can be jumped from

If only the bottom left position is occupied, then a right jump is allowed
If only the bottom right position is occupied, then a left jump is allowed

This does not allow peas to jump from the lower side of ramps, which may or may not be desired.
This also does not allow peas to jump from a peak made of two ramps /\

If any of these circumstances become desirable in the future it should be relatively simple to code in exceptions as all the link types and corner positions are explicitly maintained