import pygame
import scripts.constants
from scripts.character import Peasant, Wizard, Paladin, Pikemen, Dwarf, Elf, Knight
from scripts.weapon import Bow, Throwable, TwoHandedSword, Spear
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
from scripts.cards_system import CardManager
from concurrent.futures import ThreadPoolExecutor
from scripts.generete import generate, reset_prev_mobs



# pygame init
pygame.mixer.init()
pygame.init()
pygame.display.init()
room = 0

# loading config
loadConfig()
# display settings etc
is_fullscreened = scripts.constants.FULLSCREEN
if is_fullscreened == True:
    screen = changeResolution((scripts.constants.SCREEN_WIDTH,scripts.constants.SCREEN_HEIGHT),False)
else:
    screen = changeResolution((scripts.constants.SCREEN_WIDTH,scripts.constants.SCREEN_HEIGHT),True)
    
display = pygame.Surface((scripts.constants.DISPLAY_WIDTH, scripts.constants.DISPLAY_HEIGHT))
fade = False
pygame_quit = False

# defining aplications name etc. and clock
pygame.display.set_caption('Dungeon Crawler')
icon = pygame.image.load("assets/icon/icon.png")
pygame.display.set_icon(icon)
clock = pygame.time.Clock()
music = Music()
time = 0
counter = None
E_pressed_counter = pygame.time.get_ticks()
E_pressed = False

# define player movement variables
moving_left = False
moving_right = False
moving_up = False
moving_down = False
moving = False
is_flipped = False

# create player
player = Peasant(120,300,100)

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

# create background and HUD
background = Bg()
hud = HUD(player,world_level)
main_menu = Menu()
town = Town()
in_town = True
build_menu = False
build_button_pressed = False
fight_key_town_button_pressed = False

#weapons
weapon = Bow(0,0,'bows','classic_bow', player.level, hud, False, player)
#weapon = Throwable(0,0,'throwables','crusader_throwing_axe', player.level, hud)
#weapon = TwoHandedSword(0,0,'two_handed_swords','sword', player.level, hud)
#weapon = Spear(0,0,'spears',"blade_on_stick", player.level + 10, hud,  False ,player)
magic_ball = None

#parciples
parcticle_system = ParticleSystem()


# create sprite groups
damage_text_group = pygame.sprite.Group()
arrow_group = pygame.sprite.Group()
item_group = pygame.sprite.Group()
magic_ball_group = pygame.sprite.Group()
keys_pressed = []

# chest item
chest_items = []

# generate level
generate_world = True

# card manager
card_manager = CardManager()

fade = True
# main game loop
game_is_on = True
game = False
new_level = False

font = pygame.font.Font("assets/fonts/font.ttf", 8)

