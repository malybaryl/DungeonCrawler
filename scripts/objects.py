import pygame
import scripts.constants
from random import choice 
from scripts.weapon import Bow

class Object:
    def __init__(self, type):
        self.type = type
        
class Chest(Object):
    def __init__(self, x, y, closed_chest_img, opened_chest_img):
        super().__init__(type= 'chest')
        self.assets={
            'closed_chest': closed_chest_img,
            'opened_chest': opened_chest_img,
            'e_key': pygame.image.load('assets/images/HUD/e_button/0.png')
        }
        self.image_to_show = self.assets['closed_chest']
        self.rect = pygame.Rect(x, y, 64, 64)
        self.rect.center = (x - 16,y)
        self.collider_rect = pygame.Rect(x,y,16,16)
        self.collider_rect.center = (x,y)
        self.closed = True
        self.not_draw = False
        self.delete = False
        self.time = pygame.time.get_ticks()
        self.show_e_button = False
    
    def update(self, screen_scroll, event_key_pressed, player):
        self.rect.x += screen_scroll[0]
        self.rect.y += screen_scroll[1]
        wepon = None
        
        if self.closed:
            self.image_to_show = self.assets['closed_chest']
        else:
            self.image_to_show = self.assets['opened_chest']
         
        if self.rect.colliderect(player.rect):    
            if event_key_pressed:
                if self.closed:
                    new_wepon = self.return_new_wepon()
                    x = self.rect.x + 16
                    y = self.rect.y + 16
                    wepon = Bow(x,y, 'bows', new_wepon, on_ground = True)
                    self.delete = True
                    self.time = pygame.time.get_ticks()
                self.closed = False
            if self.closed:
                self.show_e_button = True
            else:
                self.show_e_button = False
        else:
            self.show_e_button = False
        
        if self.delete:
            self.diseaper()
                
        if self.collider_rect.colliderect(player.rect):
            if self.collider_rect.top < player.rect.bottom < self.collider_rect.bottom:
                player.rect.bottom = self.collider_rect.top - 1
            elif self.collider_rect.bottom > player.rect.top > self.collider_rect.top:
                player.rect.top = self.rect.bottom + 1
            elif self.collider_rect.left < player.rect.right < self.collider_rect.right:
                player.rect.right = self.collider_rect.left - 1
            elif self.collider_rect.right > player.rect.left > self.collider_rect.left:
                player.rect.left = self.collider_rect.right + 1
                
        return wepon
                
    def return_new_wepon(self):
        wepon = choice(scripts.constants.BOWS)
        
        return wepon
    
    def diseaper(self):
        if pygame.time.get_ticks() - self.time >= 2000:
            self.not_draw = True
            
         
    def draw(self, surface):
        if not self.not_draw:
            if self.show_e_button:
                surface.blit(self.assets['e_key'], (self.rect.x + 24, self.rect.y))
            surface.blit(self.image_to_show, (self.rect.x + 16, self.rect.y + 16))
        if scripts.constants.SHOW_HITBOX:
                pygame.draw.rect(surface, scripts.constants.BLUE, self.rect, 1)
                pygame.draw.rect(surface, scripts.constants.RED, self.collider_rect, 1)