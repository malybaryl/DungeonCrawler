import pygame
import scripts.constants
from scripts.load import loadImage, loadImages

class HUD:
    def __init__(self, player):
        self.assets={
            "coursor": loadImages("HUD/coursor"),
            "gold": pygame.transform.scale(loadImage("coin/0.png"),(16,16))
        }
        pygame.mouse.set_visible(False)    
        self.pos = None
        self.full_health = player.health
        self.health = player.health
        self.gold = player.gold
        self.font = pygame.font.Font("assets/fonts/font.ttf",8)
        self.image = self.font.render(str(self.gold), True, scripts.constants.WHITE)
    
    def update(self, player):
        self.pos = pygame.mouse.get_pos()
        self.health = player.health
        self.gold = player.gold
        self.image = self.font.render(str(self.gold), True, scripts.constants.WHITE)

    def draw(self, display):
        # drawing HUD Background
        pygame.draw.rect(display,scripts.constants.COLORHUD,(0,0,scripts.constants.DISPLAY_WIDTH,20))
        # drawing player health
        pygame.draw.rect(display,scripts.constants.DARKRED,(5,5,self.full_health,10))
        pygame.draw.rect(display,scripts.constants.RED,(5,5,self.health,10))
        # drawing info gold
        display.blit(self.assets["gold"],(self.full_health+5,2))
        display.blit(self.image,(self.full_health+22,8))
        # drawing coursor
        display.blit(pygame.transform.scale(self.assets["coursor"][0],(24,24)),(self.pos[0]/scripts.constants.SCALE_WIDTH,self.pos[1]/scripts.constants.SCALE_HEIGHT)) 
        display.blit(pygame.transform.scale(self.assets["coursor"][1],(24,24)),(self.pos[0]/scripts.constants.SCALE_WIDTH-24,self.pos[1]/scripts.constants.SCALE_HEIGHT-24)) 
        display.blit(pygame.transform.scale(self.assets["coursor"][2],(24,24)),(self.pos[0]/scripts.constants.SCALE_WIDTH,self.pos[1]/scripts.constants.SCALE_HEIGHT-24)) 
        display.blit(pygame.transform.scale(self.assets["coursor"][3],(24,24)),(self.pos[0]/scripts.constants.SCALE_WIDTH-24,self.pos[1]/scripts.constants.SCALE_HEIGHT)) 