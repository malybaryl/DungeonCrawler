import pygame
import scripts.constants
from random import choice 
from scripts.weapon import Bow, Throwable, TwoHandedSword, Spear


class Object:
    
    def __init__(self, type):
        self.type = type
        
    def update(self, *args):
        pass
    
    def draw(self, *args):
        pass
    
        
    
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
    
    
    def update(self, screen_scroll, event_key_pressed, player, hud):
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
                    type_of_weapon, new_wepon = self.return_new_wepon()
                    x = self.rect.x + 16
                    y = self.rect.y + 16
                    if type_of_weapon == 'bows':
                        wepon = Bow(x,y, type_of_weapon, new_wepon, player.level , hud, True, player)
                    elif type_of_weapon == 'throwables':
                        wepon = Throwable(x,y, type_of_weapon, new_wepon, player.level , hud, True, player)
                    elif type_of_weapon == 'two_handed_swords':
                        wepon = TwoHandedSword(x,y, type_of_weapon, new_wepon, player.level , hud ,True, player)
                    elif type_of_weapon == 'spears':
                        wepon = Spear(x,y, type_of_weapon, new_wepon, player.level , hud, True, player)
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
        type_of_weapons = choice(scripts.constants.TYPES_OF_WEAPONS)
        
        if type_of_weapons == 'bows':
            wepon = choice(scripts.constants.BOWS)
        elif type_of_weapons == 'throwables':
            wepon = choice(scripts.constants.THROWABLES)
        elif type_of_weapons == 'two_handed_swords':
            wepon = choice(scripts.constants.TWOHANDEDSWORDS)
        elif type_of_weapons == 'spears':
            wepon = choice(scripts.constants.SPEARS)
            
        return type_of_weapons, wepon
    
    
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
      
      
                
class FireUpPlayer(Object):
    def __init__(self, x, y):
        type = 'fire_up_player'
        super().__init__(type)
        self.rect = pygame.Rect(x, y, 32, 32)
        self.rect.center = (x,y)
        
        
    def update(self, screen_scroll, player, world_level):
        self.rect.x += screen_scroll[0]
        self.rect.y += screen_scroll[1]
        if self.rect.colliderect(player.rect) and player.alive:
            player.on_fire_trigger(1 * world_level, 3, 1)
            
            
    def draw(self, surface):
        if scripts.constants.SHOW_HITBOX:
            pygame.draw.rect(surface, scripts.constants.BLUE, self.rect, 32, 1)

class RoomEnterence(Object):
    def __init__(self, x, y, type):
        super().__init__(type)
        self.rect = pygame.Rect(x, y, 34, 66)
        self.rect.center = (x - 1,y - 1)
    
    def update(self, screen_scroll, player):
        self.rect.x += screen_scroll[0]
        self.rect.y += screen_scroll[1]
        if self.rect.colliderect(player.rect):
            print('True')
            return True
        print('False')   
        return False

class NextRoomEnterence(RoomEnterence):
    def __init__(self, x, y):
        type = 'next_room_enterence'
        super().__init__(x,y,type)

class PreviousRoomEnterence(RoomEnterence):
    def __init__(self, x, y):
        type = 'previous_room_enterence'
        super().__init__(x,y,type)
 
        
        
            
            