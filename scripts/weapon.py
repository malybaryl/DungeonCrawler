from typing import Any
import pygame
import scripts.constants
import math
import random
from scripts.load import loadImages
from scripts.mathFunc import distance

# type_of_weapon: 'bows', 'throwables'
# BOWS:'slingshot', 'classic_bow', 'composite_bow', 'crossbow', 'deer_tamer', 'iron_bow', 'lava_guardian_crossbow'
# THROWABLES: 'rock', 'knive', 'throwing_axe', 'throwing_spear', 'broken_druid_staff, 'crusader_throwing_axe', 'lava_defenders_penetrator'
# TWO HANDED SWORDS: 'wooden_sword', 'rusted_sword', 'sword', 'katana', 'great_sword', 'sharpened_druid_staff', 'master_curved_slasher'
# SPEARS: 'wooden_spear', 'wooden_pitchfork', 'spear', 'pitchfork', 'extended_sickle', 'guard_spear', 'blade_on_stick', 'pike_with_a_wolf's_tooth', 'angel's_spear'
class Weapon:
    def __init__(self, type_of_weapon, weapon, on_ground, player_level, hud, player):  
        self.assets = {
            "weapon": loadImages(f"wepons/{type_of_weapon}/{weapon}"),  
            'e_key': pygame.image.load('assets/images/HUD/e_button/0.png'),
            "sound": pygame.mixer.Sound(f"assets/audio/{type_of_weapon}.mp3")
        }
        self.hud = hud
        self.type = type_of_weapon
        self.assets["sound"].set_volume(scripts.constants.FX_VOLUME)
        self.weapon = weapon
        self.original_image = self.assets["weapon"][0]
        self.on_ground = on_ground
        self.time = pygame.time.get_ticks()   
        self.event_key_cooldown = pygame.time.get_ticks()
        self.show_e_button = False
        self.weapon_level = player_level
        self.min_damage = self.set_min_damage(self.weapon_level, player.minimal_damage_multiplied)
        self.max_damage = self.set_max_damage(self.weapon_level, player.maximal_damage_multiplied)
        self.animate_x = 0
        self.animate_cooldown = pygame.time.get_ticks()
        if not self.on_ground:
            self.update_info_damage(hud)
       
        
    def set_min_damage(self, weapon_level, minimal_damage_multiply):
        min_damage = 3
        
        # BOWS
        if self.weapon == 'slingshot':
            min_damage = 3 * weapon_level * minimal_damage_multiply
        elif self.weapon == 'classic_bow':
            min_damage = 5 * weapon_level * minimal_damage_multiply
        elif self.weapon == 'composite_bow':
            min_damage = 5 * weapon_level * minimal_damage_multiply
        elif self.weapon == 'crossbow':
            min_damage = 20 * weapon_level * minimal_damage_multiply
        elif self.weapon == 'deer_tamer':
            min_damage = 20 * weapon_level * minimal_damage_multiply
        elif self.weapon == 'iron_bow':
            min_damage = 15 * weapon_level * minimal_damage_multiply
        elif self.weapon == 'lava_guardian_crossbow':
            min_damage = 20 * weapon_level * minimal_damage_multiply
            
        # THROWABLES
        elif self.weapon == 'rock':
            min_damage = 2 * weapon_level * minimal_damage_multiply
        elif self.weapon == 'knive':
            min_damage = 4 * weapon_level * minimal_damage_multiply
        elif self.weapon == 'throwing_axe':
            min_damage = 15 * weapon_level * minimal_damage_multiply
        elif self.weapon == 'throwing_spear':
            min_damage = 5 * weapon_level * minimal_damage_multiply
        elif self.weapon == 'broken_druid_staff':
            min_damage = 15 * weapon_level * minimal_damage_multiply
        elif self.weapon == 'crusader_throwing_axe':
            min_damage = 25 * weapon_level * minimal_damage_multiply
        elif self.weapon == 'lava_defenders_penetrator':
            min_damage = 15 * weapon_level * minimal_damage_multiply
        
        # THROWABLES
        elif self.weapon == 'wooden_sword':
            min_damage = 10 * weapon_level * minimal_damage_multiply
        elif self.weapon == 'rusted_sword':
            min_damage = 15 * weapon_level * minimal_damage_multiply
        elif self.weapon == 'sword':
            min_damage = 20 * weapon_level * minimal_damage_multiply
        elif self.weapon == 'katana':
            min_damage = 25 * weapon_level * minimal_damage_multiply
        elif self.weapon == 'great_sword':
            min_damage = 30 * weapon_level * minimal_damage_multiply
        elif self.weapon == 'sharpened_druid_staff':
            min_damage = 40 * weapon_level * minimal_damage_multiply
        elif self.weapon == 'master_curved_slasher':
            min_damage = 50 * weapon_level * minimal_damage_multiply
        
        # SPEARS
        elif self.weapon == 'wooden_spear':
            min_damage = 2 * weapon_level * minimal_damage_multiply
        elif self.weapon == 'spear':
            min_damage = 5 * weapon_level * minimal_damage_multiply
        elif self.weapon == 'extended_sickle':
            min_damage = 10 * weapon_level * minimal_damage_multiply
        elif self.weapon == 'guard_spear':
            min_damage = 15 * weapon_level * minimal_damage_multiply
        elif self.weapon == 'wooden_pitchfork':
            min_damage = 1 * weapon_level * minimal_damage_multiply
        elif self.weapon == 'pitchfork':
            min_damage = 3 * weapon_level * minimal_damage_multiply
        elif self.weapon == 'blade_on_stick':
            min_damage = 9 * weapon_level * minimal_damage_multiply
        elif self.weapon == "pike_with_a_wolf's_tooth":
            min_damage = 12 * weapon_level * minimal_damage_multiply
        elif self.weapon == "angel's_spear":
            min_damage = 16 * weapon_level * minimal_damage_multiply
        
        return int(min_damage)
        
        
    def set_max_damage(self, weapon_level, maximal_damage_mutiply):
        max_damage = 8
        
        # BOWS
        if self.weapon == 'slingshot':
            max_damage = 8 * weapon_level * maximal_damage_mutiply
        elif self.weapon == 'classic_bow':
            max_damage = 15 * weapon_level * maximal_damage_mutiply
        elif self.weapon == 'composite_bow':
            max_damage = 40 * weapon_level * maximal_damage_mutiply
        elif self.weapon == 'crossbow':
            max_damage = 40 * weapon_level * maximal_damage_mutiply
        elif self.weapon == 'deer_tamer':
            max_damage = 40 * weapon_level * maximal_damage_mutiply
        elif self.weapon == 'iron_bow':
            max_damage = 25 * weapon_level * maximal_damage_mutiply
        elif self.weapon == 'lava_guardian_crossbow':
            max_damage = 40 * weapon_level * maximal_damage_mutiply
            
        # THROWABLES
        elif self.weapon == 'rock':
            max_damage = 4 * weapon_level * maximal_damage_mutiply
        elif self.weapon == 'knive':
            max_damage = 8 * weapon_level * maximal_damage_mutiply
        elif self.weapon == 'throwing_axe':
            max_damage = 35 * weapon_level  * maximal_damage_mutiply   
        elif self.weapon == 'throwing_spear':
            max_damage = 20 * weapon_level  * maximal_damage_mutiply   
        elif self.weapon == 'broken_druid_staff':
            max_damage = 25 * weapon_level  * maximal_damage_mutiply   
        elif self.weapon == 'crusader_throwing_axe':
            max_damage = 50 * weapon_level   * maximal_damage_mutiply  
        elif self.weapon == 'lava_defenders_penetrator':
            max_damage = 25 * weapon_level   * maximal_damage_mutiply 
            
        # THROWABLES
        elif self.weapon == 'wooden_sword':
            max_damage = 15 * weapon_level * maximal_damage_mutiply
        elif self.weapon == 'rusted_sword':
            max_damage = 20 * weapon_level * maximal_damage_mutiply
        elif self.weapon == 'sword':
            max_damage = 25 * weapon_level * maximal_damage_mutiply
        elif self.weapon == 'katana':
            max_damage = 30 * weapon_level * maximal_damage_mutiply
        elif self.weapon == 'great_sword':
            max_damage = 35 * weapon_level * maximal_damage_mutiply
        elif self.weapon == 'sharpened_druid_staff':
            max_damage = 45 * weapon_level * maximal_damage_mutiply
        elif self.weapon == 'master_curved_slasher':
            max_damage = 55 * weapon_level  * maximal_damage_mutiply
        
        # SPEARS
        elif self.weapon == 'wooden_spear':
            max_damage = 5 * weapon_level * maximal_damage_mutiply
        elif self.weapon == 'spear':
            max_damage = 15 * weapon_level * maximal_damage_mutiply
        elif self.weapon == 'extended_sickle':
            max_damage = 25 * weapon_level * maximal_damage_mutiply
        elif self.weapon == 'guard_spear':
            max_damage = 30 * weapon_level * maximal_damage_mutiply
        elif self.weapon == 'wooden_pitchfork':
            max_damage = 5 * weapon_level * maximal_damage_mutiply
        elif self.weapon == 'pitchfork':
            max_damage = 15 * weapon_level * maximal_damage_mutiply
        elif self.weapon == 'blade_on_stick':
            max_damage = 45 * weapon_level * maximal_damage_mutiply
        elif self.weapon == "pike_with_a_wolf's_tooth":
            max_damage = 60 * weapon_level * maximal_damage_mutiply
        elif self.weapon == "angel's_spear":
            max_damage = 80 * weapon_level * maximal_damage_mutiply
    
        
        return int(max_damage)
    
    
    def update_info_damage(self, hud):
        hud.min_damage = self.min_damage
        hud.max_damage = self.max_damage
        hud.damege_text = hud.font.render(f"Damage: {self.min_damage}-{self.max_damage}", True, scripts.constants.WHITE)
        
    def update_minimal_damage(self, player, hud):
        self.min_damage = int(self.set_min_damage(self.weapon_level, player.minimal_damage_multiplied))
        if self.min_damage >= self.max_damage:
            self.max_damage = self.min_damage
        self.update_info_damage(hud)     
    
    def update_maximal_damage(self, player, hud):
        self.max_damage = int(self.set_max_damage(self.weapon_level, player.maximal_damage_multiplied))
        self.update_info_damage(hud)     
       
    def is_on_ground(self, screen_scroll):
        self.rect.centerx += screen_scroll[0]
        self.rect.centery += screen_scroll[1]
    
    def change_weapon(self, main_weapon, hud, player):
        if pygame.time.get_ticks() - self.event_key_cooldown >= 1500:
            original_class_ = main_weapon.__class__
            original_weapon_level_ = main_weapon.weapon_level
            assets_ = main_weapon.assets
            weapon_ = main_weapon.weapon
            original_x_cord_ = main_weapon.rect.x
            original_y_cord_ = main_weapon.rect.y
            original_type_ = main_weapon.type
            original_image_ = main_weapon.original_image
            original_min_damage_ = main_weapon.min_damage
            original_max_damage_ = main_weapon.max_damage
            original_shot_cooldown_ = main_weapon.shot_cooldown
            if self.type == 'bows' or self.type == 'throwables':
                original_distance_ = main_weapon.distance
            print('im here')
            main_weapon.__class__ = self.__class__  
            if self.type == 'bows':
                main_weapon.__init__(self.rect.x, self.rect.y, self.type, self.weapon, self.weapon_level, hud,False, player)  
                hud.visible_coursor(True)
            elif self.type == 'throwables':
                main_weapon.__init__(self.rect.x, self.rect.y,self.type, self.weapon, self.weapon_level, hud,False, player)   
                hud.visible_coursor(True)
            elif self.type == 'two_handed_swords':
                main_weapon.__init__(self.rect.x, self.rect.y,self.type, self.weapon, self.weapon_level, hud,False, player) 
                hud.visible_coursor(False)
            elif self.type == 'spears':
                main_weapon.__init__(self.rect.x, self.rect.y,self.type, self.weapon, self.weapon_level, hud,False, player) 
                hud.visible_coursor(False)
                      
            main_weapon.assets = self.assets
            main_weapon.weapon = self.weapon
            main_weapon.type = self.type
            main_weapon.original_image = self.original_image
            main_weapon.min_damage = self.set_min_damage(main_weapon.weapon_level, player.minimal_damage_multiplied)
            main_weapon.max_damage = self.set_max_damage(main_weapon.weapon_level, player.maximal_damage_multiplied)
            main_weapon.update_info_damage(hud)
            main_weapon.shot_cooldown = self.shot_cooldown
            if self.type == 'bows' or self.type == 'throwables':
                main_weapon.distance = self.distance
            
            self.__class__ = original_class_  
            if original_type_ == 'bows':
                self.__init__(original_x_cord_ + 16, original_y_cord_ + 16, original_type_, weapon_, original_weapon_level_, hud, True, player)  
            elif original_type_ == 'throwables':
                self.__init__(original_x_cord_ + 16, original_y_cord_ + 16,original_type_, weapon_, original_weapon_level_, hud, True, player) 
            elif original_type_ == 'two_handed_swords':
                self.__init__(original_x_cord_ + 16, original_y_cord_ + 16,original_type_, weapon_, original_weapon_level_, hud, True, player) 
            elif original_type_ == 'spears':
                self.__init__(original_x_cord_ + 16, original_y_cord_ + 16,original_type_, weapon_, original_weapon_level_, hud, True, player) 
                
            self.assets = assets_
            self.weapon = weapon_
            self.type = original_type_
            self.original_image = original_image_
            self.min_damage = original_min_damage_
            self.max_damage = original_max_damage_
            self.event_key_cooldown = pygame.time.get_ticks()
            self.shot_cooldown = original_shot_cooldown_
            if self.type == 'bows' or self.type == 'throwables':
                self.distance = original_distance_
        
        
    def pick_up_weapon(self, player, event_key_pressed, main_weapon, hud):
        if player.rect.colliderect(self.rect):
            self.show_e_button = True
            if event_key_pressed:
                    self.change_weapon(main_weapon, hud, player)
                    event_key_pressed = False
        else:
            self.show_e_button = False
             
        return event_key_pressed  
        
    
    def change_fx_volume(self):
        self.assets["sound"].set_volume(scripts.constants.FX_VOLUME)



