from typing import Any
import pygame
import scripts.constants
import math
from scripts.load import loadImages
import random

class Weapon:
    def __init__(self, type_of_weapon, weapon, on_ground):  # type_of_weapon: 'bows'
        self.assets = {
            "weapon": loadImages(f"wepons/{type_of_weapon}/{weapon}"),  # 'slingshot', 'classic_bow', 'composite_bow', 'crossbow'
            'e_key': pygame.image.load('assets/images/HUD/e_button/0.png')
            # "sound": pygame.mixer.Sound("assets/audio/bow.mp3")
        }
        # self.assets["sound"].set_volume(scripts.constants.FX_VOLUME)
        self.weapon = weapon
        self.original_image = self.assets["weapon"][0]
        self.on_ground = on_ground
        self.time = pygame.time.get_ticks()   
        self.event_key_cooldown = pygame.time.get_ticks()
        self.show_e_button = False
        
    
    def is_on_ground(self, screen_scroll):
        self.rect.centerx += screen_scroll[0]
        self.rect.centery += screen_scroll[1]
    
    def change_weapon(self, main_weapon):
        if pygame.time.get_ticks() - self.event_key_cooldown >= 1500:
            assets_ = main_weapon.assets
            weapon_ = main_weapon.weapon
            original_image_ = main_weapon.original_image
            
            main_weapon.assets = self.assets
            main_weapon.weapon = self.weapon
            main_weapon.original_image = self.original_image
            
            self.assets = assets_
            self.weapon = weapon_
            self.original_image = original_image_
            self.event_key_cooldown = pygame.time.get_ticks()
        
        
    def pick_up_weapon(self, player, event_key_pressed, main_weapon):
        if player.rect.colliderect(self.rect):
            self.show_e_button = True
            if event_key_pressed:
                    self.change_weapon(main_weapon)
                    event_key_pressed = False
        else:
            self.show_e_button = False
             
        return event_key_pressed  
        
        
       

    def change_fx_volume(self):
        #self.assets["sound"].set_volume(scripts.constants.FX_VOLUME)
        pass

class Bow(Weapon):
    def __init__(self, x, y, type_of_weapon, weapon, on_ground=False):
        super().__init__(type_of_weapon, weapon, on_ground)
        self.angle = 0
        self.image_to_show = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = pygame.Rect(0, 0, 32, 32)
        self.rect.center = (x, y)
        self.fired = False
        self.last_shot = pygame.time.get_ticks()
        self.flip = False
        
    def update(self,player, screen_scroll, main_weapon, event_key_pressed):
        if self.on_ground:
            self.is_on_ground(screen_scroll)
            self.pick_up_weapon(player, event_key_pressed, main_weapon)
            arrow = None
            
            
        else:
            self.rect.center = player.rect.center
        
            shot_cooldown = 500
            arrow = None
            pos = pygame.mouse.get_pos()
            pos_x = pos[0]/ scripts.constants.SCALE_WIDTH
            pos_y = pos[1]/ scripts.constants.SCALE_HEIGHT
            x_dist = (pos_x - self.rect.centerx) 
            y_dist = -(pos_y - self.rect.centery)  # negative because y coordinates increase down the screen
            self.angle = math.degrees(math.atan2(y_dist,x_dist)) 
            if pos_x < self.rect.centerx:
                self.flip = True
            else:
                self.flip = False
        
            # get mouseclick
            if pygame.mouse.get_pressed()[0] and not self.fired and (pygame.time.get_ticks()- self.last_shot) >= shot_cooldown:
                if self.weapon == "slingshot":
                    arrow = Arrow('rock',self)
                elif self.weapon == 'classic_bow':
                    arrow = Arrow('classic_arrow',self)
                elif self.weapon == 'composite_bow':
                    arrow = Arrow("composite_arrow",self)
                elif self.weapon == 'crossbow':
                    arrow = Arrow("bolt",self)
                self.fired = True
                self.last_shot = pygame.time.get_ticks()
                #self.assets["sound"].play()

            # reset mouseclick
            if pygame.mouse.get_pressed()[0] == False:
                self.fired = False
        
        return arrow, event_key_pressed
    

    def draw(self, surface):
        if self.show_e_button:
                surface.blit(self.assets['e_key'], (self.rect.x + 8, self.rect.y - 16))
                
        if self.weapon == 'slingshot' or self.weapon == 'crossbow':
            if not self.flip:
                self.image_to_show= pygame.transform.rotate(self.original_image, self.angle)
            else:
                if self.weapon == 'slingshot':
                    self.image_to_show= pygame.transform.flip(pygame.transform.rotate(self.original_image, self.angle),True,True)
                elif self.weapon == 'crossbow':
                    self.image_to_show= pygame.transform.flip(pygame.transform.rotate(self.original_image, -self.angle),False,True)
                    
        else:
            self.image_to_show= pygame.transform.rotate(self.original_image, self.angle)
        
        if self.weapon == "slingshot":
            surface.blit(self.image_to_show, (self.rect.center[0]-int(self.image_to_show.get_width()/2)+1,self.rect.center[1]-int(self.image_to_show.get_height()/2)-5))
        elif self.weapon == 'crossbow':
            surface.blit(self.image_to_show, (self.rect.center[0]-int(self.image_to_show.get_width()/2)+3,self.rect.center[1]-int(self.image_to_show.get_height()/2)-3))
        else:  
            surface.blit(self.image_to_show, (self.rect.center[0]-int(self.image_to_show.get_width()/2)-1,self.rect.center[1]-int(self.image_to_show.get_height()/2)-2))
        if scripts.constants.SHOW_HITBOX:
            pygame.draw.rect(surface, scripts.constants.RED, self.rect, 1)

