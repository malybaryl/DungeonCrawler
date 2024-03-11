import pygame
import scripts.constants
from scripts.character import Character
from scripts.weapon import Bow, TwoHandedSword, Mace, OneHandedAxe, OneHandedHammer
from scripts.changeResolution import changeResolution
from scripts.load import loadConfig
from scripts.background import Bg
from scripts.damageText import DamageText
from scripts.HUD import HUD
from scripts.items import Item
from scripts.world import draw_grid, World 
from scripts.music import Music
from scripts.menu import Menu
from scripts.town import Town
from scripts.particles import ParticleSystem

# loading config
loadConfig()

# pygame init
pygame.mixer.init()
pygame.init()

# display settings etc
is_fullscreened = scripts.constants.FULLSCREEN
if is_fullscreened == True:
    screen = changeResolution((scripts.constants.SCREEN_WIDTH,scripts.constants.SCREEN_HEIGHT),False)
else:
    screen = changeResolution((scripts.constants.SCREEN_WIDTH,scripts.constants.SCREEN_HEIGHT),True)
display = pygame.Surface((scripts.constants.DISPLAY_WIDTH, scripts.constants.DISPLAY_HEIGHT))
fade = False

# defining aplications name etc. and clock
pygame.display.set_caption('Dungeon Crawler')
icon = pygame.image.load("assets/icon/icon.png")
pygame.display.set_icon(icon)
clock = pygame.time.Clock()
music = Music()
time = 0

# define player movement variables
moving_left = False
moving_right = False
moving_up = False
moving_down = False
moving = False
is_flipped = False
E_pressed = False

# create player and player wepon
player = Character(120,300,100,"player1")
bow = Bow("crossbow",100,100)
#sword = OneHandedHammer('hammer',100,100)
magic_ball = None

#define game varibles
scroll_map = [player.rect.x,player.rect.y]

# create level1
world = World()
mobs_world = World()
world_data = []
world_mobs_data = []
boss_list=[]
exit_tiles=[]
enemy_list=[]
world_level = 0
fight_town_button_pressed = False
world.proced_csv_file()

# create background and HUD
background = Bg()
hud = HUD(player,world_level)
main_menu = Menu()
town = Town()
in_town = True
build_menu = False
build_button_pressed = False
fight_key_town_button_pressed = False


#parciples
parcticle_system = ParticleSystem()


# create sprite groups
damage_text_group = pygame.sprite.Group()
arrow_group = pygame.sprite.Group()
item_group = pygame.sprite.Group()
magic_ball_group = pygame.sprite.Group()

# generate level
generate_world = True