class Bow(Weapon):
    def __init__(self, x, y, type_of_weapon, weapon, player_level, hud, on_ground=False, player = None):
        super().__init__(type_of_weapon, weapon, on_ground, player_level, hud, player)
        self.angle = 0
        self.image_to_show = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = pygame.Rect(0, 0, 32, 32)
        self.rect.center = (x, y)
        self.fired = False
        self.last_shot = pygame.time.get_ticks()
        self.flip = False
        self.double_shot = False
        self.double_shot_cooldown = 0
        if self.weapon != 'crossbow':
            self.shot_cooldown = 500
            self.distance = 200
        else:
            self.shot_cooldown = 1000
            self.distance = 250
        
    def update(self,player, screen_scroll, main_weapon, event_key_pressed, hud):
        if self.on_ground:
            self.is_on_ground(screen_scroll)
            self.pick_up_weapon(player, event_key_pressed, main_weapon, hud)
            arrow = None
            
        else:
            self.rect.center = player.rect.center
        
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
            if pygame.mouse.get_pressed()[0] and not self.fired and (pygame.time.get_ticks()- self.last_shot) >= self.shot_cooldown:
                if self.weapon == "slingshot":
                    arrow = Arrow('rock',self)
                elif self.weapon == 'classic_bow':
                    arrow = Arrow('classic_arrow',self)
                elif self.weapon == 'composite_bow':
                    arrow = Arrow("composite_arrow",self)
                elif self.weapon == 'crossbow':
                    arrow = Arrow("bolt",self)
                elif self.weapon == 'deer_tamer':
                    arrow = Arrow("bolt",self)
                elif self.weapon == 'iron_bow':
                    arrow = Arrow("iron_bow",self)
                    self.double_shot = True
                    self.double_shot_cooldown = pygame.time.get_ticks()
                elif self.weapon == 'lava_guardian_crossbow':
                    arrow = Arrow("lava_guardian_crossbow",self)
                else:
                    arrow = Arrow('classic_arrow',self)
                self.fired = True
                self.last_shot = pygame.time.get_ticks()
                self.assets["sound"].play()
                
            # double shot handler
            if self.double_shot:
                if pygame.time.get_ticks() - self.double_shot_cooldown >= 100:
                    if self.weapon == 'iron_bow':
                        arrow = Arrow("iron_bow",self)
                    self.double_shot = False

            # reset mouseclick
            if pygame.mouse.get_pressed()[0] == False:
                self.fired = False
        
        return arrow, event_key_pressed
    

    def draw(self, surface):
        if self.show_e_button:
                surface.blit(self.assets['e_key'], (self.rect.x + 8, self.rect.y - 16))
                
        if self.weapon == 'slingshot' or self.weapon == 'crossbow' or self.weapon == 'lava_guardian_crossbow':
            if not self.flip:
                self.image_to_show= pygame.transform.rotate(self.original_image, self.angle)
            else:
                if self.weapon == 'slingshot':
                    self.image_to_show= pygame.transform.flip(pygame.transform.rotate(self.original_image, self.angle),True,True)
                elif self.weapon == 'crossbow' or self.weapon == 'lava_guardian_crossbow':
                    self.image_to_show= pygame.transform.flip(pygame.transform.rotate(self.original_image, -self.angle),False,True)
                    
        else:
            self.image_to_show= pygame.transform.rotate(self.original_image, self.angle)
        
        if self.weapon == "slingshot":
            surface.blit(self.image_to_show, (self.rect.center[0]-int(self.image_to_show.get_width()/2)+1,self.rect.center[1]-int(self.image_to_show.get_height()/2)-5))
        elif self.weapon == 'crossbow' or self.weapon == 'lava_guardian_crossbow':
            surface.blit(self.image_to_show, (self.rect.center[0]-int(self.image_to_show.get_width()/2)+3,self.rect.center[1]-int(self.image_to_show.get_height()/2)-3))
        else:  
            surface.blit(self.image_to_show, (self.rect.center[0]-int(self.image_to_show.get_width()/2)-1,self.rect.center[1]-int(self.image_to_show.get_height()/2)-2))
        if scripts.constants.SHOW_HITBOX:
            pygame.draw.rect(surface, scripts.constants.RED, self.rect, 1)



