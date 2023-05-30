import pygame
import sys
import random

from ui.button import Button
from client import Client
from ui.slider import Slider

pygame.init()

SCREEN = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Menu")

BG = pygame.image.load("resources/mainMenu/Background.png")
PBG = pygame.image.load("resources/mainMenu/Play Background.png")

FPS_VALUE = [30, 60, 120, 144, 240, 360]
FPS_CHOICE = 1

def get_font(size):  # Returns Press-Start-2P in the desired size
    return pygame.font.Font("resources/mainMenu/font.ttf", size)




def play():
    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.blit(PBG, (0, 0))

        PLAY_SINGLEPLAYER = Button(image=pygame.image.load("resources/mainMenu/Options Rect.png"), pos=(320, 260),
                                   text_input="Singleplayer", font=get_font(40), base_color="White",
                                   hovering_color="Green")

        PLAY_SINGLEPLAYER.changeColor(PLAY_MOUSE_POS)
        PLAY_SINGLEPLAYER.update(SCREEN)

        PLAY_MULTIPLAYER = Button(image=pygame.image.load("resources/mainMenu/Options Rect.png"), pos=(960, 260),
                                  text_input="Multiplayer", font=get_font(40), base_color="White",
                                  hovering_color="Green")

        PLAY_MULTIPLAYER.changeColor(PLAY_MOUSE_POS)
        PLAY_MULTIPLAYER.update(SCREEN)

        PLAY_BACK = Button(image=None, pos=(640, 460),
                           text_input="BACK", font=get_font(75), base_color="White", hovering_color="Green")

        PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        PLAY_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    main_menu()
                if PLAY_SINGLEPLAYER.checkForInput(PLAY_MOUSE_POS):
                    client = Client(1280, 720, FPS_VALUE[FPS_CHOICE])
                    client.run()
                if PLAY_MULTIPLAYER.checkForInput(PLAY_MOUSE_POS):
                    print('Multiplayer work in progress...')
                    playMultiplayer()

        pygame.display.update()


def playMultiplayer():
    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.blit(PBG, (0, 0))

        HOST_GAME = Button(image=pygame.image.load("resources/mainMenu/Play Rect.png"), pos=(320, 260),
                           text_input="Host Game", font=get_font(40), base_color="White",
                           hovering_color="Green")

        HOST_GAME.changeColor(PLAY_MOUSE_POS)
        HOST_GAME.update(SCREEN)

        JOIN_GAME = Button(image=pygame.image.load("resources/mainMenu/Play Rect.png"), pos=(960, 260),
                           text_input="Join Game", font=get_font(40), base_color="White",
                           hovering_color="Green")

        JOIN_GAME.changeColor(PLAY_MOUSE_POS)
        JOIN_GAME.update(SCREEN)

        PLAY_BACK = Button(image=None, pos=(640, 460),
                           text_input="BACK", font=get_font(75), base_color="White", hovering_color="Green")

        PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        PLAY_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    play()
                if HOST_GAME.checkForInput(PLAY_MOUSE_POS):
                    print('Work in progress...')  # TODO Host game option
                if JOIN_GAME.checkForInput(PLAY_MOUSE_POS):
                    print('Work in progress...')  # TODO Join game option

        pygame.display.update()


