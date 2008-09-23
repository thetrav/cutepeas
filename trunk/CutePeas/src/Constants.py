import Coordinates

SCREEN_WIDTH = 800
SCREEN_WIDTH_ODE = Coordinates.pixelsToOde(SCREEN_WIDTH) 
SCREEN_HEIGHT = 600
SCREEN_HEIGHT_ODE = Coordinates.pixelsToOde(SCREEN_HEIGHT)


SCROLL_LINE_HEIGHT = 30
UP_SCROLL_LINE = SCROLL_LINE_HEIGHT
DOWN_SCROLL_LINE = SCREEN_HEIGHT - SCROLL_LINE_HEIGHT
Y_SCROLL_SPEED_ODE = Coordinates.pixelsToOde(1)

FLOOR_POS = SCREEN_HEIGHT - 50
FLOOR_POS_ODE = Coordinates.pixelsToOde(FLOOR_POS)

MAX_FPS = 72

BLOCKS_WIDE = 9
BLOCKS_HIGH = 9

BLOCK_WIDTH = 71
BLOCK_WIDTH_ODE = Coordinates.pixelsToOde(BLOCK_WIDTH)
BLOCK_HEIGHT = 50
BLOCK_HEIGHT_ODE = Coordinates.pixelsToOde(BLOCK_HEIGHT)
BLOCK_HEIGHT_REAL = 61
BLOCK_Y_OVERLAP = BLOCK_HEIGHT_REAL - BLOCK_HEIGHT
BLOCK_Y_OVERLAP_ODE = Coordinates.pixelsToOde(BLOCK_Y_OVERLAP)

X_OFFSET = 50
X_OFFSET_ODE = Coordinates.pixelsToOde(X_OFFSET)
X_BORDER = X_OFFSET + BLOCKS_WIDE * BLOCK_WIDTH

Y_OFFSET = 90
Y_OFFSET_ODE = Coordinates.pixelsToOde(Y_OFFSET)
Y_BORDER = Y_OFFSET + BLOCKS_HIGH * BLOCK_HEIGHT

PEA_RADIUS = 18

#mouse event constants
LEFT = 1
RIGHT = 3
WHEEL_UP=4
WHEEL_DOWN=5

# cloud constants
MIN_TIME = 1000
MAX_TIME = 4000
WIND_SPEED = 0.00001


#Event IDs

EVENT_NODE_GRAPH_UPDATED = "EVENT_NODE_GRAPH_UPDATED"

X = 0
Y = 1
Z = 2

DRAW_HIT_BOXES = False
DRAW_NODES = True
DRAW_PATH = False

def debug(words):
    output("DEBUG: ", words)

def error(words):
    output("ERROR: ", words)
    
def output(start, words):
    for word in words:
        start += str(word)
    print start
    
def returnFalseFunction():
    return False

def returnTrueFunction():
    return True
