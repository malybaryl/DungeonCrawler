import pygame
import scripts.constants
from scripts.load import loadImages
from scripts.character import Character
from scripts.enemies import Orc, Orc_Shaman_Boss

def draw_grid(display):
        for x in range(30):
            pygame.draw.line(display, scripts.constants.WHITE, (x*scripts.constants.TILE_SIZE,0), (x*scripts.constants.TILE_SIZE, scripts.constants.SCREEN_HEIGHT))
            pygame.draw.line(display, scripts.constants.WHITE, (0,x*scripts.constants.TILE_SIZE), (scripts.constants.SCREEN_WIDTH, x*scripts.constants.TILE_SIZE))
            

class World():
    def __init__(self):
        self.assets={
            "castle": loadImages("tilemap/castle")
        }
        self.map_tiles = []
        self.obstacle_tile = []
        self.exit_tile = None
        self.player = None
        self.boss_list = []
        self.character_list = []

    def process_date(self, data, type):
        self.level_lenght = len(data)
        # iterate throught each value in level data file
        for y, row in enumerate(data):
             for x, tile in enumerate(row):
                image = self.assets[type][tile]
                image_rect = image.get_rect()
                image_x = x * scripts.constants.TILE_SIZE 
                image_y = y * scripts.constants.TILE_SIZE 
                image_rect.x= image_x
                image_rect.y= image_y       
                tile_data = [image, image_rect, image_x, image_y]

                # add image date to main tiles list
                if tile >= 0:
                    self.map_tiles.append(tile_data)
                if tile == 0 or tile == 1 or tile == 2 or tile == 3 or tile == 4 or tile == 5 or tile == 21 or tile == 22 or tile == 23 or tile == 24 or tile == 27:
                    self.obstacle_tile.append(tile_data) 
                if tile == 26:
                    self.player = Character(tile_data[2],tile_data[3],scripts.constants.PLAYER_HP)
                if tile == 25:
                    self.character_list.append(Orc(tile_data[2],tile_data[3],scripts.constants.ORC_HP))
                if tile == 28:
                    self.boss_list.append(Orc_Shaman_Boss(tile_data[2],tile_data[3],scripts.constants.ORC_SHAMAN_HP))

        return self.player, self.character_list, self.boss_list
                    
    
    def update(self, screen_scroll):
        for tile in self.map_tiles:
            tile[2] += screen_scroll[0]
            tile[3] += screen_scroll[1]
            tile[1].center = (tile[2], tile[3])


    def draw(self,surface):
        for tile in self.map_tiles:
            if tile[0]!=25 or tile[0]!=26:
                surface.blit(tile[0], tile[1])
    