def options():
    global FPS_CHOICE
    MUSIC_SLIDER = Slider(width=200, height=20, x_pos=220, y_pos=265, color="WHITE", active_color="GREEN", value=1)
    SOUND_EFFECTS_SLIDER = Slider(width=200, height=20, x_pos=220, y_pos=455, color="WHITE", active_color="GREEN", value=1)
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("black")

        OPTIONS_TEXT = get_font(45).render("Options", True, "WHITE")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 60))
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)

        SOUND_TEXT = get_font(50).render("Sound", True, "#b68f40")
        SOUND_RECT = SOUND_TEXT.get_rect(center=(320, 160))

        SCREEN.blit(SOUND_TEXT, SOUND_RECT)

        MUSIC_TEXT = get_font(25).render("Music", True, "#b68f40")
        MUSIC_RECT = MUSIC_TEXT.get_rect(center=(320, 230))

        SCREEN.blit(MUSIC_TEXT, MUSIC_RECT)

        MUSIC_SLIDER.draw(SCREEN)

        MUSIC_VALUE_TEXT = get_font(20).render(str(round(MUSIC_SLIDER.value * 100)) + "%", True, "#b68f40")
        MUSIC_VALUE_RECT = MUSIC_VALUE_TEXT.get_rect(center=(320, 315))

        SCREEN.blit(MUSIC_VALUE_TEXT, MUSIC_VALUE_RECT)

        SOUND_EFFECTS_TEXT = get_font(25).render("Sound effects", True, "#b68f40")
        SOUND_EFFECTS_RECT = SOUND_EFFECTS_TEXT.get_rect(center=(320, 420))

        SCREEN.blit(SOUND_EFFECTS_TEXT, SOUND_EFFECTS_RECT)

        SOUND_EFFECTS_SLIDER.draw(SCREEN)

        SOUND_EFFECTS_VALUE_TEXT = get_font(20).render(str(round(SOUND_EFFECTS_SLIDER.value * 100)) + "%", True, "#b68f40")
        SOUND_EFFECTS_VALUE_RECT = SOUND_EFFECTS_VALUE_TEXT.get_rect(center=(320, 505))

        SCREEN.blit(SOUND_EFFECTS_VALUE_TEXT, SOUND_EFFECTS_VALUE_RECT)

        VIDEO_TEXT = get_font(50).render("Video", True, "#b68f40")
        VIDEO_RECT = VIDEO_TEXT.get_rect(center=(1040, 160))

        SCREEN.blit(VIDEO_TEXT, VIDEO_RECT)

        FPS_TEXT = get_font(25).render("FPS", True, "#b68f40")
        FPS_RECT = FPS_TEXT.get_rect(center=(1040, 230))
        SCREEN.blit(FPS_TEXT, FPS_RECT)

        FPS_VALUE_TEXT = get_font(35).render(str(FPS_VALUE[FPS_CHOICE]), True, "#b68f40")
        FPS_VALUE_RECT = FPS_VALUE_TEXT.get_rect(center=(1040, 290))
        SCREEN.blit(FPS_VALUE_TEXT, FPS_VALUE_RECT)

        FPS_LEFT = Button(image=pygame.image.load("resources/mainMenu/left_arrow.png"), pos=(940, 288),
                          text_input="", font=get_font(10), base_color="White", hovering_color="Green")
        FPS_LEFT.update(SCREEN)

        FPS_RIGHT = Button(image=pygame.image.load("resources/mainMenu/right_arrow.png"), pos=(1140, 288),
                           text_input="", font=get_font(10), base_color="White", hovering_color="Green")
        FPS_RIGHT.update(SCREEN)

        OPTIONS_BACK = Button(image=None, pos=(640, 660),
                              text_input="BACK", font=get_font(75), base_color="White", hovering_color="Green")

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()
                if FPS_RIGHT.checkForInput(OPTIONS_MOUSE_POS):
                    if FPS_CHOICE == 5:
                        FPS_CHOICE = 0
                    else:
                        FPS_CHOICE += 1
                if FPS_LEFT.checkForInput(OPTIONS_MOUSE_POS):
                    if FPS_CHOICE == 0:
                        FPS_CHOICE = 5
                    else:
                        FPS_CHOICE -= 1
                if MUSIC_SLIDER.rect.collidepoint(OPTIONS_MOUSE_POS):
                    MUSIC_SLIDER.active = True
                if SOUND_EFFECTS_SLIDER.rect.collidepoint(OPTIONS_MOUSE_POS):
                    SOUND_EFFECTS_SLIDER.active = True
            elif event.type == pygame.MOUSEBUTTONUP:
                MUSIC_SLIDER.active = False
                SOUND_EFFECTS_SLIDER.active = False
            elif event.type == pygame.MOUSEMOTION:
                if MUSIC_SLIDER.active:
                    MUSIC_SLIDER.update_slider_value(event.pos[0])
                if SOUND_EFFECTS_SLIDER.active:
                    SOUND_EFFECTS_SLIDER.update_slider_value(event.pos[0])

        pygame.display.update()


def main_menu():
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(50).render("Just another Rougelike", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        PLAY_BUTTON = Button(image=pygame.image.load("resources/mainMenu/Play Rect.png"), pos=(640, 250),
                             text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        OPTIONS_BUTTON = Button(image=pygame.image.load("resources/mainMenu/Options Rect.png"), pos=(640, 400),
                                text_input="OPTIONS", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("resources/mainMenu/Quit Rect.png"), pos=(640, 550),
                             text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


main_menu()
