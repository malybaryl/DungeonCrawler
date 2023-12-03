import pygame

class DamageText(pygame.sprite.Sprite):
    def __init__(self,x,y, damage, color):
        pygame.sprite.Sprite.__init__(self)
        self.font = pygame.font.Font("assets/fonts/font.ttf",8)
        self.image = self.font.render(damage, True, color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.counter = 0

    def update(self):
        # move damage text up
        self.rect.y -= 1
        # delete the counter after few seconds
        self.counter += 1
        if self.counter > 30:
            self.kill()     