class Arrow(pygame.sprite.Sprite):
    def __init__(self,type_of_arrow, bow):
        pygame.sprite.Sprite.__init__(self)
        self.x_cord = bow.rect.center[0]
        self.y_cord = bow.rect.center[1]
        self.angle = -bow.angle
        self.assets = {
            "arrow": loadImages(f"wepons/arrows/{type_of_arrow}")
        }
        self.original_image = pygame.transform.flip(self.assets["arrow"][0], True, False)
        self.image_to_show = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = pygame.Rect(0,0,16,16)
        self.rect.center = (self.x_cord,self.y_cord)
        
        #calculate the horizontal and vertical speeds based on the angle
        self.dx = math.cos(math.radians(self.angle)) * scripts.constants.ARROW_SPEED
        self.dy = math.sin(math.radians(self.angle)) * scripts.constants.ARROW_SPEED

    def update(self, enemy_list, screen_scroll, obstacle_tile, boss_list):
        # reset variables
        damage = 0
        damage_pos = None

        #reposition based on speed and screen scroll
        self.rect.x += screen_scroll[0] + self.dx
        self.rect.y += screen_scroll[1] + self.dy

        # check for collision
        for obstacle in obstacle_tile:
            if obstacle[1].colliderect(self.rect):
                self.kill()
        
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
        for enemy in boss_list:
            if enemy.rect.colliderect(self.rect) and enemy.alive:
                damage = 10 + random.randint(-5,5)
                damage_pos = enemy.rect
                enemy.health -= damage
                self.kill()
                break
        return damage, damage_pos

    def draw(self, surface):
        surface.blit(pygame.transform.flip(self.image_to_show,True,False), (self.rect.center[0]-int(self.image_to_show.get_width()/2),self.rect.center[1]-int(self.image_to_show.get_height()/2)))
        if scripts.constants.SHOW_HITBOX:
            pygame.draw.rect(surface, scripts.constants.RED, self.rect, 1)

