import pygame

class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, scale):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 10
        self.direction = direction
        self.images = [] # 1D frame list
        for num in range(0, 3):
            img = pygame.image.load("assets/img/slash/slash" + str(num) + ".png").convert_alpha()
            img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
            self.images.append(img)
        self.frame_index = 0
        self.flip = False
        self.image = self.images[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.counter = 0

    def update(self, screen_scroll, SCREEN_WIDTH):
        SLASH_SPEED = 4
        # update explosion amimation
        self.counter += 1

        if self.counter >= SLASH_SPEED:
            x = self.rect.centerx
            y = self.rect.bottom
            self.counter = 0
            self.frame_index += 1
            # if the animation is complete then keep the last frame
            if self.frame_index >= len(self.images):
                self.frame_index = len(self.images) - 1
            else:
                self.image = self.images[self.frame_index]
                self.rect = self.image.get_rect()
                self.rect.centerx = x
                self.rect.bottom = y
        # move bullet
        self.rect.x += (self.direction * self.speed) + screen_scroll
        # check if bullet has gone off screen
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()