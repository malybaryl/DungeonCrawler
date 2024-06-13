import pygame
import scripts.constants
from scripts.load import loadImage, loadImages, save_score_to_score_table


class HUD:
    def __init__(self, player, world_level):
        self.assets={
            "coursor": loadImages("HUD/coursor"),
            "gold": loadImage("coin/0.png"),
            "red_fade": loadImage("effects/redfade/0.png"),
            "buttons": loadImages("HUD/button"),
            "health_bar": loadImage("HUD/health_bar/0.png"),
            "main_HUD": loadImage("HUD/main_HUD/0.png"),
            'info_icons_HUD': loadImages('HUD/icons_info_HUD'), # resolution 17x17
        }
        pygame.mouse.set_visible(False)    
        self.pos = None
        self.info = False
        self.time = 0
        self.final_gold = 0
        self.calculate_final_gold = True
        self.world_level = world_level
        self.full_health = player.health_max
        self.health = player.health
        self.old_health = player.old_health
        self.new_health = player.new_health
        self.gold = player.gold
        self.was_hit = player.player_was_hit
        self.was_heal = player.player_was_heal
        self.current_experience = player.current_experience
        self.experience_to_gain_new_level = player.experience_to_gain_new_level
        self.experience_percange = self.current_experience / self.experience_to_gain_new_level
        self.player_level = player.level
        self.font = pygame.font.Font("assets/fonts/font.ttf",8)
        self.font2 = pygame.font.Font("assets/fonts/font.ttf",48)
        self.font3 = pygame.font.Font("assets/fonts/font.ttf",16)
        self.experience_text = self.font.render(str(self.current_experience)+'/'+str(self.experience_to_gain_new_level), True, scripts.constants.WHITE)
        self.player_level_text = self.font.render('Hero Level:' + str(self.player_level), True, scripts.constants.WHITE)
        self.image_world_level_infor = self.font.render(str(self.gold), True, scripts.constants.WHITE)
        self.image_died = self.font2.render("YOU DIED", True, scripts.constants.RED)
        self.image_player_hp = self.font.render(str(self.health)+'/'+str(self.full_health), True, scripts.constants.WHITE)
        self.image_world_level = self.font.render("WORLD LEVEL: "+str(self.world_level), True, scripts.constants.WHITE)
        self.player_alive = player.alive
        self.player_image = pygame.transform.scale(player.assets["player_idle"][0],(64,64))
        self.statistic_text = self.font.render("STATISTICS", True, scripts.constants.WHITE)
        self.final_gold_text = self.font.render(f"GOLD += {self.final_gold}", True, scripts.constants.WHITE)
        self.min_damage = 0
        self.max_damage = 0
        self.health = 'HP:'
        self.health_text = self.font.render(self.health, True, scripts.constants.WHITE)
        self.damege_text = self.font.render(f"Damage:{self.min_damage}-{self.max_damage}", True, scripts.constants.WHITE)
        self.back_to_town_text = self.font.render("SAVE & BACK TO TOWN", True, scripts.constants.WHITE)
        self.back_to_town_button_clicked = False
        self.back_to_town_button_to_show = pygame.transform.scale(self.assets["buttons"][0],(166,26)) 
        # fade transition varibles
        self.x_fade = 0
        self.y_fade = 0
        self.draw_x_right = True
        self.draw_y_down = True
        self.draw_red_fade_= True
        self.counter = pygame.time.get_ticks()
        self.image_counter = self.font.render("TIME: 00:00:00", True, scripts.constants.WHITE)
        self.hours = 0
        self.minutes = 0
        self.seconds = 0
        self.hours_str = str(self.hours)
        self.minutes_str = str(self.minutes)
        self.seconds_str = str(self.seconds)
        self.healthbar_boss = HealthBarBoss(None, None)
        self.input_text = ''
        self.input_rect = pygame.Rect(scripts.constants.DISPLAY_WIDTH//2 - 45, scripts.constants.DISPLAY_HEIGHT * 3//4 - 32, 90, 18)
        self.keys_index = 0
        self.prev_keys_pressed_len = 0
        self.cooldown_death = True
        self.cooldown_death_clock = 0
        self.cooldown_death_do_once = True
        self.text_input_image_to_show = self.font.render('Enter your nickname and save your score', True, scripts.constants.WHITE)
        self.coursor = self.assets["coursor"][4]
        self.cliked = True
        self.cliked_cooldown = 0
        self.draw_coursor = True
        self.sword_icon = True
        self.weapon_image = None
    
    def update_icon_sword(self, weapon_image):
        self.sword_icon = False
        scale = weapon_image.get_size()[0] / weapon_image.get_size()[1]
        self.weapon_image = pygame.transform.scale(weapon_image,(16*scale,16))
        
        
    
    def update_experience_bar(self, player):
        self.current_experience = int(player.current_experience)
        self.experience_to_gain_new_level = int(player.experience_to_gain_new_level)
        self.experience_percange = self.current_experience / self.experience_to_gain_new_level
        self.player_level = player.level
        
        self.experience_text = self.font.render(str(self.current_experience)+'/'+str(self.experience_to_gain_new_level), True, scripts.constants.WHITE)
        self.player_level_text = self.font.render('Hero Level:' + str(self.player_level), True, scripts.constants.WHITE)
        
    
    def refresh_player_image(self, player):
        self.player_image = pygame.transform.scale(player.assets["player_idle"][0],(64,64))
        
     
    def update_character_health_bar(self, player):
        self.full_health = player.health_max
        self.image_player_hp = self.font.render(str(self.health)+'/'+str(self.full_health), True, scripts.constants.WHITE)
    
    def update(self, player, world_level, town, game_counter, keys_pressed):
        pygame.init()
        self.pos = pygame.mouse.get_pos()
        self.world_level = world_level
        self.health = player.health
        self.gold = player.gold
        self.was_hit = player.player_was_hit
        self.old_health = player.old_health
        self.new_health = player.new_health
        self.was_heal = player.player_was_heal
        self.image = self.font.render(str(self.gold), True, scripts.constants.WHITE)
        self.image_player_hp = self.font.render(str(self.health)+'/'+str(self.full_health), True, scripts.constants.WHITE)
        self.image_world_level = self.font.render("WORLD LEVEL: "+str(self.world_level), True, scripts.constants.WHITE)
        self.player_alive = player.alive
        
        # game counter
        if game_counter - self.counter >= 1000:
            self.counter = game_counter
            self.seconds += 1
            if self.seconds >= 60:
                self.seconds = 0
                self.minutes += 1
                if self.minutes >= 60:
                    self.minutes = 0
                    self.hours += 1
                    
        self.hours_str = str(self.hours)
        self.minutes_str = str(self.minutes)
        self.seconds_str = str(self.seconds)
        
        if self.hours < 10:
            self.hours_str = '0' + str(self.hours)
        else:
            self.hours_str = str(self.hours)
        if self.minutes < 10:
            self.minutes_str = '0' + str(self.minutes)
        else:
            self.minutes_str = str(self.minutes)
        if self.seconds < 10:
            self.seconds_str = '0' + str(self.seconds)
        else:
            self.seconds_str = str(self.seconds)
        
        self.image_counter = self.font.render(f"TIME: {self.hours_str}:{self.minutes_str}:{self.seconds_str}", True, scripts.constants.WHITE)
        
               
        back_to_town = False
        if not self.player_alive: 
            
            if self.calculate_final_gold:
                self.final_gold = int(self.gold + (self.gold*self.world_level*0.1))
                self.final_gold_text = self.font.render(f"GOLD += {self.final_gold}", True, scripts.constants.WHITE)
                self.calculate_final_gold = False
            
            if self.cooldown_death_do_once:
                self.cooldown_death_clock = pygame.time.get_ticks()
                self.cooldown_death = True
                self.cooldown_death_do_once = False
                
            # drawing text imput
            if len(keys_pressed) > 0:
                if len(self.input_text) < 11:
                    if len(keys_pressed) > self.prev_keys_pressed_len:
                        if keys_pressed[self.keys_index] != 8:
                            self.input_text += chr(keys_pressed[self.keys_index]).upper()
                            self.keys_index += 1
                            self.prev_keys_pressed_len = len(keys_pressed)
                        else:
                            self.input_text = self.input_text[:-1]
                            self.keys_index += 1
                            self.prev_keys_pressed_len = len(keys_pressed)
                else:
                    self.input_text = self.input_text[:-1]
                
                
            if pygame.mouse.get_pressed()[0]:
                self.cliked = True
                self.cliked_cooldown = pygame.time.get_ticks()
                self.coursor = self.assets["coursor"][5]
                if scripts.constants.DISPLAY_WIDTH//2-56 < self.pos[0]/scripts.constants.SCALE_WIDTH < scripts.constants.DISPLAY_WIDTH//2-56+112 and 3*scripts.constants.DISPLAY_HEIGHT//4 < self.pos[1]/scripts.constants.SCALE_HEIGHT < 3*scripts.constants.DISPLAY_HEIGHT//4+26:
                    self.back_to_town_button_clicked = True
                    self.time = pygame.time.get_ticks()
            if self.back_to_town_button_clicked:
                self.back_to_town_button_to_show = pygame.transform.scale(self.assets["buttons"][1],(166,26))
                if (pygame.time.get_ticks() - self.time) >= 100:
                    back_to_town = True
                    save_score_to_score_table(self.input_text, self.hours, self.minutes, self.seconds, world_level)
                    # adding gold to town
                    scripts.constants.GOLD += self.final_gold
                    # button handler
                    self.back_to_town_button_clicked = False
                    self.back_to_town_button_to_show = pygame.transform.scale(self.assets["buttons"][0],(166,26))
            if self.cliked:
                if pygame.time.get_ticks() - self.cliked_cooldown > 100:
                    self.cliked = False
                    self.coursor_to_show = self.assets['coursor'][4]
        return back_to_town
    


    def info_show(self):
        if self.info:
            self.info = False
        elif not self.info:
            self.info = True

    def draw_boss_hp(self,display, hp, hp_max, boss_name="BOOS"):
        if self.player_alive:
            if hp > 0:
                pygame.draw.rect(display,scripts.constants.BLACK,(scripts.constants.DISPLAY_WIDTH/2-150,scripts.constants.DISPLAY_HEIGHT/10-1,300,18))
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
                # drawing info world level
                display.blit(self.image_world_level,(2,2))
                # drawing info gold
                display.blit(self.assets["gold"],(8,scripts.constants.DISPLAY_HEIGHT-50))
                display.blit(self.image,(37,scripts.constants.DISPLAY_HEIGHT-38))
                # drawing experience bar
                pygame.draw.rect(display, scripts.constants.YELLOW, (0, scripts.constants.DISPLAY_HEIGHT - 12, self.experience_percange * scripts.constants.DISPLAY_WIDTH, 12))
                # drawing main HUD
                display.blit(self.assets['main_HUD'],(0,0))
                # sword icon
                if self.sword_icon:
                    display.blit(self.assets['info_icons_HUD'][0],(74,121))
                else:
                    display.blit(self.weapon_image,(74,121))
                # shield icon
                display.blit(self.assets['info_icons_HUD'][1],(95,121))
                # shoes icon
                display.blit(self.assets['info_icons_HUD'][2],(131,100))
                # tors icon
                display.blit(self.assets['info_icons_HUD'][3],(131,75))
                # helmet icon
                display.blit(self.assets['info_icons_HUD'][4],(131,51))
                # necles icon
                display.blit(self.assets['info_icons_HUD'][5],(40,51))
                # ring 1 icon
                display.blit(self.assets['info_icons_HUD'][6],(40,75))
                # ring 2 icon
                display.blit(self.assets['info_icons_HUD'][7],(40,100))
                # drawing player image
                display.blit(self.player_image,((scripts.constants.DISPLAY_WIDTH//7-6),(scripts.constants.DISPLAY_HEIGHT//7+15)))
                # STATISCTIS
                display.blit(self.statistic_text,(scripts.constants.DISPLAY_WIDTH*5/6-110,scripts.constants.DISPLAY_HEIGHT/8 - 8))
                # Experience Bar
                display.blit(self.experience_text,((scripts.constants.DISPLAY_WIDTH//2 - self.experience_text.get_size()[0]//2),scripts.constants.DISPLAY_HEIGHT - 10))
                # drawing player health
                display.blit(self.health_text,(scripts.constants.DISPLAY_WIDTH*7//17,scripts.constants.DISPLAY_HEIGHT*3//16))
                pygame.draw.rect(display,scripts.constants.BLACK,(scripts.constants.DISPLAY_WIDTH*7//16 + self.health_text.get_size()[0]*2//3, scripts.constants.DISPLAY_HEIGHT*3//16 - self.health_text.get_size()[1]//2,102,14))
                pygame.draw.rect(display,scripts.constants.DARKRED,(scripts.constants.DISPLAY_WIDTH*7//16 + self.health_text.get_size()[0]*2//3+1, scripts.constants.DISPLAY_HEIGHT*3//16 - self.health_text.get_size()[1]//2+1,100,12))
                pygame.draw.rect(display,scripts.constants.RED,(scripts.constants.DISPLAY_WIDTH*7//16 + self.health_text.get_size()[0]*2//3+1, scripts.constants.DISPLAY_HEIGHT*3//16 - self.health_text.get_size()[1]//2+1,(self.health/self.full_health)*100,12))
                display.blit(self.image_player_hp,(scripts.constants.DISPLAY_WIDTH*7//16 + self.health_text.get_size()[0]*2//3 + 51 - self.image_player_hp.get_size()[0]//2, scripts.constants.DISPLAY_HEIGHT*3//16))
                display.blit(self.damege_text,(scripts.constants.DISPLAY_WIDTH*12//17,scripts.constants.DISPLAY_HEIGHT*3//16))
                display.blit(self.player_level_text,(scripts.constants.DISPLAY_WIDTH*7//17,scripts.constants.DISPLAY_HEIGHT*4//16))
                # drawing counter
                display.blit(self.image_counter, (scripts.constants.DISPLAY_WIDTH - 116,2))
                # drawing coursor
                display.blit(self.coursor,(self.pos[0]/scripts.constants.SCALE_WIDTH,self.pos[1]/scripts.constants.SCALE_HEIGHT))

            else:
                # drawing healthbar
                pygame.draw.rect(display,scripts.constants.DARKRED,(2,2,80,7))
                pygame.draw.rect(display,scripts.constants.BLACK,(2,10,70,3))
                if self.was_hit:
                    pygame.draw.rect(display,scripts.constants.YELLOW,(2,2,(self.old_health/self.full_health)*80,7))
                if self.was_heal:
                    pygame.draw.rect(display,scripts.constants.GREEN,(2,2,(self.new_health/self.full_health)*80,7))
                pygame.draw.rect(display,scripts.constants.RED,(2,2,(self.health/self.full_health)*80,7))
                display.blit(self.assets["health_bar"], (0,0))
                
                # drawing boss healthbar
            
                self.healthbar_boss.draw(display)

                # drawing coursor
                if self.draw_coursor:
                    display.blit(pygame.transform.scale(self.assets["coursor"][0],(24,24)),(self.pos[0]/scripts.constants.SCALE_WIDTH,self.pos[1]/scripts.constants.SCALE_HEIGHT)) 
                    display.blit(pygame.transform.scale(self.assets["coursor"][1],(24,24)),(self.pos[0]/scripts.constants.SCALE_WIDTH-24,self.pos[1]/scripts.constants.SCALE_HEIGHT-24)) 
                    display.blit(pygame.transform.scale(self.assets["coursor"][2],(24,24)),(self.pos[0]/scripts.constants.SCALE_WIDTH,self.pos[1]/scripts.constants.SCALE_HEIGHT-24)) 
                    display.blit(pygame.transform.scale(self.assets["coursor"][3],(24,24)),(self.pos[0]/scripts.constants.SCALE_WIDTH-24,self.pos[1]/scripts.constants.SCALE_HEIGHT)) 
        
        else:
            if self.cooldown_death:
                display.blit(self.image_died,(50, scripts.constants.DISPLAY_HEIGHT/2-20))
                if pygame.time.get_ticks() - self.cooldown_death_clock >= 2000:
                    self.cooldown_death = False
            else:
                display.fill(scripts.constants.BROWN)
                display.blit(self.image_died,(50, 16))
                display.blit(self.final_gold_text,(scripts.constants.DISPLAY_WIDTH//2 - self.final_gold_text.get_width()//2,scripts.constants.DISPLAY_HEIGHT//2 - self.final_gold_text.get_height()//2))
                display.blit(self.text_input_image_to_show, (90, 80))
                display.blit(self.back_to_town_button_to_show,(scripts.constants.DISPLAY_WIDTH//2- 83,3*scripts.constants.DISPLAY_HEIGHT//4))
                display.blit(self.back_to_town_text,(scripts.constants.DISPLAY_WIDTH//2- 76,3*scripts.constants.DISPLAY_HEIGHT//4+10))
                self.draw_text_input(display, self.input_text, self.input_rect, scripts.constants.WHITE)
                display.blit(self.coursor,(self.pos[0]/scripts.constants.SCALE_WIDTH,self.pos[1]/scripts.constants.SCALE_HEIGHT))


    def visible_coursor(self, bool):
        self.draw_coursor = bool
    
    
    def draw_text_input(self, display, input_text, rect, font_color):
        pygame.draw.rect(display, scripts.constants.BLACK, rect, 2)
        if input_text != "":
            text_surface = self.font.render(input_text, True, font_color)
            display.blit(text_surface, (rect.x + 5, rect.y + 5))
        
    def draw_red_fade(self,display,player):
        if not self.cooldown_death:
            pass  
        elif player.health < (player.health_max*0.2):
            display.blit(self.assets["red_fade"],(0,0))
        

class HealthBarBoss:
    def __init__(self, name, health):
        self.assets={
            'health_bar': loadImages('HUD/health_bar_boss')
        }
        self.font = pygame.font.Font("assets/fonts/font.ttf",8)
        self.name = name
        self.name_text = ''
        self.full_health = health
        self.health = health
        self.show = False
        self.show_name = self.font.render(name, True, scripts.constants.WHITE)
    
    def update(self, health):
        self.health = health
        
    def set_max_health(self, max_health):
        self.full_health = max_health
        
    def set_name(self, name):
        self.name = name
        self.show_name = self.font.render(name, True, scripts.constants.WHITE)
        
    def set_show(self, bool):
        self.show = bool
    
    def draw(self, surface):
        if self.show:
            if self.health >= 0:
                surface.blit(self.assets['health_bar'][0],(scripts.constants.DISPLAY_WIDTH - 167, 0))
                pygame.draw.rect(surface ,scripts.constants.RED,(scripts.constants.DISPLAY_WIDTH - 154, 4,(self.health/self.full_health) * 148,10))
                surface.blit(self.assets['health_bar'][1],(scripts.constants.DISPLAY_WIDTH - 167, 0))
                if self.name == 'DRUID':
                    surface.blit(self.show_name,(scripts.constants.DISPLAY_WIDTH - 100, 6))
        