class Magicball(pygame.sprite.Sprite):
    def __init__(self, type_of_magicball, x, y, target_x, target_y):
        pygame.sprite.Sprite.__init__(self)
        self.type = type_of_magicball
        if self.type == 'fireball':
            self.assets = {
                "magicball": loadImages("effects/fireball"),
                "audio": pygame.mixer.Sound(f"assets/audio/{type_of_magicball}.mp3")
            }
            self.assets["audio"].set_volume(scripts.constants.FX_VOLUME)
            self.sound_counter= pygame.time.get_ticks()
        elif self.type == 'troll_rock':
            self.assets = {
                "magicball": loadImages("effects/rock_troll"),
            }
        elif self.type == 'attack_ent':
            self.assets = {
                "magicball": loadImages("effects/attack_ent"),
            }
        self.original_image = self.assets["magicball"][0]
        self.animation_index = 0
        self.x_cord = x
        self.y_cord = y        
        x_dist = (target_x - x)
        y_dist = -(target_y - y)
        self.angle = math.degrees(math.atan2(y_dist,x_dist))
        self.image_to_show = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = pygame.Rect(0,0,32,16)
        self.rect.center = (self.x_cord, self.y_cord)

        #calculate the horizontal and vertical speeds based on the angle
        self.dx = math.cos(math.radians(self.angle)) * scripts.constants.MAGIC_BALL_SPEED
        self.dy = -(math.sin(math.radians(self.angle)) * scripts.constants.MAGIC_BALL_SPEED)
        
    def update(self, screen_scroll, player, obstacle_tiles):
        #handle audio
        
        player_on_fire = False
        # current_time = pygame.time.get_ticks()
        # if self.type == 'fireball':
        #     if current_time - self.sound_counter >= 100:
        #         self.assets["audio"].play()
        #         self.sound_counter = current_time

        #handle animation
       
        if self.type == 'fireball':
            self.image_to_show = pygame.transform.rotate(self.assets["magicball"][math.floor(self.animation_index)],self.angle)
            self.animation_index += 0.2
            if self.animation_index >= 7:
                self.animation_index = 5
        elif self.type == 'troll_rock':
            self.image_to_show = pygame.transform.rotate(self.assets["magicball"][math.floor(self.animation_index)],self.angle)
            self.angle += 1
            
            # checking colision
            for obstacle in obstacle_tiles:
                if obstacle[1].colliderect(self.rect):
                    self.kill()
        elif self.type == 'attack_ent':
            self.image_to_show = pygame.transform.flip(pygame.transform.rotate(self.assets["magicball"][math.floor(self.animation_index)],self.angle),True,True)
            self.animation_index += 0.2
            if self.animation_index >= 2:
                self.animation_index = 0
            
            # checking colision
            for obstacle in obstacle_tiles:
                if obstacle[1].colliderect(self.rect):
                    self.kill()
            


        #reposition based on speed and screen scroll
        self.rect.x += screen_scroll[0] + self.dx
        self.rect.y += screen_scroll[1] + self.dy
        
        # check if magic ball has gone off screen
        if self.rect.right < 0 or self.rect.left > scripts.constants.DISPLAY_WIDTH or self.rect.bottom < 0 or self.rect.top > scripts.constants.DISPLAY_HEIGHT:
            self.kill()

        # check collision between magicball and enemies
        if player.rect.colliderect(self.rect) and player.alive:
                if self.type == 'fireball':
                    player_on_fire = True
                    self.kill()
                elif self.type == 'troll_rock':
                    player.health -= scripts.constants.TROLL_DAMAGE
                    self.kill()
                elif self.type == 'attack_ent':
                    player.health -= scripts.constants.ENT_DAMAGE
                    self.kill()
        
        return player_on_fire
    
    def change_fx_volume(self):
        self.assets["audio"].set_volume(scripts.constants.FX_VOLUME)
                
    def draw(self, surface):
        surface.blit(self.image_to_show, (self.rect.centerx-16,self.rect.centery-16))
        if scripts.constants.SHOW_HITBOX:
            pygame.draw.rect(surface, scripts.constants.RED, self.rect, 1)
            
            
