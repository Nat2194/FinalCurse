import pygame, os, random

class SmartestMonster(pygame.sprite.Sprite):

    def __init__(self, x, y, scale):
        super().__init__()
        self.health = 250
        self.max_health = 250
        self.alive = True
        self.death_anim = False
        self.attack_damage = 30
        self.xi = 0
        self.yi = 0
        self.vx = 0
        self.vy = 0
        self.dx = 0
        self.dy = 0
        self.resistance = (0, 0)  # vecteur de resistance
        self.jumping = False
        self.fall = False
        self.t = 0
        self.attack_cooldown = 0
        self.attacking = False
        self.collision_player = False
        self.flip = False
        self.animation_list = [] #2D list of frame, 1st Dimension is Action
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()
        self.death_anim = False  # deletes the monster if False and health <= 0
        self.n_color = random.randrange(0, 4)  # the color of the monster


        # load all images for the players
        animation_types = ["Idle", "Jump", "Death", "Hurt"]
        for animation in animation_types:
            # reset temporary list of images
            temp_list = []
            # count number of files in the folder
            num_of_frames = len(os.listdir("assets/img/enemy/monster/" + animation)) // 4 #there are 4 colors in each folder
            for i in range(num_of_frames):
                img = pygame.image.load(
                    "assets/img/enemy/monster/" + animation + "/" + str(self.n_color) + "_" + str(
                        i) + ".png").convert_alpha()
                img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                temp_list.append(img)
            self.animation_list.append(temp_list)

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.killed_by_player = False  # boolean used to know if a bonus is given to the player


    def update(self):
        self.update_animation()
        self.check_alive()
        # update cooldown
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

    def compute_vy(self, p_x, p_y):
        Dx = (p_x - self.rect.x)
        if -70 < Dx < 70 or Dx > 500 or Dx < -500:
            self.vx = 0
            self.vy = 50
        else:
            if Dx < 0:
                self.vx = -Dx // 10
                self.vx *= -1
            else:
                self.vx = Dx // 10
            self.vy = (-(p_y - self.rect.y) + 4 * (Dx / self.vx) ** 2) * (self.vx / Dx)  # gravity = 8

    def jump_process(self):
        self.dx = self.vx * self.t + self.xi - self.rect.x
        self.dy = 4 * (self.t ** 2) - self.vy * self.t - (self.rect.y - self.yi)

    def attack(self):
        if self.attack_cooldown == 0:
            self.attack_cooldown = 50
            self.attacking = True
            self.update_action(3)
        else:
            self.attacking = False

    def update_animation(self):
        # update animation
        ANIMATION_COOLDOWN = 100
        # saves the position for death animation
        bottom = self.rect.bottom
        # update image depending on current frame
        self.image = self.animation_list[self.action][self.frame_index]
        if self.vx < 0:
            self.flip = True
        else:
            self.flip = False
        if self.action == 2:  # if it's death animation
            self.rect.height = self.image.get_height()
            self.rect.y = bottom - self.rect.height
        # check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        # if the animation has run out the reset back to the start
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 2:
                self.death_anim = False
            elif self.action == 3:
                self.update_action(0)
                self.attacking = False
            else:
                self.frame_index = 0

    def update_action(self, new_action):
        # check if the new action is different to the previous one
        if new_action != self.action:
            self.action = new_action
            # update the animation settings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def check_alive(self):
        if self.health <= 0:
            self.health = 0
            self.jumping = False
            self.attacking = False
            self.vx = 0
            self.alive = False
            self.update_action(2)
            if not self.death_anim:
                self.death_anim = True