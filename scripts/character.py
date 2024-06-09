import pygame
import scripts.constants
import math
from scripts.load import loadImages
import random

class Character():
    def __init__(self, x, y, health, type, max_idle_animation, max_run_animation, max_dead_animation):
        self.type = type
        self.rect = pygame.Rect(0,0,16,30)
        self.rect.center = (x,y)
        self.image_to_show = 0
        self.animation_index = [["idle",0],
                                ["run",0],
                                ["dead",0],
                                ["onFire",0]]
        self.max_idle_animation = max_idle_animation
        self.max_run_animation = max_run_animation
        self.max_dead_animation = max_dead_animation
        self.assets = {
        "player_idle": loadImages(f"char/{self.type}/idle"),
        "player_run": loadImages(f"char/{self.type}/run"),
        "player_dead": loadImages(f"char/{self.type}/dead"),
        "player_on_fire": loadImages("effects/onFire"),
        "walk_sound": pygame.mixer.Sound("assets/audio/walk.mp3"),
        'died_sound': pygame.mixer.Sound("assets/audio/died.wav")
        }
        self.assets["walk_sound"].set_volume(scripts.constants.FX_VOLUME)
        self.assets["died_sound"].set_volume(scripts.constants.FX_VOLUME)
        self.play_died_sound_once = True
        self.health = health
        self.old_health = health
        self.new_health = health
        self.health_max = scripts.constants.PLAYER_HP
        self.alive = True
        self.gold = 0
        self.died_counter = 0
        self.sound_counter = pygame.time.get_ticks()
        self.is_on_fire = False
        self.image_on_fire = self.assets["player_on_fire"][0]
        self.on_fire_counter = pygame.time.get_ticks()
        self.on_fire_counter_end = pygame.time.get_ticks()
        self.player_was_hit = False
        self.player_was_heal = False
        self.level = 1
        self.current_experience = 0
        self.experience_to_gain_new_level = 25
        self.on_fire_time = None
        self.on_fire_tics = None
        self.fire_damage = None
        self.on_fire_damage_cooldown = None
        self.on_fire_how_long = None
        self.is_on_fire = False
        self.minimal_damage_multiplied = 1
        self.maximal_damage_multiplied = 1
        self.hud_experience_bar_refresh = False

   
    def move(self, dx, dy, obstacle_tile):
        # screen scroll

        screen_scroll = [0,0]
        if self.alive:
            # sound walk handler
            current_time = pygame.time.get_ticks()
            if current_time - self.sound_counter >= 500:
                if dx > 0 :
                    self.assets["walk_sound"].play()
                elif dx < 0:
                    self.assets["walk_sound"].play()
                if dy > 0:
                    self.assets["walk_sound"].play()
                elif dy < 0:
                    self.assets["walk_sound"].play()
                self.sound_counter = current_time
            # move camera left right
            if self.rect.right > (scripts.constants.DISPLAY_WIDTH - scripts.constants.SCROLL_THRESH_X):
                screen_scroll[0] = (scripts.constants.DISPLAY_WIDTH - scripts.constants.SCROLL_THRESH_X) - self.rect.right
                self.rect.right = scripts.constants.DISPLAY_WIDTH - scripts.constants.SCROLL_THRESH_X
            if self.rect.left < scripts.constants.SCROLL_THRESH_X:
                screen_scroll[0] = scripts.constants.SCROLL_THRESH_X - self.rect.left
                self.rect.left = scripts.constants.SCROLL_THRESH_X
            # move camera up down
            if self.rect.bottom > (scripts.constants.DISPLAY_HEIGHT - scripts.constants.SCROLL_THRESH_Y):
                screen_scroll[1] = (scripts.constants.DISPLAY_HEIGHT - scripts.constants.SCROLL_THRESH_Y) - self.rect.bottom
                self.rect.bottom = scripts.constants.DISPLAY_HEIGHT - scripts.constants.SCROLL_THRESH_Y 
            if self.rect.top < scripts.constants.SCROLL_THRESH_Y:
                screen_scroll[1] = scripts.constants.SCROLL_THRESH_Y - self.rect.top
                self.rect.top = scripts.constants.SCROLL_THRESH_Y 
            # control diagonal speed
            if dx != 0 and dy != 0:
                dx = dx * (math.sqrt(2)/2)
                dy = dy * (math.sqrt(2)/2)
            self.rect.x += dx 
            old_dx = self.rect.x - dx 
            # check for collision x
            for obstacle in obstacle_tile:
                if obstacle[1].colliderect(self.rect):
                    # check which side the collision is from
                    if dx > 0:
                        self.rect.x = old_dx - 1
                    if dx < 0:
                        self.rect.x = old_dx + 1
            self.rect.y += dy
            old_dy = self.rect.y - dy
            # check for collision y
            for obstacle in obstacle_tile:
                if obstacle[1].colliderect(self.rect):
                    # check which side the collision is from
                    if dy > 0:
                        self.rect.y = old_dy - 1
                    if dy < 0:
                        self.rect.y = old_dy + 1
        return screen_scroll

    def update(self, flip, moving, health, gold, hud, delta_time):
        level_up = False
        if self.alive:
            #print (str(self.current_experience) + '-' + str(self.experience_to_gain_new_level) + ' | ' + str(self.level))
            
            # handle animation
            # update image
            if not moving and not flip:
                self.image_to_show = self.assets["player_idle"][math.floor(self.animation_index[0][1])]
                self.animation_index[0][1] += 0.1 * delta_time
                if self.animation_index[0][1] >= self.max_idle_animation:
                    self.animation_index[0][1] = 0
            if not moving and flip:
                self.image_to_show = pygame.transform.flip(self.assets["player_idle"][math.floor(self.animation_index[0][1])],True,False)
                self.animation_index[0][1] += 0.1 * delta_time
                if self.animation_index[0][1] >= self.max_idle_animation:
                    self.animation_index[0][1] = 0
            if moving and flip:
                self.image_to_show = pygame.transform.flip(self.assets["player_run"][math.floor(self.animation_index[1][1])],True,False)
                self.animation_index[1][1] += 0.1 * delta_time
                if self.animation_index[1][1] >= self.max_run_animation:
                    self.animation_index[1][1] = 0
            if moving and not flip:
                self.image_to_show = self.assets["player_run"][math.floor(self.animation_index[1][1])]
                self.animation_index[1][1] += 0.1 * delta_time
                if self.animation_index[1][1] >= self.max_run_animation:
                    self.animation_index[1][1] = 0
            # health update
            self.health = health
            if self.player_was_hit:
                if self.old_health <= self.health:
                    self.player_was_hit = False
                else:
                    self.old_health -= 0.1 * delta_time
            if self.player_was_heal:
                if self.health >= self.new_health:
                    self.health = self.new_health
                    self.player_was_heal = False
                else:
                    self.health += 1 * delta_time
            else:
                self.new_health = health
            # gold update
            self.gold = gold
            
            # experience handlerer
            if self.current_experience >= self.experience_to_gain_new_level:
                self.level += 1
                level_up = True
                self.current_experience = self.current_experience - self.experience_to_gain_new_level
                if self.current_experience <= 0:
                    self.current_experience = 0
                self.experience_to_gain_new_level *= 2
            
            if self.hud_experience_bar_refresh:
                hud.update_experience_bar(self)
                self.hud_experience_bar_refresh = False
                
                 
            # is on fire?
            if self.is_on_fire:
                self.on_fire()
            
            # is alive?
            if self.health <= 0:
                self.alive = False
        else: 
            if not flip:
                self.image_to_show = self.assets["player_dead"][math.floor(self.animation_index[2][1])]
                self.animation_index[2][1] += 0.05 * delta_time
                if self.animation_index[2][1] >= self.max_dead_animation:
                    self.animation_index[2][1] = self.max_dead_animation
            else:
                self.image_to_show = pygame.transform.flip(self.assets["player_dead"][math.floor(self.animation_index[2][1])],True,False)
                self.animation_index[2][1] += 0.05 * delta_time
                if self.animation_index[2][1] >= self.max_dead_animation:
                    self.animation_index[2][1] = self.max_dead_animation
                
            hud.healthbar_boss.set_show(False)
            
            if self.play_died_sound_once:
                self.assets['died_sound'].play()
                self.play_died_sound_once = False
        return level_up


    def died(self, delta_time):
        end = False
        self.died_counter += 1 * delta_time
        if self.died_counter > 10000:
            end = True
            self.play_died_sound_once = True
        return end
    
    
    def change_fx_volume(self):
        self.assets["walk_sound"].set_volume(scripts.constants.FX_VOLUME)
        self.assets["died_sound"].set_volume(scripts.constants.FX_VOLUME)
        

    def add_experience(self, experience_points):
        self.current_experience += experience_points
        self.hud_experience_bar_refresh = True
        
        
    def on_fire_trigger(self, damage, time, tics):
        self.on_fire_time = pygame.time.get_ticks()
        self.on_fire_tics = tics
        self.fire_damage = damage
        self.on_fire_damage_cooldown = pygame.time.get_ticks()
        self.on_fire_how_long = time
        self.is_on_fire = True
        
    def on_fire(self):
        
        if self.is_on_fire:
            # handle animation
            self.image_on_fire = self.assets["player_on_fire"][math.floor(self.animation_index[3][1])]
            self.animation_index[3][1] += 0.2 
            if self.animation_index[3][1] >= 3:
                self.animation_index[3][1] = 0
            if pygame.time.get_ticks() - self.on_fire_counter_end >= 50000:
                self.is_on_fire = False
                self.on_fire_counter_end = pygame.time.get_ticks()
                self.on_fire_counter = pygame.time.get_ticks()
                
            if pygame.time.get_ticks() - self.on_fire_damage_cooldown >= self.on_fire_tics * 1000:
                self.health -= self.fire_damage
                self.on_fire_damage_cooldown = pygame.time.get_ticks()
                
            if pygame.time.get_ticks() - self.on_fire_time >= self.on_fire_how_long * 1000:
                self.is_on_fire = False


    def draw(self, surface):
            surface.blit(self.image_to_show, (self.rect.center[0]-16,self.rect.center[1]-18))
            if self.is_on_fire:
               surface.blit(self.image_on_fire, (self.rect.center[0]-16,self.rect.center[1]-18)) 
            if scripts.constants.SHOW_HITBOX:
                pygame.draw.rect(surface, scripts.constants.RED, self.rect, 1)
        
        
class Peasant(Character):
    def __init__(self, x, y, health):
        type = 'player1'
        super().__init__(x, y, health, type, 4,3,5)
        
class Wizard(Character):
    def __init__(self, x, y, health):
        type = 'wizard'
        super().__init__(x, y, health, type, 3,3,6)
        
class Dwarf(Character):
    def __init__(self, x, y, health):
        type = 'dwarf'
        super().__init__(x, y, health, type, 3, 3, 3)

class Knight(Character):
    def __init__(self, x, y, health):
        type = 'knight'
        super().__init__(x, y, health, type, 3, 3, 3)

class Pikemen(Character):
    def __init__(self, x, y, health):
        type = 'pikemen'
        super().__init__(x, y, health, type, 3, 3, 3)

class Elf(Character):
    def __init__(self, x, y, health):
        type = 'elf'
        super().__init__(x, y, health, type, 3, 3, 3)

class Paladin(Character):
    def __init__(self, x, y, health):
        type = 'paladin'
        super().__init__(x, y, health, type, 3, 3, 3)

class Druid(Character):
    def __init__(self, x, y, health):
        type = 'druid'
        super().__init__(x, y, health, type, 3, 3, 3)
               