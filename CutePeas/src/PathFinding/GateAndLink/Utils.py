from Constants import *
import math

def snapToPos(odePos):
    return [snap(odePos[0], X_OFFSET_ODE, NODE_X_GAP_ODE), snap(odePos[1], Y_OFFSET_ODE, NODE_Y_GAP_ODE)]

def snap(odePos, offset, gap):
    return math.floor((odePos - offset) / gap) * gap + offset

def toScreenCoords(x):
    return x*BLOCK_WIDTH_ODE + X_OFFSET_ODE