# class TwoHandedSword():
#     def __init__(self, type_of_sword, x,y):
#         self.assets={
#             'sword': loadImages(f'wepons/two_handed_swords/{type_of_sword}') # 'wooden_sword', 'rusted_sword', 'sword', 'great_sword', 'katana'
#         }
#         self.type_of_sword = type_of_sword
#         self.image_to_show = pygame.transform.rotate(self.assets['sword'][0], -30)
#         self.rect = self.image_to_show.get_rect()
#         self.rect.center = (x,y)
#         self.is_fliped = False
#         self.min_damage = 10
#         self.max_damage = 20
#         self.attack = False
#         self.angle = 15
#         self.attack_trigger = pygame.time.get_ticks()
#         self.can_attack = True
        
        
#     def update(self, player, player_is_fliped, mobs):
#         self.rect.center = player.rect.center
#         damage = 0
#         damage_pos = None
        
#         if pygame.time.get_ticks() - self.attack_trigger >= 700:
#             self.can_attack = True
#         else:
#             self.can_attack = False
            
#         if pygame.mouse.get_pressed()[0] and not self.attack and self.can_attack:
#             self.attack = True
#             self.attack_trigger = pygame.time.get_ticks()
        
#         if self.attack:
#             self.rect.y += 32
#             self.angle = -90
#             if not player_is_fliped:
#                 self.rect.x += 16
#                 self.rect = pygame.Rect(self.rect.x, self.rect.y -32, 50,32)
#             else:
#                 self.rect.x -= 32
#                 self.rect = pygame.Rect(self.rect.x+16, self.rect.y -32, 50,32)
#             if pygame.time.get_ticks() - self.attack_trigger >= 200:
#                 for mob in mobs:
#                     if self.rect.colliderect(mob.rect):
#                         if mob.alive:
#                             damage = random.randint(self.min_damage,self.max_damage)
#                             mob.health -= damage
#                             damage_pos = mob.rect
#                 self.angle = 15
#                 self.rect.center = player.rect.center 
#                 self.attack = False
            
        
#         if player_is_fliped:
#             self.is_fliped = True
#         else:
#             self.is_fliped = False
        
#         if not self.is_fliped:
#             self.image_to_show = pygame.transform.rotate(self.assets['sword'][0], self.angle)
#         else:
#             self.image_to_show = pygame.transform.flip(pygame.transform.rotate(self.assets['sword'][0], self.angle), True, False)
    
#         return damage, damage_pos
            
#     def draw(self, surface):
#         if self.attack:
#             if not self.is_fliped:
#                 surface.blit(self.image_to_show, (self.rect.centerx-8,self.rect.centery))
#             else:
#                 surface.blit(self.image_to_show, (self.rect.centerx-24,self.rect.centery))
#         else:
#             surface.blit(self.image_to_show, (self.rect.centerx-8,self.rect.centery-32))
#         if scripts.constants.SHOW_HITBOX:
#             pygame.draw.rect(surface, scripts.constants.RED, self.rect, 1)
            
# class Mace():
#     def __init__(self, type_of_mace, x,y):
#         self.assets={
#             'mace': loadImages(f'wepons/maces/{type_of_mace}') # 'stick', 'stick_with_nail', 'club_with_spikes', 'mace'
#         }
#         self.type_of_mace = type_of_mace
#         self.image_to_show = pygame.transform.rotate(self.assets['mace'][0], -30)
#         self.rect = pygame.Rect(0,0,32,32)
#         self.rect.center = (x,y)
#         self.is_fliped = False
#         self.min_damage = 15
#         self.max_damage = 30
#         self.attack = False
#         self.angle = 30
#         self.attack_trigger = pygame.time.get_ticks()
#         self.can_attack = True
        
        
#     def update(self, player, player_is_fliped, mobs):
#         self.rect.center = player.rect.center
#         damage = 0
#         damage_pos = None
        
#         if pygame.time.get_ticks() - self.attack_trigger >= 1500:
#             self.can_attack = True
#         else:
#             self.can_attack = False
            
#         if pygame.mouse.get_pressed()[0] and not self.attack and self.can_attack:
#             self.attack = True
#             self.attack_trigger = pygame.time.get_ticks()
        
