import pygame
import os.path

images = {}

# Not private, to allow [test] clients to modify the base dir relative to where they're at.
IMAGE_BASE_DIR = os.path.join(os.pardir, 'data', 'images')

def loadImage(name, colorkey=None):
    fullname = os.path.join(IMAGE_BASE_DIR, name + '.png')
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
    
def buttonImageSet(name, list):
    list.append("Button-"+name)
    list.append("Button-"+name+"-Hover")
    list.append("Button-"+name+"-Down")
    
def loadImages():
    imageStrings = ["Background",
                    "Logo",
                    "Gold-Ball", 
                    "Happy-Points",
                    "Flag-Pole",
                    "Flag-Good",
                    "Flag-Bad",
                    "Icon-Time",
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
    buttonImageSet("New-Game", imageStrings)
    buttonImageSet("Exit-Game", imageStrings)
    for image in imageStrings:
        cacheImage(images, image)
    