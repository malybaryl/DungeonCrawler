from random import randint, choice
from concurrent.futures import ThreadPoolExecutor

def generating_grassland(room, rooms_to_go):
    fence_chance_spawn = 20 # 0 - 100
    decorations_chance_spawn = 5 # 0 - 100
    grass_map_chance = 1 # 0-100
    treasure_room_chance = 10 # 0 - 10
    grass_map = False
    ent_chance_spawn = 25 # 0-100
    world_level = 1
    slime_chance_spawn = 50
    wolf_chance_spawn = 10
    goblin_chance_spawn = 20
    troll_chance_spawn = 20
    max_enemy_chance = slime_chance_spawn + wolf_chance_spawn + goblin_chance_spawn + troll_chance_spawn
    
    if room != 1 and room != rooms_to_go:
        chance_for_trasure_room = randint(0,100)
        if chance_for_trasure_room > treasure_room_chance:
            choose_kind_of_room = randint(0,3)
            if choose_kind_of_room == 0:
                # ground
                amount_of_enemies = randint(1 * world_level, 2* world_level)
                rows_and_cols = 10
                ground = [[-1 for _ in range(rows_and_cols)] for _ in range(rows_and_cols)]
                walls = [[-1 for _ in range(rows_and_cols)] for _ in range(rows_and_cols)]
                decorations_down = [[-1 for _ in range(rows_and_cols)] for _ in range(rows_and_cols)]
                decorations_up = [[-1 for _ in range(rows_and_cols)] for _ in range(rows_and_cols)]
                mobs_and_objects = [[-1 for _ in range(rows_and_cols)] for _ in range(rows_and_cols)]
                
                # first row
                ground[0][1] = 22
                walls[0][1] = 99
                for x in range (2, rows_and_cols - 2):
                    ground[0][x] = 23
                    walls[0][x] = 99
                ground[0][rows_and_cols - 2] = 24
                walls[0][rows_and_cols - 2] = 99
                
                chance_for_grass_map = randint (0,100)
                if chance_for_grass_map <= grass_map_chance:
                    grass_map = True
                # fill middle
                for x in range (1, rows_and_cols - 1):
                    for y in range (1, rows_and_cols - 1):
                        ground [y][x] = choice([72,82,83,84])
                        # decorations random
                        if not grass_map: 
                            chance = randint(0,100)
                            if chance <= decorations_chance_spawn:
                                if y != rows_and_cols // 2 and y != rows_and_cols//2 - 1:
                                    if x != rows_and_cols // 2 and x != rows_and_cols//2 - 1:
                                        choose_decoration = choice([2,3,10,11,12,13,21,25,90,96])
                                        if choose_decoration != 90:
                                            decorations_down[y][x] = choose_decoration
                                            if choose_decoration != 21 and choose_decoration != 25:
                                                walls[y][x] = 99
                                        else:
                                            if y>1:
                                                decorations_down[y][x] = choose_decoration
                                                walls[y][x] = 99
                                                decorations_up[y-1][x] = 80
                                                decorations_up[y-2][x] = 70        
                        else:
                            decorations_up[y][x] = 20
                                
                # first col
                ground[1][0] = 31
                walls[0][0] = 99
                walls[1][0] = 99
                y = 2
                while y < rows_and_cols - 2:
                    if y != rows_and_cols // 2 - 2:
                        ground[y][0] = 71
                        walls[y][0] = 99
                        y += 1
                    else:
                        ground[y][0] = 41 
                        walls[y][0] = 99
                        ground[y + 1][0] = choice([72,82,83,84])
                        mobs_and_objects[y + 1][0] = 101
                        walls[y + 1][0] = 99
                        ground[y + 2][0] = choice([72,82,83,84])
                        walls[y + 2][0] = 99
                        ground[y + 3][0] = 61
                        walls[y + 3][0] = 99
                        y += 4 
                ground[rows_and_cols - 2][0] = 81
                walls[rows_and_cols - 2][0] = 99
                ground[rows_and_cols - 1][0] = 91
                walls[rows_and_cols - 1][0] = 99
                
                # last row
                for x in range (1, rows_and_cols - 1):
                    ground[rows_and_cols - 1][x] = 92
                    walls[rows_and_cols - 1][x] = 99
                
                # last col
                ground[1][rows_and_cols - 1] = 35
                walls[0][rows_and_cols - 1] = 99
                walls[1][rows_and_cols - 1] = 99
                y = 2
                while y < rows_and_cols - 2:
                    if y != rows_and_cols // 2 - 2:
                        ground[y][rows_and_cols - 1] = 75
                        walls[y][rows_and_cols - 1] = 99
                        y += 1
                    else:
                        ground[y][rows_and_cols - 1] = 45 
                        walls[y][rows_and_cols - 1] = 99
                        ground[y + 1][rows_and_cols - 1] = choice([72,82,83,84])
                        mobs_and_objects[y + 1][rows_and_cols - 1] = 100
                        walls[y + 1][rows_and_cols - 1] = 99
                        ground[y + 2][rows_and_cols - 1] = choice([72,82,83,84])
                        walls[y + 2][rows_and_cols - 1] = 99
                        ground[y + 3][rows_and_cols - 1] = 65
                        walls[y + 3][rows_and_cols - 1] = 99
                        y += 4          
                ground[rows_and_cols - 2][rows_and_cols - 1] = 85 
                walls[rows_and_cols - 2][rows_and_cols - 1] = 99 
                ground[rows_and_cols - 1][rows_and_cols - 1] = 95
                walls[rows_and_cols - 1][rows_and_cols - 1] = 99
                
                
                # fence
                for x in range (1, rows_and_cols - 1):
                    if ground[0][x] == 22 or ground[0][x] == 23 or ground[0][x] == 24:
                        chance = randint(0,100)
                        if chance <= fence_chance_spawn:
                            decorations_down[0][x] = choice([97,98])
                    if ground[rows_and_cols - 1][x] == 92:
                        chance = randint(0,100)
                        if chance <= fence_chance_spawn:
                            decorations_up[rows_and_cols - 2][x] = choice([97,98])
                
                mobs_and_objects[rows_and_cols//2][1] = 40
                x = 0
                while x < amount_of_enemies:
                    x_cord = randint(2,rows_and_cols-3)  
                    y_cord = randint(2,rows_and_cols-3)  
                    if y_cord != rows_and_cols//2 and x_cord != 1:
                        chance_enemy_spawn = randint(0, max_enemy_chance)
                        if chance_enemy_spawn <= slime_chance_spawn:
                            enemy = 50
                        elif chance_enemy_spawn <= slime_chance_spawn + wolf_chance_spawn:
                            enemy = 60
                        elif chance_enemy_spawn <= slime_chance_spawn + wolf_chance_spawn + troll_chance_spawn:
                            enemy = 51
                        elif chance_enemy_spawn <= slime_chance_spawn + wolf_chance_spawn + troll_chance_spawn + goblin_chance_spawn:
                            enemy = 52
                        else:
                            enemy = 50
                        mobs_and_objects[y_cord][x_cord] = enemy
                        walls[y_cord][x_cord] = -1
                        if decorations_down[y_cord][x_cord] != 90:
                            decorations_down[y_cord][x_cord] = -1
                        else:
                            decorations_down[y_cord][x_cord] = -1
                            decorations_up[y_cord-1][x_cord] = -1
                            decorations_up[y_cord-2][x_cord] = -1            
                        x += 1
                                  
            elif choose_kind_of_room == 1:
                # ground
                amount_of_enemies = randint(4 * world_level, 8* world_level)
                rows_and_cols = 20
                ground = [[-1 for _ in range(rows_and_cols)] for _ in range(rows_and_cols)]
                walls = [[-1 for _ in range(rows_and_cols)] for _ in range(rows_and_cols)]
                decorations_down = [[-1 for _ in range(rows_and_cols)] for _ in range(rows_and_cols)]
                decorations_up = [[-1 for _ in range(rows_and_cols)] for _ in range(rows_and_cols)]
                mobs_and_objects = [[-1 for _ in range(rows_and_cols)] for _ in range(rows_and_cols)]
                
                # first row
                ground[0][1] = 22
                walls[0][1] = 99
                for x in range (2, rows_and_cols - 2):
                    ground[0][x] = 23
                    walls[0][x] = 99
                ground[0][rows_and_cols - 2] = 24
                walls[0][rows_and_cols - 2] = 99
                
                chance_for_grass_map = randint (0,100)
                if chance_for_grass_map <= grass_map_chance:
                    grass_map = True
                # fill middle
                for x in range (1, rows_and_cols - 1):
                    for y in range (1, rows_and_cols - 1):
                        ground [y][x] = choice([72,82,83,84])
                        # decorations random
                        if not grass_map: 
                            chance = randint(0,100)
                            if chance <= decorations_chance_spawn:
                                if y != rows_and_cols // 2 and y != rows_and_cols//2 - 1:
                                    if x != rows_and_cols // 2 and x != rows_and_cols//2 - 1:
                                        choose_decoration = choice([2,3,10,11,12,13,21,25,90,96])
                                        if choose_decoration != 90:
                                            decorations_down[y][x] = choose_decoration
                                            if choose_decoration != 21 and choose_decoration != 25:
                                                walls[y][x] = 99
                                        else:
                                            if y>1:
                                                decorations_down[y][x] = choose_decoration
                                                walls[y][x] = 99
                                                decorations_up[y-1][x] = 80
                                                decorations_up[y-2][x] = 70        
                        else:
                            decorations_up[y][x] = 20
                                
                # first col
                ground[1][0] = 31
                walls[0][0] = 99
                walls[1][0] = 99
                y = 2
                while y < rows_and_cols - 2:
                    if y != rows_and_cols // 2 - 2:
                        ground[y][0] = 71
                        walls[y][0] = 99
                        y += 1
                    else:
                        ground[y][0] = 41 
                        walls[y][0] = 99
                        ground[y + 1][0] = choice([72,82,83,84])
                        mobs_and_objects[y + 1][0] = 101
                        walls[y + 1][0] = 99
                        ground[y + 2][0] = choice([72,82,83,84])
                        walls[y + 2][0] = 99
                        ground[y + 3][0] = 61
                        walls[y + 3][0] = 99
                        y += 4 
                ground[rows_and_cols - 2][0] = 81
                walls[rows_and_cols - 2][0] = 99
                ground[rows_and_cols - 1][0] = 91
                walls[rows_and_cols - 1][0] = 99
                
                # last row
                for x in range (1, rows_and_cols - 1):
                    ground[rows_and_cols - 1][x] = 92
                    walls[rows_and_cols - 1][x] = 99
                
                # last col
                
                ground[1][rows_and_cols - 1] = 35
                walls[0][rows_and_cols - 1] = 99
                walls[1][rows_and_cols - 1] = 99
                y = 2
                while y < rows_and_cols - 2:
                    if y != rows_and_cols // 2 - 2:
                        ground[y][rows_and_cols - 1] = 75
                        walls[y][rows_and_cols - 1] = 99
                        y += 1
                    else:
                        ground[y][rows_and_cols - 1] = 45 
                        walls[y][rows_and_cols - 1] = 99
                        ground[y + 1][rows_and_cols - 1] = choice([72,82,83,84])
                        mobs_and_objects[y+1][rows_and_cols - 1] = 100
                        walls[y + 1][rows_and_cols - 1] = 99
                        ground[y + 2][rows_and_cols - 1] = choice([72,82,83,84])
                        walls[y + 2][rows_and_cols - 1] = 99
                        ground[y + 3][rows_and_cols - 1] = 65
                        walls[y + 3][rows_and_cols - 1] = 99
                        y += 4          
                ground[rows_and_cols - 2][rows_and_cols - 1] = 85 
                walls[rows_and_cols - 2][rows_and_cols - 1] = 99 
                ground[rows_and_cols - 1][rows_and_cols - 1] = 95
                walls[rows_and_cols - 1][rows_and_cols - 1] = 99
                
                
                # fence
                for x in range (1, rows_and_cols - 1):
                    if ground[0][x] == 22 or ground[0][x] == 23 or ground[0][x] == 24:
                        chance = randint(0,100)
                        if chance <= fence_chance_spawn:
                            decorations_down[0][x] = choice([97,98])
                    if ground[rows_and_cols - 1][x] == 92:
                        chance = randint(0,100)
                        if chance <= fence_chance_spawn:
                            decorations_up[rows_and_cols - 2][x] = choice([97,98])
                
                mobs_and_objects[rows_and_cols//2][1] = 40
                x = 0
                while x < amount_of_enemies:
                    x_cord = randint(2,rows_and_cols-3)  
                    y_cord = randint(2,rows_and_cols-3)  
                    if y_cord != rows_and_cols//2 and x_cord != 1:
                        chance_enemy_spawn = randint(0, max_enemy_chance)
                        if chance_enemy_spawn <= slime_chance_spawn:
                            enemy = 50
                        elif chance_enemy_spawn <= slime_chance_spawn + wolf_chance_spawn:
                            enemy = 60
                        elif chance_enemy_spawn <= slime_chance_spawn + wolf_chance_spawn + troll_chance_spawn:
                            enemy = 51
                        elif chance_enemy_spawn <= slime_chance_spawn + wolf_chance_spawn + troll_chance_spawn + goblin_chance_spawn:
                            enemy = 52
                        else:
                            enemy = 50
                        mobs_and_objects[y_cord][x_cord] = enemy
                        walls[y_cord][x_cord] = -1
                        if decorations_down[y_cord][x_cord] != 90:
                            decorations_down[y_cord][x_cord] = -1
                        else:
                            decorations_down[y_cord][x_cord] = -1
                            decorations_up[y_cord-1][x_cord] = -1
                            decorations_up[y_cord-2][x_cord] = -1            
                        x += 1
            elif choose_kind_of_room == 2:
                # ground
                amount_of_enemies = randint(3 * world_level, 6* world_level)
                rows_and_cols = 20
                ground = [[-1 for _ in range(rows_and_cols)] for _ in range(rows_and_cols)]
                walls = [[-1 for _ in range(rows_and_cols)] for _ in range(rows_and_cols)]
                decorations_down = [[-1 for _ in range(rows_and_cols)] for _ in range(rows_and_cols)]
                decorations_up = [[-1 for _ in range(rows_and_cols)] for _ in range(rows_and_cols)]
                mobs_and_objects = [[-1 for _ in range(rows_and_cols)] for _ in range(rows_and_cols)]
                
                # first row
                ground[0][6] = 22
                walls[0][6] = 99
                for x in range (7, rows_and_cols - 7):
                    ground[0][x] = 23
                    walls[0][x] = 99
                ground[0][rows_and_cols - 7] = 24
                walls[0][rows_and_cols - 7] = 99
                
                chance_for_grass_map = randint (0,100)
                if chance_for_grass_map <= grass_map_chance:
                    grass_map = True
                # fill middle
                for x in range (6, rows_and_cols - 6):
                    for y in range (1, rows_and_cols - 1):
                        ground [y][x] = choice([72,82,83,84])
                        # decorations random
                        if not grass_map: 
                            chance = randint(0,100)
                            if chance <= decorations_chance_spawn:
                                if y != rows_and_cols // 2 and y != rows_and_cols//2 - 1:
                                    if x != rows_and_cols // 2 and x != rows_and_cols//2 - 1:
                                        choose_decoration = choice([2,3,10,11,12,13,21,25,90,96])
                                        if choose_decoration != 90:
                                            decorations_down[y][x] = choose_decoration
                                            if choose_decoration != 21 and choose_decoration != 25:
                                                walls[y][x] = 99
                                        else:
                                            if y>1:
                                                decorations_down[y][x] = choose_decoration
                                                walls[y][x] = 99
                                                decorations_up[y-1][x] = 80
                                                decorations_up[y-2][x] = 70        
                        else:
                            decorations_up[y][x] = 20
                                
                # first col
                ground[1][5] = 31
                walls[0][5] = 99
                walls[1][5] = 99
                y = 2
                while y < rows_and_cols - 2:
                    if y != rows_and_cols // 2 - 2:
                        ground[y][5] = 71
                        walls[y][5] = 99
                        y += 1
                    else:
                        ground[y][5] = 41 
                        walls[y][5] = 99
                        ground[y + 1][5] = choice([72,82,83,84])
                        walls[y][5] = 99
                        ground[y + 1][4] = choice([72,82,83,84])
                        ground[y][4] = 23
                        walls[y][4] = 99
                        ground[y + 1][3] = choice([72,82,83,84])
                        ground[y][3] = 23
                        walls[y][3] = 99
                        ground[y + 1][2] = choice([72,82,83,84])
                        ground[y][2] = 23
                        walls[y][2] = 99
                        ground[y + 1][1] = choice([72,82,83,84])
                        ground[y][1] = 23
                        walls[y][1] = 99
                        ground[y + 1][0] = choice([72,82,83,84])
                        ground[y][0] = 23
                        mobs_and_objects[y + 1][0] = 101
                        walls[y + 1][0] = 99
                        ground[y + 2][5] = choice([72,82,83,84])
                        ground[y + 2][4] = choice([72,82,83,84])
                        ground[y + 3][4] = 92
                        walls[y + 3][4] = 99
                        ground[y + 2][3] = choice([72,82,83,84])
                        ground[y + 3][3] = 92
                        walls[y + 3][3] = 99
                        ground[y + 2][2] = choice([72,82,83,84])
                        ground[y + 3][2] = 92
                        walls[y + 3][2] = 99
                        ground[y + 2][1] = choice([72,82,83,84])
                        ground[y + 3][1] = 92
                        walls[y + 3][1] = 99
                        ground[y + 2][0] = choice([72,82,83,84])
                        ground[y + 3][0] = 92
                        walls[y + 3][0] = 99
                        walls[y + 2][0] = 99
                        ground[y + 3][5] = 61
                        walls[y + 3][5] = 99
                        y += 4 
                ground[rows_and_cols - 2][5] = 81
                walls[rows_and_cols - 2][5] = 99
                ground[rows_and_cols - 1][5] = 91
                walls[rows_and_cols - 1][5] = 99
                
                # last row
                for x in range (6, rows_and_cols - 6):
                    ground[rows_and_cols - 1][x] = 92
                    walls[rows_and_cols - 1][x] = 99
                
                # last col
                ground[1][rows_and_cols - 6] = 35
                walls[0][rows_and_cols - 1] = 99
                walls[1][rows_and_cols - 1] = 99
                y = 2
                while y < rows_and_cols - 2:
                    if y != rows_and_cols // 2 - 2:
                        ground[y][rows_and_cols - 6] = 75
                        walls[y][rows_and_cols - 6] = 99
                        y += 1
                    else:
                        ground[y][rows_and_cols - 6] = 45 
                        walls[y][rows_and_cols - 6] = 99
                        ground[y + 1][rows_and_cols - 6] = choice([72,82,83,84])
                        ground[y + 1][rows_and_cols - 5] = choice([72,82,83,84])
                        ground[y][rows_and_cols - 5] = 23
                        walls[y][rows_and_cols - 5] = 99
                        walls[1][rows_and_cols - 6] = 99
                        ground[y + 1][rows_and_cols - 4] = choice([72,82,83,84])
                        ground[y][rows_and_cols - 4] = 23
                        walls[y][rows_and_cols - 4] = 99
                        ground[y + 1][rows_and_cols - 3] = choice([72,82,83,84])
                        ground[y][rows_and_cols - 3] = 23
                        walls[y][rows_and_cols - 3] = 99
                        ground[y + 1][rows_and_cols - 2] = choice([72,82,83,84])
                        ground[y][rows_and_cols - 2] = 23
                        walls[y][rows_and_cols - 2] = 99
                        ground[y + 1][rows_and_cols - 1] = choice([72,82,83,84])
                        ground[y][rows_and_cols - 1] = 23
                        walls[y][rows_and_cols - 1] = 99
                        mobs_and_objects[y+1][rows_and_cols - 1] = 100
                        walls[y + 1][rows_and_cols - 1] = 99
                        ground[y + 2][rows_and_cols - 6] = choice([72,82,83,84])
                        ground[y + 2][rows_and_cols - 5] = choice([72,82,83,84])
                        ground[y + 3][rows_and_cols - 5] = 92
                        walls[y + 3][rows_and_cols - 5] = 99
                        ground[y + 2][rows_and_cols - 4] = choice([72,82,83,84])
                        ground[y + 3][rows_and_cols - 4] = 92
                        walls[y + 3][rows_and_cols - 4] = 99
                        ground[y + 2][rows_and_cols - 3] = choice([72,82,83,84])
                        ground[y + 3][rows_and_cols - 3] = 92
                        walls[y + 3][rows_and_cols - 3] = 99
                        ground[y + 2][rows_and_cols - 2] = choice([72,82,83,84])
                        ground[y + 3][rows_and_cols - 2] = 92
                        walls[y + 3][rows_and_cols - 2] = 99
                        ground[y + 2][rows_and_cols - 1] = choice([72,82,83,84])
                        ground[y + 3][rows_and_cols - 1] = 92
                        walls[y + 3][rows_and_cols - 1] = 99
                        walls[y + 2][rows_and_cols - 1] = 99
                        ground[y + 3][rows_and_cols - 6] = 65
                        walls[y + 3][rows_and_cols - 6] = 99
                        y += 4          
                ground[rows_and_cols - 2][rows_and_cols - 6] = 85 
                walls[rows_and_cols - 2][rows_and_cols - 6] = 99 
                ground[rows_and_cols - 1][rows_and_cols - 6] = 95
                walls[rows_and_cols - 1][rows_and_cols - 6] = 99
                
                
                # fence
                for x in range (6, rows_and_cols - 6):
                    if ground[0][x] == 22 or ground[0][x] == 23 or ground[0][x] == 24:
                        chance = randint(0,100)
                        if chance <= fence_chance_spawn:
                            decorations_down[0][x] = choice([97,98])
                    if ground[rows_and_cols - 1][x] == 92:
                        chance = randint(0,100)
                        if chance <= fence_chance_spawn:
                            decorations_up[rows_and_cols - 2][x] = choice([97,98])
                
                mobs_and_objects[rows_and_cols//2][1] = 40
                x = 0
                while x < amount_of_enemies:
                    x_cord = randint(7,rows_and_cols-7)  
                    y_cord = randint(2,rows_and_cols-3)  
                    if y_cord != rows_and_cols//2 and x_cord != 1:
                        chance_enemy_spawn = randint(0, max_enemy_chance)
                        if chance_enemy_spawn <= slime_chance_spawn:
                            enemy = 50
                        elif chance_enemy_spawn <= slime_chance_spawn + wolf_chance_spawn:
                            enemy = 60
                        elif chance_enemy_spawn <= slime_chance_spawn + wolf_chance_spawn + troll_chance_spawn:
                            enemy = 51
                        elif chance_enemy_spawn <= slime_chance_spawn + wolf_chance_spawn + troll_chance_spawn + goblin_chance_spawn:
                            enemy = 52
                        else:
                            enemy = 50
                        mobs_and_objects[y_cord][x_cord] = enemy
                        walls[y_cord][x_cord] = -1
                        if decorations_down[y_cord][x_cord] != 90:
                            decorations_down[y_cord][x_cord] = -1
                        else:
                            decorations_down[y_cord][x_cord] = -1
                            decorations_up[y_cord-1][x_cord] = -1
                            decorations_up[y_cord-2][x_cord] = -1            
                        x += 1
                        
            else:
                # ground
                amount_of_enemies = randint(3 * world_level, 6* world_level)
                rows_and_cols = 20
                ground = [[-1 for _ in range(rows_and_cols)] for _ in range(rows_and_cols)]
                walls = [[-1 for _ in range(rows_and_cols)] for _ in range(rows_and_cols)]
                decorations_down = [[-1 for _ in range(rows_and_cols)] for _ in range(rows_and_cols)]
                decorations_up = [[-1 for _ in range(rows_and_cols)] for _ in range(rows_and_cols)]
                mobs_and_objects = [[-1 for _ in range(rows_and_cols)] for _ in range(rows_and_cols)]
                
                # first row
                for x in range (2, rows_and_cols - 2):
                    ground[5][x] = 23
                    walls[5][x] = 99
                ground[5][rows_and_cols -2] = 24
                walls[5][rows_and_cols -2] = 99
                walls[5][6] == 99
                chance_for_grass_map = randint (0,100)
                if chance_for_grass_map <= grass_map_chance:
                    grass_map = True
                ground[5][1] = 22
                walls[5][1] = 99
                # fill middle
                for x in range (1, rows_and_cols - 1):
                    for y in range (6, rows_and_cols - 6):
                        ground [y][x] = choice([72,82,83,84])
                        # decorations random
                        if not grass_map: 
                            chance = randint(0,100)
                            if chance <= decorations_chance_spawn:
                                if y != rows_and_cols // 2 and y != rows_and_cols//2 - 1:
                                    if x != rows_and_cols // 2 and x != rows_and_cols//2 - 1:
                                        choose_decoration = choice([2,3,10,11,12,13,21,25,90,96])
                                        if choose_decoration != 90:
                                            decorations_down[y][x] = choose_decoration
                                            if choose_decoration != 21 and choose_decoration != 25:
                                                walls[y][x] = 99
                                        else:
                                            if y>1:
                                                decorations_down[y][x] = choose_decoration
                                                walls[y][x] = 99
                                                decorations_up[y-1][x] = 80
                                                decorations_up[y-2][x] = 70        
                        else:
                            decorations_up[y][x] = 20
                                
                # first col
                ground[6][0] = 31
                walls[5][0] = 99
                walls[6][0] = 99
                y = 7
                while y < rows_and_cols - 7:
                    if y != rows_and_cols // 2 - 2:
                        ground[y][0] = 71
                        walls[y][0] = 99
                        y += 1
                    else:
                        ground[y][0] = 41 
                        walls[y][0] = 99
                        ground[y + 1][0] = choice([72,82,83,84])
                        mobs_and_objects[y+1][0] = 101
                        walls[y + 1][0] = 99
                        ground[y + 2][0] = choice([72,82,83,84])
                        walls[y + 2][0] = 99
                        ground[y + 3][0] = 61
                        walls[y + 3][0] = 99
                        y += 4              
                ground[rows_and_cols - 7][0] = 81 
                walls[rows_and_cols - 7][0] = 99 
                ground[rows_and_cols - 6][0] = 91
                walls[rows_and_cols - 6][0] = 99
                
                # last row
                for x in range (1, rows_and_cols - 1):
                    ground[rows_and_cols - 6][x] = 92
                    walls[rows_and_cols - 6][x] = 99
                
                # last col
                ground[6][rows_and_cols - 1] = 35
                walls[5][rows_and_cols - 1] = 99
                walls[6][rows_and_cols - 1] = 99
                y = 7
                while y < rows_and_cols - 7:
                    if y != rows_and_cols // 2 - 2:
                        ground[y][rows_and_cols - 1] = 75
                        walls[y][rows_and_cols - 1] = 99
                        y += 1
                    else:
                        ground[y][rows_and_cols - 1] = 45 
                        walls[y][rows_and_cols - 1] = 99
                        ground[y + 1][rows_and_cols - 1] = choice([72,82,83,84])
                        mobs_and_objects[y+1][rows_and_cols - 1] = 100
                        walls[y + 1][rows_and_cols - 1] = 99
                        ground[y + 2][rows_and_cols - 1] = choice([72,82,83,84])
                        walls[y + 2][rows_and_cols - 1] = 99
                        ground[y + 3][rows_and_cols - 1] = 65
                        walls[y + 3][rows_and_cols - 1] = 99
                        y += 4              
                ground[rows_and_cols - 7][rows_and_cols - 1] = 85 
                walls[rows_and_cols - 7][rows_and_cols - 1] = 99 
                ground[rows_and_cols - 6][rows_and_cols - 1] = 95
                walls[rows_and_cols - 6][rows_and_cols - 1] = 99
                
                
                # fence
                for x in range (6, rows_and_cols - 6):
                    if ground[0][x] == 22 or ground[0][x] == 23 or ground[0][x] == 24:
                        chance = randint(0,100)
                        if chance <= fence_chance_spawn:
                            decorations_down[0][x] = choice([97,98])
                    if ground[rows_and_cols - 1][x] == 92:
                        chance = randint(0,100)
                        if chance <= fence_chance_spawn:
                            decorations_up[rows_and_cols - 2][x] = choice([97,98])
                
                mobs_and_objects[rows_and_cols//2][1] = 40
                x = 0
                while x < amount_of_enemies:
                    x_cord = randint(2,rows_and_cols-3)  
                    y_cord = randint(7,rows_and_cols-7)  
                    if y_cord != rows_and_cols//2 and x_cord != 1:
                        chance_enemy_spawn = randint(0, max_enemy_chance)
                        if chance_enemy_spawn <= slime_chance_spawn:
                            enemy = 50
                        elif chance_enemy_spawn <= slime_chance_spawn + wolf_chance_spawn:
                            enemy = 60
                        elif chance_enemy_spawn <= slime_chance_spawn + wolf_chance_spawn + troll_chance_spawn:
                            enemy = 51
                        elif chance_enemy_spawn <= slime_chance_spawn + wolf_chance_spawn + troll_chance_spawn + goblin_chance_spawn:
                            enemy = 52
                        else:
                            enemy = 50
                        mobs_and_objects[y_cord][x_cord] = enemy
                        walls[y_cord][x_cord] = -1
                        if decorations_down[y_cord][x_cord] != 90:
                            decorations_down[y_cord][x_cord] = -1
                        else:
                            decorations_down[y_cord][x_cord] = -1
                            decorations_up[y_cord-1][x_cord] = -1
                            decorations_up[y_cord-2][x_cord] = -1            
                        x += 1
        else:
            # ground
            rows_and_cols = 20
            ground = [[-1 for _ in range(rows_and_cols)] for _ in range(rows_and_cols)]
            walls = [[-1 for _ in range(rows_and_cols)] for _ in range(rows_and_cols)]
            decorations_down = [[-1 for _ in range(rows_and_cols)] for _ in range(rows_and_cols)]
            decorations_up = [[-1 for _ in range(rows_and_cols)] for _ in range(rows_and_cols)]
            mobs_and_objects = [[-1 for _ in range(rows_and_cols)] for _ in range(rows_and_cols)]
                
            # first row
            ground[0][1] = 22
            walls[0][1] = 99
            for x in range (2, rows_and_cols - 2):
                ground[0][x] = 23
                walls[0][x] = 99
            ground[0][rows_and_cols - 2] = 24
            walls[0][rows_and_cols - 2] = 99
                
            chance_for_grass_map = randint (0,100)
            if chance_for_grass_map <= grass_map_chance:
                grass_map = True
            # fill middle
            for x in range (1, rows_and_cols - 1):
                for y in range (1, rows_and_cols - 1):
                    ground [y][x] = choice([72,82,83,84])
                    # decorations random
                    if not grass_map: 
                        chance = randint(0,100)
                        if chance <= decorations_chance_spawn:
                            if y != rows_and_cols // 2 and y != rows_and_cols//2 - 1:
                                if x != rows_and_cols // 2 and x != rows_and_cols//2 - 1:
                                    choose_decoration = choice([2,3,10,11,12,13,21,25,90,96])
                                    if choose_decoration != 90:
                                        decorations_down[y][x] = choose_decoration
                                        if choose_decoration != 21 and choose_decoration != 25:
                                            walls[y][x] = 99
                                    else:
                                        if y>1:
                                            decorations_down[y][x] = choose_decoration
                                            walls[y][x] = 99
                                            decorations_up[y-1][x] = 80
                                            decorations_up[y-2][x] = 70        
                    else:
                        decorations_up[y][x] = 20
                                
            # first col
            ground[1][0] = 31
            walls[0][0] = 99
            walls[1][0] = 99
            y = 2
            while y < rows_and_cols - 2:
                if y != rows_and_cols // 2 - 2:
                    ground[y][0] = 71
                    walls[y][0] = 99
                    y += 1
                else:
                    ground[y][0] = 41 
                    walls[y][0] = 99
                    ground[y + 1][0] = choice([72,82,83,84])
                    walls[y + 1][0] = 99
                    mobs_and_objects[y + 1][0] = 101
                    ground[y + 2][0] = choice([72,82,83,84])
                    walls[y + 2][0] = 99
                    ground[y + 3][0] = 61
                    walls[y + 3][0] = 99
                    y += 4 
            ground[rows_and_cols - 2][0] = 81
            walls[rows_and_cols - 2][0] = 99
            ground[rows_and_cols - 1][0] = 91
            walls[rows_and_cols - 1][0] = 99
                
            # last row
            for x in range (1, rows_and_cols - 1):
                ground[rows_and_cols - 1][x] = 92
                walls[rows_and_cols - 1][x] = 99
                
            # last col
            ground[1][rows_and_cols - 1] = 35
            walls[0][rows_and_cols - 1] = 99
            walls[1][rows_and_cols - 1] = 99
            y = 2
            while y < rows_and_cols - 2:
                if y != rows_and_cols // 2 - 2:
                    ground[y][rows_and_cols - 1] = 75
                    walls[y][rows_and_cols - 1] = 99
                    y += 1
                else:
                    ground[y][rows_and_cols - 1] = 45 
                    walls[y][rows_and_cols - 1] = 99
                    ground[y + 1][rows_and_cols - 1] = choice([72,82,83,84])
                    walls[y + 1][rows_and_cols - 1] = 99
                    mobs_and_objects[y + 1][rows_and_cols - 1] = 100
                    ground[y + 2][rows_and_cols - 1] = choice([72,82,83,84])
                    walls[y + 2][rows_and_cols - 1] = 99
                    ground[y + 3][rows_and_cols - 1] = 65
                    walls[y + 3][rows_and_cols - 1] = 99
                    y += 4          
            ground[rows_and_cols - 2][rows_and_cols - 1] = 85 
            walls[rows_and_cols - 2][rows_and_cols - 1] = 99 
            ground[rows_and_cols - 1][rows_and_cols - 1] = 95
            walls[rows_and_cols - 1][rows_and_cols - 1] = 99
                
                
            # fence
            for x in range (1, rows_and_cols - 1):
                if ground[0][x] == 22 or ground[0][x] == 23 or ground[0][x] == 24:
                    chance = randint(0,100)
                    if chance <= fence_chance_spawn:
                        decorations_down[0][x] = choice([97,98])
                if ground[rows_and_cols - 1][x] == 92:
                    chance = randint(0,100)
                    if chance <= fence_chance_spawn:
                        decorations_up[rows_and_cols - 2][x] = choice([97,98])
                
            mobs_and_objects[rows_and_cols//2][1] = 40
            mobs_and_objects[rows_and_cols//2][rows_and_cols//2] = 0
            for x in range(-2,3):
                for y in range (-2,3):
                    if x != 0 and y != 0:
                        chance_ent_spawn = randint(0,100)
                        if chance_ent_spawn <= ent_chance_spawn:
                            mobs_and_objects[rows_and_cols//2 + y][rows_and_cols//2 + x] = 53
                            walls[rows_and_cols//2 + y][rows_and_cols//2 + x] = -1
                            decorations_down[rows_and_cols//2 + y][rows_and_cols//2 + x] = -1
                            decorations_up[rows_and_cols//2 + y - 1][rows_and_cols//2 + x] = -2
                            decorations_up[rows_and_cols//2 + y - 2][rows_and_cols//2 + x] = -2
                        
    else:
        if room == 1:
            # FIRST ROOM
            # ground
            rows_and_cols = 10
            ground = [[-1 for _ in range(rows_and_cols)] for _ in range(rows_and_cols)]
            walls = [[-1 for _ in range(rows_and_cols)] for _ in range(rows_and_cols)]
            decorations_down = [[-1 for _ in range(rows_and_cols)] for _ in range(rows_and_cols)]
            decorations_up = [[-1 for _ in range(rows_and_cols)] for _ in range(rows_and_cols)]
            mobs_and_objects = [[-1 for _ in range(rows_and_cols)] for _ in range(rows_and_cols)]
            
            # first row
            ground[0][1] = 22
            walls[0][1] = 99
            for x in range (2, rows_and_cols - 2):
                ground[0][x] = 23
                walls[0][x] = 99
            ground[0][rows_and_cols - 2] = 24
            walls[0][rows_and_cols - 2] = 99
            
            chance_for_grass_map = randint (0,100)
            if chance_for_grass_map <= grass_map_chance:
                grass_map = True
            # fill middle
            for x in range (1, rows_and_cols - 1):
                for y in range (1, rows_and_cols - 1):
                    ground [y][x] = choice([72,82,83,84])
                    # decorations random
                    if not grass_map: 
                        chance = randint(0,100)
                        if chance <= decorations_chance_spawn:
                            if y != rows_and_cols // 2 and y != rows_and_cols//2 - 1:
                                if x != rows_and_cols // 2 and x != rows_and_cols//2 - 1:
                                    choose_decoration = choice([2,3,10,11,12,13,21,25,90,96])
                                    if choose_decoration != 90:
                                        decorations_down[y][x] = choose_decoration
                                        if choose_decoration != 21 and choose_decoration != 25:
                                            walls[y][x] = 99
                                    else:
                                        if y>1:
                                            decorations_down[y][x] = choose_decoration
                                            walls[y][x] = 99
                                            decorations_up[y-1][x] = 80
                                            decorations_up[y-2][x] = 70        
                    else:
                        decorations_up[y][x] = 20
                            
            # first col
            ground[1][0] = 31
            walls[0][0] = 99
            walls[1][0] = 99
            for y in range (2, rows_and_cols - 2):
                ground[y][0] = 71
                walls[y][0] = 99
            ground[rows_and_cols - 2][0] = 81
            walls[rows_and_cols - 2][0] = 99
            ground[rows_and_cols - 1][0] = 91
            walls[rows_and_cols - 1][0] = 99
            
            # last row
            for x in range (1, rows_and_cols - 1):
                ground[rows_and_cols - 1][x] = 92
                walls[rows_and_cols - 1][x] = 99
            
            # last col
            ground[1][rows_and_cols - 1] = 35
            walls[0][rows_and_cols - 1] = 99
            walls[1][rows_and_cols - 1] = 99
            y = 2
            while y < rows_and_cols - 2:
                if y != rows_and_cols // 2 - 2:
                    ground[y][rows_and_cols - 1] = 75
                    walls[y][rows_and_cols - 1] = 99
                    y += 1
                else:
                    ground[y][rows_and_cols - 1] = 45 
                    walls[y][rows_and_cols - 1] = 99
                    ground[y + 1][rows_and_cols - 1] = choice([72,82,83,84])
                    mobs_and_objects[y+1][rows_and_cols - 1] = 100
                    walls[y + 1][rows_and_cols - 1] = 99
                    ground[y + 2][rows_and_cols - 1] = choice([72,82,83,84])
                    walls[y + 2][rows_and_cols - 1] = 91
                    ground[y + 3][rows_and_cols - 1] = 65
                    walls[y + 3][rows_and_cols - 1] = 99
                    y += 4          
            ground[rows_and_cols - 2][rows_and_cols - 1] = 85 
            walls[rows_and_cols - 2][rows_and_cols - 1] = 99 
            ground[rows_and_cols - 1][rows_and_cols - 1] = 95
            walls[rows_and_cols - 1][rows_and_cols - 1] = 99
            
            
            # fence
            for x in range (1, rows_and_cols - 1):
                if ground[0][x] == 22 or ground[0][x] == 23 or ground[0][x] == 24:
                    chance = randint(0,100)
                    if chance <= fence_chance_spawn:
                        decorations_down[0][x] = choice([97,98])
                if ground[rows_and_cols - 1][x] == 92:
                    chance = randint(0,100)
                    if chance <= fence_chance_spawn:
                        decorations_up[rows_and_cols - 2][x] = choice([97,98])
            
            mobs_and_objects[rows_and_cols//2][rows_and_cols//2] = 40
        
        else:
            # ground
            rows_and_cols = 20
            ground = [[-1 for _ in range(rows_and_cols)] for _ in range(rows_and_cols)]
            walls = [[-1 for _ in range(rows_and_cols)] for _ in range(rows_and_cols)]
            decorations_down = [[-1 for _ in range(rows_and_cols)] for _ in range(rows_and_cols)]
            decorations_up = [[-1 for _ in range(rows_and_cols)] for _ in range(rows_and_cols)]
            mobs_and_objects = [[-1 for _ in range(rows_and_cols)] for _ in range(rows_and_cols)]
                
            # first row
            ground[0][1] = 22
            walls[0][1] = 99
            for x in range (2, rows_and_cols - 2):
                ground[0][x] = 23
                walls[0][x] = 99
            ground[0][rows_and_cols - 2] = 24
            walls[0][rows_and_cols - 2] = 99
                
            chance_for_grass_map = randint (0,100)
            if chance_for_grass_map <= grass_map_chance:
                grass_map = True
             # fill middle
            for x in range (1, rows_and_cols - 1):
                for y in range (1, rows_and_cols - 1):
                    ground [y][x] = choice([72,82,83,84])
                    # decorations random
                    if not grass_map: 
                        pass       
                    else:
                        decorations_up[y][x] = 20
                                
            # first col
            ground[1][0] = 31
            walls[0][0] = 99
            walls[1][0] = 99
            y = 2
            while y < rows_and_cols - 2:
                if y != rows_and_cols // 2 - 2:
                    ground[y][0] = 71
                    walls[y][0] = 99
                    y += 1
                else:
                    ground[y][0] = 41 
                    walls[y][0] = 99
                    ground[y + 1][0] = choice([72,82,83,84])
                    walls[y + 1][0] = 99
                    mobs_and_objects[y + 1][0] = 101
                    ground[y + 2][0] = choice([72,82,83,84])
                    walls[y + 2][0] = 99
                    ground[y + 3][0] = 61
                    walls[y + 3][0] = 99
                    y += 4 
            ground[rows_and_cols - 2][0] = 81
            walls[rows_and_cols - 2][0] = 99
            ground[rows_and_cols - 1][0] = 91
            walls[rows_and_cols - 1][0] = 99
                
            # last row
            for x in range (1, rows_and_cols - 1):
                ground[rows_and_cols - 1][x] = 92
                walls[rows_and_cols - 1][x] = 99
                
            # last col
            ground[1][rows_and_cols - 1] = 35
            walls[0][rows_and_cols - 1] = 99
            walls[1][rows_and_cols - 1] = 99
            y = 2
            while y < rows_and_cols - 2:
                ground[y][rows_and_cols - 1] = 75
                walls[y][rows_and_cols - 1] = 99
                y += 1        
            ground[rows_and_cols - 2][rows_and_cols - 1] = 85 
            walls[rows_and_cols - 2][rows_and_cols - 1] = 99 
            ground[rows_and_cols - 1][rows_and_cols - 1] = 95
            walls[rows_and_cols - 1][rows_and_cols - 1] = 99
                 
            # fence
            for x in range (1, rows_and_cols - 1):
                if ground[0][x] == 22 or ground[0][x] == 23 or ground[0][x] == 24:
                    chance = randint(0,100)
                    if chance <= fence_chance_spawn:
                        decorations_down[0][x] = choice([97,98])
                if ground[rows_and_cols - 1][x] == 92:
                    chance = randint(0,100)
                    if chance <= fence_chance_spawn:
                        decorations_up[rows_and_cols - 2][x] = choice([97,98])
            
            # hero    
            mobs_and_objects[rows_and_cols//2][1] = 40
            # fire_slime   
            mobs_and_objects[rows_and_cols//2][rows_and_cols//2] = 54
            # slimes
            mobs_and_objects[rows_and_cols//2 - 2][rows_and_cols//2 - 2] = 50
            mobs_and_objects[rows_and_cols//2 - 2][rows_and_cols//2 ] = 50
            mobs_and_objects[rows_and_cols//2 - 2][rows_and_cols//2 + 2] = 50
            mobs_and_objects[rows_and_cols//2][rows_and_cols//2 - 2] = 50
            mobs_and_objects[rows_and_cols//2][rows_and_cols//2 + 2] = 50
            mobs_and_objects[rows_and_cols//2 + 2][rows_and_cols//2 - 2] = 50
            mobs_and_objects[rows_and_cols//2 + 2][rows_and_cols//2] = 50
            mobs_and_objects[rows_and_cols//2 + 2][rows_and_cols//2 + 2] = 50
            # portal
            mobs_and_objects[rows_and_cols//2 + 2][rows_and_cols - 3] = 30
    
    return ground, walls, decorations_down, decorations_up, mobs_and_objects
        

def generate(world_level = 0):
    tasks = []
    levels = []
    range_of_rooms = (10,15)
    rooms_to_go = randint(range_of_rooms[0],range_of_rooms[1]) # tupla
    
        
    if world_level < 12:
        for x in range (1, rooms_to_go + 1):
            tasks.append([x, rooms_to_go])            
                    
                        
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(generating_grassland, *task) for task in tasks]
                    
            for future in futures:
                ground, walls, decorations_down, decorations_up, mobs_and_objects = future.result()
                levels.append([ground, walls, decorations_down, decorations_up, mobs_and_objects])
        
    return levels, rooms_to_go        


def reset_prev_mobs(levels, room):
    if room == 0:
        return levels
    levels[room - 1][4]
    for x in range(0, len(levels[room-1][4])):
        for y in range(0, len(levels[room-1][4])):
            levels[room - 1][4][y][x] = -1
        
    levels[room - 1][4][len(levels[room-1][4])//2][len(levels[room-1][4]) - 2] = 40
    levels[room - 1][4][len(levels[room-1][4])//2][len(levels[room-1][4]) - 1] = 100
    levels[room - 1][4][len(levels[room-1][4])//2][0] = 101
    return levels
    
    