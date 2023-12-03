import pygame
import os
import scripts.constants

BASE_IMG_PATH = "assets/images/"

def loadImage(path):
    return pygame.image.load(BASE_IMG_PATH + path).convert_alpha()

def loadImages(path):
    images = []
    for img_name in sorted(os.listdir(BASE_IMG_PATH + path)):
        images.append(loadImage(path + "/" + img_name))
    return images

def loadConfig():
    
    words = []

    with open("config/config.txt", encoding="UTF-8") as f:
        for line in f:
            words.append(line.strip().split(" "))
   
    scripts.constants.SCREEN_WIDTH = int(words[0][1])
    scripts.constants.SCREEN_HEIGHT = int(words[1][1])
    if words[2][1]== "yes":
        scripts.constants.FULLSCREEN = True
    else:
        scripts.constants.FULLSCREEN = False
    