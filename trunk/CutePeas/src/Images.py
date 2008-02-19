import pygame

images = {}

def loadImage(name, colorkey=None):
    fullname = '../data/images/' + name + '.png'
    try:
        image = pygame.image.load(fullname)
    except pygame.error, message:
        print 'Cannot load image: ' + name
        raise SystemExit, message
    return image.convert_alpha()

def cacheImage(cache, name):
    cache[name] = loadImage(name)
    
def blockImageSet(blockName, list):
    list.append("Tool-"+blockName)
    list.append("Block-Place-"+blockName)
    list.append("Block-"+blockName) 
    
def loadImages():
    imageStrings = ["Background", 
              "Gold-Ball", 
              "Happy-Points",
              "Pea-Standard",
              "Tool-Background", 
              "Tool-Selected", 
              "Tool-Delete", 
              "Pointer-Standard",
              "Pointer-Delete",
              "Plate",
              "Cloud1",
              "Cloud2",
              "Cloud3",
              "1",
              "2",
              "3"]
    blockImageSet("Normal",imageStrings) 
    blockImageSet("Gel",imageStrings)
    blockImageSet("RightRamp",imageStrings)
    blockImageSet("LeftRamp",imageStrings)
    blockImageSet("Spring",imageStrings) 
    for image in imageStrings:
        cacheImage(images, image)
    