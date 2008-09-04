SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

UP_SCROLL_LINE = 10
DOWN_SCROLL_LINE = SCREEN_HEIGHT - 10
Y_SCROLL_SPEED = 1

FLOOR_POS = SCREEN_HEIGHT - 50

MAX_FPS = 72

BLOCKS_WIDE = 9
BLOCKS_HIGH = 9

BLOCK_WIDTH = 71
BLOCK_HEIGHT = 50
BLOCK_HEIGHT_REAL = 61
BLOCK_Y_OVERLAP = BLOCK_HEIGHT_REAL - BLOCK_HEIGHT

X_OFFSET = 50
X_BORDER = X_OFFSET + BLOCKS_WIDE * BLOCK_WIDTH

Y_OFFSET = 90
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
    
def returnFalseFunction():
    return False

def returnTrueFunction():
    return True
