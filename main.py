import pygame
import scripts.constants
from scripts.character import Character
from scripts.weapon import Bow, Arrow
from scripts.changeResolution import changeResolution
from scripts.load import loadConfig
from scripts.background import Bg
from scripts.enemies import Orc

loadConfig()

pygame.init()

is_fullscreened = scripts.constants.FULLSCREEN
if is_fullscreened == True:
    screen = changeResolution((scripts.constants.SCREEN_WIDTH,scripts.constants.SCREEN_HEIGHT),False)
else:
    screen = changeResolution((scripts.constants.SCREEN_WIDTH,scripts.constants.SCREEN_HEIGHT),True)
display = pygame.Surface((scripts.constants.DISPLAY_WIDTH, scripts.constants.DISPLAY_HEIGHT))
pygame.display.set_caption('Dungeon Clawler')
clock = pygame.time.Clock()

# define player movement variables
moving_left = False
moving_right = False
moving_up = False
moving_down = False
moving = False
is_flipped = False


# create player
player = Character(100,100)
bow = Bow()
aroow = Arrow()
background = Bg()
orc = Orc(0,50)
# main game loop
game_is_on = True
while game_is_on:

    # event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        # take keyboard presses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                moving_left = True
            if event.key == pygame.K_d:
                moving_right = True
            if event.key == pygame.K_w:
                moving_up = True
            if event.key == pygame.K_s:
                moving_down = True
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                   
        # keyboard button relaeased
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False
            if event.key == pygame.K_w:
                moving_up = False
            if event.key == pygame.K_s:
                moving_down = False


    # background color
    display.fill(scripts.constants.BG)

    # calculate player movement
    dx = 0
    dy = 0
    moving = False
    if moving_right:
        dx = scripts.constants.SPEED
        is_flipped = False
        moving = True
    if moving_left:
        dx = -scripts.constants.SPEED
        is_flipped = True
        moving = True
    if moving_up:
        dy = -scripts.constants.SPEED
        moving = True
    if moving_down:
        dy = scripts.constants.SPEED
        moving = True

    # move player
    player.move(dx,dy)
    orc.move()
    
    # update player
    player.update(is_flipped, moving)
    orc.update()
    background.update()
    # draw player on screen
    background.draw(display)
    player.draw(display)
    bow.draw(display)
    aroow.draw(display)
    orc.draw(display)
    

    pygame.display.update()
    clock.tick(60)
    screen.blit(pygame.transform.scale(display, screen.get_size()),(0, 0))