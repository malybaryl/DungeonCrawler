import pygame
import scripts.constants
import math
import random
from scripts.load import loadImages
from scripts.weapon import Magicball

class Orc():
    def __init__(self, x, y, health):
        self.rect = pygame.Rect(0,0,16,26)
        self.rect.center = (x,y)
        self.animation_index = [["run",0],["hit",0],["dead",0]]
        self.assets = {
        "orc_run": loadImages("char/orc/run"),
        "orc_hit": loadImages("char/orc/hit"),
        "orc_dead": loadImages("char/orc/dead"),
        "orc_hit_sound": pygame.mixer.Sound("assets/audio/orcHit.mp3")
        }
        self.assets["orc_hit_sound"].set_volume(scripts.constants.FX_VOLUME)
        self.image_to_show = self.assets["orc_run"][math.floor(self.animation_index[0][1])]
        self.health = health
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
        

    def move(self, obstacle_tile, player, screen_scroll):
       # reposition depending on screen_scroll
        self.rect.x += screen_scroll[0]
        self.rect.y += screen_scroll[1]

        if self.alive:
            if not self.chaise and self.on_screen():
                # reset values
                self.dx = 0
                self.dy = 0
                colision_x = False
                colision_y = False

                if self.walk_left:
                    self.dx = -scripts.constants.ORC_SPEED
                if self.walk_right:
                    self.dx = scripts.constants.ORC_SPEED
                if self.walk_down:
                    self.dy = scripts.constants.ORC_SPEED
                if self.walk_up:
                    self.dy = -scripts.constants.ORC_SPEED

                # update x position
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

                if self.rect.centerx > player.rect.centerx:
                    self.dx = -scripts.constants.ORC_SPEED
                if self.rect.centerx < player.rect.centerx:
                    self.dx = scripts.constants.ORC_SPEED
                if self.rect.centery > player.rect.centery:
                    self.dy = -scripts.constants.ORC_SPEED
                if self.rect.centery < player.rect.centery:
                    self.dy = scripts.constants.ORC_SPEED

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

    def on_screen(self):
        return -25 <= self.rect.right <= scripts.constants.DISPLAY_WIDTH + 25 and -25 <= self.rect.bottom <= scripts.constants.DISPLAY_HEIGHT +25



    def update(self, player, obstacle_tile):
        # reset values
        gold = False
        health_potion = False
        self.alive = True
        clipped_line = None
        if self.alive:
            # check if mob has died
            if self.health <= 0:
                self.health = 0
                self.alive = False
            # handle animation
            # update flip direction
            if self.dx > 0:
                self.is_fliped = False
            if self.dx < 0:
                self.is_fliped = True
            # walk right
            if not self.is_fliped:
                self.image_to_show = self.assets["orc_run"][math.floor(self.animation_index[0][1])]
                self.animation_index[0][1] += 0.1
                if self.animation_index[0][1] >= 5:
                    self.animation_index[0][1] = 0
            # attact right
            if self.rect.colliderect(player.rect) and not self.is_fliped:
                self.image_to_show = self.assets["orc_hit"][math.floor(self.animation_index[1][1])]
                self.animation_index[1][1] += 0.1
                if self.animation_index[1][1] >= 5:
                    self.animation_index[1][1] = 0
            # walk left
            if  self.is_fliped:
                self.image_to_show = pygame.transform.flip(self.assets["orc_run"][math.floor(self.animation_index[0][1])],True,False)
                self.animation_index[0][1] += 0.1
                if self.animation_index[0][1] >= 5:
                    self.animation_index[0][1] = 0
            # attact left
            if self.rect.colliderect(player.rect) and self.is_fliped:
                self.image_to_show = pygame.transform.flip(self.assets["orc_hit"][math.floor(self.animation_index[1][1])],True,False)
                self.animation_index[1][1] += 0.1
                if self.animation_index[1][1] >= 5:
                    self.animation_index[1][1] = 0
            if self.health < 0:
                self.alive = False
            # create a line of sight from enemy to the player
            self.line_of_sight = ((self.rect.centerx, self.rect.centery), (player.rect.centerx, player.rect.centery))
            # check if line of sight passes through an obstacle tile
            for obstacle in obstacle_tile:
                if obstacle[1].clipline(self.line_of_sight):
                    clipped_line = obstacle[1].clipline(self.line_of_sight)
            dist = math.sqrt(((self.rect.centerx - player.rect.centerx)**2)+((self.rect.centery-player.rect.centery)**2))
            # check if chaise
            if not clipped_line:
                if dist <= scripts.constants.ORC_RANGE or self.health < 40:
                    self.chaise = True
        # when not alive
        if not self.alive:
            if self.randgold <= 50:
                gold = True
            if self.randpotion <= 10:
                health_potion = True
            if self.is_fliped:
                self.image_to_show = self.assets["orc_dead"][math.floor(self.animation_index[2][1])]
                self.animation_index[2][1] += 0.05
                if self.animation_index[2][1] >= 5:
                    self.animation_index[2][1] = 5
                    self.dead_counter += 1
                if self.dead_counter > 30:
                    self.delete = True 
            else: 
                self.image_to_show = pygame.transform.flip(self.assets["orc_dead"][math.floor(self.animation_index[2][1])],True,False)
                self.animation_index[2][1] += 0.05
                if self.animation_index[2][1] >= 5:
                    self.animation_index[2][1] = 5
                    self.dead_counter += 1
                if self.dead_counter > 30:
                    self.delete = True
        return gold, health_potion, self.alive

                 

    def hit_player(self, damage, player):
        counter = 1000
        if self.alive:
            if self.rect.colliderect(player.rect) and (pygame.time.get_ticks()-self.last_hit) >= counter:
                self.assets["orc_hit_sound"].play()
                player.health -= damage
                self.last_hit = pygame.time.get_ticks()

    def change_fx_volume(self):
        self.assets["orc_hit_sound"].set_volume(scripts.constants.FX_VOLUME)
                    
    def draw(self, surface):
            surface.blit(self.image_to_show, (self.rect.center[0]-16,self.rect.center[1]-20))
            if scripts.constants.SHOW_HITBOX:
                pygame.draw.rect(surface, scripts.constants.RED, self.rect, 1)
            if scripts.constants.SHOW_LINE_OF_SIGHT and not self.chaise:
                pygame.draw.line(surface, scripts.constants.WHITE, self.line_of_sight[0], self.line_of_sight[1])
            elif scripts.constants.SHOW_LINE_OF_SIGHT and self.chaise:
                pygame.draw.line(surface, scripts.constants.RED, self.line_of_sight[0], self.line_of_sight[1])


