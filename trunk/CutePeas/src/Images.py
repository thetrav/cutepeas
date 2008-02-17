import pygame

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
    
def loadImages(cache):
    images = ("Background",
              "Gold-Ball",
              "Happy-Points",
              "Tool-StandardBlock",
              "Tool-Background")
    for image in images:
        cacheImage(cache, image)
    