class Arrow(pygame.sprite.Sprite):
    def __init__(self, type_of_arrow, bow):
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
        self.min_damage = bow.min_damage
        self.max_damage = bow.max_damage
        self.distance = bow.distance
        self.type_of_arrow = type_of_arrow
        
        #calculate the horizontal and vertical speeds based on the angle
        self.dx = math.cos(math.radians(self.angle)) * scripts.constants.ARROW_SPEED
        self.dy = math.sin(math.radians(self.angle)) * scripts.constants.ARROW_SPEED

    def update(self, weapon, enemy_list, screen_scroll, obstacle_tile, boss_list):
        # reset variables
        damage = 0
        damage_pos = None
        current_distance = distance(self.rect.x, self.rect.y, self.x_cord, self.y_cord)

        # animation handle
        if self.type_of_arrow == 'throwing_axe' or self.type_of_arrow == 'crusader_throwing_axe':
            if self.dx >= 0:
                self.image_to_show = pygame.transform.rotate(self.original_image, self.angle)
                self.angle += 25
            else:
                self.image_to_show = pygame.transform.flip(self.original_image, True, False)
                self.image_to_show = pygame.transform.rotate(self.image_to_show, self.angle) 
                self.angle -= 25
            
        #reposition based on speed and screen scroll
        self.rect.x += screen_scroll[0] + self.dx
        self.rect.y += screen_scroll[1] + self.dy

        # check for collision
        for obstacle in obstacle_tile:
            if obstacle[1].colliderect(self.rect):
                self.kill()
        
        # check if arrow has gone off distance
        if current_distance >= self.distance:
            self.kill()

        # check collision between arrow and enemies
        for enemy in enemy_list:
            if enemy.rect.colliderect(self.rect) and enemy.alive:
                damage = random.randint(self.min_damage , self.max_damage)
                damage_pos = enemy.rect
                enemy.health -= damage
                self.kill()
                break
        for enemy in boss_list:
            if enemy.rect.colliderect(self.rect) and enemy.alive:
                damage = random.randint(self.min_damage , self.max_damage)
                damage_pos = enemy.rect
                enemy.health -= damage
                self.kill()
                break
        return damage, damage_pos

    def draw(self, surface):
        surface.blit(pygame.transform.flip(self.image_to_show,True,False), (self.rect.center[0]-int(self.image_to_show.get_width()/2),self.rect.center[1]-int(self.image_to_show.get_height()/2)))
        if scripts.constants.SHOW_HITBOX:
            pygame.draw.rect(surface, scripts.constants.RED, self.rect, 1)



