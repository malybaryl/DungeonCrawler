import pygame

def changeResolution(resolution = (0,0), isFullscrened = False):
    if isFullscrened:
        screen = pygame.display.set_mode((resolution[0],resolution[1]))
    else:
        screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
    return screen