fade = True
# main game loop
game_is_on = True
game = False
while game_is_on:

    if game:
        if in_town:
            # event handler
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        game = False
                    if event.key == pygame.K_b:
                        time = pygame.time.get_ticks()
                        build_button_pressed = True
                    if event.key == pygame.K_f:
                        fight_key_town_button_pressed = True
                
            if build_button_pressed:
                if (pygame.time.get_ticks() - time) >= 100:
                    if build_menu:
                        build_menu = False
                    else:
                        build_menu = True
                    build_button_pressed = False
            
            if fight_key_town_button_pressed:
                if (pygame.time.get_ticks() - time) >= 100:
                    if fight_town_button_pressed:
                        fight_town_button_pressed = False
                    else:
                        fight_town_button_pressed = True
                    fight_key_town_button_pressed = False
                    
                    
            in_town, build_menu, fight_town_button_pressed = town.update(build_menu, fight_town_button_pressed)
            town.clouds()     
            town.draw(display)
        else:  
            
            # check if new level
            new_level = world.check_if_new_level(exit_tiles, player)
            
            if fight_town_button_pressed:
                generate_world = True
                fade = True
                fight_town_button_pressed = False
                world_level = 0
                
        
            if new_level:
                generate_world = True
                player_hp, player_max_hp, player_gold = world.new_level(player)
                fade = True
                new_level = True
            
            # generate new world
            if generate_world:
                # clear world data 
                world_data.clear()
                enemy_list.clear()
                boss_list.clear()
                exit_tiles.clear()
                world.world_mobs_data.clear()
                world.obstacle_tile.clear()
                world.decorations_up_tiles.clear()
                world.map_tiles.clear()
                world.boss_list.clear()
                world.objects.clear()
                world.proced_csv_file()
                # generete new level
                #world_data = world.generate()  
                #world_mobs_data=world.generate()
                player, enemy_list, boss_list, exit_tiles= world.process_date(world.world_data, "grassland")
                player, enemy_list, boss_list, exit_tiles= world.process_date(world.world_mobs_data, "grassland")
                player, enemy_list, boss_list, exit_tiles = world.process_date(world.world_objects_data, "grassland")
                player, enemy_list, boss_list, exit_tiles= world.process_date(world.world_decorations_up, "grassland")
                player, enemy_list, boss_list, exit_tiles= world.process_date(world.world_decorations_down, "grassland")
                
                generate_world = False 
                world_level += 1 
                # restore player statistic
                if new_level:
                    player.health = player_hp
                    player.health_max = player_max_hp
                    player.gold = player_gold
                    new_level = False

            
            # event handler
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

                # take keyboard presses
                if event.type == pygame.KEYDOWN:
                    if player.alive:
                        if event.key == pygame.K_a:
                            moving_left = True
                        if event.key == pygame.K_d:
                            moving_right = True
                        if event.key == pygame.K_w:
                            moving_up = True
                        if event.key == pygame.K_s:
                            moving_down = True
                    if event.key == pygame.K_ESCAPE:
                        game = False
                    if event.key == pygame.K_TAB:
                        hud.info_show()
                    if event.key == pygame.K_e:
                        E_pressed = True
                        
                        

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
                    if event.key == pygame.K_e:
                        E_pressed = False

            
            # calculate player movement
            dx = 0
            dy = 0
            moving = False
            if moving_right:
                dx = scripts.constants.SPEED
                is_flipped = False
                moving = True
                parcticle_system.create_particle(player.rect.x+player.rect.width/2, player.rect.y+player.rect.height,scripts.constants.BROWN,'left')
            if moving_left:
                dx = -scripts.constants.SPEED
                is_flipped = True
                moving = True
                parcticle_system.create_particle(player.rect.x+player.rect.width/2, player.rect.y+player.rect.height,scripts.constants.BROWN,'right')
            if moving_up:
                dy = -scripts.constants.SPEED
                moving = True
                parcticle_system.create_particle(player.rect.x+player.rect.width/2, player.rect.y+player.rect.height,scripts.constants.BROWN,'down')
            if moving_down:
                dy = scripts.constants.SPEED
                moving = True
                parcticle_system.create_particle(player.rect.x+player.rect.width/2, player.rect.y+player.rect.height,scripts.constants.BROWN,'up')
                
            
            
            # move player
            scroll_map = player.move(dx,dy, world.obstacle_tile)
            
                # for boss in boss_list:
                #     boss.move(world.obstacle_tile, player, scroll_map)
            
            # update 
            world.update(scroll_map)
            player.update(is_flipped, moving, player.health, player.gold)
            parcticle_system.update()
            for object in world.objects:
                if object.type == 'chest':
                    object.update(scroll_map, E_pressed, player)
            in_town = hud.update(player, world_level, town)
            if player.alive:
                # sword
                # damage, damage_pos = sword.update(player, is_flipped, enemy_list)
                # if damage:
                #     damage_text = DamageText(damage_pos.centerx, damage_pos.y, str(damage), scripts.constants.RED)
                #     damage_text_group.add(damage_text)
                arrow = bow.update(player)
                if arrow:   
                    arrow_group.add(arrow)
                for arrow in arrow_group:
                    damage, damage_pos = arrow.update(enemy_list, scroll_map, world.obstacle_tile, boss_list)
                    if damage:
                        damage_text = DamageText(damage_pos.centerx, damage_pos.y, str(damage), scripts.constants.RED)
                        damage_text_group.add(damage_text)
                damage_text_group.update(scroll_map)
                for enemy in enemy_list:
                    magic_ball = enemy.move(world.obstacle_tile, player, scroll_map)
                    if magic_ball:
                        magic_ball_group.add(magic_ball)
                    enemy.hit_player(enemy.damage, player)
                    gold_, potion_, enemy_alive, show_hp = enemy.update(player, world.obstacle_tile)
                    if enemy.delete:
                        if gold_:
                            item_group.add(Item(enemy.rect.center[0],enemy.rect.center[1],"coin"))
                        if potion_:
                            item_group.add(Item(enemy.rect.center[0],enemy.rect.center[1],"health_potion"))
                        enemy_list.remove(enemy)    
                for item in item_group:
                    item.update(player, scroll_map)
                background.update()
                #draw_hp_boss, magic_ball = boss.update(player,world.obstacle_tile)
                for magic_ball in magic_ball_group:
                    player.is_on_fire = magic_ball.update(scroll_map, player, world.obstacle_tile)
                if player.is_on_fire:
                    player.on_fire()
            if not player.alive:
                end = player.died()
                if end:
                    game_is_on = False
            
            # draw 
            
            background.draw(display)
            world.draw(display)
            if scripts.constants.SHOW_GRID:
                draw_grid(display)
            for items in item_group:
                items.draw(display)
            
            world.draw_src(display,exit_tiles)
            damage_text_group.draw(display)
            for enemy in enemy_list:
                enemy.draw(display)
            # for boss in boss_list:
            #     boss.draw(display)
            if show_hp:
                hud.draw_boss_hp(display,enemy.health, enemy.max_health, enemy.name)
            parcticle_system.draw(display)
            player.draw(display)
            if player.alive:
                #sword.draw(display)
                bow.draw(display)
            for object in world.objects:
                object.draw(display)
            for arrow in arrow_group:
                arrow.draw(display)
            for magic_ball in magic_ball_group:
                magic_ball.draw(display)
            world.draw_src(display, world.decorations_up_tiles)
            hud.draw(display)
            if fade:
                fade = hud.draw_fade(display)
            hud.draw_red_fade(display,player)
            
            

    # main menu handler    
    elif not game:
        game = main_menu.update(music,screen, player, bow, enemy_list, boss_list, magic_ball_group) #main_menu.update(music,screen, player, bow, enemy_list, boss_list, magic_ball_group)
        main_menu.draw(display)
        
        # event handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game = True
    
        

    # display all on screen
    pygame.display.update()
    clock.tick(60)
    screen.blit(pygame.transform.scale(display, screen.get_size()),(0, 0))