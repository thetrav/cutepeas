# Introduction #

The current physics implementation OdePhysics, throws out a collision event every time there is a collision, at first glance it would appear that we can simply take every collision and treat it as a new bounce for score.

If life were that simple I'd be finished with this project a lot quicker.  Unfortunately, using that technique ends up with over 200 bounces for a manouver that I estimate as being worth 3 scored bounces.

# Details #

There are a two separate issues that are causing this behaviour
  1. low velocity collisions at the end of the jump
  1. multiple collisions thrown against the same object on a single bounce


I've ran some statistical analysis of a standard physics jump and produced the following graph.
the xpos and ypos have been adjusted to lower the change in the Y axis, as the velocities are quite low values.
I'm considering normalising the positional values, as all we really need to look at are the change patterns rather than specific values.
http://travis.dixon.net.au/wp-content/uploads/2008/06/bounce-graph.PNG

# Potential solutions #

## one bounce per block ##
Personally I feel this one is a bit of a heavy handed approach, but it does provide a simple solution to the problem and will therefore probably be implemented first just so I can move on with getting the score system happening.

It's pretty obvious how it works, each pea has a set of blocks that is cleared on each jump, and then blocks can only be added once.

### advantages ###
  * Simple
### disadvantages ###
  * Removes a lot of potential for users to create multi bounce patterns
  * Removes the ability to add depth to the scoring mechanism by adding multipliers when one block is hit numerous times
  * Lowers overall score achievable by users
  * Users may expect more score for more bounces and feel a little cheated by the one bounce rule

## statistical analysis of past velocity and positions ##
The gold plated approach would be to work out local minima/maxima within a threshold for determining which collisions count as bounces and which don't.
Obviously that would be a substantial overhead both in dev time and cpu cycles, but given the simplicity of the game I think the CPU shouldn't be a real problem.

### advantages ###
  * Gives maximum control over determining scored bounces
  * A reasonably complex problem that will be fun to implement (for people who like graphs and medium to large data sets)

### disadvantages ###
  * Long time to develop
  * Possible performance impact
  * May not yield a satisfactory solution when fully investigated
  * Difficult to handle bugs

## Obvious solution ##
This is just here for completeness, but I get the feeling that there's an obvious solution that I just haven't figured out yet that makes the whole problem just go away.