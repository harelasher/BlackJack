import sys
import pygame
from pygame.locals import *

# Variables
LoggedIn = False


# (rect_x + rect_width // 2, rect_y + rect_height // 2) --
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)


# Initialize the pygame
pygame.init()

display_width = 800
display_height = 600

# Create the screen
screen = pygame.display.set_mode((display_width, display_height))
overlay = pygame.image.load('Pictures/overlay.png').convert()

# Title and icon
pygame.display.set_caption("BlackJack")
icon = pygame.image.load('Pictures/BJ.png')
pygame.display.set_icon(icon)

# Avatars
# **screen.blit(Man, (display_width / 1.15, 120 // 2 - 32))**
Man = pygame.image.load('Pictures/Man.png')
Man2 = pygame.image.load('Pictures/Man2.png')
woman = pygame.image.load('Pictures/woman.png')
woman2 = pygame.image.load('Pictures/woman2.png')

# Fonts
MainScreenFont = pygame.font.SysFont("gabriola", 80)
ButtonFont = pygame.font.Font("Fonts/Copperplate Gothic Bold Regular.ttf", 28)
MediumFont = pygame.font.SysFont("gabriola", 40)
LowFont = pygame.font.SysFont("gabriola", 20)
HelveticaFont = pygame.font.Font('Fonts/Copperplate Gothic Bold Regular.ttf', 20)

clock = pygame.time.Clock()


def main_menu():
    while True:
        screen.blit(overlay, (0, 0))

        draw_text("BlackJack", MainScreenFont, (255, 255, 255), screen, display_width // 2, 120 // 2)
        draw_text("By Harel Asher", LowFont, (255, 255, 255), screen, display_width // 2, 220 // 2)

        play_button = pygame.Rect(265, 200, 270, 65)
        pygame.draw.rect(screen, "white", play_button, 3, border_radius=10)
        draw_text("Login", ButtonFont, (255, 255, 255), screen, (play_button.x + play_button.w // 2),
                  (play_button.y + play_button.h // 2))

        help_button = pygame.Rect(play_button.x, play_button.y + 110, play_button.w, play_button.h)
        pygame.draw.rect(screen, "white", help_button, 3, border_radius=10)
        draw_text("Register", ButtonFont, (255, 255, 255), screen, (help_button.x + help_button.w // 2),
                  (help_button.y + play_button.h // 2))

        quit_button = pygame.Rect(help_button.x, help_button.y + 110, help_button.w, help_button.h)
        pygame.draw.rect(screen, "white", quit_button, 3, border_radius=10)
        draw_text("quit", ButtonFont, (255, 255, 255), screen, (quit_button.x + quit_button.w // 2),
                  (quit_button.y + help_button.h // 2))

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if play_button.collidepoint(event.pos):
                    login_menu()
                if help_button.collidepoint(event.pos):
                    register_menu()
                if quit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()
        clock.tick(120)


def login_menu():
    active_username = False
    active_password = False
    username_txt = ""
    password_txt = ""
    if not LoggedIn:
        running = True
        while running:
            screen.blit(overlay, (0, 0))

            draw_text("BlackJack", MainScreenFont, (255, 255, 255), screen, display_width // 2, 120 // 2)
            draw_text("By Harel Asher", LowFont, (255, 255, 255), screen, display_width // 2, 220 // 2)

            draw_text("login", ButtonFont, (255, 255, 255), screen, display_width // 2, 232 - 40)

            username_button = pygame.Rect(265, 240, 270, 60)
            pygame.draw.rect(screen, "white", username_button, 3, border_radius=10)

            password_button = pygame.Rect(username_button.x, username_button.y + 90, username_button.w,
                                          username_button.h)
            pygame.draw.rect(screen, "white", password_button, 3, border_radius=10)

            enter_button = pygame.Rect(username_button.x + 70, password_button.y + 90, username_button.w - 140,
                                       username_button.h)
            pygame.draw.rect(screen, "white", enter_button, 3)
            draw_text("enter", ButtonFont, (255, 255, 255), screen, (enter_button.x + enter_button.w // 2),
                      (enter_button.y + enter_button.h // 2))

            draw_text(username_txt, ButtonFont, (255, 255, 255), screen, username_button.x + username_button.w // 2,
                      username_button.y + username_button.h // 2)
            draw_text(password_txt, ButtonFont, (255, 255, 255), screen, password_button.x + password_button.w // 2,
                      password_button.y + password_button.h // 2)

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == MOUSEBUTTONDOWN:
                    if username_button.collidepoint(event.pos):
                        active_username = True
                    elif password_button.collidepoint(event.pos):
                        active_password = True
                    if not username_button.collidepoint(event.pos):
                        active_username = False
                    if not password_button.collidepoint(event.pos):
                        active_password = False

                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        return
                    if active_username:
                        if event.key == pygame.K_BACKSPACE:
                            username_txt = username_txt[:-1]
                        elif len(username_txt) < 9:
                            username_txt += event.unicode.lower()
                    if active_password:
                        if event.key == pygame.K_BACKSPACE:
                            password_txt = password_txt[:-1]
                        elif len(password_txt) < 9:
                            password_txt += event.unicode.lower()

            pygame.display.update()
            clock.tick(120)
    else:
        pass


def register_menu():
    active_username = False
    active_password = False
    username_txt = ""
    password_txt = ""
    if not LoggedIn:
        running = True
        while running:
            screen.blit(overlay, (0, 0))

            draw_text("BlackJack", MainScreenFont, (255, 255, 255), screen, display_width // 2, 120 // 2)
            draw_text("By Harel Asher", LowFont, (255, 255, 255), screen, display_width // 2, 220 // 2)

            draw_text("register", ButtonFont, (255, 255, 255), screen, display_width // 2, 232 - 40)

            username_button = pygame.Rect(265, 240, 270, 60)
            pygame.draw.rect(screen, "white", username_button, 3, border_radius=10)

            password_button = pygame.Rect(username_button.x, username_button.y + 90, username_button.w,
                                          username_button.h)
            pygame.draw.rect(screen, "white", password_button, 3, border_radius=10)

            enter_button = pygame.Rect(username_button.x + 70, password_button.y + 90, username_button.w - 140,
                                       username_button.h)
            pygame.draw.rect(screen, "white", enter_button, 3)
            draw_text("enter", ButtonFont, (255, 255, 255), screen, (enter_button.x + enter_button.w // 2),
                      (enter_button.y + enter_button.h // 2))

            draw_text(username_txt, ButtonFont, (255, 255, 255), screen, username_button.x + username_button.w // 2,
                      username_button.y + username_button.h // 2)
            draw_text(password_txt, ButtonFont, (255, 255, 255), screen, password_button.x + password_button.w // 2,
                      password_button.y + password_button.h // 2)

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == MOUSEBUTTONDOWN:
                    if username_button.collidepoint(event.pos):
                        active_username = True
                    elif password_button.collidepoint(event.pos):
                        active_password = True
                    if not username_button.collidepoint(event.pos):
                        active_username = False
                    if not password_button.collidepoint(event.pos):
                        active_password = False

                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        return
                    if active_username:
                        if event.key == pygame.K_BACKSPACE:
                            username_txt = username_txt[:-1]
                        elif len(username_txt) < 9:
                            username_txt += event.unicode.lower()
                    if active_password:
                        if event.key == pygame.K_BACKSPACE:
                            password_txt = password_txt[:-1]
                        elif len(password_txt) < 9:
                            password_txt += event.unicode.lower()

            pygame.display.update()
            clock.tick(120)
    else:
        pass


main_menu()
