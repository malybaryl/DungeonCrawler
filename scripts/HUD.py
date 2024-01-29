import pygame
import scripts.constants
from scripts.load import loadImage, loadImages


class HUD:
    def __init__(self, player, world_level):
        self.assets={
            "coursor": loadImages("HUD/coursor"),
            "gold": pygame.transform.scale(loadImage("coin/0.png"),(16,16)),
            "red_fade": loadImage("effects/redfade/0.png"),
            "buttons": loadImages("HUD/button")
        }
        pygame.mouse.set_visible(False)    
        self.pos = None
        self.info = False
        self.time = 0
        self.world_level = world_level
        self.full_health = player.health_max
        self.health = player.health
        self.gold = player.gold
        self.font = pygame.font.Font("assets/fonts/font.ttf",8)
        self.font2 = pygame.font.Font("assets/fonts/font.ttf",48)
        self.font3 = pygame.font.Font("assets/fonts/font.ttf",16)
        self.image_world_level_infor = self.font.render(str(self.gold), True, scripts.constants.WHITE)
        self.image_died = self.font2.render("YOU DIED", True, scripts.constants.RED)
        self.image_player_hp = self.font.render(str(self.health)+'/'+str(self.full_health), True, scripts.constants.WHITE)
        self.image_world_level = self.font.render("WORLD LEVEL: "+str(self.world_level), True, scripts.constants.WHITE)
        self.player_alive = player.alive
        self.player_image = pygame.transform.scale(player.assets["player_idle"][0],(64,64))
        self.statistic_text = self.font.render("STATISTICS", True, scripts.constants.WHITE)
        self.damege_text = self.font.render("Damage: 5-15", True, scripts.constants.WHITE)
        self.back_to_town_text = self.font.render("BACK TO TOWN", True, scripts.constants.WHITE)
        self.back_to_town_button_clicked = False
        self.back_to_town_button_to_show = pygame.transform.scale(self.assets["buttons"][0],(112,26)) 
        # fade transition varibles
        self.x_fade = 0
        self.y_fade = 0
        self.draw_x_right = True
        self.draw_y_down = True
        self.draw_red_fade_= True
    
    def update(self, player, world_level, town):
        self.pos = pygame.mouse.get_pos()
        self.world_level = world_level
        self.health = player.health
        self.gold = player.gold
        self.image = self.font.render(str(self.gold), True, scripts.constants.WHITE)
        self.image_player_hp = self.font.render(str(self.health)+'/'+str(self.full_health), True, scripts.constants.WHITE)
        self.image_world_level = self.font.render("WORLD LEVEL: "+str(self.world_level), True, scripts.constants.WHITE)
        self.player_alive = player.alive
        back_to_town = False
        if not self.player_alive: 
            if pygame.mouse.get_pressed()[0]:
                if scripts.constants.DISPLAY_WIDTH//2-56 < self.pos[0]/scripts.constants.SCALE_WIDTH < scripts.constants.DISPLAY_WIDTH//2-56+112 and 3*scripts.constants.DISPLAY_HEIGHT//4 < self.pos[1]/scripts.constants.SCALE_HEIGHT < 3*scripts.constants.DISPLAY_HEIGHT//4+26:
                        self.back_to_town_button_clicked = True
                        self.time = pygame.time.get_ticks()
            if self.back_to_town_button_clicked:
                self.back_to_town_button_to_show = pygame.transform.scale(self.assets["buttons"][1],(112,26))
                if (pygame.time.get_ticks() - self.time) >= 100:
                    back_to_town = True
                    # adding gold to town
                    town.gold += self.gold + (self.gold*self.world_level*0.1)
                    # button handler
                    self.back_to_town_button_clicked = False
                    self.back_to_town_button_to_show = pygame.transform.scale(self.assets["buttons"][0],(112,26))
        return back_to_town
    


    def info_show(self):
        if self.info:
            self.info = False
        elif not self.info:
            self.info = True


    def draw_boss_hp(self,display, hp, hp_max, boss_name="BOOS"):
        if self.player_alive:
            if hp > 0:
                pygame.draw.rect(display,scripts.constants.BLACK,(scripts.constants.DISPLAY_WIDTH/2-150,scripts.constants.DISPLAY_HEIGHT/10-1,230,18))
                pygame.draw.rect(display,scripts.constants.DARKRED,(scripts.constants.DISPLAY_WIDTH/2-149,scripts.constants.DISPLAY_HEIGHT/10,298,16))
                pygame.draw.rect(display,scripts.constants.RED,(scripts.constants.DISPLAY_WIDTH/2-1,scripts.constants.DISPLAY_HEIGHT/10,(hp/hp_max)*150,16))
                pygame.draw.rect(display,scripts.constants.RED,(scripts.constants.DISPLAY_WIDTH/2 - ((hp/hp_max)*150)+1,scripts.constants.DISPLAY_HEIGHT/10,(hp/hp_max)*150,16))
                image = self.font3.render(boss_name, True, scripts.constants.WHITE)
                display.blit(image,((scripts.constants.DISPLAY_WIDTH/2)-(len(boss_name)*8),scripts.constants.DISPLAY_HEIGHT/10+1))

    def draw_fade(self, display):
            fade = True
            # drawing fades
            pygame.draw.rect(display, scripts.constants.BLACK,(0,0,self.x_fade,scripts.constants.DISPLAY_HEIGHT))
            pygame.draw.rect(display, scripts.constants.BLACK,(0,0,scripts.constants.DISPLAY_WIDTH,self.y_fade))
            pygame.draw.rect(display, scripts.constants.BLACK,(scripts.constants.DISPLAY_WIDTH-self.x_fade,0,self.x_fade,scripts.constants.DISPLAY_HEIGHT))
            pygame.draw.rect(display, scripts.constants.BLACK,(0,scripts.constants.DISPLAY_HEIGHT-self.y_fade,scripts.constants.DISPLAY_WIDTH,self.y_fade))
            
            # hadle left and right fade
            if self.draw_x_right:
                self.x_fade += scripts.constants.FADE_SPEED * (scripts.constants.DISPLAY_WIDTH/scripts.constants.DISPLAY_HEIGHT)
            elif not self.draw_x_right:
                self.x_fade -= scripts.constants.FADE_SPEED * (scripts.constants.DISPLAY_WIDTH/scripts.constants.DISPLAY_HEIGHT)
            if self.x_fade > scripts.constants.DISPLAY_WIDTH//2:
                self.draw_x_right = False
            
            # handle up and down fade
            if self.draw_y_down:
                self.y_fade += scripts.constants.FADE_SPEED 
            elif not self.draw_y_down:
                self.y_fade -= scripts.constants.FADE_SPEED 
            if self.y_fade > scripts.constants.DISPLAY_HEIGHT//2:
                self.draw_y_down = False

            # reset values and stop fade
            if self.x_fade < 0:
                self.x_fade = 0
                self.y_fade = 0
                self.draw_x_right = True
                self.draw_y_down = True
                fade = False
            return fade

    def draw(self, display):
        if self.player_alive:
            if self.info:
                pygame.draw.rect(display,scripts.constants.WHITE,(scripts.constants.DISPLAY_WIDTH/8-2,scripts.constants.DISPLAY_HEIGHT/8-2,scripts.constants.DISPLAY_WIDTH-scripts.constants.DISPLAY_WIDTH/4+4,scripts.constants.DISPLAY_HEIGHT-scripts.constants.DISPLAY_HEIGHT/4+4))
                pygame.draw.rect(display,scripts.constants.MAINMENU_COLOR,(scripts.constants.DISPLAY_WIDTH/8,scripts.constants.DISPLAY_HEIGHT/8,scripts.constants.DISPLAY_WIDTH-scripts.constants.DISPLAY_WIDTH/4,scripts.constants.DISPLAY_HEIGHT-scripts.constants.DISPLAY_HEIGHT/4))
                # drawing info world level
                display.blit(self.image_world_level,(2,2))
                # drawing info gold
                display.blit(self.assets["gold"],(2,scripts.constants.DISPLAY_HEIGHT-18))
                display.blit(self.image,(18,scripts.constants.DISPLAY_HEIGHT-13))
                # drawing player image
                pygame.draw.rect(display,scripts.constants.MAINMENU_COLOR_DARKER,((scripts.constants.DISPLAY_WIDTH/6),(scripts.constants.DISPLAY_HEIGHT/6)+((scripts.constants.DISPLAY_HEIGHT/6)/2),64,64))
                display.blit(self.player_image,((scripts.constants.DISPLAY_WIDTH/6),(scripts.constants.DISPLAY_HEIGHT/6)+((scripts.constants.DISPLAY_HEIGHT/6)/2)))
                # STATISCTIS
                display.blit(self.statistic_text,(scripts.constants.DISPLAY_WIDTH*5/6-64-32,scripts.constants.DISPLAY_HEIGHT/8+4))
                pygame.draw.rect(display,scripts.constants.MAINMENU_COLOR_DARKER,(scripts.constants.DISPLAY_WIDTH*5/6-128-2,scripts.constants.DISPLAY_HEIGHT/8+16+4-2,135,125))
                # drawing player health
                pygame.draw.rect(display,scripts.constants.BLACK,(scripts.constants.DISPLAY_WIDTH*5/6-128,scripts.constants.DISPLAY_HEIGHT/8+16+4,102,12))
                pygame.draw.rect(display,scripts.constants.DARKRED,(scripts.constants.DISPLAY_WIDTH*5/6-128+1,scripts.constants.DISPLAY_HEIGHT/8+16+4-2+5-2,100,10))
                pygame.draw.rect(display,scripts.constants.RED,(scripts.constants.DISPLAY_WIDTH*5/6-128+1,scripts.constants.DISPLAY_HEIGHT/8+16+4-2+5-2,(self.health/self.full_health)*100,10))
                display.blit(self.image_player_hp,(scripts.constants.DISPLAY_WIDTH*5/6-128+24,scripts.constants.DISPLAY_HEIGHT/8+16+6))
                display.blit(self.damege_text,(scripts.constants.DISPLAY_WIDTH*5/6-128,scripts.constants.DISPLAY_HEIGHT/8+16+4+16))
                # drawing coursor
                display.blit(pygame.transform.scale(self.assets["coursor"][0],(24,24)),(self.pos[0]/scripts.constants.SCALE_WIDTH,self.pos[1]/scripts.constants.SCALE_HEIGHT)) 

            else:
                # drawing coursor
                display.blit(pygame.transform.scale(self.assets["coursor"][0],(24,24)),(self.pos[0]/scripts.constants.SCALE_WIDTH,self.pos[1]/scripts.constants.SCALE_HEIGHT)) 
                display.blit(pygame.transform.scale(self.assets["coursor"][1],(24,24)),(self.pos[0]/scripts.constants.SCALE_WIDTH-24,self.pos[1]/scripts.constants.SCALE_HEIGHT-24)) 
                display.blit(pygame.transform.scale(self.assets["coursor"][2],(24,24)),(self.pos[0]/scripts.constants.SCALE_WIDTH,self.pos[1]/scripts.constants.SCALE_HEIGHT-24)) 
                display.blit(pygame.transform.scale(self.assets["coursor"][3],(24,24)),(self.pos[0]/scripts.constants.SCALE_WIDTH-24,self.pos[1]/scripts.constants.SCALE_HEIGHT)) 
        if not self.player_alive:
            display.blit(self.image_died,(50, scripts.constants.DISPLAY_HEIGHT/2-20))
            display.blit(self.back_to_town_button_to_show,(scripts.constants.DISPLAY_WIDTH//2-56,3*scripts.constants.DISPLAY_HEIGHT//4))
            display.blit(self.back_to_town_text,(scripts.constants.DISPLAY_WIDTH//2-49,3*scripts.constants.DISPLAY_HEIGHT//4+10))
            display.blit(pygame.transform.scale(self.assets["coursor"][0],(24,24)),(self.pos[0]/scripts.constants.SCALE_WIDTH,self.pos[1]/scripts.constants.SCALE_HEIGHT))

    def draw_red_fade(self,display,player):
        if player.health < (player.health_max*0.2):
            display.blit(self.assets["red_fade"],(0,0))

       