class Orc_Shaman_Boss(Orc):
    def __init__(self, x, y, health):
        super().__init__(x, y, health)
        self.assets={
            "orc_run": loadImages("char/orc_shaman/walk"),
            "orc_hit": loadImages("char/orc_shaman/attact"),
            "orc_dead": loadImages("char/orc_shaman/dead"),
            "orc_hit_sound": pygame.mixer.Sound("assets/audio/orcHit.mp3")
        }
        self.assets["orc_hit_sound"].set_volume(scripts.constants.FX_VOLUME)
        self.rect = pygame.Rect(0,0,28,56)
        self.rect.center = (x,y)
        self.health_max = health
        self.name = "SHAMAN"
        self.fireball_trigger = pygame.time.get_ticks()

    def draw(self, surface):
        surface.blit(self.image_to_show, (self.rect.center[0]-32,self.rect.center[1]-40))
        if scripts.constants.SHOW_HITBOX:
            pygame.draw.rect(surface, scripts.constants.RED, self.rect, 1)
        if scripts.constants.SHOW_LINE_OF_SIGHT and not self.chaise:
            pygame.draw.line(surface, scripts.constants.WHITE, self.line_of_sight[0], self.line_of_sight[1])
        elif scripts.constants.SHOW_LINE_OF_SIGHT and self.chaise:
            pygame.draw.line(surface, scripts.constants.RED, self.line_of_sight[0], self.line_of_sight[1])

    def update(self, player, obstacle_tile):
        
        # reset values
        self.alive = True
        clipped_line = None
        fireball = None

        if self.health < 0:
                self.alive = False

        if self.alive:
            # check if mob has died
            if self.health <= 0:
                self.health = 0
                self.alive = False
            # handle animation
            # update flip direction
            if self.dx > 0:
                self.is_fliped = False
            if self.dx < 0:
                self.is_fliped = True
            # walk right
            if not self.is_fliped:
                self.image_to_show = self.assets["orc_run"][math.floor(self.animation_index[0][1])]
                self.animation_index[0][1] += 0.1
                if self.animation_index[0][1] >= 6:
                    self.animation_index[0][1] = 0
            # attact right
            if self.rect.colliderect(player.rect) and not self.is_fliped:
                self.image_to_show = self.assets["orc_hit"][math.floor(self.animation_index[1][1])]
                self.animation_index[1][1] += 0.1
                if self.animation_index[1][1] >= 4:
                    self.animation_index[1][1] = 0
                damage = 10 + random.randint(-5,5)
                self.hit_player(damage, player)
            # walk left
            if  self.is_fliped:
                self.image_to_show = pygame.transform.flip(self.assets["orc_run"][math.floor(self.animation_index[0][1])],True,False)
                self.animation_index[0][1] += 0.1
                if self.animation_index[0][1] >= 6:
                    self.animation_index[0][1] = 0
            # attact left
            if self.rect.colliderect(player.rect) and self.is_fliped:
                self.image_to_show = pygame.transform.flip(self.assets["orc_hit"][math.floor(self.animation_index[1][1])],True,False)
                self.animation_index[1][1] += 0.1
                if self.animation_index[1][1] >= 4:
                    self.animation_index[1][1] = 0
                damage = 10 + random.randint(-5,5)
                self.hit_player(damage, player)
            # create a line of sight from enemy to the player
            self.line_of_sight = ((self.rect.centerx, self.rect.centery), (player.rect.centerx, player.rect.centery))
            # check if line of sight passes through an obstacle tile
            for obstacle in obstacle_tile:
                if obstacle[1].clipline(self.line_of_sight):
                    clipped_line = obstacle[1].clipline(self.line_of_sight)
            dist = math.sqrt(((self.rect.centerx - player.rect.centerx)**2)+((self.rect.centery-player.rect.centery)**2))
            # check if chaise
            if not clipped_line:
                if dist <= scripts.constants.ORC_RANGE or self.health < 40:
                    self.chaise = True
            if self.chaise:
                actuall_time = pygame.time.get_ticks()
                
                if actuall_time - self.fireball_trigger >= 5000:
                    self.stunned = True
                    if self.is_fliped:
                        self.image_to_show = pygame.transform.flip(self.assets["orc_hit"][math.floor(self.animation_index[1][1])],True,False)
                    elif not self.is_fliped:
                        self.image_to_show = self.assets["orc_hit"][math.floor(self.animation_index[1][1])]
                    self.animation_index[1][1] += 0.1
                    if self.animation_index[1][1] >= 4:
                        self.fireball_trigger = actuall_time
                        fireball = self.fireball(player)
                        self.animation_index[1][1] = 0
                        self.stunned = False

                    
        
        # when not alive
        if not self.alive:

            if self.is_fliped:
                self.image_to_show = self.assets["orc_dead"][math.floor(self.animation_index[2][1])]
                self.animation_index[2][1] += 0.05
                if self.animation_index[2][1] >= 4:
                    self.animation_index[2][1] = 4
            else: 
                self.image_to_show = pygame.transform.flip(self.assets["orc_dead"][math.floor(self.animation_index[2][1])],True,False)
                self.animation_index[2][1] += 0.05
                if self.animation_index[2][1] >= 4:
                    self.animation_index[2][1] = 4
        
        
        return self.chaise, fireball
    
    def fireball(self, player):
        return Magicball("fireball",self.rect.centerx,self.rect.centery, player.rect.centerx, player.rect.centery)
    
    
        
        

                    