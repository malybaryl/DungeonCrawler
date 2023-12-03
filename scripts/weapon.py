from typing import Any
import pygame
import scripts.constants
import math
from scripts.load import loadImages
import random

class Bow:
    def __init__(self,type_of_bow,x,y):
        self.assets = {
            "bow": loadImages(f"wepons/bow/{type_of_bow}")
        }
        self.type_of_bow = type_of_bow
        self.original_image = self.assets["bow"][0]
        self.angle = 0
        self.image_to_show= pygame.transform.rotate(self.original_image, self.angle)
        self.rect = pygame.Rect(0,0,32,32)
        self.rect.center = (x,y)
        self.fired = False
        self.last_shot = pygame.time.get_ticks()
    
    def update(self,player):
        self.rect.center = player.rect.center
        shot_cooldown = 500
        arrow = None
        pos = pygame.mouse.get_pos()
        pos_x = pos[0]/ scripts.constants.SCALE_WIDTH
        pos_y = pos[1]/ scripts.constants.SCALE_HEIGHT
        x_dist = (pos_x - self.rect.centerx) 
        y_dist = -(pos_y - self.rect.centery)  # negative because y coordinates increase down the screen
        self.angle = math.degrees(math.atan2(y_dist,x_dist)) 
       
        # get mouseclick
        if pygame.mouse.get_pressed()[0] and not self.fired and (pygame.time.get_ticks()- self.last_shot) >= shot_cooldown:
            arrow = Arrow("classicArrow",self)
            self.fired = True
            self.last_shot = pygame.time.get_ticks()

        # reset mouseclick
        if pygame.mouse.get_pressed()[0] == False:
            self.fired = False
        
        return arrow

    def draw(self, surface):
        self.image_to_show= pygame.transform.rotate(self.original_image, self.angle)
        surface.blit(self.image_to_show, (self.rect.center[0]-int(self.image_to_show.get_width()/2),self.rect.center[1]-int(self.image_to_show.get_height()/2)))
        #pygame.draw.rect(surface, scripts.constants.RED, self.rect, 1)

class Arrow(pygame.sprite.Sprite):
    def __init__(self,type_of_arrow, bow):
        pygame.sprite.Sprite.__init__(self)
        self.x_cord = bow.rect.center[0]
        self.y_cord = bow.rect.center[1]
        self.angle = -bow.angle
        self.assets = {
            "arrow": loadImages(f"wepons/arrow/{type_of_arrow}")
        }
        self.original_image = self.assets["arrow"][0]
        self.image_to_show = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = pygame.Rect(0,0,16,16)
        self.rect.center = (self.x_cord,self.y_cord)
        #calculate the horizontal and vertical speeds based on the angle
        self.dx = math.cos(math.radians(self.angle)) * scripts.constants.ARROW_SPEED
        self.dy = math.sin(math.radians(self.angle)) * scripts.constants.ARROW_SPEED

    def update(self, enemy_list):
        # reset variables
        damage = 0
        damage_pos = None
        #reposition based on speed
        self.rect.x += self.dx
        self.rect.y += self.dy
        
        # check if arrow has gone off screen
        if self.rect.right < 0 or self.rect.left > scripts.constants.DISPLAY_WIDTH or self.rect.bottom < 0 or self.rect.top > scripts.constants.DISPLAY_HEIGHT:
            self.kill()

        # check collision between arrow and enemies
        for enemy in enemy_list:
            if enemy.rect.colliderect(self.rect) and enemy.alive:
                damage = 10 + random.randint(-5,5)
                damage_pos = enemy.rect
                enemy.health -= damage
                self.kill()
                break
        return damage, damage_pos

    def draw(self, surface):
        surface.blit(pygame.transform.flip(self.image_to_show,True,False), (self.rect.center[0]-int(self.image_to_show.get_width()/2),self.rect.center[1]-int(self.image_to_show.get_height()/2)))
        pygame.draw.rect(surface, scripts.constants.RED, self.rect, 1)