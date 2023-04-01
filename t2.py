import sys
import pygame
import string
import socket
from t import *
import ast
import time

import queue
import threading

information_queue = queue.Queue()
stop_event = threading.Event()

# available chars for the username/password
available_chars = string.ascii_lowercase + string.digits


def circle_surface(color, radius, x, y, width=0):
    shape_surf = pygame.Surface((x * 2, y * 2), pygame.SRCALPHA)
    pygame.draw.circle(shape_surf, color, (x, y), radius, width)
    return shape_surf


# (rect_x + rect_width // 2, rect_y + rect_height // 2) -->
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)


# label_rect = textobj.get_rect(center=(x, y))
def draw_text_Left(text, font, color, surface, x, y, ):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)


def draw_text_Right(text, font, color, surface, x, y, ):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topright = (x, y)
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
Man = pygame.image.load('Pictures/Man.png').convert_alpha()
Highlighted_man = pygame.image.load('Pictures/Highlighted_man.png').convert_alpha()
Man2 = pygame.image.load('Pictures/Man2.png').convert_alpha()
Highlighted_man2 = pygame.image.load('Pictures/Highlighted_man2.png').convert_alpha()
woman = pygame.image.load('Pictures/woman.png').convert_alpha()
Highlighted_woman = pygame.image.load('Pictures/Highlighted_woman.png').convert_alpha()
woman2 = pygame.image.load('Pictures/woman2.png').convert_alpha()
Highlighted_woman2 = pygame.image.load('Pictures/Highlighted_woman2.png').convert_alpha()
pfp_pictures = [Man, Man2, woman, woman2]
podium = pygame.image.load('Pictures/podium.png').convert_alpha()
Highlighted_podium = pygame.image.load('Pictures/Highlighted_podium.png').convert_alpha()
Highlighted_pfp = [Highlighted_man, Highlighted_man2, Highlighted_woman, Highlighted_woman2]

first_place = pygame.image.load('Pictures/1st_medal.png').convert_alpha()
second_place = pygame.image.load('Pictures/2nd_medal.png').convert_alpha()
third_place = pygame.image.load('Pictures/3rd_medal.png').convert_alpha()
all_medals = [first_place, second_place, third_place]

bj_table = pygame.image.load('Pictures/blackjack_table.png').convert_alpha()
# Fonts
MainScreenFont = pygame.font.SysFont("gabriola", 80)
ButtonFont = pygame.font.Font("Fonts/Copperplate Gothic Bold Regular.ttf", 28)
MediumFont = pygame.font.SysFont("gabriola", 40)
LowFont = pygame.font.SysFont("gabriola", 20)
HelveticaFont = pygame.font.Font('Fonts/Copperplate Gothic Bold Regular.ttf', 20)

clock = pygame.time.Clock()
_circle_cache = {}


def _circlepoints(r):
    r = int(round(r))
    if r in _circle_cache:
        return _circle_cache[r]
    x, y, e = r, 0, 1 - r
    _circle_cache[r] = points = []
    while x >= y:
        points.append((x, y))
        y += 1
        if e < 0:
            e += 2 * y - 1
        else:
            x -= 1
            e += 2 * (y - x) - 1
    points += [(y, x) for x, y in points if x > y]
    points += [(-x, y) for x, y in points if x]
    points += [(x, -y) for x, y in points if y]
    points.sort()
    return points


def render1(text, font, gfcolor=pygame.Color('white'), ocolor=(0, 0, 0), opx=8):
    textsurface = font.render(text, True, gfcolor).convert_alpha()
    w = textsurface.get_width() + 2 * opx
    h = font.get_height()

    osurf = pygame.Surface((w, h + 2 * opx)).convert_alpha()
    osurf.fill((0, 0, 0, 0))

    surf = osurf.copy()

    osurf.blit(font.render(text, True, ocolor).convert_alpha(), (0, 0))

    for dx, dy in _circlepoints(opx):
        surf.blit(osurf, (dx + opx, dy + opx))

    surf.blit(textsurface, (opx, opx))
    return surf


