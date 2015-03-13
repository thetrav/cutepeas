# Notes #

  * Physics sim is not used for general movement and animations, only used when peas jump
  * Physics sim deals with peas, surfaces and bounce listeners nothing else (eg, no calling the block class, no messing with the score, no doing any rendering [for rendering the surfaces and peas in debug mode](except.md))

The major interface to the physics engine is going to be as such:

## Physics.addSurfaces(surfacesList) ##
This will be called by the UI whenever a block is dropped that contains new Surface objects.  The surface objects will all have been created and initialized to the correct internal state (eg, pos, bounciness etc).

## Physics.removeSurfaces(surfacesList) ##
This will be called by the UI whenever a block is deleted.  The list of surfaces will contain the same object references that were sent in a previous call to addSurfaces

## Physics.update(pea, timeD) ##
This will be called by the render loop or a pea which is jumping.  The expectation is that the physics engine will take the timeD and use it to calculate
  1. The position of the pea after traveling for timeD, bouncing off things, being affected by gravity etc.
  1. The surfaces that have been hit by the pea in this time chunk
**Output**
  * The pea object reference should have its internal state updated by the Physics engine
  * If surfaces were hit then two things need to be notified (preferably through a listener/event model).
    1. The pea's score manager
    1. The surfaces bounce reaction handler
  * If the pea has finished its fall, the pea will need to know to change its movement mode, and the score will need to be updated with the peas score.  The pea might also have been killed and the death handler will need to be notified, preferably through a listener/event model).

# Issues #

## Unscored Jump ##
The game will at some stage require some physics simulated jumps to go unscored (eg, level load, peas getting trapped, peas falling off removed blocks).
How does this impact the physics system interface, how should it be implemented?

# Third Party Physics #
Lately I've been investigating third party physics libraries, and have had a crack at PyOde