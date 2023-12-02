import pygame
import scripts.constants
import math
from scripts.load import loadImages

class Orc():
    def __init__(self, x, y, health):
        self.rect = pygame.Rect(0,0,16,26)
        self.rect.center = (x,y)
        self.image_to_show = 0
        self.animation_index = [["run",0]]
        self.assets = {
        "orc_run": loadImages("char/orc/run")
        }
        self.health = health
        self.alive = True

    def move(self):
        self.rect.x += 0

    def update(self):
        # check if mob has died
        if self.health <= 0:
            self.health = 0
            self.alive = False
        # handle animation
        # update image   
        self.image_to_show = self.assets["orc_run"][math.floor(self.animation_index[0][1])]
        self.animation_index[0][1] += 0.1
        if self.animation_index[0][1] >= 5:
            self.animation_index[0][1] = 0
       
        

    def draw(self, surface):
            surface.blit(self.image_to_show, (self.rect.center[0]-16,self.rect.center[1]-20))
            pygame.draw.rect(surface, scripts.constants.RED, self.rect, 1)
        