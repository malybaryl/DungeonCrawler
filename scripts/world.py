import pygame
import scripts.character
import scripts.constants
import scripts.enemies
from scripts.load import loadImages
from scripts.character import Peasant, Wizard, Dwarf, Knight, Pikemen, Elf, Paladin, Druid
from scripts.enemies import Slime, Wolf, Troll, Goblin, Ent, SlimeFireWizard, Druid, Imp
from scripts.objects import Chest, NextRoomEnterence, PreviousRoomEnterence, FireUpPlayer
from scripts.world_process_funcs import process_1_ground_csv, process_2_decoration_dows_csv, process_3_decorations_up_csv, process_4_walls_csv, process_5_mobs_and_objects_csv, process_6_ground2_csv
from random import randint
from concurrent.futures import ThreadPoolExecutor

def draw_grid(display):
        for x in range(30):
            pygame.draw.line(display, scripts.constants.WHITE, (x*scripts.constants.TILE_SIZE,0), (x*scripts.constants.TILE_SIZE, scripts.constants.SCREEN_HEIGHT))
            pygame.draw.line(display, scripts.constants.WHITE, (0,x*scripts.constants.TILE_SIZE), (scripts.constants.SCREEN_WIDTH, x*scripts.constants.TILE_SIZE))
            

class World():
    def __init__(self):
        self.assets={
            "grassland": loadImages("tilemap/grassland"),
            'lavaland': loadImages("tilemap/lavaland")
        }
        self.map_tiles = []
        self.map_tiles2 = []
        self.obstacle_tile = []
        self.decorations_up_tiles = []
        self.decorations_down_tiles = []
        self.player = None
        self.character_list = []
        self.gate_tiles = []
        self.objects = []
        
        self.world_data = []
        self.world_data2 = []
        self.world_mobs_and_objects_data = []
        self.world_decoration_down_data = []
        self.world_decoration_up_data = []
        self.walls = []
        
        self.world_level = 1
        

    def proced_csv_file(self, rows=50, cols=50, world_level = 1):
        self.world_level = world_level
        if world_level < 4:
            if world_level % 3 == 0:
                choice = 3
            else:
                choice = randint(0,0)
        else:
            choice = randint(4,4)
            
        if choice == 0:
            level = '001'
            tasks = []
            
            tasks.append((process_1_ground_csv, "grassland", cols, rows, level))
            tasks.append((process_2_decoration_dows_csv, "grassland", cols, rows, level))
            tasks.append((process_3_decorations_up_csv, "grassland", cols, rows, level))
            tasks.append((process_4_walls_csv, "grassland", cols, rows, level))
            tasks.append((process_5_mobs_and_objects_csv, "grassland", cols, rows, level))
            
            with ThreadPoolExecutor() as executor:
                futures = [executor.submit(task[0], task[1], task[2], task[3], task[4]) for task in tasks]
    
            results = [future.result() for future in futures]
    
            self.world_data = results[0]
            self.world_decoration_down_data = results[1]
            self.world_decoration_up_data = results[2]
            self.walls = results[3]
            self.world_mobs_and_objects_data = results[4]
        
        if choice == 3:
            level = 'druid'
            tasks = []
            
            tasks.append((process_1_ground_csv, "grassland", cols, rows, level))
            tasks.append((process_2_decoration_dows_csv, "grassland", cols, rows, level))
            tasks.append((process_3_decorations_up_csv, "grassland", cols, rows, level))
            tasks.append((process_4_walls_csv, "grassland", cols, rows, level))
            tasks.append((process_5_mobs_and_objects_csv, "grassland", cols, rows, level))
            
            with ThreadPoolExecutor() as executor:
                futures = [executor.submit(task[0], task[1], task[2], task[3], task[4]) for task in tasks]
    
            results = [future.result() for future in futures]
    
            self.world_data = results[0]
            self.world_decoration_down_data = results[1]
            self.world_decoration_up_data = results[2]
            self.walls = results[3]
            self.world_mobs_and_objects_data = results[4]
        
        elif choice == 4:
            level = '004'
            tasks = []
            
            tasks.append((process_1_ground_csv, "lavaland", cols, rows, level))
            tasks.append((process_2_decoration_dows_csv, "lavaland", cols, rows, level))
            tasks.append((process_3_decorations_up_csv, "lavaland", cols, rows, level))
            tasks.append((process_4_walls_csv, "lavaland", cols, rows, level))
            tasks.append((process_5_mobs_and_objects_csv, "lavaland", cols, rows, level))
            tasks.append((process_6_ground2_csv, 'lavaland', cols, rows, level))
            
            with ThreadPoolExecutor() as executor:
                futures = [executor.submit(task[0], task[1], task[2], task[3], task[4]) for task in tasks]
    
            results = [future.result() for future in futures]
    
            self.world_data = results[0]
            self.world_decoration_down_data = results[1]
            self.world_decoration_up_data = results[2]
            self.walls = results[3]
            self.world_mobs_and_objects_data = results[4]
        
        
    
    def process_date(self, data, type, switch):
        self.level_lenght = len(data)
        # iterate throught each value in level data file
        
        # walls tiles
        if switch == 0:
            if type == 'grassland':
                for y, row in enumerate(data):
                    for x, tile in enumerate(row):
                        if tile >= 0:
                            # wall tile
                            if tile == 99:
                                image = self.assets[type][0]
                                image_rect = image.get_rect()
                                image_x = x * scripts.constants.TILE_SIZE 
                                image_y = y * scripts.constants.TILE_SIZE 
                                image_rect.x= image_x
                                image_rect.y= image_y       
                                tile_data = [image, image_rect, image_x, image_y]
                                self.obstacle_tile.append(tile_data) 
            elif type == 'lavaland':
                for y, row in enumerate(data):
                    for x, tile in enumerate(row):
                        if tile >= 0:
                            # wall tile
                            if tile == 3:
                                image = self.assets[type][0]
                                image_rect = image.get_rect()
                                image_x = x * scripts.constants.TILE_SIZE 
                                image_y = y * scripts.constants.TILE_SIZE 
                                image_rect.x= image_x
                                image_rect.y= image_y       
                                tile_data = [image, image_rect, image_x, image_y]
                                self.obstacle_tile.append(tile_data) 
                    
        # ground tiles 1 and 2                        
        elif switch == 1 or switch == 2:
            if type == 'grassland':
                for y, row in enumerate(data):
                    for x, tile in enumerate(row):
                        if tile >= 0:
                            # ground type 1
                            if tile == 82:
                                image = self.assets[type][0]
                                image_rect = image.get_rect()
                                image_x = x * scripts.constants.TILE_SIZE 
                                image_y = y * scripts.constants.TILE_SIZE 
                                image_rect.x= image_x
                                image_rect.y= image_y       
                                tile_data = [image, image_rect, image_x, image_y]
                                if switch == 1:
                                    self.map_tiles.append(tile_data)
                                else:
                                    self.map_tiles2.append(tile_data)        
                            # ground type 2
                            elif tile == 83:
                                image = self.assets[type][1]
                                image_rect = image.get_rect()
                                image_x = x * scripts.constants.TILE_SIZE 
                                image_y = y * scripts.constants.TILE_SIZE 
                                image_rect.x= image_x
                                image_rect.y= image_y       
                                tile_data = [image, image_rect, image_x, image_y]
                                if switch == 1:
                                    self.map_tiles.append(tile_data)
                                else:
                                    self.map_tiles2.append(tile_data)
                            # ground type 3
                            elif tile == 84:
                                image = self.assets[type][2]
                                image_rect = image.get_rect()
                                image_x = x * scripts.constants.TILE_SIZE 
                                image_y = y * scripts.constants.TILE_SIZE 
                                image_rect.x= image_x
                                image_rect.y= image_y       
                                tile_data = [image, image_rect, image_x, image_y]
                                if switch == 1:
                                    self.map_tiles.append(tile_data)
                                else:
                                    self.map_tiles2.append(tile_data)
                            # ground type 4
                            elif tile == 72:
                                image = self.assets[type][3]
                                image_rect = image.get_rect()
                                image_x = x * scripts.constants.TILE_SIZE 
                                image_y = y * scripts.constants.TILE_SIZE 
                                image_rect.x= image_x
                                image_rect.y= image_y       
                                tile_data = [image, image_rect, image_x, image_y]
                                if switch == 1:
                                    self.map_tiles.append(tile_data)
                                else:
                                    self.map_tiles2.append(tile_data)
                            # connect top left
                            elif tile == 73:
                                image = self.assets[type][4]
                                image_rect = image.get_rect()
                                image_x = x * scripts.constants.TILE_SIZE 
                                image_y = y * scripts.constants.TILE_SIZE 
                                image_rect.x= image_x
                                image_rect.y= image_y       
                                tile_data = [image, image_rect, image_x, image_y]
                                if switch == 1:
                                    self.map_tiles.append(tile_data)
                                else:
                                    self.map_tiles2.append(tile_data)
                            # connect top right    
                            elif tile == 74:
                                image = self.assets[type][5]
                                image_rect = image.get_rect()
                                image_x = x * scripts.constants.TILE_SIZE 
                                image_y = y * scripts.constants.TILE_SIZE 
                                image_rect.x= image_x
                                image_rect.y= image_y       
                                tile_data = [image, image_rect, image_x, image_y]
                                if switch == 1:
                                    self.map_tiles.append(tile_data)
                                else:
                                    self.map_tiles2.append(tile_data)
                            # down 
                            elif tile == 92:
                                image = self.assets[type][6]
                                image_rect = image.get_rect()
                                image_x = x * scripts.constants.TILE_SIZE 
                                image_y = y * scripts.constants.TILE_SIZE 
                                image_rect.x= image_x
                                image_rect.y= image_y       
                                tile_data = [image, image_rect, image_x, image_y]
                                if switch == 1:
                                    self.map_tiles.append(tile_data)
                                else:
                                    self.map_tiles2.append(tile_data)
                            # connect down left    
                            elif tile == 93:
                                image = self.assets[type][7]
                                image_rect = image.get_rect()
                                image_x = x * scripts.constants.TILE_SIZE 
                                image_y = y * scripts.constants.TILE_SIZE 
                                image_rect.x= image_x
                                image_rect.y= image_y       
                                tile_data = [image, image_rect, image_x, image_y]
                                if switch == 1:
                                    self.map_tiles.append(tile_data)
                                else:
                                    self.map_tiles2.append(tile_data)
                            # connect down right    
                            elif tile == 94:
                                image = self.assets[type][8]
                                image_rect = image.get_rect()
                                image_x = x * scripts.constants.TILE_SIZE 
                                image_y = y * scripts.constants.TILE_SIZE 
                                image_rect.x= image_x
                                image_rect.y= image_y       
                                tile_data = [image, image_rect, image_x, image_y]
                                if switch == 1:
                                    self.map_tiles.append(tile_data)
                                else:
                                    self.map_tiles2.append(tile_data)
                            # corner down left 1
                            elif tile == 91:
                                image = self.assets[type][9]
                                image_rect = image.get_rect()
                                image_x = x * scripts.constants.TILE_SIZE 
                                image_y = y * scripts.constants.TILE_SIZE 
                                image_rect.x= image_x
                                image_rect.y= image_y       
                                tile_data = [image, image_rect, image_x, image_y]
                                if switch == 1:
                                    self.map_tiles.append(tile_data)
                                else:
                                    self.map_tiles2.append(tile_data)
                            # corner down right 1
                            elif tile == 95:
                                image = self.assets[type][10]
                                image_rect = image.get_rect()
                                image_x = x * scripts.constants.TILE_SIZE 
                                image_y = y * scripts.constants.TILE_SIZE 
                                image_rect.x= image_x
                                image_rect.y= image_y       
                                tile_data = [image, image_rect, image_x, image_y]
                                if switch == 1:
                                    self.map_tiles.append(tile_data)
                                else:
                                    self.map_tiles2.append(tile_data)
                            # corner down left 2
                            elif tile == 81:
                                image = self.assets[type][11]
                                image_rect = image.get_rect()
                                image_x = x * scripts.constants.TILE_SIZE 
                                image_y = y * scripts.constants.TILE_SIZE 
                                image_rect.x= image_x
                                image_rect.y= image_y       
                                tile_data = [image, image_rect, image_x, image_y]
                                if switch == 1:
                                    self.map_tiles.append(tile_data)
                                else:
                                    self.map_tiles2.append(tile_data)
                            # left
                            elif tile == 71:
                                image = self.assets[type][12]
                                image_rect = image.get_rect()
                                image_x = x * scripts.constants.TILE_SIZE 
                                image_y = y * scripts.constants.TILE_SIZE 
                                image_rect.x= image_x
                                image_rect.y= image_y       
                                tile_data = [image, image_rect, image_x, image_y]
                                if switch == 1:
                                    self.map_tiles.append(tile_data)
                                else:
                                    self.map_tiles2.append(tile_data)
                            # connect left down
                            elif tile == 61:
                                image = self.assets[type][13]
                                image_rect = image.get_rect()
                                image_x = x * scripts.constants.TILE_SIZE 
                                image_y = y * scripts.constants.TILE_SIZE 
                                image_rect.x= image_x
                                image_rect.y= image_y       
                                tile_data = [image, image_rect, image_x, image_y]
                                if switch == 1:
                                    self.map_tiles.append(tile_data)
                                else:
                                    self.map_tiles2.append(tile_data)
                            # connect left top
                            elif tile == 41:
                                image = self.assets[type][14]
                                image_rect = image.get_rect()
                                image_x = x * scripts.constants.TILE_SIZE 
                                image_y = y * scripts.constants.TILE_SIZE 
                                image_rect.x= image_x
                                image_rect.y= image_y       
                                tile_data = [image, image_rect, image_x, image_y]
                                if switch == 1:
                                    self.map_tiles.append(tile_data)
                                else:
                                    self.map_tiles2.append(tile_data)
                            # corner left top
                            elif tile == 31:
                                image = self.assets[type][15]
                                image_rect = image.get_rect()
                                image_x = x * scripts.constants.TILE_SIZE 
                                image_y = y * scripts.constants.TILE_SIZE 
                                image_rect.x= image_x
                                image_rect.y= image_y       
                                tile_data = [image, image_rect, image_x, image_y]
                                if switch == 1:
                                    self.map_tiles.append(tile_data)
                                else:
                                    self.map_tiles2.append(tile_data)
                            # right
                            elif tile == 75:
                                image = self.assets[type][16]
                                image_rect = image.get_rect()
                                image_x = x * scripts.constants.TILE_SIZE 
                                image_y = y * scripts.constants.TILE_SIZE 
                                image_rect.x= image_x
                                image_rect.y= image_y       
                                tile_data = [image, image_rect, image_x, image_y]
                                if switch == 1:
                                    self.map_tiles.append(tile_data)
                                else:
                                    self.map_tiles2.append(tile_data)
                            # connect right down
                            elif tile == 65:
                                image = self.assets[type][17]
                                image_rect = image.get_rect()
                                image_x = x * scripts.constants.TILE_SIZE 
                                image_y = y * scripts.constants.TILE_SIZE 
                                image_rect.x= image_x
                                image_rect.y= image_y       
                                tile_data = [image, image_rect, image_x, image_y]
                                if switch == 1:
                                    self.map_tiles.append(tile_data)
                                else:
                                    self.map_tiles2.append(tile_data)
                            # connect right top
                            elif tile == 45:
                                image = self.assets[type][18]
                                image_rect = image.get_rect()
                                image_x = x * scripts.constants.TILE_SIZE 
                                image_y = y * scripts.constants.TILE_SIZE 
                                image_rect.x= image_x
                                image_rect.y= image_y       
                                tile_data = [image, image_rect, image_x, image_y]
                                if switch == 1:
                                    self.map_tiles.append(tile_data)
                                else:
                                    self.map_tiles2.append(tile_data)
                            # corner top right
                            elif tile == 35:
                                image = self.assets[type][19]
                                image_rect = image.get_rect()
                                image_x = x * scripts.constants.TILE_SIZE 
                                image_y = y * scripts.constants.TILE_SIZE 
                                image_rect.x= image_x
                                image_rect.y= image_y       
                                tile_data = [image, image_rect, image_x, image_y]
                                if switch == 1:
                                    self.map_tiles.append(tile_data)
                                else:
                                    self.map_tiles2.append(tile_data)
                            # top type 1
                            elif tile == 22:
                                image = self.assets[type][20]
                                image_rect = image.get_rect()
                                image_x = x * scripts.constants.TILE_SIZE 
                                image_y = y * scripts.constants.TILE_SIZE 
                                image_rect.x= image_x
                                image_rect.y= image_y       
                                tile_data = [image, image_rect, image_x, image_y]
                                if switch == 1:
                                    self.map_tiles.append(tile_data)
                                else:
                                    self.map_tiles2.append(tile_data)
                            # top type 2
                            elif tile == 23:
                                image = self.assets[type][21]
                                image_rect = image.get_rect()
                                image_x = x * scripts.constants.TILE_SIZE 
                                image_y = y * scripts.constants.TILE_SIZE 
                                image_rect.x= image_x
                                image_rect.y= image_y       
                                tile_data = [image, image_rect, image_x, image_y]
                                if switch == 1:
                                    self.map_tiles.append(tile_data)
                                else:
                                    self.map_tiles2.append(tile_data)
                            # top type 3
                            if tile == 24:
                                image = self.assets[type][22]
                                image_rect = image.get_rect()
                                image_x = x * scripts.constants.TILE_SIZE 
                                image_y = y * scripts.constants.TILE_SIZE 
                                image_rect.x= image_x
                                image_rect.y= image_y       
                                tile_data = [image, image_rect, image_x, image_y]
                                if switch == 1:
                                    self.map_tiles.append(tile_data)
                                else:
                                    self.map_tiles2.append(tile_data)
                            elif tile == 85:
                                image = self.assets[type][49]
                                image_rect = image.get_rect()
                                image_x = x * scripts.constants.TILE_SIZE 
                                image_y = y * scripts.constants.TILE_SIZE 
                                image_rect.x= image_x
                                image_rect.y= image_y       
                                tile_data = [image, image_rect, image_x, image_y]
                                if switch == 1:
                                    self.map_tiles.append(tile_data)
                                else:
                                    self.map_tiles2.append(tile_data)
            elif type == 'lavaland':
                for y, row in enumerate(data):
                    for x, tile in enumerate(row):
                        if tile >= 0:
                            # corner right 2
                            if tile == 95:
                                image = self.assets[type][62]
                                image_rect = image.get_rect()
                                image_x = x * scripts.constants.TILE_SIZE 
                                image_y = y * scripts.constants.TILE_SIZE 
                                image_rect.x= image_x
                                image_rect.y= image_y       
                                tile_data = [image, image_rect, image_x, image_y]
                                if switch == 1:
                                    self.map_tiles.append(tile_data)
                                else:
                                    self.map_tiles2.append(tile_data) 
                            # corner left 2
                            if tile == 94:
                                image = self.assets[type][61]
                                image_rect = image.get_rect()
                                image_x = x * scripts.constants.TILE_SIZE 
                                image_y = y * scripts.constants.TILE_SIZE 
                                image_rect.x= image_x
                                image_rect.y= image_y       
                                tile_data = [image, image_rect, image_x, image_y]
                                if switch == 1:
                                    self.map_tiles.append(tile_data)
                                else:
                                    self.map_tiles2.append(tile_data) 
                            # flat rock
                            if tile == 92:
                                image = self.assets[type][59]
                                image_rect = image.get_rect()
                                image_x = x * scripts.constants.TILE_SIZE 
                                image_y = y * scripts.constants.TILE_SIZE 
                                image_rect.x= image_x
                                image_rect.y= image_y       
                                tile_data = [image, image_rect, image_x, image_y]
                                if switch == 1:
                                    self.map_tiles.append(tile_data)
                                else:
                                    self.map_tiles2.append(tile_data) 
                            # ground type 1
                            elif tile == 91:
                                image = self.assets[type][58]
                                image_rect = image.get_rect()
                                image_x = x * scripts.constants.TILE_SIZE 
                                image_y = y * scripts.constants.TILE_SIZE 
                                image_rect.x= image_x
                                image_rect.y= image_y       
                                tile_data = [image, image_rect, image_x, image_y]
                                if switch == 1:
                                    self.map_tiles.append(tile_data)
                                else:
                                    self.map_tiles2.append(tile_data) 
                            # ground type 2
                            elif tile == 90:
                                image = self.assets[type][57]
                                image_rect = image.get_rect()
                                image_x = x * scripts.constants.TILE_SIZE 
                                image_y = y * scripts.constants.TILE_SIZE 
                                image_rect.x= image_x
                                image_rect.y= image_y       
                                tile_data = [image, image_rect, image_x, image_y]
                                if switch == 1:
                                    self.map_tiles.append(tile_data)
                                else:
                                    self.map_tiles2.append(tile_data) 
                            # ground type 3
                            elif tile == 86:
                                image = self.assets[type][53]
                                image_rect = image.get_rect()
                                image_x = x * scripts.constants.TILE_SIZE 
                                image_y = y * scripts.constants.TILE_SIZE 
                                image_rect.x= image_x
                                image_rect.y= image_y       
                                tile_data = [image, image_rect, image_x, image_y]
                                if switch == 1:
                                    self.map_tiles.append(tile_data)
                                else:
                                    self.map_tiles2.append(tile_data) 
                            # connect right 1
                            elif tile == 85:
                                image = self.assets[type][52]
                                image_rect = image.get_rect()
                                image_x = x * scripts.constants.TILE_SIZE 
                                image_y = y * scripts.constants.TILE_SIZE 
                                image_rect.x= image_x
                                image_rect.y= image_y       
                                tile_data = [image, image_rect, image_x, image_y]
                                if switch == 1:
                                    self.map_tiles.append(tile_data)
                                else:
                                    self.map_tiles2.append(tile_data) 
                            # connect left 1
                            elif tile == 84:
                                image = self.assets[type][51]
                                image_rect = image.get_rect()
                                image_x = x * scripts.constants.TILE_SIZE 
                                image_y = y * scripts.constants.TILE_SIZE 
                                image_rect.x= image_x
                                image_rect.y= image_y       
                                tile_data = [image, image_rect, image_x, image_y]
                                if switch == 1:
                                    self.map_tiles.append(tile_data)
                                else:
                                    self.map_tiles2.append(tile_data) 
                            # corner down right
                            elif tile == 82:
                                image = self.assets[type][49]
                                image_rect = image.get_rect()
                                image_x = x * scripts.constants.TILE_SIZE 
                                image_y = y * scripts.constants.TILE_SIZE 
                                image_rect.x= image_x
                                image_rect.y= image_y       
                                tile_data = [image, image_rect, image_x, image_y]
                                if switch == 1:
                                    self.map_tiles.append(tile_data)
                                else:
                                    self.map_tiles2.append(tile_data) 
                            # down
                            elif tile == 81:
                                image = self.assets[type][48]
                                image_rect = image.get_rect()
                                image_x = x * scripts.constants.TILE_SIZE 
                                image_y = y * scripts.constants.TILE_SIZE 
                                image_rect.x= image_x
                                image_rect.y= image_y       
                                tile_data = [image, image_rect, image_x, image_y]
                                if switch == 1:
                                    self.map_tiles.append(tile_data)
                                else:
                                    self.map_tiles2.append(tile_data) 
                            # corner down left
                            elif tile == 80:
                                image = self.assets[type][47]
                                image_rect = image.get_rect()
                                image_x = x * scripts.constants.TILE_SIZE 
                                image_y = y * scripts.constants.TILE_SIZE 
                                image_rect.x= image_x
                                image_rect.y= image_y       
                                tile_data = [image, image_rect, image_x, image_y]
                                if switch == 1:
                                    self.map_tiles.append(tile_data)
                                else:
                                    self.map_tiles2.append(tile_data) 
                            # right
                            elif tile == 72:
                                image = self.assets[type][39]
                                image_rect = image.get_rect()
                                image_x = x * scripts.constants.TILE_SIZE 
                                image_y = y * scripts.constants.TILE_SIZE 
                                image_rect.x= image_x
                                image_rect.y= image_y       
                                tile_data = [image, image_rect, image_x, image_y]
                                if switch == 1:
                                    self.map_tiles.append(tile_data)
                                else:
                                    self.map_tiles2.append(tile_data) 
                            # ground type 4
                            elif tile == 71:
                                image = self.assets[type][38]
                                image_rect = image.get_rect()
                                image_x = x * scripts.constants.TILE_SIZE 
                                image_y = y * scripts.constants.TILE_SIZE 
                                image_rect.x= image_x
                                image_rect.y= image_y       
                                tile_data = [image, image_rect, image_x, image_y]
                                if switch == 1:
                                    self.map_tiles.append(tile_data)
                                else:
                                    self.map_tiles2.append(tile_data) 
                            # left
                            elif tile == 70:
                                image = self.assets[type][37]
                                image_rect = image.get_rect()
                                image_x = x * scripts.constants.TILE_SIZE 
                                image_y = y * scripts.constants.TILE_SIZE 
                                image_rect.x= image_x
                                image_rect.y= image_y       
                                tile_data = [image, image_rect, image_x, image_y]
                                if switch == 1:
                                    self.map_tiles.append(tile_data)
                                else:
                                    self.map_tiles2.append(tile_data) 
                            # ground type 5
                            elif tile == 62:
                                image = self.assets[type][32]
                                image_rect = image.get_rect()
                                image_x = x * scripts.constants.TILE_SIZE 
                                image_y = y * scripts.constants.TILE_SIZE 
                                image_rect.x= image_x
                                image_rect.y= image_y       
                                tile_data = [image, image_rect, image_x, image_y]
                                if switch == 1:
                                    self.map_tiles.append(tile_data)
                                else:
                                    self.map_tiles2.append(tile_data) 
                            # ground type 6
                            elif tile == 61:
                                image = self.assets[type][31]
                                image_rect = image.get_rect()
                                image_x = x * scripts.constants.TILE_SIZE 
                                image_y = y * scripts.constants.TILE_SIZE 
                                image_rect.x= image_x
                                image_rect.y= image_y       
                                tile_data = [image, image_rect, image_x, image_y]
                                if switch == 1:
                                    self.map_tiles.append(tile_data)
                                else:
                                    self.map_tiles2.append(tile_data) 
                            # ground type 7
                            elif tile == 60:
                                image = self.assets[type][30]
                                image_rect = image.get_rect()
                                image_x = x * scripts.constants.TILE_SIZE 
                                image_y = y * scripts.constants.TILE_SIZE 
                                image_rect.x= image_x
                                image_rect.y= image_y       
                                tile_data = [image, image_rect, image_x, image_y]
                                if switch == 1:
                                    self.map_tiles.append(tile_data)
                                else:
                                    self.map_tiles2.append(tile_data) 
                            # ground type 8
                            elif tile == 55:
                                image = self.assets[type][28]
                                image_rect = image.get_rect()
                                image_x = x * scripts.constants.TILE_SIZE 
                                image_y = y * scripts.constants.TILE_SIZE 
                                image_rect.x= image_x
                                image_rect.y= image_y       
                                tile_data = [image, image_rect, image_x, image_y]
                                if switch == 1:
                                    self.map_tiles.append(tile_data)
                                else:
                                    self.map_tiles2.append(tile_data) 
                            # down 2
                            elif tile == 53:
                                image = self.assets[type][26]
                                image_rect = image.get_rect()
                                image_x = x * scripts.constants.TILE_SIZE 
                                image_y = y * scripts.constants.TILE_SIZE 
                                image_rect.x= image_x
                                image_rect.y= image_y       
                                tile_data = [image, image_rect, image_x, image_y]
                                if switch == 1:
                                    self.map_tiles.append(tile_data)
                                else:
                                    self.map_tiles2.append(tile_data) 
                            # connect right 2
                            elif tile == 52:
                                image = self.assets[type][25]
                                image_rect = image.get_rect()
                                image_x = x * scripts.constants.TILE_SIZE 
                                image_y = y * scripts.constants.TILE_SIZE 
                                image_rect.x= image_x
                                image_rect.y= image_y       
                                tile_data = [image, image_rect, image_x, image_y]
                                if switch == 1:
                                    self.map_tiles.append(tile_data)
                                else:
                                    self.map_tiles2.append(tile_data) 
                            # corner top right
                            elif tile == 51:
                                image = self.assets[type][24]
                                image_rect = image.get_rect()
                                image_x = x * scripts.constants.TILE_SIZE 
                                image_y = y * scripts.constants.TILE_SIZE 
                                image_rect.x= image_x
                                image_rect.y= image_y       
                                tile_data = [image, image_rect, image_x, image_y]
                                if switch == 1:
                                    self.map_tiles.append(tile_data)
                                else:
                                    self.map_tiles2.append(tile_data) 
                            # connect left down
                            elif tile == 50:
                                image = self.assets[type][23]
                                image_rect = image.get_rect()
                                image_x = x * scripts.constants.TILE_SIZE 
                                image_y = y * scripts.constants.TILE_SIZE 
                                image_rect.x= image_x
                                image_rect.y= image_y       
                                tile_data = [image, image_rect, image_x, image_y]
                                if switch == 1:
                                    self.map_tiles.append(tile_data)
                                else:
                                    self.map_tiles2.append(tile_data) 
                            # connect down 1
                            elif tile == 43:
                                image = self.assets[type][20]
                                image_rect = image.get_rect()
                                image_x = x * scripts.constants.TILE_SIZE 
                                image_y = y * scripts.constants.TILE_SIZE 
                                image_rect.x= image_x
                                image_rect.y= image_y       
                                tile_data = [image, image_rect, image_x, image_y]
                                if switch == 1:
                                    self.map_tiles.append(tile_data)
                                else:
                                    self.map_tiles2.append(tile_data) 
                            # connect top right
                            elif tile == 42:
                                image = self.assets[type][19]
                                image_rect = image.get_rect()
                                image_x = x * scripts.constants.TILE_SIZE 
                                image_y = y * scripts.constants.TILE_SIZE 
                                image_rect.x= image_x
                                image_rect.y= image_y       
                                tile_data = [image, image_rect, image_x, image_y]
                                if switch == 1:
                                    self.map_tiles.append(tile_data)
                                else:
                                    self.map_tiles2.append(tile_data) 
                            # corner top left
                            elif tile == 41:
                                image = self.assets[type][18]
                                image_rect = image.get_rect()
                                image_x = x * scripts.constants.TILE_SIZE 
                                image_y = y * scripts.constants.TILE_SIZE 
                                image_rect.x= image_x
                                image_rect.y= image_y       
                                tile_data = [image, image_rect, image_x, image_y]
                                if switch == 1:
                                    self.map_tiles.append(tile_data)
                                else:
                                    self.map_tiles2.append(tile_data) 
                            # connect top left
                            elif tile == 40:
                                image = self.assets[type][17]
                                image_rect = image.get_rect()
                                image_x = x * scripts.constants.TILE_SIZE 
                                image_y = y * scripts.constants.TILE_SIZE 
                                image_rect.x= image_x
                                image_rect.y= image_y       
                                tile_data = [image, image_rect, image_x, image_y]
                                if switch == 1:
                                    self.map_tiles.append(tile_data)
                                else:
                                    self.map_tiles2.append(tile_data) 
                            # connect top 2
                            elif tile == 33:
                                image = self.assets[type][14]
                                image_rect = image.get_rect()
                                image_x = x * scripts.constants.TILE_SIZE 
                                image_y = y * scripts.constants.TILE_SIZE 
                                image_rect.x= image_x
                                image_rect.y= image_y       
                                tile_data = [image, image_rect, image_x, image_y]
                                if switch == 1:
                                    self.map_tiles.append(tile_data)
                                else:
                                    self.map_tiles2.append(tile_data) 
                            # top right
                            elif tile == 32:
                                image = self.assets[type][13]
                                image_rect = image.get_rect()
                                image_x = x * scripts.constants.TILE_SIZE 
                                image_y = y * scripts.constants.TILE_SIZE 
                                image_rect.x= image_x
                                image_rect.y= image_y       
                                tile_data = [image, image_rect, image_x, image_y]
                                if switch == 1:
                                    self.map_tiles.append(tile_data)
                                else:
                                    self.map_tiles2.append(tile_data) 
                            # top
                            elif tile == 31:
                                image = self.assets[type][12]
                                image_rect = image.get_rect()
                                image_x = x * scripts.constants.TILE_SIZE 
                                image_y = y * scripts.constants.TILE_SIZE 
                                image_rect.x= image_x
                                image_rect.y= image_y       
                                tile_data = [image, image_rect, image_x, image_y]
                                if switch == 1:
                                    self.map_tiles.append(tile_data)
                                else:
                                    self.map_tiles2.append(tile_data) 
                            # top left
                            elif tile == 30:
                                image = self.assets[type][11]
                                image_rect = image.get_rect()
                                image_x = x * scripts.constants.TILE_SIZE 
                                image_y = y * scripts.constants.TILE_SIZE 
                                image_rect.x= image_x
                                image_rect.y= image_y       
                                tile_data = [image, image_rect, image_x, image_y]
                                if switch == 1:
                                    self.map_tiles.append(tile_data)
                                else:
                                    self.map_tiles2.append(tile_data) 
                            # right 2
                            elif tile == 24:
                                image = self.assets[type][9]
                                image_rect = image.get_rect()
                                image_x = x * scripts.constants.TILE_SIZE 
                                image_y = y * scripts.constants.TILE_SIZE 
                                image_rect.x= image_x
                                image_rect.y= image_y       
                                tile_data = [image, image_rect, image_x, image_y]
                                if switch == 1:
                                    self.map_tiles.append(tile_data)
                                else:
                                    self.map_tiles2.append(tile_data) 
                            # left 2
                            elif tile == 23:
                                image = self.assets[type][8]
                                image_rect = image.get_rect()
                                image_x = x * scripts.constants.TILE_SIZE 
                                image_y = y * scripts.constants.TILE_SIZE 
                                image_rect.x= image_x
                                image_rect.y= image_y       
                                tile_data = [image, image_rect, image_x, image_y]
                                if switch == 1:
                                    self.map_tiles.append(tile_data)
                                else:
                                    self.map_tiles2.append(tile_data) 
                            # right 3
                            elif tile == 21:
                                image = self.assets[type][6]
                                image_rect = image.get_rect()
                                image_x = x * scripts.constants.TILE_SIZE 
                                image_y = y * scripts.constants.TILE_SIZE 
                                image_rect.x= image_x
                                image_rect.y= image_y       
                                tile_data = [image, image_rect, image_x, image_y]
                                if switch == 1:
                                    self.map_tiles.append(tile_data)
                                else:
                                    self.map_tiles2.append(tile_data) 
                            # left 3
                            elif tile == 20:
                                image = self.assets[type][5]
                                image_rect = image.get_rect()
                                image_x = x * scripts.constants.TILE_SIZE 
                                image_y = y * scripts.constants.TILE_SIZE 
                                image_rect.x= image_x
                                image_rect.y= image_y       
                                tile_data = [image, image_rect, image_x, image_y]
                                if switch == 1:
                                    self.map_tiles.append(tile_data)
                                else:
                                    self.map_tiles2.append(tile_data) 
        
        # decorations down 3 decorations up 4                        
        elif switch == 3 or switch == 4:
            if type == 'grassland':
                for y, row in enumerate(data):
                    for x, tile in enumerate(row):
                        if tile >= 0:
                            # log
                            if tile == 2:
                                image = self.assets[type][25]
                                image_rect = image.get_rect()
                                image_x = x * scripts.constants.TILE_SIZE 
                                image_y = y * scripts.constants.TILE_SIZE 
                                image_rect.x= image_x
                                image_rect.y= image_y       
                                tile_data = [image, image_rect, image_x, image_y]
                                if switch == 3:
                                    self.decorations_down_tiles.append(tile_data)
                                else:
                                    self.decorations_up_tiles.append(tile_data)
                            # cut down tree            
                            elif tile == 3:
                                image = self.assets[type][26]
                                image_rect = image.get_rect()
                                image_x = x * scripts.constants.TILE_SIZE 
                                image_y = y * scripts.constants.TILE_SIZE 
                                image_rect.x= image_x
                                image_rect.y= image_y       
                                tile_data = [image, image_rect, image_x, image_y]
                                if switch == 3:
                                    self.decorations_down_tiles.append(tile_data)
                                else:
                                    self.decorations_up_tiles.append(tile_data)
                            # rock type 1
                            elif tile == 10:
                                image = self.assets[type][27]
                                image_rect = image.get_rect()
                                image_x = x * scripts.constants.TILE_SIZE 
                                image_y = y * scripts.constants.TILE_SIZE 
                                image_rect.x= image_x
                                image_rect.y= image_y       
                                tile_data = [image, image_rect, image_x, image_y]
                                if switch == 3:
                                    self.decorations_down_tiles.append(tile_data)
                                else:
                                    self.decorations_up_tiles.append(tile_data)
                            # rock type 2
                            elif tile == 11:
                                image = self.assets[type][28]
                                image_rect = image.get_rect()
                                image_x = x * scripts.constants.TILE_SIZE 
                                image_y = y * scripts.constants.TILE_SIZE 
                                image_rect.x= image_x
                                image_rect.y= image_y       
                                tile_data = [image, image_rect, image_x, image_y]
                                if switch == 3:
                                    self.decorations_down_tiles.append(tile_data)
                                else:
                                    self.decorations_up_tiles.append(tile_data)
                            # lake
                            elif tile == 12:
                                image = self.assets[type][29]
                                image_rect = image.get_rect()
                                image_x = x * scripts.constants.TILE_SIZE 
                                image_y = y * scripts.constants.TILE_SIZE 
                                image_rect.x= image_x
                                image_rect.y= image_y       
                                tile_data = [image, image_rect, image_x, image_y]
                                if switch == 3:
                                    self.decorations_down_tiles.append(tile_data)
                                else:
                                    self.decorations_up_tiles.append(tile_data)
                            # bush
                            elif tile == 13:
                                image = self.assets[type][30]
                                image_rect = image.get_rect()
                                image_x = x * scripts.constants.TILE_SIZE 
                                image_y = y * scripts.constants.TILE_SIZE 
                                image_rect.x= image_x
                                image_rect.y= image_y       
                                tile_data = [image, image_rect, image_x, image_y]
                                if switch == 3:
                                    self.decorations_down_tiles.append(tile_data)
                                else:
                                    self.decorations_up_tiles.append(tile_data)
                            # grass
                            elif tile == 20:
                                image = self.assets[type][31]
                                image_rect = image.get_rect()
                                image_x = x * scripts.constants.TILE_SIZE 
                                image_y = y * scripts.constants.TILE_SIZE 
                                image_rect.x= image_x
                                image_rect.y= image_y       
                                tile_data = [image, image_rect, image_x, image_y]
                                if switch == 3:
                                    self.decorations_down_tiles.append(tile_data)
                                else:
                                    self.decorations_up_tiles.append(tile_data)
                            # flower type 1
                            elif tile == 21:
                                image = self.assets[type][32]
                                image_rect = image.get_rect()
                                image_x = x * scripts.constants.TILE_SIZE 
                                image_y = y * scripts.constants.TILE_SIZE 
                                image_rect.x= image_x
                                image_rect.y= image_y       
                                tile_data = [image, image_rect, image_x, image_y]
                                if switch == 3:
                                    self.decorations_down_tiles.append(tile_data)
                                else:
                                    self.decorations_up_tiles.append(tile_data)
                            # flower type 2
                            elif tile == 25:
                                image = self.assets[type][33]
                                image_rect = image.get_rect()
                                image_x = x * scripts.constants.TILE_SIZE 
                                image_y = y * scripts.constants.TILE_SIZE 
                                image_rect.x= image_x
                                image_rect.y= image_y       
                                tile_data = [image, image_rect, image_x, image_y]
                                if switch == 3:
                                    self.decorations_down_tiles.append(tile_data)
                                else:
                                    self.decorations_up_tiles.append(tile_data)
                            # wood storage    
                            elif tile == 96:
                                image = self.assets[type][35]
                                image_rect = image.get_rect()
                                image_x = x * scripts.constants.TILE_SIZE 
                                image_y = y * scripts.constants.TILE_SIZE 
                                image_rect.x= image_x
                                image_rect.y= image_y       
                                tile_data = [image, image_rect, image_x, image_y]
                                if switch == 3:
                                    self.decorations_down_tiles.append(tile_data)
                                else:
                                    self.decorations_up_tiles.append(tile_data)
                            # fence
                            elif tile == 97:
                                image = self.assets[type][36]
                                image_rect = image.get_rect()
                                image_x = x * scripts.constants.TILE_SIZE 
                                image_y = y * scripts.constants.TILE_SIZE 
                                image_rect.x= image_x
                                image_rect.y= image_y       
                                tile_data = [image, image_rect, image_x, image_y]
                                if switch == 3:
                                    self.decorations_down_tiles.append(tile_data)
                                else:
                                    self.decorations_up_tiles.append(tile_data)
                            # broken fence
                            elif tile == 98:
                                image = self.assets[type][37]
                                image_rect = image.get_rect()
                                image_x = x * scripts.constants.TILE_SIZE 
                                image_y = y * scripts.constants.TILE_SIZE 
                                image_rect.x= image_x
                                image_rect.y= image_y       
                                tile_data = [image, image_rect, image_x, image_y]
                                if switch == 3:
                                    self.decorations_down_tiles.append(tile_data)
                                else:
                                    self.decorations_up_tiles.append(tile_data)
                            # tree down part
                            elif tile == 90:
                                image = self.assets[type][38]
                                image_rect = image.get_rect()
                                image_x = x * scripts.constants.TILE_SIZE 
                                image_y = y * scripts.constants.TILE_SIZE 
                                image_rect.x= image_x
                                image_rect.y= image_y       
                                tile_data = [image, image_rect, image_x, image_y]
                                if switch == 3:
                                    self.decorations_down_tiles.append(tile_data)
                                else:
                                    self.decorations_up_tiles.append(tile_data)
                            # tree middle part
                            elif tile == 80:
                                image = self.assets[type][39]
                                image_rect = image.get_rect()
                                image_x = x * scripts.constants.TILE_SIZE 
                                image_y = y * scripts.constants.TILE_SIZE 
                                image_rect.x= image_x
                                image_rect.y= image_y       
                                tile_data = [image, image_rect, image_x, image_y]
                                if switch == 3:
                                    self.decorations_down_tiles.append(tile_data)
                                else:
                                    self.decorations_up_tiles.append(tile_data)
                            # tree top part
                            elif tile == 70:
                                image = self.assets[type][40]
                                image_rect = image.get_rect()
                                image_x = x * scripts.constants.TILE_SIZE 
                                image_y = y * scripts.constants.TILE_SIZE 
                                image_rect.x= image_x
                                image_rect.y= image_y       
                                tile_data = [image, image_rect, image_x, image_y]
                                if switch == 3:
                                    self.decorations_down_tiles.append(tile_data)
                                else:
                                    self.decorations_up_tiles.append(tile_data)
            elif type == 'lavaland':
                for y, row in enumerate(data):
                    for x, tile in enumerate(row):
                        if tile >= 0:
                            # column down
                            if tile == 98:
                                image = self.assets[type][65]
                                image_rect = image.get_rect()
                                image_x = x * scripts.constants.TILE_SIZE 
                                image_y = y * scripts.constants.TILE_SIZE 
                                image_rect.x= image_x
                                image_rect.y= image_y       
                                tile_data = [image, image_rect, image_x, image_y]
                                if switch == 3:
                                    self.decorations_down_tiles.append(tile_data)
                                else:
                                    self.decorations_up_tiles.append(tile_data)
                            # dust
                            elif tile == 97:
                                image = self.assets[type][64]
                                image_rect = image.get_rect()
                                image_x = x * scripts.constants.TILE_SIZE 
                                image_y = y * scripts.constants.TILE_SIZE 
                                image_rect.x= image_x
                                image_rect.y= image_y       
                                tile_data = [image, image_rect, image_x, image_y]
                                if switch == 3:
                                    self.decorations_down_tiles.append(tile_data)
                                else:
                                    self.decorations_up_tiles.append(tile_data)
                            # a lot of dust
                            elif tile == 96:
                                image = self.assets[type][63]
                                image_rect = image.get_rect()
                                image_x = x * scripts.constants.TILE_SIZE 
                                image_y = y * scripts.constants.TILE_SIZE 
                                image_rect.x= image_x
                                image_rect.y= image_y       
                                tile_data = [image, image_rect, image_x, image_y]
                                if switch == 3:
                                    self.decorations_down_tiles.append(tile_data)
                                else:
                                    self.decorations_up_tiles.append(tile_data)
                            # lamp down
                            elif tile == 89:
                                image = self.assets[type][56]
                                image_rect = image.get_rect()
                                image_x = x * scripts.constants.TILE_SIZE 
                                image_y = y * scripts.constants.TILE_SIZE 
                                image_rect.x= image_x
                                image_rect.y= image_y       
                                tile_data = [image, image_rect, image_x, image_y]
                                if switch == 3:
                                    self.decorations_down_tiles.append(tile_data)
                                else:
                                    self.decorations_up_tiles.append(tile_data)
                            # column middle
                            elif tile == 88:
                                image = self.assets[type][55]
                                image_rect = image.get_rect()
                                image_x = x * scripts.constants.TILE_SIZE 
                                image_y = y * scripts.constants.TILE_SIZE 
                                image_rect.x= image_x
                                image_rect.y= image_y       
                                tile_data = [image, image_rect, image_x, image_y]
                                if switch == 3:
                                    self.decorations_down_tiles.append(tile_data)
                                else:
                                    self.decorations_up_tiles.append(tile_data)
                            # broken column
                            elif tile == 87:
                                image = self.assets[type][54]
                                image_rect = image.get_rect()
                                image_x = x * scripts.constants.TILE_SIZE 
                                image_y = y * scripts.constants.TILE_SIZE 
                                image_rect.x= image_x
                                image_rect.y= image_y       
                                tile_data = [image, image_rect, image_x, image_y]
                                if switch == 3:
                                    self.decorations_down_tiles.append(tile_data)
                                else:
                                    self.decorations_up_tiles.append(tile_data)
                            # lamp top
                            elif tile == 79:
                                image = self.assets[type][46]
                                image_rect = image.get_rect()
                                image_x = x * scripts.constants.TILE_SIZE 
                                image_y = y * scripts.constants.TILE_SIZE 
                                image_rect.x= image_x
                                image_rect.y= image_y       
                                tile_data = [image, image_rect, image_x, image_y]
                                if switch == 3:
                                    self.decorations_down_tiles.append(tile_data)
                                else:
                                    self.decorations_up_tiles.append(tile_data)
                            # column top
                            elif tile == 78:
                                image = self.assets[type][45]
                                image_rect = image.get_rect()
                                image_x = x * scripts.constants.TILE_SIZE 
                                image_y = y * scripts.constants.TILE_SIZE 
                                image_rect.x= image_x
                                image_rect.y= image_y       
                                tile_data = [image, image_rect, image_x, image_y]
                                if switch == 3:
                                    self.decorations_down_tiles.append(tile_data)
                                else:
                                    self.decorations_up_tiles.append(tile_data)
                            # smoke right
                            elif tile == 77:
                                image = self.assets[type][44]
                                image_rect = image.get_rect()
                                image_x = x * scripts.constants.TILE_SIZE 
                                image_y = y * scripts.constants.TILE_SIZE 
                                image_rect.x= image_x
                                image_rect.y= image_y       
                                tile_data = [image, image_rect, image_x, image_y]
                                if switch == 3:
                                    self.decorations_down_tiles.append(tile_data)
                                else:
                                    self.decorations_up_tiles.append(tile_data)
                            # smoke middle
                            elif tile == 76:
                                image = self.assets[type][43]
                                image_rect = image.get_rect()
                                image_x = x * scripts.constants.TILE_SIZE 
                                image_y = y * scripts.constants.TILE_SIZE 
                                image_rect.x= image_x
                                image_rect.y= image_y       
                                tile_data = [image, image_rect, image_x, image_y]
                                if switch == 3:
                                    self.decorations_down_tiles.append(tile_data)
                                else:
                                    self.decorations_up_tiles.append(tile_data)
                            # smoke left
                            elif tile == 75:
                                image = self.assets[type][42]
                                image_rect = image.get_rect()
                                image_x = x * scripts.constants.TILE_SIZE 
                                image_y = y * scripts.constants.TILE_SIZE 
                                image_rect.x= image_x
                                image_rect.y= image_y       
                                tile_data = [image, image_rect, image_x, image_y]
                                if switch == 3:
                                    self.decorations_down_tiles.append(tile_data)
                                else:
                                    self.decorations_up_tiles.append(tile_data)
                            # decorated column down
                            elif tile == 74:
                                image = self.assets[type][41]
                                image_rect = image.get_rect()
                                image_x = x * scripts.constants.TILE_SIZE 
                                image_y = y * scripts.constants.TILE_SIZE 
                                image_rect.x= image_x
                                image_rect.y= image_y       
                                tile_data = [image, image_rect, image_x, image_y]
                                if switch == 3:
                                    self.decorations_down_tiles.append(tile_data)
                                else:
                                    self.decorations_up_tiles.append(tile_data)
                            # paladin statue
                            elif tile == 66:
                                image = self.assets[type][36]
                                image_rect = image.get_rect()
                                image_x = x * scripts.constants.TILE_SIZE 
                                image_y = y * scripts.constants.TILE_SIZE 
                                image_rect.x= image_x
                                image_rect.y= image_y       
                                tile_data = [image, image_rect, image_x, image_y]
                                if switch == 3:
                                    self.decorations_down_tiles.append(tile_data)
                                else:
                                    self.decorations_up_tiles.append(tile_data)
                            # stone
                            elif tile == 65:
                                image = self.assets[type][35]
                                image_rect = image.get_rect()
                                image_x = x * scripts.constants.TILE_SIZE 
                                image_y = y * scripts.constants.TILE_SIZE 
                                image_rect.x= image_x
                                image_rect.y= image_y       
                                tile_data = [image, image_rect, image_x, image_y]
                                if switch == 3:
                                    self.decorations_down_tiles.append(tile_data)
                                else:
                                    self.decorations_up_tiles.append(tile_data)
                            # decorated column top
                            elif tile == 64:
                                image = self.assets[type][34]
                                image_rect = image.get_rect()
                                image_x = x * scripts.constants.TILE_SIZE 
                                image_y = y * scripts.constants.TILE_SIZE 
                                image_rect.x= image_x
                                image_rect.y= image_y       
                                tile_data = [image, image_rect, image_x, image_y]
                                if switch == 3:
                                    self.decorations_down_tiles.append(tile_data)
                                else:
                                    self.decorations_up_tiles.append(tile_data)
                            # gargoyla statue
                            elif tile == 56:
                                image = self.assets[type][29]
                                image_rect = image.get_rect()
                                image_x = x * scripts.constants.TILE_SIZE 
                                image_y = y * scripts.constants.TILE_SIZE 
                                image_rect.x= image_x
                                image_rect.y= image_y       
                                tile_data = [image, image_rect, image_x, image_y]
                                if switch == 3:
                                    self.decorations_down_tiles.append(tile_data)
                                else:
                                    self.decorations_up_tiles.append(tile_data)
                            # rocks
                            elif tile == 54:
                                image = self.assets[type][27]
                                image_rect = image.get_rect()
                                image_x = x * scripts.constants.TILE_SIZE 
                                image_y = y * scripts.constants.TILE_SIZE 
                                image_rect.x= image_x
                                image_rect.y= image_y       
                                tile_data = [image, image_rect, image_x, image_y]
                                if switch == 3:
                                    self.decorations_down_tiles.append(tile_data)
                                else:
                                    self.decorations_up_tiles.append(tile_data)
                            # angel statue right down
                            elif tile == 55:
                                image = self.assets[type][22]
                                image_rect = image.get_rect()
                                image_x = x * scripts.constants.TILE_SIZE 
                                image_y = y * scripts.constants.TILE_SIZE 
                                image_rect.x= image_x
                                image_rect.y= image_y       
                                tile_data = [image, image_rect, image_x, image_y]
                                if switch == 3:
                                    self.decorations_down_tiles.append(tile_data)
                                else:
                                    self.decorations_up_tiles.append(tile_data)
                            # angel statue left down
                            elif tile == 54:
                                image = self.assets[type][21]
                                image_rect = image.get_rect()
                                image_x = x * scripts.constants.TILE_SIZE 
                                image_y = y * scripts.constants.TILE_SIZE 
                                image_rect.x= image_x
                                image_rect.y= image_y       
                                tile_data = [image, image_rect, image_x, image_y]
                                if switch == 3:
                                    self.decorations_down_tiles.append(tile_data)
                                else:
                                    self.decorations_up_tiles.append(tile_data)
                            # angel statue right top
                            elif tile == 45:
                                image = self.assets[type][16]
                                image_rect = image.get_rect()
                                image_x = x * scripts.constants.TILE_SIZE 
                                image_y = y * scripts.constants.TILE_SIZE 
                                image_rect.x= image_x
                                image_rect.y= image_y       
                                tile_data = [image, image_rect, image_x, image_y]
                                if switch == 3:
                                    self.decorations_down_tiles.append(tile_data)
                                else:
                                    self.decorations_up_tiles.append(tile_data)
                            # angel statue left top
                            elif tile == 44:
                                image = self.assets[type][15]
                                image_rect = image.get_rect()
                                image_x = x * scripts.constants.TILE_SIZE 
                                image_y = y * scripts.constants.TILE_SIZE 
                                image_rect.x= image_x
                                image_rect.y= image_y       
                                tile_data = [image, image_rect, image_x, image_y]
                                if switch == 3:
                                    self.decorations_down_tiles.append(tile_data)
                                else:
                                    self.decorations_up_tiles.append(tile_data)
                            # lavalake
                            elif tile == 25:
                                image = self.assets[type][10]
                                image_rect = image.get_rect()
                                image_x = x * scripts.constants.TILE_SIZE 
                                image_y = y * scripts.constants.TILE_SIZE 
                                image_rect.x= image_x
                                image_rect.y= image_y       
                                tile_data = [image, image_rect, image_x, image_y]
                                if switch == 3:
                                    self.decorations_down_tiles.append(tile_data)
                                else:
                                    self.decorations_up_tiles.append(tile_data)
                            # angel statue right top
                            elif tile == 45:
                                image = self.assets[type][16]
                                image_rect = image.get_rect()
                                image_x = x * scripts.constants.TILE_SIZE 
                                image_y = y * scripts.constants.TILE_SIZE 
                                image_rect.x= image_x
                                image_rect.y= image_y       
                                tile_data = [image, image_rect, image_x, image_y]
                                if switch == 3:
                                    self.decorations_down_tiles.append(tile_data)
                                else:
                                    self.decorations_up_tiles.append(tile_data)
                            # filar
                            elif tile == 6:
                                image = self.assets[type][4]
                                image_rect = image.get_rect()
                                image_x = x * scripts.constants.TILE_SIZE 
                                image_y = y * scripts.constants.TILE_SIZE 
                                image_rect.x= image_x
                                image_rect.y= image_y       
                                tile_data = [image, image_rect, image_x, image_y]
                                if switch == 3:
                                    self.decorations_down_tiles.append(tile_data)
                                else:
                                    self.decorations_up_tiles.append(tile_data)
                            
                       
        # mobs, objects etc.                       
        elif switch == 5:
            if type == 'grassland':
                for y, row in enumerate(data):
                    for x, tile in enumerate(row):
                        if tile >= 0:
                            if tile == 100:
                                self.objects.append(NextRoomEnterence(x * scripts.constants.TILE_SIZE, y * scripts.constants.TILE_SIZE))
                            if tile == 101:
                                self.objects.append(PreviousRoomEnterence(x * scripts.constants.TILE_SIZE, y * scripts.constants.TILE_SIZE))
                                
                                                
                            # CHEST
                            if tile == 0:
                                self.objects.append(Chest(x * scripts.constants.TILE_SIZE, y * scripts.constants.TILE_SIZE, closed_chest_img = self.assets[type][23], opened_chest_img = self.assets[type][24]))
                            
                            # PORTAL
                            elif tile == 30:
                                image = self.assets[type][34]
                                image_rect = image.get_rect()
                                image_x = x * scripts.constants.TILE_SIZE 
                                image_y = y * scripts.constants.TILE_SIZE 
                                image_rect.x= image_x
                                image_rect.y= image_y       
                                tile_data = [image, image_rect, image_x, image_y]
                                self.gate_tiles.append(tile_data) 
                            
                            # PLAYER
                            elif tile == 40:
                                image = None
                                image_rect = None
                                image_x = x * scripts.constants.TILE_SIZE 
                                image_y = y * scripts.constants.TILE_SIZE        
                                tile_data = [image, image_rect, image_x, image_y]
                                if scripts.constants.HERO == 'player1':
                                    self.player = Peasant(tile_data[2],tile_data[3],scripts.constants.PLAYER_HP)
                                elif scripts.constants.HERO == 'wizard':
                                    self.player = Wizard(tile_data[2],tile_data[3],scripts.constants.PLAYER_HP)
                                elif scripts.constants.HERO == 'dwarf':
                                    self.player = Dwarf(tile_data[2],tile_data[3],scripts.constants.PLAYER_HP)
                                elif scripts.constants.HERO == 'knight':
                                    self.player = Knight(tile_data[2],tile_data[3],scripts.constants.PLAYER_HP)
                                elif scripts.constants.HERO == 'pikemen':
                                    self.player = Pikemen(tile_data[2],tile_data[3],scripts.constants.PLAYER_HP)
                                elif scripts.constants.HERO == 'elf':
                                    self.player = Elf(tile_data[2],tile_data[3],scripts.constants.PLAYER_HP)
                                elif scripts.constants.HERO == 'paladin':
                                    self.player = Paladin(tile_data[2],tile_data[3],scripts.constants.PLAYER_HP)
                                elif scripts.constants.HERO == 'druid':
                                    self.player = scripts.character.Druid(tile_data[2],tile_data[3],scripts.constants.PLAYER_HP)
                            
                            # SLIME
                            elif tile == 50:
                                image = None
                                image_rect = None
                                image_x = x * scripts.constants.TILE_SIZE 
                                image_y = y * scripts.constants.TILE_SIZE        
                                tile_data = [image, image_rect, image_x, image_y]
                                self.character_list.append(Slime(tile_data[2],tile_data[3],scripts.constants.SLIME_HP, self.world_level))
                            
                            # WOLF
                            elif tile == 60:
                                image = None
                                image_rect = None
                                image_x = x * scripts.constants.TILE_SIZE 
                                image_y = y * scripts.constants.TILE_SIZE        
                                tile_data = [image, image_rect, image_x, image_y]
                                self.character_list.append(Wolf(tile_data[2],tile_data[3],scripts.constants.WOLF_HP, self.world_level))
                                #self.character_list.append(Imp(tile_data[2],tile_data[3],scripts.constants.WOLF_HP, self.world_level))
                            
                            # TROLL
                            elif tile == 51:
                                image = None
                                image_rect = None
                                image_x = x * scripts.constants.TILE_SIZE 
                                image_y = y * scripts.constants.TILE_SIZE        
                                tile_data = [image, image_rect, image_x, image_y]
                                self.character_list.append(Troll(tile_data[2],tile_data[3],scripts.constants.TROLL_HP, self.world_level))
                            
                            # GOBLIN
                            elif tile == 52:
                                image = None
                                image_rect = None
                                image_x = x * scripts.constants.TILE_SIZE 
                                image_y = y * scripts.constants.TILE_SIZE        
                                tile_data = [image, image_rect, image_x, image_y]
                                self.character_list.append(Goblin(tile_data[2],tile_data[3],scripts.constants.GOBLIN_HP, self.world_level))
                            
                            # ENT
                            elif tile == 53:
                                image = None
                                image_rect = None
                                image_x = x * scripts.constants.TILE_SIZE 
                                image_y = y * scripts.constants.TILE_SIZE        
                                tile_data = [image, image_rect, image_x, image_y]
                                self.character_list.append(Ent(tile_data[2],tile_data[3],scripts.constants.ENT_HP, self.world_level))
                            
                            # SLIME FIRE WIZARD
                            elif tile == 54:
                                image = None
                                image_rect = None
                                image_x = x * scripts.constants.TILE_SIZE 
                                image_y = y * scripts.constants.TILE_SIZE        
                                tile_data = [image, image_rect, image_x, image_y]
                                self.character_list.append(SlimeFireWizard(tile_data[2],tile_data[3],scripts.constants.SLIME_FIRE_WIZARD_HP, self.world_level))
                            
                            # DRUID
                            elif tile == 55:
                                image = None
                                image_rect = None
                                image_x = x * scripts.constants.TILE_SIZE 
                                image_y = y * scripts.constants.TILE_SIZE        
                                tile_data = [image, image_rect, image_x, image_y]
                                self.character_list.append(scripts.enemies.Druid(tile_data[2],tile_data[3],scripts.constants.DRUID_HP, self.world_level))
            elif type == 'lavaland':
                for y, row in enumerate(data):
                    for x, tile in enumerate(row):
                        if tile >= 0:                
                            # CHEST
                            if tile == 0:
                                self.objects.append(Chest(x * scripts.constants.TILE_SIZE, y * scripts.constants.TILE_SIZE, closed_chest_img = self.assets[type][0], opened_chest_img = self.assets[type][1]))
                            
                            # PORTAL
                            elif tile == 22:
                                image = self.assets[type][7]
                                image_rect = image.get_rect()
                                image_x = x * scripts.constants.TILE_SIZE 
                                image_y = y * scripts.constants.TILE_SIZE 
                                image_rect.x= image_x
                                image_rect.y= image_y       
                                tile_data = [image, image_rect, image_x, image_y]
                                self.gate_tiles.append(tile_data) 
                            
                            # FIRE UP PLAYER
                            elif tile == 2:
                                 self.objects.append(FireUpPlayer(x * scripts.constants.TILE_SIZE, y * scripts.constants.TILE_SIZE))
                            # GAYZER
                            elif tile == 4:
                                pass 
                            # EXP
                            elif tile == 5:
                                pass 
                            
                            # PLAYER
                            elif tile == 10:
                                image = None
                                image_rect = None
                                image_x = x * scripts.constants.TILE_SIZE 
                                image_y = y * scripts.constants.TILE_SIZE        
                                tile_data = [image, image_rect, image_x, image_y]
                                if scripts.constants.HERO == 'player1':
                                    self.player = Peasant(tile_data[2],tile_data[3],scripts.constants.PLAYER_HP)
                                elif scripts.constants.HERO == 'wizard':
                                    self.player = Wizard(tile_data[2],tile_data[3],scripts.constants.PLAYER_HP)
                                elif scripts.constants.HERO == 'dwarf':
                                    self.player = Dwarf(tile_data[2],tile_data[3],scripts.constants.PLAYER_HP)
                                elif scripts.constants.HERO == 'knight':
                                    self.player = Knight(tile_data[2],tile_data[3],scripts.constants.PLAYER_HP)
                                elif scripts.constants.HERO == 'pikemen':
                                    self.player = Pikemen(tile_data[2],tile_data[3],scripts.constants.PLAYER_HP)
                                elif scripts.constants.HERO == 'elf':
                                    self.player = Elf(tile_data[2],tile_data[3],scripts.constants.PLAYER_HP)
                                elif scripts.constants.HERO == 'paladin':
                                    self.player = Paladin(tile_data[2],tile_data[3],scripts.constants.PLAYER_HP)
                                elif scripts.constants.HERO == 'druid':
                                    self.player = scripts.character.Druid(tile_data[2],tile_data[3],scripts.constants.PLAYER_HP)
                            
                            # SLIME
                            elif tile == 11:
                                image = None
                                image_rect = None
                                image_x = x * scripts.constants.TILE_SIZE 
                                image_y = y * scripts.constants.TILE_SIZE        
                                tile_data = [image, image_rect, image_x, image_y]
                                self.character_list.append(Slime(tile_data[2],tile_data[3],scripts.constants.SLIME_HP, self.world_level))
                            
                            # WOLF
                            elif tile == 12:
                                image = None
                                image_rect = None
                                image_x = x * scripts.constants.TILE_SIZE 
                                image_y = y * scripts.constants.TILE_SIZE        
                                tile_data = [image, image_rect, image_x, image_y]
                                self.character_list.append(Wolf(tile_data[2],tile_data[3],scripts.constants.WOLF_HP, self.world_level))
                                #self.character_list.append(Imp(tile_data[2],tile_data[3],scripts.constants.WOLF_HP, self.world_level))
                            
                            # TROLL
                            elif tile == 13:
                                image = None
                                image_rect = None
                                image_x = x * scripts.constants.TILE_SIZE 
                                image_y = y * scripts.constants.TILE_SIZE        
                                tile_data = [image, image_rect, image_x, image_y]
                                self.character_list.append(Troll(tile_data[2],tile_data[3],scripts.constants.TROLL_HP, self.world_level))
                            
                            # GOBLIN
                            elif tile == 14:
                                image = None
                                image_rect = None
                                image_x = x * scripts.constants.TILE_SIZE 
                                image_y = y * scripts.constants.TILE_SIZE        
                                tile_data = [image, image_rect, image_x, image_y]
                                self.character_list.append(Goblin(tile_data[2],tile_data[3],scripts.constants.GOBLIN_HP, self.world_level))
                            
                            # ENT
                            elif tile == 15:
                                image = None
                                image_rect = None
                                image_x = x * scripts.constants.TILE_SIZE 
                                image_y = y * scripts.constants.TILE_SIZE        
                                tile_data = [image, image_rect, image_x, image_y]
                                self.character_list.append(Ent(tile_data[2],tile_data[3],scripts.constants.ENT_HP, self.world_level))
                            
                            # SLIME FIRE WIZARD
                            elif tile == 16:
                                image = None
                                image_rect = None
                                image_x = x * scripts.constants.TILE_SIZE 
                                image_y = y * scripts.constants.TILE_SIZE        
                                tile_data = [image, image_rect, image_x, image_y]
                                self.character_list.append(SlimeFireWizard(tile_data[2],tile_data[3],scripts.constants.SLIME_FIRE_WIZARD_HP, self.world_level))
                            
                            # DRUID
                            elif tile == 17:
                                image = None
                                image_rect = None
                                image_x = x * scripts.constants.TILE_SIZE 
                                image_y = y * scripts.constants.TILE_SIZE        
                                tile_data = [image, image_rect, image_x, image_y]
                                self.character_list.append(scripts.enemies.Druid(tile_data[2],tile_data[3],scripts.constants.DRUID_HP, self.world_level))
        
        
    def generate(self, mobs = False):  
        pass
    
    def update(self, screen_scroll):
        for tile in self.obstacle_tile:
            tile[2] += screen_scroll[0]
            tile[3] += screen_scroll[1]
            tile[1].center = (tile[2], tile[3])
        for tile in self.map_tiles:
            tile[2] += screen_scroll[0]
            tile[3] += screen_scroll[1]
            tile[1].center = (tile[2], tile[3])
        if self.map_tiles2:
            for tile in self.map_tiles2:
                tile[2] += screen_scroll[0]
                tile[3] += screen_scroll[1]
                tile[1].center = (tile[2], tile[3])
        for tile in self.decorations_down_tiles:
            tile[2] += screen_scroll[0]
            tile[3] += screen_scroll[1]
            tile[1].center = (tile[2], tile[3])
        for tile in self.decorations_up_tiles:
            tile[2] += screen_scroll[0]
            tile[3] += screen_scroll[1]
            tile[1].center = (tile[2], tile[3])
        for tile in self.gate_tiles:
            tile[2] += screen_scroll[0]
            tile[3] += screen_scroll[1]
            tile[1].center = (tile[2], tile[3])

    def draw(self,surface):
        for tile in self.map_tiles:
            surface.blit(tile[0], tile[1])
        if self.map_tiles2:
            for tile in self.map_tiles2:
                surface.blit(tile[0], tile[1])
        for tile in self.decorations_down_tiles:
            surface.blit(tile[0], tile[1])
        if self.gate_tiles:
            for tile in self.gate_tiles:
                surface.blit(tile[0], tile[1])
    
    def draw_src(self,surface, source):
        for tile in source:
            surface.blit(tile[0], tile[1])

    def new_level(self, player):
        return player.health, player.health_max, player.gold, player.level, player.current_experience, player.experience_to_gain_new_level
    
    def check_if_new_level(self, exit_tiles, player, new_level):
        for exit_tile in exit_tiles:
            if exit_tile[1].colliderect(player.rect):
                new_level = True
                return new_level
        return new_level

                

                