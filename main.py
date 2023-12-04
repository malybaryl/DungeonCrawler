import pygame
import scripts.constants
from scripts.character import Character
from scripts.weapon import Bow
from scripts.changeResolution import changeResolution
from scripts.load import loadConfig
from scripts.background import Bg
from scripts.enemies import Orc
from scripts.damageText import DamageText
from scripts.HUD import HUD
from scripts.items import Item

# loading config
loadConfig()

# pygame init
pygame.init()

# display settings etc
is_fullscreened = scripts.constants.FULLSCREEN
if is_fullscreened == True:
    screen = changeResolution((scripts.constants.SCREEN_WIDTH,scripts.constants.SCREEN_HEIGHT),False)
else:
    screen = changeResolution((scripts.constants.SCREEN_WIDTH,scripts.constants.SCREEN_HEIGHT),True)
display = pygame.Surface((scripts.constants.DISPLAY_WIDTH, scripts.constants.DISPLAY_HEIGHT))

# defining aplications name etc. and clock
pygame.display.set_caption('Dungeon Clawler')
clock = pygame.time.Clock()

# define player movement variables
moving_left = False
moving_right = False
moving_up = False
moving_down = False
moving = False
is_flipped = False

# create player and player wepon
player = Character(100,100,100)
bow = Bow("classicBow",100,100)

# create background and HUD
background = Bg()
hud = HUD(player)

# create mobs
orc = Orc(50,50,100)

# create enoty enemy list
enemy_list = []
enemy_list.append(orc)

# create sprite groups
damage_text_group = pygame.sprite.Group()
arrow_group = pygame.sprite.Group()
item_group = pygame.sprite.Group()

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

    # move enemies 
    orc.move()
    
    # update 
    player.update(is_flipped, moving, player.health, player.gold)
    hud.update(player)
    arrow = bow.update(player)
    if arrow:
        arrow_group.add(arrow)
    for arrow in arrow_group:
        damage, damage_pos = arrow.update(enemy_list)
        if damage:
            damage_text = DamageText(damage_pos.centerx, damage_pos.y, str(damage), scripts.constants.RED)
            damage_text_group.add(damage_text)
    damage_text_group.update()
    for enemy in enemy_list:
        enemy.hit_player(10,player)
        gold_, potion_, enemy_alive = enemy.update(player)
        if gold_:
            item_group.add(Item(enemy.rect.center[0],enemy.rect.center[1],"coin"))
        if potion_:
            item_group.add(Item(enemy.rect.center[0],enemy.rect.center[1],"health_potion"))
        if not enemy_alive:
            enemy_list.pop()
    for item in item_group:
        item.update(player)
    background.update()

    # draw 
    background.draw(display)
    player.draw(display)
    bow.draw(display)
    for arrow in arrow_group:
        arrow.draw(display)
    for items in item_group:
        items.draw(display)
    damage_text_group.draw(display)
    for enemy in enemy_list:
        enemy.draw(display)
    hud.draw(display)
    
    # display all on screen
    pygame.display.update()
    clock.tick(60)
    screen.blit(pygame.transform.scale(display, screen.get_size()),(0, 0))