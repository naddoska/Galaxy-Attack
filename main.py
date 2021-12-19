import os
import pygame
import argparse

from screens.game import game
from screens.controls import audio_cfg, display_cfg, controls
from screens.score_board import score_board
from screens.background import slow_bg_obj
from models.button import Button

from constants import TITLE,\
    BOSS_SHIP,\
    PLAYER_SPACE_SHIP,\
    PLAYER_LASER,\
    startImage,\
    controlImage,\
    trophyImage,\
    CANVAS,\
    framespersec,\
    FPS,\
    FONT_PATH,\
    MENU_MUSIC_PATH

# parsing arguments
ag = argparse.ArgumentParser()
ag.add_argument("--mute", help="disable all sounds", action="store_true")
args = vars(ag.parse_args())

if args["mute"]:
    audio_cfg.toggle_mute()

pygame.font.init()

pygame.display.set_caption(TITLE)

click = False


def main():
    title_font = pygame.font.Font(os.path.join(FONT_PATH, 'edit_undo.ttf'), 60)
    sub_title_font = pygame.font.Font(os.path.join(FONT_PATH, 'neue.ttf'), 30)
    control_font = pygame.font.Font(os.path.join(FONT_PATH, 'neue.ttf'), 36)
    audio_cfg.play_music(MENU_MUSIC_PATH)

    greenbtn = Button((7, 8, 16), 120, 225, 195, 66, "MOUSE")

    run = True
    while run:
        pygame.mouse.set_visible(True)
        slow_bg_obj.update()
        slow_bg_obj.render(CANVAS)

        window_width = CANVAS.get_width()
        background_width = slow_bg_obj.rectBGimg.width
        screen_rect = CANVAS.get_rect()
        center_x = screen_rect.centerx
        starting_x = center_x - background_width//2
        ending_x = center_x + background_width//2

        pos = pygame.mouse.get_pos()

        if greenbtn.isOver(pos):
            if click:
                game(True)

        greenbtn.draw(CANVAS, (255, 255, 255))

        title_label = title_font.render('Start the Game', 1, (0, 209, 0))
        CANVAS.blit(title_label, (window_width//2 -
                    title_label.get_width()//2 - 15, 350))
        CANVAS.blit(startImage, (window_width//2 +
                    title_label.get_width()//2, 353))
        sub_title_label = sub_title_font.render(
            'Press ENTER to play with KEYBOARD', 1, (249, 166, 2))
        CANVAS.blit(sub_title_label, (window_width//2 -
                    sub_title_label.get_width()//2, 410))
        sub_title_label = sub_title_font.render(
            'Click LEFT MOUSE button to play with MOUSE', 1, (249, 166, 2))
        CANVAS.blit(sub_title_label, (window_width//2 -
                    sub_title_label.get_width()//2, 450))

        # Ships
        CANVAS.blit(BOSS_SHIP, (starting_x + 285, 75))
        CANVAS.blit(PLAYER_SPACE_SHIP, (window_width//2 - 50, 575))
        CANVAS.blit(PLAYER_LASER, (window_width//2 - 50, 475))

        # Control Page
        control_label = control_font.render('[c]', 1, (255, 255, 255))
        CANVAS.blit(control_label, (starting_x + 95, 32))
        CANVAS.blit(controlImage, (starting_x + 30, 15))

        # ScoreBoard Page
        score_label = control_font.render('[s]', 1, (255, 255, 255))
        CANVAS.blit(score_label, (ending_x - 67, 30))
        CANVAS.blit(trophyImage, (ending_x - 130, 25))

        audio_cfg.display_volume(CANVAS)
        pygame.display.update()
        framespersec.tick(FPS)  # capping frame rate to 60
        click = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            # Keyboard events
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_m:
                    audio_cfg.toggle_mute()
                if event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:
                    audio_cfg.inc_volume(5)
                if event.key == pygame.K_MINUS:
                    audio_cfg.dec_volume(5)
                if event.key == pygame.K_f:
                    display_cfg.toggle_full_screen()

            # Mouse click events
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
                # if greenbtn.isOver(pos):
                #     click = True

            # Mouse hover events
            if event.type == pygame.MOUSEMOTION:
                if greenbtn.isOver(pos):
                    greenbtn.color = (255, 0, 0)
                else:
                    greenbtn.color = (7, 8, 16)
        keys = pygame.key.get_pressed()
        buttonclick = pygame.mouse.get_pressed()
        if keys[pygame.K_ESCAPE] or keys[pygame.K_q]:
            run = False

        if keys[pygame.K_c]:
            controls()

        if keys[pygame.K_s]:
            score_board()

        if keys[pygame.K_RETURN]:
            game()

        # On Hold
        # if buttonclick[0]:
        #     game(True)

    pygame.quit()


main()
