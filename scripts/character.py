import pygame
import scripts.constants
import math
from scripts.load import loadImages
import random

class Character():
    def __init__(self, x, y, health):
        self.rect = pygame.Rect(0,0,16,30)
        self.rect.center = (x,y)
        self.image_to_show = 0
        self.animation_index = [["idle",0], ["run",0], ["dead",0], ["onFire",0]]
        self.assets = {
        "player_idle": loadImages("char/player1/idle"),
        "player_run": loadImages("char/player1/run"),
        "player_dead": loadImages("char/player1/dead"),
        "player_on_fire": loadImages("effects/onFire"),
        "walk_sound": pygame.mixer.Sound("assets/audio/walk.mp3")
        }
        self.assets["walk_sound"].set_volume(scripts.constants.FX_VOLUME)
        self.health = health
        self.health_max = scripts.constants.PLAYER_HP
        self.alive = True
        self.gold = 0
        self.died_counter = 0
        self.sound_counter = pygame.time.get_ticks()
        self.is_on_fire = False
        self.image_on_fire = self.assets["player_on_fire"][0]
        self.on_fire_counter = pygame.time.get_ticks()
        self.on_fire_counter_end = pygame.time.get_ticks()

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

    def update(self, flip, moving, health, gold):
        if self.alive:
            # handle animation
            # update image
            if not moving and not flip:
                self.image_to_show = self.assets["player_idle"][math.floor(self.animation_index[0][1])]
                self.animation_index[0][1] += 0.1
                if self.animation_index[0][1] >= 4:
                    self.animation_index[0][1] = 0
            if not moving and flip:
                self.image_to_show = pygame.transform.flip(self.assets["player_idle"][math.floor(self.animation_index[0][1])],True,False)
                self.animation_index[0][1] += 0.1
                if self.animation_index[0][1] >= 4:
                    self.animation_index[0][1] = 0
            if moving and flip:
                self.image_to_show = pygame.transform.flip(self.assets["player_run"][math.floor(self.animation_index[1][1])],True,False)
                self.animation_index[1][1] += 0.1
                if self.animation_index[1][1] >= 4:
                    self.animation_index[1][1] = 0
            if moving and not flip:
                self.image_to_show = self.assets["player_run"][math.floor(self.animation_index[1][1])]
                self.animation_index[1][1] += 0.1
                if self.animation_index[1][1] >= 4:
                    self.animation_index[1][1] = 0
        # health update
        self.health = health
        # gold update
        self.gold = gold
        # is alive?
        if self.health <= 0:
            if not flip:
                self.image_to_show = self.assets["player_dead"][math.floor(self.animation_index[2][1])]
                self.animation_index[2][1] += 0.05
                if self.animation_index[2][1] >= 5:
                    self.animation_index[2][1] = 5
            else:
                self.image_to_show = pygame.transform.flip(self.assets["player_dead"][math.floor(self.animation_index[2][1])],True,False)
                self.animation_index[2][1] += 0.05
                if self.animation_index[2][1] >= 5:
                    self.animation_index[2][1] = 5
            self.alive = False

    def died(self):
        end = False
        self.died_counter += 1
        if self.died_counter > 10000:
            end = True
        return end
    
    def change_fx_volume(self):
        self.assets["walk_sound"].set_volume(scripts.constants.FX_VOLUME)

    def on_fire(self):
        self.is_on_fire = True
        if self.is_on_fire:
            # handle animation
            self.image_on_fire = self.assets["player_on_fire"][math.floor(self.animation_index[3][1])]
            self.animation_index[3][1] += 0.2
            if self.animation_index[3][1] >= 11:
                self.animation_index[3][1] = 0
            if pygame.time.get_ticks() - self.on_fire_counter >= 1000:
                damage = random.randint(1,5)
                self.health -= damage
                self.on_fire_counter = pygame.time.get_ticks()
            if pygame.time.get_ticks() - self.on_fire_counter_end >= 50000:
                self.is_on_fire = False
                self.on_fire_counter_end = pygame.time.get_ticks()
                self.on_fire_counter = pygame.time.get_ticks()



    def draw(self, surface):
            surface.blit(self.image_to_show, (self.rect.center[0]-16,self.rect.center[1]-18))
            if self.is_on_fire:
               surface.blit(self.image_on_fire, (self.rect.center[0]-16,self.rect.center[1]-18)) 
            if scripts.constants.SHOW_HITBOX:
                pygame.draw.rect(surface, scripts.constants.RED, self.rect, 1)
        
        
        