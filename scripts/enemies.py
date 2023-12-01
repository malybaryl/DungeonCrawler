import pygame
import scripts.constants
import math
from scripts.load import loadImages

class Orc():
    def __init__(self, x, y):
        self.rect = pygame.Rect(0,0,16,26)
        self.rect.center = (x,y)
        self.image_to_show = 0
        self.animation_index = [["run",0]]
        self.assets = {
        "orc_run": loadImages("char/orc/run")
        }

    def move(self):
        self.rect.x += 1

    def update(self):
        # handle animation
        # update image   
        self.image_to_show = self.assets["orc_run"][math.floor(self.animation_index[0][1])]
        self.animation_index[0][1] += 0.1
        if self.animation_index[0][1] >= 5:
            self.animation_index[0][1] = 0
        pass

    def draw(self, surface):
            surface.blit(self.image_to_show, (self.rect.center[0]-16,self.rect.center[1]-20))
            pygame.draw.rect(surface, scripts.constants.RED, self.rect, 1)
        