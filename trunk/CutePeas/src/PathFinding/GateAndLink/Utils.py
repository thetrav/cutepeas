from Constants import *
import math

def snapToPos(pos):
    return [snap(pos[0], X_OFFSET, NODE_X_GAP), snap(pos[1], Y_OFFSET, NODE_Y_GAP)]

def snap(pos, offset, gap):
    return math.floor((pos - offset) / gap) * gap + offset

def toScreenCoords(x):
    return x*BLOCK_WIDTH + X_OFFSET

