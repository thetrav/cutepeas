Pea movement will need to work fairly closely with the PathFinding implementation, specifically the node objects.

# Challenges within Pea Movement #

  * Peas must be rotated and placed in the right place so it looks like they are following the blocks along.
  * Care must be taken not to overlap the pea image and the surface image
  * Pea shadow placement may be tricky, haven't thought about it much yet
  * Peas jumping between blocks (separate to the scored jumps) will need to look like the pea is actually jumping, not just moving accross thin air

While the initial implementation is relatively straight forward, the peas are the star of the show, so all of their movements should be aesthetically pleasing, and ideally the animations should give character to an otherwise very static character.  This gives a lot of scope to doing extra work above and beyond what's required for functionality in terms of whole sprite animations or even animated features within the character like blinking eyes, emitting particles, or morphing the pea shape itself.  Designing and then implementing all of these extra bits should be a non trivial challenge.


## Implementation idea ##
danc suggests breaking the movement patterns into different segments.
This could be a pretty easy way to do it, because in reality we know how much time we want it to take for each pea to traverse each node segment, and we can work out which sort of traversal is occurring, so maybe a separate bit of code for each of the identified movement modes and then just use a timer rather than collisions to work out that nodes have been reached?


![http://lostgarden.com/uploaded_images/ExamplesOfPeaMovement-771062.jpg](http://lostgarden.com/uploaded_images/ExamplesOfPeaMovement-771062.jpg)

## Integration with Physics ##
Remember also that there must be a mechanism for transferring between the PhysicsSimulation  and PathFinding systems.  This will involve:
  1. ensuring that the update happens on the correct system
  1. detaching and re-associating peas from nodes when they jump & land.

Another idea I've had is to use the physics system to move the pea around in movement mode as well as in regular mode, here's how it works:
  1. The pea is transitioning between falling and moving modes (min Y velocity at a collision with a horizontal surface)
  1. The transition itself is done on a collision
  1. The peas velocity becomes a normalized vector of the surfaces direction
  1. If the next node is in the other direction the vector will be reversed
  1. When rendered the pea is rotated to face its vector

This should get relatively smooth transitions as well as deal with the issue of which side the pea should be to avoid overlapping the block graphic.
There are a few problems to this approach that I still need to solve

  1. What happens when the pea collides with multiple surfaces at corners?
  1. How do we handle a pea going around a corner?  in the current description it just hits the corner and rotate 90 degrees, something smoother would be preferable (this one isn't game breaking though)