while game_is_on:
    pygame.init()
    #delta_time = clock.tick() / 1000.0
    delta_time = 1
    
    # events system
    for event in pygame.event.get():
        if event.type == pygame.QUIT or pygame_quit:
                game_is_on = False
        if game:
            # in town events
            if in_town:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        game = False
                    if event.key == pygame.K_b:
                        time = pygame.time.get_ticks()
                        build_button_pressed = True
                    if event.key == pygame.K_f:
                        fight_key_town_button_pressed = True 
            else:
                # in game events
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
                    else:
                        # input box events
                        if event.unicode.isalpha():
                            keys_pressed.append(event.key)
                        elif event.key == pygame.K_BACKSPACE:
                            keys_pressed.append(event.key)
                            
                    if event.key == pygame.K_ESCAPE:
                        game = False
                    if event.key == pygame.K_TAB:
                        hud.info_show()
                    if event.key == pygame.K_e:
                        if pygame.time.get_ticks() - E_pressed_counter >= 1500:
                            E_pressed = True
                            E_pressed_counter = pygame.time.get_ticks()
                        else:
                            E_pressed = False
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
        else:
            # main menu events
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game = True
                   
    if game:
        if in_town:       
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
            if not in_town:
                if scripts.constants.HERO == 'player1':
                    player = Peasant(0,0,scripts.constants.PLAYER_HP)
                elif scripts.constants.HERO == 'wizard':
                    player = Wizard(0,0,scripts.constants.PLAYER_HP)
                elif scripts.constants.HERO == 'dwarf':
                     player = Dwarf(0,0,scripts.constants.PLAYER_HP)
                elif scripts.constants.HERO == 'knight':
                     player = Knight(0,0,scripts.constants.PLAYER_HP)
                elif scripts.constants.HERO == 'pikemen':
                    player = Pikemen(0,0,scripts.constants.PLAYER_HP)
                elif scripts.constants.HERO == 'elf':
                    player = Elf(0,0,scripts.constants.PLAYER_HP)
                elif scripts.constants.HERO == 'paladin':
                    player = Paladin(0,0,scripts.constants.PLAYER_HP)
                elif scripts.constants.HERO == 'druid':
                    player = scripts.character.Druid(0,0,scripts.constants.PLAYER_HP)
            town.clouds()     
            town.draw(display)
        else:  
            
            # check if new level 
            new_level = world.check_if_new_level(exit_tiles, player, new_level)
            counter = pygame.time.get_ticks()
            
            
            if fight_town_button_pressed:
                generate_world = True
                fade = True
                fight_town_button_pressed = False
                world_level = 0
                hud.seconds = 0
                hud.minutes = 0
                hud.hours = 0 
                room = 0
                new_world_level = True
                generate_world_2 = True
                levels, rooms_to_go = generate(world_level)
                if player.type == 'player1':
                    weapon = Bow(0,0,'bows','slingshot', player.level, hud, False, player)
                    hud.visible_coursor(True)
                elif player.type == 'elf':
                    weapon = Throwable(0,0,'throwables','rock', player.level, hud, False, player)
                    hud.visible_coursor(True)
                elif player.type == 'knight':
                    weapon = TwoHandedSword(0,0,'two_handed_swords','wooden_sword', player.level, hud, False, player)
                    hud.visible_coursor(False)
                elif player.type == 'pikemen':
                    weapon = Spear(0,0,'spears',"wooden_spear", player.level, hud, False, player)
                    hud.visible_coursor(False)
                        
            if new_level:
                generate_world = True
                player_hp, player_max_hp, player_gold, player_level, player_current_experience, player_experience_to_gain_new_level = world.new_level(player)
                fade = True
                new_level = True
            
            # generate new world
            if generate_world:
                # clear world data 
                chest_items.clear()
                keys_pressed.clear()
                world_data.clear()
                world_mobs_data.clear()
                boss_list.clear()
                exit_tiles.clear()
                enemy_list.clear()
                
                damage_text_group.empty()
                arrow_group.empty()
                item_group.empty()
                magic_ball_group.empty()
                
                world.map_tiles.clear()
                world.map_tiles2.clear()
                world.obstacle_tile.clear()
                world.decorations_up_tiles.clear()
                world.decorations_down_tiles.clear()
                world.character_list.clear()
                world.gate_tiles.clear()
                world.objects.clear()
                world.world_data.clear()
                world.world_data2.clear()
                world.world_mobs_and_objects_data.clear()
                world.world_decoration_down_data.clear()
                world.world_decoration_up_data.clear()
                world.walls.clear()
                if new_world_level:
                    world_level += 1 
                new_world_level = True
                
                if world_level < 3:
                    reset_prev_mobs(levels, room)
                    if world_level == 2:
                        if generate_world_2:
                            levels, rooms_to_go = generate(world_level)
                            room = rooms_to_go - rooms_to_go
                            generate_world_2 = False
                    tasks = [
                        (levels[room][0], "grassland", 1),
                        (levels[room][1], "grassland", 0),
                        (levels[room][2], "grassland", 3),
                        (levels[room][3], "grassland", 4 ),
                        (levels[room][4], "grassland", 5),
                        ]
                        
                    with ThreadPoolExecutor() as executor:
                        futures = [executor.submit(world.process_date, *task) for task in tasks]
                    
                    for future in futures:
                        future.result()
                    
                    if room == rooms_to_go - 1:
                        room = 0
                elif world_level == 3:
                    world.proced_csv_file(world_level=world_level)
                    tasks = [
                        (world.walls, "grassland", 0),
                        (world.world_data, "grassland", 1),
                        (world.world_decoration_down_data, "grassland", 3),
                        (world.world_decoration_up_data, "grassland", 4 ),
                        (world.world_mobs_and_objects_data, "grassland", 5),
                        ]
                    
                    if world.world_data2:
                        tasks.append((world.world_data2, "grassland", 2))
                        
                    with ThreadPoolExecutor() as executor:
                        futures = [executor.submit(world.process_date, *task) for task in tasks]
                    
                    for future in futures:
                        future.result()
                else:
                    world.proced_csv_file(world_level=world_level)
                    
                    tasks = [
                        (world.walls, "lavaland", 0),
                        (world.world_data, "lavaland", 1),
                        (world.world_decoration_down_data, "lavaland", 3),
                        (world.world_decoration_up_data, "lavaland", 4 ),
                        (world.world_mobs_and_objects_data, "lavaland", 5),
                        ]
                    
                    if world.world_data2:
                        tasks.append((world.world_data2, "lavaland", 2))
                        
                    with ThreadPoolExecutor() as executor:
                        futures = [executor.submit(world.process_date, *task) for task in tasks]
                    
                    for future in futures:
                        future.result()
                        
                exit_tiles = world.gate_tiles 
                enemy_list = world.character_list  
                player = world.player
                level_up = False
                generate_world = False 

                background.refresh_world_level(world_level)
                
                hud.refresh_player_image(player)
                hud.update_icon_sword(weapon.assets['icon'])
                # restore player statistic
                if new_level:
                    player.health = player_hp
                    player.health_max = player_max_hp
                    player.gold = player_gold
                    player.level = player_level
                    player.current_experience = player_current_experience
                    player.experience_to_gain_new_level = player_experience_to_gain_new_level
                    new_level = False
                

            
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
                     
            # update 
            if not level_up:
                world.update(scroll_map)
                level_up = player.update(is_flipped, moving, player.health, player.gold, hud, delta_time)
                if level_up:
                    pick_cards = True
                parcticle_system.update()
                in_town = hud.update(player, world_level, town, counter, keys_pressed)
                if player.alive:
                    if weapon.__class__ != TwoHandedSword and weapon.__class__ != Spear:
                        arrow, E_pressed = weapon.update(player, scroll_map, weapon, E_pressed, hud)
                        if arrow:   
                            arrow_group.add(arrow)
                        for arrow in arrow_group:
                            damage, damage_pos = arrow.update(weapon, enemy_list, scroll_map, world.obstacle_tile, boss_list)
                            if damage:
                                damage_text = DamageText(damage_pos.centerx, damage_pos.y, str(damage), scripts.constants.RED)
                                damage_text_group.add(damage_text)
                    else:
                        damage, damage_pos, E_pressed = weapon.update(player, scroll_map, weapon, E_pressed, hud, is_flipped, enemy_list)
                        if damage:
                            damage_text = DamageText(damage_pos.centerx, damage_pos.y, str(damage), scripts.constants.RED)
                            damage_text_group.add(damage_text)
                    damage_text_group.update(scroll_map)
                    for object in world.objects:
                        if object.type == 'chest':
                            chest_weapon = object.update(scroll_map, E_pressed, player, hud)
                            if E_pressed:
                                hud.update_icon_sword(weapon.assets['icon'])
                            if chest_weapon:
                                chest_items.append(chest_weapon)
                        elif object.type == 'next_room_enterence':
                            if object.update(scroll_map, player):
                                room += 1
                                new_level = True
                                new_world_level = False
                        elif object.type == 'previous_room_enterence':
                            if object.update(scroll_map, player):
                                room -= 1
                                new_level = True
                                new_world_level = False
                        elif object.type == 'fire_up_player':
                            object.update(scroll_map, player, world_level)
                    if chest_items:
                        for chest_item in chest_items:
                            if chest_item.__class__ != TwoHandedSword and chest_item.__class__ != Spear:
                                try:
                                    arrow, E_pressed = chest_item.update(player, scroll_map, weapon, E_pressed, hud)
                                except:
                                    pass
                            else:
                                try:
                                    damage, damage_pos, E_pressed = chest_item.update(player, scroll_map, weapon, E_pressed, hud, is_flipped, enemy_list)
                                except:
                                    pass
                    for enemy in enemy_list:
                        if enemy.type == 'druid':
                            bolt1, bolt2, bolt3, bolt4, bolt5, bolt6, bolt7, bolt8, mob = enemy.move(world.obstacle_tile, player, scroll_map)
                            if bolt1:
                                magic_ball_group.add(bolt1)
                            if bolt2:
                                magic_ball_group.add(bolt2)
                            if bolt3:
                                magic_ball_group.add(bolt3)
                            if bolt4:
                                magic_ball_group.add(bolt4)
                            if bolt5:
                                magic_ball_group.add(bolt5)
                            if bolt6:
                                magic_ball_group.add(bolt6)
                            if bolt7:
                                magic_ball_group.add(bolt7)
                            if bolt8:
                                magic_ball_group.add(bolt8) 
                            if mob:
                                enemy_list.append(mob)   
                        else:
                            magic_ball = enemy.move(world.obstacle_tile, player, scroll_map)
                        if magic_ball:
                            magic_ball_group.add(magic_ball)
                        enemy.hit_player(enemy.damage, player)
                        if enemy.type == 'druid':
                            gold_, potion_, enemy_alive, exit_tiles  = enemy.update(player, world.obstacle_tile, hud, town, exit_tiles)
                        else:
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
                    for magic_ball in magic_ball_group:
                        if magic_ball.type == 'druid_bolt':
                            magic_ball.update(scroll_map, player)
                        else:
                            magic_ball.update(scroll_map, player, world.obstacle_tile)
                    if player.is_on_fire:
                        player.on_fire()
                if not player.alive:
                    end = player.died()
                    if end:
                        game_is_on = False
            else:
                if pick_cards:
                    card_manager.pick_cards()
                    pick_cards = False
                level_up = card_manager.update(player, hud, weapon)
            # draw             
            background.draw(display)
            world.draw(display)
            if scripts.constants.SHOW_GRID:
                draw_grid(display)
            for items in item_group:
                items.draw(display)
            if chest_items:
                for chest_item in chest_items:
                        chest_item.draw(display)
            world.draw_src(display,exit_tiles)
            damage_text_group.draw(display)
            for enemy in enemy_list:
                enemy.draw(display)
            parcticle_system.draw(display)
            player.draw(display)
            if player.alive:
                weapon.draw(display)
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
            if level_up:
                card_manager.draw(display)
                
                
        # main menu handler    
    elif not game:
        game, pygame_quit = main_menu.update(music,screen, player, weapon, enemy_list, boss_list, magic_ball_group) #main_menu.update(music,screen, player, bow, enemy_list, boss_list, magic_ball_group)
        main_menu.draw(display)
        if pygame_quit:
            pygame.quit()
        
    # fps handler
    if scripts.constants.SHOW_FPS:
        fps = clock.get_fps()
        fps_to_show = font.render(f'FPS:{int(fps)}', True, scripts.constants.WHITE)
        display.blit(fps_to_show, (scripts.constants.DISPLAY_WIDTH - int(fps_to_show.get_width()) - 2, scripts.constants.DISPLAY_HEIGHT - int(fps_to_show.get_height() + 2)))
        
    # display all on screen
    try:
        if pygame.display.get_init():
            pygame.display.update()
    except:
        pass
    
    
    
    clock.tick(60)
    try:
        screen.blit(pygame.transform.scale(display, screen.get_size()),(0, 0))
    except:
        pass
    
