import pygame, sys

from pygame.locals import *
from Button import Button
from Images import images
from Cursor import Cursor
from Tool import *
from Scenery import *
from Pea import *

LEFT = 1
RIGHT = 3

def newButton(image, yPos, tool):
    return Button(images["Tool-"+image], images["Tool-"+image], images["Tool-Selected"], tool, 725, yPos, 47, 47)

class UserInterface:
    def __init__(self, animations):
        self.selectedButton = None
        yStart = 15
        spacing = 50
        
        self.buttons = (
                        newButton("Delete", yStart, DeleteTool()),
                        newButton("GelBlock", yStart + spacing, GelBlockTool(animations)),
                        newButton("StandardBlock", yStart + spacing*2, NormalBlockTool(animations)),
                        newButton("LeftRamp", yStart + spacing*3, LeftRampTool(animations)),
                        newButton("RightRamp", yStart + spacing*4, RightRampTool(animations)),
                        newButton("Spring", yStart + spacing*5, SpringTool(animations))
                        )
        
        for button in self.buttons:
            button.addListener(self)
        
        self.scene = Scenery()
        
        self.cursor = Cursor(images["Pointer-Standard"], self.scene)
        self.pea = Pea(images["Pea-Standard"])
        
    def render(self, screen):
        self.scene.render(screen)
        screen.blit(images["Tool-Background"], (720, 10))
        for button in self.buttons:
            button.render(screen)
        self.cursor.render(screen)
        self.pea.render(screen)
    
    def handleEvent(self, event):
        if event.type == MOUSEMOTION:
            for button in self.buttons:
                button.mouseMotion(event)
            self.cursor.mouseMotion(event)
        elif event.type == MOUSEBUTTONDOWN:
            if event.button == LEFT:
                for button in self.buttons:
                    button.mouseDown(event)
                self.cursor.toolUsed(self.scene)
            elif event.button == RIGHT and self.selectedButton:
                self.deSelectEvent()
        elif event.type == MOUSEBUTTONUP:
            for button in self.buttons:
                button.mouseUp(event)
                
    def buttonFired(self, button):
        self.deSelectEvent()
        button.select()
        self.selectedButton = button
        self.cursor.toolChanged(button.tool)
        
    def deSelectEvent(self):
        if self.selectedButton:
            self.selectedButton.deSelect()
            self.selectedButton = None
            self.cursor.toolCleared()
            self.scene.toolCleared()
            