#         if self.attack:
#             self.rect.y += 32
#             self.angle = -90
#             if not player_is_fliped:
#                 self.rect.x += 16
#                 self.rect = pygame.Rect(self.rect.x, self.rect.y -32, 40,40)
#             else:
#                 self.rect.x -= 32
#                 self.rect = pygame.Rect(self.rect.x+16, self.rect.y -32, 40,40)
#             if pygame.time.get_ticks() - self.attack_trigger >= 200:
#                 for mob in mobs:
#                     if self.rect.colliderect(mob.rect):
#                         if mob.alive:
#                             damage = random.randint(self.min_damage,self.max_damage)
#                             mob.health -= damage
#                             damage_pos = mob.rect
#                 self.angle = 30
#                 self.rect.center = player.rect.center 
#                 self.attack = False
            
        
#         if player_is_fliped:
#             self.is_fliped = True
#         else:
#             self.is_fliped = False
        
#         if not self.is_fliped:
#             self.image_to_show = pygame.transform.rotate(self.assets['mace'][0], self.angle)
#         else:
#             self.image_to_show = pygame.transform.flip(pygame.transform.rotate(self.assets['mace'][0], self.angle), True, False)
    
#         return damage, damage_pos
            
#     def draw(self, surface):
#         if self.attack:
#             if not self.is_fliped:
#                 surface.blit(self.image_to_show, (self.rect.centerx-8,self.rect.centery))
#             else:
#                 surface.blit(self.image_to_show, (self.rect.centerx-24,self.rect.centery))
#         else:
#             if not self.is_fliped:
#                 surface.blit(self.image_to_show, (self.rect.centerx-16,self.rect.centery-32))
#             else:
#                 surface.blit(self.image_to_show, (self.rect.centerx-8,self.rect.centery-32))
#         if scripts.constants.SHOW_HITBOX:
#             pygame.draw.rect(surface, scripts.constants.RED, self.rect, 1)

# class OneHandedAxe():
#     def __init__(self, type_of_axe, x,y):
#         self.assets={
#             'axe': loadImages(f'wepons/one_handed_axes/{type_of_axe}') # 'rusted_axe', 'axe'
#         }
#         self.type_of_mace = type_of_axe
#         self.image_to_show = pygame.transform.rotate(self.assets['axe'][0], -30)
#         self.rect = pygame.Rect(0,16,16,48)
#         self.rect.center = (x,y)
#         self.is_fliped = False
#         self.min_damage = 9
#         self.max_damage = 18
#         self.attack = False
#         self.angle = -45
#         self.attack_trigger = pygame.time.get_ticks()
#         self.can_attack = True
        
        
#     def update(self, player, player_is_fliped, mobs):
#         self.rect.center = player.rect.center
#         damage = 0
#         damage_pos = None
        
#         if pygame.time.get_ticks() - self.attack_trigger >= 400:
#             self.can_attack = True
#         else:
#             self.can_attack = False
            
#         if pygame.mouse.get_pressed()[0] and not self.attack and self.can_attack:
#             self.attack = True
#             self.attack_trigger = pygame.time.get_ticks()
        
#         if self.attack:
#             self.rect.y += 32
#             self.angle = -90
#             if not player_is_fliped:
#                 self.rect.x += 16
#                 self.rect = pygame.Rect(self.rect.x + 8, self.rect.y -32, 16,48)
#             else:
#                 self.rect.x -= 32
#                 self.rect = pygame.Rect(self.rect.x+ 8, self.rect.y -32, 16, 48)
#             if pygame.time.get_ticks() - self.attack_trigger >= 200:
#                 for mob in mobs:
#                     if self.rect.colliderect(mob.rect):
#                         if mob.alive:
#                             damage = random.randint(self.min_damage,self.max_damage)
#                             mob.health -= damage
#                             damage_pos = mob.rect
#                 self.angle = -45
#                 self.rect.center = player.rect.center 
#                 self.attack = False
            
        
#         if player_is_fliped:
#             self.is_fliped = True
#         else:
#             self.is_fliped = False
        
