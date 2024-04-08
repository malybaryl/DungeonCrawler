import pygame
import scripts.constants
from scripts.load import loadImages
from scripts.character import Character
from scripts.enemies import Slime, Wolf, Troll, Goblin, Ent, SlimeFireWizard, Druid
from scripts.objects import Chest
from random import randint
import csv

def draw_grid(display):
        for x in range(30):
            pygame.draw.line(display, scripts.constants.WHITE, (x*scripts.constants.TILE_SIZE,0), (x*scripts.constants.TILE_SIZE, scripts.constants.SCREEN_HEIGHT))
            pygame.draw.line(display, scripts.constants.WHITE, (0,x*scripts.constants.TILE_SIZE), (scripts.constants.SCREEN_WIDTH, x*scripts.constants.TILE_SIZE))
            

class World():
    def __init__(self):
        self.assets={
            "castle": loadImages("tilemap/castle"),
            "grassland": loadImages("tilemap/grassland")
        }
        self.map_tiles = []
        self.obstacle_tile = []
        self.decorations_up_tiles = []
        self.exit_tile = None
        self.player = None
        self.boss_list = []
        self.character_list = []
        self.gate_tiles = []
        self.world_data = []
        self.world_mobs_data = []
        self.world_objects_data = []
        self.world_decorations_down = []
        self.world_decorations_up = []
        self.objects = []
        

    def proced_csv_file(self, rows=50, cols=50, world_level = 1):
        
        if world_level % 3 == 0:
            choice = 3
        else:
            choice = randint(0,1)
            
        if choice == 0:
            for row in range(rows):
                r = [-1] * cols
                self.world_data.append(r)
            with open("assets/levels/001/grassland_ground.csv", newline="") as csvfile:
                reader = csv.reader(csvfile, delimiter= ",")
                for x, row in enumerate(reader):
                    for y, tile in enumerate(row):
                        self.world_data[x][y]= int(tile)
            
            for row in range(rows):
                r = [-1] * cols
                self.world_mobs_data.append(r)
            with open("assets/levels/001/grassland_mobs.csv", newline="") as csvfile:
                reader = csv.reader(csvfile, delimiter= ",")
                for x, row in enumerate(reader):
                    for y, tile in enumerate(row):
                        self.world_mobs_data[x][y]= int(tile)
        
            for row in range(rows):
                r = [-1] * cols
                self.world_objects_data.append(r)
            with open("assets/levels/001/grassland_objects.csv", newline="") as csvfile:
                reader = csv.reader(csvfile, delimiter= ",")
                for x, row in enumerate(reader):
                    for y, tile in enumerate(row):
                        self.world_objects_data[x][y]= int(tile)
            
            for row in range(rows):
                r = [-1] * cols
                self.world_decorations_up.append(r)
            with open("assets/levels/001/grassland_decorationsup.csv", newline="") as csvfile:
                reader = csv.reader(csvfile, delimiter= ",")
                for x, row in enumerate(reader):
                    for y, tile in enumerate(row):
                        self.world_decorations_up[x][y]= int(tile)
            
            for row in range(rows):
                r = [-1] * cols
                self.world_decorations_down.append(r)
            with open("assets/levels/001/grassland_decorationsdown.csv", newline="") as csvfile:
                reader = csv.reader(csvfile, delimiter= ",")
                for x, row in enumerate(reader):
                    for y, tile in enumerate(row):
                        self.world_decorations_down[x][y]= int(tile)
        
        elif choice == 1:
            for row in range(rows):
                r = [-1] * cols
                self.world_data.append(r)
            with open("assets/levels/002/grassland_ground.csv", newline="") as csvfile:
                reader = csv.reader(csvfile, delimiter= ",")
                for x, row in enumerate(reader):
                    for y, tile in enumerate(row):
                        self.world_data[x][y]= int(tile)
            
            for row in range(rows):
                r = [-1] * cols
                self.world_mobs_data.append(r)
            with open("assets/levels/002/grassland_mobs.csv", newline="") as csvfile:
                reader = csv.reader(csvfile, delimiter= ",")
                for x, row in enumerate(reader):
                    for y, tile in enumerate(row):
                        self.world_mobs_data[x][y]= int(tile)
        
            for row in range(rows):
                r = [-1] * cols
                self.world_objects_data.append(r)
            with open("assets/levels/002/grassland_objects.csv", newline="") as csvfile:
                reader = csv.reader(csvfile, delimiter= ",")
                for x, row in enumerate(reader):
                    for y, tile in enumerate(row):
                        self.world_objects_data[x][y]= int(tile)
            
            for row in range(rows):
                r = [-1] * cols
                self.world_decorations_up.append(r)
            with open("assets/levels/002/grassland_decorationsup.csv", newline="") as csvfile:
                reader = csv.reader(csvfile, delimiter= ",")
                for x, row in enumerate(reader):
                    for y, tile in enumerate(row):
                        self.world_decorations_up[x][y]= int(tile)
            
            for row in range(rows):
                r = [-1] * cols
                self.world_decorations_down.append(r)
            with open("assets/levels/002/grassland_decorationsdown.csv", newline="") as csvfile:
                reader = csv.reader(csvfile, delimiter= ",")
                for x, row in enumerate(reader):
                    for y, tile in enumerate(row):
                        self.world_decorations_down[x][y]= int(tile)
                        
        elif choice == 3:
            for row in range(rows):
                r = [-1] * cols
                self.world_data.append(r)
            with open("assets/levels/druid/grassland_ground.csv", newline="") as csvfile:
                reader = csv.reader(csvfile, delimiter= ",")
                for x, row in enumerate(reader):
                    for y, tile in enumerate(row):
                        self.world_data[x][y]= int(tile)
            
            for row in range(rows):
                r = [-1] * cols
                self.world_mobs_data.append(r)
            with open("assets/levels/druid/grassland_mobs.csv", newline="") as csvfile:
                reader = csv.reader(csvfile, delimiter= ",")
                for x, row in enumerate(reader):
                    for y, tile in enumerate(row):
                        self.world_mobs_data[x][y]= int(tile)
        
            for row in range(rows):
                r = [-1] * cols
                self.world_objects_data.append(r)
            with open("assets/levels/druid/grassland_objects.csv", newline="") as csvfile:
                reader = csv.reader(csvfile, delimiter= ",")
                for x, row in enumerate(reader):
                    for y, tile in enumerate(row):
                        self.world_objects_data[x][y]= int(tile)
            
            for row in range(rows):
                r = [-1] * cols
                self.world_decorations_up.append(r)
            with open("assets/levels/druid/grassland_decorationsup.csv", newline="") as csvfile:
                reader = csv.reader(csvfile, delimiter= ",")
                for x, row in enumerate(reader):
                    for y, tile in enumerate(row):
                        self.world_decorations_up[x][y]= int(tile)
            
            for row in range(rows):
                r = [-1] * cols
                self.world_decorations_down.append(r)
            with open("assets/levels/druid/grassland_decorationsdown.csv", newline="") as csvfile:
                reader = csv.reader(csvfile, delimiter= ",")
                for x, row in enumerate(reader):
                    for y, tile in enumerate(row):
                        self.world_decorations_down[x][y]= int(tile)
        
    
    def process_date(self, data, type):
        self.level_lenght = len(data)
        # iterate throught each value in level data file
        for y, row in enumerate(data):
             for x, tile in enumerate(row):

                if type == 'grassland':
                # add image date to main tiles list
                    if tile >= 0:
                        if tile == 82:
                            image = self.assets[type][0]
                            image_rect = image.get_rect()
                            image_x = x * scripts.constants.TILE_SIZE 
                            image_y = y * scripts.constants.TILE_SIZE 
                            image_rect.x= image_x
                            image_rect.y= image_y       
                            tile_data = [image, image_rect, image_x, image_y]
                            self.map_tiles.append(tile_data)
                        if tile == 83:
                            image = self.assets[type][1]
                            image_rect = image.get_rect()
                            image_x = x * scripts.constants.TILE_SIZE 
                            image_y = y * scripts.constants.TILE_SIZE 
                            image_rect.x= image_x
                            image_rect.y= image_y       
                            tile_data = [image, image_rect, image_x, image_y]
                            self.map_tiles.append(tile_data)
                        if tile == 84:
                            image = self.assets[type][2]
                            image_rect = image.get_rect()
                            image_x = x * scripts.constants.TILE_SIZE 
                            image_y = y * scripts.constants.TILE_SIZE 
                            image_rect.x= image_x
                            image_rect.y= image_y       
                            tile_data = [image, image_rect, image_x, image_y]
                            self.map_tiles.append(tile_data)
                        if tile == 72:
                            image = self.assets[type][3]
                            image_rect = image.get_rect()
                            image_x = x * scripts.constants.TILE_SIZE 
                            image_y = y * scripts.constants.TILE_SIZE 
                            image_rect.x= image_x
                            image_rect.y= image_y       
                            tile_data = [image, image_rect, image_x, image_y]
                            self.map_tiles.append(tile_data)
                        if tile == 73:
                            image = self.assets[type][4]
                            image_rect = image.get_rect()
                            image_x = x * scripts.constants.TILE_SIZE 
                            image_y = y * scripts.constants.TILE_SIZE 
                            image_rect.x= image_x
                            image_rect.y= image_y       
                            tile_data = [image, image_rect, image_x, image_y]
                            self.map_tiles.append(tile_data)
                            self.obstacle_tile.append(tile_data)
                        if tile == 74:
                            image = self.assets[type][5]
                            image_rect = image.get_rect()
                            image_x = x * scripts.constants.TILE_SIZE 
                            image_y = y * scripts.constants.TILE_SIZE 
                            image_rect.x= image_x
                            image_rect.y= image_y       
                            tile_data = [image, image_rect, image_x, image_y]
                            self.map_tiles.append(tile_data)
                            self.obstacle_tile.append(tile_data)
                        if tile == 92:
                            image = self.assets[type][6]
                            image_rect = image.get_rect()
                            image_x = x * scripts.constants.TILE_SIZE 
                            image_y = y * scripts.constants.TILE_SIZE 
                            image_rect.x= image_x
                            image_rect.y= image_y       
                            tile_data = [image, image_rect, image_x, image_y]
                            self.map_tiles.append(tile_data)
                            self.obstacle_tile.append(tile_data)
                        if tile == 93:
                            image = self.assets[type][7]
                            image_rect = image.get_rect()
                            image_x = x * scripts.constants.TILE_SIZE 
                            image_y = y * scripts.constants.TILE_SIZE 
                            image_rect.x= image_x
                            image_rect.y= image_y       
                            tile_data = [image, image_rect, image_x, image_y]
                            self.map_tiles.append(tile_data)
                            self.obstacle_tile.append(tile_data)
                        if tile == 94:
                            image = self.assets[type][8]
                            image_rect = image.get_rect()
                            image_x = x * scripts.constants.TILE_SIZE 
                            image_y = y * scripts.constants.TILE_SIZE 
                            image_rect.x= image_x
                            image_rect.y= image_y       
                            tile_data = [image, image_rect, image_x, image_y]
                            self.map_tiles.append(tile_data)
                            self.obstacle_tile.append(tile_data)
                        if tile == 91:
                            image = self.assets[type][9]
                            image_rect = image.get_rect()
                            image_x = x * scripts.constants.TILE_SIZE 
                            image_y = y * scripts.constants.TILE_SIZE 
                            image_rect.x= image_x
                            image_rect.y= image_y       
                            tile_data = [image, image_rect, image_x, image_y]
                            self.map_tiles.append(tile_data)
                            self.obstacle_tile.append(tile_data)
                        if tile == 95:
                            image = self.assets[type][10]
                            image_rect = image.get_rect()
                            image_x = x * scripts.constants.TILE_SIZE 
                            image_y = y * scripts.constants.TILE_SIZE 
                            image_rect.x= image_x
                            image_rect.y= image_y       
                            tile_data = [image, image_rect, image_x, image_y]
                            self.map_tiles.append(tile_data)
                            self.obstacle_tile.append(tile_data)
                        if tile == 81:
                            image = self.assets[type][11]
                            image_rect = image.get_rect()
                            image_x = x * scripts.constants.TILE_SIZE 
                            image_y = y * scripts.constants.TILE_SIZE 
                            image_rect.x= image_x
                            image_rect.y= image_y       
                            tile_data = [image, image_rect, image_x, image_y]
                            self.map_tiles.append(tile_data)
                            self.obstacle_tile.append(tile_data)
                        if tile == 71:
                            image = self.assets[type][12]
                            image_rect = image.get_rect()
                            image_x = x * scripts.constants.TILE_SIZE 
                            image_y = y * scripts.constants.TILE_SIZE 
                            image_rect.x= image_x
                            image_rect.y= image_y       
                            tile_data = [image, image_rect, image_x, image_y]
                            self.map_tiles.append(tile_data)
                            self.obstacle_tile.append(tile_data)
                        if tile == 61:
                            image = self.assets[type][13]
                            image_rect = image.get_rect()
                            image_x = x * scripts.constants.TILE_SIZE 
                            image_y = y * scripts.constants.TILE_SIZE 
                            image_rect.x= image_x
                            image_rect.y= image_y       
                            tile_data = [image, image_rect, image_x, image_y]
                            self.map_tiles.append(tile_data)
                            self.obstacle_tile.append(tile_data)
                        if tile == 41:
                            image = self.assets[type][14]
                            image_rect = image.get_rect()
                            image_x = x * scripts.constants.TILE_SIZE 
                            image_y = y * scripts.constants.TILE_SIZE 
                            image_rect.x= image_x
                            image_rect.y= image_y       
                            tile_data = [image, image_rect, image_x, image_y]
                            self.map_tiles.append(tile_data)
                            self.obstacle_tile.append(tile_data)
                        if tile == 31:
                            image = self.assets[type][15]
                            image_rect = image.get_rect()
                            image_x = x * scripts.constants.TILE_SIZE 
                            image_y = y * scripts.constants.TILE_SIZE 
                            image_rect.x= image_x
                            image_rect.y= image_y       
                            tile_data = [image, image_rect, image_x, image_y]
                            self.map_tiles.append(tile_data)
                            self.obstacle_tile.append(tile_data)
                        if tile == 75:
                            image = self.assets[type][16]
                            image_rect = image.get_rect()
                            image_x = x * scripts.constants.TILE_SIZE 
                            image_y = y * scripts.constants.TILE_SIZE 
                            image_rect.x= image_x
                            image_rect.y= image_y       
                            tile_data = [image, image_rect, image_x, image_y]
                            self.map_tiles.append(tile_data)
                            self.obstacle_tile.append(tile_data)
                        if tile == 65:
                            image = self.assets[type][17]
                            image_rect = image.get_rect()
                            image_x = x * scripts.constants.TILE_SIZE 
                            image_y = y * scripts.constants.TILE_SIZE 
                            image_rect.x= image_x
                            image_rect.y= image_y       
                            tile_data = [image, image_rect, image_x, image_y]
                            self.map_tiles.append(tile_data)
                            self.obstacle_tile.append(tile_data)
                        if tile == 45:
                            image = self.assets[type][18]
                            image_rect = image.get_rect()
                            image_x = x * scripts.constants.TILE_SIZE 
                            image_y = y * scripts.constants.TILE_SIZE 
                            image_rect.x= image_x
                            image_rect.y= image_y       
                            tile_data = [image, image_rect, image_x, image_y]
                            self.map_tiles.append(tile_data)
                            self.obstacle_tile.append(tile_data)
                        if tile == 35:
                            image = self.assets[type][19]
                            image_rect = image.get_rect()
                            image_x = x * scripts.constants.TILE_SIZE 
                            image_y = y * scripts.constants.TILE_SIZE 
                            image_rect.x= image_x
                            image_rect.y= image_y       
                            tile_data = [image, image_rect, image_x, image_y]
                            self.map_tiles.append(tile_data)
                            self.obstacle_tile.append(tile_data)
                        if tile == 22:
                            image = self.assets[type][20]
                            image_rect = image.get_rect()
                            image_x = x * scripts.constants.TILE_SIZE 
                            image_y = y * scripts.constants.TILE_SIZE 
                            image_rect.x= image_x
                            image_rect.y= image_y       
                            tile_data = [image, image_rect, image_x, image_y]
                            self.map_tiles.append(tile_data)
                            self.obstacle_tile.append(tile_data)
                        if tile == 23:
                            image = self.assets[type][21]
                            image_rect = image.get_rect()
                            image_x = x * scripts.constants.TILE_SIZE 
                            image_y = y * scripts.constants.TILE_SIZE 
                            image_rect.x= image_x
                            image_rect.y= image_y       
                            tile_data = [image, image_rect, image_x, image_y]
                            self.map_tiles.append(tile_data)
                            self.obstacle_tile.append(tile_data)
                        if tile == 24:
                            image = self.assets[type][22]
                            image_rect = image.get_rect()
                            image_x = x * scripts.constants.TILE_SIZE 
                            image_y = y * scripts.constants.TILE_SIZE 
                            image_rect.x= image_x
                            image_rect.y= image_y       
                            tile_data = [image, image_rect, image_x, image_y]
                            self.map_tiles.append(tile_data)
                            self.obstacle_tile.append(tile_data)
                        if tile == 0:
                            self.objects.append(Chest(x * scripts.constants.TILE_SIZE, y * scripts.constants.TILE_SIZE, closed_chest_img = self.assets[type][23], opened_chest_img = self.assets[type][24]))
                        if tile == 2:
                            image = self.assets[type][25]
                            image_rect = image.get_rect()
                            image_x = x * scripts.constants.TILE_SIZE 
                            image_y = y * scripts.constants.TILE_SIZE 
                            image_rect.x= image_x
                            image_rect.y= image_y       
                            tile_data = [image, image_rect, image_x, image_y]
                            self.map_tiles.append(tile_data)
                            self.obstacle_tile.append(tile_data)
                        if tile == 3:
                            image = self.assets[type][26]
                            image_rect = image.get_rect()
                            image_x = x * scripts.constants.TILE_SIZE 
                            image_y = y * scripts.constants.TILE_SIZE 
                            image_rect.x= image_x
                            image_rect.y= image_y       
                            tile_data = [image, image_rect, image_x, image_y]
                            self.map_tiles.append(tile_data)
                            self.obstacle_tile.append(tile_data)
                        if tile == 10:
                            image = self.assets[type][27]
                            image_rect = image.get_rect()
                            image_x = x * scripts.constants.TILE_SIZE 
                            image_y = y * scripts.constants.TILE_SIZE 
                            image_rect.x= image_x
                            image_rect.y= image_y       
                            tile_data = [image, image_rect, image_x, image_y]
                            self.map_tiles.append(tile_data)
                            self.obstacle_tile.append(tile_data)
                        if tile == 11:
                            image = self.assets[type][28]
                            image_rect = image.get_rect()
                            image_x = x * scripts.constants.TILE_SIZE 
                            image_y = y * scripts.constants.TILE_SIZE 
                            image_rect.x= image_x
                            image_rect.y= image_y       
                            tile_data = [image, image_rect, image_x, image_y]
                            self.map_tiles.append(tile_data)
                            self.obstacle_tile.append(tile_data)
                        if tile == 12:
                            image = self.assets[type][29]
                            image_rect = image.get_rect()
                            image_x = x * scripts.constants.TILE_SIZE 
                            image_y = y * scripts.constants.TILE_SIZE 
                            image_rect.x= image_x
                            image_rect.y= image_y       
                            tile_data = [image, image_rect, image_x, image_y]
                            self.map_tiles.append(tile_data)
                            self.obstacle_tile.append(tile_data)
                        if tile == 13:
                            image = self.assets[type][30]
                            image_rect = image.get_rect()
                            image_x = x * scripts.constants.TILE_SIZE 
                            image_y = y * scripts.constants.TILE_SIZE 
                            image_rect.x= image_x
                            image_rect.y= image_y       
                            tile_data = [image, image_rect, image_x, image_y]
                            self.map_tiles.append(tile_data)
                            self.obstacle_tile.append(tile_data)
                        if tile == 20:
                            image = self.assets[type][31]
                            image_rect = image.get_rect()
                            image_x = x * scripts.constants.TILE_SIZE 
                            image_y = y * scripts.constants.TILE_SIZE 
                            image_rect.x= image_x
                            image_rect.y= image_y       
                            tile_data = [image, image_rect, image_x, image_y]
                            self.map_tiles.append(tile_data)
                            self.decorations_up_tiles.append(tile_data)
                        if tile == 21:
                            image = self.assets[type][32]
                            image_rect = image.get_rect()
                            image_x = x * scripts.constants.TILE_SIZE 
                            image_y = y * scripts.constants.TILE_SIZE 
                            image_rect.x= image_x
                            image_rect.y= image_y       
                            tile_data = [image, image_rect, image_x, image_y]
                            self.map_tiles.append(tile_data)
                        if tile == 25:
                            image = self.assets[type][33]
                            image_rect = image.get_rect()
                            image_x = x * scripts.constants.TILE_SIZE 
                            image_y = y * scripts.constants.TILE_SIZE 
                            image_rect.x= image_x
                            image_rect.y= image_y       
                            tile_data = [image, image_rect, image_x, image_y]
                            self.map_tiles.append(tile_data)
                        if tile == 30:
                            image = self.assets[type][34]
                            image_rect = image.get_rect()
                            image_x = x * scripts.constants.TILE_SIZE 
                            image_y = y * scripts.constants.TILE_SIZE 
                            image_rect.x= image_x
                            image_rect.y= image_y       
                            tile_data = [image, image_rect, image_x, image_y]
                            self.gate_tiles.append(tile_data) 
                        if tile == 96:
                            image = self.assets[type][35]
                            image_rect = image.get_rect()
                            image_x = x * scripts.constants.TILE_SIZE 
                            image_y = y * scripts.constants.TILE_SIZE 
                            image_rect.x= image_x
                            image_rect.y= image_y       
                            tile_data = [image, image_rect, image_x, image_y]
                            self.map_tiles.append(tile_data)
                            self.obstacle_tile.append(tile_data)
                        if tile == 85:
                            image = self.assets[type][49]
                            image_rect = image.get_rect()
                            image_x = x * scripts.constants.TILE_SIZE 
                            image_y = y * scripts.constants.TILE_SIZE 
                            image_rect.x= image_x
                            image_rect.y= image_y       
                            tile_data = [image, image_rect, image_x, image_y]
                            self.map_tiles.append(tile_data)
                            self.obstacle_tile.append(tile_data)
                        if tile == 97:
                            image = self.assets[type][36]
                            image_rect = image.get_rect()
                            image_x = x * scripts.constants.TILE_SIZE 
                            image_y = y * scripts.constants.TILE_SIZE 
                            image_rect.x= image_x
                            image_rect.y= image_y       
                            tile_data = [image, image_rect, image_x, image_y]
                            self.map_tiles.append(tile_data)
                            self.obstacle_tile.append(tile_data)
                        if tile == 98:
                            image = self.assets[type][37]
                            image_rect = image.get_rect()
                            image_x = x * scripts.constants.TILE_SIZE 
                            image_y = y * scripts.constants.TILE_SIZE 
                            image_rect.x= image_x
                            image_rect.y= image_y       
                            tile_data = [image, image_rect, image_x, image_y]
                            self.map_tiles.append(tile_data)
                            self.obstacle_tile.append(tile_data)
                        if tile == 90:
                            image = self.assets[type][38]
                            image_rect = image.get_rect()
                            image_x = x * scripts.constants.TILE_SIZE 
                            image_y = y * scripts.constants.TILE_SIZE 
                            image_rect.x= image_x
                            image_rect.y= image_y       
                            tile_data = [image, image_rect, image_x, image_y]
                            self.map_tiles.append(tile_data)
                            self.obstacle_tile.append(tile_data)
                        if tile == 80:
                            image = self.assets[type][39]
                            image_rect = image.get_rect()
                            image_x = x * scripts.constants.TILE_SIZE 
                            image_y = y * scripts.constants.TILE_SIZE 
                            image_rect.x= image_x
                            image_rect.y= image_y       
                            tile_data = [image, image_rect, image_x, image_y]
                            self.map_tiles.append(tile_data)
                            self.decorations_up_tiles.append(tile_data)
                        if tile == 70:
                            image = self.assets[type][40]
                            image_rect = image.get_rect()
                            image_x = x * scripts.constants.TILE_SIZE 
                            image_y = y * scripts.constants.TILE_SIZE 
                            image_rect.x= image_x
                            image_rect.y= image_y       
                            tile_data = [image, image_rect, image_x, image_y]
                            self.map_tiles.append(tile_data)
                            self.decorations_up_tiles.append(tile_data)
                        if tile == 40:
                            image = None
                            image_rect = None
                            image_x = x * scripts.constants.TILE_SIZE 
                            image_y = y * scripts.constants.TILE_SIZE        
                            tile_data = [image, image_rect, image_x, image_y]
                            self.player = Character(tile_data[2],tile_data[3],scripts.constants.PLAYER_HP,scripts.constants.HERO)
                               
                        if tile == 50:
                            image = None
                            image_rect = None
                            image_x = x * scripts.constants.TILE_SIZE 
                            image_y = y * scripts.constants.TILE_SIZE        
                            tile_data = [image, image_rect, image_x, image_y]
                            self.character_list.append(Slime(tile_data[2],tile_data[3],scripts.constants.SLIME_HP))
                        if tile == 60:
                            image = None
                            image_rect = None
                            image_x = x * scripts.constants.TILE_SIZE 
                            image_y = y * scripts.constants.TILE_SIZE        
                            tile_data = [image, image_rect, image_x, image_y]
                            self.character_list.append(Wolf(tile_data[2],tile_data[3],scripts.constants.WOLF_HP))
                        if tile == 51:
                            image = None
                            image_rect = None
                            image_x = x * scripts.constants.TILE_SIZE 
                            image_y = y * scripts.constants.TILE_SIZE        
                            tile_data = [image, image_rect, image_x, image_y]
                            self.character_list.append(Troll(tile_data[2],tile_data[3],scripts.constants.TROLL_HP))
                        if tile == 52:
                            image = None
                            image_rect = None
                            image_x = x * scripts.constants.TILE_SIZE 
                            image_y = y * scripts.constants.TILE_SIZE        
                            tile_data = [image, image_rect, image_x, image_y]
                            self.character_list.append(Goblin(tile_data[2],tile_data[3],scripts.constants.GOBLIN_HP))
                        if tile == 53:
                            image = None
                            image_rect = None
                            image_x = x * scripts.constants.TILE_SIZE 
                            image_y = y * scripts.constants.TILE_SIZE        
                            tile_data = [image, image_rect, image_x, image_y]
                            self.character_list.append(Ent(tile_data[2],tile_data[3],scripts.constants.ENT_HP))
                        if tile == 54:
                            image = None
                            image_rect = None
                            image_x = x * scripts.constants.TILE_SIZE 
                            image_y = y * scripts.constants.TILE_SIZE        
                            tile_data = [image, image_rect, image_x, image_y]
                            self.character_list.append(SlimeFireWizard(tile_data[2],tile_data[3],scripts.constants.SLIME_FIRE_WIZARD_HP))
                        if tile == 55:
                            image = None
                            image_rect = None
                            image_x = x * scripts.constants.TILE_SIZE 
                            image_y = y * scripts.constants.TILE_SIZE        
                            tile_data = [image, image_rect, image_x, image_y]
                            self.character_list.append(Druid(tile_data[2],tile_data[3],scripts.constants.DRUID_HP))
        
 
        return self.player, self.character_list, self.boss_list, self.gate_tiles
        
    def generate(self, mobs = False):  
        pass
    
    def update(self, screen_scroll):
        for tile in self.map_tiles:
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
    
    def draw_src(self,surface, source):
        for tile in source:
            surface.blit(tile[0], tile[1])

    def new_level(self, player):
        return player.health, player.health_max, player.gold
    
    def check_if_new_level(self, exit_tiles, player):
        for exit_tile in exit_tiles:
            if exit_tile[1].colliderect(player.rect):
                return True
        return False

                

                