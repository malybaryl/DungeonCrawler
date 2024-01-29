import pygame
from scripts.load import loadImages, loadImage
import scripts.constants
import random

class Town():
    def __init__(self):
        self.assets ={
            "town": loadImages("town/png"),
            "coursor": loadImages("HUD/coursor"),
            "hut": loadImages("town/house"),
            "smith": loadImages("town/smith"),
            "font_8": pygame.font.Font("assets/fonts/font.ttf",8),
            "gold": pygame.transform.scale(loadImage("coin/0.png"),(16,16)),
            "buttons": loadImages("HUD/button")
        }
        self.gold = 0
        self.gold_text = self.assets["font_8"].render(f"{self.gold}", True, scripts.constants.WHITE)
        self.pos = pygame.mouse.get_pos()
        self.hut_builded = False
        self.hut_cost = 100
        self.hut_cost_text = self.assets["font_8"].render(f"{self.hut_cost}", True, scripts.constants.WHITE)
        self.hut_description_1 = 'The Hut is where'
        self.hut_description_2 = '"The Peasant"'
        self.hut_description_3 = 'lives. You can'
        self.hut_description_4 = 'develop his'
        self.hut_description_5 = 'skills here.'
        self.hut_description_text_1 = self.assets["font_8"].render(self.hut_description_1, True, scripts.constants.WHITE)
        self.hut_description_text_2 = self.assets["font_8"].render(self.hut_description_2, True, scripts.constants.WHITE)
        self.hut_description_text_3 = self.assets["font_8"].render(self.hut_description_3, True, scripts.constants.WHITE)
        self.hut_description_text_4 = self.assets["font_8"].render(self.hut_description_4, True, scripts.constants.WHITE)
        self.hut_description_text_5 = self.assets["font_8"].render(self.hut_description_5, True, scripts.constants.WHITE)
        self.smith_builded = False
        self.smith_cost = 50
        self.smith_cost_text = self.assets["font_8"].render(f"{self.smith_cost}", True, scripts.constants.WHITE)
        self.smith_description_1 = 'You can buy new'
        self.smith_description_2 = 'weapons here.'
        self.smith_description_text_1 = self.assets["font_8"].render(self.smith_description_1, True, scripts.constants.WHITE)
        self.smith_description_text_2 = self.assets["font_8"].render(self.smith_description_2, True, scripts.constants.WHITE)
        self.cloud_1 = [random.randint(0,scripts.constants.DISPLAY_WIDTH), random.randint(0,scripts.constants.DISPLAY_HEIGHT//4)]
        self.cloud_2 = [random.randint(0,scripts.constants.DISPLAY_WIDTH), random.randint(0,scripts.constants.DISPLAY_HEIGHT//4)]
        self.cloud_3 = [random.randint(0,scripts.constants.DISPLAY_WIDTH), random.randint(0,scripts.constants.DISPLAY_HEIGHT//4)]
        self.cloud_4 = [random.randint(0,scripts.constants.DISPLAY_WIDTH), random.randint(0,scripts.constants.DISPLAY_HEIGHT//4)]
        self.cloud_5 = [random.randint(0,scripts.constants.DISPLAY_WIDTH), random.randint(0,scripts.constants.DISPLAY_HEIGHT//4)]
        self.cloud_speed_1 = random.randint(1,2)
        self.cloud_speed_2 = random.randint(1,2)
        self.cloud_speed_3 = random.randint(1,2)
        self.cloud_speed_4 = random.randint(1,2)
        self.cloud_speed_5 = random.randint(1,2)
        self.time = 0
        self.fight_button_pressed = False
        self.build_button_pressed = False
        self.build_menu = False
        self.draw_hut_info = False
        self.draw_smith_info = False
        self.smith_cliked = False
        self.hut_cliked = False
        self.draw_confim = False
        self.yes = self.assets["font_8"].render('YES',True,scripts.constants.WHITE)        
        self.no = self.assets["font_8"].render('NO',True,scripts.constants.WHITE)        
        self.confim_text_line_1 = ""        
        self.confim_text_line_2 = ""
        self.confim_text_line_3 = ""
        self.confim_text_line_4 = ""
        self.confim_text_line_5 = ""
        self.confim_text_to_show_1 = self.assets["font_8"].render(self.confim_text_line_1,True,scripts.constants.WHITE)        
        self.confim_text_to_show_2 = self.assets["font_8"].render(self.confim_text_line_2,True,scripts.constants.WHITE)
        self.confim_text_to_show_3 = self.assets["font_8"].render(self.confim_text_line_3,True,scripts.constants.WHITE)
        self.confim_text_to_show_4 = self.assets["font_8"].render(self.confim_text_line_4,True,scripts.constants.WHITE)
        self.confim_text_to_show_5 = self.assets["font_8"].render(self.confim_text_line_5,True,scripts.constants.WHITE)

        
        
    def clouds(self):
       self.cloud_1[0] -= self.cloud_speed_1 
       self.cloud_2[0] -= self.cloud_speed_2 
       self.cloud_3[0] -= self.cloud_speed_3 
       self.cloud_4[0] -= self.cloud_speed_4 
       self.cloud_5[0] -= self.cloud_speed_5
       if self.cloud_1[0] < -64:
            self.cloud_1 = [scripts.constants.DISPLAY_WIDTH+64, random.randint(0,scripts.constants.DISPLAY_HEIGHT//4)]
            self.cloud_speed_1 = random.randint(1,2)
       if self.cloud_2[0] < -64:
            self.cloud_2 = [scripts.constants.DISPLAY_WIDTH+64, random.randint(0,scripts.constants.DISPLAY_HEIGHT//4)]
            self.cloud_speed_2 = random.randint(1,2)
       if self.cloud_3[0] < -64:
            self.cloud_3 = [scripts.constants.DISPLAY_WIDTH+64, random.randint(0,scripts.constants.DISPLAY_HEIGHT//4)]
            self.cloud_speed_3 = random.randint(1,2) 
       if self.cloud_4[0] < -64:
            self.cloud_4 = [scripts.constants.DISPLAY_WIDTH+64, random.randint(0,scripts.constants.DISPLAY_HEIGHT//4)]
            self.cloud_speed_4 = random.randint(1,2) 
       if self.cloud_5[0] < -64:
            self.cloud_5 = [scripts.constants.DISPLAY_WIDTH+64, random.randint(0,scripts.constants.DISPLAY_HEIGHT//4)]
            self.cloud_speed_5 = random.randint(1,2) 
       
    def confim(self):
        answer = 0 # 0- wait 1- yes 2- no
        show = True
        if pygame.mouse.get_pressed()[0]:
            if scripts.constants.DISPLAY_WIDTH//3+10 < self.pos[0]/scripts.constants.SCALE_WIDTH < scripts.constants.DISPLAY_WIDTH//3+10+64 and scripts.constants.DISPLAY_HEIGHT//3+58 < self.pos[1]/scripts.constants.SCALE_HEIGHT < scripts.constants.DISPLAY_HEIGHT//3+58+32:
                answer = 1
                show = False
            elif scripts.constants.DISPLAY_WIDTH//3+84 < self.pos[0]/scripts.constants.SCALE_WIDTH < scripts.constants.DISPLAY_WIDTH//3+84+64 and scripts.constants.DISPLAY_HEIGHT//3+58 < self.pos[1]/scripts.constants.SCALE_HEIGHT < scripts.constants.DISPLAY_HEIGHT//3+58+32:
                answer = 2
                show = False
        return answer, show
     
    def update(self, build_menu_key_pressed):
        self.pos = pygame.mouse.get_pos()
        in_town = True
        fight_button_pressed = False
        self.gold = self.gold
        self.gold_text = self.assets["font_8"].render(f"{self.gold}", True, scripts.constants.WHITE)
        
        if pygame.mouse.get_pressed()[0]:
            if scripts.constants.DISPLAY_WIDTH-34 < self.pos[0]/scripts.constants.SCALE_WIDTH < scripts.constants.DISPLAY_WIDTH-2 and scripts.constants.DISPLAY_HEIGHT-34 < self.pos[1]/scripts.constants.SCALE_HEIGHT < scripts.constants.DISPLAY_HEIGHT-2:
                    self.fight_button_pressed = True
                    self.time = pygame.time.get_ticks()
            if 2 < self.pos[0]/scripts.constants.SCALE_WIDTH < 34 and scripts.constants.DISPLAY_HEIGHT-34 < self.pos[1]/scripts.constants.SCALE_HEIGHT < scripts.constants.DISPLAY_HEIGHT-2:
                    self.build_button_pressed = True
                    self.time = pygame.time.get_ticks()
        if self.build_menu:
            if pygame.mouse.get_pressed()[2]:
                if scripts.constants.DISPLAY_WIDTH/8+4 < self.pos[0]/scripts.constants.SCALE_WIDTH < scripts.constants.DISPLAY_WIDTH/8+36 and scripts.constants.DISPLAY_HEIGHT/8+4 < self.pos[1]/scripts.constants.SCALE_HEIGHT < scripts.constants.DISPLAY_HEIGHT/8+40:
                    self.draw_hut_info = True
                if scripts.constants.DISPLAY_WIDTH/8+40 < self.pos[0]/scripts.constants.SCALE_WIDTH < scripts.constants.DISPLAY_WIDTH/8+62 and scripts.constants.DISPLAY_HEIGHT/8+4 < self.pos[1]/scripts.constants.SCALE_HEIGHT < scripts.constants.DISPLAY_HEIGHT/8+40:
                    self.draw_smith_info = True
            else:
                self.draw_hut_info = False
                self.draw_smith_info = False
            if pygame.mouse.get_pressed()[0]:
                if scripts.constants.DISPLAY_WIDTH/8+4 < self.pos[0]/scripts.constants.SCALE_WIDTH < scripts.constants.DISPLAY_WIDTH/8+36 and scripts.constants.DISPLAY_HEIGHT/8+4 < self.pos[1]/scripts.constants.SCALE_HEIGHT < scripts.constants.DISPLAY_HEIGHT/8+40:
                    self.hut_cliked = True
                if scripts.constants.DISPLAY_WIDTH/8+40 < self.pos[0]/scripts.constants.SCALE_WIDTH < scripts.constants.DISPLAY_WIDTH/8+62 and scripts.constants.DISPLAY_HEIGHT/8+4 < self.pos[1]/scripts.constants.SCALE_HEIGHT < scripts.constants.DISPLAY_HEIGHT/8+40:
                    self.smith_cliked = True
            
            if self.hut_cliked:
                if self.hut_cost <= self.gold:
                    self.confim_text_line_1 = 'Are you sure you' 
                    self.confim_text_line_2 = 'want to build'
                    self.confim_text_line_3 = '"The Hut"? Cost:'
                    self.confim_text_line_4 = f'{self.hut_cost} gold'
                    self.confim_text_line_5 = ''
                    self.confim_text_to_show_1 = self.assets["font_8"].render(self.confim_text_line_1,True,scripts.constants.WHITE)        
                    self.confim_text_to_show_2 = self.assets["font_8"].render(self.confim_text_line_2,True,scripts.constants.WHITE)        
                    self.confim_text_to_show_3 = self.assets["font_8"].render(self.confim_text_line_3,True,scripts.constants.WHITE)        
                    self.confim_text_to_show_4 = self.assets["font_8"].render(self.confim_text_line_4,True,scripts.constants.WHITE)        
                    self.confim_text_to_show_4 = self.assets["font_8"].render(self.confim_text_line_5,True,scripts.constants.WHITE)        
                    answer, self.draw_confim = self.confim()
                    if answer > 0.5 and answer < 1.5:
                        self.hut_builded = True
                        self.gold -= self.hut_cost
                        self.hut_cliked = False
                    elif answer > 1.5 and answer < 2.5:
                        self.hut_cliked = False
                else:
                    self.hut_cliked = False
            if self.smith_cliked:
                if self.smith_cost <= self.gold:
                    self.confim_text_line_1 = 'Are you sure you' 
                    self.confim_text_line_2 = 'want to build'
                    self.confim_text_line_3 = '"The Smith"? Cost:'
                    self.confim_text_line_4 = f'{self.smith_cost} gold'
                    self.confim_text_line_5 = ''
                    self.confim_text_to_show_1 = self.assets["font_8"].render(self.confim_text_line_1,True,scripts.constants.WHITE)        
                    self.confim_text_to_show_2 = self.assets["font_8"].render(self.confim_text_line_2,True,scripts.constants.WHITE)        
                    self.confim_text_to_show_3 = self.assets["font_8"].render(self.confim_text_line_3,True,scripts.constants.WHITE)        
                    self.confim_text_to_show_4 = self.assets["font_8"].render(self.confim_text_line_4,True,scripts.constants.WHITE)        
                    self.confim_text_to_show_4 = self.assets["font_8"].render(self.confim_text_line_5,True,scripts.constants.WHITE)        
                    answer, self.draw_confim = self.confim()
                    if answer > 0.5 and answer < 1.5:
                        self.smith_builded = True
                        self.gold -= self.smith_cost
                        self.smith_cliked = False
                    elif answer > 1.5 and answer < 2.5:
                        self.smith_cliked = False
                else:
                    self.smith_cliked = False
            
        if build_menu_key_pressed:
            if self.build_menu:
                self.build_menu = False
                build_menu_key_pressed = False
            else:
                self.build_menu = True
                build_menu_key_pressed = False
            
        if self.fight_button_pressed:
                if (pygame.time.get_ticks() - self.time) >= 100:
                    in_town = False
                    fight_button_pressed = True
                    self.fight_button_pressed = False       
        if self.build_button_pressed:
                if (pygame.time.get_ticks() - self.time) >= 100:
                    if self.build_menu:
                        self.build_menu = False
                        self.build_button_pressed = False
                    else:
                        self.build_menu = True
                        self.build_button_pressed = False
                    
        return in_town, build_menu_key_pressed, fight_button_pressed
        
    def draw(self,display):
        # sky
        display.blit(self.assets["town"][0],(0,0))
        # clouds
        display.blit(self.assets["town"][1],(self.cloud_1[0],self.cloud_1[1]))
        display.blit(self.assets["town"][2],(self.cloud_2[0],self.cloud_2[1]))
        display.blit(self.assets["town"][3],(self.cloud_3[0],self.cloud_3[1]))
        display.blit(self.assets["town"][4],(self.cloud_4[0],self.cloud_4[1]))
        display.blit(self.assets["town"][5],(self.cloud_5[0],self.cloud_5[1]))
        # forest
        display.blit(self.assets["town"][6],(0,0))
        # tree
        display.blit(self.assets["town"][7],(0,0))
        display.blit(self.assets["town"][8],(0,0))
        # buildings
        display.blit(self.assets["town"][9],(0,0))
        if self.hut_builded:
            display.blit(self.assets["town"][10],(0,0))
        if self.smith_builded:
            display.blit(self.assets["town"][11],(0,0))
        # HUD
        pygame.draw.rect(display,scripts.constants.WHITE,(0,scripts.constants.DISPLAY_HEIGHT-32,scripts.constants.DISPLAY_WIDTH,scripts.constants.DISPLAY_HEIGHT))
        pygame.draw.rect(display,scripts.constants.MAINMENU_COLOR_DARKER,(0,scripts.constants.DISPLAY_HEIGHT-30,scripts.constants.DISPLAY_WIDTH,scripts.constants.DISPLAY_HEIGHT))
            # buttons
        display.blit(self.assets["town"][13],(0,0))
        display.blit(self.assets["town"][14],(0,0))
        display.blit(self.assets["town"][15],(0,0))
            # resources
        pygame.draw.rect(display,scripts.constants.WHITE,(scripts.constants.DISPLAY_WIDTH//3-2,scripts.constants.DISPLAY_HEIGHT-25,148,22))
        pygame.draw.rect(display,scripts.constants.MAINMENU_COLOR,(scripts.constants.DISPLAY_WIDTH//3-1,scripts.constants.DISPLAY_HEIGHT-24,146,20))
        display.blit(self.assets["gold"],(scripts.constants.DISPLAY_WIDTH//3, scripts.constants.DISPLAY_HEIGHT-23))
        display.blit(self.gold_text,(scripts.constants.DISPLAY_WIDTH//3+16, scripts.constants.DISPLAY_HEIGHT-18))
        # bulding menu
        if self.build_menu:
            # frame
            pygame.draw.rect(display,scripts.constants.WHITE,(scripts.constants.DISPLAY_WIDTH/8-2,scripts.constants.DISPLAY_HEIGHT/8-2,scripts.constants.DISPLAY_WIDTH-scripts.constants.DISPLAY_WIDTH/4+4,scripts.constants.DISPLAY_HEIGHT-scripts.constants.DISPLAY_HEIGHT/4+4))
            pygame.draw.rect(display,scripts.constants.MAINMENU_COLOR,(scripts.constants.DISPLAY_WIDTH/8,scripts.constants.DISPLAY_HEIGHT/8,scripts.constants.DISPLAY_WIDTH-scripts.constants.DISPLAY_WIDTH/4,scripts.constants.DISPLAY_HEIGHT-scripts.constants.DISPLAY_HEIGHT/4))
            # buildings
            if self.hut_builded:
                pygame.draw.rect(display,scripts.constants.GREY,(scripts.constants.DISPLAY_WIDTH/8+4,scripts.constants.DISPLAY_HEIGHT/8+4,32,32))
                display.blit(self.assets["hut"][0],(scripts.constants.DISPLAY_WIDTH/8+4,scripts.constants.DISPLAY_HEIGHT/8+4))
            else:
                if self.gold >= self.hut_cost:
                    pygame.draw.rect(display,scripts.constants.GREEN,(scripts.constants.DISPLAY_WIDTH/8+4,scripts.constants.DISPLAY_HEIGHT/8+4,32,32))
                else:
                    pygame.draw.rect(display,scripts.constants.RED,(scripts.constants.DISPLAY_WIDTH/8+4,scripts.constants.DISPLAY_HEIGHT/8+4,32,32))
                display.blit(self.assets["hut"][0],(scripts.constants.DISPLAY_WIDTH/8+4,scripts.constants.DISPLAY_HEIGHT/8+4))
                display.blit(self.hut_cost_text, (scripts.constants.DISPLAY_WIDTH/8+4,scripts.constants.DISPLAY_HEIGHT/8+4))
            # confirm frame
            if self.draw_confim:
                pygame.draw.rect(display,scripts.constants.WHITE,(scripts.constants.DISPLAY_WIDTH//3, scripts.constants.DISPLAY_HEIGHT//3,scripts.constants.DISPLAY_WIDTH//3,scripts.constants.DISPLAY_HEIGHT//3))
                pygame.draw.rect(display,scripts.constants.MAINMENU_COLOR_DARKER,(scripts.constants.DISPLAY_WIDTH//3+2, scripts.constants.DISPLAY_HEIGHT//3+2,scripts.constants.DISPLAY_WIDTH//3-4,scripts.constants.DISPLAY_HEIGHT//3-4))
                display.blit(self.confim_text_to_show_1,(scripts.constants.DISPLAY_WIDTH//3+6, scripts.constants.DISPLAY_HEIGHT//3+6))
                display.blit(self.confim_text_to_show_2,(scripts.constants.DISPLAY_WIDTH//3+6, scripts.constants.DISPLAY_HEIGHT//3+16))
                display.blit(self.confim_text_to_show_3,(scripts.constants.DISPLAY_WIDTH//3+6, scripts.constants.DISPLAY_HEIGHT//3+26))
                display.blit(self.confim_text_to_show_4,(scripts.constants.DISPLAY_WIDTH//3+6, scripts.constants.DISPLAY_HEIGHT//3+36))
                display.blit(self.confim_text_to_show_5,(scripts.constants.DISPLAY_WIDTH//3+6, scripts.constants.DISPLAY_HEIGHT//3+46))
                display.blit(self.assets["buttons"][0], (scripts.constants.DISPLAY_WIDTH//3+10, scripts.constants.DISPLAY_HEIGHT//3+58))
                display.blit(self.yes, (scripts.constants.DISPLAY_WIDTH//3+30, scripts.constants.DISPLAY_HEIGHT//3+70))
                display.blit(self.assets["buttons"][0], (scripts.constants.DISPLAY_WIDTH//3+84, scripts.constants.DISPLAY_HEIGHT//3+58))
                display.blit(self.no, (scripts.constants.DISPLAY_WIDTH//3+84+26, scripts.constants.DISPLAY_HEIGHT//3+70))
                
            if self.smith_builded:
                pygame.draw.rect(display,scripts.constants.GREY,(scripts.constants.DISPLAY_WIDTH/8+40,scripts.constants.DISPLAY_HEIGHT/8+4,32,32))
                display.blit(self.assets["smith"][0],(scripts.constants.DISPLAY_WIDTH/8+40,scripts.constants.DISPLAY_HEIGHT/8+4))
            else:
                if self.gold >= self.smith_cost:
                    pygame.draw.rect(display,scripts.constants.GREEN,(scripts.constants.DISPLAY_WIDTH/8+40,scripts.constants.DISPLAY_HEIGHT/8+4,32,32))
                else:
                    pygame.draw.rect(display,scripts.constants.RED,(scripts.constants.DISPLAY_WIDTH/8+40,scripts.constants.DISPLAY_HEIGHT/8+4,32,32))
                display.blit(self.assets["smith"][0],(scripts.constants.DISPLAY_WIDTH/8+40,scripts.constants.DISPLAY_HEIGHT/8+4))
                display.blit(self.smith_cost_text, (scripts.constants.DISPLAY_WIDTH/8+40,scripts.constants.DISPLAY_HEIGHT/8+4))
            if self.draw_hut_info:
                pygame.draw.rect(display,scripts.constants.WHITE,(self.pos[0]/scripts.constants.SCALE_WIDTH,self.pos[1]/scripts.constants.SCALE_HEIGHT,150,100))
                pygame.draw.rect(display,scripts.constants.MAINMENU_COLOR_DARKER,(self.pos[0]/scripts.constants.SCALE_WIDTH+2,self.pos[1]/scripts.constants.SCALE_HEIGHT+2,146,96))
                display.blit(self.hut_description_text_1,(self.pos[0]/scripts.constants.SCALE_WIDTH+4,self.pos[1]/scripts.constants.SCALE_HEIGHT+4))
                display.blit(self.hut_description_text_2,(self.pos[0]/scripts.constants.SCALE_WIDTH+4,self.pos[1]/scripts.constants.SCALE_HEIGHT+14))
                display.blit(self.hut_description_text_3,(self.pos[0]/scripts.constants.SCALE_WIDTH+4,self.pos[1]/scripts.constants.SCALE_HEIGHT+24))
                display.blit(self.hut_description_text_4,(self.pos[0]/scripts.constants.SCALE_WIDTH+4,self.pos[1]/scripts.constants.SCALE_HEIGHT+34))
                display.blit(self.hut_description_text_5,(self.pos[0]/scripts.constants.SCALE_WIDTH+4,self.pos[1]/scripts.constants.SCALE_HEIGHT+44))
            if self.draw_smith_info:
                pygame.draw.rect(display,scripts.constants.WHITE,(self.pos[0]/scripts.constants.SCALE_WIDTH,self.pos[1]/scripts.constants.SCALE_HEIGHT,150,100))
                pygame.draw.rect(display,scripts.constants.MAINMENU_COLOR_DARKER,(self.pos[0]/scripts.constants.SCALE_WIDTH+2,self.pos[1]/scripts.constants.SCALE_HEIGHT+2,146,96))
                display.blit(self.smith_description_text_1,(self.pos[0]/scripts.constants.SCALE_WIDTH+4,self.pos[1]/scripts.constants.SCALE_HEIGHT+4))
                display.blit(self.smith_description_text_2,(self.pos[0]/scripts.constants.SCALE_WIDTH+4,self.pos[1]/scripts.constants.SCALE_HEIGHT+14))
                
                
        # drawing coursor
        display.blit(pygame.transform.scale(self.assets["coursor"][0],(24,24)),(self.pos[0]/scripts.constants.SCALE_WIDTH,self.pos[1]/scripts.constants.SCALE_HEIGHT)) 
        