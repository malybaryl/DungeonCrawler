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
    if words[3][1]== "yes":
        scripts.constants.SHOW_HITBOX = True
    else:
        scripts.constants.SHOW_HITBOX = False
    if words[4][1]== "yes":
        scripts.constants.SHOW_GRID = True
    else:
        scripts.constants.SHOW_GRID = False
    if words[5][1]== "yes":
        scripts.constants.SHOW_LINE_OF_SIGHT = True
    else:
        scripts.constants.SHOW_LINE_OF_SIGHT = False
    if words[6][1]== "yes":
        scripts.constants.MUSIC = True
    else:
        scripts.constants.MUSIC = False
    scripts.constants.MUSIC_VOLUME = float(words[7][1])
    scripts.constants.FX_VOLUME = float(words[8][1])

def change_values_of_config(key, new_value):
    with open("config/config.txt", 'r') as f:
        lines = f.readlines()

    found = False
    for i, line in enumerate(lines):
        if line.startswith(key):
            lines[i] = f"{key} {new_value}\n"
            found = True
            break

    if not found:
        lines.append(f"{key} {new_value}\n")

    with open("config/config.txt", 'w') as f:
        f.writelines(lines)


def loadCredits():
    lines = []

    with open("credits/credits.txt", encoding="UTF-8") as f:
        for line in f:
            lines.append(line.strip())
    
    return lines

        
    
    