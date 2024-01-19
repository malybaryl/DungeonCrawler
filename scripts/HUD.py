import pygame
import scripts.constants
from scripts.load import loadImage, loadImages

class HUD:
    def __init__(self, player, world_level):
        self.assets={
            "coursor": loadImages("HUD/coursor"),
            "gold": pygame.transform.scale(loadImage("coin/0.png"),(16,16))
        }
        pygame.mouse.set_visible(False)    
        self.pos = None
        self.info = False
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
        # fade transition varibles
        self.x_fade = 0
        self.y_fade = 0
        self.draw_x_right = True
        self.draw_y_down = True
        self.draw_red_fade_= True
    
    def update(self, player, world_level):
        self.pos = pygame.mouse.get_pos()
        self.world_level = world_level
        self.health = player.health
        self.gold = player.gold
        self.image = self.font.render(str(self.gold), True, scripts.constants.WHITE)
        self.image_player_hp = self.font.render(str(self.health)+'/'+str(self.full_health), True, scripts.constants.WHITE)
        self.image_world_level = self.font.render("WORLD LEVEL: "+str(self.world_level), True, scripts.constants.WHITE)
        self.player_alive = player.alive

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
                # drawing player health
                pygame.draw.rect(display,scripts.constants.BLACK,(scripts.constants.DISPLAY_WIDTH/8-2+4,scripts.constants.DISPLAY_HEIGHT/8-2+4,102,12))
                pygame.draw.rect(display,scripts.constants.DARKRED,(scripts.constants.DISPLAY_WIDTH/8-2+5,scripts.constants.DISPLAY_HEIGHT/8-2+5,100,10))
                pygame.draw.rect(display,scripts.constants.RED,(scripts.constants.DISPLAY_WIDTH/8-2+5,scripts.constants.DISPLAY_HEIGHT/8-2+5,(self.health/self.full_health)*100,10))
                display.blit(self.image_player_hp,(scripts.constants.DISPLAY_WIDTH/8-2+25,scripts.constants.DISPLAY_HEIGHT/8-2+6))
                # drawing info world level
                display.blit(self.image_world_level,(scripts.constants.DISPLAY_WIDTH/8-2+5,scripts.constants.DISPLAY_HEIGHT/8-2+20))
                # drawing info gold
                display.blit(self.assets["gold"],(scripts.constants.DISPLAY_WIDTH/8-2+5,scripts.constants.DISPLAY_HEIGHT/8-2+30))
                display.blit(self.image,(scripts.constants.DISPLAY_WIDTH/8-2+5+22,scripts.constants.DISPLAY_HEIGHT/8-2+26+8))
            # drawing coursor
            display.blit(pygame.transform.scale(self.assets["coursor"][0],(24,24)),(self.pos[0]/scripts.constants.SCALE_WIDTH,self.pos[1]/scripts.constants.SCALE_HEIGHT)) 
            display.blit(pygame.transform.scale(self.assets["coursor"][1],(24,24)),(self.pos[0]/scripts.constants.SCALE_WIDTH-24,self.pos[1]/scripts.constants.SCALE_HEIGHT-24)) 
            display.blit(pygame.transform.scale(self.assets["coursor"][2],(24,24)),(self.pos[0]/scripts.constants.SCALE_WIDTH,self.pos[1]/scripts.constants.SCALE_HEIGHT-24)) 
            display.blit(pygame.transform.scale(self.assets["coursor"][3],(24,24)),(self.pos[0]/scripts.constants.SCALE_WIDTH-24,self.pos[1]/scripts.constants.SCALE_HEIGHT)) 
        if not self.player_alive:
            display.blit(self.image_died,(50, scripts.constants.DISPLAY_HEIGHT/2-20))

    def draw_red_fade(self,display,player):
        if player.health < (player.health_max/2):
            pass # zrobic rysunek czerwonego przezroczystego rysunku
        elif player.health < (player.health_max*0.9):
            pass

       