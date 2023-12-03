import pygame
import scripts.constants
from scripts.load import loadImage

class HUD:
    def __init__(self, player):
        self.assets={
            "coursor": pygame.transform.scale(loadImage("HUD/coursor.png"),(24,24))
        }
        pygame.mouse.set_visible(False)    
        self.pos = None
        self.full_health = player.health
        self.health = player.health
    
    def update(self, player):
        self.pos = pygame.mouse.get_pos()
        self.health = player.health

    def draw(self, display):
        # drawing HUD Background
        pygame.draw.rect(display,scripts.constants.COLORHUD,(0,0,scripts.constants.DISPLAY_WIDTH,20))
        # drawing player health
        pygame.draw.rect(display,scripts.constants.DARKRED,(5,5,self.full_health,10))
        pygame.draw.rect(display,scripts.constants.RED,(5,5,self.health,10))
        # drawing coursor
        display.blit(self.assets["coursor"],(self.pos[0]/scripts.constants.SCALE_WIDTH,self.pos[1]/scripts.constants.SCALE_HEIGHT)) 