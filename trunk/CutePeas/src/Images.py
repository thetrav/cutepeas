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
    
def loadImages():
    imageStrings = ("Background", 
              "Gold-Ball", 
              "Happy-Points", 
              "Tool-StandardBlock", 
              "Tool-Background", 
              "Tool-Selected", 
              "Tool-GelBlock", 
              "Tool-Delete", 
              "Tool-GelBlock", 
              "Tool-StandardBlock", 
              "Tool-LeftRamp", 
              "Tool-RightRamp", 
              "Tool-Spring",
              "Pointer-Standard",
              "Plate")
    for image in imageStrings:
        cacheImage(images, image)
    