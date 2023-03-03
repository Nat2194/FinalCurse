""" Final Curse Game, by Les Joueurs du Greniers (Team 84)"""

import pygame, shelve, os
from pygame import mixer
import menu_button
from game import Game

pygame.init()
mixer.init()

SCREEN_WIDTH = 0
SCREEN_HEIGHT = 0
title_size = 0

def square_screen():
    global SCREEN_WIDTH, SCREEN_HEIGHT, title_size
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)
    title_size = 70

def full_screen():
    global SCREEN_WIDTH, SCREEN_HEIGHT, title_size
    SCREEN_WIDTH = 1380
    SCREEN_HEIGHT = 710
    title_size = 100

square_screen()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Final Curse")

# set framerate
clock = pygame.time.Clock()
FPS = 60

screen_scroll = -2
bg_scroll = 0
start_game = False

mouse_cooldown = 0

# load music and sounds
pygame.mixer.music.load("assets/menu/audio/music_menu.mp3")
volume = 0.3
volume_fx = 0.3
pygame.mixer.music.set_volume(volume)
pygame.mixer.music.play(-1, 0.0, 5000)


# load images
# button images
new_game_img = pygame.image.load("assets/menu/img/start.png").convert_alpha()
exit_img = pygame.image.load("assets/menu/img/exit.png").convert_alpha()
menu_img = pygame.image.load("assets/menu/img/menu.png").convert_alpha()
resume_img = pygame.image.load("assets/menu/img/resume.png").convert_alpha()
return_img = pygame.image.load("assets/menu/img/return.png").convert_alpha()
option_img = pygame.image.load('assets/menu/img/option.png').convert_alpha()
option_img = pygame.transform.scale(option_img, (85, 85))
plus_img = pygame.image.load('assets/menu/img/plus.png')
plus_img = pygame.transform.scale(plus_img, (85, 85))
minus_img = pygame.image.load('assets/menu/img/moins.png')
minus_img = pygame.transform.scale(minus_img, (85, 85))
play_img = pygame.image.load('assets/menu/img/play.png')
play_img = pygame.transform.scale(play_img, (85, 85))
pause_img = pygame.image.load('assets/menu/img/pause.png')
pause_img = pygame.transform.scale(pause_img, (85, 85))
mute_img = pygame.image.load('assets/menu/img/mute.png')
mute_img = pygame.transform.scale(mute_img, (85, 85))
credits_img = pygame.image.load('assets/menu/img/credits.png').convert_alpha()
save1_img = pygame.image.load("assets/menu/img/save1.png").convert_alpha()
save2_img = pygame.image.load("assets/menu/img/save2.png").convert_alpha()
save3_img = pygame.image.load("assets/menu/img/save3.png").convert_alpha()
# background
pine1_img = pygame.image.load("assets/menu/img/Background/pine1.png").convert_alpha()
pine2_img = pygame.image.load("assets/menu/img/Background/pine2.png").convert_alpha()
mountain_img = pygame.image.load("assets/menu/img/Background/mountain.png").convert_alpha()
sky_img = pygame.image.load("assets/menu/img/Background/sky_cloud.png").convert_alpha()


