import pygame

class HealthBar():
    def __init__(self, x, y, max_hp):
        self.x = x
        self.y = y
        self.max_hp = max_hp


    def draw(self, hp, screen):
        #calculate health ratio
        ratio = hp / self.max_hp
        pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y, 150, 20))
        pygame.draw.rect(screen, (0, 255, 0), (self.x, self.y, 150 * ratio, 20))
