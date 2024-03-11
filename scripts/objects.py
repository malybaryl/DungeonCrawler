import pygame
import scripts.constants


class Object:
    def __init__(self, type):
        self.type = type
        
class Chest(Object):
    def __init__(self, x, y, closed_chest_img, opened_chest_img):
        super().__init__(type= 'chest')
        self.assets={
            'closed_chest': closed_chest_img,
            'opened_chest': opened_chest_img
        }
        self.image_to_show = self.assets['closed_chest']
        self.rect = pygame.Rect(x, y, 64, 64)
        self.rect.center = (x - 16,y)
        self.collider_rect = pygame.Rect(x,y,16,16)
        self.collider_rect.center = (x,y)
        self.closed = True
    
    def update(self, screen_scroll, event_key_pressed, player):
        self.rect.x += screen_scroll[0]
        self.rect.y += screen_scroll[1]
        
        if self.closed:
            self.image_to_show = self.assets['closed_chest']
        else:
            self.image_to_show = self.assets['opened_chest']
         
        if self.rect.colliderect(player.rect):    
            if event_key_pressed:
                self.closed = False
                
        if self.collider_rect.colliderect(player.rect):
            if self.collider_rect.top < player.rect.bottom < self.collider_rect.bottom:
                player.rect.bottom = self.collider_rect.top - 1
            elif self.collider_rect.bottom > player.rect.top > self.collider_rect.top:
                player.rect.top = self.rect.bottom + 1
            elif self.collider_rect.left < player.rect.right < self.collider_rect.right:
                player.rect.right = self.collider_rect.left - 1
            elif self.collider_rect.right > player.rect.left > self.collider_rect.left:
                player.rect.left = self.collider_rect.right + 1
            
            
    def draw(self, surface):
        surface.blit(self.image_to_show, (self.rect.x + 16, self.rect.y + 16))
        if scripts.constants.SHOW_HITBOX:
                pygame.draw.rect(surface, scripts.constants.BLUE, self.rect, 1)
                pygame.draw.rect(surface, scripts.constants.RED, self.collider_rect, 1)