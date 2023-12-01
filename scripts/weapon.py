import pygame
import scripts.constants
import math
from scripts.load import loadImage, loadImages

class Bow:
    def __init__(self):
        self.assets = {
            "bow": loadImages("wepons/bow")
        }

    def draw(self, surface):
        surface.blit(self.assets["bow"][0], (100,100))

class Arrow:
    def __init__(self):
        self.assets = {
            "arrow": loadImages("wepons/arrow")
        }

    def draw(self, surface):
        surface.blit(self.assets["arrow"][0], (60,100))