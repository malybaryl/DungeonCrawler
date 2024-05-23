import pygame
import scripts.constants
from scripts.load import loadImage, loadImages
import math

class Item(pygame.sprite.Sprite):
    def __init__(self, x, y, item_type):
        pygame.sprite.Sprite.__init__(self)
        self.assets ={
            "coin": loadImages("coin"),
            "health_potion": pygame.transform.scale(loadImage("potion/0.png"),(16,16)),
            'pick_up_coin_sound': pygame.mixer.Sound("assets/audio/coin_pick.wav"),
            'pick_up_potion_sound': pygame.mixer.Sound("assets/audio/potion_pick.wav")
        }
        self.assets['pick_up_coin_sound'].set_volume(scripts.constants.FX_VOLUME)
        self.assets['pick_up_potion_sound'].set_volume(scripts.constants.FX_VOLUME)
        self.item_type = item_type # coin, health_potion
        self.index = {
            "coin": 0
        }
        self.rect = pygame.Rect(0,0,16,16)
        self.rect.center = (x,y)

    def update(self, player, screen_scroll) :
        # reposition based on screen scrool
        self.rect.x += screen_scroll[0]
        self.rect.y += screen_scroll[1]

        # check if item has been colleted
        if self.item_type == "health_potion":
            if self.rect.colliderect(player.rect):
                if player.health < player.health_max:
                    if player.health >= player.health_max//2:
                        player.new_health = player.health_max
                    else:
                        player.new_health += player.health_max//2
                    player.player_was_heal = True
                    self.assets['pick_up_potion_sound'].play()
                    self.kill()
        if self.item_type == "coin":
            if self.rect.colliderect(player.rect):
                player.gold += 1
                self.assets['pick_up_coin_sound'].play()
                self.kill()

    def draw(self, display):
        if self.item_type == "health_potion": 
            display.blit(self.assets[self.item_type],(self.rect.center[0]-8,self.rect.center[1]-8))
            if scripts.constants.SHOW_HITBOX:
                pygame.draw.rect(display, scripts.constants.RED, self.rect, 1)
        elif self.item_type == "coin":
            display.blit(self.assets[self.item_type][math.floor(self.index[self.item_type])],(self.rect.center[0]-16,self.rect.center[1]-16))
            self.index[self.item_type] += 0.1
            if self.index[self.item_type] > 6:
                self.index[self.item_type] = 0
            if scripts.constants.SHOW_HITBOX:
                pygame.draw.rect(display, scripts.constants.RED, self.rect, 1)