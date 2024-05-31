import pygame
import scripts.constants

def changeResolution(resolution = (0,0), isFullscrened = False):
    pygame.init()
    if isFullscrened:
        screen = pygame.display.set_mode((resolution[0],resolution[1]))
        display_size=pygame.display.get_window_size()
        scripts.constants.SCALE_WIDTH = display_size[0] / scripts.constants.DISPLAY_WIDTH
        scripts.constants.SCALE_HEIGHT = display_size[1] / scripts.constants.DISPLAY_HEIGHT
    else:
        screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        display_size=pygame.display.get_window_size()
        scripts.constants.SCALE_WIDTH = display_size[0] / scripts.constants.DISPLAY_WIDTH
        scripts.constants.SCALE_HEIGHT = display_size[1] / scripts.constants.DISPLAY_HEIGHT
        
    return screen