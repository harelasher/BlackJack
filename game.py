import sys
import pygame
from pygame.locals import *
import string
import socket
from t import *

# Variables
global LoggedIn

available_chars = string.ascii_lowercase + string.digits + string.punctuation


# (rect_x + rect_width // 2, rect_y + rect_height // 2) -->
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

# DataBase

clock = pygame.time.Clock()


def bj_screen():
    screen.blit(overlay, (0, 0))
    draw_text("BlackJack", MainScreenFont, (255, 255, 255), screen, display_width // 2, 120 // 2)
    draw_text("By Harel Asher", LowFont, (255, 255, 255), screen, display_width // 2, 220 // 2)


# to show to regular screen


def main_menu(conn):
    global LoggedIn
    LoggedIn = False
    while True:
        bj_screen()

        login_button = pygame.Rect(265, 200, 270, 65)
        pygame.draw.rect(screen, "white", login_button, 3, border_radius=10)
        draw_text("Login", ButtonFont, (255, 255, 255), screen, (login_button.x + login_button.w // 2),
                  (login_button.y + login_button.h // 2))

        Register_button = pygame.Rect(login_button.x, login_button.y + 110, login_button.w, login_button.h)
        pygame.draw.rect(screen, "white", Register_button, 3, border_radius=10)
        draw_text("Register", ButtonFont, (255, 255, 255), screen, (Register_button.x + Register_button.w // 2),
                  (Register_button.y + login_button.h // 2))

        quit_button = pygame.Rect(Register_button.x, Register_button.y + 110, Register_button.w, Register_button.h)
        pygame.draw.rect(screen, "white", quit_button, 3, border_radius=10)
        draw_text("quit", ButtonFont, (255, 255, 255), screen, (quit_button.x + quit_button.w // 2),
                  (quit_button.y + Register_button.h // 2))

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if login_button.collidepoint(event.pos):
                    login_menu(conn)
                if Register_button.collidepoint(event.pos):
                    register_menu(conn)
                if quit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()
        clock.tick(120)


# main screen of the game


def login_menu(conn):
    global LoggedIn
    active_username = False
    active_password = False
    username_txt = ""
    password_txt = ""

    if LoggedIn:
        loggedin_menu(conn)

    while True:
        bj_screen()

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
                elif enter_button.collidepoint(event.pos):
                    cmd, msg = build_send_recv_parse(conn, PROTOCOL_CLIENT["login_msg"],
                                                     username_txt + DATA_DELIMITER + password_txt)
                    if cmd == 'LOGIN_OK':
                        loggedin_menu(conn)
                    else:
                        print(msg)
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
                    elif len(username_txt) < 9 and event.unicode.lower() in available_chars:
                        username_txt += event.unicode.lower()
                if active_password:
                    if event.key == pygame.K_BACKSPACE:
                        password_txt = password_txt[:-1]
                    elif len(password_txt) < 9 and event.unicode.lower() in available_chars:
                        password_txt += event.unicode.lower()

        pygame.display.update()
        clock.tick(120)


# login page


def register_menu(conn):
    global LoggedIn
    active_username = False
    active_password = False
    username_txt = ""
    password_txt = ""
    if LoggedIn:
        loggedin_menu(conn)

    while True:
        bj_screen()

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
                elif enter_button.collidepoint(event.pos):
                    cmd, msg = build_send_recv_parse(conn, PROTOCOL_CLIENT["register_msg"],
                                                     username_txt + DATA_DELIMITER + password_txt)
                    if cmd == 'REGISTER_OK':
                        loggedin_menu(conn)
                    else:
                        print(msg)
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
                    elif len(username_txt) < 9 and event.unicode.lower() in available_chars:
                        username_txt += event.unicode.lower()
                if active_password:
                    if event.key == pygame.K_BACKSPACE:
                        password_txt = password_txt[:-1]
                    elif len(password_txt) < 9 and event.unicode.lower() in available_chars:
                        password_txt += event.unicode.lower()

        pygame.display.update()
        clock.tick(120)


# register page


def loggedin_menu(conn):
    global LoggedIn
    while True:
        bj_screen()

        play_button = pygame.Rect(265, 180, 270, 65)
        pygame.draw.rect(screen, "white", play_button, 3, border_radius=10)
        draw_text("play", ButtonFont, (255, 255, 255), screen, (play_button.x + play_button.w // 2),
                  (play_button.y + play_button.h // 2))

        logout_button = pygame.Rect(play_button.x, play_button.y + 90, play_button.w, play_button.h)
        pygame.draw.rect(screen, "white", logout_button, 3, border_radius=10)
        draw_text("logout", ButtonFont, (255, 255, 255), screen, (logout_button.x + logout_button.w // 2),
                  (logout_button.y + play_button.h // 2))

        help_button = pygame.Rect(play_button.x, logout_button.y + 90, play_button.w, play_button.h)
        pygame.draw.rect(screen, "white", help_button, 3, border_radius=10)
        draw_text("help", ButtonFont, (255, 255, 255), screen, (help_button.x + help_button.w // 2),
                  (help_button.y + play_button.h // 2))

        quit_button = pygame.Rect(play_button.x, help_button.y + 90, play_button.w, play_button.h)
        pygame.draw.rect(screen, "white", quit_button, 3, border_radius=10)
        draw_text("quit", ButtonFont, (255, 255, 255), screen, (quit_button.x + quit_button.w // 2),
                  (quit_button.y + play_button.h // 2))

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
                    play_menu(conn)
                if help_button.collidepoint(event.pos):
                    help_menu(conn)
                if logout_button.collidepoint(event.pos):
                    LoggedIn = False
                    main_menu(conn)
                if quit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()
        clock.tick(120)


#  user is logged and he can: logout and go to the 'main_menu', play to play the game, help for tutorial, and quit


def play_menu(conn):
    while True:
        screen.fill((0, 0, 0))

        pygame.display.update()
        clock.tick(120)


def help_menu(conn):
    while True:
        screen.fill((0, 0, 0))

        pygame.display.update()
        clock.tick(120)


def connect(ip, port):
    """Connects to the server"""
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((ip, port))
    return client_socket


def main(ip, port):
    """Main function for the client"""
    client_socket = connect(ip, port)
    main_menu(client_socket)
    client_socket.close()


if __name__ == "__main__":
    main("127.0.0.1", 5000)
