import pygame, sys
import Animation, TitleScreen
from Constants import *
from pygame.locals import *
import UserInterface.UserInterface
import UserInterface.Scroll
import Images

class Game:
    def __init__(self):
        self.window = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
        pygame.display.set_caption('Cute Peas')
        
        self.screen = pygame.display.get_surface()
        Images.loadImages()
    
    def handleInput(self, events):
        for event in events:
            if event.type == QUIT:
                print 'Goodbye!'
                sys.exit(0)
            else:
                self.userInterface.handleEvent(event)
    
    def render(self, screen):
        self.level.render(screen)
        pygame.display.flip()
        
    def transition(self, newLevel):
        self.level.dispose()
        self.level = newLevel
        UserInterface.Scroll.globalViewPort.offset = [0,0]
        
    def main(self):
        self.userInterface = UserInterface.UserInterface.UserInterface()
        Animation.animations.append(UserInterface.Scroll.globalViewPort)
        self.level = TitleScreen.TitleScreen(self.userInterface, self)
        clock = pygame.time.Clock()
        clock.tick() #initialise timer
        timeToRun = 250
        while True:
            self.handleInput(pygame.event.get())
            if timeToRun > 0:
                time = clock.get_time()
                for animation in Animation.animations:
                    animation.update(time)
                #timeToRun -= time
            self.render(self.screen)
            clock.tick(MAX_FPS)
        
Game().main()