#         if not self.is_fliped:
#             self.image_to_show = pygame.transform.rotate(self.assets['axe'][0], self.angle)
#         else:
#             self.image_to_show = pygame.transform.flip(pygame.transform.rotate(self.assets['axe'][0], self.angle), True, False)
    
#         return damage, damage_pos
            
#     def draw(self, surface):
#         if self.attack:
#             if not self.is_fliped:
#                 surface.blit(self.image_to_show, (self.rect.centerx-24,self.rect.centery))
#             else:
#                 surface.blit(self.image_to_show, (self.rect.centerx,self.rect.centery))
#         else:
#             if not self.is_fliped:
#                 surface.blit(self.image_to_show, (self.rect.centerx,self.rect.centery-16))
#             else:
#                 surface.blit(self.image_to_show, (self.rect.centerx-20,self.rect.centery-16))
#         if scripts.constants.SHOW_HITBOX:
#             pygame.draw.rect(surface, scripts.constants.RED, self.rect, 1)

# class OneHandedHammer():
#     def __init__(self, type_of_hammer, x,y):
#         self.assets={
#             'hammer': loadImages(f'wepons/one_handed_hammers/{type_of_hammer}') # 'hammer'
#         }
#         self.type_of_mace = type_of_hammer
#         self.image_to_show = pygame.transform.rotate(self.assets['hammer'][0], -30)
#         self.rect = pygame.Rect(-8,-8,48, 48)
#         self.rect.center = (x,y)
#         self.is_fliped = False
#         self.min_damage = 9
#         self.max_damage = 18
#         self.attack = False
#         self.angle = -45
#         self.attack_trigger = pygame.time.get_ticks()
#         self.can_attack = True
        
        
#     def update(self, player, player_is_fliped, mobs):
#         self.rect.center = player.rect.center
#         damage = 0
#         damage_pos = None
        
#         if pygame.time.get_ticks() - self.attack_trigger >= 400:
#             self.can_attack = True
#         else:
#             self.can_attack = False
            
#         if pygame.mouse.get_pressed()[0] and not self.attack and self.can_attack:
#             self.attack = True
#             self.attack_trigger = pygame.time.get_ticks()
        
#         if self.attack:
#             self.angle = -90
#             if not player_is_fliped:
#                 self.rect = pygame.Rect(self.rect.x -8, self.rect.y -8, 48,48)
#             else:
#                 self.rect = pygame.Rect(self.rect.x-8, self.rect.y -8, 48, 48)
#             if pygame.time.get_ticks() - self.attack_trigger >= 200:
#                 for mob in mobs:
#                     if self.rect.colliderect(mob.rect):
#                         if mob.alive:
#                             damage = random.randint(self.min_damage,self.max_damage)
#                             mob.health -= damage
#                             damage_pos = mob.rect
#                 self.angle = -45
#                 self.rect.center = player.rect.center 
#                 self.attack = False
            
        
#         if player_is_fliped:
#             self.is_fliped = True
#         else:
#             self.is_fliped = False
        
#         if not self.is_fliped:
#             self.image_to_show = pygame.transform.rotate(self.assets['hammer'][0], self.angle)
#         else:
#             self.image_to_show = pygame.transform.flip(pygame.transform.rotate(self.assets['hammer'][0], self.angle), True, False)
    
#         return damage, damage_pos
            
#     def draw(self, surface):
#         if self.attack:
#             if not self.is_fliped:
#                 surface.blit(self.image_to_show, (self.rect.centerx-24,self.rect.centery))
#             else:
#                 surface.blit(self.image_to_show, (self.rect.centerx,self.rect.centery))
#         else:
#             if not self.is_fliped:
#                 surface.blit(self.image_to_show, (self.rect.centerx,self.rect.centery-16))
#             else:
#                 surface.blit(self.image_to_show, (self.rect.centerx-20,self.rect.centery-16))
#         if scripts.constants.SHOW_HITBOX:
#             pygame.draw.rect(surface, scripts.constants.RED, self.rect, 1)
            
        