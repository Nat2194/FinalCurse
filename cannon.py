import pygame, os
from cannonball import Cannonball

class Cannon(pygame.sprite.Sprite):

    def __init__(self, x, y, scale):
        super().__init__()
        self.attack_damage = 20
        self.vx = 0
        self.vy = 0
        self.dy = 0
        self.resistance = (0, 0)  # vecteur de resistance
        self.fire = False # doing the cannon animation
        self.shoot = False # shooting a cannonball
        self.flip = False #to change sprite orientation
        self.animation_list = [] #2D list of frame, 1st Dimension is Action
        self.scale = scale #scale of the sprite
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()


        # load all images for the players
        animation_types = ["Idle", "Shoot"]
        for animation in animation_types:
            # reset temporary list of images
            temp_list = []
            # count number of files in the folder
            num_of_frames = len(os.listdir("assets/img/enemy/cannon/" + animation))
            for i in range(num_of_frames):
                img = pygame.image.load(
                    "assets/img/enemy/cannon/" + animation + "/" + str(i) + ".png").convert_alpha()
                img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                temp_list.append(img)
            self.animation_list.append(temp_list)

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (x, y)
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def spawn_cannonball(self):
        self.cannonball = Cannonball(self.scale)
        self.cannonball.rect.x = self.rect.x
        self.cannonball.rect.y = self.rect.y
        self.cannonball.xi = self.rect.left
        self.cannonball.yi = self.rect.top
        self.cannonball.t = 0

    def fire_process(self):
        self.cannonball.dx = self.vx * self.cannonball.t + self.cannonball.xi - self.cannonball.rect.x
        self.cannonball.dy = 4 * (self.cannonball.t ** 2) - self.vy * self.cannonball.t - (self.cannonball.rect.y - self.cannonball.yi)

    def update_animation(self):
        # update animation
        ANIMATION_COOLDOWN = 100
        # update image depending on current frame
        self.image = self.animation_list[self.action][self.frame_index]
        if self.vx > 0:
            self.flip = True
        else:
            self.flip = False
        # check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        # if the animation has run out the reset back to the start
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 1:
                self.update_action(0)
                self.fire = False #end of fire animation
                self.shoot = True #shoots a cannonball
                self.spawn_cannonball()
            else:
                self.frame_index = 0

    def update_action(self, new_action):
        # check if the new action is different to the previous one
        if new_action != self.action:
            self.action = new_action
            # update the animation settings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()
