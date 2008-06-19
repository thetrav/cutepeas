SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

FLOOR_POS = SCREEN_HEIGHT - 50

#scenery constants
BLOCK_WIDTH = 71
BLOCK_HEIGHT = 50
BLOCK_HEIGHT_REAL = 61
BLOCK_Y_OVERLAP = BLOCK_HEIGHT_REAL - BLOCK_HEIGHT


MAX_FPS = 72

BLOCKS_WIDE = 9
BLOCKS_HIGH = 9

X_OFFSET = 50
X_BORDER = X_OFFSET + BLOCKS_WIDE * BLOCK_WIDTH

Y_OFFSET = 90
Y_BORDER = Y_OFFSET + BLOCKS_HIGH * BLOCK_HEIGHT

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

PEA_RADIUS = 18
DRAW_HIT_BOXES = False
DRAW_NODES = False
DRAW_PATH = False

def debug(words):
    output("DEBUG: ", words)

def error(words):
    output("ERROR: ", words)
    
def output(start, words):
    for word in words:
        start += str(word)
    print start