import pygame
import scripts.constants
import math
import random
from scripts.load import loadImages
from scripts.weapon import Magicball
 
class Enemy():
    def __init__(self, type , x, y, health):
        self.type = type
        self.rect = pygame.Rect(8,8,16,16)
        self.rect.center = (x,y)
        self.animation_index = [["run",0],
                                ["dead",0],
                                ["idle",0],
                                ["heal",0],
                                ["attack",0]]
        if self.type == 'slime':
            self.assets = {
            "slime_run": loadImages("char/slime/idle,walk,hit"),
            "slime_dead": loadImages("char/slime/dead"),
            "orc_hit_sound": pygame.mixer.Sound("assets/audio/orcHit.mp3")
            }
            self.attack = False
            self.damage = 8
            self.image_to_show = self.assets["slime_run"][math.floor(self.animation_index[0][1])]
        elif self.type == 'wolf':
            self.assets = {
            "wolf_run": loadImages("char/wolf/walk"),
            "wolf_dead": loadImages("char/wolf/dead"),
            "wolf_attact": loadImages("char/wolf/attack"),
            "orc_hit_sound": pygame.mixer.Sound("assets/audio/orcHit.mp3")
            }
            self.image_to_show = self.assets["wolf_run"][math.floor(self.animation_index[0][1])]
            self.damage = 15
            self.attack = False
        elif self.type == 'troll':
            self.assets = {
            "troll_run": loadImages("char/troll/walk"),
            "troll_dead": loadImages("char/troll/dead"),
            "troll_attact": loadImages("char/troll/attack"),
            "troll_idle": loadImages("char/troll/idle"),
            "orc_hit_sound": pygame.mixer.Sound("assets/audio/orcHit.mp3")
            }
            self.image_to_show = self.assets["troll_run"][math.floor(self.animation_index[0][1])]
            self.damage = 0
            self.trigger_magic_ball = False
            self.attack = False
        
        elif self.type == 'slime_fire_wizard':
            self.assets={
            "slime_fire_wizard_run": loadImages("char/slime_fire_wizard/walk,idle"),
            "slime_fire_wizard_hit": loadImages("char/slime_fire_wizard/attack"),
            "slime_fire_wizard_dead": loadImages("char/slime_fire_wizard/dead"),
            "orc_hit_sound": pygame.mixer.Sound("assets/audio/orcHit.mp3")
            }
            self.image_to_show = self.assets["slime_fire_wizard_run"][math.floor(self.animation_index[0][1])]
            self.damage = 25
            self.name = "SLIME WIZARD"
            self.fireball_trigger = pygame.time.get_ticks()
            self.rect = pygame.Rect(32,32,48,48)
            self.rect.center = (x,y)
            self.attack = False
            
        elif self.type == 'goblin':
            self.assets = {
            "goblin_run": loadImages("char/goblin/walk"),
            "goblin_dead": loadImages("char/goblin/dead"),
            "goblin_attact": loadImages("char/goblin/attack"),
            "orc_hit_sound": pygame.mixer.Sound("assets/audio/orcHit.mp3")
            }
            self.image_to_show = self.assets["goblin_run"][math.floor(self.animation_index[0][1])]
            self.damage = 12
            self.attack = False
            
        elif self.type == 'ent':
            self.assets = {
            "ent_idle": loadImages("char/ent/idle"),
            "ent_dead": loadImages("char/ent/dead"),
            "ent_attack": loadImages("char/ent/attack"),
            "orc_hit_sound": pygame.mixer.Sound("assets/audio/orcHit.mp3")
            }
            self.time = pygame.time.get_ticks()
            self.image_to_show = self.assets["ent_idle"][math.floor(self.animation_index[0][1])]
            self.damage = 0
            self.attack = False
            self.image_to_show_attack = self.assets["ent_attack"][math.floor(self.animation_index[4][1])]
        self.assets["orc_hit_sound"].set_volume(scripts.constants.FX_VOLUME)
        self.health = health
        self.max_health = health
        self.alive = True
        self.delete = False
        self.dead_counter = 0
        self.randgold = random.randint(0,100)
        self.randpotion = random.randint(0,100)
        self.last_hit = pygame.time.get_ticks()
        self.move_clock = pygame.time.get_ticks()
        self.is_fliped = False
        self.dx = 0
        self.dy = 0
        self.chaise = False
        self.line_of_sight = 0
        self.dead_counter = 0
        self.wander_timer = 0
        self.walk_left = False
        self.walk_right = True
        self.walk_up = False
        self.walk_down = False
        self.change_direction = 0
        self.stunned = False
        self.dist = None
        
    def magic_ball(self, player):
        if self.type == 'slime_fire_wizard':
            return Magicball("fireball",self.rect.centerx,self.rect.centery, player.rect.centerx, player.rect.centery)
        if self.type == 'troll':
            return Magicball("troll_rock",self.rect.centerx,self.rect.centery, player.rect.centerx, player.rect.centery)
        if self.type == 'ent':
            return Magicball("attack_ent",self.rect.centerx,self.rect.centery, player.rect.centerx, player.rect.centery)
            

    def move(self, obstacle_tile, player, screen_scroll):
       # reposition depending on screen_scroll
        self.rect.x += screen_scroll[0]
        self.rect.y += screen_scroll[1]
        magicball = None
        
            
        if self.alive:
            if not self.chaise and self.on_screen():
                if not self.type == 'ent':
                    # reset values
                    self.dx = 0
                    self.dy = 0
                    colision_x = False
                    colision_y = False

                    if self.type == 'troll':
                        
                        if pygame.time.get_ticks() - self.move_clock > 5000:
                            self.move_clock = pygame.time.get_ticks()
                            if self.stunned:
                                self.stunned = False
                            else:
                                self.stunned = True
                        
                    if self.walk_left:
                        self.dx = -scripts.constants.SLIME_SPEED
                        self.is_fliped = False
                    if self.walk_right:
                        self.dx = scripts.constants.SLIME_SPEED
                        self.is_fliped = True
                    if self.walk_down:
                        self.dy = scripts.constants.SLIME_SPEED
                    if self.walk_up:
                        self.dy = -scripts.constants.SLIME_SPEED

                    # update x position
                    if not self.stunned:
                        self.rect.x += self.dx
                        old_x = self.rect.x - self.dx

                    # checking colision x
                    for obstacle in obstacle_tile:
                        if obstacle[1].colliderect(self.rect):
                            colision_x = True
                            # checking from which side is collision
                            if self.dx > 0:
                                self.rect.x = old_x
                            if self.dx < 0:
                                self.rect.x = old_x

                    # update y position       
                    if not self.stunned:
                        self.rect.y += self.dy
                        old_y = self.rect.y - self.dy

                    # checking colision y
                    for obstacle in obstacle_tile:
                        if obstacle[1].colliderect(self.rect):
                            colision_y = True
                            # checking from which side is collision
                            if self.dy > 0:
                                self.rect.y = old_y
                            if self.dy < 0:
                                self.rect.y = old_y

                    # if collison or 5 second change diretion of moving
                    if colision_x or colision_y or pygame.time.get_ticks() > self.wander_timer:
                        self.walk_down = False
                        self.walk_up = False
                        self.walk_left = False
                        self.walk_right = False
                        self.change_direction = random.randint(0, 3)
                        if self.change_direction == 0:
                            self.walk_down = True
                        elif self.change_direction == 1:
                            self.walk_up = True
                        elif self.change_direction == 2:
                            self.walk_left = True
                        elif self.change_direction == 3:
                            self.walk_right = True
                        self.wander_timer = pygame.time.get_ticks() + 5000

            if self.chaise:
                
                # reset values
                self.dx = 0
                self.dy = 0

                if self.type == 'slime' or self.type == 'slime_fire_wizard':
                    if self.rect.centerx > player.rect.centerx:
                        self.dx = -scripts.constants.SLIME_SPEED
                        self.is_fliped = False
                    if self.rect.centerx < player.rect.centerx:
                        self.dx = scripts.constants.SLIME_SPEED
                        self.is_fliped = True
                    if self.rect.centery > player.rect.centery:
                        self.dy = -scripts.constants.SLIME_SPEED
                    if self.rect.centery < player.rect.centery:
                        self.dy = scripts.constants.SLIME_SPEED
                
                elif self.type == 'wolf':
                    if self.rect.centerx > player.rect.centerx:
                        self.dx = -3* scripts.constants.SLIME_SPEED
                        self.is_fliped = False
                    if self.rect.centerx < player.rect.centerx:
                        self.dx = 3* scripts.constants.SLIME_SPEED
                        self.is_fliped = True
                    if self.rect.centery > player.rect.centery:
                        self.dy = -3* scripts.constants.SLIME_SPEED
                    if self.rect.centery < player.rect.centery:
                        self.dy = 3*scripts.constants.SLIME_SPEED
                
                elif self.type == 'troll':
                    if not self.attack:
                        
                        if self.rect.centerx + 1 > player.rect.centerx:
                            if self.rect.centerx + 1 > player.rect.centerx + scripts.constants.TROLL_AIM_RANGE:
                                self.dx = -scripts.constants.SLIME_SPEED
                                self.is_fliped = False  
                            else:
                                self.dx = scripts.constants.SLIME_SPEED
                                self.trigger_magic_ball = True
                                self.attack = True
                                self.is_fliped = False                                                    
                        if self.rect.centerx - 1 < player.rect.centerx:
                            if self.rect.centerx - 1 < player.rect.centerx - scripts.constants.TROLL_AIM_RANGE:
                                self.dx =  scripts.constants.SLIME_SPEED
                                self.is_fliped = True 
                            else:
                                self.dx = -scripts.constants.SLIME_SPEED
                                self.trigger_magic_ball = True
                                self.attack = True   
                                self.is_fliped = True
                        if self.rect.centery + 1 > player.rect.centery:
                            if self.rect.centery + 1 < player.rect.centery + scripts.constants.TROLL_AIM_RANGE:
                                 self.dy = -scripts.constants.SLIME_SPEED
                            else:
                                self.dy = scripts.constants.SLIME_SPEED
                                self.trigger_magic_ball = True
                                self.attack = True
                        if self.rect.centery - 1 < player.rect.centery:
                            if self.rect.centery - 1 < player.rect.centery + scripts.constants.TROLL_AIM_RANGE:
                                self.dy = scripts.constants.SLIME_SPEED
                            else:
                                self.dy = -scripts.constants.SLIME_SPEED
                                self.attack = True 
    
                    elif self.attack:
                        if self.animation_index[4][1] >= 8:
                            magicball = self.magic_ball(player)
                            self.attack = False
                            self.animation_index[4][1] = 0
                
                elif self.type == 'goblin':
                    if self.rect.centerx > player.rect.centerx:
                        self.dx = -scripts.constants.SLIME_SPEED
                        self.is_fliped = False
                    if self.rect.centerx < player.rect.centerx:
                        self.dx = scripts.constants.SLIME_SPEED
                        self.is_fliped = True
                    if self.rect.centery > player.rect.centery:
                        self.dy = -scripts.constants.SLIME_SPEED
                    if self.rect.centery < player.rect.centery:
                        self.dy = scripts.constants.SLIME_SPEED
                        
                    if self.rect.colliderect(player.rect):
                        self.attack = True
                    else:
                        self.attack = False
                        
                elif self.type == 'ent':
                    if pygame.time.get_ticks() - self.time >= 5000:
                        self.attack = True
                        self.trigger_magic_ball = True
                    
                    if self.attack:
                        if self.trigger_magic_ball:
                            magicball = self.magic_ball(player)
                            self.trigger_magic_ball = False
                            self.time = pygame.time.get_ticks()
                    
                
                    
                    
                    
                
                elif self.type == 'slime_fire_wizard':
                    actuall_time = pygame.time.get_ticks()
                
                    if actuall_time - self.fireball_trigger >= 5000:
                        self.stunned = True
                        if self.is_fliped:
                            self.image_to_show = pygame.transform.flip(self.assets["slime_fire_wizard_hit"][math.floor(self.animation_index[1][1])],True,False)
                        elif not self.is_fliped:
                            self.image_to_show = self.assets["slime_fire_wizard_hit"][math.floor(self.animation_index[1][1])]
                        self.animation_index[1][1] += 0.1
                        if self.animation_index[1][1] >= 4:
                            self.fireball_trigger = actuall_time
                            magicball = self.fireball(player)
                            self.animation_index[1][1] = 0
                            self.stunned = False
    

                # update x position
                if not self.stunned:
                    self.rect.x += self.dx

                # checking colision x
                for obstacle in obstacle_tile:
                    if obstacle[1].colliderect(self.rect):
                        # checking from which side is collision
                        if self.dx > 0:
                            self.rect.right = obstacle[1].left - 1
                        if self.dx < 0:
                            self.rect.left = obstacle[1].right + 1

                # update y position
                if not self.stunned:
                    self.rect.y += self.dy

                # checking colision y
                for obstacle in obstacle_tile:
                    if obstacle[1].colliderect(self.rect):
                        # checking from which side is collision
                        if self.dy > 0:
                            self.rect.bottom = obstacle[1].top - 1
                        if self.dy < 0:
                            self.rect.top = obstacle[1].bottom + 1
        return magicball

    def on_screen(self):
        return -25 <= self.rect.right <= scripts.constants.DISPLAY_WIDTH + 25 and -25 <= self.rect.bottom <= scripts.constants.DISPLAY_HEIGHT +25

    
        


    def update(self, player, obstacle_tile):
        # reset values
        gold = False
        health_potion = False
        self.alive = True
        clipped_line = None
        show_hp = False
        
        if self.alive:
            # check if mob has died
            if self.health <= 0:
                self.health = 0
                self.alive = False
            
            # handle animation
            # walk 
            if self.type == 'slime' or self.type == 'troll' or self.type == 'goblin' or self.type == 'ent' or self.type == 'slime_fire_wizard':
                if self.type == 'slime':
                    self.image_to_show = self.assets["slime_run"][math.floor(self.animation_index[0][1])]
                    self.animation_index[0][1] += 0.1
                    if self.animation_index[0][1] >= 13:
                        self.animation_index[0][1] = 0
                
                elif self.type == 'slime_fire_wizard':
                    self.image_to_show = self.assets["slime_fire_wizard_run"][math.floor(self.animation_index[0][1])]
                    self.animation_index[0][1] += 0.1
                    if self.animation_index[0][1] >= 9.4:
                        self.animation_index[0][1] = 0
                    
                    if self.chaise:
                        show_hp = True
                        
                
                elif self.type == 'goblin':
                    if not self.attack:
                        if not self.is_fliped:
                            self.image_to_show = self.assets["goblin_run"][math.floor(self.animation_index[0][1])]
                            self.animation_index[0][1] += 0.1
                            if self.animation_index[0][1] >= 3:
                                self.animation_index[0][1] = 0
                        else:
                            self.image_to_show = pygame.transform.flip(self.assets["goblin_run"][math.floor(self.animation_index[0][1])],True,False)
                            self.animation_index[0][1] += 0.1
                            if self.animation_index[0][1] >= 3:
                                self.animation_index[0][1] = 0
                    else:
                        if not self.is_fliped:
                            self.image_to_show = self.assets["goblin_attact"][math.floor(self.animation_index[4][1])]
                            self.animation_index[4][1] += 0.1
                            if self.animation_index[4][1] >= 3:
                                self.animation_index[4][1] = 0
                        else:
                            self.image_to_show = pygame.transform.flip(self.assets["goblin_attact"][math.floor(self.animation_index[4][1])],True,False)
                            self.animation_index[4][1] += 0.1
                            if self.animation_index[4][1] >= 3:
                                self.animation_index[4][1] = 0
                
                elif self.type == 'troll':
                    if not self.stunned:

                        if self.attack:
                            if not self.is_fliped:
                                self.image_to_show = self.assets["troll_attact"][math.floor(self.animation_index[4][1])]
                                self.animation_index[4][1] += 0.1
                                if self.animation_index[4][1] >= 8.4:
                                    self.animation_index[4][1] = 8
                            else:
                                self.image_to_show = pygame.transform.flip(self.assets["troll_attact"][math.floor(self.animation_index[4][1])],True,False)
                                self.animation_index[4][1] += 0.1
                                if self.animation_index[4][1] >= 8.4:
                                    self.animation_index[4][1] = 8
                        else:
                            if not self.is_fliped:
                                self.image_to_show = self.assets["troll_run"][math.floor(self.animation_index[0][1])]
                                self.animation_index[0][1] += 0.1
                                if self.animation_index[0][1] >= 6:
                                    self.animation_index[0][1] = 0
                            else:
                                self.image_to_show = pygame.transform.flip(self.assets["troll_run"][math.floor(self.animation_index[0][1])], True, False)
                                self.animation_index[0][1] += 0.1
                                if self.animation_index[0][1] >= 6:
                                    self.animation_index[0][1] = 0
                    else:
                        if not self.is_fliped:
                            self.image_to_show = self.assets["troll_idle"][math.floor(self.animation_index[2][1])]
                            self.animation_index[2][1] += 0.05
                            if self.animation_index[2][1] >= 1.4:
                                self.animation_index[2][1] = 0
                
                elif self.type == 'ent':
                    if self.attack:
                        self.image_to_show_attack = self.assets["ent_attack"][math.floor(self.animation_index[4][1])]
                        self.animation_index[4][1] += 0.05
                        if self.animation_index[4][1] >= 3.4:
                            self.animation_index[4][1] = 0
                            self.attack = False
                        
            else:
                if self.chaise:
                    if self.type == 'wolf':
                        if not self.is_fliped:
                            self.image_to_show = self.assets["wolf_attact"][math.floor(self.animation_index[0][1])]
                            self.animation_index[0][1] += 0.1
                            if self.animation_index[0][1] >= 3:
                                self.animation_index[0][1] = 0
                        else:
                            self.image_to_show = pygame.transform.flip(self.assets["wolf_attact"][math.floor(self.animation_index[0][1])], True, False)
                            self.animation_index[0][1] += 0.1
                            if self.animation_index[0][1] >= 3:
                                self.animation_index[0][1] = 0
                            
                
                else:  
                    if self.type == 'wolf':
                        if not self.is_fliped:
                            self.image_to_show = self.assets["wolf_run"][math.floor(self.animation_index[0][1])]
                            self.animation_index[0][1] += 0.1
                            if self.animation_index[0][1] >= 3:
                                self.animation_index[0][1] = 0
                        else:
                            self.image_to_show = pygame.transform.flip(self.assets["wolf_run"][math.floor(self.animation_index[0][1])], True, False)
                            self.animation_index[0][1] += 0.1
                            if self.animation_index[0][1] >= 3:
                                self.animation_index[0][1] = 0

            
            
            if self.health < 0:
                self.alive = False
            # create a line of sight from enemy to the player
            self.line_of_sight = ((self.rect.centerx, self.rect.centery), (player.rect.centerx, player.rect.centery))
            # check if line of sight passes through an obstacle tile
            for obstacle in obstacle_tile:
                if obstacle[1].clipline(self.line_of_sight):
                    clipped_line = obstacle[1].clipline(self.line_of_sight)
            self.dist = math.sqrt(((self.rect.centerx - player.rect.centerx)**2)+((self.rect.centery-player.rect.centery)**2))
            # check if chaise
            if not clipped_line:
                if self.type == 'slime':
                    if self.dist <= scripts.constants.SLIME_RANGE or self.health < 0.9*self.max_health:
                        self.chaise = True
                        self.stunned = False
                elif self.type == 'wolf':
                    if self.dist <= scripts.constants.WOLF_RANGE or self.health < 0.9*self.max_health:
                        self.chaise = True
                        self.stunned = False
                elif self.type == 'troll':
                    if self.dist <= scripts.constants.TROLL_RANGE or self.health < 0.9*self.max_health:
                        self.chaise = True
                        self.stunned = False
                elif self.type == 'goblin':
                    if self.dist <= scripts.constants.GOBLIN_RANGE or self.health < 0.9*self.max_health:
                        self.chaise = True
                        self.stunned = False
                elif self.type == 'ent':
                    if self.dist <= scripts.constants.ENT_RANGE or self.health < 0.9*self.max_health:
                        self.chaise = True
                        self.stunned = False
                elif self.type == 'slime_fire_wizard':
                    if self.dist <= scripts.constants.SLIME_FIRE_WIZARD_RANGE or self.health < 0.9*self.max_health:
                        self.chaise = True
                        self.stunned = False
        # when not alive
        if not self.alive:
            if self.randgold <= 50:
                gold = True
            if self.randpotion <= 10:
                health_potion = True
            
            if self.type == 'slime':
                self.image_to_show = self.assets["slime_dead"][math.floor(self.animation_index[1][1])]
                self.animation_index[1][1] += 0.05
                if self.animation_index[1][1] >= 8:
                    self.animation_index[1][1] = 8
                    self.dead_counter += 1
                if self.dead_counter > 30:
                    self.delete = True
                    
            elif self.type == 'slime_fire_wizard':
                self.image_to_show = self.assets["slime_fire_wizard_dead"][math.floor(self.animation_index[1][1])]
                self.animation_index[1][1] += 0.05
                if self.animation_index[1][1] >= 7.4:
                    self.animation_index[1][1] = 7
                    self.dead_counter += 1
                if self.dead_counter > 30:
                    self.delete = True
            elif self.type == 'wolf':
                self.image_to_show = self.assets["wolf_dead"][math.floor(self.animation_index[1][1])]
                self.animation_index[1][1] += 0.05
                if self.animation_index[1][1] >= 2:
                    self.animation_index[1][1] = 2
                    self.dead_counter += 1
                if self.dead_counter > 30:
                    self.delete = True
            
            elif self.type == 'troll':
                self.image_to_show = self.assets["troll_dead"][math.floor(self.animation_index[1][1])]
                self.animation_index[1][1] += 0.05
                if self.animation_index[1][1] >= 2:
                    self.animation_index[1][1] = 2
                    self.dead_counter += 1
                if self.dead_counter > 30:
                    self.delete = True
                    
            elif self.type == 'goblin':
                self.image_to_show = self.assets["goblin_dead"][math.floor(self.animation_index[1][1])]
                self.animation_index[1][1] += 0.05
                if self.animation_index[1][1] >= 3:
                    self.animation_index[1][1] = 3
                    self.dead_counter += 1
                if self.dead_counter > 30:
                    self.delete = True
            
            elif self.type == 'ent':
                self.image_to_show = self.assets["ent_dead"][math.floor(self.animation_index[1][1])]
                self.animation_index[1][1] += 0.05
                if self.animation_index[1][1] >= 8:
                    self.animation_index[1][1] = 8
                    self.dead_counter += 1
                if self.dead_counter > 30:
                    self.delete = True
                    
        return gold, health_potion, self.alive, show_hp

                 

    def hit_player(self, damage, player):
        counter = 1000
        if self.alive:
            if self.rect.colliderect(player.rect) and (pygame.time.get_ticks()-self.last_hit) >= counter:
                self.assets["orc_hit_sound"].play()
                player.old_health = player.health
                player.player_was_hit = True
                player.health -= damage
                self.last_hit = pygame.time.get_ticks()

    def change_fx_volume(self):
        self.assets["orc_hit_sound"].set_volume(scripts.constants.FX_VOLUME)
                    
    def draw(self, surface):
            if not self.type == 'slime_fire_wizard':
                surface.blit(self.image_to_show, (self.rect.center[0]-16,self.rect.center[1]-20))
            else: 
                surface.blit(self.image_to_show, (self.rect.center[0]-32,self.rect.center[1]-42))
                
            if self.type == 'ent':
                if self.attack:
                    surface.blit(self.image_to_show_attack, (self.rect.center[0]-16,self.rect.center[1]-20))
            if scripts.constants.SHOW_HITBOX:
                pygame.draw.rect(surface, scripts.constants.RED, self.rect, 1)
            if scripts.constants.SHOW_LINE_OF_SIGHT and not self.chaise:
                pygame.draw.line(surface, scripts.constants.WHITE, self.line_of_sight[0], self.line_of_sight[1])
            elif scripts.constants.SHOW_LINE_OF_SIGHT and self.chaise:
                pygame.draw.line(surface, scripts.constants.RED, self.line_of_sight[0], self.line_of_sight[1])
  
        
        

                    