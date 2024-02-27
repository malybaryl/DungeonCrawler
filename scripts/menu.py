import pygame
import scripts.constants
from scripts.load import loadImages, loadCredits, change_values_of_config
from scripts.music import Music
from scripts.changeResolution import changeResolution
import math

class Menu:
    def __init__(self):
        self.assets={
            "buttons": loadImages("HUD/button"),
            "coursor": loadImages("HUD/coursor"),
            "font1": pygame.font.Font("assets/fonts/font.ttf",8),
            "font2": pygame.font.Font("assets/fonts/font.ttf",24),
            "logo": loadImages("HUD/logo")
        }
        self.version = "0.0.6"
        self.pos = pygame.mouse.get_pos()
        self.main_menu = True
        self.settings_menu = False
        self.credits_menu = False
        self.logo_x = 256
        self.logo_y = 64
        self.logo = pygame.transform.scale(self.assets["logo"][0],(self.logo_x,self.logo_y))
        self.answer_YES="YES"
        self.answer_NO="NO"
        self.answer_YES_caption = self.assets["font1"].render(self.answer_YES ,True, scripts.constants.WHITE)
        self.answer_NO_caption = self.assets["font1"].render(self.answer_NO ,True, scripts.constants.WHITE)
        self.play = "PLAY"
        self.play_caption = self.assets["font1"].render(self.play ,True, scripts.constants.WHITE)
        self.play_cliked = False
        self.play_button_to_show = self.assets["buttons"][0]
        self.version_caption = self.assets["font1"].render(self.version ,True, scripts.constants.WHITE)
        self.time = pygame.time.get_ticks()
        self.quit = "QUIT"
        self.quit_caption = self.assets["font1"].render(self.quit ,True, scripts.constants.WHITE)
        self.quit_cliked = False
        self.quit_button_to_show = self.assets["buttons"][0]
        self.settings = "OPTIONS"
        self.settings_caption = self.assets["font1"].render(self.settings ,True, scripts.constants.WHITE)
        self.settings_cliked = False
        self.settings_button_to_show = self.assets["buttons"][0]
        self.back = "BACK"
        self.back_caption = self.assets["font1"].render(self.back ,True, scripts.constants.WHITE)
        self.back_button_to_show = self.assets["buttons"][0]
        self.back_cliked = False
        self.back_credits_button_to_show = self.assets["buttons"][0]
        self.back_credits_cliked = False
        self.resolution = "RESOLUTION: "
        self.resolution_caption = self.assets["font1"].render(self.resolution ,True, scripts.constants.WHITE)
        self.fullscreen = "FULLSCREEN: "
        self.fullscreen_caption = self.assets["font1"].render(self.fullscreen ,True, scripts.constants.WHITE)
        self.music_volume = "MUSIC VOLUME: "
        self.music_volume_caption = self.assets["font1"].render(self.music_volume ,True, scripts.constants.WHITE)
        self.effects_volume = "EFFECTS VOLUME: "
        self.effects_volume_caption = self.assets["font1"].render(self.effects_volume ,True, scripts.constants.WHITE)
        self.save = "SAVE"
        self.save_caption = self.assets["font1"].render(self.save ,True, scripts.constants.WHITE)
        self.save_button_to_show = self.assets["buttons"][0]
        self.save_cliked = False
        self.credits_button_to_show = self.assets["buttons"][2]
        self.credits_cliked = False
        self.resolution_960x540 = "960x540"
        self.resolution_960x540_caption = self.assets["font1"].render(self.resolution_960x540 ,True, scripts.constants.WHITE)
        self.percent_0 = "0%"
        self.percent_10 = "10%"
        self.percent_20 = "20%"
        self.percent_30 = "30%"
        self.percent_40 = "40%"
        self.percent_50 = "50%"
        self.percent_60 = "60%"
        self.percent_70 = "70%"
        self.percent_80 = "80%"
        self.percent_90 = "90%"
        self.percent_100 = "100%"
        self.percent_0_caption = self.assets["font1"].render(self.percent_0 ,True, scripts.constants.WHITE)
        self.percent_10_caption = self.assets["font1"].render(self.percent_10 ,True, scripts.constants.WHITE)
        self.percent_20_caption = self.assets["font1"].render(self.percent_20 ,True, scripts.constants.WHITE)
        self.percent_30_caption = self.assets["font1"].render(self.percent_30 ,True, scripts.constants.WHITE)
        self.percent_40_caption = self.assets["font1"].render(self.percent_40 ,True, scripts.constants.WHITE)
        self.percent_50_caption = self.assets["font1"].render(self.percent_50 ,True, scripts.constants.WHITE)
        self.percent_60_caption = self.assets["font1"].render(self.percent_60 ,True, scripts.constants.WHITE)
        self.percent_70_caption = self.assets["font1"].render(self.percent_70 ,True, scripts.constants.WHITE)
        self.percent_80_caption = self.assets["font1"].render(self.percent_80 ,True, scripts.constants.WHITE)
        self.percent_90_caption = self.assets["font1"].render(self.percent_90 ,True, scripts.constants.WHITE)
        self.percent_100_caption = self.assets["font1"].render(self.percent_100 ,True, scripts.constants.WHITE)
        self.lines = []
        self.credits_to_show= []
        self.y = scripts.constants.DISPLAY_HEIGHT//4
        self.read_once = True
        self.is_fullscreened = scripts.constants.FULLSCREEN
        self.to_save_is_fullscreened = scripts.constants.FULLSCREEN
        self.music_volume_value = scripts.constants.MUSIC_VOLUME
        self.to_save_music_volume = scripts.constants.MUSIC_VOLUME
        self.effects_volume_value = scripts.constants.FX_VOLUME
        self.to_save_effects_volume_value = scripts.constants.FX_VOLUME
        self.is_music = scripts.constants.MUSIC
        self.music_volume_value_caption = self.percent_0_caption
        self.effects_volume_value_caption = self.percent_0_caption
        self.music_volume_clicked = False
        self.fullscreen_clicked = False
        self.effects_volume_clicked = False
        self.raise_up = False
        
    
    def update(self, music, screen, player, bow, enemy_list, boss_list, magic_ball_group):
        self.pos = pygame.mouse.get_pos()
        game = False
        screen = screen
        
        
        # loading credits
        if self.read_once:
            self.lines = loadCredits()
            for line in self.lines:
                text = self.assets["font1"].render(line.strip(), True, scripts.constants.WHITE)
                rect = text.get_rect(center=(scripts.constants.DISPLAY_WIDTH//2, self.y))
                self.y += 15
                self.credits_to_show.append([text,rect])
            self.read_once = False

        if self.main_menu:
            # logo animation handler
            self.logo = pygame.transform.scale(self.assets["logo"][0],(math.floor(self.logo_x), math.floor(self.logo_y)))
            if self.raise_up:
                self.logo_y += 0.1
                self.logo_x += 0.3
            else:
                self.logo_y -= 0.1 
                self.logo_x -= 0.3
            if self.logo_x >= 266:
                self.raise_up = False
            elif self.logo_x <= 246:
                self.raise_up = True
            
            
            
            if pygame.mouse.get_pressed()[0]:
                # if play button is clicked
                if scripts.constants.DISPLAY_WIDTH/2-16 < self.pos[0]/scripts.constants.SCALE_WIDTH < scripts.constants.DISPLAY_WIDTH/2+ 16 and scripts.constants.DISPLAY_HEIGHT/2 < self.pos[1]/scripts.constants.SCALE_HEIGHT < scripts.constants.DISPLAY_HEIGHT/2 + 32:
                    self.play_cliked = True
                    self.time = pygame.time.get_ticks()
                
                # if settings button is clicked
                if scripts.constants.DISPLAY_WIDTH/2-16 < self.pos[0]/scripts.constants.SCALE_WIDTH < scripts.constants.DISPLAY_WIDTH/2+ 16 and scripts.constants.DISPLAY_HEIGHT/2+32 < self.pos[1]/scripts.constants.SCALE_HEIGHT < scripts.constants.DISPLAY_HEIGHT/2 + 32 + 32:
                    self.settings_cliked = True
                    self.time = pygame.time.get_ticks()

                # if quit button is clicked
                if scripts.constants.DISPLAY_WIDTH/2-16 < self.pos[0]/scripts.constants.SCALE_WIDTH < scripts.constants.DISPLAY_WIDTH/2+ 16 and scripts.constants.DISPLAY_HEIGHT/2+64 < self.pos[1]/scripts.constants.SCALE_HEIGHT < scripts.constants.DISPLAY_HEIGHT/2 + 32 +64:
                    self.quit_cliked = True
                    self.time = pygame.time.get_ticks()
                
                # if credits button is clicked
                if 2 < self.pos[0]/scripts.constants.SCALE_WIDTH < 34 and scripts.constants.DISPLAY_HEIGHT-34 < self.pos[1]/scripts.constants.SCALE_HEIGHT < scripts.constants.DISPLAY_HEIGHT-2:
                    self.credits_cliked = True
                    self.time = pygame.time.get_ticks()
            
            # play button deley
            if self.play_cliked:
                self.play_button_to_show = self.assets["buttons"][1]
                if (pygame.time.get_ticks() - self.time) >= 100:
                    game = True
                    self.play_cliked = False
                    self.play_button_to_show = self.assets["buttons"][0]
            
            # settings button deley
            if self.settings_cliked:
                self.settings_button_to_show = self.assets["buttons"][1]
                if (pygame.time.get_ticks() - self.time) >= 100:
                    self.main_menu = False
                    self.settings_menu = True
                    self.settings_cliked = False
                    self.settings_button_to_show = self.assets["buttons"][0]

            # quit button deley
            if self.quit_cliked:
                self.quit_button_to_show = self.assets["buttons"][1]
                if (pygame.time.get_ticks() - self.time) >= 100:
                    pygame.quit()
                    self.quit_cliked = False
                    self.quit_button_to_show = self.assets["buttons"][0]
            
            # credits button deley
            if self.credits_cliked:
                self.credits_button_to_show = self.assets["buttons"][3]
                if (pygame.time.get_ticks() - self.time) >= 100:
                    self.main_menu = False
                    self.credits_menu = True
                    self.credits_cliked = False
                    self.credits_button_to_show = self.assets["buttons"][2]

        if self.settings_menu:
            if pygame.mouse.get_pressed()[0]:
                # if back button is clicked
                if scripts.constants.DISPLAY_WIDTH/2-16-48 < self.pos[0]/scripts.constants.SCALE_WIDTH < scripts.constants.DISPLAY_WIDTH/2+ 16-48 and scripts.constants.DISPLAY_HEIGHT/2+64 < self.pos[1]/scripts.constants.SCALE_HEIGHT < scripts.constants.DISPLAY_HEIGHT/2 + 32 +64:
                    self.back_cliked = True
                    self.time = pygame.time.get_ticks()
                
                # if save button is clicked
                if scripts.constants.DISPLAY_WIDTH/2-16+48 < self.pos[0]/scripts.constants.SCALE_WIDTH < scripts.constants.DISPLAY_WIDTH/2+ 16+48 and scripts.constants.DISPLAY_HEIGHT/2+64 < self.pos[1]/scripts.constants.SCALE_HEIGHT < scripts.constants.DISPLAY_HEIGHT/2 + 32 +64:
                    self.save_cliked = True
                    self.time = pygame.time.get_ticks()

                # fullscreen clicked
                if (scripts.constants.DISPLAY_WIDTH/8) < self.pos[0]/scripts.constants.SCALE_WIDTH < scripts.constants.DISPLAY_WIDTH//2 and scripts.constants.DISPLAY_HEIGHT/8+16 < self.pos[1]/scripts.constants.SCALE_HEIGHT < scripts.constants.DISPLAY_HEIGHT/8 +32:
                    self.fullscreen_clicked = True
                    self.time = pygame.time.get_ticks()

                # music volume clicked
                if (scripts.constants.DISPLAY_WIDTH/8) < self.pos[0]/scripts.constants.SCALE_WIDTH < scripts.constants.DISPLAY_WIDTH//2 and scripts.constants.DISPLAY_HEIGHT/8+32 < self.pos[1]/scripts.constants.SCALE_HEIGHT < scripts.constants.DISPLAY_HEIGHT/8 +48:
                    self.music_volume_clicked = True
                    self.time = pygame.time.get_ticks()

                # fx volume clicked
                if (scripts.constants.DISPLAY_WIDTH/8) < self.pos[0]/scripts.constants.SCALE_WIDTH < scripts.constants.DISPLAY_WIDTH//2 and scripts.constants.DISPLAY_HEIGHT/8+48 < self.pos[1]/scripts.constants.SCALE_HEIGHT < scripts.constants.DISPLAY_HEIGHT/8 +64:
                    self.effects_volume_clicked = True
                    self.time = pygame.time.get_ticks()
                    
            
            # back button deley
            if self.back_cliked:
                self.back_button_to_show = self.assets["buttons"][1]
                if (pygame.time.get_ticks() - self.time) >= 100:
                    self.is_fullscreened = self.to_save_is_fullscreened
                    self.music_volume_value = self.to_save_music_volume
                    self.effects_volume_value = self.to_save_effects_volume_value
                    self.main_menu = True
                    self.settings_menu = False
                    self.back_cliked = False
                    self.back_button_to_show = self.assets["buttons"][0]
            
            # save button deley
            if self.save_cliked:
                self.save_button_to_show = self.assets["buttons"][1]
                if (pygame.time.get_ticks() - self.time) >= 100:
                    # fullscreen handler
                    self.to_save_is_fullscreened = self.is_fullscreened
                    scripts.constants.FULLSCREEN = self.is_fullscreened
                    if self.is_fullscreened == True:
                        change_values_of_config("FULLSCREEN:", "yes")
                        screen = changeResolution((scripts.constants.SCREEN_WIDTH,scripts.constants.SCREEN_HEIGHT),False)
                    else:
                        change_values_of_config("FULLSCREEN:", "no")
                        screen = changeResolution((scripts.constants.SCREEN_WIDTH,scripts.constants.SCREEN_HEIGHT),True)
                    
                    # music volume handler
                    self.to_save_music_volume = self.music_volume_value
                    scripts.constants.MUSIC_VOLUME = self.to_save_music_volume
                    change_values_of_config("MUSIC_VOLUME:", scripts.constants.MUSIC_VOLUME)
                    music.change_volume(scripts.constants.MUSIC_VOLUME)
                    
                    # fx volume handler
                    self.to_save_effects_volume = self.effects_volume_value
                    scripts.constants.FX_VOLUME = self.to_save_effects_volume
                    change_values_of_config("FX_VOLUME:", scripts.constants.FX_VOLUME)
                    music.change_fx_volume(player, bow, enemy_list, boss_list, magic_ball_group)

                    self.save_cliked = False
                    self.save_button_to_show = self.assets["buttons"][0]
            
            # fullscreen button deley
            if self.fullscreen_clicked:
                if (pygame.time.get_ticks() - self.time) >= 100:
                    if self.is_fullscreened:
                        self.is_fullscreened = False
                    else:
                        self.is_fullscreened = True
                    self.fullscreen_clicked = False
            
            # music volume button deley
            if self.music_volume_clicked:
                if (pygame.time.get_ticks() - self.time) >= 100:
                    self.music_volume_value += 0.1
                    if self.music_volume_value >= 1.0:
                        self.music_volume_value = 0.0
                    self.music_volume_clicked = False
            
            # fx volume button deley
            if self.effects_volume_clicked:
                if (pygame.time.get_ticks() - self.time) >= 100:
                    self.effects_volume_value += 0.1
                    if self.effects_volume_value >= 1.0:
                        self.effects_volume_value = 0.0
                    self.effects_volume_clicked = False

            # settings handler
            if self.is_fullscreened:
                self.fullscreen_answer = self.answer_YES_caption
            elif not self.is_fullscreened:
                self.fullscreen_answer = self.answer_NO_caption
            
            
            if self.music_volume_value <= 0.01:
                self.is_music = False
                self.music_volume_value_caption = self.percent_0_caption
            elif 0.01 < self.music_volume_value <= 0.1:
                self.is_music = True
                self.music_volume_value_caption = self.percent_10_caption
            elif 0.1 < self.music_volume_value <= 0.2:
                self.is_music = True
                self.music_volume_value_caption = self.percent_20_caption
            elif 0.2 < self.music_volume_value <= 0.3:
                self.is_music = True
                self.music_volume_value_caption = self.percent_30_caption
            elif 0.3 < self.music_volume_value <= 0.4:
                self.is_music = True
                self.music_volume_value_caption = self.percent_40_caption
            elif 0.4 < self.music_volume_value <= 0.5:
                self.is_music = True
                self.music_volume_value_caption = self.percent_50_caption
            elif 0.5 < self.music_volume_value <= 0.6:
                self.is_music = True
                self.music_volume_value_caption = self.percent_60_caption
            elif 0.6 < self.music_volume_value <= 0.7:
                self.is_music = True
                self.music_volume_value_caption = self.percent_70_caption
            elif 0.7 < self.music_volume_value <= 0.8:
                self.is_music = True
                self.music_volume_value_caption = self.percent_80_caption
            elif 0.8 < self.music_volume_value <= 0.9:
                self.is_music = True
                self.music_volume_value_caption = self.percent_90_caption
            elif 0.9 < self.music_volume_value <= 1:
                self.music_volume_value_caption = self.percent_100_caption
                self.is_music = True
            
            
            
            if self.effects_volume_value <= 0.01:
                self.effects_volume_value_caption = self.percent_0_caption
            elif 0.01 < self.effects_volume_value <= 0.1:
                self.effects_volume_value_caption = self.percent_10_caption
            elif 0.1 < self.effects_volume_value <= 0.2:
                self.effects_volume_value_caption = self.percent_20_caption
            elif 0.2 < self.effects_volume_value <= 0.3:
                self.effects_volume_value_caption = self.percent_30_caption
            elif 0.3 < self.effects_volume_value <= 0.4:
                self.effects_volume_value_caption = self.percent_40_caption
            elif 0.4 < self.effects_volume_value <= 0.5:
                self.effects_volume_value_caption = self.percent_50_caption
            elif 0.5 < self.effects_volume_value <= 0.6:
                self.effects_volume_value_caption = self.percent_60_caption
            elif 0.6 < self.effects_volume_value <= 0.7:
                self.effects_volume_value_caption = self.percent_70_caption
            elif 0.7 < self.effects_volume_value <= 0.8:
                self.effects_volume_value_caption = self.percent_80_caption
            elif 0.8 < self.effects_volume_value <= 0.9:
                self.effects_volume_value_caption = self.percent_90_caption
            elif 0.9 < self.effects_volume_value <= 1:
                self.effects_volume_value_caption = self.percent_100_caption
            else:
                self.effects_volume_value_caption = self.percent_0_caption



        if self.credits_menu:
            if pygame.mouse.get_pressed()[0]:
                # if back button is clicked
                if 6 < self.pos[0]/scripts.constants.SCALE_WIDTH < 48 and scripts.constants.DISPLAY_HEIGHT - 34 < self.pos[1]/scripts.constants.SCALE_HEIGHT < scripts.constants.DISPLAY_HEIGHT - 2:
                    self.back_credits_cliked = True
                    self.time = pygame.time.get_ticks()

            if self.back_credits_cliked:
                self.back_credits_button_to_show = self.assets["buttons"][1]
                if (pygame.time.get_ticks() - self.time) >= 100:
                    self.credits_menu = False
                    self.back_credits_cliked = False
                    self.main_menu = True
                    self.back_credits_button_to_show = self.assets["buttons"][0]

        
        return game


    def draw(self,surface):
        # drawing background
        pygame.draw.rect(surface,scripts.constants.MAINMENU_COLOR,(0,0,scripts.constants.DISPLAY_WIDTH,scripts.constants.DISPLAY_HEIGHT))
        
        if self.main_menu:
            # drawing logo
            surface.blit(self.logo,(scripts.constants.DISPLAY_WIDTH/2-self.logo_x//2,scripts.constants.DISPLAY_HEIGHT/4-self.logo_y//2))

            # drawing buttons
            surface.blit(self.play_button_to_show, ((scripts.constants.DISPLAY_WIDTH/2)-(self.assets["buttons"][0].get_width()/2),scripts.constants.DISPLAY_HEIGHT/2))
            surface.blit(self.play_caption, ((scripts.constants.DISPLAY_WIDTH/2)-(self.assets["buttons"][0].get_width()/4),scripts.constants.DISPLAY_HEIGHT/2 + (self.assets["buttons"][0].get_height()/3)+2))
            
            surface.blit(self.settings_button_to_show, ((scripts.constants.DISPLAY_WIDTH/2)-(self.assets["buttons"][0].get_width()/2),scripts.constants.DISPLAY_HEIGHT/2+32))
            surface.blit(self.settings_caption, ((scripts.constants.DISPLAY_WIDTH/2)-(self.assets["buttons"][0].get_width()/2)+4,scripts.constants.DISPLAY_HEIGHT/2 + (self.assets["buttons"][0].get_height()/3)+2+32))
            
            surface.blit(self.quit_button_to_show, ((scripts.constants.DISPLAY_WIDTH/2)-(self.assets["buttons"][0].get_width()/2),scripts.constants.DISPLAY_HEIGHT/2+64))
            surface.blit(self.quit_caption, ((scripts.constants.DISPLAY_WIDTH/2)-(self.assets["buttons"][0].get_width()/4),scripts.constants.DISPLAY_HEIGHT/2 + (self.assets["buttons"][0].get_height()/3)+2+64))
            
            surface.blit(self.credits_button_to_show, (2,scripts.constants.DISPLAY_HEIGHT - 34))
            
            
            # drawing version
            surface.blit(self.version_caption, (scripts.constants.DISPLAY_WIDTH - 48,scripts.constants.DISPLAY_HEIGHT - 12))
        
        if self.settings_menu:
            # drawing buttons
            surface.blit(self.back_button_to_show, ((scripts.constants.DISPLAY_WIDTH/2)-(self.assets["buttons"][0].get_width()/2) - 48,scripts.constants.DISPLAY_HEIGHT/2+64))
            surface.blit(self.back_caption, ((scripts.constants.DISPLAY_WIDTH/2)-(self.assets["buttons"][0].get_width()/4)- 48,scripts.constants.DISPLAY_HEIGHT/2 + (self.assets["buttons"][0].get_height()/3)+2+64))
            
            surface.blit(self.save_button_to_show, ((scripts.constants.DISPLAY_WIDTH/2)-(self.assets["buttons"][0].get_width()/2) + 48,scripts.constants.DISPLAY_HEIGHT/2+64))
            surface.blit(self.save_caption, ((scripts.constants.DISPLAY_WIDTH/2)-(self.assets["buttons"][0].get_width()/4)+ 48,scripts.constants.DISPLAY_HEIGHT/2 + (self.assets["buttons"][0].get_height()/3)+2+64))

            # drawing setings
            surface.blit(self.resolution_caption, ((scripts.constants.DISPLAY_WIDTH/8),scripts.constants.DISPLAY_HEIGHT/8))
            surface.blit(self.resolution_960x540_caption, ((scripts.constants.DISPLAY_WIDTH/8) + (self.resolution_caption.get_width()),scripts.constants.DISPLAY_HEIGHT/8))
            
            surface.blit(self.fullscreen_caption, ((scripts.constants.DISPLAY_WIDTH/8),scripts.constants.DISPLAY_HEIGHT/8+16))
            surface.blit(self.fullscreen_answer, ((scripts.constants.DISPLAY_WIDTH/8) + (self.fullscreen_caption.get_width()),scripts.constants.DISPLAY_HEIGHT/8+16))
            
            surface.blit(self.music_volume_caption, ((scripts.constants.DISPLAY_WIDTH/8),scripts.constants.DISPLAY_HEIGHT/8+32))
            surface.blit(self.music_volume_value_caption, ((scripts.constants.DISPLAY_WIDTH/8) + (self.music_volume_caption.get_width()),scripts.constants.DISPLAY_HEIGHT/8+32))
            
            surface.blit(self.effects_volume_caption, ((scripts.constants.DISPLAY_WIDTH/8),scripts.constants.DISPLAY_HEIGHT/8+48))
            surface.blit(self.effects_volume_value_caption, ((scripts.constants.DISPLAY_WIDTH/8) + (self.effects_volume_caption.get_width()),scripts.constants.DISPLAY_HEIGHT/8+48))

        if self.credits_menu:
            # drawing buttons
            surface.blit(self.back_credits_button_to_show, (6,scripts.constants.DISPLAY_HEIGHT - 34))
            surface.blit(self.back_caption, (((self.assets["buttons"][0].get_width()/3)-3+4,scripts.constants.DISPLAY_HEIGHT - 22)))

            # drawing credits
            for text in self.credits_to_show:
                surface.blit(text[0],text[1])

        # drawing coursor
        surface.blit(pygame.transform.scale(self.assets["coursor"][0],(24,24)),(self.pos[0]/scripts.constants.SCALE_WIDTH,self.pos[1]/scripts.constants.SCALE_HEIGHT)) 