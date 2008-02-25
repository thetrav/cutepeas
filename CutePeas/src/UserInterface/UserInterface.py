import pygame, sys

from pygame.locals import *
from Button import Button
from Images import images
from Cursor import Cursor
from Tool import *
from Scenery import *
from Pea import *
import Text, Score, Animation, Timer, Particles.Particles


LEFT = 1
RIGHT = 3
WHEEL_UP=4
WHEEL_DOWN=5

def newButton(image, yPos, tool):
    return Button(images["Tool-"+image], images["Tool-"+image], images["Tool-Selected"], tool, 725, yPos, 47, 47)

class UserInterface:
    def __init__(self):
        self.selectedButton = None
#        yStart = 15
#        spacing = 50
        
#        self.buttons = (
#                        newButton("Delete", yStart, DeleteTool()),
#                        newButton("Gel", yStart + spacing, GelBlockTool()),
#                        newButton("Normal", yStart + spacing*2, NormalBlockTool()),
#                        newButton("LeftRamp", yStart + spacing*3, LeftRampTool()),
#                        newButton("RightRamp", yStart + spacing*4, RightRampTool()),
#                        newButton("Spring", yStart + spacing*5, SpringTool())
#                        )
        
#        for button in self.buttons:
#            button.addListener(self)
        
#        self.scene = Scenery()
        
        self.buttons = []
        
        self.activeWidgets = []
        self.passiveWidgets = []
        self.scene = None
        self.cursor = Cursor(images["Pointer-Standard"])
        
        
        #self.score = Score.Score()
        #Animation.animations.append(self.score)
        
        #self.timer = Timer.Timer()
        #Animation.animations.append(self.timer)

    def addButton(self, button):
        self.buttons.append(button)
        button.addListener(self)
        
    def setScene(self, scene):
        self.scene = scene
        self.cursor.setScene(scene)
        
    def render(self, screen):
        if self.scene:
            self.scene.render(screen)
        self.renderTools(screen)
        self.passiveWidget
        #self.score.render(screen, (300,10))
        #self.timer.render(screen, (600,10))
        self.cursor.render(screen)
        
    def renderTools(self, screen):
        screen.blit(images["Tool-Background"], (720, 10))
        for button in self.buttons:
            button.render(screen)
    
    def handleEvent(self, event):
        if event.type == MOUSEMOTION:
            for button in self.buttons:
                button.mouseMotion(event)
            self.cursor.mouseMotion(event)
        elif event.type == MOUSEBUTTONDOWN:
            if event.button == LEFT:
                for button in self.buttons:
                    button.mouseDown(event)
                self.cursor.toolUsed()
            elif event.button == RIGHT and self.selectedButton:
                self.deSelectEvent()
            elif event.button == WHEEL_UP:
                self.scrollButton(-1)
            elif event.button == WHEEL_DOWN:
                self.scrollButton(+1)
        elif event.type == MOUSEBUTTONUP:
            for button in self.buttons:
                button.mouseUp(event)
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                raise "quit"
                
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
    
    def scrollButton(self, direction):
        buttons = self.buttons
        buttonCount = len(buttons)
        for x in xrange(buttonCount):
            if self.selectedButton == None or buttons[x] == self.selectedButton:
                self.deSelectEvent()
                buttonInd = x + direction
                if buttonInd < 0:
                    buttonInd = buttonCount-1
                elif buttonInd == buttonCount:
                    buttonInd = 0
                buttons[buttonInd].fireEvent()
                return