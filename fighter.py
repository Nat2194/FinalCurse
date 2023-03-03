import pygame, random, os, shelve
from damagetext import DamageText

#fighter class
class Fighter():
    def __init__(self, x, y, name, hp, max_hp, strength, potions, scale, save):
        self.name = name
        # load player data
        shelfFile = shelve.open('data/saves/save' + str(save))
        level = shelfFile['Level']
        shelfFile.close()
        if self.name == "player":
            self.path = "assets/turnbyturn/img/player/"
        elif self.name == "player2":
            self.path = "assets/turnbyturn/img/player2/"
        elif self.name == "player3":
            self.path = "assets/turnbyturn/img/player3/"
        else:
            self.path = "assets/turnbyturn/img/enemy/level" + str(level) + "/" + self.name + "/"
        self.save = save
        self.hp = hp
        self.max_hp = max_hp
        self.xp = 0
        self.xp_level = self.xp// 100
        self.strength = strength
        self.start_potions = potions
        self.potions = potions
        self.alive = True
        self.casting_spell = False
        self.animation_list = [] #2D list of frame, 1st Dimension is Action
        self.frame_index = 0
        self.action = 0 #0:idle, 1:attack, 2:hurt, 3:dead
        self.update_time = pygame.time.get_ticks()
        # load all images for the player
        animation_types = ["Idle", "Attack1", "Attack2", "Hurt", "Death"]
        for animation in animation_types:
            # reset temporary list of images
            temp_list = []
            # count number of files in the folder
            num_of_frames = len(os.listdir(self.path + animation))
            for i in range(num_of_frames):
                img = pygame.image.load(self.path + animation + "/" + str(i) + ".png").convert_alpha()
                img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                temp_list.append(img)
            self.animation_list.append(temp_list)
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        #load player data
        if self.name == "player":
            # load player data
            shelfFile = shelve.open('data/saves/save' + str(save))
            self.hp = shelfFile['PlayerHealth']
            self.max_hp = shelfFile['PlayerMaxHealth']
            self.strength = shelfFile['PlayerAttack']
            self.xp = shelfFile['PlayerXP']
            self.xp_level = shelfFile['PlayerLevelXP']
            shelfFile.close()
        elif self.name == "player2" or self.name == "player3":
            # load player data
            shelfFile = shelve.open('data/saves/save' + str(save))
            self.hp = shelfFile['PlayerMaxHealth']
            self.max_hp = shelfFile['PlayerMaxHealth']
            self.strength = shelfFile['PlayerAttack']
            shelfFile.close()



    def update(self):
        animation_cooldown = 150
        # update xp
        xp_level = self.xp // 100
        if xp_level > self.xp_level:
            n_level = xp_level - self.xp_level
            self.xp_level = xp_level
            self.strength += 25 * n_level
            self.max_hp += n_level * 30
            self.hp += n_level * 30
        #handle animation
        bottom = self.rect.bottom
        if self.name != "player":
            right = self.rect.right
        # update image depending on current frame
        #update image
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect.height = self.image.get_height()
        self.rect.bottom = bottom
        if self.name != "player":
            self.rect.width = self.image.get_width()
            self.rect.right = right
        #check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        #if the animation has run out then reset back to the start
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 4:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.idle()



    def idle(self):
        #set variables to idle animation
        self.action = 0
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()


    def attack(self, target, damage_text_group):
        #deal damage to enemy
        rand = random.randint(-5, 5)
        damage = self.strength + rand
        target.hp -= damage
        #run enemy hurt animation
        target.hurt()
        #check if target has died
        if target.hp < 1:
            target.hp = 0
            target.alive = False
            target.death()
            xp_amount = random.randint(15, 25)
            self.xp += xp_amount
            damage_text = DamageText(self.rect.centerx, self.rect.y,
                                     str(xp_amount), (0, 150, 255))
            damage_text_group.add(damage_text)
        damage_text = DamageText(target.rect.centerx, target.rect.y, str(damage), (255,0,0))
        damage_text_group.add(damage_text)
        #set variables to attack animation
        self.action = random.randint(1,2)
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        if self.name == "FinalBoss" and self.action == 2:
            self.casting_spell = True

    def hurt(self):
        #set variables to hurt animation
        self.action = 3
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def death(self):
        #set variables to death animation
        self.action = 4
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()


    def reset (self):
        self.alive = True
        self.potions = self.start_potions
        self.hp = self.max_hp
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()
        if self.name == "player":
            # load player data
            shelfFile = shelve.open('data/saves/save' + str(self.save))
            self.hp = shelfFile['PlayerHealth']
            self.max_hp = shelfFile['PlayerMaxHealth']
            self.strength = shelfFile['PlayerAttack']
            self.xp = shelfFile['PlayerXP']
            self.xp_level = shelfFile['PlayerLevelXP']
            shelfFile.close()
        elif self.name == "player2" or self.name == "player3":
            # load player data
            shelfFile = shelve.open('data/saves/save' + str(self.save))
            self.max_hp = shelfFile['PlayerMaxHealth']
            self.strength = shelfFile['PlayerAttack']
            shelfFile.close()


    def draw(self, screen):
        screen.blit(self.image, self.rect)