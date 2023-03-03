import pygame

class Cannonball(pygame.sprite.Sprite):

    def __init__(self, scale):
        super().__init__()
        self.image = pygame.image.load('assets/img/enemy/cannon/cannonball.png')
        self.image = pygame.transform.scale(self.image,
                                            (int(self.image.get_width() * scale), int(self.image.get_height() * scale)))
        self.rect = self.image.get_rect()
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.rect.x = 0 #position de départ pas importante
        self.rect.y = 0
        self.dx = 0
        self.dy = 0
        self.xi = self.rect.x
        self.yi = self.rect.y
        self.t = 0