def bj_screen():
    screen.blit(overlay, (0, 0))
    draw_text("BlackJack", MainScreenFont, (255, 255, 255), screen, display_width // 2, 120 // 2)
    draw_text("By Harel Asher", LowFont, (255, 255, 255), screen, display_width // 2, 215 // 2)


# to show to regular screen


def main_menu(conn):
    while True:
        bj_screen()

        login_button = pygame.Rect(265, 200, 270, 65)
        pygame.draw.rect(screen, "white", login_button, 3, border_radius=10)
        draw_text("login", ButtonFont, (255, 255, 255), screen, (login_button.x + login_button.w // 2),
                  (login_button.y + login_button.h // 2))

        Register_button = pygame.Rect(login_button.x, login_button.y + 110, login_button.w, login_button.h)
        pygame.draw.rect(screen, "white", Register_button, 3, border_radius=10)
        draw_text("register", ButtonFont, (255, 255, 255), screen, (Register_button.x + Register_button.w // 2),
                  (Register_button.y + login_button.h // 2))

        quit_button = pygame.Rect(Register_button.x, Register_button.y + 110, Register_button.w, Register_button.h)
        pygame.draw.rect(screen, "white", quit_button, 3, border_radius=10)
        draw_text("quit", ButtonFont, (255, 255, 255), screen, (quit_button.x + quit_button.w // 2),
                  (quit_button.y + Register_button.h // 2))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if login_button.collidepoint(event.pos):
                    login_menu(conn)
                elif Register_button.collidepoint(event.pos):
                    register_menu(conn)
                elif quit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()
        clock.tick(120)


# main screen of the game


def login_menu(conn):
    active_username = False
    active_password = False
    username_txt = ""
    password_txt = ""
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

        cursor = pygame.Rect((0, 0), (0, 0))
        if active_username:
            txt = ButtonFont.render(username_txt, True, (255, 255, 255))
            rect = txt.get_rect()
            rect.center = (username_button.x + username_button.w // 2,
                           username_button.y + username_button.h // 2)
            cursor = pygame.Rect(rect.topright, (3, rect.height))
        elif active_password:
            txt = ButtonFont.render(password_txt, True, (255, 255, 255))
            rect = txt.get_rect()
            rect.center = (password_button.x + password_button.w // 2,
                           password_button.y + password_button.h // 2)
            cursor = pygame.Rect(rect.topright, (3, rect.height))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if username_button.collidepoint(event.pos):
                    active_username = True
                elif password_button.collidepoint(event.pos):
                    active_password = True
                elif enter_button.collidepoint(event.pos):
                    cmd, msg = build_send_recv_parse(conn, PROTOCOL_CLIENT["login_msg"],
                                                     username_txt + DATA_DELIMITER + password_txt)
                    if cmd == 'LOGIN_OK':
                        loggedin_menu(conn, ast.literal_eval(msg))
                    else:
                        print(msg)
                if not username_button.collidepoint(event.pos):
                    active_username = False
                if not password_button.collidepoint(event.pos):
                    active_password = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
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

        if time.time() % 1 > 0.5 and (active_username or active_password):
            pygame.draw.rect(screen, 'white', cursor)
        pygame.display.update()
        clock.tick(120)


# login page


def register_menu(conn):
    active_username = False
    active_password = False
    username_txt = ""
    password_txt = ""

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

        cursor = pygame.Rect((0, 0), (0, 0))
        if active_username:
            txt = ButtonFont.render(username_txt, True, (255, 255, 255))
            rect = txt.get_rect()
            rect.center = (username_button.x + username_button.w // 2,
                           username_button.y + username_button.h // 2)
            cursor = pygame.Rect(rect.topright, (3, rect.height))
        elif active_password:
            txt = ButtonFont.render(password_txt, True, (255, 255, 255))
            rect = txt.get_rect()
            rect.center = (password_button.x + password_button.w // 2,
                           password_button.y + password_button.h // 2)
            cursor = pygame.Rect(rect.topright, (3, rect.height))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if username_button.collidepoint(event.pos):
                    active_username = True
                elif password_button.collidepoint(event.pos):
                    active_password = True
                elif enter_button.collidepoint(event.pos):
                    cmd, msg = build_send_recv_parse(conn, PROTOCOL_CLIENT["register_msg"],
                                                     username_txt + DATA_DELIMITER + password_txt)
                    if cmd == 'REGISTER_OK':
                        loggedin_menu(conn, ast.literal_eval(msg))
                    else:
                        print(msg)
                if not username_button.collidepoint(event.pos):
                    active_username = False
                if not password_button.collidepoint(event.pos):
                    active_password = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
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

        if time.time() % 1 > 0.5 and (active_username or active_password):
            pygame.draw.rect(screen, 'white', cursor)
        pygame.display.update()
        clock.tick(120)


# register page


def loggedin_menu(conn, user_info):
    print(user_info)
    while True:
        bj_screen()

        play_button = pygame.Rect(265, 190, 270, 65)
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
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if play_button.collidepoint(event.pos):
                    user_info = play_menu(conn, user_info)
                elif help_button.collidepoint(event.pos):
                    help_menu(conn, user_info)
                elif logout_button.collidepoint(event.pos):
                    build_and_send_message(conn, PROTOCOL_CLIENT["logout_msg"], user_info[1])
                    main_menu(conn)
                elif quit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()
        clock.tick(120)


#  user is logged and he can: logout and go to the 'main_menu', play to play the game, help for tutorial, and quit


def play_menu(conn, user_info):
    highlighted_podium_true = False
    highlighted_pfp_pic_true = False
    bj_txt_true = False
    while True:
        screen.blit(overlay, (0, 0))
        draw_text("BlackJack", MainScreenFont, (255, 255, 255), screen, display_width // 2, 120 // 2)
        draw_text(f"chips: {user_info[2]}", HelveticaFont, (255, 255, 255), screen, display_width // 2, 215 // 2)

        pfp_pic = pfp_pictures[user_info[4]]
        pfp_pic_rect = pfp_pic.get_rect()
        pfp_pic_rect.center = (display_width / 1.075, 120 // 2)
        screen.blit(pfp_pic, pfp_pic_rect)

        Highlighted_pfp_pic = Highlighted_pfp[user_info[4]]
        Highlighted_pfp_pic_rect = Highlighted_pfp_pic.get_rect()
        Highlighted_pfp_pic_rect.center = (display_width / 1.075, 120 // 2)
        pfp_pic_mask = pygame.mask.from_surface(Highlighted_pfp_pic)
        if highlighted_pfp_pic_true:
            screen.blit(Highlighted_pfp_pic, Highlighted_pfp_pic_rect)

        podium_rect = podium.get_rect()
        podium_rect.center = (display_width / 1.25, 120 // 2)
        screen.blit(podium, podium_rect)

        Highlighted_podium_rect = Highlighted_podium.get_rect()
        Highlighted_podium_rect.center = (display_width / 1.25, 120 // 2)
        Highlighted_podium_mask = pygame.mask.from_surface(Highlighted_podium)
        if highlighted_podium_true:
            screen.blit(Highlighted_podium, Highlighted_podium_rect)

        bj_txt = render1('BlackJack', MainScreenFont)
        blackjack_rect = bj_txt.get_rect()
        blackjack_rect.center = (display_width // 2, 120 // 2)
        BlackJack_mask = pygame.mask.from_surface(bj_txt)
        if bj_txt_true:
            screen.blit(bj_txt, blackjack_rect)

        table_button1 = pygame.Rect(100, 230, 140, 140)
        pygame.draw.rect(screen, "black", table_button1)

        table_button2 = pygame.Rect(table_button1.x + table_button1.w + 90, table_button1.y, table_button1.w,
                                    table_button1.h)
        pygame.draw.rect(screen, "black", table_button2)

        table_button3 = pygame.Rect(table_button2.x + table_button2.w + 90, table_button2.y, table_button2.w,
                                    table_button2.h)
        pygame.draw.rect(screen, "black", table_button3)

        for event in pygame.event.get():
            if event.type == pygame.MOUSEMOTION:
                if blackjack_rect.collidepoint(event.pos) and \
                        BlackJack_mask.get_at((event.pos[0] - blackjack_rect.x, event.pos[1] - blackjack_rect.y)):
                    bj_txt_true = True
                else:
                    bj_txt_true = False
                if Highlighted_pfp_pic_rect.collidepoint(event.pos) and \
                        pfp_pic_mask.get_at(
                            (event.pos[0] - Highlighted_pfp_pic_rect.x, event.pos[1] - Highlighted_pfp_pic_rect.y)):
                    highlighted_pfp_pic_true = True
                else:
                    highlighted_pfp_pic_true = False
                if Highlighted_podium_rect.collidepoint(event.pos) and \
                        Highlighted_podium_mask.get_at(
                            (event.pos[0] - Highlighted_podium_rect.x, event.pos[1] - Highlighted_podium_rect.y)):
                    highlighted_podium_true = True
                else:
                    highlighted_podium_true = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if blackjack_rect.collidepoint(event.pos) and \
                        BlackJack_mask.get_at((event.pos[0] - blackjack_rect.x, event.pos[1] - blackjack_rect.y)):
                    return user_info
                if Highlighted_pfp_pic_rect.collidepoint(event.pos) and \
                        pfp_pic_mask.get_at(
                            (event.pos[0] - Highlighted_pfp_pic_rect.x, event.pos[1] - Highlighted_pfp_pic_rect.y)):
                    highlighted_pfp_pic_true = False
                    user_info = profile_menu(conn, user_info)
                if Highlighted_podium_rect.collidepoint(event.pos) and \
                        Highlighted_podium_mask.get_at(
                            (event.pos[0] - Highlighted_podium_rect.x, event.pos[1] - Highlighted_podium_rect.y)):
                    highlighted_podium_true = False
                    leaderboard_menu(conn, user_info)
                if table_button1.collidepoint(event.pos):
                    table1(conn, user_info)
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return user_info
        pygame.display.update()
        clock.tick(120)


def profile_menu(conn, user_info):
    highlighted_podium_true = False
    highlighted_pfp_pic_true = False
    bj_txt_true = False
    big_pfp = pfp_pictures[user_info[4]]
    while True:
        screen.blit(overlay, (0, 0))
        draw_text("BlackJack", MainScreenFont, (255, 255, 255), screen, display_width // 2, 120 // 2)
        draw_text('profile page', HelveticaFont, (255, 255, 255), screen, display_width // 2, 215 // 2)

        pfp_pic = pfp_pictures[user_info[4]]
        pfp_pic_rect = pfp_pic.get_rect()
        pfp_pic_rect.center = (display_width / 1.075, 120 // 2)
        screen.blit(pfp_pic, pfp_pic_rect)

        Highlighted_pfp_pic = Highlighted_pfp[user_info[4]]
        Highlighted_pfp_pic_rect = Highlighted_pfp_pic.get_rect()
        Highlighted_pfp_pic_rect.center = (display_width / 1.075, 120 // 2)
        pfp_pic_mask = pygame.mask.from_surface(Highlighted_pfp_pic)
        if highlighted_pfp_pic_true:
            screen.blit(Highlighted_pfp_pic, Highlighted_pfp_pic_rect)

        podium_rect = podium.get_rect()
        podium_rect.center = (display_width / 1.25, 120 // 2)
        screen.blit(podium, podium_rect)

        Highlighted_podium_rect = Highlighted_podium.get_rect()
        Highlighted_podium_rect.center = (display_width / 1.25, 120 // 2)
        Highlighted_podium_mask = pygame.mask.from_surface(Highlighted_podium)
        if highlighted_podium_true:
            screen.blit(Highlighted_podium, Highlighted_podium_rect)

        bj_txt = render1('BlackJack', MainScreenFont)
        blackjack_rect = bj_txt.get_rect()
        blackjack_rect.center = (display_width // 2, 120 // 2)
        BlackJack_mask = pygame.mask.from_surface(bj_txt)
        if bj_txt_true:
            screen.blit(bj_txt, blackjack_rect)

        screen.blit(pygame.transform.scale(big_pfp, (250, 250)), (75, 170))
        save_pfp_button = pygame.Rect(120, 440, 160, 45)
        pygame.draw.rect(screen, "white", save_pfp_button)
        draw_text("save", HelveticaFont, "black", screen, save_pfp_button.x + save_pfp_button.w / 2,
                  save_pfp_button.y + save_pfp_button.h / 2)

        left_arrow = pygame.Rect(20, 290, 20, 45)
        pygame.draw.rect(screen, "white", left_arrow)
        right_arrow = pygame.Rect(360, 290, 20, 45)
        pygame.draw.rect(screen, "white", right_arrow)

        draw_text_Left("username:", HelveticaFont, (255, 255, 255), screen, display_width // 2, 330 // 2)
        Line1 = pygame.Rect(display_width // 2, 490 // 2, 340, 2)
        pygame.draw.rect(screen, "white", Line1)
        draw_text_Right(user_info[1], HelveticaFont, (255, 255, 255), screen, 740, 490 // 2 - 22)

        draw_text_Left("current chips:", HelveticaFont, (255, 255, 255), screen, display_width // 2, 500 // 2)
        Line2 = pygame.Rect(display_width // 2, 660 // 2, 340, 2)
        pygame.draw.rect(screen, "white", Line2)
        draw_text_Right(str(user_info[2]), HelveticaFont, (255, 255, 255), screen, 740, 660 // 2 - 22)

        draw_text_Left("biggest chips amount:", HelveticaFont, (255, 255, 255), screen, display_width // 2, 670 // 2)
        Line3 = pygame.Rect(display_width // 2, 830 // 2, 340, 2)
        pygame.draw.rect(screen, "white", Line3)
        draw_text_Right(str(user_info[3]), HelveticaFont, (255, 255, 255), screen, 740, 830 // 2 - 22)

        draw_text_Left("win/loss/push:", HelveticaFont, (255, 255, 255), screen, display_width // 2, 840 // 2)
        Line3 = pygame.Rect(display_width // 2, 1000 // 2, 340, 2)
        pygame.draw.rect(screen, "white", Line3)
        draw_text_Right(user_info[7], HelveticaFont, (255, 255, 255), screen, 740, 1000 // 2 - 22)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEMOTION:
                if blackjack_rect.collidepoint(event.pos) and \
                        BlackJack_mask.get_at((event.pos[0] - blackjack_rect.x, event.pos[1] - blackjack_rect.y)):
                    bj_txt_true = True
                else:
                    bj_txt_true = False
                if Highlighted_pfp_pic_rect.collidepoint(event.pos) and \
                        pfp_pic_mask.get_at(
                            (event.pos[0] - Highlighted_pfp_pic_rect.x, event.pos[1] - Highlighted_pfp_pic_rect.y)):
                    highlighted_pfp_pic_true = True
                else:
                    highlighted_pfp_pic_true = False
                if Highlighted_podium_rect.collidepoint(event.pos) and \
                        Highlighted_podium_mask.get_at(
                            (event.pos[0] - Highlighted_podium_rect.x, event.pos[1] - Highlighted_podium_rect.y)):
                    highlighted_podium_true = True
                else:
                    highlighted_podium_true = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if blackjack_rect.collidepoint(event.pos) and \
                        BlackJack_mask.get_at((event.pos[0] - blackjack_rect.x, event.pos[1] - blackjack_rect.y)):
                    return user_info
                # if Highlighted_pfp_pic_rect.collidepoint(event.pos) and \
                #         pfp_pic_mask.get_at(
                #             (event.pos[0] - Highlighted_pfp_pic_rect.x, event.pos[1] - Highlighted_pfp_pic_rect.y)):
                #     draw_text("click", ButtonFont, "black", screen, 400, 400)
                elif Highlighted_podium_rect.collidepoint(event.pos) and \
                        Highlighted_podium_mask.get_at(
                            (event.pos[0] - Highlighted_podium_rect.x, event.pos[1] - Highlighted_podium_rect.y)):
                    return leaderboard_menu(conn, user_info)
                elif save_pfp_button.collidepoint(event.pos):
                    if pfp_pictures.index(big_pfp) != user_info[4]:
                        cmd, msg = build_send_recv_parse(conn, PROTOCOL_CLIENT["change_pfp"],
                                                         user_info[1] + DATA_DELIMITER + str(
                                                             pfp_pictures.index(big_pfp)))
                        if cmd == PROTOCOL_SERVER['change_pfp_ok']:
                            user_info = ast.literal_eval(msg)
                elif right_arrow.collidepoint(event.pos):
                    if pfp_pictures.index(big_pfp) == 3:
                        big_pfp = pfp_pictures[0]
                    else:
                        big_pfp = pfp_pictures[pfp_pictures.index(big_pfp) + 1]
                elif left_arrow.collidepoint(event.pos):
                    big_pfp = pfp_pictures[pfp_pictures.index(big_pfp) - 1]
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return user_info
        pygame.display.update()
        clock.tick(120)


def leaderboard_menu(conn, user_info):
    highlighted_podium_true = False
    highlighted_pfp_pic_true = False
    bj_txt_true = False
    cmd, msg = build_send_recv_parse(conn, PROTOCOL_CLIENT["get_leaderboard"], "")
    users_leaderboard = ast.literal_eval(msg)
    prev_time = time.time()
    print(users_leaderboard)
    while True:
        screen.blit(overlay, (0, 0))
        draw_text("BlackJack", MainScreenFont, (255, 255, 255), screen, display_width // 2, 120 // 2)
        draw_text("leaderboard of the biggest scores", HelveticaFont, (255, 255, 255), screen, display_width // 2,
                  215 // 2)

        pfp_pic = pfp_pictures[user_info[4]]
        pfp_pic_rect = pfp_pic.get_rect()
        pfp_pic_rect.center = (display_width / 1.075, 120 // 2)
        screen.blit(pfp_pic, pfp_pic_rect)

        Highlighted_pfp_pic = Highlighted_pfp[user_info[4]]
        Highlighted_pfp_pic_rect = Highlighted_pfp_pic.get_rect()
        Highlighted_pfp_pic_rect.center = (display_width / 1.075, 120 // 2)
        pfp_pic_mask = pygame.mask.from_surface(Highlighted_pfp_pic)
        if highlighted_pfp_pic_true:
            screen.blit(Highlighted_pfp_pic, Highlighted_pfp_pic_rect)

        podium_rect = podium.get_rect()
        podium_rect.center = (display_width / 1.25, 120 // 2)
        screen.blit(podium, podium_rect)

        Highlighted_podium_rect = Highlighted_podium.get_rect()
        Highlighted_podium_rect.center = (display_width / 1.25, 120 // 2)
        Highlighted_podium_mask = pygame.mask.from_surface(Highlighted_podium)
        if highlighted_podium_true:
            screen.blit(Highlighted_podium, Highlighted_podium_rect)

        bj_txt = render1('BlackJack', MainScreenFont)
        blackjack_rect = bj_txt.get_rect()
        blackjack_rect.center = (display_width // 2, 120 // 2)
        BlackJack_mask = pygame.mask.from_surface(bj_txt)
        if bj_txt_true:
            screen.blit(bj_txt, blackjack_rect)

        for i in range(len(users_leaderboard)):
            draw_text(str(i + 1), ButtonFont, 'white', screen, 60, 180 + i * 90)
            if i < 3:
                medal = all_medals[i]
                pfp_pic_rect = medal.get_rect()
                pfp_pic_rect.center = (135, 188 + i * 90)
                screen.blit(medal, pfp_pic_rect)

            user_pfp = pfp_pictures[users_leaderboard[i][1]]
            pfp_pic_rect = user_pfp.get_rect()
            pfp_pic_rect.center = (230, 180 + i * 90)
            screen.blit(user_pfp, pfp_pic_rect)

            draw_text(users_leaderboard[i][0], ButtonFont, 'white', screen, 400, 180 + i * 90)

            draw_text(str(users_leaderboard[i][2]), ButtonFont, 'white', screen, 650, 180 + i * 90)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEMOTION:
                if blackjack_rect.collidepoint(event.pos) and \
                        BlackJack_mask.get_at((event.pos[0] - blackjack_rect.x, event.pos[1] - blackjack_rect.y)):
                    bj_txt_true = True
                else:
                    bj_txt_true = False
                if Highlighted_pfp_pic_rect.collidepoint(event.pos) and \
                        pfp_pic_mask.get_at(
                            (event.pos[0] - Highlighted_pfp_pic_rect.x, event.pos[1] - Highlighted_pfp_pic_rect.y)):
                    highlighted_pfp_pic_true = True
                else:
                    highlighted_pfp_pic_true = False
                if Highlighted_podium_rect.collidepoint(event.pos) and \
                        Highlighted_podium_mask.get_at(
                            (event.pos[0] - Highlighted_podium_rect.x, event.pos[1] - Highlighted_podium_rect.y)):
                    highlighted_podium_true = True
                else:
                    highlighted_podium_true = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if blackjack_rect.collidepoint(event.pos) and \
                        BlackJack_mask.get_at((event.pos[0] - blackjack_rect.x, event.pos[1] - blackjack_rect.y)):
                    return user_info
                if Highlighted_pfp_pic_rect.collidepoint(event.pos) and \
                        pfp_pic_mask.get_at(
                            (event.pos[0] - Highlighted_pfp_pic_rect.x, event.pos[1] - Highlighted_pfp_pic_rect.y)):
                    return profile_menu(conn, user_info)
                elif Highlighted_podium_rect.collidepoint(event.pos) and \
                        Highlighted_podium_mask.get_at(
                            (event.pos[0] - Highlighted_podium_rect.x, event.pos[1] - Highlighted_podium_rect.y)) \
                        and time.time() - prev_time >= 1:
                    prev_time += 3
                    cmd, msg = build_send_recv_parse(conn, PROTOCOL_CLIENT["get_leaderboard"], "")
                    users_leaderboard = ast.literal_eval(msg)
                    highlighted_podium_true = False
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return user_info
        pygame.display.update()
        clock.tick(120)


def receive_information_from_server(conn):
    while not stop_event.is_set():
        # replace this with your code to receive information from the server
        cmd, msg = recv_message_and_parse(conn)
        if msg:
            # add received information to the queue
            information_queue.put(msg)
    print("--closed thread--")


def table1(conn, user_info):
    stop_event.clear()
    server_thread = threading.Thread(target=receive_information_from_server, args=(conn, ))
    server_thread.start()
    build_and_send_message(conn, PROTOCOL_CLIENT["join_table"], "0")

    game_state = {
        "seats": [
            {
                "name": None,
                "profile_picture": None,
                "cards": None,
                "bet": None
            },
            {
                "name": None,
                "profile_picture": None,
                "cards": None,
                "bet": None
            },
            {
                "name": None,
                "profile_picture": None,
                "cards": None,
                "bet": None
            }
        ],
        "dealer": {
            "cards": None,
            "is_showing": False
        },
        "is_game_over": False,
        "winner": None
    }

    offset_x = None
    scroll_value = 0
    scroll_bar_rect = pygame.Rect(440, 540, 300, 20)

    # Define the rectangle of the scroll bar handle
    scroll_handle_rect = pygame.Rect(scroll_bar_rect.x, scroll_bar_rect.y - 5, 20, 30)
    left_button_rect = pygame.Rect(scroll_bar_rect.x - 40, scroll_bar_rect.y - 5, 30, 30)
    right_button_rect = pygame.Rect(scroll_bar_rect.x + scroll_bar_rect.w + 10, scroll_bar_rect.y - 5, 30, 30)

    taken_seat = None

    while True:
        try:
            information = information_queue.get_nowait()
            game_state = ast.literal_eval(str(information))
        except queue.Empty:
            pass

        bj_screen()
        screen.blit(bj_table, (-10, 0))

        hit_button = circle_surface("black", 50, 70, 180)  # (center coordinates), radius
        hit_mask = pygame.mask.from_surface(hit_button)

        stand_button = circle_surface("black", 50, 70, 180 + 120)  # (center coordinates), radius
        stand_mask = pygame.mask.from_surface(stand_button)

        double_down_button = circle_surface("black", 50, 70, 180 + 120 + 120)  # (center coordinates), radius
        double_down_mask = pygame.mask.from_surface(double_down_button)

        bet_amount_button = pygame.Rect(scroll_bar_rect.x - 50, 510, scroll_bar_rect.w + 100, 80)
        profile_picture = pygame.transform.scale(pfp_pictures[user_info[4]], (70, 70))

        mone = None
        for i in range(len(game_state["seats"])):
            if game_state["seats"][i]["name"] == user_info[1]:
                mone = i
        taken_seat = mone

        if taken_seat is None:
            table_seat1_noWidth = circle_surface("black", 32, 200, 400, 3)  # (center coordinates), radius
            table_seat1 = circle_surface("black", 32, 200, 400)
            table_seat1_mask = pygame.mask.from_surface(table_seat1)
            screen.blit(table_seat1_noWidth, (0, 0))
            draw_text("sit", HelveticaFont, "white", screen, 200, 390)
            draw_text("here", HelveticaFont, "white", screen, 200, 404)

            table_seat2_noWidth = circle_surface("black", 32, 400, 475, 3)  # (center coordinates), radius
            table_seat2 = circle_surface("black", 32, 400, 475)
            table_seat2_mask = pygame.mask.from_surface(table_seat2)
            screen.blit(table_seat2_noWidth, (0, 0))
            draw_text("sit", HelveticaFont, "white", screen, 400, 465)
            draw_text("here", HelveticaFont, "white", screen, 400, 479)

            table_seat3_noWidth = circle_surface("black", 32, 595, 400, 3)  # (center coordinates), radius
            table_seat3 = circle_surface("black", 32, 595, 400)
            table_seat3_mask = pygame.mask.from_surface(table_seat3)
            screen.blit(table_seat3_noWidth, (0, 0))
            draw_text("sit", HelveticaFont, "white", screen, 595, 390)
            draw_text("here", HelveticaFont, "white", screen, 595, 404)

        if game_state["seats"][0]["name"] is not None:
            profile_rect = profile_picture.get_rect(center=(200, 400))
            screen.blit(pygame.transform.scale(pfp_pictures[int(game_state["seats"][0]["profile_picture"])],
                                               (70, 70)), profile_rect)
            draw_text(game_state["seats"][0]["name"], HelveticaFont, "white", screen, 200, 435)

        if game_state["seats"][1]["name"] is not None:
            profile_rect = profile_picture.get_rect(center=(400, 475))
            screen.blit(pygame.transform.scale(pfp_pictures[int(game_state["seats"][1]["profile_picture"])],
                                               (70, 70)), profile_rect)
            draw_text(game_state["seats"][1]["name"], HelveticaFont, "white", screen, 400, 510)

        if game_state["seats"][2]["name"] is not None:
            profile_rect = profile_picture.get_rect(center=(595, 400))
            screen.blit(pygame.transform.scale(pfp_pictures[int(game_state["seats"][2]["profile_picture"])],
                                               (70, 70)), profile_rect)
            draw_text(game_state["seats"][2]["name"], HelveticaFont, "white", screen, 595, 435)

        if taken_seat is not None:
            screen.blit(hit_button, (0, 0))
            draw_text("hit", HelveticaFont, "white", screen, 70, 180)

            screen.blit(stand_button, (0, 0))
            draw_text("stand", HelveticaFont, "white", screen, 70, 180 + 120)

            screen.blit(double_down_button, (0, 0))
            draw_text("double", HelveticaFont, "white", screen, 70, 180 + 120 + 120 - 7)
            draw_text("down", HelveticaFont, "white", screen, 70, 180 + 120 + 120 + 7)

            pygame.draw.rect(screen, "black", bet_amount_button)
            draw_text("bet amount", HelveticaFont, "white", screen, bet_amount_button.x + bet_amount_button.w / 2,
                      bet_amount_button.y + 10)

            ##########
            MAX_VALUE = user_info[2]

            pygame.draw.rect(screen, 'GRAY', scroll_bar_rect)
            pygame.draw.rect(screen, 'BLACK', scroll_bar_rect, 2)

            # Draw the scroll handle
            pygame.draw.rect(screen, 'GRAY', scroll_handle_rect)
            pygame.draw.rect(screen, 'BLACK', scroll_handle_rect, 2)

            # Draw the label for the scroll value
            label = ButtonFont.render(str(scroll_value), True, 'white')
            rect = label.get_rect(
                center=(bet_amount_button.x + bet_amount_button.w / 2, scroll_bar_rect.y + scroll_bar_rect.h + 15))
            screen.blit(label, rect)

            # Draw the left button
            pygame.draw.rect(screen, 'GRAY', left_button_rect)
            pygame.draw.rect(screen, 'BLACK', left_button_rect, 2)
            left_button_label = ButtonFont.render("<", True, 'BLACK')
            left_button_label_rect = left_button_label.get_rect(center=left_button_rect.center)
            screen.blit(left_button_label, left_button_label_rect)

            # Draw the right button
            pygame.draw.rect(screen, 'GRAY', right_button_rect)
            pygame.draw.rect(screen, 'BLACK', right_button_rect, 2)
            right_button_label = ButtonFont.render(">", True, 'BLACK')
            right_button_label_rect = right_button_label.get_rect(center=right_button_rect.center)
            screen.blit(right_button_label, right_button_label_rect)

            cursor = pygame.Rect((rect.bottomleft[0], rect.bottomleft[1] - 5), (rect.width, 2))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                stop_event.set()
                build_and_send_message(conn, PROTOCOL_CLIENT["leave_game"],
                                       '0' + DATA_DELIMITER + str(taken_seat))
                server_thread.join()
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if taken_seat is not None:
                        build_and_send_message(conn, PROTOCOL_CLIENT["leave_seat"],
                                               '0' + DATA_DELIMITER + str(taken_seat))
                        taken_seat = None
                    else:
                        stop_event.set()
                        build_and_send_message(conn, PROTOCOL_CLIENT["leave_table"], "0")
                        server_thread.join()
                        return user_info
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if table_seat1_mask.get_rect().collidepoint(event.pos) and \
                        table_seat1_mask.get_at(
                            (event.pos[0] - table_seat1_mask.get_rect().x,
                             event.pos[1] - table_seat1_mask.get_rect().y)) and taken_seat is None and game_state["seats"][0]["name"] is None:
                    build_and_send_message(conn, PROTOCOL_CLIENT["join_seat"],
                                                     '0' + DATA_DELIMITER + '0')
                elif table_seat2.get_rect().collidepoint(event.pos) and \
                        table_seat2_mask.get_at(
                            (event.pos[0] - table_seat2_mask.get_rect().x,
                             event.pos[1] - table_seat2_mask.get_rect().y)) and taken_seat is None and game_state["seats"][1]["name"] is None:
                    build_and_send_message(conn, PROTOCOL_CLIENT["join_seat"],
                                                     '0' + DATA_DELIMITER + '1')
                elif table_seat3_mask.get_rect().collidepoint(event.pos) and \
                        table_seat3_mask.get_at(
                            (event.pos[0] - table_seat3_mask.get_rect().x,
                             event.pos[1] - table_seat3_mask.get_rect().y)) and taken_seat is None and game_state["seats"][2]["name"] is None:
                    build_and_send_message(conn, PROTOCOL_CLIENT["join_seat"],
                                                     '0' + DATA_DELIMITER + '2')
                if taken_seat is not None:
                    if hit_mask.get_rect().collidepoint(event.pos) and \
                            hit_mask.get_at(
                                (event.pos[0] - hit_mask.get_rect().x, event.pos[1] - hit_mask.get_rect().y)):
                        print("hit")
                    if stand_mask.get_rect().collidepoint(event.pos) and \
                            stand_mask.get_at(
                                (event.pos[0] - stand_mask.get_rect().x, event.pos[1] - stand_mask.get_rect().y)):
                        print("stand")
                    elif double_down_mask.get_rect().collidepoint(event.pos) and \
                            double_down_mask.get_at((event.pos[0] - double_down_mask.get_rect().x,
                                                     event.pos[1] - double_down_mask.get_rect().y)):
                        print("double_down")
                    elif scroll_bar_rect.collidepoint(event.pos):
                        # Set the offset for the scroll handle
                        scroll_handle_rect.x = event.pos[0] - scroll_handle_rect.w / 2
                        if scroll_handle_rect.x < scroll_bar_rect.x:
                            scroll_handle_rect.x = scroll_bar_rect.x
                        elif scroll_handle_rect.x + scroll_handle_rect.w > scroll_bar_rect.x + scroll_bar_rect.w:
                            scroll_handle_rect.x = scroll_bar_rect.x + scroll_bar_rect.w - scroll_handle_rect.w
                        scroll_value = int((scroll_handle_rect.x - scroll_bar_rect.left) / (
                                scroll_bar_rect.width - scroll_handle_rect.width) * MAX_VALUE)
                        offset_x = 1
                    elif left_button_rect.collidepoint(event.pos):
                        scroll_value = max(0, scroll_value - 1)
                        scroll_handle_rect.x = int(
                            scroll_bar_rect.left + scroll_value / MAX_VALUE * (
                                    scroll_bar_rect.width - scroll_handle_rect.width))
                        offset_x = None
                    elif right_button_rect.collidepoint(event.pos):
                        scroll_value = min(MAX_VALUE, scroll_value + 1)
                        scroll_handle_rect.x = int(
                            scroll_bar_rect.left + scroll_value / MAX_VALUE * (
                                    scroll_bar_rect.width - scroll_handle_rect.width))
                        offset_x = None
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and offset_x is not None and taken_seat is not None:
                    if scroll_bar_rect.x + scroll_bar_rect.w - scroll_handle_rect.w / 2 < event.pos[0]:
                        scroll_handle_rect.x = scroll_bar_rect.x + scroll_bar_rect.w - scroll_handle_rect.w
                    elif event.pos[0] - scroll_handle_rect.w / 2 < scroll_bar_rect.x:
                        scroll_handle_rect.x = scroll_bar_rect.x
                    else:
                        scroll_handle_rect.x = event.pos[0] - scroll_handle_rect.w / 2
                    offset_x = None
            elif event.type == pygame.MOUSEMOTION:
                if offset_x is not None and taken_seat is not None:
                    if scroll_bar_rect.x + scroll_bar_rect.w - scroll_handle_rect.w / 2 < event.pos[0]:
                        scroll_handle_rect.x = scroll_bar_rect.x + scroll_bar_rect.w - scroll_handle_rect.w
                    elif event.pos[0] - scroll_handle_rect.w / 2 < scroll_bar_rect.x:
                        scroll_handle_rect.x = scroll_bar_rect.x
                    else:
                        scroll_handle_rect.x = event.pos[0] - scroll_handle_rect.w / 2
                    # Update the scroll value based on the position of the scroll handle
                    scroll_value = int((scroll_handle_rect.x - scroll_bar_rect.left) / (
                            scroll_bar_rect.width - scroll_handle_rect.width) * MAX_VALUE)

        # pygame.draw.rect(screen, 'black', cursor)
        pygame.display.update()
        clock.tick(120)
        # print(game_state)


def help_menu(conn, user_info):
    help_screen = pygame.Surface((600, 400))  # the size of your rect
    help_screen.set_alpha(128)  # alpha level
    help_screen.fill((0, 0, 0))  # this fills the entire surface
    screen.blit(help_screen, (100, 155))  # (0,0) are the top-left coordinates
    help_screen_dimensions = pygame.Rect(100, 155, 600, 400)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if not help_screen_dimensions.collidepoint(event.pos):
                    return
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
    main("127.0.0.1", 51235)
