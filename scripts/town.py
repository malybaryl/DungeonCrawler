import pygame
from scripts.load import loadImages, loadImage
import scripts.constants
import random
import math

class Town():
    def __init__(self):
        self.assets ={
            "town": loadImages("town/png"),
            "coursor": loadImages("HUD/coursor"),
            "hut": loadImages("town/house"),
            "smith": loadImages("town/smith"),
            "wizard_tower": loadImages("town/wizard_tower"),
            "dwarfs_house": loadImages("town/dwarfs_house"),
            "knight_castle": loadImages("town/knight_castle"),
            "pikemen_tower": loadImages("town/pikemen_tower"),
            "canals": loadImages("town/canals"),
            "statue": loadImages("town/statue"),
            "crow": loadImages("town/crow"),
            "upgrade_town": loadImages("town/upgrade_town"),
            "walls": loadImages("town/walls"),
            "font_8": pygame.font.Font("assets/fonts/font.ttf",8),
            "font_16": pygame.font.Font("assets/fonts/font.ttf",16),
            "gold": pygame.transform.scale(loadImage("coin/0.png"),(30,30)),
            "buttons": loadImages("HUD/button"),
            "build_menu_frame": pygame.transform.scale(loadImage("town/build_menu_frame/0.png"),(scripts.constants.DISPLAY_WIDTH*3//4,scripts.constants.DISPLAY_HEIGHT*3//4)),
            "fight_button_menu": loadImage("town/hero_choice/0.png"),
            "player1": pygame.transform.scale(loadImage("char/player1/idle/0.png"),(64,64)),
            "wizard": pygame.transform.scale(loadImage("char/wizard/idle/0.png"),(64,64)),
            "dwarf": pygame.transform.scale(loadImage("char/dwarf/idle/0.png"),(64,64)),
            "knight": pygame.transform.scale(loadImage("char/knight/idle/0.png"),(64,64)),
            "pikemen": pygame.transform.scale(loadImage("char/pikemen/idle/0.png"),(64,64)),
            "elf": pygame.transform.scale(loadImage("char/elf/idle/0.png"),(64,64)),
            "paladin": pygame.transform.scale(loadImage("char/paladin/idle/0.png"),(64,64)),
            "druid": pygame.transform.scale(loadImage("char/druid/idle/0.png"),(64,64))
        }
        self.town_level = 0
        self.gold = scripts.constants.GOLD
        self.gold_text = self.assets["font_8"].render(f"{self.gold}", True, scripts.constants.BLACK)
        self.pos = pygame.mouse.get_pos()
        self.draw_character_pick = False
        self.back_button_to_show = self.assets['buttons'][4]
        self.character_pick_text = 'CHOOSE YOUR HERO'
        self.character_pick_text_to_show = self.assets["font_16"].render(self.character_pick_text, True, scripts.constants.WHITE)
        self.no_hero_text_1 = "You don't have any Heros..."
        self.no_hero_text_1_to_show = self.assets["font_8"].render(self.no_hero_text_1, True, scripts.constants.WHITE)
        self.no_hero_text_2 = "Buy THE HUT in town to recive your first Hero!"
        self.no_hero_text_2_to_show = self.assets["font_8"].render(self.no_hero_text_2, True, scripts.constants.WHITE)
        self.characters = []
        # BUILDINGS
        self.info_cliked = False
            # the_hut
        self.hut_builded = False
        self.hut_cost = 100
        self.hut_cost_text = self.assets["font_8"].render(f"{self.hut_cost}", True, scripts.constants.WHITE)
        self.hut_description_1 = 'The Hut is where'
        self.hut_description_2 = '"The Peasant"'
        self.hut_description_3 = 'lives.'
        self.hut_description_4 = ''
        self.hut_description_5 = ''
        self.hut_description_text_1 = self.assets["font_8"].render(self.hut_description_1, True, scripts.constants.WHITE)
        self.hut_description_text_2 = self.assets["font_8"].render(self.hut_description_2, True, scripts.constants.WHITE)
        self.hut_description_text_3 = self.assets["font_8"].render(self.hut_description_3, True, scripts.constants.WHITE)
        self.hut_description_text_4 = self.assets["font_8"].render(self.hut_description_4, True, scripts.constants.WHITE)
        self.hut_description_text_5 = self.assets["font_8"].render(self.hut_description_5, True, scripts.constants.WHITE)
        self.draw_hut_info = False
        self.hut_cliked = False
            # smith
        self.smith_builded = False
        self.smith_cost = 50
        self.smith_cost_text = self.assets["font_8"].render(f"{self.smith_cost}", True, scripts.constants.WHITE)
        self.smith_description_1 = 'You can buy new'
        self.smith_description_2 = 'weapons here.'
        self.smith_description_3 = 'Required: The Hut'
        self.smith_description_text_1 = self.assets["font_8"].render(self.smith_description_1, True, scripts.constants.WHITE)
        self.smith_description_text_2 = self.assets["font_8"].render(self.smith_description_2, True, scripts.constants.WHITE)
        self.smith_description_text_3 = self.assets["font_8"].render(self.smith_description_3, True, scripts.constants.WHITE)
        self.draw_smith_info = False
        self.smith_cliked = False
            # wizard_tower
        self.wizard_tower_builded = False
        self.wizard_tower_cost = 400
        self.wizard_tower_cost_text = self.assets["font_8"].render(f"{self.wizard_tower_cost}", True, scripts.constants.WHITE)
        self.wizard_tower_description_1 = 'The Wizard Tower'
        self.wizard_tower_description_2 = 'is where "The '
        self.wizard_tower_description_3 = 'Wizard" lives.'
        self.wizard_tower_description_4 = ''
        self.wizard_tower_description_5 = ''
        self.wizard_tower_description_text_1 = self.assets["font_8"].render(self.wizard_tower_description_1, True, scripts.constants.WHITE)
        self.wizard_tower_description_text_2 = self.assets["font_8"].render(self.wizard_tower_description_2, True, scripts.constants.WHITE)
        self.wizard_tower_description_text_3 = self.assets["font_8"].render(self.wizard_tower_description_3, True, scripts.constants.WHITE)
        self.wizard_tower_description_text_4 = self.assets["font_8"].render(self.wizard_tower_description_4, True, scripts.constants.WHITE)
        self.wizard_tower_description_text_5 = self.assets["font_8"].render(self.wizard_tower_description_5, True, scripts.constants.WHITE)
        self.draw_wizard_tower_info = False
        self.wizard_tower_cliked = False
            # dwarfs_house
        self.dwarfs_house_builded = False
        self.dwarfs_house_cost = 400
        self.dwarfs_house_cost_text = self.assets["font_8"].render(f"{self.dwarfs_house_cost}", True, scripts.constants.WHITE)
        self.dwarfs_house_description_1 = "The Dwarf's House"
        self.dwarfs_house_description_2 = 'is the place'
        self.dwarfs_house_description_3 = 'where you can'
        self.dwarfs_house_description_4 = 'meet the great'
        self.dwarfs_house_description_5 = 'warrior "Dwarf".'
        self.dwarfs_house_description_text_1 = self.assets["font_8"].render(self.dwarfs_house_description_1, True, scripts.constants.WHITE)
        self.dwarfs_house_description_text_2 = self.assets["font_8"].render(self.dwarfs_house_description_2, True, scripts.constants.WHITE)
        self.dwarfs_house_description_text_3 = self.assets["font_8"].render(self.dwarfs_house_description_3, True, scripts.constants.WHITE)
        self.dwarfs_house_description_text_4 = self.assets["font_8"].render(self.dwarfs_house_description_4, True, scripts.constants.WHITE)
        self.dwarfs_house_description_text_5 = self.assets["font_8"].render(self.dwarfs_house_description_5, True, scripts.constants.WHITE)
        self.draw_dwarfs_house_info = False
        self.dwarfs_house_cliked = False
            # knight castle
        self.knight_castle_builded = False
        self.knight_castle_cost = 400
        self.knight_castle_cost_text = self.assets["font_8"].render(f"{self.knight_castle_cost}", True, scripts.constants.WHITE)
        self.knight_castle_description_1 = 'The Knight Castle'
        self.knight_castle_description_2 = 'is the mighty '
        self.knight_castle_description_3 = 'place where'
        self.knight_castle_description_4 = 'you can meet'
        self.knight_castle_description_5 = '"Black Knight"'
        self.knight_castle_description_text_1 = self.assets["font_8"].render(self.knight_castle_description_1, True, scripts.constants.WHITE)
        self.knight_castle_description_text_2 = self.assets["font_8"].render(self.knight_castle_description_2, True, scripts.constants.WHITE)
        self.knight_castle_description_text_3 = self.assets["font_8"].render(self.knight_castle_description_3, True, scripts.constants.WHITE)
        self.knight_castle_description_text_4 = self.assets["font_8"].render(self.knight_castle_description_4, True, scripts.constants.WHITE)
        self.knight_castle_description_text_5 = self.assets["font_8"].render(self.knight_castle_description_5, True, scripts.constants.WHITE)
        self.draw_knight_castle_info = False
        self.knight_castle_cliked = False
            # pikemen tower
        self.pikemen_tower_builded = False
        self.pikemen_tower_cost = 400
        self.pikemen_tower_cost_text = self.assets["font_8"].render(f"{self.pikemen_tower_cost}", True, scripts.constants.WHITE)
        self.pikemen_tower_description_1 = 'The Pikemen Tower'
        self.pikemen_tower_description_2 = 'is the tall tower'
        self.pikemen_tower_description_3 = 'where "Pikemen" '
        self.pikemen_tower_description_4 = 'is the guard.'
        self.pikemen_tower_description_5 = ''
        self.pikemen_tower_description_text_1 = self.assets["font_8"].render(self.pikemen_tower_description_1, True, scripts.constants.WHITE)
        self.pikemen_tower_description_text_2 = self.assets["font_8"].render(self.pikemen_tower_description_2, True, scripts.constants.WHITE)
        self.pikemen_tower_description_text_3 = self.assets["font_8"].render(self.pikemen_tower_description_3, True, scripts.constants.WHITE)
        self.pikemen_tower_description_text_4 = self.assets["font_8"].render(self.pikemen_tower_description_4, True, scripts.constants.WHITE)
        self.pikemen_tower_description_text_5 = self.assets["font_8"].render(self.pikemen_tower_description_5, True, scripts.constants.WHITE)
        self.draw_pikemen_tower_info = False
        self.pikemen_tower_cliked = False
            # canals
        self.canals_builded = False
        self.canals_cost = 600
        self.canals_cost_text = self.assets["font_8"].render(f"{self.canals_cost}", True, scripts.constants.WHITE)
        self.canals_description_1 = 'The Canals is'
        self.canals_description_2 = 'the dark place'
        self.canals_description_3 = 'where very bad'
        self.canals_description_4 = 'people lives.'
        self.canals_description_5 = 'Not only people...'
        self.canals_description_text_1 = self.assets["font_8"].render(self.canals_description_1, True, scripts.constants.WHITE)
        self.canals_description_text_2 = self.assets["font_8"].render(self.canals_description_2, True, scripts.constants.WHITE)
        self.canals_description_text_3 = self.assets["font_8"].render(self.canals_description_3, True, scripts.constants.WHITE)
        self.canals_description_text_4 = self.assets["font_8"].render(self.canals_description_4, True, scripts.constants.WHITE)
        self.canals_description_text_5 = self.assets["font_8"].render(self.canals_description_5, True, scripts.constants.WHITE)
        self.draw_canals_info = False
        self.canals_cliked = False
            # statue
        self.statue_builded = False
        self.statue_cost = 1000
        self.statue_cost_text = self.assets["font_8"].render(f"{self.statue_cost}", True, scripts.constants.WHITE)
        self.statue_description_1 = 'The Statue Of'
        self.statue_description_2 = 'Goddest is the'
        self.statue_description_3 = 'most importent'
        self.statue_description_4 = 'being for "The'
        self.statue_description_5 = 'Paladin Knight"'
        self.statue_description_text_1 = self.assets["font_8"].render(self.statue_description_1, True, scripts.constants.WHITE)
        self.statue_description_text_2 = self.assets["font_8"].render(self.statue_description_2, True, scripts.constants.WHITE)
        self.statue_description_text_3 = self.assets["font_8"].render(self.statue_description_3, True, scripts.constants.WHITE)
        self.statue_description_text_4 = self.assets["font_8"].render(self.statue_description_4, True, scripts.constants.WHITE)
        self.statue_description_text_5 = self.assets["font_8"].render(self.statue_description_5, True, scripts.constants.WHITE)
        self.draw_statue_info = False
        self.statue_cliked = False
            # crow
        self.crow_builded = False
        if scripts.constants.DRUID_DEFEAT:
            self.crow_cost = 600
        else:
            self.crow_cost = '???'
        self.crow_cost_text = self.assets["font_8"].render(f"{self.crow_cost}", True, scripts.constants.WHITE)
        self.crow_description_1 = '???'
        self.crow_description_2 = ''
        self.crow_description_3 = ''
        self.crow_description_4 = ''
        self.crow_description_5 = ''
        self.crow_description_text_1 = self.assets["font_8"].render(self.crow_description_1, True, scripts.constants.WHITE)
        self.crow_description_text_2 = self.assets["font_8"].render(self.crow_description_2, True, scripts.constants.WHITE)
        self.crow_description_text_3 = self.assets["font_8"].render(self.crow_description_3, True, scripts.constants.WHITE)
        self.crow_description_text_4 = self.assets["font_8"].render(self.crow_description_4, True, scripts.constants.WHITE)
        self.crow_description_text_5 = self.assets["font_8"].render(self.crow_description_5, True, scripts.constants.WHITE)
        self.draw_crow_info = False
        self.crow_cliked = False
            #upgrade town building
        self.upgrade_town_builded = False
        self.upgrade_town_cost = 150
        self.upgrade_town_cost_text = self.assets["font_8"].render(f"{self.upgrade_town_cost}", True, scripts.constants.WHITE)
        self.upgrade_town_description_1 = 'Upgrade Town'
        self.upgrade_town_description_2 = 'Required: At least'
        self.upgrade_town_description_3 = '5 buildinng in the'
        self.upgrade_town_description_4 = 'town.'
        self.upgrade_town_description_5 = ''
        self.upgrade_town_description_text_1 = self.assets["font_8"].render(self.upgrade_town_description_1, True, scripts.constants.WHITE)
        self.upgrade_town_description_text_2 = self.assets["font_8"].render(self.upgrade_town_description_2, True, scripts.constants.WHITE)
        self.upgrade_town_description_text_3 = self.assets["font_8"].render(self.upgrade_town_description_3, True, scripts.constants.WHITE)
        self.upgrade_town_description_text_4 = self.assets["font_8"].render(self.upgrade_town_description_4, True, scripts.constants.WHITE)
        self.upgrade_town_description_text_5 = self.assets["font_8"].render(self.upgrade_town_description_5, True, scripts.constants.WHITE)
        self.draw_upgrade_town_info = False
        self.upgrade_town_cliked = False
            #upgrade town building
        self.walls_builded = False
        self.walls_cost = 300
        self.walls_cost_text = self.assets["font_8"].render(f"{self.walls_cost}", True, scripts.constants.WHITE)
        self.walls_description_1 = 'The Walls'
        self.walls_description_2 = 'Required: The '
        self.walls_description_3 = 'Wizard Tower,The'
        self.walls_description_4 = 'Knight Castle,'
        self.walls_description_5 = 'The Pikemen Tower.'
        self.walls_description_text_1 = self.assets["font_8"].render(self.walls_description_1, True, scripts.constants.WHITE)
        self.walls_description_text_2 = self.assets["font_8"].render(self.walls_description_2, True, scripts.constants.WHITE)
        self.walls_description_text_3 = self.assets["font_8"].render(self.walls_description_3, True, scripts.constants.WHITE)
        self.walls_description_text_4 = self.assets["font_8"].render(self.walls_description_4, True, scripts.constants.WHITE)
        self.walls_description_text_5 = self.assets["font_8"].render(self.walls_description_5, True, scripts.constants.WHITE)
        self.draw_walls_info = False
        self.walls_cliked = False
        # CLOUDS
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
        self.draw_confim = False
        self.back_button_pressed = False
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
        self.coursor = self.assets["coursor"][4]
        self.pressed = False
        self.pressed_cooldown = 0
        self.smith_menu = False
        self.smith_menu_cliked = False
        

        
        
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
     
    def update(self, build_menu_key_pressed, fight_town_button_pressed):
        self.pos = pygame.mouse.get_pos()
        in_town = True
        fight_button_pressed = False
        self.gold = math.ceil(scripts.constants.GOLD)
        self.gold_text = self.assets["font_8"].render(f"{self.gold}", True, scripts.constants.BLACK)
        if pygame.mouse.get_pressed()[0]:
            self.coursor = self.assets["coursor"][5]
            self.pressed = True
            self.pressed_cooldown = pygame.time.get_ticks()
            if not self.fight_button_pressed:
                # fight menu cliked
                if scripts.constants.DISPLAY_WIDTH-34 < self.pos[0]/scripts.constants.SCALE_WIDTH < scripts.constants.DISPLAY_WIDTH-2 and scripts.constants.DISPLAY_HEIGHT-34 < self.pos[1]/scripts.constants.SCALE_HEIGHT < scripts.constants.DISPLAY_HEIGHT-2:
                        self.fight_button_pressed = True
                        self.time = pygame.time.get_ticks()
                # build menu cliked
                elif 2 < self.pos[0]/scripts.constants.SCALE_WIDTH < 34 and scripts.constants.DISPLAY_HEIGHT-34 < self.pos[1]/scripts.constants.SCALE_HEIGHT < scripts.constants.DISPLAY_HEIGHT-2:
                        self.build_button_pressed = True
                        self.time = pygame.time.get_ticks()
                # character menu cliked
                # ---------------------
                # 36
                
                # smith menu cliked
                elif 70 < self.pos[0]/scripts.constants.SCALE_WIDTH < 102 and scripts.constants.DISPLAY_HEIGHT-34 < self.pos[1]/scripts.constants.SCALE_HEIGHT < scripts.constants.DISPLAY_HEIGHT-2:
                        self.smith_menu_cliked = True
                        self.time = pygame.time.get_ticks()
        
        if self.pressed:
            if pygame.time.get_ticks() - self.pressed_cooldown >= 100:
                self.coursor = self.assets["coursor"][4]
                self.pressed = False
            
        # building menu handler            
        if self.build_menu:
           
            if pygame.mouse.get_pressed()[2]:
                # add here +36 width & height!                                                                        #+ 22 here
                if scripts.constants.DISPLAY_WIDTH/8+4+8 < self.pos[0]/scripts.constants.SCALE_WIDTH < scripts.constants.DISPLAY_WIDTH/8+36+8 and scripts.constants.DISPLAY_HEIGHT/8+4 < self.pos[1]/scripts.constants.SCALE_HEIGHT < scripts.constants.DISPLAY_HEIGHT/8+40:
                    if not self.info_cliked:
                        self.draw_hut_info = True
                    self.info_cliked = True
                elif scripts.constants.DISPLAY_WIDTH/8+40+8 < self.pos[0]/scripts.constants.SCALE_WIDTH < scripts.constants.DISPLAY_WIDTH/8+62+8 and scripts.constants.DISPLAY_HEIGHT/8+4 < self.pos[1]/scripts.constants.SCALE_HEIGHT < scripts.constants.DISPLAY_HEIGHT/8+40:
                    if not self.info_cliked:
                        self.draw_smith_info = True
                    self.info_cliked = True
                elif scripts.constants.DISPLAY_WIDTH/8+76+8 < self.pos[0]/scripts.constants.SCALE_WIDTH < scripts.constants.DISPLAY_WIDTH/8+98+8 and scripts.constants.DISPLAY_HEIGHT/8+4 < self.pos[1]/scripts.constants.SCALE_HEIGHT < scripts.constants.DISPLAY_HEIGHT/8+40:
                    if not self.info_cliked:
                        self.draw_wizard_tower_info = True
                    self.info_cliked = True
                elif scripts.constants.DISPLAY_WIDTH/8+112+8 < self.pos[0]/scripts.constants.SCALE_WIDTH < scripts.constants.DISPLAY_WIDTH/8+134+8 and scripts.constants.DISPLAY_HEIGHT/8+4 < self.pos[1]/scripts.constants.SCALE_HEIGHT < scripts.constants.DISPLAY_HEIGHT/8+40:
                    if not self.info_cliked:
                        self.draw_dwarfs_house_info = True
                    self.info_cliked = True
                elif scripts.constants.DISPLAY_WIDTH/8+148+8 < self.pos[0]/scripts.constants.SCALE_WIDTH < scripts.constants.DISPLAY_WIDTH/8+170+8 and scripts.constants.DISPLAY_HEIGHT/8+4 < self.pos[1]/scripts.constants.SCALE_HEIGHT < scripts.constants.DISPLAY_HEIGHT/8+40:
                    if not self.info_cliked:
                        self.draw_knight_castle_info = True
                    self.info_cliked = True
                elif scripts.constants.DISPLAY_WIDTH/8+184+8 < self.pos[0]/scripts.constants.SCALE_WIDTH < scripts.constants.DISPLAY_WIDTH/8+206+8 and scripts.constants.DISPLAY_HEIGHT/8+4 < self.pos[1]/scripts.constants.SCALE_HEIGHT < scripts.constants.DISPLAY_HEIGHT/8+40:
                    if not self.info_cliked:
                        self.draw_pikemen_tower_info = True
                    self.info_cliked = True
                elif scripts.constants.DISPLAY_WIDTH/8+220+8 < self.pos[0]/scripts.constants.SCALE_WIDTH < scripts.constants.DISPLAY_WIDTH/8+242+8 and scripts.constants.DISPLAY_HEIGHT/8+4 < self.pos[1]/scripts.constants.SCALE_HEIGHT < scripts.constants.DISPLAY_HEIGHT/8+40:
                    if not self.info_cliked:
                        self.draw_canals_info = True
                    self.info_cliked = True
                elif scripts.constants.DISPLAY_WIDTH/8+256+8 < self.pos[0]/scripts.constants.SCALE_WIDTH < scripts.constants.DISPLAY_WIDTH/8+278+8 and scripts.constants.DISPLAY_HEIGHT/8+4 < self.pos[1]/scripts.constants.SCALE_HEIGHT < scripts.constants.DISPLAY_HEIGHT/8+40:
                    if not self.info_cliked:
                        self.draw_statue_info = True
                    self.info_cliked = True
                elif scripts.constants.DISPLAY_WIDTH/8+292+8 < self.pos[0]/scripts.constants.SCALE_WIDTH < scripts.constants.DISPLAY_WIDTH/8+314+8 and scripts.constants.DISPLAY_HEIGHT/8+4 < self.pos[1]/scripts.constants.SCALE_HEIGHT < scripts.constants.DISPLAY_HEIGHT/8+40:
                    if not self.info_cliked:
                        self.draw_crow_info = True
                    self.info_cliked = True
                elif scripts.constants.DISPLAY_WIDTH/8+4+8 < self.pos[0]/scripts.constants.SCALE_WIDTH < scripts.constants.DISPLAY_WIDTH/8+36+8 and scripts.constants.DISPLAY_HEIGHT/8+4+32+4 < self.pos[1]/scripts.constants.SCALE_HEIGHT < scripts.constants.DISPLAY_HEIGHT/8+40 + 32 + 4:
                    if not self.info_cliked:
                        self.draw_upgrade_town_info = True
                    self.info_cliked = True
                elif scripts.constants.DISPLAY_WIDTH/8+40+8 < self.pos[0]/scripts.constants.SCALE_WIDTH < scripts.constants.DISPLAY_WIDTH/8+62+8 and scripts.constants.DISPLAY_HEIGHT/8+4+32+4 < self.pos[1]/scripts.constants.SCALE_HEIGHT < scripts.constants.DISPLAY_HEIGHT/8+40 + 32 + 4:
                    if not self.info_cliked:
                        self.draw_walls_info = True
                    self.info_cliked = True
            else:
                self.info_cliked = False
                self.draw_hut_info = False
                self.draw_smith_info = False
                self.draw_wizard_tower_info = False
                self.draw_dwarfs_house_info = False
                self.draw_knight_castle_info = False
                self.draw_pikemen_tower_info = False
                self.draw_canals_info = False
                self.draw_statue_info = False
                self.draw_crow_info = False
                self.draw_upgrade_town_info = False
                self.draw_walls_info = False
                
            if pygame.mouse.get_pressed()[0]:
                if scripts.constants.DISPLAY_WIDTH/8+4+8 < self.pos[0]/scripts.constants.SCALE_WIDTH < scripts.constants.DISPLAY_WIDTH/8+36+8 and scripts.constants.DISPLAY_HEIGHT/8+4 < self.pos[1]/scripts.constants.SCALE_HEIGHT < scripts.constants.DISPLAY_HEIGHT/8+40:
                    self.hut_cliked = True
                if scripts.constants.DISPLAY_WIDTH/8+40+8 < self.pos[0]/scripts.constants.SCALE_WIDTH < scripts.constants.DISPLAY_WIDTH/8+62+8 and scripts.constants.DISPLAY_HEIGHT/8+4 < self.pos[1]/scripts.constants.SCALE_HEIGHT < scripts.constants.DISPLAY_HEIGHT/8+40:
                    self.smith_cliked = True
                if scripts.constants.DISPLAY_WIDTH/8+76+8 < self.pos[0]/scripts.constants.SCALE_WIDTH < scripts.constants.DISPLAY_WIDTH/8+98+8 and scripts.constants.DISPLAY_HEIGHT/8+4 < self.pos[1]/scripts.constants.SCALE_HEIGHT < scripts.constants.DISPLAY_HEIGHT/8+40:
                    self.wizard_tower_cliked = True
                if scripts.constants.DISPLAY_WIDTH/8+112+8 < self.pos[0]/scripts.constants.SCALE_WIDTH < scripts.constants.DISPLAY_WIDTH/8+134+8 and scripts.constants.DISPLAY_HEIGHT/8+4 < self.pos[1]/scripts.constants.SCALE_HEIGHT < scripts.constants.DISPLAY_HEIGHT/8+40:
                    self.dwarfs_house_cliked = True
                if scripts.constants.DISPLAY_WIDTH/8+148+8 < self.pos[0]/scripts.constants.SCALE_WIDTH < scripts.constants.DISPLAY_WIDTH/8+170+8 and scripts.constants.DISPLAY_HEIGHT/8+4 < self.pos[1]/scripts.constants.SCALE_HEIGHT < scripts.constants.DISPLAY_HEIGHT/8+40:
                    self.knight_castle_cliked = True
                if scripts.constants.DISPLAY_WIDTH/8+184+8 < self.pos[0]/scripts.constants.SCALE_WIDTH < scripts.constants.DISPLAY_WIDTH/8+206+8 and scripts.constants.DISPLAY_HEIGHT/8+4 < self.pos[1]/scripts.constants.SCALE_HEIGHT < scripts.constants.DISPLAY_HEIGHT/8+40:
                    self.pikemen_tower_cliked = True
                if scripts.constants.DISPLAY_WIDTH/8+220+8 < self.pos[0]/scripts.constants.SCALE_WIDTH < scripts.constants.DISPLAY_WIDTH/8+242+8 and scripts.constants.DISPLAY_HEIGHT/8+4 < self.pos[1]/scripts.constants.SCALE_HEIGHT < scripts.constants.DISPLAY_HEIGHT/8+40:
                    self.canals_cliked = True
                if scripts.constants.DISPLAY_WIDTH/8+256+8 < self.pos[0]/scripts.constants.SCALE_WIDTH < scripts.constants.DISPLAY_WIDTH/8+278+8 and scripts.constants.DISPLAY_HEIGHT/8+4 < self.pos[1]/scripts.constants.SCALE_HEIGHT < scripts.constants.DISPLAY_HEIGHT/8+40:
                    self.statue_cliked = True
                if scripts.constants.DISPLAY_WIDTH/8+292+8 < self.pos[0]/scripts.constants.SCALE_WIDTH < scripts.constants.DISPLAY_WIDTH/8+314+8 and scripts.constants.DISPLAY_HEIGHT/8+4 < self.pos[1]/scripts.constants.SCALE_HEIGHT < scripts.constants.DISPLAY_HEIGHT/8+40:
                    self.crow_cliked = True
                if scripts.constants.DISPLAY_WIDTH/8+4+8 < self.pos[0]/scripts.constants.SCALE_WIDTH < scripts.constants.DISPLAY_WIDTH/8+36+8 and scripts.constants.DISPLAY_HEIGHT/8+4+32+4 < self.pos[1]/scripts.constants.SCALE_HEIGHT < scripts.constants.DISPLAY_HEIGHT/8+40 + 32 + 4:
                    self.upgrade_town_cliked = True
                if scripts.constants.DISPLAY_WIDTH/8+40+8 < self.pos[0]/scripts.constants.SCALE_WIDTH < scripts.constants.DISPLAY_WIDTH/8+62+8 and scripts.constants.DISPLAY_HEIGHT/8+4+32+4 < self.pos[1]/scripts.constants.SCALE_HEIGHT < scripts.constants.DISPLAY_HEIGHT/8+40 + 32 + 4:
                    self.walls_cliked = True
                
            if self.hut_cliked:
                if not self.hut_builded:
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
                            self.town_level += 1
                            scripts.constants.GOLD -= self.hut_cost
                            scripts.constants.AMOUNT_OF_HEROS += 1
                            self.characters.append('player1')
                            self.hut_cliked = False
                        elif answer > 1.5 and answer < 2.5:
                            self.hut_cliked = False
                    else:
                        self.hut_cliked = False
                else:
                        self.hut_cliked = False
                
            if self.smith_cliked:
                if self.hut_builded and not self.smith_builded:
                    if self.smith_cost <= self.gold and self.hut_builded:
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
                            self.town_level += 1
                            scripts.constants.GOLD -= self.smith_cost
                            self.smith_cliked = False
                        elif answer > 1.5 and answer < 2.5:
                            self.smith_cliked = False
                    else:
                        self.smith_cliked = False
                else:
                        self.smith_cliked = False
                
            if self.wizard_tower_cliked:
                if not self.wizard_tower_builded:
                    if self.wizard_tower_cost <= self.gold:
                        self.confim_text_line_1 = 'Are you sure you' 
                        self.confim_text_line_2 = 'want to build'
                        self.confim_text_line_3 = '"The Wizard Tower"'
                        self.confim_text_line_4 = f'? Cost:{self.wizard_tower_cost}'
                        self.confim_text_line_5 = 'gold'
                        self.confim_text_to_show_1 = self.assets["font_8"].render(self.confim_text_line_1,True,scripts.constants.WHITE)        
                        self.confim_text_to_show_2 = self.assets["font_8"].render(self.confim_text_line_2,True,scripts.constants.WHITE)        
                        self.confim_text_to_show_3 = self.assets["font_8"].render(self.confim_text_line_3,True,scripts.constants.WHITE)        
                        self.confim_text_to_show_4 = self.assets["font_8"].render(self.confim_text_line_4,True,scripts.constants.WHITE)        
                        self.confim_text_to_show_4 = self.assets["font_8"].render(self.confim_text_line_5,True,scripts.constants.WHITE)        
                        answer, self.draw_confim = self.confim()
                        if answer > 0.5 and answer < 1.5:
                            self.wizard_tower_builded = True
                            self.town_level += 1
                            scripts.constants.GOLD -= self.wizard_tower_cost
                            scripts.constants.AMOUNT_OF_HEROS += 1
                            self.characters.append('wizard')
                            self.wizard_tower_cliked = False
                        elif answer > 1.5 and answer < 2.5:
                            self.wizard_tower_cliked = False
                    else:
                        self.wizard_tower_cliked = False
                else:
                        self.wizard_tower_cliked = False
            
            if self.dwarfs_house_cliked:
                if not self.dwarfs_house_builded:
                    if self.dwarfs_house_cost <= self.gold:
                        self.dwarfs_house_line_1 = 'Are you sure you' 
                        self.dwarfs_house_line_2 = 'want to build'
                        self.dwarfs_house_line_3 = '"The Wizard Tower"'
                        self.dwarfs_house_line_4 = f'? Cost:{self.dwarfs_house_cost}'
                        self.dwarfs_house_line_5 = 'gold'
                        self.dwarfs_house_to_show_1 = self.assets["font_8"].render(self.confim_text_line_1,True,scripts.constants.WHITE)        
                        self.dwarfs_house_to_show_2 = self.assets["font_8"].render(self.confim_text_line_2,True,scripts.constants.WHITE)        
                        self.dwarfs_house_to_show_3 = self.assets["font_8"].render(self.confim_text_line_3,True,scripts.constants.WHITE)        
                        self.dwarfs_house_to_show_4 = self.assets["font_8"].render(self.confim_text_line_4,True,scripts.constants.WHITE)        
                        self.dwarfs_house_to_show_4 = self.assets["font_8"].render(self.confim_text_line_5,True,scripts.constants.WHITE)        
                        answer, self.draw_confim = self.confim()
                        if answer > 0.5 and answer < 1.5:
                            self.dwarfs_house_builded = True
                            self.town_level += 1
                            scripts.constants.GOLD -= self.dwarfs_house_cost
                            scripts.constants.AMOUNT_OF_HEROS += 1
                            self.characters.append('dwarf')
                            self.dwarfs_house_cliked = False
                        elif answer > 1.5 and answer < 2.5:
                            self.dwarfs_house_cliked = False
                    else:
                        self.dwarfs_house_cliked = False
                else:
                        self.dwarfs_house_cliked = False
            
            if self.knight_castle_cliked:
                if not self.knight_castle_builded:
                    if self.knight_castle_cost <= self.gold:
                        self.knight_castle_line_1 = 'Are you sure you' 
                        self.knight_castle_line_2 = 'want to build'
                        self.knight_castle_line_3 = '"The Wizard Tower"'
                        self.knight_castle_line_4 = f'? Cost:{self.knight_castle_cost}'
                        self.knight_castle_line_5 = 'gold'
                        self.knight_castle_to_show_1 = self.assets["font_8"].render(self.confim_text_line_1,True,scripts.constants.WHITE)        
                        self.knight_castle_to_show_2 = self.assets["font_8"].render(self.confim_text_line_2,True,scripts.constants.WHITE)        
                        self.knight_castle_to_show_3 = self.assets["font_8"].render(self.confim_text_line_3,True,scripts.constants.WHITE)        
                        self.knight_castle_to_show_4 = self.assets["font_8"].render(self.confim_text_line_4,True,scripts.constants.WHITE)        
                        self.knight_castle_to_show_4 = self.assets["font_8"].render(self.confim_text_line_5,True,scripts.constants.WHITE)        
                        answer, self.draw_confim = self.confim()
                        if answer > 0.5 and answer < 1.5:
                            self.knight_castle_builded = True
                            self.town_level += 1
                            scripts.constants.GOLD -= self.knight_castle_cost
                            scripts.constants.AMOUNT_OF_HEROS += 1
                            self.characters.append('knight')
                            self.knight_castle_cliked = False
                        elif answer > 1.5 and answer < 2.5:
                            self.knight_castle_cliked = False
                    else:
                        self.knight_castle_cliked = False
                else:
                        self.knight_castle_cliked = False
            
            if self.pikemen_tower_cliked:
                if not self.pikemen_tower_builded:
                    if self.pikemen_tower_cost <= self.gold:
                        self.pikemen_tower_line_1 = 'Are you sure you' 
                        self.pikemen_tower_line_2 = 'want to build'
                        self.pikemen_tower_line_3 = '"The Hut"? Cost:'
                        self.pikemen_tower_line_4 = f'{self.pikemen_tower_cost} gold'
                        self.pikemen_tower_line_5 = ''
                        self.pikemen_tower_to_show_1 = self.assets["font_8"].render(self.pikemen_tower_line_1,True,scripts.constants.WHITE)        
                        self.pikemen_tower_to_show_2 = self.assets["font_8"].render(self.pikemen_tower_line_2,True,scripts.constants.WHITE)        
                        self.pikemen_tower_to_show_3 = self.assets["font_8"].render(self.pikemen_tower_line_3,True,scripts.constants.WHITE)        
                        self.pikemen_tower_to_show_4 = self.assets["font_8"].render(self.pikemen_tower_line_4,True,scripts.constants.WHITE)        
                        self.pikemen_tower_to_show_4 = self.assets["font_8"].render(self.pikemen_tower_line_5,True,scripts.constants.WHITE)        
                        answer, self.draw_confim = self.confim()
                        if answer > 0.5 and answer < 1.5:
                            self.pikemen_tower_builded = True
                            self.town_level += 1
                            scripts.constants.GOLD -= self.pikemen_tower_cost
                            scripts.constants.AMOUNT_OF_HEROS += 1
                            self.characters.append('pikemen')
                            self.pikemen_tower_cliked = False
                        elif answer > 1.5 and answer < 2.5:
                            self.pikemen_tower_cliked = False
                    else:
                        self.pikemen_tower_cliked = False
                else:
                        self.pikemen_tower_cliked = False
            
            if self.canals_cliked:
                if not self.canals_builded:
                    if self.canals_cost <= self.gold:
                        self.canals_line_1 = 'Are you sure you' 
                        self.canals_line_2 = 'want to build'
                        self.canals_line_3 = '"The Hut"? Cost:'
                        self.canals_line_4 = f'{self.canals_cost} gold'
                        self.canals_line_5 = ''
                        self.canals_to_show_1 = self.assets["font_8"].render(self.canals_line_1,True,scripts.constants.WHITE)        
                        self.canals_to_show_2 = self.assets["font_8"].render(self.canals_line_2,True,scripts.constants.WHITE)        
                        self.canals_to_show_3 = self.assets["font_8"].render(self.canals_line_3,True,scripts.constants.WHITE)        
                        self.canals_to_show_4 = self.assets["font_8"].render(self.canals_line_4,True,scripts.constants.WHITE)        
                        self.canals_to_show_4 = self.assets["font_8"].render(self.canals_line_5,True,scripts.constants.WHITE)        
                        answer, self.draw_confim = self.confim()
                        if answer > 0.5 and answer < 1.5:
                            self.canals_builded = True
                            self.town_level += 1
                            scripts.constants.GOLD -= self.canals_cost
                            scripts.constants.AMOUNT_OF_HEROS += 1
                            self.characters.append('elf')
                            self.canals_cliked = False
                        elif answer > 1.5 and answer < 2.5:
                            self.canals_cliked = False
                    else:
                        self.canals_cliked = False
                else:
                        self.canals_cliked = False
            
            if self.statue_cliked:
                if not self.statue_builded:
                    if self.statue_cost <= self.gold:
                        self.statue_line_1 = 'Are you sure you' 
                        self.statue_line_2 = 'want to build'
                        self.statue_line_3 = '"The Hut"? Cost:'
                        self.statue_line_4 = f'{self.statue_cost} gold'
                        self.statue_line_5 = ''
                        self.statue_to_show_1 = self.assets["font_8"].render(self.statue_line_1,True,scripts.constants.WHITE)        
                        self.statue_to_show_2 = self.assets["font_8"].render(self.statue_line_2,True,scripts.constants.WHITE)        
                        self.statue_to_show_3 = self.assets["font_8"].render(self.statue_line_3,True,scripts.constants.WHITE)        
                        self.statue_to_show_4 = self.assets["font_8"].render(self.statue_line_4,True,scripts.constants.WHITE)        
                        self.statue_to_show_4 = self.assets["font_8"].render(self.statue_line_5,True,scripts.constants.WHITE)        
                        answer, self.draw_confim = self.confim()
                        if answer > 0.5 and answer < 1.5:
                            self.statue_builded = True
                            self.town_level += 1
                            scripts.constants.GOLD -= self.statue_cost
                            scripts.constants.AMOUNT_OF_HEROS += 1
                            self.characters.append('paladin')
                            self.statue_cliked = False
                        elif answer > 1.5 and answer < 2.5:
                            self.statue_cliked = False
                    else:
                        self.statue_cliked = False
                else:
                        self.statue_cliked = False
            
            if self.crow_cliked:
                if not self.crow_builded:
                    if scripts.constants.DRUID_DEFEAT:
                        if self.crow_cost <= self.gold:
                            self.crow_line_1 = 'Are you sure you' 
                            self.crow_line_2 = 'want to build'
                            self.crow_line_3 = '"The Hut"? Cost:'
                            self.crow_line_4 = f'{self.crow_cost} gold'
                            self.crow_line_5 = ''
                            self.crow_to_show_1 = self.assets["font_8"].render(self.crow_line_1,True,scripts.constants.WHITE)        
                            self.crow_to_show_2 = self.assets["font_8"].render(self.crow_line_2,True,scripts.constants.WHITE)        
                            self.crow_to_show_3 = self.assets["font_8"].render(self.crow_line_3,True,scripts.constants.WHITE)        
                            self.crow_to_show_4 = self.assets["font_8"].render(self.crow_line_4,True,scripts.constants.WHITE)        
                            self.crow_to_show_4 = self.assets["font_8"].render(self.crow_line_5,True,scripts.constants.WHITE)        
                            answer, self.draw_confim = self.confim()
                            if answer > 0.5 and answer < 1.5:
                                self.crow_builded = True
                                self.town_level += 1
                                scripts.constants.GOLD -= self.crow_cost
                                scripts.constants.AMOUNT_OF_HEROS += 1
                                self.characters.append('druid')
                                self.crow_cliked = False
                            elif answer > 1.5 and answer < 2.5:
                                self.crow_cliked = False
                        else:
                            self.crow_cliked = False
                    else:
                        self.crow_cliked = False
                else:
                    self.crow_cliked = False
            
            if self.upgrade_town_cliked:
                if not self.upgrade_town_builded:
                    if self.town_level >= 5:
                        if self.upgrade_town_cost <= self.gold:
                            self.upgrade_town_line_1 = 'Are you sure you' 
                            self.upgrade_town_line_2 = 'want to build'
                            self.upgrade_town_line_3 = '"The Hut"? Cost:'
                            self.upgrade_town_line_4 = f'{self.crow_cost} gold'
                            self.upgrade_town_line_5 = ''
                            self.upgrade_town_to_show_1 = self.assets["font_8"].render(self.upgrade_town_line_1,True,scripts.constants.WHITE)        
                            self.upgrade_town_to_show_2 = self.assets["font_8"].render(self.upgrade_town_line_2,True,scripts.constants.WHITE)        
                            self.upgrade_town_to_show_3 = self.assets["font_8"].render(self.upgrade_town_line_3,True,scripts.constants.WHITE)        
                            self.upgrade_town_to_show_4 = self.assets["font_8"].render(self.upgrade_town_line_4,True,scripts.constants.WHITE)        
                            self.upgrade_town_to_show_4 = self.assets["font_8"].render(self.upgrade_town_line_5,True,scripts.constants.WHITE)        
                            answer, self.draw_confim = self.confim()
                            if answer > 0.5 and answer < 1.5:
                                self.upgrade_town_builded = True
                                self.town_level += 1
                                scripts.constants.GOLD -= self.upgrade_town_cost
                                self.upgrade_town_cliked = False
                            elif answer > 1.5 and answer < 2.5:
                                self.upgrade_town_cliked = False
                        else:
                            self.upgrade_town_cliked = False
                    else:
                        self.upgrade_town_cliked = False
                else:
                    self.upgrade_town_cliked = False
            
            if self.walls_cliked:
                if not self.walls_builded:
                    if self.wizard_tower_builded and self.knight_castle_builded and self.pikemen_tower_builded:
                        if self.walls_cost <= self.gold:
                            self.walls_line_1 = 'Are you sure you' 
                            self.walls_line_2 = 'want to build'
                            self.walls_line_3 = '"The Hut"? Cost:'
                            self.walls_line_4 = f'{self.crow_cost} gold'
                            self.walls_line_5 = ''
                            self.walls_to_show_1 = self.assets["font_8"].render(self.walls_line_1,True,scripts.constants.WHITE)        
                            self.walls_to_show_2 = self.assets["font_8"].render(self.walls_line_2,True,scripts.constants.WHITE)        
                            self.walls_to_show_3 = self.assets["font_8"].render(self.walls_line_3,True,scripts.constants.WHITE)        
                            self.walls_to_show_4 = self.assets["font_8"].render(self.walls_line_4,True,scripts.constants.WHITE)        
                            self.walls_to_show_4 = self.assets["font_8"].render(self.walls_line_5,True,scripts.constants.WHITE)        
                            answer, self.draw_confim = self.confim()
                            if answer > 0.5 and answer < 1.5:
                                self.walls_builded = True
                                self.town_level += 1
                                scripts.constants.GOLD -= self.walls_cost
                                self.walls_cliked = False
                            elif answer > 1.5 and answer < 2.5:
                                self.walls_cliked = False
                        else:
                            self.walls_cliked = False
                    else:
                        self.walls_cliked = False
                else:
                        self.walls_cliked = False
        
        # smith menu handler
        if self.smith_menu:
            pass
              
        if build_menu_key_pressed:
            if not self.fight_button_pressed:
                if self.build_menu:
                    self.build_menu = False
                    build_menu_key_pressed = False
                else:
                    self.build_menu = True
                    build_menu_key_pressed = False
            
        if self.build_button_pressed:
            if not self.fight_button_pressed:
                if (pygame.time.get_ticks() - self.time) >= 100:
                    if self.build_menu:
                        self.build_menu = False
                        self.build_button_pressed = False
                    else:
                        self.build_menu = True
                        self.build_button_pressed = False
            
        if self.smith_menu_cliked:
            if not self.fight_button_pressed:
                if (pygame.time.get_ticks() - self.time) >= 100:
                    if self.smith_menu:
                        self.smith_menu = False
                        self.smith_menu_cliked = False
                    else:
                        self.smith_menu = True
                        self.smith_menu_cliked = False
                    
        if fight_town_button_pressed:
            if self.fight_button_pressed:
                self.fight_button_pressed = False
                self.draw_character_pick = False
            else:
                self.fight_button_pressed = True
                self.draw_character_pick = True    
    
            
        if self.fight_button_pressed:
            self.build_menu = False
            self.draw_character_pick = True
                    
            if pygame.mouse.get_pressed()[0]:
                if 5 < self.pos[0]/scripts.constants.SCALE_WIDTH < 5+32 and scripts.constants.DISPLAY_HEIGHT-34 < self.pos[1]/scripts.constants.SCALE_HEIGHT < scripts.constants.DISPLAY_HEIGHT-2:
                    self.back_button_pressed = True
                    self.back_button_to_show = self.assets['buttons'][7]
                    self.time = pygame.time.get_ticks() 
                        
                if scripts.constants.AMOUNT_OF_HEROS > 0.5 and scripts.constants.AMOUNT_OF_HEROS < 1.5:
                    if scripts.constants.DISPLAY_WIDTH//2-32 < self.pos[0]/scripts.constants.SCALE_WIDTH < scripts.constants.DISPLAY_WIDTH//2-32+64 and scripts.constants.DISPLAY_HEIGHT//2-32 < self.pos[1]/scripts.constants.SCALE_HEIGHT < scripts.constants.DISPLAY_HEIGHT//2-32+64:
                        scripts.constants.HERO = self.characters[0]
                        in_town = False
                        fight_button_pressed = True 
                        self.fight_button_pressed = False
                        self.draw_character_pick = False
                            
                elif scripts.constants.AMOUNT_OF_HEROS > 1.5 and scripts.constants.AMOUNT_OF_HEROS < 2.5:
                    if scripts.constants.DISPLAY_WIDTH//2-32-32 < self.pos[0]/scripts.constants.SCALE_WIDTH < scripts.constants.DISPLAY_WIDTH//2-32-32+64 and scripts.constants.DISPLAY_HEIGHT//2-32 < self.pos[1]/scripts.constants.SCALE_HEIGHT < scripts.constants.DISPLAY_HEIGHT//2-32+64:
                        scripts.constants.HERO = self.characters[0]
                        in_town = False
                        fight_button_pressed = True 
                        self.fight_button_pressed = False
                        self.draw_character_pick = False
                            
                    elif scripts.constants.DISPLAY_WIDTH//2-32+32 < self.pos[0]/scripts.constants.SCALE_WIDTH < scripts.constants.DISPLAY_WIDTH//2-32+32+64 and scripts.constants.DISPLAY_HEIGHT//2-32 < self.pos[1]/scripts.constants.SCALE_HEIGHT < scripts.constants.DISPLAY_HEIGHT//2-32+64:
                        scripts.constants.HERO = self.characters[1]
                        in_town = False
                        self.fight_button_pressed = False
                        self.draw_character_pick = False  
                        fight_button_pressed = True
                
                elif scripts.constants.AMOUNT_OF_HEROS > 2.5 and scripts.constants.AMOUNT_OF_HEROS < 3.5:
                    if scripts.constants.DISPLAY_WIDTH//2-80 < self.pos[0]/scripts.constants.SCALE_WIDTH < scripts.constants.DISPLAY_WIDTH//2-16 and scripts.constants.DISPLAY_HEIGHT//2-32 < self.pos[1]/scripts.constants.SCALE_HEIGHT < scripts.constants.DISPLAY_HEIGHT//2-32+64:
                        scripts.constants.HERO = self.characters[0]
                        in_town = False
                        fight_button_pressed = True 
                        self.fight_button_pressed = False
                        self.draw_character_pick = False
                            
                    elif scripts.constants.DISPLAY_WIDTH//2-32 < self.pos[0]/scripts.constants.SCALE_WIDTH < scripts.constants.DISPLAY_WIDTH//2+32 and scripts.constants.DISPLAY_HEIGHT//2-32 < self.pos[1]/scripts.constants.SCALE_HEIGHT < scripts.constants.DISPLAY_HEIGHT//2-32+64:
                        scripts.constants.HERO = self.characters[1]
                        in_town = False
                        self.fight_button_pressed = False
                        self.draw_character_pick = False  
                        fight_button_pressed = True
                    
                    elif scripts.constants.DISPLAY_WIDTH//2+16 < self.pos[0]/scripts.constants.SCALE_WIDTH < scripts.constants.DISPLAY_WIDTH//2+80 and scripts.constants.DISPLAY_HEIGHT//2-32 < self.pos[1]/scripts.constants.SCALE_HEIGHT < scripts.constants.DISPLAY_HEIGHT//2-32+64:
                        scripts.constants.HERO = self.characters[2]
                        in_town = False
                        self.fight_button_pressed = False
                        self.draw_character_pick = False  
                        fight_button_pressed = True
                
                elif scripts.constants.AMOUNT_OF_HEROS > 3.5 and scripts.constants.AMOUNT_OF_HEROS < 4.5:
                    if scripts.constants.DISPLAY_WIDTH//2-128 < self.pos[0]/scripts.constants.SCALE_WIDTH < scripts.constants.DISPLAY_WIDTH//2-64 and scripts.constants.DISPLAY_HEIGHT//2-32 < self.pos[1]/scripts.constants.SCALE_HEIGHT < scripts.constants.DISPLAY_HEIGHT//2-32+64:
                        scripts.constants.HERO = self.characters[0]
                        in_town = False
                        fight_button_pressed = True 
                        self.fight_button_pressed = False
                        self.draw_character_pick = False
                            
                    elif scripts.constants.DISPLAY_WIDTH//2-64 < self.pos[0]/scripts.constants.SCALE_WIDTH < scripts.constants.DISPLAY_WIDTH//2 and scripts.constants.DISPLAY_HEIGHT//2-32 < self.pos[1]/scripts.constants.SCALE_HEIGHT < scripts.constants.DISPLAY_HEIGHT//2-32+64:
                        scripts.constants.HERO = self.characters[1]
                        in_town = False
                        self.fight_button_pressed = False
                        self.draw_character_pick = False  
                        fight_button_pressed = True
                    
                    elif scripts.constants.DISPLAY_WIDTH//2 < self.pos[0]/scripts.constants.SCALE_WIDTH < scripts.constants.DISPLAY_WIDTH//2+64 and scripts.constants.DISPLAY_HEIGHT//2-32 < self.pos[1]/scripts.constants.SCALE_HEIGHT < scripts.constants.DISPLAY_HEIGHT//2-32+64:
                        scripts.constants.HERO = self.characters[2]
                        in_town = False
                        self.fight_button_pressed = False
                        self.draw_character_pick = False  
                        fight_button_pressed = True
                    
                    elif scripts.constants.DISPLAY_WIDTH//2 + 64 < self.pos[0]/scripts.constants.SCALE_WIDTH < scripts.constants.DISPLAY_WIDTH//2+ 128 and scripts.constants.DISPLAY_HEIGHT//2-32 < self.pos[1]/scripts.constants.SCALE_HEIGHT < scripts.constants.DISPLAY_HEIGHT//2-32+64:
                        scripts.constants.HERO = self.characters[3]
                        in_town = False
                        self.fight_button_pressed = False
                        self.draw_character_pick = False  
                        fight_button_pressed = True
                
                elif scripts.constants.AMOUNT_OF_HEROS > 4.5 and scripts.constants.AMOUNT_OF_HEROS < 5.5:
                    if scripts.constants.DISPLAY_WIDTH//2-160 < self.pos[0]/scripts.constants.SCALE_WIDTH < scripts.constants.DISPLAY_WIDTH//2-96 and scripts.constants.DISPLAY_HEIGHT//2-32 < self.pos[1]/scripts.constants.SCALE_HEIGHT < scripts.constants.DISPLAY_HEIGHT//2-32+64:
                        scripts.constants.HERO = self.characters[0]
                        in_town = False
                        fight_button_pressed = True 
                        self.fight_button_pressed = False
                        self.draw_character_pick = False
                            
                    elif scripts.constants.DISPLAY_WIDTH//2-96 < self.pos[0]/scripts.constants.SCALE_WIDTH < scripts.constants.DISPLAY_WIDTH//2-32 and scripts.constants.DISPLAY_HEIGHT//2-32 < self.pos[1]/scripts.constants.SCALE_HEIGHT < scripts.constants.DISPLAY_HEIGHT//2-32+64:
                        scripts.constants.HERO = self.characters[1]
                        in_town = False
                        self.fight_button_pressed = False
                        self.draw_character_pick = False  
                        fight_button_pressed = True
                    
                    elif scripts.constants.DISPLAY_WIDTH//2-32 < self.pos[0]/scripts.constants.SCALE_WIDTH < scripts.constants.DISPLAY_WIDTH//2+32 and scripts.constants.DISPLAY_HEIGHT//2-32 < self.pos[1]/scripts.constants.SCALE_HEIGHT < scripts.constants.DISPLAY_HEIGHT//2-32+64:
                        scripts.constants.HERO = self.characters[2]
                        in_town = False
                        self.fight_button_pressed = False
                        self.draw_character_pick = False  
                        fight_button_pressed = True
                    
                    elif scripts.constants.DISPLAY_WIDTH//2 + 32 < self.pos[0]/scripts.constants.SCALE_WIDTH < scripts.constants.DISPLAY_WIDTH//2+ 96 and scripts.constants.DISPLAY_HEIGHT//2-32 < self.pos[1]/scripts.constants.SCALE_HEIGHT < scripts.constants.DISPLAY_HEIGHT//2-32+64:
                        scripts.constants.HERO = self.characters[3]
                        in_town = False
                        self.fight_button_pressed = False
                        self.draw_character_pick = False  
                        fight_button_pressed = True
                    
                    elif scripts.constants.DISPLAY_WIDTH//2 + 96 < self.pos[0]/scripts.constants.SCALE_WIDTH < scripts.constants.DISPLAY_WIDTH//2+ 160 and scripts.constants.DISPLAY_HEIGHT//2-32 < self.pos[1]/scripts.constants.SCALE_HEIGHT < scripts.constants.DISPLAY_HEIGHT//2-32+64:
                        scripts.constants.HERO = self.characters[4]
                        in_town = False
                        self.fight_button_pressed = False
                        self.draw_character_pick = False  
                        fight_button_pressed = True
                
                elif scripts.constants.AMOUNT_OF_HEROS > 5.5 and scripts.constants.AMOUNT_OF_HEROS < 6.5:
                    if scripts.constants.DISPLAY_WIDTH//2-192 < self.pos[0]/scripts.constants.SCALE_WIDTH < scripts.constants.DISPLAY_WIDTH//2-128 and scripts.constants.DISPLAY_HEIGHT//2-32 < self.pos[1]/scripts.constants.SCALE_HEIGHT < scripts.constants.DISPLAY_HEIGHT//2-32+64:
                        scripts.constants.HERO = self.characters[0]
                        in_town = False
                        fight_button_pressed = True 
                        self.fight_button_pressed = False
                        self.draw_character_pick = False
                            
                    elif scripts.constants.DISPLAY_WIDTH//2-128 < self.pos[0]/scripts.constants.SCALE_WIDTH < scripts.constants.DISPLAY_WIDTH//2-64 and scripts.constants.DISPLAY_HEIGHT//2-32 < self.pos[1]/scripts.constants.SCALE_HEIGHT < scripts.constants.DISPLAY_HEIGHT//2-32+64:
                        scripts.constants.HERO = self.characters[1]
                        in_town = False
                        self.fight_button_pressed = False
                        self.draw_character_pick = False  
                        fight_button_pressed = True
                    
                    elif scripts.constants.DISPLAY_WIDTH//2 - 64 < self.pos[0]/scripts.constants.SCALE_WIDTH < scripts.constants.DISPLAY_WIDTH//2 and scripts.constants.DISPLAY_HEIGHT//2-32 < self.pos[1]/scripts.constants.SCALE_HEIGHT < scripts.constants.DISPLAY_HEIGHT//2-32+64:
                        scripts.constants.HERO = self.characters[2]
                        in_town = False
                        self.fight_button_pressed = False
                        self.draw_character_pick = False  
                        fight_button_pressed = True
                    
                    elif scripts.constants.DISPLAY_WIDTH//2 < self.pos[0]/scripts.constants.SCALE_WIDTH < scripts.constants.DISPLAY_WIDTH//2+ 64 and scripts.constants.DISPLAY_HEIGHT//2-32 < self.pos[1]/scripts.constants.SCALE_HEIGHT < scripts.constants.DISPLAY_HEIGHT//2-32+64:
                        scripts.constants.HERO = self.characters[3]
                        in_town = False
                        self.fight_button_pressed = False
                        self.draw_character_pick = False  
                        fight_button_pressed = True
                    elif scripts.constants.DISPLAY_WIDTH//2 + 64 < self.pos[0]/scripts.constants.SCALE_WIDTH < scripts.constants.DISPLAY_WIDTH//2+ 128 and scripts.constants.DISPLAY_HEIGHT//2-32 < self.pos[1]/scripts.constants.SCALE_HEIGHT < scripts.constants.DISPLAY_HEIGHT//2-32+64:
                        scripts.constants.HERO = self.characters[4]
                        in_town = False
                        self.fight_button_pressed = False
                        self.draw_character_pick = False  
                        fight_button_pressed = True
                    elif scripts.constants.DISPLAY_WIDTH//2 + 128 < self.pos[0]/scripts.constants.SCALE_WIDTH < scripts.constants.DISPLAY_WIDTH//2+ 192 and scripts.constants.DISPLAY_HEIGHT//2-32 < self.pos[1]/scripts.constants.SCALE_HEIGHT < scripts.constants.DISPLAY_HEIGHT//2-32+64:
                        scripts.constants.HERO = self.characters[5]
                        in_town = False
                        self.fight_button_pressed = False
                        self.draw_character_pick = False  
                        fight_button_pressed = True
                
                elif scripts.constants.AMOUNT_OF_HEROS > 6.5 and scripts.constants.AMOUNT_OF_HEROS < 7.5:
                    if scripts.constants.DISPLAY_WIDTH//2-224 < self.pos[0]/scripts.constants.SCALE_WIDTH < scripts.constants.DISPLAY_WIDTH//2-160 and scripts.constants.DISPLAY_HEIGHT//2-32 < self.pos[1]/scripts.constants.SCALE_HEIGHT < scripts.constants.DISPLAY_HEIGHT//2-32+64:
                        scripts.constants.HERO = self.characters[0]
                        in_town = False
                        fight_button_pressed = True 
                        self.fight_button_pressed = False
                        self.draw_character_pick = False
                            
                    elif scripts.constants.DISPLAY_WIDTH//2-160 < self.pos[0]/scripts.constants.SCALE_WIDTH < scripts.constants.DISPLAY_WIDTH//2-96 and scripts.constants.DISPLAY_HEIGHT//2-32 < self.pos[1]/scripts.constants.SCALE_HEIGHT < scripts.constants.DISPLAY_HEIGHT//2-32+64:
                        scripts.constants.HERO = self.characters[1]
                        in_town = False
                        self.fight_button_pressed = False
                        self.draw_character_pick = False  
                        fight_button_pressed = True
                    
                    elif scripts.constants.DISPLAY_WIDTH//2 - 96 < self.pos[0]/scripts.constants.SCALE_WIDTH < scripts.constants.DISPLAY_WIDTH//2 - 32 and scripts.constants.DISPLAY_HEIGHT//2-32 < self.pos[1]/scripts.constants.SCALE_HEIGHT < scripts.constants.DISPLAY_HEIGHT//2-32+64:
                        scripts.constants.HERO = self.characters[2]
                        in_town = False
                        self.fight_button_pressed = False
                        self.draw_character_pick = False  
                        fight_button_pressed = True
                    
                    elif scripts.constants.DISPLAY_WIDTH//2 - 32 < self.pos[0]/scripts.constants.SCALE_WIDTH < scripts.constants.DISPLAY_WIDTH//2+ 32 and scripts.constants.DISPLAY_HEIGHT//2-32 < self.pos[1]/scripts.constants.SCALE_HEIGHT < scripts.constants.DISPLAY_HEIGHT//2-32+64:
                        scripts.constants.HERO = self.characters[3]
                        in_town = False
                        self.fight_button_pressed = False
                        self.draw_character_pick = False  
                        fight_button_pressed = True
                    elif scripts.constants.DISPLAY_WIDTH//2 + 32 < self.pos[0]/scripts.constants.SCALE_WIDTH < scripts.constants.DISPLAY_WIDTH//2+ 96 and scripts.constants.DISPLAY_HEIGHT//2-32 < self.pos[1]/scripts.constants.SCALE_HEIGHT < scripts.constants.DISPLAY_HEIGHT//2-32+64:
                        scripts.constants.HERO = self.characters[4]
                        in_town = False
                        self.fight_button_pressed = False
                        self.draw_character_pick = False  
                        fight_button_pressed = True
                    elif scripts.constants.DISPLAY_WIDTH//2 + 96 < self.pos[0]/scripts.constants.SCALE_WIDTH < scripts.constants.DISPLAY_WIDTH//2+ 160 and scripts.constants.DISPLAY_HEIGHT//2-32 < self.pos[1]/scripts.constants.SCALE_HEIGHT < scripts.constants.DISPLAY_HEIGHT//2-32+64:
                        scripts.constants.HERO = self.characters[5]
                        in_town = False
                        self.fight_button_pressed = False
                        self.draw_character_pick = False  
                        fight_button_pressed = True
                    elif scripts.constants.DISPLAY_WIDTH//2 + 160 < self.pos[0]/scripts.constants.SCALE_WIDTH < scripts.constants.DISPLAY_WIDTH//2+ 224 and scripts.constants.DISPLAY_HEIGHT//2-32 < self.pos[1]/scripts.constants.SCALE_HEIGHT < scripts.constants.DISPLAY_HEIGHT//2-32+64:
                        scripts.constants.HERO = self.characters[6]
                        in_town = False
                        self.fight_button_pressed = False
                        self.draw_character_pick = False  
                        fight_button_pressed = True   
                
                elif scripts.constants.AMOUNT_OF_HEROS > 7.5 and scripts.constants.AMOUNT_OF_HEROS < 8.5:
                    if scripts.constants.DISPLAY_WIDTH//2-128 < self.pos[0]/scripts.constants.SCALE_WIDTH < scripts.constants.DISPLAY_WIDTH//2-64 and scripts.constants.DISPLAY_HEIGHT//2-64 < self.pos[1]/scripts.constants.SCALE_HEIGHT < scripts.constants.DISPLAY_HEIGHT//2:
                        scripts.constants.HERO = self.characters[0]
                        in_town = False
                        fight_button_pressed = True 
                        self.fight_button_pressed = False
                        self.draw_character_pick = False
                            
                    elif scripts.constants.DISPLAY_WIDTH//2- 64 < self.pos[0]/scripts.constants.SCALE_WIDTH < scripts.constants.DISPLAY_WIDTH//2 and scripts.constants.DISPLAY_HEIGHT//2-64 < self.pos[1]/scripts.constants.SCALE_HEIGHT < scripts.constants.DISPLAY_HEIGHT//2:
                        scripts.constants.HERO = self.characters[1]
                        in_town = False
                        self.fight_button_pressed = False
                        self.draw_character_pick = False  
                        fight_button_pressed = True
                    
                    elif scripts.constants.DISPLAY_WIDTH//2 < self.pos[0]/scripts.constants.SCALE_WIDTH < scripts.constants.DISPLAY_WIDTH//2 + 64 and scripts.constants.DISPLAY_HEIGHT//2-64 < self.pos[1]/scripts.constants.SCALE_HEIGHT < scripts.constants.DISPLAY_HEIGHT//2:
                        scripts.constants.HERO = self.characters[2]
                        in_town = False
                        self.fight_button_pressed = False
                        self.draw_character_pick = False  
                        fight_button_pressed = True
                    
                    elif scripts.constants.DISPLAY_WIDTH//2 +64 < self.pos[0]/scripts.constants.SCALE_WIDTH < scripts.constants.DISPLAY_WIDTH//2+ 128 and scripts.constants.DISPLAY_HEIGHT//2-64 < self.pos[1]/scripts.constants.SCALE_HEIGHT < scripts.constants.DISPLAY_HEIGHT//2:
                        scripts.constants.HERO = self.characters[3]
                        in_town = False
                        self.fight_button_pressed = False
                        self.draw_character_pick = False  
                        fight_button_pressed = True
                    elif scripts.constants.DISPLAY_WIDTH//2 - 128 < self.pos[0]/scripts.constants.SCALE_WIDTH < scripts.constants.DISPLAY_WIDTH//2- 64 and scripts.constants.DISPLAY_HEIGHT//2+32 < self.pos[1]/scripts.constants.SCALE_HEIGHT < scripts.constants.DISPLAY_HEIGHT//2+96:
                        scripts.constants.HERO = self.characters[4]
                        in_town = False
                        self.fight_button_pressed = False
                        self.draw_character_pick = False  
                        fight_button_pressed = True
                    elif scripts.constants.DISPLAY_WIDTH//2 - 64 < self.pos[0]/scripts.constants.SCALE_WIDTH < scripts.constants.DISPLAY_WIDTH//2 and scripts.constants.DISPLAY_HEIGHT//2+32 < self.pos[1]/scripts.constants.SCALE_HEIGHT < scripts.constants.DISPLAY_HEIGHT//2+96:
                        scripts.constants.HERO = self.characters[5]
                        in_town = False
                        self.fight_button_pressed = False
                        self.draw_character_pick = False  
                        fight_button_pressed = True
                    elif scripts.constants.DISPLAY_WIDTH//2 < self.pos[0]/scripts.constants.SCALE_WIDTH < scripts.constants.DISPLAY_WIDTH//2+ 64 and scripts.constants.DISPLAY_HEIGHT//2+32 < self.pos[1]/scripts.constants.SCALE_HEIGHT < scripts.constants.DISPLAY_HEIGHT//2+96:
                        scripts.constants.HERO = self.characters[6]
                        in_town = False
                        self.fight_button_pressed = False
                        self.draw_character_pick = False  
                        fight_button_pressed = True   
                    elif scripts.constants.DISPLAY_WIDTH//2 + 64 < self.pos[0]/scripts.constants.SCALE_WIDTH < scripts.constants.DISPLAY_WIDTH//2+ 128 and scripts.constants.DISPLAY_HEIGHT//2+32 < self.pos[1]/scripts.constants.SCALE_HEIGHT < scripts.constants.DISPLAY_HEIGHT//2+96:
                        scripts.constants.HERO = self.characters[6]
                        in_town = False
                        self.fight_button_pressed = False
                        self.draw_character_pick = False  
                        fight_button_pressed = True   
                        
                
                        
                                         
            if self.back_button_pressed:
                if (pygame.time.get_ticks() - self.time) >= 100:
                    self.back_button_to_show = self.assets['buttons'][4]
                    self.draw_character_pick = False
                    self.fight_button_pressed = False
                    self.back_button_pressed = False
                
                    
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
        # upgrade town path building
        # tree
        if self.dwarfs_house_builded:
            display.blit(self.assets["town"][17],(0,0))
        if self.walls_builded:
            display.blit(self.assets["town"][19],(0,0))
        display.blit(self.assets["town"][7],(0,0))
        if self.upgrade_town_builded:
            display.blit(self.assets["town"][18],(0,0))
        display.blit(self.assets["town"][8],(0,0))
        # buildings
        display.blit(self.assets["town"][9],(0,0))
        if self.hut_builded:
            display.blit(self.assets["town"][10],(0,0))
        if self.smith_builded:
            display.blit(self.assets["town"][11],(0,0))
        if self.wizard_tower_builded:
            display.blit(self.assets["town"][16],(0,0))
        if self.knight_castle_builded:
            display.blit(self.assets["town"][23],(0,0))
        if self.pikemen_tower_builded:
            display.blit(self.assets["town"][20],(0,0))
        if self.canals_builded:
            display.blit(self.assets["town"][24],(0,0))
        if self.statue_builded:
            display.blit(self.assets["town"][25],(0,0))
        if scripts.constants.DRUID_DEFEAT:
            display.blit(self.assets["town"][21],(0,0))   
        if self.crow_builded:
            display.blit(self.assets["town"][22],(0,0))
        # HUD
        display.blit(self.assets["town"][12],(0,0))
            # buttons
        display.blit(self.assets["town"][13],(0,0))
        #display.blit(self.assets["town"][14],(0,0))
        display.blit(self.assets["town"][15],(0,0))
            # resources
        display.blit(self.assets["gold"],(scripts.constants.DISPLAY_WIDTH//3-8, scripts.constants.DISPLAY_HEIGHT-23-7))
        display.blit(self.gold_text,(scripts.constants.DISPLAY_WIDTH//3+18, scripts.constants.DISPLAY_HEIGHT-18))
        # hero menu picker
        if self.draw_character_pick:
            display.blit(self.assets["fight_button_menu"],(0,0))
            display.blit(self.character_pick_text_to_show, (scripts.constants.DISPLAY_WIDTH//4-10,5))
            display.blit(self.back_button_to_show, (5,scripts.constants.DISPLAY_HEIGHT-32))
            if scripts.constants.AMOUNT_OF_HEROS < 0.5:                                     
                display.blit(self.no_hero_text_1_to_show, (scripts.constants.DISPLAY_WIDTH//4+10,scripts.constants.DISPLAY_HEIGHT//2))
                display.blit(self.no_hero_text_2_to_show, (scripts.constants.DISPLAY_WIDTH//4-55,scripts.constants.DISPLAY_HEIGHT//2+16))
            elif scripts.constants.AMOUNT_OF_HEROS > 0.5 and scripts.constants.AMOUNT_OF_HEROS < 1.5:
                display.blit(self.assets[self.characters[0]],(scripts.constants.DISPLAY_WIDTH//2-32,scripts.constants.DISPLAY_HEIGHT//2-32))
            elif scripts.constants.AMOUNT_OF_HEROS > 1.5 and scripts.constants.AMOUNT_OF_HEROS < 2.5:
                display.blit(self.assets[self.characters[0]],(scripts.constants.DISPLAY_WIDTH//2-32-32,scripts.constants.DISPLAY_HEIGHT//2-32))
                display.blit(self.assets[self.characters[1]],(scripts.constants.DISPLAY_WIDTH//2-32+32,scripts.constants.DISPLAY_HEIGHT//2-32))
            elif scripts.constants.AMOUNT_OF_HEROS > 2.5 and scripts.constants.AMOUNT_OF_HEROS < 3.5:
                display.blit(self.assets[self.characters[0]],(scripts.constants.DISPLAY_WIDTH//2- 80,scripts.constants.DISPLAY_HEIGHT//2-32))
                display.blit(self.assets[self.characters[1]],(scripts.constants.DISPLAY_WIDTH//2- 32,scripts.constants.DISPLAY_HEIGHT//2-32))
                display.blit(self.assets[self.characters[2]],(scripts.constants.DISPLAY_WIDTH//2+ 16,scripts.constants.DISPLAY_HEIGHT//2-32))
            elif scripts.constants.AMOUNT_OF_HEROS > 3.5 and scripts.constants.AMOUNT_OF_HEROS < 4.5:
                display.blit(self.assets[self.characters[0]],(scripts.constants.DISPLAY_WIDTH//2- 128,scripts.constants.DISPLAY_HEIGHT//2-32))
                display.blit(self.assets[self.characters[1]],(scripts.constants.DISPLAY_WIDTH//2- 64,scripts.constants.DISPLAY_HEIGHT//2-32))
                display.blit(self.assets[self.characters[2]],(scripts.constants.DISPLAY_WIDTH//2,scripts.constants.DISPLAY_HEIGHT//2-32))
                display.blit(self.assets[self.characters[3]],(scripts.constants.DISPLAY_WIDTH//2+ 64,scripts.constants.DISPLAY_HEIGHT//2-32))
            elif scripts.constants.AMOUNT_OF_HEROS > 4.5 and scripts.constants.AMOUNT_OF_HEROS < 5.5:
                display.blit(self.assets[self.characters[0]],(scripts.constants.DISPLAY_WIDTH//2- 160,scripts.constants.DISPLAY_HEIGHT//2-32))
                display.blit(self.assets[self.characters[1]],(scripts.constants.DISPLAY_WIDTH//2- 96,scripts.constants.DISPLAY_HEIGHT//2-32))
                display.blit(self.assets[self.characters[2]],(scripts.constants.DISPLAY_WIDTH//2 - 32,scripts.constants.DISPLAY_HEIGHT//2-32))
                display.blit(self.assets[self.characters[3]],(scripts.constants.DISPLAY_WIDTH//2 + 32,scripts.constants.DISPLAY_HEIGHT//2-32))
                display.blit(self.assets[self.characters[4]],(scripts.constants.DISPLAY_WIDTH//2+ 96,scripts.constants.DISPLAY_HEIGHT//2-32))
            elif scripts.constants.AMOUNT_OF_HEROS > 5.5 and scripts.constants.AMOUNT_OF_HEROS < 6.5:
                display.blit(self.assets[self.characters[0]],(scripts.constants.DISPLAY_WIDTH//2- 192,scripts.constants.DISPLAY_HEIGHT//2-32))
                display.blit(self.assets[self.characters[1]],(scripts.constants.DISPLAY_WIDTH//2- 128,scripts.constants.DISPLAY_HEIGHT//2-32))
                display.blit(self.assets[self.characters[2]],(scripts.constants.DISPLAY_WIDTH//2 - 64,scripts.constants.DISPLAY_HEIGHT//2-32))
                display.blit(self.assets[self.characters[3]],(scripts.constants.DISPLAY_WIDTH//2 ,scripts.constants.DISPLAY_HEIGHT//2-32))
                display.blit(self.assets[self.characters[4]],(scripts.constants.DISPLAY_WIDTH//2+ 64,scripts.constants.DISPLAY_HEIGHT//2-32))
                display.blit(self.assets[self.characters[5]],(scripts.constants.DISPLAY_WIDTH//2+ 128,scripts.constants.DISPLAY_HEIGHT//2-32))
            elif scripts.constants.AMOUNT_OF_HEROS > 6.5 and scripts.constants.AMOUNT_OF_HEROS < 7.5:
                display.blit(self.assets[self.characters[0]],(scripts.constants.DISPLAY_WIDTH//2- 224,scripts.constants.DISPLAY_HEIGHT//2-32))
                display.blit(self.assets[self.characters[1]],(scripts.constants.DISPLAY_WIDTH//2- 160,scripts.constants.DISPLAY_HEIGHT//2-32))
                display.blit(self.assets[self.characters[2]],(scripts.constants.DISPLAY_WIDTH//2 - 96,scripts.constants.DISPLAY_HEIGHT//2-32))
                display.blit(self.assets[self.characters[3]],(scripts.constants.DISPLAY_WIDTH//2 -32,scripts.constants.DISPLAY_HEIGHT//2-32))
                display.blit(self.assets[self.characters[4]],(scripts.constants.DISPLAY_WIDTH//2+ 32,scripts.constants.DISPLAY_HEIGHT//2-32))
                display.blit(self.assets[self.characters[5]],(scripts.constants.DISPLAY_WIDTH//2+ 96,scripts.constants.DISPLAY_HEIGHT//2-32))
                display.blit(self.assets[self.characters[6]],(scripts.constants.DISPLAY_WIDTH//2+ 160,scripts.constants.DISPLAY_HEIGHT//2-32))
            elif scripts.constants.AMOUNT_OF_HEROS > 7.5 and scripts.constants.AMOUNT_OF_HEROS < 8.5:
                display.blit(self.assets[self.characters[0]],(scripts.constants.DISPLAY_WIDTH//2- 128,scripts.constants.DISPLAY_HEIGHT//2-64))
                display.blit(self.assets[self.characters[1]],(scripts.constants.DISPLAY_WIDTH//2- 64,scripts.constants.DISPLAY_HEIGHT//2-64))
                display.blit(self.assets[self.characters[2]],(scripts.constants.DISPLAY_WIDTH//2,scripts.constants.DISPLAY_HEIGHT//2-64))
                display.blit(self.assets[self.characters[3]],(scripts.constants.DISPLAY_WIDTH//2+ 64,scripts.constants.DISPLAY_HEIGHT//2-64))
                display.blit(self.assets[self.characters[4]],(scripts.constants.DISPLAY_WIDTH//2- 128,scripts.constants.DISPLAY_HEIGHT//2+ 32))
                display.blit(self.assets[self.characters[5]],(scripts.constants.DISPLAY_WIDTH//2- 64,scripts.constants.DISPLAY_HEIGHT//2+32))
                display.blit(self.assets[self.characters[6]],(scripts.constants.DISPLAY_WIDTH//2,scripts.constants.DISPLAY_HEIGHT//2+32))
                display.blit(self.assets[self.characters[7]],(scripts.constants.DISPLAY_WIDTH//2+ 64,scripts.constants.DISPLAY_HEIGHT//2+32))
            
            
        
        # bulding menu
        if self.build_menu:
            # frame
            display.blit(self.assets["build_menu_frame"],(scripts.constants.DISPLAY_WIDTH//8-4,scripts.constants.DISPLAY_HEIGHT//8-4))
            # buildings
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
                
            if self.hut_builded:
                pygame.draw.rect(display,scripts.constants.GREY,(scripts.constants.DISPLAY_WIDTH/8+4+8,scripts.constants.DISPLAY_HEIGHT/8+4,32,32))
                display.blit(self.assets["hut"][0],(scripts.constants.DISPLAY_WIDTH/8+4+8,scripts.constants.DISPLAY_HEIGHT/8+4))
            else:
                if self.gold >= self.hut_cost:
                    pygame.draw.rect(display,scripts.constants.GREEN,(scripts.constants.DISPLAY_WIDTH/8+4+8,scripts.constants.DISPLAY_HEIGHT/8+4,32,32))
                else:
                    pygame.draw.rect(display,scripts.constants.RED,(scripts.constants.DISPLAY_WIDTH/8+4+8,scripts.constants.DISPLAY_HEIGHT/8+4,32,32))
                display.blit(self.assets["hut"][0],(scripts.constants.DISPLAY_WIDTH/8+4+8,scripts.constants.DISPLAY_HEIGHT/8+4))
                display.blit(self.hut_cost_text, (scripts.constants.DISPLAY_WIDTH/8+4+8,scripts.constants.DISPLAY_HEIGHT/8+4))
                
            if self.smith_builded:
                pygame.draw.rect(display,scripts.constants.GREY,(scripts.constants.DISPLAY_WIDTH/8+40+8,scripts.constants.DISPLAY_HEIGHT/8+4,32,32))
                display.blit(self.assets["smith"][0],(scripts.constants.DISPLAY_WIDTH/8+40+8,scripts.constants.DISPLAY_HEIGHT/8+4))
            else:
                if self.gold >= self.smith_cost and self.hut_builded:
                    pygame.draw.rect(display,scripts.constants.GREEN,(scripts.constants.DISPLAY_WIDTH/8+40+8,scripts.constants.DISPLAY_HEIGHT/8+4,32,32))
                else:
                    pygame.draw.rect(display,scripts.constants.RED,(scripts.constants.DISPLAY_WIDTH/8+40+8,scripts.constants.DISPLAY_HEIGHT/8+4,32,32))
                display.blit(self.assets["smith"][0],(scripts.constants.DISPLAY_WIDTH/8+40+8,scripts.constants.DISPLAY_HEIGHT/8+4))
                display.blit(self.smith_cost_text, (scripts.constants.DISPLAY_WIDTH/8+40+8,scripts.constants.DISPLAY_HEIGHT/8+4))
            
            if self.wizard_tower_builded:
                pygame.draw.rect(display,scripts.constants.GREY,(scripts.constants.DISPLAY_WIDTH/8+40+36+8,scripts.constants.DISPLAY_HEIGHT/8+4,32,32))
                display.blit(self.assets["wizard_tower"][0],(scripts.constants.DISPLAY_WIDTH/8+40+36+8,scripts.constants.DISPLAY_HEIGHT/8+4))
            else:
                if self.gold >= self.wizard_tower_cost:
                    pygame.draw.rect(display,scripts.constants.GREEN,(scripts.constants.DISPLAY_WIDTH/8+40+36+8,scripts.constants.DISPLAY_HEIGHT/8+4,32,32))
                else:
                    pygame.draw.rect(display,scripts.constants.RED,(scripts.constants.DISPLAY_WIDTH/8+40+36+8,scripts.constants.DISPLAY_HEIGHT/8+4,32,32))
                display.blit(self.assets["wizard_tower"][0],(scripts.constants.DISPLAY_WIDTH/8+40+36+8,scripts.constants.DISPLAY_HEIGHT/8+4))
                display.blit(self.wizard_tower_cost_text, (scripts.constants.DISPLAY_WIDTH/8+40+36+8,scripts.constants.DISPLAY_HEIGHT/8+4))
            
            if self.dwarfs_house_builded:
                pygame.draw.rect(display,scripts.constants.GREY,(scripts.constants.DISPLAY_WIDTH/8+112+8,scripts.constants.DISPLAY_HEIGHT/8+4,32,32))
                display.blit(self.assets["dwarfs_house"][0],(scripts.constants.DISPLAY_WIDTH/8+112+8,scripts.constants.DISPLAY_HEIGHT/8+4))
            else:
                if self.gold >= self.dwarfs_house_cost:
                    pygame.draw.rect(display,scripts.constants.GREEN,(scripts.constants.DISPLAY_WIDTH/8+112+8,scripts.constants.DISPLAY_HEIGHT/8+4,32,32))
                else:
                    pygame.draw.rect(display,scripts.constants.RED,(scripts.constants.DISPLAY_WIDTH/8+112+8,scripts.constants.DISPLAY_HEIGHT/8+4,32,32))
                display.blit(self.assets["dwarfs_house"][0],(scripts.constants.DISPLAY_WIDTH/8+112+8,scripts.constants.DISPLAY_HEIGHT/8+4))
                display.blit(self.dwarfs_house_cost_text, (scripts.constants.DISPLAY_WIDTH/8+112+8,scripts.constants.DISPLAY_HEIGHT/8+4))
            
            if self.knight_castle_builded:
                pygame.draw.rect(display,scripts.constants.GREY,(scripts.constants.DISPLAY_WIDTH/8+148+8,scripts.constants.DISPLAY_HEIGHT/8+4,32,32))
                display.blit(self.assets["knight_castle"][0],(scripts.constants.DISPLAY_WIDTH/8+148+8,scripts.constants.DISPLAY_HEIGHT/8+4))
            else:
                if self.gold >= self.knight_castle_cost:
                    pygame.draw.rect(display,scripts.constants.GREEN,(scripts.constants.DISPLAY_WIDTH/8+148+8,scripts.constants.DISPLAY_HEIGHT/8+4,32,32))
                else:
                    pygame.draw.rect(display,scripts.constants.RED,(scripts.constants.DISPLAY_WIDTH/8+148+8,scripts.constants.DISPLAY_HEIGHT/8+4,32,32))
                display.blit(self.assets["knight_castle"][0],(scripts.constants.DISPLAY_WIDTH/8+148+8,scripts.constants.DISPLAY_HEIGHT/8+4))
                display.blit(self.knight_castle_cost_text, (scripts.constants.DISPLAY_WIDTH/8+148+8,scripts.constants.DISPLAY_HEIGHT/8+4))
                
            if self.pikemen_tower_builded:
                pygame.draw.rect(display,scripts.constants.GREY,(scripts.constants.DISPLAY_WIDTH/8+184+8,scripts.constants.DISPLAY_HEIGHT/8+4,32,32))
                display.blit(self.assets["pikemen_tower"][0],(scripts.constants.DISPLAY_WIDTH/8+184+8,scripts.constants.DISPLAY_HEIGHT/8+4))
            else:
                if self.gold >= self.pikemen_tower_cost:
                    pygame.draw.rect(display,scripts.constants.GREEN,(scripts.constants.DISPLAY_WIDTH/8+184+8,scripts.constants.DISPLAY_HEIGHT/8+4,32,32))
                else:
                    pygame.draw.rect(display,scripts.constants.RED,(scripts.constants.DISPLAY_WIDTH/8+184+8,scripts.constants.DISPLAY_HEIGHT/8+4,32,32))
                display.blit(self.assets["pikemen_tower"][0],(scripts.constants.DISPLAY_WIDTH/8+184+8,scripts.constants.DISPLAY_HEIGHT/8+4))
                display.blit(self.pikemen_tower_cost_text, (scripts.constants.DISPLAY_WIDTH/8+184+8,scripts.constants.DISPLAY_HEIGHT/8+4))
            
            if self.canals_builded:
                pygame.draw.rect(display,scripts.constants.GREY,(scripts.constants.DISPLAY_WIDTH/8+220+8,scripts.constants.DISPLAY_HEIGHT/8+4,32,32))
                display.blit(self.assets["canals"][0],(scripts.constants.DISPLAY_WIDTH/8+220+8,scripts.constants.DISPLAY_HEIGHT/8+4))
            else:
                if self.gold >= self.canals_cost:
                    pygame.draw.rect(display,scripts.constants.GREEN,(scripts.constants.DISPLAY_WIDTH/8+220+8,scripts.constants.DISPLAY_HEIGHT/8+4,32,32))
                else:
                    pygame.draw.rect(display,scripts.constants.RED,(scripts.constants.DISPLAY_WIDTH/8+220+8,scripts.constants.DISPLAY_HEIGHT/8+4,32,32))
                display.blit(self.assets["canals"][0],(scripts.constants.DISPLAY_WIDTH/8+220+8,scripts.constants.DISPLAY_HEIGHT/8+4))
                display.blit(self.canals_cost_text, (scripts.constants.DISPLAY_WIDTH/8+220+8,scripts.constants.DISPLAY_HEIGHT/8+4))
            
            if self.statue_builded:
                pygame.draw.rect(display,scripts.constants.GREY,(scripts.constants.DISPLAY_WIDTH/8+256+8,scripts.constants.DISPLAY_HEIGHT/8+4,32,32))
                display.blit(self.assets["statue"][0],(scripts.constants.DISPLAY_WIDTH/8+256+8,scripts.constants.DISPLAY_HEIGHT/8+4))
            else:
                if self.gold >= self.statue_cost:
                    pygame.draw.rect(display,scripts.constants.GREEN,(scripts.constants.DISPLAY_WIDTH/8+256+8,scripts.constants.DISPLAY_HEIGHT/8+4,32,32))
                else:
                    pygame.draw.rect(display,scripts.constants.RED,(scripts.constants.DISPLAY_WIDTH/8+256+8,scripts.constants.DISPLAY_HEIGHT/8+4,32,32))
                display.blit(self.assets["statue"][0],(scripts.constants.DISPLAY_WIDTH/8+256+8,scripts.constants.DISPLAY_HEIGHT/8+4))
                display.blit(self.statue_cost_text, (scripts.constants.DISPLAY_WIDTH/8+256+8,scripts.constants.DISPLAY_HEIGHT/8+4))
            
            if self.crow_builded:
                pygame.draw.rect(display,scripts.constants.GREY,(scripts.constants.DISPLAY_WIDTH/8+292+8,scripts.constants.DISPLAY_HEIGHT/8+4,32,32))
                display.blit(self.assets["crow"][0],(scripts.constants.DISPLAY_WIDTH/8+292+8,scripts.constants.DISPLAY_HEIGHT/8+4))
            else:
                if scripts.constants.DRUID_DEFEAT:
                    if self.gold >= self.crow_cost:
                        pygame.draw.rect(display,scripts.constants.GREEN,(scripts.constants.DISPLAY_WIDTH/8+292+8,scripts.constants.DISPLAY_HEIGHT/8+4,32,32))
                else:
                    pygame.draw.rect(display,scripts.constants.RED,(scripts.constants.DISPLAY_WIDTH/8+292+8,scripts.constants.DISPLAY_HEIGHT/8+4,32,32))
                display.blit(self.assets["crow"][0],(scripts.constants.DISPLAY_WIDTH/8+292+8,scripts.constants.DISPLAY_HEIGHT/8+4))
                display.blit(self.crow_cost_text, (scripts.constants.DISPLAY_WIDTH/8+292+8,scripts.constants.DISPLAY_HEIGHT/8+4))
                
            if self.upgrade_town_builded:
                pygame.draw.rect(display,scripts.constants.GREY,(scripts.constants.DISPLAY_WIDTH/8+4+8,scripts.constants.DISPLAY_HEIGHT/8+4+32+4,32,32))
                display.blit(self.assets["upgrade_town"][0],(scripts.constants.DISPLAY_WIDTH/8+4+8,scripts.constants.DISPLAY_HEIGHT/8+4+32+4))
            else:
                if self.town_level >= 5 and self.gold >= self.upgrade_town_cost:
                    pygame.draw.rect(display,scripts.constants.GREEN,(scripts.constants.DISPLAY_WIDTH/8+4+8,scripts.constants.DISPLAY_HEIGHT/8+4+32+4,32,32))
                else:
                    pygame.draw.rect(display,scripts.constants.RED,(scripts.constants.DISPLAY_WIDTH/8+4+8,scripts.constants.DISPLAY_HEIGHT/8+4+32+4,32,32))
                display.blit(self.assets["upgrade_town"][0],(scripts.constants.DISPLAY_WIDTH/8+4+8,scripts.constants.DISPLAY_HEIGHT/8+4+32+4))
                display.blit(self.upgrade_town_cost_text, (scripts.constants.DISPLAY_WIDTH/8+4+8,scripts.constants.DISPLAY_HEIGHT/8+4+32+4))
            
            if self.walls_builded:
                pygame.draw.rect(display,scripts.constants.GREY,(scripts.constants.DISPLAY_WIDTH/8+40+8,scripts.constants.DISPLAY_HEIGHT/8+4+32+4,32,32))
                display.blit(self.assets["walls"][0],(scripts.constants.DISPLAY_WIDTH/8+40+8,scripts.constants.DISPLAY_HEIGHT/8+4+32+4))
            else:
                if self.wizard_tower_builded and self.knight_castle_builded and self.pikemen_tower_builded:
                    if self.gold >= self.walls_cost:
                        pygame.draw.rect(display,scripts.constants.GREEN,(scripts.constants.DISPLAY_WIDTH/8+40+8,scripts.constants.DISPLAY_HEIGHT/8+4+32+4,32,32))
                else:
                    pygame.draw.rect(display,scripts.constants.RED,(scripts.constants.DISPLAY_WIDTH/8+40+8,scripts.constants.DISPLAY_HEIGHT/8+4+32+4,32,32))
                display.blit(self.assets["walls"][0],(scripts.constants.DISPLAY_WIDTH/8+40+8,scripts.constants.DISPLAY_HEIGHT/8+4+32+4))
                display.blit(self.walls_cost_text, (scripts.constants.DISPLAY_WIDTH/8+40+8,scripts.constants.DISPLAY_HEIGHT/8+4+32+4))
            
            if self.draw_hut_info:
                pygame.draw.rect(display,scripts.constants.WHITE,(self.pos[0]/scripts.constants.SCALE_WIDTH+16,self.pos[1]/scripts.constants.SCALE_HEIGHT+16,150,100))
                pygame.draw.rect(display,scripts.constants.MAINMENU_COLOR_DARKER,(self.pos[0]/scripts.constants.SCALE_WIDTH+16+2,self.pos[1]/scripts.constants.SCALE_HEIGHT+2+16,146,96))
                display.blit(self.hut_description_text_1,(self.pos[0]/scripts.constants.SCALE_WIDTH+4+16,self.pos[1]/scripts.constants.SCALE_HEIGHT+4+16))
                display.blit(self.hut_description_text_2,(self.pos[0]/scripts.constants.SCALE_WIDTH+4+16,self.pos[1]/scripts.constants.SCALE_HEIGHT+14+16))
                display.blit(self.hut_description_text_3,(self.pos[0]/scripts.constants.SCALE_WIDTH+4+16,self.pos[1]/scripts.constants.SCALE_HEIGHT+24+16))
                display.blit(self.hut_description_text_4,(self.pos[0]/scripts.constants.SCALE_WIDTH+4+16,self.pos[1]/scripts.constants.SCALE_HEIGHT+34+16))
                display.blit(self.hut_description_text_5,(self.pos[0]/scripts.constants.SCALE_WIDTH+4+16,self.pos[1]/scripts.constants.SCALE_HEIGHT+44+16))
            
            if self.draw_smith_info:
                pygame.draw.rect(display,scripts.constants.WHITE,(self.pos[0]/scripts.constants.SCALE_WIDTH+16,self.pos[1]/scripts.constants.SCALE_HEIGHT+16,150,100))
                pygame.draw.rect(display,scripts.constants.MAINMENU_COLOR_DARKER,(self.pos[0]/scripts.constants.SCALE_WIDTH+2+16,self.pos[1]/scripts.constants.SCALE_HEIGHT+2+16,146,96))
                display.blit(self.smith_description_text_1,(self.pos[0]/scripts.constants.SCALE_WIDTH+4+16,self.pos[1]/scripts.constants.SCALE_HEIGHT+4+16))
                display.blit(self.smith_description_text_2,(self.pos[0]/scripts.constants.SCALE_WIDTH+4+16,self.pos[1]/scripts.constants.SCALE_HEIGHT+14+16))
                display.blit(self.smith_description_text_3,(self.pos[0]/scripts.constants.SCALE_WIDTH+4+16,self.pos[1]/scripts.constants.SCALE_HEIGHT+24+16))
                if not self.hut_builded:
                    display.blit(self.smith_description_text_3,(self.pos[0]/scripts.constants.SCALE_WIDTH+4+16,self.pos[1]/scripts.constants.SCALE_HEIGHT+24+16))
            
            if self.draw_wizard_tower_info:
                pygame.draw.rect(display,scripts.constants.WHITE,(self.pos[0]/scripts.constants.SCALE_WIDTH+16,self.pos[1]/scripts.constants.SCALE_HEIGHT+16,150,100))
                pygame.draw.rect(display,scripts.constants.MAINMENU_COLOR_DARKER,(self.pos[0]/scripts.constants.SCALE_WIDTH+2+16,self.pos[1]/scripts.constants.SCALE_HEIGHT+2+16,146,96))
                display.blit(self.wizard_tower_description_text_1,(self.pos[0]/scripts.constants.SCALE_WIDTH+4+16,self.pos[1]/scripts.constants.SCALE_HEIGHT+4+16))
                display.blit(self.wizard_tower_description_text_2,(self.pos[0]/scripts.constants.SCALE_WIDTH+4+16,self.pos[1]/scripts.constants.SCALE_HEIGHT+14+16))
                display.blit(self.wizard_tower_description_text_3,(self.pos[0]/scripts.constants.SCALE_WIDTH+4+16,self.pos[1]/scripts.constants.SCALE_HEIGHT+24+16))
                display.blit(self.wizard_tower_description_text_4,(self.pos[0]/scripts.constants.SCALE_WIDTH+4+16,self.pos[1]/scripts.constants.SCALE_HEIGHT+34+16))
                display.blit(self.wizard_tower_description_text_5,(self.pos[0]/scripts.constants.SCALE_WIDTH+4+16,self.pos[1]/scripts.constants.SCALE_HEIGHT+44+16))
                if not self.hut_builded:
                    display.blit(self.wizard_tower_description_text_3,(self.pos[0]/scripts.constants.SCALE_WIDTH+4+16,self.pos[1]/scripts.constants.SCALE_HEIGHT+24+16))
            
            if self.draw_dwarfs_house_info:
                pygame.draw.rect(display,scripts.constants.WHITE,(self.pos[0]/scripts.constants.SCALE_WIDTH+16,self.pos[1]/scripts.constants.SCALE_HEIGHT+16,150,100))
                pygame.draw.rect(display,scripts.constants.MAINMENU_COLOR_DARKER,(self.pos[0]/scripts.constants.SCALE_WIDTH+2+16,self.pos[1]/scripts.constants.SCALE_HEIGHT+2+16,146,96))
                display.blit(self.dwarfs_house_description_text_1,(self.pos[0]/scripts.constants.SCALE_WIDTH+4+16,self.pos[1]/scripts.constants.SCALE_HEIGHT+4+16))
                display.blit(self.dwarfs_house_description_text_2,(self.pos[0]/scripts.constants.SCALE_WIDTH+4+16,self.pos[1]/scripts.constants.SCALE_HEIGHT+14+16))
                display.blit(self.dwarfs_house_description_text_3,(self.pos[0]/scripts.constants.SCALE_WIDTH+4+16,self.pos[1]/scripts.constants.SCALE_HEIGHT+24+16))
                display.blit(self.dwarfs_house_description_text_4,(self.pos[0]/scripts.constants.SCALE_WIDTH+4+16,self.pos[1]/scripts.constants.SCALE_HEIGHT+34+16))
                display.blit(self.dwarfs_house_description_text_5,(self.pos[0]/scripts.constants.SCALE_WIDTH+4+16,self.pos[1]/scripts.constants.SCALE_HEIGHT+44+16))
                if not self.hut_builded:
                    display.blit(self.dwarfs_house_description_text_3,(self.pos[0]/scripts.constants.SCALE_WIDTH+4+16,self.pos[1]/scripts.constants.SCALE_HEIGHT+24+16))
            
            if self.draw_knight_castle_info:
                pygame.draw.rect(display,scripts.constants.WHITE,(self.pos[0]/scripts.constants.SCALE_WIDTH+16,self.pos[1]/scripts.constants.SCALE_HEIGHT+16,150,100))
                pygame.draw.rect(display,scripts.constants.MAINMENU_COLOR_DARKER,(self.pos[0]/scripts.constants.SCALE_WIDTH+2+16,self.pos[1]/scripts.constants.SCALE_HEIGHT+2+16,146,96))
                display.blit(self.knight_castle_description_text_1,(self.pos[0]/scripts.constants.SCALE_WIDTH+4+16,self.pos[1]/scripts.constants.SCALE_HEIGHT+4+16))
                display.blit(self.knight_castle_description_text_2,(self.pos[0]/scripts.constants.SCALE_WIDTH+4+16,self.pos[1]/scripts.constants.SCALE_HEIGHT+14+16))
                display.blit(self.knight_castle_description_text_3,(self.pos[0]/scripts.constants.SCALE_WIDTH+4+16,self.pos[1]/scripts.constants.SCALE_HEIGHT+24+16))
                display.blit(self.knight_castle_description_text_4,(self.pos[0]/scripts.constants.SCALE_WIDTH+4+16,self.pos[1]/scripts.constants.SCALE_HEIGHT+34+16))
                display.blit(self.knight_castle_description_text_5,(self.pos[0]/scripts.constants.SCALE_WIDTH+4+16,self.pos[1]/scripts.constants.SCALE_HEIGHT+44+16))
                if not self.hut_builded:
                    display.blit(self.knight_castle_description_text_3,(self.pos[0]/scripts.constants.SCALE_WIDTH+4+16,self.pos[1]/scripts.constants.SCALE_HEIGHT+24+16))
                
            if self.draw_pikemen_tower_info:
                pygame.draw.rect(display,scripts.constants.WHITE,(self.pos[0]/scripts.constants.SCALE_WIDTH+16,self.pos[1]/scripts.constants.SCALE_HEIGHT+16,150,100))
                pygame.draw.rect(display,scripts.constants.MAINMENU_COLOR_DARKER,(self.pos[0]/scripts.constants.SCALE_WIDTH+2+16,self.pos[1]/scripts.constants.SCALE_HEIGHT+2+16,146,96))
                display.blit(self.pikemen_tower_description_text_1,(self.pos[0]/scripts.constants.SCALE_WIDTH+4+16,self.pos[1]/scripts.constants.SCALE_HEIGHT+4+16))
                display.blit(self.pikemen_tower_description_text_2,(self.pos[0]/scripts.constants.SCALE_WIDTH+4+16,self.pos[1]/scripts.constants.SCALE_HEIGHT+14+16))
                display.blit(self.pikemen_tower_description_text_3,(self.pos[0]/scripts.constants.SCALE_WIDTH+4+16,self.pos[1]/scripts.constants.SCALE_HEIGHT+24+16))
                display.blit(self.pikemen_tower_description_text_4,(self.pos[0]/scripts.constants.SCALE_WIDTH+4+16,self.pos[1]/scripts.constants.SCALE_HEIGHT+34+16))
                display.blit(self.pikemen_tower_description_text_5,(self.pos[0]/scripts.constants.SCALE_WIDTH+4+16,self.pos[1]/scripts.constants.SCALE_HEIGHT+44+16))
                if not self.hut_builded:
                    display.blit(self.pikemen_tower_description_text_3,(self.pos[0]/scripts.constants.SCALE_WIDTH+4+16,self.pos[1]/scripts.constants.SCALE_HEIGHT+24+16))
            
            if self.draw_canals_info:
                pygame.draw.rect(display,scripts.constants.WHITE,(self.pos[0]/scripts.constants.SCALE_WIDTH+16,self.pos[1]/scripts.constants.SCALE_HEIGHT+16,150,100))
                pygame.draw.rect(display,scripts.constants.MAINMENU_COLOR_DARKER,(self.pos[0]/scripts.constants.SCALE_WIDTH+2+16,self.pos[1]/scripts.constants.SCALE_HEIGHT+2+16,146,96))
                display.blit(self.canals_description_text_1,(self.pos[0]/scripts.constants.SCALE_WIDTH+4+16,self.pos[1]/scripts.constants.SCALE_HEIGHT+4+16))
                display.blit(self.canals_description_text_2,(self.pos[0]/scripts.constants.SCALE_WIDTH+4+16,self.pos[1]/scripts.constants.SCALE_HEIGHT+14+16))
                display.blit(self.canals_description_text_3,(self.pos[0]/scripts.constants.SCALE_WIDTH+4+16,self.pos[1]/scripts.constants.SCALE_HEIGHT+24+16))
                display.blit(self.canals_description_text_4,(self.pos[0]/scripts.constants.SCALE_WIDTH+4+16,self.pos[1]/scripts.constants.SCALE_HEIGHT+34+16))
                display.blit(self.canals_description_text_5,(self.pos[0]/scripts.constants.SCALE_WIDTH+4+16,self.pos[1]/scripts.constants.SCALE_HEIGHT+44+16))
                if not self.hut_builded:
                    display.blit(self.canals_description_text_3,(self.pos[0]/scripts.constants.SCALE_WIDTH+4+16,self.pos[1]/scripts.constants.SCALE_HEIGHT+24+16))
            
            if self.draw_statue_info:
                pygame.draw.rect(display,scripts.constants.WHITE,(self.pos[0]/scripts.constants.SCALE_WIDTH+16 - 150,self.pos[1]/scripts.constants.SCALE_HEIGHT+16,150,100))
                pygame.draw.rect(display,scripts.constants.MAINMENU_COLOR_DARKER,(self.pos[0]/scripts.constants.SCALE_WIDTH+2+16 - 150,self.pos[1]/scripts.constants.SCALE_HEIGHT+2+16,146,96))
                display.blit(self.statue_description_text_1,(self.pos[0]/scripts.constants.SCALE_WIDTH+4+16 - 150,self.pos[1]/scripts.constants.SCALE_HEIGHT+4+16))
                display.blit(self.statue_description_text_2,(self.pos[0]/scripts.constants.SCALE_WIDTH+4+16 - 150,self.pos[1]/scripts.constants.SCALE_HEIGHT+14+16))
                display.blit(self.statue_description_text_3,(self.pos[0]/scripts.constants.SCALE_WIDTH+4+16 - 150,self.pos[1]/scripts.constants.SCALE_HEIGHT+24+16))
                display.blit(self.statue_description_text_4,(self.pos[0]/scripts.constants.SCALE_WIDTH+4+16 - 150,self.pos[1]/scripts.constants.SCALE_HEIGHT+34+16))
                display.blit(self.statue_description_text_5,(self.pos[0]/scripts.constants.SCALE_WIDTH+4+16 - 150,self.pos[1]/scripts.constants.SCALE_HEIGHT+44+16))
                if not self.statue_builded:
                    display.blit(self.statue_description_text_3,(self.pos[0]/scripts.constants.SCALE_WIDTH+4+16 - 150,self.pos[1]/scripts.constants.SCALE_HEIGHT+24+16))
            
            if self.draw_crow_info:
                pygame.draw.rect(display,scripts.constants.WHITE,(self.pos[0]/scripts.constants.SCALE_WIDTH+16 - 150,self.pos[1]/scripts.constants.SCALE_HEIGHT+16,150,100))
                pygame.draw.rect(display,scripts.constants.MAINMENU_COLOR_DARKER,(self.pos[0]/scripts.constants.SCALE_WIDTH+2+16 - 150,self.pos[1]/scripts.constants.SCALE_HEIGHT+2+16,146,96))
                display.blit(self.crow_description_text_1,(self.pos[0]/scripts.constants.SCALE_WIDTH+4+16 - 150,self.pos[1]/scripts.constants.SCALE_HEIGHT+4+16))
                display.blit(self.crow_description_text_2,(self.pos[0]/scripts.constants.SCALE_WIDTH+4+16 - 150,self.pos[1]/scripts.constants.SCALE_HEIGHT+14+16))
                display.blit(self.crow_description_text_3,(self.pos[0]/scripts.constants.SCALE_WIDTH+4+16 - 150,self.pos[1]/scripts.constants.SCALE_HEIGHT+24+16))
                display.blit(self.crow_description_text_4,(self.pos[0]/scripts.constants.SCALE_WIDTH+4+16 - 150,self.pos[1]/scripts.constants.SCALE_HEIGHT+34+16))
                display.blit(self.crow_description_text_5,(self.pos[0]/scripts.constants.SCALE_WIDTH+4+16 - 150,self.pos[1]/scripts.constants.SCALE_HEIGHT+44+16))
                if not self.crow_builded:
                    display.blit(self.crow_description_text_3,(self.pos[0]/scripts.constants.SCALE_WIDTH+4+16 - 150,self.pos[1]/scripts.constants.SCALE_HEIGHT+24+16))
            
            if self.draw_upgrade_town_info:
                pygame.draw.rect(display,scripts.constants.WHITE,(self.pos[0]/scripts.constants.SCALE_WIDTH+16,self.pos[1]/scripts.constants.SCALE_HEIGHT+16,150,100))
                pygame.draw.rect(display,scripts.constants.MAINMENU_COLOR_DARKER,(self.pos[0]/scripts.constants.SCALE_WIDTH+2+16,self.pos[1]/scripts.constants.SCALE_HEIGHT+2+16,146,96))
                display.blit(self.upgrade_town_description_text_1,(self.pos[0]/scripts.constants.SCALE_WIDTH+4+16,self.pos[1]/scripts.constants.SCALE_HEIGHT+4+16))
                display.blit(self.upgrade_town_description_text_2,(self.pos[0]/scripts.constants.SCALE_WIDTH+4+16,self.pos[1]/scripts.constants.SCALE_HEIGHT+14+16))
                display.blit(self.upgrade_town_description_text_3,(self.pos[0]/scripts.constants.SCALE_WIDTH+4+16,self.pos[1]/scripts.constants.SCALE_HEIGHT+24+16))
                display.blit(self.upgrade_town_description_text_4,(self.pos[0]/scripts.constants.SCALE_WIDTH+4+16,self.pos[1]/scripts.constants.SCALE_HEIGHT+34+16))
                display.blit(self.upgrade_town_description_text_5,(self.pos[0]/scripts.constants.SCALE_WIDTH+4+16,self.pos[1]/scripts.constants.SCALE_HEIGHT+44+16))
                if not self.upgrade_town_builded:
                    display.blit(self.upgrade_town_description_text_3,(self.pos[0]/scripts.constants.SCALE_WIDTH+4+16,self.pos[1]/scripts.constants.SCALE_HEIGHT+24+16))
            
            if self.draw_walls_info:
                pygame.draw.rect(display,scripts.constants.WHITE,(self.pos[0]/scripts.constants.SCALE_WIDTH+16,self.pos[1]/scripts.constants.SCALE_HEIGHT+16,150,100))
                pygame.draw.rect(display,scripts.constants.MAINMENU_COLOR_DARKER,(self.pos[0]/scripts.constants.SCALE_WIDTH+2+16,self.pos[1]/scripts.constants.SCALE_HEIGHT+2+16,146,96))
                display.blit(self.walls_description_text_1,(self.pos[0]/scripts.constants.SCALE_WIDTH+4+16,self.pos[1]/scripts.constants.SCALE_HEIGHT+4+16))
                display.blit(self.walls_description_text_2,(self.pos[0]/scripts.constants.SCALE_WIDTH+4+16,self.pos[1]/scripts.constants.SCALE_HEIGHT+14+16))
                display.blit(self.walls_description_text_3,(self.pos[0]/scripts.constants.SCALE_WIDTH+4+16,self.pos[1]/scripts.constants.SCALE_HEIGHT+24+16))
                display.blit(self.walls_description_text_4,(self.pos[0]/scripts.constants.SCALE_WIDTH+4+16,self.pos[1]/scripts.constants.SCALE_HEIGHT+34+16))
                display.blit(self.walls_description_text_5,(self.pos[0]/scripts.constants.SCALE_WIDTH+4+16,self.pos[1]/scripts.constants.SCALE_HEIGHT+44+16))
                if not self.walls_builded:
                    display.blit(self.walls_description_text_3,(self.pos[0]/scripts.constants.SCALE_WIDTH+4+16,self.pos[1]/scripts.constants.SCALE_HEIGHT+24+16))
                
        # drawing coursor
        display.blit(self.coursor,(self.pos[0]/scripts.constants.SCALE_WIDTH,self.pos[1]/scripts.constants.SCALE_HEIGHT)) 
        