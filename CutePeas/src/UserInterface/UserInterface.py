import pygame, sys
from pygame.locals import *

import Animation
import Button
import Constants
import Cursor
import Images
import Score
import Text
import Timer
import Tool
from Constants import *


class UserInterface:
    def __init__(self):
        self.activeWidgets = []
        self.passiveWidgets = []
        self.scene = None
        self.cursor = Cursor.Cursor(Images.images["Pointer-Standard"])

    def addButton(self, button):
        self.buttons.append(button)
        button.addListener(self)
        
    def addActiveWidget(self, widget):
        self.activeWidgets.append(widget)
        
    def removeActiveWidget(self, widget):
        self.activeWidgets.remove(widget)
        
    def addPassiveWidget(self, widget):
        self.passiveWidgets.append(widget)
        
    def removePassiveWidget(self, widget):
        self.passiveWidgets.remove(widget)
        
    def setScene(self, scene):
        self.scene = scene
        self.cursor.setScene(scene)
        
    def render(self, screen):
        if self.scene:
            self.scene.render(screen)
        for widget in self.activeWidgets:
            widget.render(screen)
        for widget in self.passiveWidgets:
            widget.render(screen)
        self.cursor.render(screen)
    
    def handleEvent(self, event):
        if event.type == MOUSEMOTION:
            for widget in self.activeWidgets:
                widget.mouseMotion(event)
            self.cursor.mouseMotion(event)
        elif event.type == MOUSEBUTTONDOWN:
            if event.button == LEFT:
                noWidgetFired = True
                for widget in self.activeWidgets:
                    print 'calling mouseDown'
                    if widget.mouseDown(event):
                        print 'button down'
                        noWidgetFired = False
                if noWidgetFired:
                    self.cursor.toolUsed()
            elif event.button == RIGHT:
                self.deSelectEvent()
                self.cursor.toolCleared()
            elif event.button == WHEEL_UP:
                self.scrollButton(-1)
            elif event.button == WHEEL_DOWN:
                self.scrollButton(+1)
        elif event.type == MOUSEBUTTONUP:
            for widget in self.activeWidgets:
                widget.mouseUp(event)
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                raise "quit"
            elif event.key == K_p:
                Constants.DRAW_PATH = not Constants.DRAW_PATH
            elif event.key == K_n:
                Constants.DRAW_NODES = not Constants.DRAW_NODES
            elif event.key == K_h:
                Constants.DRAW_HIT_BOXES = not Constants.DRAW_HIT_BOXES
                
    def buttonFired(self, button):
        self.deSelectEvent()
        button.select()
        self.cursor.toolChanged(button.tool)
        
    def deSelectEvent(self):
        for widget in self.activeWidgets:
            widget.deSelectEvent()
        self.cursor.toolCleared()
        
    def scrollButton(self, direction):
        for widget in self.activeWidgets:
            widget.scrollButton(direction)