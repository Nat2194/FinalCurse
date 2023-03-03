import pygame, shelve
import random as rand
from decoration import Decoration
from water import Water
from monster import Monster
from smart_monster import SmartMonster
from smartest_monster import SmartestMonster
from cannon import Cannon
from smart_cannon import SmartCannon
from smartest_cannon import SmartestCannon
from player import Player
from item_box import ItemBox
from healthbar import HealthBar
from exit import Exit

class World():
    def __init__(self, SCREEN_HEIGHT, level, save):
        self.save = save
        self.obstacle_list = []
        self.img_list = []
        self.ROWS = 16
        self.COLS = 150
        self.TILE_SIZE = SCREEN_HEIGHT // self.ROWS
        self.TILE_TYPES = 26
        # store tiles in a list
        for x in range(self.TILE_TYPES):
                img = pygame.image.load("assets/img/tile/level" + str(level) + "/" + str(x) + ".png")
                img = pygame.transform.scale(img, (self.TILE_SIZE, self.TILE_SIZE))
                self.img_list.append(img)

        # create sprite groups
        self.monster_group = pygame.sprite.Group()
        self.n_max_monster = 0
        self.cannon_group = pygame.sprite.Group()
        self.n_max_cannon = 0
        self.bullet_group = pygame.sprite.Group()
        self.grenade_group = pygame.sprite.Group()
        self.explosion_group = pygame.sprite.Group()
        self.item_box_group = pygame.sprite.Group()
        self.decoration_group = pygame.sprite.Group()
        self.water_group = pygame.sprite.Group()
        self.exit_group = pygame.sprite.Group()


    def draw_grid(self, data, screen):
        for y, row in enumerate(data):
            for x, tile in enumerate(row):
                pygame.draw.rect(screen,(255,255,255),(x * 40, y * 40, 40, 40), 1)

    def process_data(self, data):
        self.level_length = len(data[0])
        # iterate through each value in level data file
        for y, row in enumerate(data):
            for x, tile in enumerate(row):
                if tile >= 0:
                    img = self.img_list[tile]
                    img_rect = img.get_rect()
                    img_rect.x = x * self.TILE_SIZE
                    img_rect.y = y * self.TILE_SIZE
                    tile_data = (img, img_rect)
                    if tile >= 0 and tile <= 8:
                        self.obstacle_list.append(tile_data)
                    elif tile >= 9 and tile <= 10:
                        water = Water(img, x * self.TILE_SIZE, y * self.TILE_SIZE, self.TILE_SIZE)
                        self.water_group.add(water)
                    elif tile >= 11 and tile <= 14:
                        decoration = Decoration(img, x * self.TILE_SIZE, y * self.TILE_SIZE, self.TILE_SIZE)
                        self.decoration_group.add(decoration)
                    elif tile == 15:  # create player
                        player = Player(x * self.TILE_SIZE, y * self.TILE_SIZE, 1.2)
                        health_bar = HealthBar(10, 10)
                    elif tile == 16:  # create monsters
                        monster = Monster(x * self.TILE_SIZE, y * self.TILE_SIZE, 1.65)
                        self.monster_group.add(monster)
                        self.n_max_monster += 1
                    elif tile == 17:  # create smart monsters
                        smart_monster = SmartMonster(x * self.TILE_SIZE, y * self.TILE_SIZE, 2.65)
                        self.monster_group.add(smart_monster)
                        self.n_max_monster += 1
                    elif tile == 18:  # create smartest monsters
                        smartest_monster = SmartestMonster(x * self.TILE_SIZE, y * self.TILE_SIZE, 3.65)
                        self.monster_group.add(smartest_monster)
                        self.n_max_monster += 1
                    elif tile == 19:  # create cannons
                        cannon = Cannon(x * self.TILE_SIZE, y * self.TILE_SIZE, 0.98)
                        self.cannon_group.add(cannon)
                        self.n_max_cannon += 1
                    elif tile == 20:  # create  smart cannons
                        smart_cannon = SmartCannon(x * self.TILE_SIZE, y * self.TILE_SIZE, 0.98)
                        self.cannon_group.add(smart_cannon)
                        self.n_max_cannon += 1
                    elif tile == 21:  # create  smartest cannons
                        smartest_cannon = SmartestCannon(x * self.TILE_SIZE, y * self.TILE_SIZE, 0.98)
                        self.cannon_group.add(smartest_cannon)
                        self.n_max_cannon += 1
                    elif tile == 22:  # create damage box
                        item_box = ItemBox("Damage", x * self.TILE_SIZE, y * self.TILE_SIZE, self.TILE_SIZE)
                        self.item_box_group.add(item_box)
                    elif tile == 23:  # create ammo box
                        item_box = ItemBox("Ammo", x * self.TILE_SIZE, y * self.TILE_SIZE, self.TILE_SIZE)
                        self.item_box_group.add(item_box)
                    elif tile == 24:  # create health box
                        item_box = ItemBox("Health", x * self.TILE_SIZE, y * self.TILE_SIZE, self.TILE_SIZE)
                        item_box.__init__("Health", x * self.TILE_SIZE, y * self.TILE_SIZE, self.TILE_SIZE)
                        self.item_box_group.add(item_box)
                    elif tile == 25:  # create exit
                        exit = Exit(img, x * self.TILE_SIZE, y * self.TILE_SIZE, self.TILE_SIZE)
                        self.exit_group.add(exit)
        # load player data
        shelfFile = shelve.open('data/saves/save'+str(self.save))
        player.health = shelfFile['PlayerHealth']
        player.max_health = shelfFile['PlayerMaxHealth']
        if shelfFile['PlayerX'] != 0 or shelfFile['PlayerY'] != 0:
            player.rect.x = shelfFile['PlayerX']
            player.rect.y = shelfFile['PlayerY']
        player.attack_damage = shelfFile['PlayerAttack']
        player.projectile_damage = shelfFile['PlayerProjectileDamage']
        player.ammo = shelfFile['PlayerAmmo']
        player.xp = shelfFile['PlayerXP']
        player.xp_level = shelfFile['PlayerLevelXP']
        shelfFile.close()

        return player, health_bar, self.obstacle_list, self.water_group, self.decoration_group,  self.monster_group, \
                self.cannon_group, self.item_box_group, self.exit_group

    def choice_monster(self):
        do_monster = rand.randrange(0, 30)
        if do_monster == 1:
            # Variable pour déterminer combien de monstres sautent
            n_monster = rand.randrange(self.n_max_monster + 1)
            # Variable pour déterminer quel monstre saute
            for i in range(n_monster):
                cpt_monster = 0
                which_monster = rand.randrange(self.n_max_monster + 1)
                for monster in self.monster_group:
                    if cpt_monster == which_monster and not monster.jumping and not monster.fall:
                        monster.jumping = True
                        monster.xi = monster.rect.x
                        monster.yi = monster.rect.y
                        # Vecteurs de saut aléatoires
                        monster.vx = rand.randrange(-10, 10)
                        monster.vy = rand.randrange(30, 50)
                        monster.t = 0
                    else:
                        cpt_monster += 1

    def choice_smart_monster(self, x, y):
        do_monster = rand.randrange(0, 30)
        if do_monster == 1:
            # Variable pour déterminer combien de monstres sautent
            n_monster = rand.randrange(self.n_max_monster + 1)
            # Variable pour déterminer quel monstre saute
            for i in range(n_monster):
                cpt_monster = 0
                which_monster = rand.randrange(self.n_max_monster + 1)
                for monster in self.monster_group:
                    if cpt_monster == which_monster and not monster.jumping and not monster.fall:
                        monster.jumping = True
                        monster.xi = monster.rect.x
                        monster.yi = monster.rect.y
                        # Compute the y vector
                        monster.compute_vy(x + rand.randrange(-300, 300),
                                           y + rand.randrange(-300, 300))
                        monster.t = 0
                    else:
                        cpt_monster += 1

    def choice_smartest_monster(self, x, y):
        do_monster = rand.randrange(0, 30)
        if do_monster == 1:
            # Variable pour déterminer combien de monstres sautent
            n_monster = rand.randrange(self.n_max_monster + 1)
            # Variable pour déterminer quel monstre saute
            for i in range(n_monster):
                cpt_monster = 0
                which_monster = rand.randrange(self.n_max_monster + 1)
                for monster in self.monster_group:
                    if cpt_monster == which_monster and not monster.jumping and not monster.fall:
                        monster.jumping = True
                        monster.xi = monster.rect.x
                        monster.yi = monster.rect.y
                        # Compute the y vector
                        monster.compute_vy(x, y)
                        monster.t = 0
                    else:
                        cpt_monster += 1

    def choice_cannon(self):
        do_cannon = rand.randrange(0, 30)
        if do_cannon == 1:
            # Variable pour déterminer combien de canons tirent
            n_cannon = rand.randrange(0, self.n_max_cannon)
            # Variable pour déterminer quel canon tire
            for i in range(n_cannon):
                cpt_cannon = 0
                which_cannon = rand.randrange(self.n_max_cannon)
                for cannon in self.cannon_group:
                    if cpt_cannon == which_cannon and not cannon.fire and not cannon.shoot:
                        cannon.fire = True
                        # Vecteurs de tir aléatoires
                        cannon.vx = rand.randrange(-10, 10)
                        cannon.vy = rand.randrange(30, 50)
                    else:
                        cpt_cannon += 1

    def choice_smart_cannon(self, x, y):
        do_cannon = rand.randrange(0, 30)
        if do_cannon == 1:
            # Variable pour déterminer combien de canons tirent
            n_cannon = rand.randrange(0, self.n_max_cannon)
            # Variable pour déterminer quel canon tire
            for i in range(n_cannon):
                cpt_cannon = 0
                which_cannon = rand.randrange(self.n_max_cannon)
                for cannon in self.cannon_group:
                    if cpt_cannon == which_cannon and not cannon.fire and not cannon.shoot:
                        cannon.fire = True
                        # Compute the y vector
                        cannon.compute_vy(x + rand.randrange(-100, 100),
                                           y + rand.randrange(-100, 100))
                    else:
                        cpt_cannon += 1

    def choice_smartest_cannon(self, x, y):
        do_cannon = rand.randrange(0, 30)
        if do_cannon == 1:
            # Variable pour déterminer combien de canons tirent
            n_cannon = rand.randrange(0, self.n_max_cannon)
            # Variable pour déterminer quel canon tire
            for i in range(n_cannon):
                cpt_cannon = 0
                which_cannon = rand.randrange(self.n_max_cannon)
                for cannon in self.cannon_group:
                    if cpt_cannon == which_cannon and not cannon.fire and not cannon.shoot:
                        cannon.fire = True
                        # Compute the y vector
                        cannon.compute_vy(x, y)
                    else:
                        cpt_cannon += 1