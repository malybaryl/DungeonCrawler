import pygame
import scripts.constants
import math
from scripts.load import loadImages

class Character():
    def __init__(self, x, y, health):
        self.rect = pygame.Rect(0,0,16,32)
        self.rect.center = (x,y)
        self.image_to_show = 0
        self.animation_index = [["idle",0], ["run",0]]
        self.assets = {
        "player_idle": loadImages("char/player1/idle"),
        "player_run": loadImages("char/player1/run")
        }
        self.health = health
        self.alive = True

    def move(self, dx, dy):
        # control diagonal speed
        if dx != 0 and dy != 0:
            dx = dx * (math.sqrt(2)/2)
            dy = dy * (math.sqrt(2)/2)
        self.rect.x += dx
        self.rect.y += dy

    def update(self, flip, moving):
        # handle animation
        # update image
        if not moving and not flip:
            self.image_to_show = self.assets["player_idle"][math.floor(self.animation_index[0][1])]
            self.animation_index[0][1] += 0.1
            if self.animation_index[0][1] >= 4:
                self.animation_index[0][1] = 0
        if not moving and flip:
            self.image_to_show = pygame.transform.flip(self.assets["player_idle"][math.floor(self.animation_index[0][1])],True,False)
            self.animation_index[0][1] += 0.1
            if self.animation_index[0][1] >= 4:
                self.animation_index[0][1] = 0
        if moving and flip:
            self.image_to_show = pygame.transform.flip(self.assets["player_run"][math.floor(self.animation_index[1][1])],True,False)
            self.animation_index[1][1] += 0.1
            if self.animation_index[1][1] >= 4:
                self.animation_index[1][1] = 0
        if moving and not flip:
            self.image_to_show = self.assets["player_run"][math.floor(self.animation_index[1][1])]
            self.animation_index[1][1] += 0.1
            if self.animation_index[1][1] >= 4:
                self.animation_index[1][1] = 0
        pass

    def draw(self, surface):
            surface.blit(self.image_to_show, (self.rect.center[0]-16,self.rect.center[1]-16))
            pygame.draw.rect(surface, scripts.constants.RED, self.rect, 1)
        
        
        