class MagicAttactDruid(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.direction = direction
        self.assets={
            'bolt': loadImages('char/druid_boss/druid_bolt')
        }
        self.rect = pygame.Rect(0,0,32,32)
        self.rect.center = (x,y)
        self.index = 0
        self.image_to_show = self.assets['bolt'][self.index]
        self.type = 'druid_bolt'
        self.time = pygame.time.get_ticks()

    
    def update(self, screen_scroll, player):
        self.rect.x += screen_scroll[0]
        self.rect.y += screen_scroll[1]
        # reset variables
        dx = 0
        dy = 0
        
        # handle animation
        self.index += 0.1
        if self.index >= 5:
            self.index = 0
        self.image_to_show = self.assets['bolt'][math.floor(self.index)]
        
        # define variables and move bolt
        if self.direction == 0:
            dy = -scripts.constants.MAGIC_BALL_SPEED
        elif self.direction == 1:
            dy = -scripts.constants.MAGIC_BALL_SPEED
            dx = scripts.constants.MAGIC_BALL_SPEED
        elif self.direction == 2:
            dx = scripts.constants.MAGIC_BALL_SPEED
        elif self.direction == 3:
            dy = scripts.constants.MAGIC_BALL_SPEED
            dx = scripts.constants.MAGIC_BALL_SPEED
        elif self.direction == 4:
            dy = scripts.constants.MAGIC_BALL_SPEED
        elif self.direction == 5:
            dy = scripts.constants.MAGIC_BALL_SPEED
            dx = -scripts.constants.MAGIC_BALL_SPEED
        elif self.direction == 6:
            dx = -scripts.constants.MAGIC_BALL_SPEED
        else:
            dy = -scripts.constants.MAGIC_BALL_SPEED
            dx = -scripts.constants.MAGIC_BALL_SPEED
            
        self.rect.x += dx
        self.rect.y += dy
        
        if self.rect.colliderect(player.rect):
            player.health -= 20
            self.kill()
            
        if pygame.time.get_ticks() - self.time >= 5000:
            self.kill()
        
            
    
    def draw(self, surface):
        surface.blit(self.image_to_show, (self.rect.x, self.rect.y))
        if scripts.constants.SHOW_HITBOX:
            pygame.draw.rect(surface, scripts.constants.RED, self.rect, 1)
    
    
    
class Magicball(pygame.sprite.Sprite):
    def __init__(self, type_of_magicball, x, y, target_x, target_y, level):
        pygame.sprite.Sprite.__init__(self)
        self.type = type_of_magicball
        if self.type == 'fireball':
            self.assets = {
                "magicball": loadImages("wepons/magica/fire_ball"),
                "audio": pygame.mixer.Sound(f"assets/audio/{type_of_magicball}.mp3")
            }
            self.assets["audio"].set_volume(scripts.constants.FX_VOLUME)
            self.sound_counter= pygame.time.get_ticks()
        elif self.type == 'troll_rock':
            self.assets = {
                "magicball": loadImages("effects/rock_troll"),
                "audio": pygame.mixer.Sound("assets/audio/swing.mp3")
            }
            self.assets["audio"].set_volume(scripts.constants.FX_VOLUME)
            self.sound_counter= pygame.time.get_ticks()
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
        self.rect = pygame.Rect(0,0,16,16)
        self.rect.center = (self.x_cord, self.y_cord)
        self.play_once = True
        self.level = level

        #calculate the horizontal and vertical speeds based on the angle
        self.dx = math.cos(math.radians(self.angle)) * scripts.constants.MAGIC_BALL_SPEED
        self.dy = -(math.sin(math.radians(self.angle)) * scripts.constants.MAGIC_BALL_SPEED)
        
    def update(self, screen_scroll, player, obstacle_tiles):
        #handle audio
        current_time = pygame.time.get_ticks()
        if self.type == 'fireball':
            if current_time - self.sound_counter >= 100:
                self.assets["audio"].play()
                self.sound_counter = current_time
        elif self.type == 'troll_rock':
            if self.play_once:
                self.assets["audio"].play()
                self.play_once = False
       
        #handle animation
        if self.type == 'fireball':
            self.image_to_show = pygame.transform.rotate(self.assets["magicball"][math.floor(self.animation_index)],self.angle)
            self.animation_index += 0.2
            if self.animation_index >= 5:
                self.animation_index = 2
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
                    player.on_fire_trigger(5 * self.level, 4, 1)
                    self.kill()
                elif self.type == 'troll_rock':
                    player.health -= scripts.constants.TROLL_DAMAGE * self.level
                    self.kill()
                elif self.type == 'attack_ent':
                    player.health -= scripts.constants.ENT_DAMAGE * self.level
                    self.kill()
        

    def change_fx_volume(self):
        self.assets["audio"].set_volume(scripts.constants.FX_VOLUME)
                
                
    def draw(self, surface):
        surface.blit(self.image_to_show, (self.rect.centerx-16,self.rect.centery-16))
        if scripts.constants.SHOW_HITBOX:
            pygame.draw.rect(surface, scripts.constants.RED, self.rect, 1)



class Throwable(Weapon):
    def __init__(self, x, y, type_of_weapon, weapon, player_level, hud, on_ground=False, player = None):
        super().__init__(type_of_weapon, weapon, on_ground, player_level, hud, player)
        self.angle = 0
        self.image_to_show = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = pygame.Rect(0, 0, 32, 32)
        self.rect.center = (x, y)
        self.fired = False
        self.last_shot = pygame.time.get_ticks()
        self.flip = False
        if self.weapon != 'throwing_axe' or self.weapon != 'crusader_throwing_axe':
            self.shot_cooldown = 250
        else:
            self.shot_cooldown = 1000
        self.distance = 100

        
    def update(self,player, screen_scroll, main_weapon, event_key_pressed, hud):
        if self.on_ground:
            self.is_on_ground(screen_scroll)
            self.pick_up_weapon(player, event_key_pressed, main_weapon, hud)
            arrow = None
            
        else:
            self.rect.center = player.rect.center
        
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
            if pygame.mouse.get_pressed()[0] and not self.fired and (pygame.time.get_ticks()- self.last_shot) >= self.shot_cooldown:
                if self.weapon == "rock":
                    arrow = Arrow('rock',self)
                elif self.weapon == "knive":
                    arrow = Arrow('knive',self)
                elif self.weapon == "throwing_axe":
                    arrow = Arrow('throwing_axe',self)
                elif self.weapon == "throwing_spear":
                    arrow = Arrow('throwing_spear',self)
                elif self.weapon == "broken_druid_staff":
                    arrow = Arrow('broken_druid_staff',self)
                elif self.weapon == "crusader_throwing_axe":
                    arrow = Arrow('crusader_throwing_axe',self)
                elif self.weapon == "lava_defenders_penetrator":
                    arrow = Arrow('lava_defenders_penetrator',self)
                self.fired = True
                self.last_shot = pygame.time.get_ticks()
                self.assets["sound"].play()

            # reset mouseclick
            if pygame.mouse.get_pressed()[0] == False:
                self.fired = False
        
        return arrow, event_key_pressed
    

    def draw(self, surface):
        if self.show_e_button:
                surface.blit(self.assets['e_key'], (self.rect.x + 8, self.rect.y - 16))
                
        if self.weapon == 'rock' or self.weapon == 'knive' or self.weapon == 'throwing_axe' or self.weapon == 'throwing_spear' or self.weapon == 'broken_druid_staff' or self.weapon == 'crusader_throwing_axe' or self.weapon == 'lava_defenders_penetrator':
            if not self.flip:
                self.image_to_show= pygame.transform.rotate(self.original_image, self.angle)
            else:
                if self.weapon == 'rock' or self.weapon == 'knive' or self.weapon == 'throwing_spear' or self.weapon == 'broken_druid_staff' or self.weapon == 'lava_defenders_penetrator':
                    self.image_to_show= pygame.transform.flip(pygame.transform.rotate(self.original_image, self.angle),True,True)  
                elif self.weapon == 'throwing_axe' or self.weapon == 'crusader_throwing_axe':
                    self.image_to_show= pygame.transform.flip(pygame.transform.rotate(self.original_image, -self.angle),False,True)  
                       
        else:
            self.image_to_show= pygame.transform.rotate(self.original_image, self.angle)
        
        if self.weapon == "rock" or self.weapon == 'knive' or self.weapon == 'throwing_axe' or self.weapon == 'throwing_spear' or self.weapon == 'broken_druid_staff' or self.weapon == 'crusader_throwing_axe' or self.weapon == 'lava_defenders_penetrator':
            surface.blit(self.image_to_show, (self.rect.center[0]-int(self.image_to_show.get_width()/2)+1,self.rect.center[1]-int(self.image_to_show.get_height()/2)-5))
        else:  
            surface.blit(self.image_to_show, (self.rect.center[0]-int(self.image_to_show.get_width()/2)-1,self.rect.center[1]-int(self.image_to_show.get_height()/2)-2))
        if scripts.constants.SHOW_HITBOX:
            pygame.draw.rect(surface, scripts.constants.RED, self.rect, 1)
    
          
     
class TwoHandedSword(Weapon):
    def __init__(self, x, y, type_of_weapon, weapon, player_level, hud, on_ground=False, player = None):
        super().__init__(type_of_weapon, weapon, on_ground, player_level, hud, player)
        if not on_ground:
            self.image_to_show = pygame.transform.rotate(self.original_image, 10)
        else:
            self.image_to_show = self.original_image
        self.rect = pygame.Rect(0, 0, 32, 32)
        self.rect.center = (x, y)
        self.fired = False
        self.last_shot = pygame.time.get_ticks()
        self.flip = False
        self.shot_cooldown = 1000
        self.distance = 100
        self.swing = False
        self.animate_degree = 10
        self.image_to_animate = pygame.transform.scale(self.original_image, (16, 64))
        self.animate_couner = 0
        self.animate_x_shr = 0
        self.animate_y_shr = 0
        self.animate_forward = True

        
    def update(self, player, screen_scroll, main_weapon, event_key_pressed, hud, player_is_fliped, enemy_list):
        if self.on_ground:
            self.is_on_ground(screen_scroll)
            self.pick_up_weapon(player, event_key_pressed, main_weapon, hud)
            damage = None
            damage_pos = None
            
        else:
            self.rect.center = player.rect.center
        
            damage = None
            damage_pos = None
            if player_is_fliped:
                self.flip = True
            else:
                self.flip = False
                
            # animation handler
            if not self.swing:
                if self.flip:
                    self.image_to_show = pygame.transform.flip(pygame.transform.rotate(self.original_image, 10), True, False)
                else:
                    self.image_to_show = pygame.transform.rotate(self.original_image, 10)
            else:
                self.image_to_show = pygame.transform.flip(self.image_to_animate, True, False)
                if self.flip:
                    if self.animate_forward:
                        self.animate_x_shr += 1
                        self.animate_y_shr += 4
                        if self.animate_x_shr >= 32 and self.animate_y_shr >= 128:
                            self.animate_forward = False
                    else:
                        self.animate_x_shr -= 2
                        self.animate_y_shr -= 8
                        if self.animate_x_shr <= 0 and self.animate_y_shr <= 0:
                            self.animate_x_shr = 0
                            self.animate_y_shr = 0  
                    self.image_to_animate = pygame.transform.scale(self.original_image, (self.animate_x_shr, self.animate_y_shr))
                    self.image_to_show = pygame.transform.rotate(self.image_to_animate, self.animate_degree)
                    self.animate_x -= 1
                    self.animate_couner += 1
                    if self.animate_x <= -32:
                        self.animate_x = -32
                    self.animate_degree += 9
                    if self.animate_degree >= 195:
                        self.animate_degree = 195
                    if self.animate_couner >= 50:
                        self.animate_degree = 10
                        self.swing = False
                        self.animate_x = 0
                        self.animate_couner = 0
                        self.animate_forward = True
                else:
                    if self.animate_forward:
                        self.animate_x_shr += 1
                        self.animate_y_shr += 4
                        if self.animate_x_shr >= 32 and self.animate_y_shr >= 128:
                            self.animate_forward = False
                    else:
                        self.animate_x_shr -= 2
                        self.animate_y_shr -= 8
                        if self.animate_x_shr <= 0 and self.animate_y_shr <= 0:
                            self.animate_x_shr = 0
                            self.animate_y_shr = 0  
                    self.image_to_animate = pygame.transform.scale(self.original_image, (self.animate_x_shr, self.animate_y_shr))
                    self.image_to_show = pygame.transform.rotate(self.image_to_animate, self.animate_degree)
                    self.animate_x += 1
                    self.animate_couner += 1
                    if self.animate_x >= 32:
                        self.animate_x = 32
                    self.animate_degree -= 9
                    if self.animate_degree <= -195:
                        self.animate_degree = -195
                    if self.animate_couner >= 50:
                        self.animate_degree = -10
                        self.swing = False
                        self.animate_x = 0
                        self.animate_couner = 0
                        self.animate_forward = True
        
            # get mouseclick
            if pygame.mouse.get_pressed()[0] and not self.fired and (pygame.time.get_ticks()- self.last_shot) >= self.shot_cooldown:
                # attack handeler
                damage, damage_pos = self.attack(enemy_list)
                self.swing = True
                self.fired = True
                self.last_shot = pygame.time.get_ticks()
                self.assets["sound"].play()

            # reset mouseclick
            if pygame.mouse.get_pressed()[0] == False:
                self.fired = False
        
        return damage, damage_pos, event_key_pressed
    
    def attack(self, enemy_list):
        damage = None
        damage_pos = None

        for enemy in enemy_list:
            if distance(self.rect.centerx, self.rect.centery, enemy.rect.centerx, enemy.rect.centery) <= self.distance and enemy.alive:
                if self.flip:
                    if enemy.rect.centerx <= self.rect.centerx:
                        damage = random.randint(self.min_damage , self.max_damage)
                        damage_pos = enemy.rect
                        enemy.health -= damage
                else:
                    if enemy.rect.centerx >= self.rect.centerx:
                        damage = random.randint(self.min_damage , self.max_damage)
                        damage_pos = enemy.rect
                        enemy.health -= damage
                                 
        return damage, damage_pos

    def draw(self, surface):
        if self.show_e_button:
                surface.blit(self.assets['e_key'], (self.rect.x + 8, self.rect.y - 16))
                
        surface.blit(self.image_to_show, (self.rect.center[0]-int(self.image_to_show.get_width()/2)-1 + self.animate_x,self.rect.center[1]-int(self.image_to_show.get_height()/2)-12))
        if scripts.constants.SHOW_HITBOX:
            pygame.draw.rect(surface, scripts.constants.RED, self.rect, 1)



class Spear(Weapon):
    def __init__(self, x, y, type_of_weapon, weapon, player_level, hud, on_ground=False, player = None):
        super().__init__(type_of_weapon, weapon, on_ground, player_level, hud, player)
        if self.weapon == 'wooden_spear' or self.weapon == 'spear' or self.weapon == 'extended_sickle' or self.weapon == 'guard_spear':
            self.shot_cooldown = 2000
            self.image_to_show = self.original_image
        else:
            self.shot_cooldown = 250
            self.image_to_show = pygame.transform.rotate(self.original_image, 90)
        if on_ground:
            self.image_to_show = self.original_image
        self.rect = pygame.Rect(0, 0, 32, 32)
        self.rect.center = (x, y)
        self.fired = False
        self.last_shot = pygame.time.get_ticks()
        self.flip = False
        self.distance = 100
        self.swing = False
        self.stab = False
        self.animate_degree = -10
        self.image_to_animate = pygame.transform.scale(self.original_image, (16, 64))
        self.animate_couner = 0
        self.animate_x_shr = 0
        self.animate_y_shr = 0
        self.animate_forward = True
        self.attack_cooldown = pygame.time.get_ticks()
        self.attacks = 3
        self.do_stab_once = True

        
    def update(self, player, screen_scroll, main_weapon, event_key_pressed, hud, player_is_fliped, enemy_list):
        if self.on_ground:
            self.is_on_ground(screen_scroll)
            self.pick_up_weapon(player, event_key_pressed, main_weapon, hud)
            damage = None
            damage_pos = None
            
        else:
            self.rect.center = player.rect.center
        
            damage = None
            damage_pos = None
            if player_is_fliped:
                self.flip = True
            else:
                self.flip = False
                
            # animation handler
            if not self.swing and not self.stab:
                if self.flip:
                    if self.weapon == 'wooden_spear' or self.weapon == 'spear' or self.weapon == 'extended_sickle' or self.weapon == 'guard_spear':
                        self.image_to_show = pygame.transform.flip(self.original_image, True, False)
                    else:
                        self.image_to_show = pygame.transform.rotate(self.original_image, 90)
                else:
                    if self.weapon == 'wooden_spear' or self.weapon == 'spear' or self.weapon == 'extended_sickle' or self.weapon == 'guard_spear':
                        self.image_to_show = self.original_image
                    else:
                        self.image_to_show = pygame.transform.rotate(self.original_image, -90)
            elif self.swing:
                self.image_to_show = pygame.transform.flip(self.image_to_animate, True, False)
                if self.flip:
                    self.animate_x_shr += 1
                    self.animate_y_shr += 4
                    if self.animate_x_shr >= 32 and self.animate_y_shr >= 128:
                        self.animate_x_shr = 32
                        self.animate_y_shr = 128
                    self.image_to_animate = pygame.transform.scale(self.original_image, (self.animate_x_shr, self.animate_y_shr))
                    self.image_to_show = pygame.transform.rotate(self.image_to_animate, self.animate_degree)
                    self.animate_couner += 1
                    self.animate_degree += 20
                    if self.animate_degree >= 1080:
                        self.animate_degree = 1080
                    if self.animate_couner >= 50:
                        self.animate_degree = 0
                        self.swing = False
                        self.animate_x = 0
                        self.animate_couner = 0
                        self.animate_forward = True
                        self.animate_x_shr = 0
                        self.animate_y_shr = 0
                else:
                    self.animate_x_shr += 1
                    self.animate_y_shr += 4
                    if self.animate_x_shr >= 32 and self.animate_y_shr >= 128:
                        self.animate_x_shr = 32
                        self.animate_y_shr = 128
                    self.image_to_animate = pygame.transform.scale(self.original_image, (self.animate_x_shr, self.animate_y_shr))
                    self.image_to_show = pygame.transform.rotate(self.image_to_animate, self.animate_degree)
                    self.animate_couner += 1
                    self.animate_degree -= 18
                    if self.animate_degree <= -1080:
                        self.animate_degree = -1080
                    if self.animate_couner >= 50:
                        self.animate_degree = 0
                        self.swing = False
                        self.animate_x = 0
                        self.animate_couner = 0
                        self.animate_forward = True
                        self.animate_x_shr = 0
                        self.animate_y_shr = 0
        
            # get mouseclick
            if pygame.mouse.get_pressed()[0] and not self.fired and (pygame.time.get_ticks()- self.last_shot) >= self.shot_cooldown:
                # attack handeler
                if self.weapon == 'wooden_spear' or self.weapon == 'spear' or self.weapon == 'extended_sickle' or self.weapon == 'guard_spear':
                    self.swing = True
                    self.fired = True
                    self.last_shot = pygame.time.get_ticks()
                    self.attack_cooldown = pygame.time.get_ticks()
                    self.attacks = 4
                    self.assets["sound"].play()
                else:
                    self.stab = True
                    self.do_stab_once = True
                    self.fired = True
                    self.last_shot = pygame.time.get_ticks()
                    self.assets["sound"].play()  
            
            # swing attack handler
            if self.swing:
                if pygame.time.get_ticks()- self.attack_cooldown >= 200 and self.attacks > 0:
                    damage, damage_pos = self.attack(enemy_list)
                    self.attack_cooldown = pygame.time.get_ticks()
                    self.attacks -= 1
              
            # stab attack handler      
            if self.stab:
                original_rect = pygame.rect.Rect(player.rect.x, player.rect.y, 16, 32)
                if self.do_stab_once:
                    if self.flip:
                        self.rect = pygame.rect.Rect(original_rect.left - 64, original_rect.y + 8, 64, 16)
                        self.animate_x = -16
                        self.image_to_show = pygame.transform.scale(self.image_to_show, (64, 32))
                        damage, damage_pos = self.attack(enemy_list)
                        self.do_stab_once = False
                        self.animate_cooldown = pygame.time.get_ticks()
                    else:
                        self.rect = pygame.rect.Rect(original_rect.right, original_rect.y + 8, 64, 16)
                        self.animate_x = 16
                        self.image_to_show = pygame.transform.scale(self.image_to_show, (64, 32))
                        damage, damage_pos = self.attack(enemy_list)
                        self.do_stab_once = False
                        self.animate_cooldown = pygame.time.get_ticks()
                if pygame.time.get_ticks() - self.animate_cooldown >= 100:
                    self.rect = pygame.rect.Rect(player.rect.x, player.rect.y, 16, 32)
                    self.animate_x = 0
                    if self.flip:
                        self.image_to_show = pygame.transform.rotate(self.original_image, 90)
                    else:
                        self.image_to_show = pygame.transform.rotate(self.original_image, -90)
                    self.stab = False
                    
                    

            # reset mouseclick
            if pygame.mouse.get_pressed()[0] == False:
                self.fired = False
        
        return damage, damage_pos, event_key_pressed
    
    
    def attack(self, enemy_list):
        damage = None
        damage_pos = None
        
        # swing attack
        if self.weapon == 'wooden_spear' or self.weapon == 'spear' or self.weapon == 'extended_sickle' or self.weapon == 'guard_spear':
            for enemy in enemy_list:
                if distance(self.rect.centerx, self.rect.centery, enemy.rect.centerx, enemy.rect.centery) <= self.distance and enemy.alive:
                    damage = random.randint(self.min_damage , self.max_damage)
                    damage_pos = enemy.rect
                    enemy.health -= damage
        # stab attack
        else:
            for enemy in enemy_list:
                if self.rect.colliderect(enemy.rect) and enemy.alive:
                    damage = random.randint(self.min_damage , self.max_damage)
                    damage_pos = enemy.rect
                    enemy.health -= damage   
                       
        return damage, damage_pos


    def draw(self, surface):
        if self.show_e_button:
                surface.blit(self.assets['e_key'], (self.rect.x + 8, self.rect.y - 16))
        
        if self.weapon == 'wooden_spear' or self.weapon == 'spear' or self.weapon == 'extended_sickle' or self.weapon == 'guard_spear': 
            surface.blit(self.image_to_show, (self.rect.center[0]-int(self.image_to_show.get_width()/2)-1 + self.animate_x,self.rect.center[1]-int(self.image_to_show.get_height()/2)-12))
        else:
            if self.flip:
                surface.blit(self.image_to_show, (self.rect.center[0]-int(self.image_to_show.get_width()/2)-8 + self.animate_x,self.rect.center[1]-int(self.image_to_show.get_height()/2)))
            else:
                surface.blit(self.image_to_show, (self.rect.center[0]-int(self.image_to_show.get_width()/2)+8 + self.animate_x,self.rect.center[1]-int(self.image_to_show.get_height()/2)))
                
        if scripts.constants.SHOW_HITBOX:
            pygame.draw.rect(surface, scripts.constants.RED, self.rect, 1)