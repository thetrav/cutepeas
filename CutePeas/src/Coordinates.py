import math
#These constants need to be duplicated so that Constants can import Coordinates
X = 0
Y = 1
pixels_in_an_ode_unit = 25

# straight coordinate space transforms

def odeToPixels(ode_units):
    return int(ode_units * pixels_in_an_ode_unit)

def pixelsToOde(pixels):
    return float(pixels) / float(pixels_in_an_ode_unit)

def pixelPosToOdePos(pos):
    return (pixelsToOde(pos[X]), pixelsToOde(pos[Y]), 0)

def odePosToPixelPos(odePos):
    return (odeToPixels(odePos[X]), odeToPixels(odePos[Y]))

#constants that rely on coordinate transforms
X_OFFSET = 50
X_OFFSET_ODE = pixelsToOde(X_OFFSET)
Y_OFFSET = 90
Y_OFFSET_ODE = pixelsToOde(Y_OFFSET)
BLOCK_WIDTH = 71
BLOCK_WIDTH_ODE = pixelsToOde(BLOCK_WIDTH)
BLOCK_HEIGHT = 50
BLOCK_HEIGHT_ODE = pixelsToOde(BLOCK_HEIGHT)
SCREEN_HEIGHT = 600

# snapping transforms

# to snap to a box coordinates, offset the measure, then divide by the gap discard remainder, 
# then go backwards, multiplying by gap and adding back the offset
def snapOdeToBox(measure, offset, gap):
    index = math.floor((measure - offset)/gap)
    return int(index) * gap + offset

def snapOdePosToBoxOdePos(odePos):
    i = snapOdeToBox(odePos[X], X_OFFSET_ODE, BLOCK_WIDTH_ODE)
    j = snapOdeToBox(odePos[Y], Y_OFFSET_ODE, BLOCK_HEIGHT_ODE)
    return (i,j,0)

# these transforms are used by the path finding code (usually to get a pea from the end of its jump and on to a node)
def pixelsToNearestNodePixels(pos, offset, gap):
    return int(math.floor((pos - offset) / gap) * gap + offset)

def pixelPosToNearestNodePixels(pos):
    return (pixelsToNearestNodePixels(pos[0], X_OFFSET, NODE_X_GAP), 
            pixelsToNearestNodePixels(pos[1], Y_OFFSET, NODE_Y_GAP))
