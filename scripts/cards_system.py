import pygame
import scripts.constants
from random import choice
from scripts.load import loadImage


class CardManager():
    def __init__(self):
        self.cards = []
        self.time = pygame.time.get_ticks()
    
    def pick_cards(self):
        self.cards.clear()
        self.time = pygame.time.get_ticks()
        for x in range(3):
            card = choice(scripts.constants.CARDS)
            if card == 'health_card':
                self.cards.append(HealthCard(x))
            elif card == 'light_attack_card':
                self.cards.append(LightAttackCard(x))
            elif card == 'heavy_attack_card':
                self.cards.append(HeavyAttackCard(x))
                
                
    
    def update(self, player, hud, weapon):
        loop = True
        if pygame.time.get_ticks() - self.time >= 500:
            for card in self.cards:
                loop = card.update(player, hud, weapon)
                if not loop:
                    break
        return loop
            
    def draw(self, display):
        for card in self.cards:
            card.draw(display)

class LevelUpCard:
    def __init__(self, assets, title, description_line_1, description_line_2, description_line_3
                 , description_line_4, description_line_5, description_line_6, description_line_7,
                 card_counter):
        self.assets = assets
        self.pos = pygame.mouse.get_pos()
        width, height = self.assets['card_image'].get_size()
        self.rect = pygame.rect.Rect(0, 0, width, height)
        if card_counter == 1:
            self.rect.center = (176, 55)
        elif card_counter == 2:
            self.rect.center = (32, 55)
        else:
            self.rect.center = (320, 55)
        self.card_counter = card_counter
        self.title = title
        self.title_image_to_show = self.assets['font_8'].render(self.title, True, scripts.constants.BLACK)
        self.description_line_1 = description_line_1
        self.description_line_2 = description_line_2
        self.description_line_3 = description_line_3
        self.description_line_4 = description_line_4
        self.description_line_5 = description_line_5
        self.description_line_6 = description_line_6
        self.description_line_7 = description_line_7
        self.description_line_1_ = self.assets['font_8'].render(self.description_line_1, True, scripts.constants.BLACK)
        self.description_line_2_ = self.assets['font_8'].render(self.description_line_2, True, scripts.constants.BLACK)
        self.description_line_3_ = self.assets['font_8'].render(self.description_line_3, True, scripts.constants.BLACK)
        self.description_line_4_ = self.assets['font_8'].render(self.description_line_4, True, scripts.constants.BLACK)
        self.description_line_5_ = self.assets['font_8'].render(self.description_line_5, True, scripts.constants.BLACK)
        self.description_line_6_ = self.assets['font_8'].render(self.description_line_6, True, scripts.constants.BLACK)
        self.description_line_7_ = self.assets['font_8'].render(self.description_line_7, True, scripts.constants.BLACK)
        self.coursor = None
        self.coursor_2 = None
        self.load_coursor_images_once = True
    
    
    def update(self, player, hud, weapon):
        loop = True
        if self.load_coursor_images_once:
            self.coursor = hud.assets['coursor'][4]
            self.coursor_2 = hud.assets['coursor'][5]
        self.pos = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0]:
            self.coursor = self.coursor_2
            if self.rect.centerx < self.pos[0]/scripts.constants.SCALE_WIDTH < self.rect.centerx + self.rect.width and self.rect.centery < self.pos[1]/scripts.constants.SCALE_HEIGHT < self.rect.centery + self.rect.height:
                self.activate(player, hud, weapon)
                loop = False
        return loop
            
        
    def draw(self, display):
        try:
            # drawing card
            display.blit(self.assets['card_image'],(self.rect.centerx, self.rect.centery))
            display.blit(self.title_image_to_show, (self.rect.centerx + 11, self.rect.centery + 7))
            display.blit(self.description_line_1_, (self.rect.centerx + 11, self.rect.centery + 95))
            display.blit(self.description_line_2_, (self.rect.centerx + 11, self.rect.centery + 103))
            display.blit(self.description_line_3_, (self.rect.centerx + 11, self.rect.centery + 111))
            display.blit(self.description_line_4_, (self.rect.centerx + 11, self.rect.centery + 119))
            display.blit(self.description_line_5_, (self.rect.centerx + 11, self.rect.centery + 127))
            display.blit(self.description_line_6_, (self.rect.centerx + 11, self.rect.centery + 135))
            display.blit(self.description_line_7_, (self.rect.centerx + 11, self.rect.centery + 143))
            # drawing coursor
            display.blit(self.coursor,(self.pos[0]/scripts.constants.SCALE_WIDTH,self.pos[1]/scripts.constants.SCALE_HEIGHT)) 
        except:
            pass
        
            
    
class HealthCard(LevelUpCard):
    def __init__(self, card_counter):
        assets ={
            'card_image': loadImage('cards/0.png'),
            "font_8": pygame.font.Font("assets/fonts/font.ttf",8)
         }
        title = 'STRONG HEARTH'
        description_line_1 = 'The Character'
        description_line_2 = 'will have more'
        description_line_3 = '50 points of'
        description_line_4 = 'maximum health'
        description_line_5 = ''
        description_line_6 = ''
        description_line_7 = ''
        super().__init__(assets, title, description_line_1, description_line_2, description_line_3,
                         description_line_4, description_line_5, description_line_6, description_line_7,
                         card_counter)
        self.health_to_add = 50
        
    def activate(self, player, hud, weapon):
        player.health_max += self.health_to_add
        hud.update_character_health_bar(player)



class LightAttackCard(LevelUpCard):
    def __init__(self, card_counter):
        assets ={
            'card_image': loadImage('cards/1.png'),
            "font_8": pygame.font.Font("assets/fonts/font.ttf",8)
         }
        title = 'LIGHT ATTACK'
        description_line_1 = 'Minimal damage'
        description_line_2 = 'inrease by'
        description_line_3 = '20%'
        description_line_4 = ''
        description_line_5 = ''
        description_line_6 = ''
        description_line_7 = ''
        super().__init__(assets, title, description_line_1, description_line_2, description_line_3,
                         description_line_4, description_line_5, description_line_6, description_line_7,
                         card_counter)
        self.min_damage_mulitplied = 0.2
        
    def activate(self, player, hud, weapon):
        player.minimal_damage_multiplied += self.min_damage_mulitplied
        weapon.update_minimal_damage(player, hud)



class HeavyAttackCard(LevelUpCard):
    def __init__(self, card_counter):
        assets ={
            'card_image': loadImage('cards/2.png'),
            "font_8": pygame.font.Font("assets/fonts/font.ttf",8)
         }
        title = 'HEAVY ATTACK'
        description_line_1 = 'Maximal damage'
        description_line_2 = 'inrease by'
        description_line_3 = '10%'
        description_line_4 = ''
        description_line_5 = ''
        description_line_6 = ''
        description_line_7 = ''
        super().__init__(assets, title, description_line_1, description_line_2, description_line_3,
                         description_line_4, description_line_5, description_line_6, description_line_7,
                         card_counter)
        self.max_damage_mulitplied = 0.1
        
    def activate(self, player, hud, weapon):
        player.maximal_damage_multiplied += self.max_damage_mulitplied
        weapon.update_maximal_damage(player, hud)