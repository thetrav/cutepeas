from Constants import *
pixels_in_an_ode_unit = 25

def odeToPixels(ode_units):
    return int(ode_units * pixels_in_an_ode_unit)

def pixelsToOde(pixels):
    return float(pixels) / float(pixels_in_an_ode_unit)

def pixelPosToOdePos(pos):
    return (pixelsToOde(pos[X]), pixelsToOde(pos[Y]), 0)

def odePosToPixelPos(odePos):
    return (odeToPixels(odePos[X]), odeToPixels(odePos[Y]))

def pixelsToBoxIndex(pos, offset, gap):
    return int((pos - offset)/gap)

def boxIndexToPixels(pos, offset, gap):
    return pos * gap + offset

def pixelPosToBoxIndex(pos, slots):
    i = pixelsToBoxIndex(pos[X], X_OFFSET, BLOCK_WIDTH)
    j = pixelsToBoxIndex(pos[Y], Y_OFFSET, BLOCK_HEIGHT)
    
    #This is an old work around for a selection bug.  I can't figure it out right now so it was probably the wrong solution, or not commented well enough
    # check for overlap
    #distanceFromTop = pos[Y] - boxIndexToPixels(j, Y_OFFSET, BLOCK_HEIGHT)
    #if distanceFromTop < BLOCK_Y_OVERLAP  and j > 0 and slots[i][j-1].block:
    #    j = j-1
    return (i,j)

def boxIndexToPixelPos(x, y):
    i = boxIndexToPixels(x, X_OFFSET, BLOCK_WIDTH)
    j = boxIndexToPixels(y, Y_OFFSET, BLOCK_HEIGHT)
    return (i,j)

def pixelsToNearestNodePixels(pos, offset, gap):
    return int(math.floor((pos - offset) / gap) * gap + offset)

def pixelPosToNearestNodePixels(pos):
    return (pixelsToNearestNodePixels(pos[0], X_OFFSET, NODE_X_GAP), pixelsToNearestNodePixels(pos[1], Y_OFFSET, NODE_Y_GAP))
