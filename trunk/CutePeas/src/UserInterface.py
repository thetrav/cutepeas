import pygame, sys

from pygame.locals import *
from Button import Button
from Images import images

class UserInterface:
    def __init__(self):
        self.button = Button(images["Tool-StandardBlock"], images["Tool-StandardBlock"], 725, 15, 47, 47)
    
    def render(self, screen):
        screen.blit(images["Tool-Background"], (720, 10))
        self.button.render(screen)
    
    def handleEvent(self, event):
        if event.type == MOUSEMOTION:
            self.button.mouseMotion(event)
        elif event.type == MOUSEBUTTONDOWN:
            self.button.mouseDown(event)
        elif event.type == MOUSEBUTTONUP:
            self.button.mouseUp(event)