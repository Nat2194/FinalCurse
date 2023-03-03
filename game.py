import pygame, os, csv, shelve, random
import random as rand
from world import World
import game_button
from screen_fade import ScreenFade
from projectile import Projectile
from turnbased import TurnByTurn
from damagetext import DamageText

class Game():
    def __init__(self, screen, SCREEN_WIDTH, SCREEN_HEIGHT, volume, save, level, level_complete, options, credits):
        self.screen = screen
        self.SCREEN_WIDTH = SCREEN_WIDTH
        self.SCREEN_HEIGHT = SCREEN_HEIGHT
        self.volume = volume
        self.save = save # current save slot, defined in main
        # set framerate
        self.clock = pygame.time.Clock()
        self.FPS = 60

        #copy functions from main
        self.Options = options
        self.Credits = credits

        # define game variables
        self.GRAVITY = (0, 10)
        self.SCROLL_THRESH = self.SCREEN_WIDTH // 4
        self.MAX_LEVELS = 3
        self.screen_scroll = 0
        self.bg_scroll = 0
        self.menu_scroll = 0
        self.level = level
        self.level_complete = level_complete
        self.start_intro = True

        # change music
        pygame.mixer.music.load("assets/audio/" + str(self.level) + ".mp3")
        pygame.mixer.music.play(-1, 0.0, 50)

        # load in level data and create world
        self.world = World(self.SCREEN_HEIGHT, self.level, self.save)

        # define player movement variables
        self.moving_left = False
        self.moving_right = False

        # load music and sounds

        # load images
        # button images
        self.restart_img = pygame.image.load("assets/menu/img/restart.png").convert_alpha()
        self.restart_img = pygame.transform.scale(self.restart_img, (int(self.restart_img.get_width() * 0.2),
                                                                           int(self.restart_img.get_height() * 0.2)))


        # projectile
        self.projectile_img = pygame.image.load("assets/img/icons/projectile.png").convert_alpha()
        self.projectile_img = pygame.transform.scale(self.projectile_img, (int(self.projectile_img.get_width() * 0.2),
                                                                      int(self.projectile_img.get_height() * 0.2)))

        # sword icon
        self.sword_img = pygame.image.load("assets/img/icons/sword.png").convert_alpha()
        self.sword_img = pygame.transform.scale(self.sword_img, (int(self.sword_img.get_width() * 0.1),
                                                                 int(self.sword_img.get_height() * 0.1)))

        # define colors
        self.BG = (64, 49, 54)
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.PINK = (235, 65, 54)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.BLUE = (0, 0, 255)

        self.bg_list = []

        # define font
        self.font = pygame.font.SysFont("Futura", 30)

        # create self.screen fades
        self.intro_fade = ScreenFade(1, self.BLACK, 4)
        self.death_fade = ScreenFade(2, self.PINK, 4)

        # create buttons
        self.restart_button = game_button.Button(self.SCREEN_WIDTH // 2 - 100, self.SCREEN_HEIGHT // 2 - 50, self.restart_img, 2)

        # create sprite groups
        self.monster_group = pygame.sprite.Group()
        self.cannon_group = pygame.sprite.Group()
        self.projectile_group = pygame.sprite.Group()
        self.item_box_group = pygame.sprite.Group()
        self.decoration_group = pygame.sprite.Group()
        self.water_group = pygame.sprite.Group()
        self.exit_group = pygame.sprite.Group()
        self.damage_text_group = pygame.sprite.Group()

        # create empty tile list
        self.world_data = []
        for row in range(self.world.ROWS):
            r = [-1] * self.world.COLS
            self.world_data.append(r)

        with open("data/level/level" + str(self.level) + "_data.csv", newline="") as csvfile:
            reader = csv.reader(csvfile, delimiter=",")
            for x, row in enumerate(reader):
                for y, tile in enumerate(row):
                    self.world_data[x][y] = int(tile)

        self.player, self.health_bar, self.obstacle_list, self.water_group, self.decoration_group, self.monster_group, \
        self.cannon_group, self.item_box_group, self.exit_group = self.world.process_data(self.world_data)

        #create bonus sound list
        self.sound_bonus_list = []
        # count number of files in the folder
        num_of_sounds = len(os.listdir("assets/audio/bonus"))
        for i in range(num_of_sounds):
            sound = pygame.mixer.Sound("assets/audio/bonus/" + str(i) + ".mp3")
            sound.set_volume(0.2)
            self.sound_bonus_list.append(sound)

    def square_screen(self):
        self.SCREEN_WIDTH = 800
        self.SCREEN_HEIGHT = int(self.SCREEN_WIDTH * 0.8)

    def full_screen(self):
        self.SCREEN_WIDTH = 1080
        self.SCREEN_HEIGHT = 720

    def begin_game(self):
        self.square_screen()

    def draw_text(self, text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        self.screen.blit(img, (x, y))

    def change_bg(self):
        # reset temporary list of images
        self.bg_list = []
        # count number of files in the folder
        n_bg = len(os.listdir("assets/img/background/level" + str(self.level)))
        for i in range(n_bg):
            img = pygame.image.load("assets/img/background/level" + str(self.level) + "/" + str(i) + ".png").convert_alpha()
            self.bg_list.append(img)

    def draw_bg(self):
        self.screen.fill(self.BG)
        if self.level == 1:
            width = self.bg_list[0].get_width()
            for x in range(6):
                self.screen.blit(self.bg_list[0], ((x * width) - self.bg_scroll * 0.5, 0))
                self.screen.blit(self.bg_list[1],
                                 ((x * width) - self.bg_scroll * 0.6,
                                  self.SCREEN_HEIGHT - self.bg_list[1].get_height() - 300))
                self.screen.blit(self.bg_list[2],
                                 ((x * width) - self.bg_scroll * 0.7,
                                  self.SCREEN_HEIGHT - self.bg_list[2].get_height() - 150))
                self.screen.blit(self.bg_list[3],
                                 ((x * width) - self.bg_scroll * 0.8, self.SCREEN_HEIGHT - self.bg_list[3].get_height()))
        elif self.level == 2:
            width = self.bg_list[0].get_width()
            for x in range(5):
                self.screen.blit(self.bg_list[0], ((x * width), 0))
                self.screen.blit(self.bg_list[1], ((x * width) - self.bg_scroll * 0.4, 0))
                self.screen.blit(self.bg_list[2],
                                 ((x * width) - self.bg_scroll * 0.5, 0))
                self.screen.blit(self.bg_list[3],
                                 ((x * width) - self.bg_scroll * 0.6, 0))
                self.screen.blit(self.bg_list[4],
                                 ((x * width) - self.bg_scroll * 0.7, 0))
                self.screen.blit(self.bg_list[5],
                                 ((x * width) - self.bg_scroll * 0.8, 0))
                self.screen.blit(self.bg_list[6],
                                 ((x * width) - self.bg_scroll * 0.9, 0))
        elif self.level == 3:
            width = self.bg_list[0].get_width()
            for x in range(5):
                self.screen.blit(self.bg_list[0], ((x * width) - self.bg_scroll * 0.3, 0))
                self.screen.blit(self.bg_list[1], ((x * width) - self.bg_scroll * 0.4, 0))
                self.screen.blit(self.bg_list[2],
                                 ((x * width) - self.bg_scroll * 0.5, 0))
                self.screen.blit(self.bg_list[3],
                                 ((x * width) - self.bg_scroll * 0.6, 0))
                self.screen.blit(self.bg_list[4],
                                 ((x * width) - self.bg_scroll * 0.7, 0))
                self.screen.blit(self.bg_list[5],
                                 ((x * width) - self.bg_scroll * 0.8, 0))


    # function to reset level
    def reset_level(self):
        self.world.n_max_cannon = 0
        self.world.n_max_monster = 0
        self.monster_group.empty()
        self.cannon_group.empty()
        self.projectile_group.empty()
        self.item_box_group.empty()
        self.decoration_group.empty()
        self.water_group.empty()
        self.exit_group.empty()

        # reset and fill the tile list
        self.world_data = []
        for row in range(self.world.ROWS):
            r = [-1] * self.world.COLS
            self.world_data.append(r)

        with open("data/level/level" + str(self.level) + "_data.csv", newline="") as csvfile:
            reader = csv.reader(csvfile, delimiter=",")
            for x, row in enumerate(reader):
                for y, tile in enumerate(row):
                    self.world_data[x][y] = int(tile)

        self.player, self.health_bar, self.obstacle_list, self.water_group, self.decoration_group, self.monster_group,\
        self.cannon_group, self.item_box_group, self.exit_group = self.world.process_data(self.world_data)


    def run_game(self):
        self.run = True
        while self.run:

            self.clock.tick(self.FPS)

            # update background
            self.draw_bg()
            # draw world map
            for tile in self.world.obstacle_list:
                tile[1][0] += self.screen_scroll
                self.screen.blit(tile[0], tile[1])
            # show player health
            self.draw_text("HP: ", self.font, self.WHITE, 10, 10)
            # calculate health ratio
            ratio = self.player.health / self.player.max_health
            pygame.draw.rect(self.screen, self.BLACK, (self.health_bar.x + 38, self.health_bar.y - 2, 154, 24))
            pygame.draw.rect(self.screen, self.RED, (self.health_bar.x + 40, self.health_bar.y, 150, 20))
            pygame.draw.rect(self.screen, self.GREEN, (self.health_bar.x + 40, self.health_bar.y, 150 * ratio, 20))

            # show player XP
            self.draw_text("XP: " + str(self.player.xp_level), self.font, self.WHITE, 10, 40)
            self.draw_text("LEVEL: " + str(self.player.xp_level), self.font, self.WHITE, 10, 70)
            # calculate XP ratio
            ratio = (self.player.xp % 100) / 100
            pygame.draw.rect(self.screen, self.BLACK, (self.health_bar.x + 38, self.health_bar.y + 28, 154, 24))
            pygame.draw.rect(self.screen, self.WHITE, (self.health_bar.x + 40, self.health_bar.y + 30, 150, 20))
            pygame.draw.rect(self.screen, self.BLUE, (self.health_bar.x + 40, self.health_bar.y + 30, 150 * ratio, 20))

            # show player ammo
            self.draw_text("AMMO: ", self.font, self.WHITE, 10, 100)
            for x in range(self.player.ammo):
                self.screen.blit(self.projectile_img, (90 + (x * 10), 100))
            # show strength
            self.draw_text("STRENGTH: ", self.font, self.WHITE, 10, 130)
            for x in range(self.player.attack_damage//25):
                self.screen.blit(self.sword_img, (135 + (x * 15), 125))

            self.player.update()
            self.screen.blit(pygame.transform.flip(self.player.image, self.player.flip, False), self.player.rect)

            if self.level == 1:
                self.world.choice_monster()
            elif self.level == 2:
                self.world.choice_smart_monster(self.player.rect.centerx, self.player.rect.y)
            elif self.level == 3:
                self.world.choice_smartest_monster(self.player.rect.centerx, self.player.rect.y)

            for monster in self.monster_group:
                monster.update()
                if monster.health > 0 or not monster.death_anim:
                    self.screen.blit(pygame.transform.flip(monster.image, monster.flip, False), monster.rect)

            if self.level == 1:
                self.world.choice_cannon()
            elif self.level == 2:
                self.world.choice_smart_cannon(self.player.rect.centerx, self.player.rect.y)
            elif self.level == 3:
                self.world.choice_smartest_cannon(self.player.rect.centerx, self.player.rect.y)

            for cannon in self.cannon_group:
                cannon.update_animation()
                self.screen.blit(pygame.transform.flip(cannon.image, cannon.flip, False), cannon.rect)
                if cannon.shoot:
                    self.screen.blit(cannon.cannonball.image, cannon.cannonball.rect)

            # update and draw groups
            self.item_box_group.update(self.player, self.screen_scroll, self.damage_text_group)
            self.decoration_group.update(self.screen_scroll)
            self.water_group.update(self.screen_scroll)
            self.exit_group.update(self.screen_scroll)
            self.projectile_group.update(self.screen_scroll, self.SCREEN_WIDTH)
            for projectile in self.projectile_group:
                self.screen.blit(pygame.transform.flip(projectile.image, projectile.flip, False), projectile.rect)
            self.item_box_group.draw(self.screen)
            self.decoration_group.draw(self.screen)
            self.water_group.draw(self.screen)
            self.exit_group.draw(self.screen)
            # draw the damage text
            self.damage_text_group.update()
            self.damage_text_group.draw(self.screen)

            # show intro
            if self.start_intro:
                if self.intro_fade.fade(self.screen, self.SCREEN_WIDTH, self.SCREEN_HEIGHT):
                    self.start_intro = False
                    self.intro_fade.fade_counter = 0

            # update player actions
            if self.player.alive:
                if self.player.action != 5:
                    if self.player.attacking:
                        self.player.update_action(4)  # 4: attack
                    # shoot projectiles
                    elif self.player.shoot():  # j pressed and cooldown and ammo checked
                        self.player.update_action(4)  # 4: attack
                        self.player.attacking = True
                        projectile = Projectile(
                            self.player.rect.centerx + (0.75 * self.player.rect.size[0] * self.player.direction),
                            self.player.rect.bottom,
                            self.player.direction, 0.8)
                        if self.player.direction < 0:
                            projectile.flip = True
                        self.projectile_group.add(projectile)
                    elif self.player.in_air:
                        self.player.update_action(2)  # 2: jump
                    elif self.moving_left or self.moving_right:
                        self.player.update_action(1)  # 1: run
                    else:
                        self.player.update_action(0)  # 0: idle
                self.player.move(self.moving_left, self.moving_right)
                self.screen_scroll = 0
                # apply gravity
                self.player.vy += self.player.gravity + self.player.resistance
                if self.player.vy > 10:
                    self.player.vy = 10
                self.player.dy += self.player.vy

                # check for collision
                for tile in self.world.obstacle_list:
                    # check collision in the x direction
                    if tile[1].colliderect(self.player.rect.x + self.player.dx, self.player.rect.y,
                                           self.player.rect.width, self.player.rect.height):
                        self.player.dx = 0
                    # check for collision in the y direction
                    elif tile[1].colliderect(self.player.rect.x, self.player.rect.y + self.player.dy,
                                             self.player.rect.width, self.player.rect.height):
                        # check if below the ground, i.e. jumping
                        if self.player.vy < 0:
                            self.player.vy = 0
                            self.player.dy = tile[1].bottom - self.player.rect.top
                        # check if above the ground, i.e. falling
                        elif self.player.vy >= 0:
                            self.player.vy = 0
                            self.player.in_air = False
                            self.player.nbr_jump = 0
                            self.player.dy = tile[1].top - self.player.rect.bottom
                            self.player.resistance = -0.75
                    else:
                        self.player.resistance = 0

                # check for collision with water
                if pygame.sprite.spritecollide(self.player, self.water_group, False) and not self.player.invincible:
                    self.player.health = 0

                # check for collision with exit
                if pygame.sprite.spritecollide(self.player, self.exit_group, False):
                    self.level_complete = True

                # check for collision with monster
                for monster in self.monster_group:
                    if self.player.rect.colliderect(monster.rect) and monster.alive:
                        if not monster.collision_player:  # to attack once
                            monster.collision_player = True
                            monster.attack()
                            monster.jumping = True
                            monster.xi = monster.rect.x
                            monster.yi = monster.rect.y
                            monster.vy = rand.randrange(30, 50)
                            monster.t = 0
                            if self.player.attacking:
                                monster.health -= self.player.attack_damage
                                monster.update_action(3)
                                damage_text = DamageText(monster.rect.centerx, monster.rect.y,
                                                         str(self.player.attack_damage), (255, 0, 0))
                                self.damage_text_group.add(damage_text)
                                if monster.health <= 0:
                                    monster.killed_by_player = True
                            elif monster.attacking and not self.player.invincible:
                                self.player.health -= monster.attack_damage
                                self.player.update_action(5)
                                damage_text = DamageText(monster.rect.centerx, monster.rect.y,
                                                         str(monster.attack_damage), (255, 0, 0))
                                self.damage_text_group.add(damage_text)
                    else:
                        monster.collision_player = False

                # check for collision with cannonball
                for cannon in self.cannon_group:
                    if cannon.shoot and self.player.rect.colliderect(cannon.cannonball.rect) and not self.player.invincible:
                        self.player.health -= cannon.attack_damage
                        self.player.update_action(5)
                        damage_text = DamageText(self.player.rect.centerx, self.player.rect.y,
                                                 str(cannon.attack_damage), (255, 0, 0))
                        self.damage_text_group.add(damage_text)
                        del (cannon.cannonball)
                        cannon.shoot = False

                # check if fallen off the map
                if self.player.rect.bottom > self.SCREEN_HEIGHT:
                    self.player.health = 0

                # check if going off the edges of the self.screen
                if self.player.rect.left + self.player.dx < 0 or self.player.rect.right + self.player.dx > \
                        self.SCREEN_WIDTH:
                    self.player.dx = 0

                # update rectangle position
                self.player.rect.x += self.player.dx
                self.player.rect.y += self.player.dy

                # update scroll based on player position
                if (self.player.rect.right > self.SCREEN_WIDTH - self.SCROLL_THRESH and self.bg_scroll <
                    (self.world.level_length * self.world.TILE_SIZE) - self.SCREEN_WIDTH) \
                        or (self.player.rect.left < self.SCROLL_THRESH and self.bg_scroll > abs(self.player.dx)):
                    self.player.rect.x -= self.player.dx
                    self.screen_scroll = -self.player.dx

                self.bg_scroll -= self.screen_scroll

                # check if player has completed the level
                if self.level_complete:
                    self.screen.fill((0, 0, 0))
                    self.start_intro = True
                    self.change_bg()
                    self.bg_scroll = 0
                    self.moving_left = False
                    self.moving_right = False
                    pygame.mixer.music.load("assets/turnbyturn/audio/music_intro.mp3")
                    pygame.mixer.music.play(0)
                    # save player data
                    shelfFile = shelve.open('data/saves/save' + str(self.save))
                    shelfFile['PlayerHealth'] = self.player.health
                    shelfFile['PlayerMaxHealth'] = self.player.max_health
                    shelfFile['PlayerMaxHealth'] = self.player.max_health
                    shelfFile['PlayerAttack'] = self.player.attack_damage
                    shelfFile['PlayerProjectileDamage'] = self.player.projectile_damage
                    shelfFile['PlayerAmmo'] = self.player.ammo
                    shelfFile['PlayerXP'] = self.player.xp
                    shelfFile['PlayerLevelXP'] = self.player.xp_level
                    shelfFile['BossLevel'] = True
                    shelfFile.close()
                    self.reset_level()
                    # initialize turn by turn game
                    self.tbt_level = TurnByTurn(self.screen, self.SCREEN_WIDTH, self.SCREEN_HEIGHT, self.save, self.Options)
                    # start turn by turn level
                    self.tbt_level.run()
                    # check level completion
                    shelfFile = shelve.open('data/saves/save' + str(self.save))
                    self.level = shelfFile['Level']
                    self. level_complete = False
                    shelfFile['BossLevel'] = False #it's no longer a boss level
                    shelfFile.close()
                    # run the next platformer level
                    if self.level <= self.MAX_LEVELS:
                        pygame.mixer.music.load("assets/audio/" + str(self.level) + ".mp3")
                        pygame.mixer.music.play(-1, 0.0, 50)
                        self.change_bg()
                        # load in level data and create world
                        with open("data/level/level" + str(self.level) + "_data.csv", newline="") as csvfile:
                            reader = csv.reader(csvfile, delimiter=",")
                            for x, row in enumerate(reader):
                                for y, tile in enumerate(row):
                                    self.world_data[x][y] = int(tile)
                        self.world = World(self.SCREEN_HEIGHT, self.level, self.save)
                        self.player, self.health_bar, self.obstacle_list, self.water_group, self.decoration_group, \
                        self.monster_group, self.cannon_group, self.item_box_group, self.exit_group = \
                            self.world.process_data(self.world_data)
                    else:
                        shelfFile = shelve.open('data/saves/save' + str(self.save))
                        self.level = 1 #reset progression
                        self.level = 1 #reset progression
                        shelfFile['Level'] = self.level
                        self.level_complete = False
                        shelfFile['BossLevel'] = False  # it's no longer a boss level
                        self.change_bg()
                        shelfFile.close()
                        #run cinematic
                        self.run = False
                        self.Credits()
            else:
                self.screen_scroll = 0
                # apply gravity
                self.player.dy = 1.75
                # check for collision
                for tile in self.world.obstacle_list:
                    # check for collision in the y direction
                    if tile[1].colliderect(self.player.rect.x, self.player.rect.y + self.player.dy,
                                             self.player.rect.width, self.player.rect.height):
                        # check if above the ground, i.e. falling
                        if self.player.vy >= 0:
                            self.player.vy = 0
                            self.player.dy = tile[1].top - self.player.rect.bottom
                self.player.rect.y += self.player.dy

                if self.death_fade.fade(self.screen, self.SCREEN_WIDTH, self.SCREEN_HEIGHT):
                    if self.restart_button.draw(self.screen):
                        self.death_fade.fade_counter = 0
                        self.start_intro = True
                        self.bg_scroll = 0
                        self.reset_level()
                        # load in level data and create world
                        with open("data/level/level" + str(self.level) + "_data.csv", newline="") as csvfile:
                            reader = csv.reader(csvfile, delimiter=",")
                            for x, row in enumerate(reader):
                                for y, tile in enumerate(row):
                                    self.world_data[x][y] = int(tile)
                        self.world = World(self.SCREEN_HEIGHT, self.level, self.save)
                        self.player, self.health_bar, self.obstacle_list, self.water_group, self.decoration_group, \
                        self.monster_group, self.cannon_group, self.item_box_group, self.exit_group = \
                            self.world.process_data(self.world_data)

            # check collision of projectile with tiles
            for projectile in self.projectile_group:
                for tile in self.world.obstacle_list:
                    if tile[1].colliderect(projectile.rect):
                        projectile.kill()

            # update monster actions
            for monster in self.monster_group:
                monster.dx = 0
                if monster.action != 3: #if monster isn't hurt
                    if monster.jumping:
                        if monster.alive:
                            monster.update_action(1)  # 1: jump
                            monster.jump_process()
                    else:
                        monster.fall = True
                        monster.dy = self.GRAVITY[1] + monster.resistance[1]
                        if monster.alive:
                            monster.update_action(0)  # 0: idle

                # check for collision with level
                for tile in self.world.obstacle_list:
                    # check collision with walls
                    if tile[1].colliderect(monster.rect.x + monster.dx, monster.rect.y,
                                           monster.width, monster.height):
                        monster.xi += 2 * (monster.rect.x + monster.dx - monster.xi)
                        monster.vx *= -1
                    # check for collision in the y direction
                    if tile[1].colliderect(monster.rect.x, monster.rect.y + monster.dy,
                                           monster.width, monster.height):
                        monster.jumping = False
                        # check if below the ground, i.e. thrown up
                        if monster.dy < 0:
                            monster.fall = True
                            monster.dy = tile[1].bottom - monster.rect.top
                        # check if above the ground, i.e. falling
                        elif monster.dy >= 0:
                            monster.fall = False
                            monster.dy = tile[1].top - monster.rect.bottom
                            monster.resistance = (0, -10)
                    else:
                        monster.resistance = (0, 0)

                # check for collision with water
                if pygame.sprite.spritecollide(monster, self.water_group, False):
                    monster.health = 0

                # check for collision with projectile
                if pygame.sprite.spritecollide(monster, self.projectile_group, False):
                    monster.health -= self.player.projectile_damage
                    monster.update_action(3)
                    damage_text = DamageText(monster.rect.centerx, monster.rect.y,
                                             str(self.player.projectile_damage), (255, 0, 0))
                    self.damage_text_group.add(damage_text)
                    if monster.health <= 0:
                        monster.killed_by_player = True

                # check if fallen off the map
                if monster.rect.bottom > self.SCREEN_HEIGHT:
                    monster.health = 0

                # update rectangle position
                monster.rect.x += monster.dx + self.screen_scroll
                monster.xi += self.screen_scroll
                monster.rect.y += monster.dy

            # update cannon actions
            for cannon in self.cannon_group:
                cannon.dy = self.GRAVITY[1] + cannon.resistance[1]
                if cannon.fire:
                    cannon.update_action(1)  # 1: shoot
                else:
                    cannon.update_action(0)  # 0: idle
                    if cannon.shoot:
                        cannon.cannonball.dx, cannon.cannonball.dy = 0, 0
                        cannon.fire_process()

                # check for collision with level
                for tile in self.world.obstacle_list:
                    # check collision cannonball with walls
                    if cannon.shoot and tile[1].colliderect(cannon.cannonball.rect.x + cannon.cannonball.dx,
                                                            cannon.cannonball.rect.y,
                                                            cannon.cannonball.width, cannon.cannonball.height):
                        del (cannon.cannonball)
                        cannon.shoot = False
                    # check for collision of the cannonball in the y direction
                    if cannon.shoot and tile[1].colliderect(cannon.cannonball.rect.x,
                                                            cannon.cannonball.rect.y + cannon.cannonball.dy,
                                                            cannon.cannonball.width, cannon.cannonball.height):
                        del (cannon.cannonball)
                        cannon.shoot = False
                    # check for collision of the cannon in the y direction
                    if tile[1].colliderect(cannon.rect.x, cannon.rect.y + cannon.dy,
                                           cannon.width, cannon.height):
                        # check if above the ground, i.e. falling
                        if cannon.dy >= 0:
                            cannon.dy = tile[1].top - cannon.rect.bottom
                            cannon.resistance = (0, -10)
                    else:
                        cannon.resistance = (0, 0)

                # check for collision cannonball with water
                if cannon.shoot and pygame.sprite.spritecollide(cannon.cannonball, self.water_group, False):
                    del (cannon.cannonball)
                    cannon.shoot = False

                # check if fallen off the map
                if cannon.shoot and cannon.cannonball.rect.bottom > self.SCREEN_HEIGHT:
                    del (cannon.cannonball)
                    cannon.shoot = False

                # update rectangle position
                cannon.rect.x += self.screen_scroll
                cannon.rect.y += cannon.dy
                if cannon.shoot:
                    cannon.cannonball.rect.x += cannon.cannonball.dx + self.screen_scroll
                    cannon.cannonball.xi += self.screen_scroll
                    cannon.cannonball.rect.y += cannon.cannonball.dy

            for event in pygame.event.get():
                # quit game
                if event.type == pygame.QUIT:
                    self.run = False
                # keyboard presses
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        self.moving_left = True
                    if event.key == pygame.K_d:
                        self.moving_right = True
                    if event.key == pygame.K_g:
                        if not self.player.invincible:
                            self.player.invincible = True
                            self.player.attack_damage = 5000
                            self.player.projectile_damage = 2000
                            self.player.ammo = 1000
                            self.player.n_jump_max = 100
                        else:
                            self.player.invincible = False
                            self.player.attack_damage = 50
                            self.player.projectile_damage = 20
                            self.player.ammo = 20
                            self.player.n_jump_max = 2
                    if event.key == pygame.K_SPACE:
                        self.player.attack()
                    if event.key == pygame.K_j:
                        self.player.shooting = True
                    if event.key == pygame.K_w and self.player.alive:
                        self.player.jump = True
                    if event.key == pygame.K_ESCAPE:
                        self.Options()

                # keyboard button released
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                        self.moving_left = False
                    if event.key == pygame.K_d:
                        self.moving_right = False

            for monster in self.monster_group:
                monster.t += 0.3
                if monster.health <= 0 and monster.death_anim:
                    monster.kill()
                    if monster.killed_by_player:
                        bonus_amount = random.randint(15, 25)
                        n_sound = random.randrange(2)
                        sound = self.sound_bonus_list[n_sound]
                        sound.play()
                        #switch
                        if monster.n_color == 0: #red monsters give strength
                            self.player.attack_damage += bonus_amount
                            self.player.projectile_damage += bonus_amount
                            damage_text = DamageText(self.player.rect.centerx, self.player.rect.y,
                                                 str(bonus_amount), (255, 100, 0))
                        elif monster.n_color == 1: #blue monsters give XP
                            self.player.xp += bonus_amount
                            damage_text = DamageText(self.player.rect.centerx, self.player.rect.y,
                                                str(bonus_amount), (0, 150, 255))
                        elif monster.n_color == 2: #green monsters give health
                            self.player.health += bonus_amount
                            self.player.max_health += bonus_amount
                            damage_text = DamageText(self.player.rect.centerx, self.player.rect.y,
                                                str(bonus_amount), (0, 255, 0))
                        else: #yellow monsters give ammo
                            self.player.ammo += bonus_amount % 5
                            damage_text = DamageText(self.player.rect.centerx, self.player.rect.y,
                                                str(bonus_amount), (255, 255, 0))
                        self.damage_text_group.add(damage_text)
            for cannon in self.cannon_group:
                if cannon.shoot:
                    cannon.cannonball.t += 0.3

            # world.draw_grid(world_data,self.screen) #used in level design
            pygame.display.update()