# define colors
BG = (144, 201, 120)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PINK = (235, 65, 54)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# define font
font1 = pygame.font.SysFont("Algerian", title_size)
font2 = pygame.font.SysFont("Algerian", 50)
font3 = pygame.font.SysFont("Algerian", 25)

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    rect = img.get_rect()
    screen.blit(img, (x - rect.width//2, y - rect.height//2))


def draw_bg():
    global screen_scroll, bg_scroll
    screen.fill(BG)
    width = sky_img.get_width()
    bg_scroll -= screen_scroll
    if bg_scroll * 0.8 > width:
        bg_scroll = -screen_scroll
    for x in range(10):
        screen.blit(sky_img, ((x * width) - bg_scroll * 0.5, 0))
        screen.blit(mountain_img, ((x * width) - bg_scroll * 0.6, SCREEN_HEIGHT - mountain_img.get_height() - 300))
        screen.blit(pine1_img, ((x * width) - bg_scroll * 0.7, SCREEN_HEIGHT - pine1_img.get_height() - 150))
        screen.blit(pine2_img, ((x * width) - bg_scroll * 0.8, SCREEN_HEIGHT - pine2_img.get_height()))

def NewGame():
    global game, start_game, mouse_cooldown
    NewGame_Menu = True
    # count number of files in the folder
    n = len(os.listdir("data/saves"))// 3 # because each save has 3 files
    while NewGame_Menu:
        clock.tick(FPS)
        if mouse_cooldown > 0:
            mouse_cooldown -= 1
        if n >= 3:
            draw_bg()
            draw_text('Only 3 saves allowed', font2, (0, 0, 0), SCREEN_WIDTH // 2, SCREEN_HEIGHT // 8)
            draw_text('Which one do you', font2, (0, 0, 0), SCREEN_WIDTH // 2,
                      SCREEN_HEIGHT // 8 + 50)
            draw_text('want to erase ?', font2, (0, 0, 0), SCREEN_WIDTH // 2,
                      SCREEN_HEIGHT // 8 + 100)
        else:
            # create game data
            shelfFile = shelve.open('data/saves/save' + str(n + 1))
            shelfFile['PlayerHealth'] = 100
            shelfFile['PlayerMaxHealth'] = 100
            shelfFile['PlayerX'] = 0
            shelfFile['PlayerY'] = 0
            shelfFile['PlayerAttack'] = 50
            shelfFile['PlayerProjectileDamage'] = 20
            shelfFile['PlayerAmmo'] = 10
            shelfFile['PlayerXP'] = 0
            shelfFile['PlayerLevelXP'] = 0
            shelfFile['Level'] = 1
            shelfFile['BossLevel'] = False #if the current level is a boss level
            shelfFile.close()
            game = Game(screen, SCREEN_WIDTH, SCREEN_HEIGHT, volume, n + 1, 1, False, Options, Credits)
            game.save = n + 1
            start_game = True
            NewGame_Menu = False
            game.change_bg()
            game.run_game()

        if save1_button.draw(screen) and not mouse_cooldown:
            mouse_cooldown = 20
            n = 0
        if save2_button.draw(screen) and not mouse_cooldown:
            n = 1
            mouse_cooldown = 20
        if save3_button.draw(screen) and not mouse_cooldown:
            mouse_cooldown = 20
            n = 2

        if return_button.draw(screen) and not mouse_cooldown:
            mouse_cooldown = 20
            NewGame_Menu = False
            start_game = False
            main_menu()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    NewGame_Menu = False
                    start_game = False
                    main_menu()

        pygame.display.update()


def ResumeGame():
    global game, start_game, mouse_cooldown
    Resume_Menu = True
    # count number of files in the folder
    n = len(os.listdir("data/saves")) // 3  # because each save has 3 files
    save_choice = False
    if n == 0:
        NewGame()
    elif n == 1:
        save_choice = True
    while Resume_Menu:
        clock.tick(FPS)
        draw_bg()

        if mouse_cooldown > 0:
            mouse_cooldown -= 1

        if n >= 2:

            if load1_button.draw(screen) and not mouse_cooldown:
                mouse_cooldown = 20
                n = 1
                save_choice = True
            if load2_button.draw(screen) and not mouse_cooldown:
                mouse_cooldown = 20
                n = 2
                save_choice = True
        if n == 3:
            if load3_button.draw(screen) and not mouse_cooldown:
                mouse_cooldown = 20
                save_choice = True

        if return_button.draw(screen) and not mouse_cooldown:
            mouse_cooldown = 20
            Resume_Menu = False
            start_game = False
            main_menu()

        if n <= 3 and save_choice:
            # load saved data
            shelfFile = shelve.open('data/saves/save' + str(n))
            level = shelfFile['Level']
            level_complete = shelfFile['BossLevel']
            shelfFile.close()
            Resume_Menu = False
            start_game = True
            game = Game(screen, SCREEN_WIDTH, SCREEN_HEIGHT, volume, n, level, level_complete, Options, Credits)
            game.change_bg()
            game.run_game()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    Resume_Menu = False
                    start_game = False
                    main_menu()

        pygame.display.update()


def Options():
    global volume, volume_fx, start_game, game, mouse_cooldown
    exit = False
    Options = True
    while Options:
        clock.tick(FPS)
        draw_bg()
        if mouse_cooldown > 0:
            mouse_cooldown -= 1

        if not exit:

            draw_text('Options', font1, (255, 255, 255), SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4)

            draw_text("Music Volume", font2, (255,255,255), SCREEN_WIDTH // 2 - 190, SCREEN_HEIGHT // 2)
            draw_text("FX Volume", font2, (255, 255, 255), SCREEN_WIDTH // 2 + 200, SCREEN_HEIGHT // 2)

            if minus_button_music.draw(screen) and not mouse_cooldown:
                mouse_cooldown = 20
                volume -= 0.1
                pygame.mixer.music.set_volume(volume)

            if plus_button_music.draw(screen) and not mouse_cooldown:
                mouse_cooldown = 20
                volume += 0.1
                pygame.mixer.music.set_volume(volume)

            if pygame.mixer.music.get_busy():
                if pause_button.draw(screen) and not mouse_cooldown:
                    mouse_cooldown = 20
                    pygame.mixer.music.pause()
            else:
                if play_button.draw(screen) and not mouse_cooldown:
                    mouse_cooldown = 20
                    pygame.mixer.music.unpause()

        if start_game: #if in game

            if exit:
                draw_text("Progression from last checkpoint won't be saved.", font3, (255, 255, 255), SCREEN_WIDTH//2,
                          SCREEN_HEIGHT // 2 + 50)
                draw_text("Are you sure you want to quit ?", font3, (255, 255, 255), SCREEN_WIDTH // 2,
                          SCREEN_HEIGHT // 2 + 20)
                draw_text("If yes,", font2, (255, 255, 255), SCREEN_WIDTH // 2,
                          3 * SCREEN_HEIGHT // 4 - 50)
                draw_text("Click again on Menu", font2, (255, 255, 255), SCREEN_WIDTH // 2,
                          3 * SCREEN_HEIGHT // 4)
            else:

                if minus_button_fx.draw(screen) and not mouse_cooldown:
                    mouse_cooldown = 20
                    volume_fx -= 0.1
                    game.player.update_volume(volume_fx)

                if mute_button.draw(screen) and not mouse_cooldown:
                    mouse_cooldown = 20
                    game.player.update_volume(0)


                if plus_button_fx.draw(screen) and not mouse_cooldown:
                    mouse_cooldown = 20
                    volume_fx += 0.1
                    game.player.update_volume(volume_fx)

            if return_menu_button.draw(screen) and not mouse_cooldown:
                mouse_cooldown = 20
                if not exit:
                    exit = True
                else:
                    Options = False
                    start_game = False
                    game.run = False
                    if game.level_complete:
                        game.tbt_level.running = False
                    main_menu()


        if return_button.draw(screen) and not mouse_cooldown:
            mouse_cooldown = 20
            if not exit:
                Options = False
                if not start_game:
                    main_menu()
            else:
                exit = False



        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if not start_game:
                        main_menu()

        pygame.display.update()



def Credits():
    global start_game, game, mouse_cooldown
    Credits = True
    screen_scrolly = 0
    while Credits:
        clock.tick(FPS)
        draw_bg()
        draw_text('Credits', font1, (255, 255, 255), SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4)

        if screen_scrolly > 1200:
            screen_scrolly = 0
        y = screen_scrolly // 3
        draw_text('Sound Design and Music by Max', font3, (255, 255, 255), SCREEN_WIDTH // 2, y % 400 + 200)
        y += 50
        draw_text('Sprite Design and Animation by Alix', font3, (255, 255, 255), SCREEN_WIDTH // 2, y % 400 + 200)
        y += 50
        draw_text('Menu Design by Max', font3, (255, 255, 255), SCREEN_WIDTH // 2, y % 400 + 200)
        y += 50
        draw_text('Menu code by Nima and Nathan', font3, (255, 255, 255), SCREEN_WIDTH // 2, y % 400 + 200)
        y += 50
        draw_text('Platformer code by Nathan', font3, (255, 255, 255), SCREEN_WIDTH // 2, y % 400 + 200)
        y += 50
        draw_text('Level design by Nathan', font3, (255, 255, 255), SCREEN_WIDTH // 2, y % 400 + 200)
        y += 50
        draw_text('Turn by turn code by Amine', font3, (255, 255, 255), SCREEN_WIDTH // 2, y % 400 + 200)
        y += 50
        draw_text('Time equations and trajectories by Nathan and Amine', font3, (255, 255, 255), SCREEN_WIDTH // 2, y % 400 +200)

        screen_scrolly += 1

        if mouse_cooldown > 0:
            mouse_cooldown -= 1

        if return_menu_button.draw(screen) and not mouse_cooldown:
            mouse_cooldown = 20
            Credits = False
            if start_game:  # if in-game (credits cinematic at the end of the game)
                start_game = False
            main_menu()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if start_game: # if in-game (credits cinematic at the end of the game)
                        start_game = False
                    Credits = False
        pygame.display.update()


# create buttons
new_game_button = menu_button.Button(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, new_game_img, 0.5, "center")
resume_button = menu_button.Button(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 125, resume_img, 0.5, "center")
return_button = menu_button.Button(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 250, return_img, 0.5, "center")
exit_button = menu_button.Button(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 250, exit_img, 0.5, "center")
option_button = menu_button.Button(10, 10, option_img, 1, "topleft")
return_menu_button = menu_button.Button(SCREEN_WIDTH - 10, 10, menu_img, 0.5, "topright")
credits_button = menu_button.Button(SCREEN_WIDTH - 10, 10, credits_img, 0.5, "topright")
plus_button_music = menu_button.Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 100, plus_img, 1, "center")
play_button = menu_button.Button(SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 + 100, play_img, 1, "center")
pause_button = menu_button.Button(SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 + 100, pause_img, 1, "center")
minus_button_music = menu_button.Button(SCREEN_WIDTH // 2 - 300, SCREEN_HEIGHT // 2 + 100, minus_img, 1, "center")
plus_button_fx = menu_button.Button(SCREEN_WIDTH // 2 + 300, SCREEN_HEIGHT // 2 + 100, plus_img, 1, "center")
mute_button = menu_button.Button(SCREEN_WIDTH // 2 + 200, SCREEN_HEIGHT // 2 + 100, mute_img, 1, "center")
minus_button_fx = menu_button.Button(SCREEN_WIDTH // 2 + 100, SCREEN_HEIGHT // 2 + 100, minus_img, 1, "center")
save1_button = menu_button.Button(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50, save1_img, 0.5, "center")
save2_button = menu_button.Button(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50, save2_img, 0.5, "center")
save3_button = menu_button.Button(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 150, save3_img, 0.5, "center")
load1_button = menu_button.Button(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50, save1_img, 0.5, "center")
load2_button = menu_button.Button(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50, save2_img, 0.5, "center")
load3_button = menu_button.Button(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 150, save3_img, 0.5, "center")

def main_menu():
    global start_game, screen, mouse_cooldown
    run = True
    while run:

        clock.tick(FPS)

        if mouse_cooldown > 0:
            mouse_cooldown -= 1

        if not start_game:
            # draw menu
            draw_bg()
            #draw title
            draw_text('The final curse', font1, (0, 0, 0), SCREEN_WIDTH //2, SCREEN_HEIGHT //4)
            # add buttons
            if new_game_button.draw(screen) and not mouse_cooldown:
                mouse_cooldown = 20
                NewGame()
            if resume_button.draw(screen) and not mouse_cooldown:
                mouse_cooldown = 20
                start_game = True
                ResumeGame()
            if option_button.draw(screen) and not mouse_cooldown:
                mouse_cooldown = 20
                Options()
            if credits_button.draw(screen) and not mouse_cooldown:
                mouse_cooldown = 20
                Credits()
            if exit_button.draw(screen) and not mouse_cooldown:
                mouse_cooldown = 20
                run = False
        else:
            # update background
            draw_bg()


        for event in pygame.event.get():
            # quit game
            if event.type == pygame.QUIT:
                run = False
            # keyboard presses
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False

        pygame.display.update()

main_menu()

pygame.quit()