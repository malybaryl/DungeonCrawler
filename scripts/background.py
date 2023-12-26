from scripts.load import loadImages
import scripts.constants
import pygame

class Bg():
    def __init__(self):
        self.x = 0
        self.assets ={
        "bg": loadImages("background")
        }
    
    def update(self):
        self.x += 1
        if self.x > scripts.constants.DISPLAY_WIDTH:
            self.x = -scripts.constants.DISPLAY_WIDTH

    def draw(self, surface):
        surface.fill(scripts.constants.BG)
        #surface.blit(pygame.transform.flip(self.assets["bg"][0],False,True), (self.x,-175))
        #surface.blit(self.assets["bg"][1], (-self.x,50))

