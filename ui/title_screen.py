import pygame
import sys
import random
import time

from ui.button import Button
from client import Client
from ui.slider import Slider

pygame.init()

main_screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Menu")

background = pygame.image.load("resources/mainMenu/Background.png")
play_background = pygame.image.load("resources/mainMenu/Play Background.png")
options_image = pygame.image.load("resources/mainMenu/Options Rect.png")
play_image = pygame.image.load("resources/mainMenu/Play Rect.png")
left_arrow_image = pygame.image.load("resources/mainMenu/left_arrow.png")
right_arrow_image = pygame.image.load("resources/mainMenu/right_arrow.png")
quit_image = pygame.image.load("resources/mainMenu/Quit Rect.png")

controls_button_value = [119, 97, 115, 100, 32, 101]  # ASCII value of: W, A, S, D, SPACE, E
fps_value = [30, 60, 120, 144, 240, 360]
change_button_chars = ['w', 'a', 's', 'd', 'space', 'e']
fps_choice = 1


def get_font(size):  # Returns Press-Start-2P in the desired size
    return pygame.font.Font("resources/mainMenu/font.ttf", size)


def play():
    while True:
        play_mouse_pos = pygame.mouse.get_pos()

        main_screen.blit(play_background, (0, 0))

        play_singleplayer = Button(image=options_image, pos=(320, 260),
                                   text_input="Singleplayer", font=get_font(40), base_color="White",
                                   hovering_color="Green")

        play_singleplayer.changeColor(play_mouse_pos)
        play_singleplayer.update(main_screen)

        play_multiplayer = Button(image=options_image, pos=(960, 260),
                                  text_input="Multiplayer", font=get_font(40), base_color="White",
                                  hovering_color="Green")

        play_multiplayer.changeColor(play_mouse_pos)
        play_multiplayer.update(main_screen)

        play_back = Button(image=None, pos=(640, 460),
                           text_input="BACK", font=get_font(75), base_color="White", hovering_color="Green")

        play_back.changeColor(play_mouse_pos)
        play_back.update(main_screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_back.checkForInput(play_mouse_pos):
                    main_menu()
                if play_singleplayer.checkForInput(play_mouse_pos):
                    client = Client(1280, 720, fps_value[fps_choice], controls_button_value)
                    client.run()
                if play_multiplayer.checkForInput(play_mouse_pos):
                    print('Multiplayer work in progress...')
                    playMultiplayer()
        pygame.display.update()


def playMultiplayer():
    while True:
        play_mouse_pos = pygame.mouse.get_pos()

        main_screen.blit(play_background, (0, 0))

        host_game = Button(image=play_image, pos=(320, 260),
                           text_input="Host Game", font=get_font(40), base_color="White",
                           hovering_color="Green")

        host_game.changeColor(play_mouse_pos)
        host_game.update(main_screen)

        join_game = Button(image=play_image, pos=(960, 260),
                           text_input="Join Game", font=get_font(40), base_color="White",
                           hovering_color="Green")

        join_game.changeColor(play_mouse_pos)
        join_game.update(main_screen)

        play_back = Button(image=None, pos=(640, 460),
                           text_input="BACK", font=get_font(75), base_color="White", hovering_color="Green")

        play_back.changeColor(play_mouse_pos)
        play_back.update(main_screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_back.checkForInput(play_mouse_pos):
                    play()
                if host_game.checkForInput(play_mouse_pos):
                    print('Work in progress...')  # TODO Host game option
                if join_game.checkForInput(play_mouse_pos):
                    print('Work in progress...')  # TODO Join game option

        pygame.display.update()


def options():
    global fps_choice
    music_slider = Slider(width=200, height=20, x_pos=220, y_pos=265, color="WHITE", active_color="GREEN", value=1)
    sound_effects_slider = Slider(width=200, height=20, x_pos=220, y_pos=455, color="WHITE", active_color="GREEN",
                                  value=1)
    while True:
        options_mouse_pos = pygame.mouse.get_pos()

        main_screen.fill("black")

        options_text = get_font(45).render("Options", True, "WHITE")
        options_rect = options_text.get_rect(center=(640, 60))
        main_screen.blit(options_text, options_rect)

        sound_text = get_font(50).render("Sound", True, "#b68f40")
        sound_rect = sound_text.get_rect(center=(320, 160))

        main_screen.blit(sound_text, sound_rect)

        music_text = get_font(25).render("Music", True, "#b68f40")
        music_rect = music_text.get_rect(center=(320, 230))

        main_screen.blit(music_text, music_rect)

        music_slider.draw(main_screen)

        music_value_text = get_font(20).render(str(round(music_slider.value * 100)) + "%", True, "#b68f40")
        music_value_rect = music_value_text.get_rect(center=(320, 315))

        main_screen.blit(music_value_text, music_value_rect)

        sound_effects_text = get_font(25).render("Sound effects", True, "#b68f40")
        sound_effects_rect = sound_effects_text.get_rect(center=(320, 420))

        main_screen.blit(sound_effects_text, sound_effects_rect)

        sound_effects_slider.draw(main_screen)

        sound_effects_value_text = get_font(20).render(str(round(sound_effects_slider.value * 100)) + "%", True,
                                                       "#b68f40")
        sound_effects_value_rect = sound_effects_value_text.get_rect(center=(320, 505))

        main_screen.blit(sound_effects_value_text, sound_effects_value_rect)

        video_text = get_font(50).render("Video", True, "#b68f40")
        video_rect = video_text.get_rect(center=(1040, 160))

        main_screen.blit(video_text, video_rect)

        fps_text = get_font(25).render("FPS", True, "#b68f40")
        fps_rect = fps_text.get_rect(center=(1040, 230))
        main_screen.blit(fps_text, fps_rect)

        fps_value_text = get_font(35).render(str(fps_value[fps_choice]), True, "#b68f40")
        fps_value_rect = fps_value_text.get_rect(center=(1040, 290))
        main_screen.blit(fps_value_text, fps_value_rect)

        fps_left = Button(image=left_arrow_image, pos=(940, 288),
                          text_input="", font=get_font(10), base_color="White", hovering_color="Green")
        fps_left.update(main_screen)

        fps_right = Button(image=right_arrow_image, pos=(1140, 288),
                           text_input="", font=get_font(10), base_color="White", hovering_color="Green")
        fps_right.update(main_screen)

        controls_text = Button(image=None, pos=(1040, 455),
                               text_input="Controls", font=get_font(35), base_color="#b68f40", hovering_color="Green")

        controls_text.changeColor(options_mouse_pos)
        controls_text.update(main_screen)

        options_back = Button(image=None, pos=(640, 660),
                              text_input="BACK", font=get_font(75), base_color="White", hovering_color="Green")

        options_back.changeColor(options_mouse_pos)
        options_back.update(main_screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if controls_text.checkForInput(options_mouse_pos):
                    controls()
                if options_back.checkForInput(options_mouse_pos):
                    main_menu()
                if fps_right.checkForInput(options_mouse_pos):
                    if fps_choice == 5:
                        fps_choice = 0
                    else:
                        fps_choice += 1
                if fps_left.checkForInput(options_mouse_pos):
                    if fps_choice == 0:
                        fps_choice = 5
                    else:
                        fps_choice -= 1
                if music_slider.rect.collidepoint(options_mouse_pos):
                    music_slider.active = True
                if sound_effects_slider.rect.collidepoint(options_mouse_pos):
                    sound_effects_slider.active = True
            elif event.type == pygame.MOUSEBUTTONUP:
                music_slider.active = False
                sound_effects_slider.active = False
            elif event.type == pygame.MOUSEMOTION:
                if music_slider.active:
                    music_slider.update_slider_value(event.pos[0])
                if sound_effects_slider.active:
                    sound_effects_slider.update_slider_value(event.pos[0])
        pygame.display.update()


class ExclusiveBooleanArray:
    """Boolean array that ensures only one button for example can be pressed at once"""

    def __init__(self, size):
        self.array = [False] * size

    def set_true(self, index):
        if index < 0 or index >= len(self.array):
            raise IndexError("Index out of range")

        self.array = [False] * len(self.array)
        self.array[index] = True

    def set_false(self):
        self.array = [False] * len(self.array)

    def is_true(self, index):
        if index < 0 or index >= len(self.array):
            raise IndexError("Index out of range")

        return self.array[index]

    def __iter__(self):
        return iter(self.array)


def controls():
    global controls_button_value
    controls_ispressed = ExclusiveBooleanArray(6)
    global change_button_chars
    change_button_font_size = [40] * 6
    backup_change_char = 'W'
    while True:
        controls_mouse_pos = pygame.mouse.get_pos()

        main_screen.fill("black")

        controls_text = get_font(45).render("Controls", True, "WHITE")
        controls_rect = controls_text.get_rect(center=(640, 60))
        main_screen.blit(controls_text, controls_rect)

        up_change_button = draw_text_and_button(screen=main_screen, text="UP:", position=(260, 230),
                                                font_size=25, button_pos=(460, 230), button_index=0,
                                                controls_pressed=controls_ispressed, mouse_pos=controls_mouse_pos,
                                                button_font_size=change_button_font_size)

        left_change_button = draw_text_and_button(screen=main_screen, text="LEFT:", position=(260, 330),
                                                  font_size=25, button_pos=(460, 330), button_index=1,
                                                  controls_pressed=controls_ispressed, mouse_pos=controls_mouse_pos,
                                                  button_font_size=change_button_font_size)

        down_change_button = draw_text_and_button(screen=main_screen, text="DOWN:", position=(260, 430),
                                                  font_size=25, button_pos=(460, 430), button_index=2,
                                                  controls_pressed=controls_ispressed, mouse_pos=controls_mouse_pos,
                                                  button_font_size=change_button_font_size)

        right_change_button = draw_text_and_button(screen=main_screen, text="RIGHT:", position=(260, 530),
                                                   font_size=25, button_pos=(460, 530), button_index=3,
                                                   controls_pressed=controls_ispressed, mouse_pos=controls_mouse_pos,
                                                   button_font_size=change_button_font_size)

        shoot_change_button = draw_text_and_button(screen=main_screen, text="SHOOT:", position=(760, 330),
                                                   font_size=25, button_pos=(960, 330), button_index=4,
                                                   controls_pressed=controls_ispressed, mouse_pos=controls_mouse_pos,
                                                   button_font_size=change_button_font_size)

        use_change_button = draw_text_and_button(screen=main_screen, text="USE:", position=(760, 430),
                                                   font_size=25, button_pos=(960, 430), button_index=5,
                                                   controls_pressed=controls_ispressed, mouse_pos=controls_mouse_pos,
                                                   button_font_size=change_button_font_size)

        controls_back = Button(image=None, pos=(640, 660),
                               text_input="BACK", font=get_font(75), base_color="White", hovering_color="Green")

        controls_back.changeColor(controls_mouse_pos)
        controls_back.update(main_screen)

        buttons_variables = [
            (up_change_button, 0),
            (left_change_button, 1),
            (down_change_button, 2),
            (right_change_button, 3),
            (shoot_change_button, 4),
            (use_change_button, 5)
        ]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if controls_back.checkForInput(controls_mouse_pos):
                    if all(value is False for value in controls_ispressed):
                        options()
                    else:
                        main_screen.fill('BLACK')
                        warning_text = get_font(35).render("You have to assign a button first!", True, "WHITE")
                        warning_rect = warning_text.get_rect(center=(640, 360))
                        main_screen.blit(warning_text, warning_rect)
                        pygame.display.update()
                        time.sleep(1.5)
                for button, index in buttons_variables:
                    if button.checkForInput(controls_mouse_pos):
                        if all(value != 'Press any button' for value in change_button_chars):
                            backup_change_char = change_button_chars[index]
                            controls_ispressed.set_true(index)
                            change_button_chars[index] = 'Press any button'
                            change_button_font_size[index] = 10
            elif event.type == pygame.KEYDOWN:
                for button, index in buttons_variables:
                    if button.isPressed:
                        text = pygame.key.name(event.key)
                        print(f"Button {text} pressed")
                        if all(value != text for value in change_button_chars):
                            change_button_font_size[index] = 40
                            change_button_chars[index] = text
                            controls_button_value[index] = event.key
                            controls_ispressed.set_false()
                        else:
                            change_button_chars[index] = backup_change_char
                            already_used_button()

        pygame.display.update()


def draw_text_and_button(screen, text, position, font_size, button_pos, button_index, controls_pressed, mouse_pos,
                         button_font_size):
    text_surface = get_font(font_size).render(text, True, "#b68f40")
    text_rect = text_surface.get_rect(center=position)

    screen.blit(text_surface, text_rect)

    button = Button(image=None, pos=button_pos, text_input=change_button_chars[button_index],
                    font=get_font(button_font_size[button_index]), base_color="White", hovering_color="Green")
    button.isPressed = controls_pressed.is_true(button_index)

    button.changeColor(mouse_pos)
    button.update(screen)

    return button


def already_used_button():
    main_screen.fill('BLACK')
    warning_text = get_font(35).render("That button is already assigned!", True, "WHITE")
    warning_rect = warning_text.get_rect(center=(640, 360))
    main_screen.blit(warning_text, warning_rect)
    pygame.display.update()
    time.sleep(1.5)
    controls()


def main_menu():
    while True:
        main_screen.blit(background, (0, 0))

        menu_mouse_pos = pygame.mouse.get_pos()

        menu_text = get_font(50).render("Just another Rougelike", True, "#b68f40")
        menu_rect = menu_text.get_rect(center=(640, 100))

        play_button = Button(image=play_image, pos=(640, 250),
                             text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        options_button = Button(image=options_image, pos=(640, 400),
                                text_input="OPTIONS", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        quit_button = Button(image=quit_image, pos=(640, 550),
                             text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        main_screen.blit(menu_text, menu_rect)

        for button in [play_button, options_button, quit_button]:
            button.changeColor(menu_mouse_pos)
            button.update(main_screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.checkForInput(menu_mouse_pos):
                    play()
                if options_button.checkForInput(menu_mouse_pos):
                    options()
                if quit_button.checkForInput(menu_mouse_pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


main_menu()
