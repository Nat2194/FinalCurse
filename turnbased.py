import pygame, shelve, random
import button_tbt as button
from fighter import Fighter
from healthbar_tbt import HealthBar
from damagetext import DamageText

class Spell(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        scale = 3
        for num in range(16):
            img = pygame.image.load("assets/turnbyturn/img/enemy/level3/FinalBoss/Spell/" + str(num) + ".png").convert_alpha()
            img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
            self.images.append(img)
        self.frame_index = 0
        self.image = self.images[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.top = y
        self.update_time = pygame.time.get_ticks()

    def update(self, x, y):
        animation_cooldown = 100
        # check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
            # if the animation is complete then delete
            if self.frame_index >= len(self.images):
                self.kill()
            else:
                self.image = self.images[self.frame_index]
                self.rect = self.image.get_rect()
                self.rect.centerx = x
                self.rect.top = y

class TurnByTurn():
    def __init__(self, screen, screen_width, screen_height, save, options):
        self.clock = pygame.time.Clock()
        self.fps = 60
        self.Options = options #heriting function

        self.running = True

        self.save = save
        shelfFile = shelve.open('data/saves/save' + str(save))
        self.level = shelfFile['Level']
        shelfFile.close()

        #game window
        self.screen_height = screen_height
        self.screen_width = screen_width
        self.bottom_panel = 250
        self.screen = screen

        #define game variables
        self.current_fighter = 1
        if self.level < 3:
            self.total_fighters = 5
        else:
            self.total_fighters = 4
        self.action_cooldown = 0
        self.action_wait_time = 90
        self.attack = False
        self.potion = False
        self.potion_effect = 75
        self.clicked = False
        self.game_over = 0


        #define fonts
        self.font = pygame.font.SysFont('Times New Roman', 26)

        #define colours
        self.red = (255, 0, 0)
        self.green = (0, 255, 0)

        #load images
        #background image
        self.background_img = pygame.image.load('assets/turnbyturn/img/Background/'+ str(self.level) +'.png').convert_alpha()
        #panel image
        self.panel_img = pygame.image.load('assets/turnbyturn/img/Icons/panel.png').convert_alpha()
        #button images
        self.potion_img = pygame.image.load('assets/turnbyturn/img/Icons/potion.png').convert_alpha()
        self.restart_img = pygame.image.load('assets/turnbyturn/img/Icons/restart.png').convert_alpha()
        self.continue_img = pygame.image.load('assets/turnbyturn/img/Icons/continue.png').convert_alpha()
        #load victory and defeat images
        self.victory_img = pygame.image.load('assets/turnbyturn/img/Icons/victory.png').convert_alpha()
        self.defeat_img = pygame.image.load('assets/turnbyturn/img/Icons/defeat.png').convert_alpha()
        #sword image
        self.sword_img = pygame.image.load('assets/turnbyturn/img/Icons/sword.png').convert_alpha()

        #create sprites
        self.damage_text_group = pygame.sprite.Group()
        self.spell_group = pygame.sprite.Group()
        self.ally_list_alive = []
        self.ally_list = []
        self.enemy_list = []
        self.player = Fighter(200, 270, 'player', 100, 100, 20, 3, 2, save) #dummy values for health and attack
        self.contamine = Fighter(200, 210, 'player2', 100, 100, 20, 3, 2, save) #contamine
        self.wizard = Fighter(350, 270, 'player3', 100, 100, 20, 3, 2, save) #magicien
        self.ally_list.append(self.player)
        self.ally_list.append(self.contamine)
        self.ally_list.append(self.wizard)
        self.ally_list_alive.append(self.player)
        self.ally_list_alive.append(self.contamine)
        self.ally_list_alive.append(self.wizard)

        if self.level == 1:
            self.enemy1 = Fighter(550, 270, 'Bandit', 500, 500, 10, 1, 3, save)
            self.enemy2 = Fighter(700, 270, 'HeavyBandit', 510, 510, 15, 1, 3, save)
            self.enemy_list.append(self.enemy1)
            self.enemy_list.append(self.enemy2)
        elif self.level == 2:
            self.enemy1 = Fighter(550, 290, 'Centipede', 600, 600, 20, 1, 3, save)
            self.enemy2 = Fighter(700, 270, 'Giant', 610, 610, 30, 1, 3, save)
            self.enemy_list.append(self.enemy1)
            self.enemy_list.append(self.enemy2)
        elif self.level == 3:
            self.enemy1 = Fighter(500, 200, 'FinalBoss', 1000, 1000, 55, 1, 3, save)
            self.enemy_list.append(self.enemy1)


        self.player_health_bar = HealthBar(100, self.screen_height - self.bottom_panel + 40, self.player.max_hp)
        self.contamine_health_bar = HealthBar(100, self.screen_height - self.bottom_panel + 100, self.contamine.max_hp)
        self.wizard_health_bar = HealthBar(100, self.screen_height - self.bottom_panel + 160, self.wizard.max_hp)

        self.enemy1_health_bar = HealthBar(550, self.screen_height - self.bottom_panel + 90, self.enemy1.max_hp)
        if self.level != 3:
            self.enemy2_health_bar = HealthBar(550, self.screen_height - self.bottom_panel + 150, self.enemy2.max_hp)

        # create buttons
        self.potion_button = button.Button(screen, 300, self.screen_height - self.bottom_panel + 180, self.potion_img, 64, 64)
        self.restart_button = button.Button(screen, 330, 120, self.restart_img, 120, 30)
        self.continue_button = button.Button(screen, 330, 120, self.continue_img, 120, 30)

        self.level_complete = False  # Notice
        self.speaking = True

        self.MUSIC_END = pygame.USEREVENT + 1
        pygame.mixer.music.set_endevent(self.MUSIC_END)


        #create function for drawing text
    def draw_text(self, text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        self.screen.blit(img, (x, y))


    #function for drawing background
    def draw_bg(self):
        self.screen.blit(self.background_img, (0, 0))


    #function for drawing panel
    def draw_panel(self):
        #draw panel rectangle
        self.screen.blit(self.panel_img, (0, self.screen_height - self.bottom_panel))
        for count, i in enumerate(self.ally_list):
            # show name and health
            self.draw_text(i.name + " HP: " + str(i.hp), self.font, self.red, 100,
                           (self.screen_height - self.bottom_panel + 60) + count * 60)
        for count, i in enumerate(self.enemy_list):
            #show name and health
            self.draw_text(i.name +" HP: " + str(i.hp), self.font, self.red, 550, (self.screen_height - self.bottom_panel + 60) + count * 60)

    def draw_speech_bubble(self, screen, text, text_colour, bg_colour, pos, size):
        font = pygame.font.SysFont(None, size)
        text_surface = font.render(text, True, text_colour)
        text_rect = text_surface.get_rect(midbottom=pos)

        # background
        bg_rect = text_rect.copy()
        bg_rect.inflate_ip(10, 10)

        # Frame
        frame_rect = bg_rect.copy()
        frame_rect.inflate_ip(4, 4)

        pygame.draw.rect(screen, text_colour, frame_rect)
        pygame.draw.rect(screen, bg_colour, bg_rect)
        screen.blit(text_surface, text_rect)

    def run(self):
        while self.running  and not self.level_complete:

            self.clock.tick(self.fps)

            #draw background
            self.draw_bg()

            #draw panel
            self.draw_panel()
            self.player_health_bar.draw(self.player.hp, self.screen)
            self.contamine_health_bar.draw(self.contamine.hp, self.screen)
            self.wizard_health_bar.draw(self.wizard.hp, self.screen)
            self.enemy1_health_bar.draw(self.enemy1.hp, self.screen)
            if self.level != 3:
                self.enemy2_health_bar.draw(self.enemy2.hp, self.screen)

            #draw fighters
            self.player.update()
            self.contamine.update()
            self.wizard.update()

            self.player.draw(self.screen)
            self.contamine.draw(self.screen)
            self.wizard.draw(self.screen)
            for enemy in self.enemy_list:
                enemy.update()
                enemy.draw(self.screen)

            #draw the damage text
            self.damage_text_group.update()
            self.damage_text_group.draw(self.screen)
            self.spell_group.update(self.player.rect.right, self.player.rect.top - 150)
            self.spell_group.draw(self.screen)

            #control player actions
            #reset action variables
            self.attack = False
            self.potion = False
            target = None
            #make sure mouse is visible
            pygame.mouse.set_visible(True)
            pos = pygame.mouse.get_pos()
            for count, enemy in enumerate(self.enemy_list):
                if enemy.rect.collidepoint(pos):
                    #hide mouse
                    pygame.mouse.set_visible(False)
                    #show sword in place of mouse cursor
                    self.screen.blit(self.sword_img, pos)
                    if self.clicked and enemy.alive:
                        self.attack = True
                        self.speaking = False
                        target = self.enemy_list[count]
            if self.potion_button.draw():
                self.potion = True
            #show number of potions remaining
            self.draw_text(str(self.player.potions), self.font, self.green, 285, self.screen_height - self.bottom_panel + 190)


            if self.game_over == 0:
                if self.speaking and not self.attack :
                    self.draw_speech_bubble(self.screen, "Let's fight !", (255, 255, 255), (0, 0, 255),
                                            (self.player.rect.midtop[0], self.player.rect.midtop[1]-10), 30)
                #player action
                if self.player.alive:
                    if self.current_fighter == 1:
                        self.action_cooldown += 1
                    if self.current_fighter == 1 and self.action_cooldown >= self.action_wait_time:
                        #look for player action
                        #attack
                        if self.attack and target != None:
                            self.player.attack(target, self.damage_text_group)
                            self.current_fighter += 1
                            self.action_cooldown = 0
                        #potion
                        if self.potion == True:
                            if self.player.potions > 0:
                                #check if the potion would heal the player beyond max health
                                if self.player.max_hp - self.player.hp > self.potion_effect:
                                    heal_amount = self.potion_effect
                                else:
                                    heal_amount = self.player.max_hp - self.player.hp
                                self.player.hp += heal_amount
                                self.player.potions -= 1
                                damage_text = DamageText(self.player.rect.centerx, self.player.rect.y, str(heal_amount), self.green)
                                self.damage_text_group.add(damage_text)
                                self.current_fighter += 1
                                self.action_cooldown = 0

                else:
                    self.current_fighter+=1

                if self.contamine.alive:
                    if self.current_fighter == 2:
                        self.action_cooldown += 1
                    if self.current_fighter == 2 and self.action_cooldown >= self.action_wait_time:
                        #look for player action
                        #attack
                        if self.attack and target != None:
                            self.contamine.attack(target, self.damage_text_group)
                            self.current_fighter += 1
                            self.action_cooldown = 0
                        #potion
                        if self.potion == True:
                            if self.contamine.potions > 0:
                                #check if the potion would heal the player beyond max health
                                if self.contamine.max_hp - self.contamine.hp > self.potion_effect:
                                    heal_amount = self.potion_effect
                                else:
                                    heal_amount = self.contamine.max_hp - self.contamine.hp
                                self.contamine.hp += heal_amount
                                self.contamine.potions -= 1
                                damage_text = DamageText(self.contamine.rect.centerx, self.contamine.rect.y, str(heal_amount), self.green)
                                self.damage_text_group.add(damage_text)
                                self.current_fighter += 1
                                self.action_cooldown = 0

                elif self.contamine.alive == False and self.current_fighter == 2:
                    self.current_fighter += 1


                if self.wizard.alive:
                    if self.current_fighter == 3:
                        self.action_cooldown += 1
                    if self.current_fighter == 3 and self.action_cooldown >= self.action_wait_time:
                        #look for player action
                        #attack
                        if self.attack and target != None:
                            self.wizard.attack(target, self.damage_text_group)
                            self.current_fighter += 1
                            self.action_cooldown = 0
                        #potion
                        if self.potion == True:
                            if self.wizard.potions > 0:
                                #check if the potion would heal the player beyond max health
                                if self.wizard.max_hp - self.wizard.hp > self.potion_effect:
                                    heal_amount = self.potion_effect
                                else:
                                    heal_amount = self.player.max_hp - self.player.hp
                                self.wizard.hp += heal_amount
                                self.wizard.potions -= 1
                                damage_text = DamageText(self.player.rect.centerx, self.player.rect.y, str(heal_amount), self.green)
                                self.damage_text_group.add(damage_text)
                                self.current_fighter += 1
                                self.action_cooldown = 0

                elif self.wizard.alive == False and self.current_fighter == 3:
                    self.current_fighter += 1

                if not self.player.alive :
                    self.game_over = -1

                #enemy action
                for count, enemy in enumerate(self.enemy_list):
                    if self.current_fighter == 4 + count:
                        for ally in self.ally_list:
                            if not ally.alive:
                                self.ally_list.remove(ally)


                        if len(self.ally_list) != 0:
                            target = self.ally_list[random.randrange(len(self.ally_list))]
                        else:
                            target = None
                        if enemy.alive:
                            self.action_cooldown += 1
                            if self.action_cooldown >= self.action_wait_time:
                                #check if enemy needs to heal first
                                if (enemy.hp / enemy.max_hp) < 0.5 and enemy.potions > 0:
                                    #check if the potion would heal the enemy beyond max health
                                    if enemy.max_hp - enemy.hp > self.potion_effect:
                                        heal_amount = self.potion_effect
                                    else:
                                        heal_amount = enemy.max_hp - enemy.hp
                                    enemy.hp += heal_amount
                                    enemy.potions -= 1
                                    damage_text = DamageText(enemy.rect.centerx, enemy.rect.y, str(heal_amount), self.green)
                                    self.damage_text_group.add(damage_text)
                                    self.current_fighter += 1
                                    self.action_cooldown = 0
                                #attack
                                else:
                                    enemy.attack(target, self.damage_text_group)
                                    self.current_fighter += 1
                                    self.action_cooldown = 0
                                    if enemy.casting_spell:
                                        spell = Spell(target.rect.right, target.rect.top - 170)
                                        self.spell_group.add(spell)
                                        enemy.casting_spell = False
                        else:
                            self.current_fighter += 1

                #if all fighters have had a turn then reset
                if self.current_fighter > self.total_fighters:
                    self.current_fighter = 1


            #check if all enemys are dead
            alive_enemys = 0
            for enemy in self.enemy_list:
                if enemy.alive:
                    alive_enemys += 1
            if alive_enemys == 0:
                self.game_over = 1


            #check if game is over
            if self.game_over != 0:
                if self.game_over == 1:
                    self.screen.blit(self.victory_img, (250, 50))
                    pygame.mouse.set_visible(True)
                    if self.continue_button.draw():
                        self.level_complete = True
                        # save game data
                        shelfFile = shelve.open('data/saves/save' + str(self.save))
                        shelfFile['PlayerHealth'] = self.player.hp
                        shelfFile['PlayerMaxHealth'] = self.player.max_hp
                        shelfFile['PlayerAttack'] = self.player.strength
                        shelfFile['PlayerProjectileDamage'] += self.player.xp_level * 10
                        shelfFile['PlayerXP'] = self.player.xp
                        shelfFile['PlayerLevelXP'] = self.player.xp_level
                        shelfFile['Level'] += 1
                        shelfFile.close()
                    self.action_cooldown = 0
                    self.game_over = 0
                if self.game_over == -1:
                    self.screen.blit(self.defeat_img, (290, 50))
                    if self.restart_button.draw():
                        for ally in self.ally_list:
                            ally.reset()
                    for enemy in self.enemy_list:
                        enemy.reset()
                    self.current_fighter += 1
                    self.action_cooldown = 0
                    self.game_over = 0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.clicked = True
                else:
                    self.clicked = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        # show mouse
                        pygame.mouse.set_visible(True)
                        self.Options()
                if event.type == self.MUSIC_END:
                    pygame.mixer.music.queue("assets/turnbyturn/audio/music_loop.mp3")


            pygame.display.update()
