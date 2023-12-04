import pygame
import scripts.constants
import math
import random
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
        self.randgold = random.randint(0,100)
        self.randpotion = random.randint(0,100)

    def move(self):
        self.rect.x += 0

    def update(self):
        # reset values
        gold = False
        health_potion = False
        self.alive = True
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
        if not self.alive:
            if self.randgold <= 50:
                gold = True
            if self.randpotion <= 10:
                health_potion = True
            self.alive = False
        return gold, health_potion, self.alive
    
    def hit_player(self, damage, player):
        if self.rect.colliderect(player.rect):
            player.health -= damage
             
    def draw(self, surface):
            surface.blit(self.image_to_show, (self.rect.center[0]-16,self.rect.center[1]-20))
            pygame.draw.rect(surface, scripts.constants.RED, self.rect, 1)
        