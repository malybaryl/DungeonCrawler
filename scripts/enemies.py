import pygame
import scripts.constants
import math
import random
from scripts.load import loadImages

class Orc():
    def __init__(self, x, y, health):
        self.rect = pygame.Rect(0,0,16,26)
        self.rect.center = (x,y)
        self.animation_index = [["run",0],["hit",0]]
        self.assets = {
        "orc_run": loadImages("char/orc/run"),
        "orc_hit": loadImages("char/orc/hit")
        }
        self.image_to_show = self.assets["orc_run"][math.floor(self.animation_index[0][1])]
        self.health = health
        self.alive = True
        self.randgold = random.randint(0,100)
        self.randpotion = random.randint(0,100)
        self.last_hit = pygame.time.get_ticks()
        self.is_fliped = False
        self.dx = 0
        self.dy = 0

    def move(self):
        self.rect.x += self.dx
        self.rect.y += self.dy
        

    def update(self, player):
        # reset values
        gold = False
        health_potion = False
        self.alive = True
        # check if mob has died
        if self.health <= 0:
            self.health = 0
            self.alive = False
        # handle animation
        # update flip direction
        if self.dx > 0:
            self.is_fliped = False
        if self.dx < 0:
            self.is_fliped = True
        # walk right
        if not self.is_fliped:
            self.image_to_show = self.assets["orc_run"][math.floor(self.animation_index[0][1])]
            self.animation_index[0][1] += 0.1
            if self.animation_index[0][1] >= 5:
                self.animation_index[0][1] = 0
        # attact right
        if self.rect.colliderect(player.rect) and not self.is_fliped:
            self.image_to_show = self.assets["orc_hit"][math.floor(self.animation_index[1][1])]
            self.animation_index[1][1] += 0.1
            if self.animation_index[1][1] >= 5:
                self.animation_index[1][1] = 0
        # walk left
        if  self.is_fliped:
            self.image_to_show = pygame.transform.flip(self.assets["orc_run"][math.floor(self.animation_index[0][1])],True,False)
            self.animation_index[0][1] += 0.1
            if self.animation_index[0][1] >= 5:
                self.animation_index[0][1] = 0
        # attact left
        if self.rect.colliderect(player.rect) and self.is_fliped:
            self.image_to_show = pygame.transform.flip(self.assets["orc_hit"][math.floor(self.animation_index[1][1])],True,False)
            self.animation_index[1][1] += 0.1
            if self.animation_index[1][1] >= 5:
                self.animation_index[1][1] = 0
        # when not alive
        if not self.alive:
            if self.randgold <= 50:
                gold = True
            if self.randpotion <= 10:
                health_potion = True
            self.alive = False
        return gold, health_potion, self.alive
    
    def hit_player(self, damage, player):
        counter = 1000
        if self.rect.colliderect(player.rect) and (pygame.time.get_ticks()-self.last_hit) >= counter:
            player.health -= damage
            self.last_hit = pygame.time.get_ticks()
            
             
    def draw(self, surface):
            surface.blit(self.image_to_show, (self.rect.center[0]-16,self.rect.center[1]-20))
            pygame.draw.rect(surface, scripts.constants.RED, self.rect, 1)
        