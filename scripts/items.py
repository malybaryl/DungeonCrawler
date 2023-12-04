from typing import Any
import pygame
import scripts.constants
from scripts.load import loadImage

class Item(pygame.sprite.Sprite):
    def __init__(self, x, y, item_type):
        pygame.sprite.Sprite.__init__(self)
        self.assets ={
            "coin": pygame.transform.scale(loadImage("coin/0.png"),(16,16)),
            "health_potion": pygame.transform.scale(loadImage("potion/0.png"),(16,16))
        }
        self.item_type = item_type # coin, health_potion
        self.rect = pygame.Rect(0,0,16,16)
        self.rect.center = (x,y)

    def update(self, player) :
        if self.item_type == "health_potion":
            if self.rect.colliderect(player.rect):
                player.health = 100
                self.kill()
        if self.item_type == "coin":
            if self.rect.colliderect(player.rect):
                player.gold += 1
                self.kill()

    def draw(self, display):
        display.blit(self.assets[self.item_type],(self.rect.center[0]-8,self.rect.center[1]-8))
        pygame.draw.rect(display, scripts.constants.RED, self.rect, 1)