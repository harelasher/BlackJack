import sys
import pygame
import string
import socket
from t import *
import ast
import time

# available chars for the username/password
available_chars = string.ascii_lowercase + string.digits


# (rect_x + rect_width // 2, rect_y + rect_height // 2) -->
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)


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
# all_medals = [pygame.transform.scale(first_place, (49, 49)), pygame.transform.scale(second_place, (49, 49)), pygame.transform.scale(third_place, (49, 49))]

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
        draw_text("save", HelveticaFont, "black", screen, save_pfp_button.x + save_pfp_button.w/2, save_pfp_button.y + save_pfp_button.h/2)

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
                    leaderboard_menu(conn, user_info)
                elif save_pfp_button.collidepoint(event.pos):
                    if pfp_pictures.index(big_pfp) != user_info[4]:
                        cmd, msg = build_send_recv_parse(conn, PROTOCOL_CLIENT["change_pfp"], user_info[1] + DATA_DELIMITER + str(pfp_pictures.index(big_pfp)))
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
    print(users_leaderboard)
    while True:
        screen.blit(overlay, (0, 0))
        draw_text("BlackJack", MainScreenFont, (255, 255, 255), screen, display_width // 2, 120 // 2)
        draw_text("leaderboard of the highscores", HelveticaFont, (255, 255, 255), screen, display_width // 2, 215 // 2)

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
            draw_text(str(i+1), ButtonFont, 'white', screen, 60, 180 + i*90)
            if i < 3:
                medal = all_medals[i]
                pfp_pic_rect = medal.get_rect()
                pfp_pic_rect.center = (135, 188 + i * 90)
                screen.blit(medal, pfp_pic_rect)

            user_pfp = pfp_pictures[users_leaderboard[i][1]]
            pfp_pic_rect = user_pfp.get_rect()
            pfp_pic_rect.center = (230, 180 + i*90)
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
                    draw_text("12222222222222222222222222", ButtonFont, "black", screen, 400, 400)
                # elif Highlighted_podium_rect.collidepoint(event.pos) and \
                #         Highlighted_podium_mask.get_at(
                #             (event.pos[0] - Highlighted_podium_rect.x, event.pos[1] - Highlighted_podium_rect.y)):
                #     pass
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return user_info
        pygame.display.update()
        clock.tick(120)


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
