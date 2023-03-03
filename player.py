import pygame, os, random

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, scale):
        pygame.sprite.Sprite.__init__(self)
        self.invincible = False
        self.health = 100
        self.max_health = 100
        self.xp = 0
        self.xp_level = 1
        self.alive = True
        self.attack_damage = 50
        self.projectile_damage = 20
        self.attacking = False
        self.shooting = False
        self.ammo = 10
        self.dx = 0
        self.dy = 0
        self.vy = 0
        self.gravity = 0.75 # value used for smooth animation
        self.direction = 1 # 1 if right-oriented, -1 if left-oriented
        self.jump = False
        self.in_air = False
        self.resistance = 0  # vecteur de resistance
        self.nbr_jump = 0
        self.n_jump_max = 2 #allows the player to perform a double jump while in-aire
        self.speed = 5
        self.collide_any_platform = False
        self.attack_cooldown = 0
        self.shoot_cooldown = 0
        self.flip = False
        self.correction = False #position correction in attack animation
        self.animation_list = [] #2D list of frame, 1st Dimension is Action
        self.sound_list = [] #2D list of sounds, 1st Dimension is Action
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()

        # load all images for the player
        animation_types = ["Idle", "Run", "Jump", "Death", "Attack", "Hurt"]
        for animation in animation_types:
            # reset temporary list of images
            temp_list = []
            # count number of files in the folder
            num_of_frames = len(os.listdir("assets/img/player/" + animation ))
            for i in range(num_of_frames):
                img = pygame.image.load("assets/img/player/" + animation + "/" + str(i) +".png").convert_alpha()
                img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                temp_list.append(img)
            self.animation_list.append(temp_list)

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        #load all sounds for the player
        sound_types = ["Run", "Jump", "Death", "Attack", "Hurt"]
        for sound_type in sound_types:
            # reset temporary list of sounds
            temp_list = []
            # count number of files in the folder
            num_of_sounds = len(os.listdir("assets/audio/player/" + sound_type))
            for i in range(num_of_sounds):
                sound = pygame.mixer.Sound("assets/audio/player/" + sound_type + "/" + str(i) + ".mp3")
                sound.set_volume(0.2)
                temp_list.append(sound)
            self.sound_list.append(temp_list)

    def update_volume(self, volume):
        for action in self.sound_list:
            for sound in action:
                sound.set_volume(volume)

    def update(self):
        self.update_animation()
        self.check_alive()
        # update cooldown
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

    def move(self, moving_left, moving_right):
        # reset movement variables
        self.dx = 0
        self.dy = 0

        # assign movement variables if moving left or right
        if moving_left:
            self.dx = -self.speed
            self.flip = True
            self.direction = -1
        if moving_right:
            self.dx = self.speed
            self.flip = False
            self.direction = 1

        # jump
        if self.jump:
            if not self.in_air or self.nbr_jump < self.n_jump_max:
                self.vy = -11
                self.nbr_jump += 1
                self.jump = False
                self.in_air = True

        #update xp
        xp_level = self.xp //100
        if xp_level > self.xp_level:
            n_level = xp_level - self.xp_level
            self.xp_level = xp_level
            self.attack_damage += n_level * 25
            self.projectile_damage += n_level * 25
            self.max_health += n_level * 30
            self.health += n_level * 30


    def attack(self):
        if self.attack_cooldown == 0:
            self.attack_cooldown = 20
            self.attacking = True

    def shoot(self):
        if self.shooting and self.shoot_cooldown == 0 and self.ammo > 0:
            self.shoot_cooldown = 20
            # reduce ammo
            self.ammo -= 1
            self.shooting = False
            return True

    def update_animation(self):
        # update animation
        ANIMATION_COOLDOWN = 100
        # saves the position if there is an attack or death animation in left direction
        right = self.rect.right
        bottom = self.rect.bottom
        # if a hurt animation has been displayed while on ground
        if self.action == 5 and self.frame_index == 1 and not self.in_air:
            self.update_action(0)
        # if the player is hurt while in air
        if self.action == 5 and self.in_air:
            self.frame_index = 1
        # update image depending on current frame
        self.image = self.animation_list[self.action][self.frame_index]
        # changes the position if there is an attack or death animation in left direction
        if self.direction < 0:
            self.rect.width = self.image.get_width()
            self.rect.right = right
        if self.action == 3 or self.action == 4: #if it's death or attack animation
            self.rect.height = self.image.get_height()
            self.rect.y = bottom - self.rect.height
        # check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        # if the animation has run out the reset back to the start
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 3:
                self.frame_index = len(self.animation_list[self.action]) - 1
            elif self.action == 4:
                self.update_action(0)
                self.attacking = False
            elif self.action == 5: # if the player was hurt while jumping
                self.update_action(2)
            else:
                self.frame_index = 0

    def update_action(self, new_action):
        # check if the new action is different to the previous one
        if new_action != self.action:
            self.action = new_action
            # update the animation settings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()
            if self.action != 0 and len(self.sound_list[self.action-1]) != 0: #if a sound exists for this action
                n_sound = random.randrange(len(self.sound_list[self.action-1]))
                sound = self.sound_list[self.action-1][n_sound]
                sound.play()

    def check_alive(self):
        if self.health <= 0:
            self.health = 0
            self.jump = False
            self.alive = False
            self.update_action(3)