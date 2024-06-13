from scripts.load import loadImages, loadImage
import scripts.constants
import pygame


class Bg():
    def __init__(self):
        self.assets ={
        'lavaland': self.load_lavaland_images(),
        'image_lavaland_1': loadImage('tilemap/lavaland/33.png'),
        'image_lavaland_2': loadImage('tilemap/lavaland/40.png'),
        'image_lavaland_3': loadImage('tilemap/lavaland/50.png'),
        'image_lavaland_4': loadImage('tilemap/lavaland/60.png')
        }
        self.time = pygame.time.get_ticks()
        self.world_level = 0
           
    
    def load_lavaland_images(self):
        array = []
        x = -48
        y = -48
        cols = scripts.constants.DISPLAY_WIDTH // 32
        rows = scripts.constants.DISPLAY_HEIGHT // 32
        type = 0
        
        while x < cols*32:
            x += 32 
            while y < rows*32:
                y += 32
                if type == 0:
                    array.append([loadImage('tilemap/lavaland/33.png'), type, x, y])
                elif type == 1:
                    array.append([loadImage('tilemap/lavaland/40.png'), type, x, y])
                elif type == 2:
                    array.append([loadImage('tilemap/lavaland/50.png'), type, x, y])
                elif type == 3:
                    array.append([loadImage('tilemap/lavaland/60.png'), type, x, y])
                type += 1
                if type > 3:
                    type = 0
            y = -48
        
        return array
    
    
    def refresh_world_level(self, world_level):
        self.world_level = world_level
        
        
    def update(self):
        if self.world_level > 3:
            if pygame.time.get_ticks() - self.time >= 500:
                for tile in self.assets['lavaland']:
                    if tile[1] == 0:
                        tile[0] = self.assets['image_lavaland_4'] 
                    elif tile[1] == 1:
                        tile[0] = self.assets['image_lavaland_3']                 
                    elif tile[1] == 2:
                        tile[0] = self.assets['image_lavaland_2']              
                    elif tile[1] == 3:
                        tile[0] = self.assets['image_lavaland_1']                
                    
                    tile[1] += 1
                    if tile[1] > 3:
                        tile[1] = 0
                self.time = pygame.time.get_ticks()

    def draw(self, surface):
        surface.fill(scripts.constants.BG)
        
        if self.world_level > 3:
            for tile in self.assets['lavaland']:
                surface.blit(tile[0],(tile[2],tile[3]))
        

