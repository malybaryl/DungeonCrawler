import pygame
import scripts.constants
import math
from scripts.load import loadImage, loadImages

class Character():
    def __init__(self, x, y):
        self.rect = pygame.Rect(0,0,16,32)
        self.rect.center = (x,y)
        self.image_to_show = 0
        self.idle_index = 0
        self.assets = {
        "player_idle": loadImages("char/player1/idle")
        }

    def move(self, dx, dy):
        # control diagonal speed
        if dx != 0 and dy != 0:
            dx = dx * (math.sqrt(2)/2)
            dy = dy * (math.sqrt(2)/2)
        self.rect.x += dx
        self.rect.y += dy

    def update(self, flip):
        # handle animation
        # update image
        if not flip:
            self.image_to_show = self.assets["player_idle"][math.floor(self.idle_index)]
            self.idle_index += 0.1
            if self.idle_index >= 4:
                self.idle_index = 0
        if flip:
            self.image_to_show = pygame.transform.flip(self.assets["player_idle"][math.floor(self.idle_index)],True,False)
            self.idle_index += 0.1
            if self.idle_index >= 4:
                self.idle_index = 0


    def draw(self, surface):
            surface.blit(self.image_to_show, (self.rect.center[0]-16,self.rect.center[1]-16))
            pygame.draw.rect(surface, scripts.constants.RED, self.rect, 1)
        
        
        