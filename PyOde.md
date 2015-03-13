# Introduction #
pyode is a set of python bindings for the Open Dynamics Engine ( http://www.ode.org )

# Implementation #
I've added a physics manager that uses pyode, there have been some interface changes to accommodate this:
  * add and remove surfaces have been replaced with add and remove blocks
  * add and remove pea has been added
  * peas and blocks have body and geom object respectively, they are ode aware
  * collisions will need to be handled with call backs.
  * the physics manager is responsible for moving all peas at once and has its own update method.  The peas retain their update method for game logic and non-physics animations


# Issues #
The python-pyode package available on Hardy Heron 64 bit does not appear to like triangle meshes very much (seg fault without any data).  We may be parting with my OS of choice for a while.
I've investigated some other physics libraries, but they all seem to have trouble supporting ubuntu as well, so I'm just going to stick with ODE, go to windows for dev and maybe come back to the problem when I've got a game that works.

TheBounceProblem