import sys
import pygame
import string
import socket
from networking_protocol import *
import ast
import time

import queue
import threading

information_queue = queue.Queue()
stop_event = threading.Event()

# available chars for the username/password
available_chars = string.ascii_lowercase + string.digits


def circle_surface(color, radius, x, y, width=0):
    """function to get circle surface"""
    shape_surf = pygame.Surface((x * 2, y * 2), pygame.SRCALPHA)
    pygame.draw.circle(shape_surf, color, (x, y), radius, width)
    return shape_surf


# (rect_x + rect_width // 2, rect_y + rect_height // 2) -->
def draw_text(text, font, color, surface, x, y, pos="center"):
    """function to draw text on the screen"""
    textobj = font.render(text, 1, color)
    # Render the text using the provided font and color
    textrect = textobj.get_rect()

    # Set the position of the text based on the provided 'pos' parameter
    if pos == "center":
        textrect.center = (x, y)
    elif pos == "topleft":
        textrect.topleft = (x, y)
    elif pos == "topright":
        textrect.topright = (x, y)
    elif pos == "bottomleft":
        textrect.bottomleft = (x, y)
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

visual_eye = pygame.transform.scale(pygame.image.load('Pictures/visual eye.png'), (50, 50))
left_arrow = pygame.transform.scale(pygame.image.load('Pictures/left-arrow.png'), (64, 64))
right_arrow = pygame.transform.rotate(pygame.transform.scale(pygame.image.load('Pictures/left-arrow.png'),
                                                             (64, 64)), 180)

Highlighted_BJ = pygame.image.load('Pictures/BlackJack_Highlighted.png').convert_alpha()
hourly_chips = pygame.image.load('Pictures/hourlyChips.png').convert_alpha()
Highlighted_hourly_chips = pygame.image.load('Pictures/HighlightedHourlyChips.png').convert_alpha()
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

table1_picture = pygame.transform.scale(pygame.image.load('Pictures/Table 1 picture.jpg'), (200, 200))
table2_picture = pygame.transform.scale(pygame.image.load('Pictures/table2.jpg'), (200, 200))
table3_picture = pygame.transform.scale(pygame.image.load('Pictures/table3.jpg'), (200, 200))
card_names = [
    "2c", "3c", "4c", "5c", "6c", "7c", "8c", "9c", "10c", "jc", "qc", "kc", "ac",
    "2d", "3d", "4d", "5d", "6d", "7d", "8d", "9d", "10d", "jd", "qd", "kd", "ad",
    "2h", "3h", "4h", "5h", "6h", "7h", "8h", "9h", "10h", "jh", "qh", "kh", "ah",
    "2s", "3s", "4s", "5s", "6s", "7s", "8s", "9s", "10s", "js", "qs", "ks", "as"
]
cards = {}
for card_name in card_names:
    # load every card
    card_image = pygame.image.load(f"cards/{card_name}.png")
    cards[card_name] = pygame.transform.scale(card_image, (48, 68))

bj_table = pygame.image.load('Pictures/blackjack_table.png').convert_alpha()
# Fonts
MainScreenFont = pygame.font.SysFont("gabriola", 80)
ButtonFont = pygame.font.Font("Fonts/Copperplate Gothic Bold Regular.ttf", 28)
MediumFont = pygame.font.SysFont("gabriola", 40)
LowFont = pygame.font.SysFont("gabriola", 20)
HelveticaFont = pygame.font.Font('Fonts/Copperplate Gothic Bold Regular.ttf', 20)
timer_font = pygame.font.SysFont("freesansbold", 25)

clock = pygame.time.Clock()
_circle_cache = {}
# frames per seconds
fps = 60


def bj_screen():
    """function for th default screen"""
    screen.blit(overlay, (0, 0))
    draw_text("BlackJack", MainScreenFont, (255, 255, 255), screen, display_width // 2, 120 // 2)
    draw_text("By Harel Asher", LowFont, (255, 255, 255), screen, display_width // 2, 215 // 2)


# to show to regular screen


def main_menu(conn):
    """main function for entering the game"""
    bj_txt_true = False
    while True:
        bj_screen()  # Display the Blackjack screen
        # Create login button
        login_button = pygame.Rect(265, 200, 270, 65)
        pygame.draw.rect(screen, "white", login_button, 3, border_radius=10)
        draw_text("login", ButtonFont, (255, 255, 255), screen, (login_button.x + login_button.w // 2),
                  (login_button.y + login_button.h // 2))
        # Create register button
        Register_button = pygame.Rect(login_button.x, login_button.y + 110, login_button.w, login_button.h)
        pygame.draw.rect(screen, "white", Register_button, 3, border_radius=10)
        draw_text("register", ButtonFont, (255, 255, 255), screen, (Register_button.x + Register_button.w // 2),
                  (Register_button.y + login_button.h // 2))
        # Create quit button
        quit_button = pygame.Rect(Register_button.x, Register_button.y + 110, Register_button.w, Register_button.h)
        pygame.draw.rect(screen, "white", quit_button, 3, border_radius=10)
        draw_text("quit", ButtonFont, (255, 255, 255), screen, (quit_button.x + quit_button.w // 2),
                  (quit_button.y + Register_button.h // 2))

        blackjack_rect = Highlighted_BJ.get_rect()
        blackjack_rect.center = (display_width // 2, 120 // 2)
        BlackJack_mask = pygame.mask.from_surface(Highlighted_BJ)
        if bj_txt_true:
            screen.blit(Highlighted_BJ, blackjack_rect)

        for event in pygame.event.get():
            if event.type == pygame.MOUSEMOTION:
                # Check if the mouse is over the Blackjack text and within the text's mask
                if blackjack_rect.collidepoint(event.pos) and \
                        BlackJack_mask.get_at((event.pos[0] - blackjack_rect.x, event.pos[1] - blackjack_rect.y)):
                    bj_txt_true = True
                else:
                    bj_txt_true = False
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Check which button is clicked
                if login_button.collidepoint(event.pos):
                    login_menu(conn)
                elif Register_button.collidepoint(event.pos):
                    register_menu(conn)
                elif quit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()
        clock.tick(fps)


# main screen of the game


def login_menu(conn):
    """login screen"""
    bj_txt_true = False
    active_username = False
    active_password = False
    username_txt = ""
    password_txt = ""
    hide_password = True
    used_info = " ", " "
    visual_eye.set_alpha(128)
    username_button = pygame.Rect(265, 240, 270, 60)

    password_button = pygame.Rect(username_button.x, username_button.y + 90, username_button.w,
                                  username_button.h)

    enter_button = pygame.Rect(username_button.x + 70, password_button.y + 90, username_button.w - 140,
                               username_button.h)
    error_msg = LowFont.render("", True, (255, 255, 255))
    error_msg_rect = error_msg.get_rect(center=(
        display_width / 2, (display_height / 2 + password_button.h + password_button.y) / 2 + password_button.h))
    error_msg.set_alpha(0)
    fade_direction = "in"
    while True:
        bj_screen()
        draw_text("login", ButtonFont, (255, 255, 255), screen, display_width // 2, 232 - 40)

        blackjack_rect = Highlighted_BJ.get_rect()
        blackjack_rect.center = (display_width // 2, 120 // 2)
        BlackJack_mask = pygame.mask.from_surface(Highlighted_BJ)
        if bj_txt_true:
            screen.blit(Highlighted_BJ, blackjack_rect)

        if len(password_txt) == 0:
            text_surf = HelveticaFont.render('password', True, "black")
            text_surf.set_alpha(111)
            text_rect = text_surf.get_rect(center=(password_button.x + password_button.w / 2, password_button.y
                                                   + password_button.h / 2))
            screen.blit(text_surf, text_rect)
        if len(username_txt) == 0:
            text_surf = HelveticaFont.render('username', True, "black")
            text_surf.set_alpha(111)
            text_rect = text_surf.get_rect(center=(username_button.x + username_button.w / 2, username_button.y
                                                   + username_button.h / 2))
            screen.blit(text_surf, text_rect)
        draw_text("enter", ButtonFont, (255, 255, 255), screen, (enter_button.x + enter_button.w // 2),
                  (enter_button.y + enter_button.h // 2))

        draw_text(username_txt, ButtonFont, (255, 255, 255), screen, username_button.x + username_button.w // 2,
                  username_button.y + username_button.h // 2)
        visual_eye_rec = pygame.Rect(password_button.x + password_button.w, password_button.y + 4,
                                     visual_eye.get_rect().w, visual_eye.get_rect().h)
        screen.blit(visual_eye, visual_eye_rec)
        pygame.draw.rect(screen, "white", enter_button, 3)
        pygame.draw.rect(screen, "white", username_button, 3, border_radius=10)
        pygame.draw.rect(screen, "white", password_button, 3, border_radius=10)

        if hide_password:
            draw_text(len(password_txt) * "*", ButtonFont, (255, 255, 255), screen,
                      password_button.x + password_button.w // 2,
                      password_button.y + password_button.h // 2)
        else:
            draw_text(password_txt, ButtonFont, (255, 255, 255), screen, password_button.x + password_button.w // 2,
                      password_button.y + password_button.h // 2)

        if error_msg.get_alpha() < 255 and fade_direction == "in":
            error_msg.set_alpha(error_msg.get_alpha() + 5)
        elif error_msg.get_alpha() > 0 and fade_direction == "out":
            error_msg.set_alpha(error_msg.get_alpha() - 5)
        screen.blit(error_msg, error_msg_rect)
        # Fade in/out error message

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
            if hide_password:
                txt = ButtonFont.render(len(password_txt) * "*", True, (255, 255, 255))
                rect = txt.get_rect()
                rect.center = (password_button.x + password_button.w // 2,
                               password_button.y + password_button.h // 2)
                cursor = pygame.Rect(rect.topright, (3, rect.height))

        for event in pygame.event.get():
            if event.type == pygame.MOUSEMOTION:
                if blackjack_rect.collidepoint(event.pos) and \
                        BlackJack_mask.get_at((event.pos[0] - blackjack_rect.x, event.pos[1] - blackjack_rect.y)):
                    bj_txt_true = True
                else:
                    bj_txt_true = False
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if blackjack_rect.collidepoint(event.pos) and \
                        BlackJack_mask.get_at((event.pos[0] - blackjack_rect.x, event.pos[1] - blackjack_rect.y)):
                    return
                if username_button.collidepoint(event.pos):
                    active_username = True
                elif password_button.collidepoint(event.pos):
                    active_password = True
                elif enter_button.collidepoint(event.pos):
                    if used_info != (username_txt, password_txt):
                        used_info = (username_txt, password_txt)
                        cmd, msg = build_send_recv_parse(conn, PROTOCOL_CLIENT["login_msg"],
                                                         username_txt + DATA_DELIMITER + password_txt)
                        if cmd == 'LOGIN_OK':
                            loggedin_menu(conn, ast.literal_eval(msg))
                        else:
                            error_msg = LowFont.render(msg, True, (255, 255, 255))
                            error_msg_rect = error_msg.get_rect(center=(display_width / 2, (
                                    display_height / 2 + password_button.h + password_button.y)
                                                                        / 2 + password_button.h))
                            error_msg.set_alpha(0)
                            fade_direction = "in"
                elif visual_eye_rec.collidepoint(event.pos):
                    hide_password = not hide_password
                if not username_button.collidepoint(event.pos) and not visual_eye_rec.collidepoint(event.pos):
                    active_username = False
                if not password_button.collidepoint(event.pos) and not visual_eye_rec.collidepoint(event.pos):
                    active_password = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
                if active_username:
                    # Handle username input
                    if event.key == pygame.K_BACKSPACE:
                        username_txt = username_txt[:-1]
                    elif len(username_txt) < 9 and event.unicode.lower() in available_chars:
                        username_txt += event.unicode.lower()
                    if fade_direction != "out":
                        error_msg.set_alpha(255)
                        fade_direction = "out"
                if active_password:
                    # Handle password input
                    if event.key == pygame.K_BACKSPACE:
                        password_txt = password_txt[:-1]
                    elif len(password_txt) < 9 and event.unicode.lower() in available_chars:
                        password_txt += event.unicode.lower()
                    if fade_direction != "out":
                        error_msg.set_alpha(255)
                        fade_direction = "out"

        if time.time() % 1 > 0.5 and (active_username or active_password):
            pygame.draw.rect(screen, 'white', cursor)
        pygame.display.update()
        clock.tick(fps)


# login page


def register_menu(conn):
    """register screen(similar to login)"""
    bj_txt_true = False
    active_username = False
    active_password = False
    username_txt = ""
    password_txt = ""
    hide_password = True
    used_info = " ", " "
    visual_eye.set_alpha(128)
    username_button = pygame.Rect(265, 240, 270, 60)

    password_button = pygame.Rect(username_button.x, username_button.y + 90, username_button.w,
                                  username_button.h)

    enter_button = pygame.Rect(username_button.x + 70, password_button.y + 90, username_button.w - 140,
                               username_button.h)
    error_msg = LowFont.render("", True, (255, 255, 255))
    error_msg_rect = error_msg.get_rect(center=(
        display_width / 2, (display_height / 2 + password_button.h + password_button.y) / 2 + password_button.h))
    error_msg.set_alpha(0)
    fade_direction = "in"
    while True:
        bj_screen()
        draw_text("register", ButtonFont, (255, 255, 255), screen, display_width // 2, 232 - 40)

        blackjack_rect = Highlighted_BJ.get_rect()
        blackjack_rect.center = (display_width // 2, 120 // 2)
        BlackJack_mask = pygame.mask.from_surface(Highlighted_BJ)
        if bj_txt_true:
            screen.blit(Highlighted_BJ, blackjack_rect)

        if len(password_txt) == 0:
            text_surf = HelveticaFont.render('password', True, "black")
            text_surf.set_alpha(111)
            text_rect = text_surf.get_rect(center=(password_button.x + password_button.w / 2, password_button.y
                                                   + password_button.h / 2))
            screen.blit(text_surf, text_rect)
        if len(username_txt) == 0:
            text_surf = HelveticaFont.render('username', True, "black")
            text_surf.set_alpha(111)
            text_rect = text_surf.get_rect(center=(username_button.x + username_button.w / 2, username_button.y
                                                   + username_button.h / 2))
            screen.blit(text_surf, text_rect)
        draw_text("enter", ButtonFont, (255, 255, 255), screen, (enter_button.x + enter_button.w // 2),
                  (enter_button.y + enter_button.h // 2))

        draw_text(username_txt, ButtonFont, (255, 255, 255), screen, username_button.x + username_button.w // 2,
                  username_button.y + username_button.h // 2)
        visual_eye_rec = pygame.Rect(password_button.x + password_button.w, password_button.y + 4,
                                     visual_eye.get_rect().w, visual_eye.get_rect().h)
        screen.blit(visual_eye, visual_eye_rec)
        pygame.draw.rect(screen, "white", enter_button, 3)
        pygame.draw.rect(screen, "white", username_button, 3, border_radius=10)
        pygame.draw.rect(screen, "white", password_button, 3, border_radius=10)

        if hide_password:
            draw_text(len(password_txt) * "*", ButtonFont, (255, 255, 255), screen,
                      password_button.x + password_button.w // 2,
                      password_button.y + password_button.h // 2)
        else:
            draw_text(password_txt, ButtonFont, (255, 255, 255), screen, password_button.x + password_button.w // 2,
                      password_button.y + password_button.h // 2)

        if error_msg.get_alpha() < 255 and fade_direction == "in":
            error_msg.set_alpha(error_msg.get_alpha() + 5)
        elif error_msg.get_alpha() > 0 and fade_direction == "out":
            error_msg.set_alpha(error_msg.get_alpha() - 5)
        screen.blit(error_msg, error_msg_rect)

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
            if hide_password:
                txt = ButtonFont.render(len(password_txt) * "*", True, (255, 255, 255))
                rect = txt.get_rect()
                rect.center = (password_button.x + password_button.w // 2,
                               password_button.y + password_button.h // 2)
                cursor = pygame.Rect(rect.topright, (3, rect.height))

        for event in pygame.event.get():
            if event.type == pygame.MOUSEMOTION:
                if blackjack_rect.collidepoint(event.pos) and \
                        BlackJack_mask.get_at((event.pos[0] - blackjack_rect.x, event.pos[1] - blackjack_rect.y)):
                    bj_txt_true = True
                else:
                    bj_txt_true = False
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if blackjack_rect.collidepoint(event.pos) and \
                        BlackJack_mask.get_at((event.pos[0] - blackjack_rect.x, event.pos[1] - blackjack_rect.y)):
                    return
                if username_button.collidepoint(event.pos):
                    active_username = True
                elif password_button.collidepoint(event.pos):
                    active_password = True
                elif enter_button.collidepoint(event.pos):
                    if used_info != (username_txt, password_txt):
                        used_info = (username_txt, password_txt)
                        cmd, msg = build_send_recv_parse(conn, PROTOCOL_CLIENT["register_msg"],
                                                         username_txt + DATA_DELIMITER + password_txt)
                        if cmd == 'REGISTER_OK':
                            loggedin_menu(conn, ast.literal_eval(msg))
                        else:
                            error_msg = LowFont.render(msg, True, (255, 255, 255))
                            error_msg_rect = error_msg.get_rect(center=(display_width / 2, (
                                    display_height / 2 + password_button.h + password_button.y)
                                                                        / 2 + password_button.h))
                            error_msg.set_alpha(0)
                            fade_direction = "in"
                elif visual_eye_rec.collidepoint(event.pos):
                    hide_password = not hide_password
                if not username_button.collidepoint(event.pos) and not visual_eye_rec.collidepoint(event.pos):
                    active_username = False
                if not password_button.collidepoint(event.pos) and not visual_eye_rec.collidepoint(event.pos):
                    active_password = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
                if active_username:
                    if event.key == pygame.K_BACKSPACE:
                        username_txt = username_txt[:-1]
                    elif len(username_txt) < 9 and event.unicode.lower() in available_chars:
                        username_txt += event.unicode.lower()
                    if fade_direction != "out":
                        error_msg.set_alpha(255)
                        fade_direction = "out"
                if active_password:
                    if event.key == pygame.K_BACKSPACE:
                        password_txt = password_txt[:-1]
                    elif len(password_txt) < 9 and event.unicode.lower() in available_chars:
                        password_txt += event.unicode.lower()
                    if fade_direction != "out":
                        error_msg.set_alpha(255)
                        fade_direction = "out"

        if time.time() % 1 > 0.5 and (active_username or active_password):
            pygame.draw.rect(screen, 'white', cursor)
        pygame.display.update()
        clock.tick(fps)


# register page


def loggedin_menu(conn, user_info):
    """screen after player logged in"""
    bj_txt_true = False
    while True:

        bj_screen()

        blackjack_rect = Highlighted_BJ.get_rect()
        blackjack_rect.center = (display_width // 2, 120 // 2)
        BlackJack_mask = pygame.mask.from_surface(Highlighted_BJ)
        if bj_txt_true:
            screen.blit(Highlighted_BJ, blackjack_rect)

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
            if event.type == pygame.MOUSEMOTION:
                if blackjack_rect.collidepoint(event.pos) and \
                        BlackJack_mask.get_at((event.pos[0] - blackjack_rect.x, event.pos[1] - blackjack_rect.y)):
                    bj_txt_true = True
                else:
                    bj_txt_true = False
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
                    help_menu()
                elif logout_button.collidepoint(event.pos):
                    build_and_send_message(conn, PROTOCOL_CLIENT["logout_msg"], user_info[1])
                    main_menu(conn)
                elif quit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()
        clock.tick(fps)


#  user is logged, and he can: logout and go to the 'main_menu', play to play the game, help for tutorial, and quit


def play_menu(conn, user_info):
    """player clicked on the play screen"""
    highlighted_podium_true = False
    highlighted_pfp_pic_true = False
    bj_txt_true = False
    Highlighted_hourly_pay_true = False
    response_msg = ""
    hourly_pay_msg = LowFont.render(response_msg, True, (255, 255, 255))
    hourly_pay_msg_rect = hourly_pay_msg.get_rect(center=(50, 50))
    hourly_pay_msg.set_alpha(0)
    fade_direction = ""
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

        hourly_pay_rect = hourly_chips.get_rect()
        hourly_pay_rect.center = (display_width * 0.075, 120 // 2)
        screen.blit(hourly_chips, hourly_pay_rect)

        Highlighted_hourly_pay_rect = Highlighted_hourly_chips.get_rect()
        Highlighted_hourly_pay_rect.center = (display_width * 0.075, 120 // 2)
        Highlighted_hourly_pay_mask = pygame.mask.from_surface(Highlighted_hourly_chips)
        if Highlighted_hourly_pay_true:
            screen.blit(Highlighted_hourly_chips, Highlighted_hourly_pay_rect)

        blackjack_rect = Highlighted_BJ.get_rect()
        blackjack_rect.center = (display_width // 2, 120 // 2)
        BlackJack_mask = pygame.mask.from_surface(Highlighted_BJ)
        if bj_txt_true:
            screen.blit(Highlighted_BJ, blackjack_rect)

        table_button1 = pygame.Rect(55, 195, 200, 200)
        pygame.draw.rect(screen, "black", table_button1)
        screen.blit(table1_picture, (table_button1.x, table_button1.y))

        table_button2 = pygame.Rect(table_button1.x + table_button1.w + 45, table_button1.y, table_button1.w,
                                    table_button1.h)
        pygame.draw.rect(screen, "black", table_button2)
        screen.blit(table2_picture, (table_button1.x + table_button1.w + 45, table_button1.y))

        table_button3 = pygame.Rect(table_button2.x + table_button2.w + 45, table_button2.y, table_button2.w,
                                    table_button2.h)
        pygame.draw.rect(screen, "black", table_button3)
        screen.blit(table3_picture, (table_button2.x + table_button2.w + 45, table_button2.y))

        draw_text("Click On Any Table out of the 3 To Join it and Play In It!", MediumFont, "white", screen,
                  display_width // 2, 490)
        if hourly_pay_msg.get_alpha() < 255 and fade_direction == "in":
            hourly_pay_msg.set_alpha(hourly_pay_msg.get_alpha() + 5)
        elif hourly_pay_msg.get_alpha() > 0 and fade_direction == "out":
            hourly_pay_msg.set_alpha(hourly_pay_msg.get_alpha() - 5)
        if response_msg != "":
            screen.blit(hourly_pay_msg, hourly_pay_msg_rect)

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
                if Highlighted_hourly_pay_rect.collidepoint(event.pos) and \
                        Highlighted_hourly_pay_mask.get_at(
                            (event.pos[0] - Highlighted_hourly_pay_rect.x,
                             event.pos[1] - Highlighted_hourly_pay_rect.y)):
                    Highlighted_hourly_pay_true = True
                else:
                    Highlighted_hourly_pay_true = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if blackjack_rect.collidepoint(event.pos) and \
                        BlackJack_mask.get_at((event.pos[0] - blackjack_rect.x, event.pos[1] - blackjack_rect.y)):
                    return user_info
                elif Highlighted_pfp_pic_rect.collidepoint(event.pos) and \
                        pfp_pic_mask.get_at(
                            (event.pos[0] - Highlighted_pfp_pic_rect.x, event.pos[1] - Highlighted_pfp_pic_rect.y)):
                    hourly_pay_msg.set_alpha(0)
                    fade_direction = "out"
                    highlighted_pfp_pic_true = False
                    user_info = profile_menu(conn, user_info)
                elif Highlighted_podium_rect.collidepoint(event.pos) and \
                        Highlighted_podium_mask.get_at(
                            (event.pos[0] - Highlighted_podium_rect.x, event.pos[1] - Highlighted_podium_rect.y)):
                    hourly_pay_msg.set_alpha(0)
                    fade_direction = "out"
                    highlighted_podium_true = False
                    leaderboard_menu(conn, user_info)
                elif Highlighted_hourly_pay_rect.collidepoint(event.pos) and \
                        Highlighted_hourly_pay_mask.get_at(
                            (
                                    event.pos[0] - Highlighted_hourly_pay_rect.x,
                                    event.pos[1] - Highlighted_hourly_pay_rect.y)) \
                        and (hourly_pay_msg.get_alpha() == 255 or hourly_pay_msg.get_alpha() == 0):
                    cmd, msg = build_send_recv_parse(conn, PROTOCOL_CLIENT["check_hour"], user_info[1])
                    if cmd == PROTOCOL_SERVER["update_info"]:
                        arr = ast.literal_eval(msg)
                        user_info = arr[0]
                        if arr[1][0]:
                            response_msg = "you earned 1000 chips!"
                        else:
                            if arr[1][1] == 0:
                                response_msg = "reward available in less then a minute!"
                            else:
                                response_msg = f"reward available in {arr[1][1]} minutes!"
                        hourly_pay_msg = LowFont.render(response_msg, True, (255, 255, 255))
                        hourly_pay_msg_rect = hourly_pay_msg.get_rect(topleft=(Highlighted_hourly_pay_rect.x, 205 // 2))
                        hourly_pay_msg.set_alpha(0)
                        fade_direction = "in"
                elif table_button1.collidepoint(event.pos):
                    cmd, msg = build_send_recv_parse(conn, PROTOCOL_CLIENT["join_table"],
                                                     user_info[1] + DATA_DELIMITER + "0")
                    if cmd != 'ERROR':
                        hourly_pay_msg.set_alpha(0)
                        fade_direction = "out"
                        user_info = table1(conn, user_info, "0", ast.literal_eval(msg))
                elif table_button2.collidepoint(event.pos):
                    cmd, msg = build_send_recv_parse(conn, PROTOCOL_CLIENT["join_table"],
                                                     user_info[1] + DATA_DELIMITER + "1")
                    if cmd != 'ERROR':
                        hourly_pay_msg.set_alpha(0)
                        fade_direction = "out"
                        user_info = table1(conn, user_info, "1", ast.literal_eval(msg))
                elif table_button3.collidepoint(event.pos):
                    cmd, msg = build_send_recv_parse(conn, PROTOCOL_CLIENT["join_table"],
                                                     user_info[1] + DATA_DELIMITER + "2")
                    if cmd != 'ERROR':
                        hourly_pay_msg.set_alpha(0)
                        fade_direction = "out"
                        user_info = table1(conn, user_info, "2", ast.literal_eval(msg))
                elif fade_direction != "out" and hourly_pay_msg.get_alpha() == 255:
                    fade_direction = "out"
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return user_info

        pygame.display.update()
        clock.tick(fps)


def profile_menu(conn, user_info):
    """profile screen"""
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

        blackjack_rect = Highlighted_BJ.get_rect()
        blackjack_rect.center = (display_width // 2, 120 // 2)
        BlackJack_mask = pygame.mask.from_surface(Highlighted_BJ)
        if bj_txt_true:
            screen.blit(Highlighted_BJ, blackjack_rect)

        screen.blit(pygame.transform.scale(big_pfp, (250, 250)), (75, 170))
        save_pfp_button = pygame.Rect(120, 440, 160, 45)
        pygame.draw.rect(screen, "white", save_pfp_button)
        draw_text("save", HelveticaFont, "black", screen, save_pfp_button.x + save_pfp_button.w / 2,
                  save_pfp_button.y + save_pfp_button.h / 2)

        left_arrow_rect = pygame.Rect(0, 275, 64, 64)
        left_arrow_mask = pygame.mask.from_surface(left_arrow)
        screen.blit(left_arrow, left_arrow_rect)

        right_arrow_rect = pygame.Rect(340, 275, 64, 64)
        right_arrow_mask = pygame.mask.from_surface(right_arrow)
        screen.blit(right_arrow, right_arrow_rect)

        draw_text("username:", HelveticaFont, (255, 255, 255), screen, display_width // 2, 330 // 2, "topleft")
        Line1 = pygame.Rect(display_width // 2, 490 // 2, 340, 2)
        pygame.draw.rect(screen, "white", Line1)
        draw_text(user_info[1], HelveticaFont, (255, 255, 255), screen, 740, 490 // 2 - 22, "topright")

        draw_text("current chips:", HelveticaFont, (255, 255, 255), screen, display_width // 2, 500 // 2, "topleft")
        Line2 = pygame.Rect(display_width // 2, 660 // 2, 340, 2)
        pygame.draw.rect(screen, "white", Line2)
        draw_text(str(user_info[2]), HelveticaFont, (255, 255, 255), screen, 740, 660 // 2 - 22, "topright")

        draw_text("biggest chips amount:", HelveticaFont, (255, 255, 255), screen, display_width // 2, 670 // 2,
                  "topleft")
        Line3 = pygame.Rect(display_width // 2, 830 // 2, 340, 2)
        pygame.draw.rect(screen, "white", Line3)
        draw_text(str(user_info[3]), HelveticaFont, (255, 255, 255), screen, 740, 830 // 2 - 22, "topright")

        draw_text("win/loss/push:", HelveticaFont, (255, 255, 255), screen, display_width // 2, 840 // 2, "topleft")
        Line3 = pygame.Rect(display_width // 2, 1000 // 2, 340, 2)
        pygame.draw.rect(screen, "white", Line3)
        draw_text(user_info[7], HelveticaFont, (255, 255, 255), screen, 740, 1000 // 2 - 22, "topright")
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
                elif right_arrow_rect.collidepoint(event.pos) and \
                        right_arrow_mask.get_at(
                            (event.pos[0] - right_arrow_rect.x, event.pos[1] - right_arrow_rect.y)):
                    if pfp_pictures.index(big_pfp) == 3:
                        big_pfp = pfp_pictures[0]
                    else:
                        big_pfp = pfp_pictures[pfp_pictures.index(big_pfp) + 1]
                elif left_arrow_rect.collidepoint(event.pos) and \
                        left_arrow_mask.get_at(
                            (event.pos[0] - left_arrow_rect.x, event.pos[1] - left_arrow_rect.y)):
                    big_pfp = pfp_pictures[pfp_pictures.index(big_pfp) - 1]
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return user_info
        pygame.display.update()
        clock.tick(fps)


def leaderboard_menu(conn, user_info):
    """leaderboard screen"""
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

        blackjack_rect = Highlighted_BJ.get_rect()
        blackjack_rect.center = (display_width // 2, 120 // 2)
        BlackJack_mask = pygame.mask.from_surface(Highlighted_BJ)
        if bj_txt_true:
            screen.blit(Highlighted_BJ, blackjack_rect)

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
        clock.tick(fps)


def receive_information_from_server(conn):
    """listens to the information from the server"""
    cmd, msg = "", ""
    while not stop_event.is_set():
        # receive information from the server
        try:
            cmd, msg = recv_message_and_parse(conn)
        except ConnectionResetError or ConnectionAbortedError:
            stop_event.set()
            information_queue.put((PROTOCOL_SERVER["error_msg"], "[]"))
        if msg:
            # add received information to the queue
            information_queue.put((cmd, msg))
    print("--closed thread--")


def table1(conn, user_info, chosen_table, game_state):
    """function for playing the table"""
    stop_event.clear()
    info_thread = threading.Thread(target=receive_information_from_server, args=(conn,))
    info_thread.start()
    offset_x = None
    bj_txt_true = False
    adjusted_close_time = 0
    adjusted_start_time = 0
    scroll_value = 0
    scroll_bar_rect = pygame.Rect(52, 550, 300, 20)
    value_bet = 0

    # Define the rectangle of the scroll bar handle
    scroll_handle_rect = pygame.Rect(scroll_bar_rect.x, scroll_bar_rect.y - 5, 20, 30)
    left_button_rect = pygame.Rect(scroll_bar_rect.x - 40, scroll_bar_rect.y - 5, 30, 30)
    right_button_rect = pygame.Rect(scroll_bar_rect.x + scroll_bar_rect.w + 10, scroll_bar_rect.y - 5, 30, 30)

    bone = True
    remaining_time = 1

    table_seat1_noWidth = circle_surface("black", 32, 200, 400, 3)  # (center coordinates), radius
    table_seat1 = circle_surface("black", 32, 200, 400)
    table_seat1_mask = pygame.mask.from_surface(table_seat1)

    table_seat2_noWidth = circle_surface("black", 32, 400, 475, 3)  # (center coordinates), radius
    table_seat2 = circle_surface("black", 32, 400, 475)
    table_seat2_mask = pygame.mask.from_surface(table_seat2)

    table_seat3_noWidth = circle_surface("black", 32, 595, 400, 3)  # (center coordinates), radius
    table_seat3 = circle_surface("black", 32, 595, 400)
    table_seat3_mask = pygame.mask.from_surface(table_seat3)

    MAX_VALUE = user_info[2]
    while True:

        try:
            # retrieves the information from the thread function
            cmd, msg = information_queue.get_nowait()
            var = ast.literal_eval(msg)
            if cmd == PROTOCOL_SERVER["update_info"]:
                user_info = var
            elif cmd == PROTOCOL_SERVER["get_info_table"]:
                if var["timer"] != game_state["timer"]:
                    bone = True
                game_state = var
            elif cmd == PROTOCOL_SERVER["error_msg"]:
                return connection_stopped()
            print(var)
        except queue.Empty:
            pass

        screen.blit(overlay, (0, 0))
        draw_text("BlackJack", MainScreenFont, (255, 255, 255), screen, display_width // 2, 120 // 2)
        draw_text(f"chips: {user_info[2]}", HelveticaFont, (255, 255, 255), screen, display_width // 2, 215 // 2)
        draw_text(f"table {str(int(chosen_table) + 1)}", HelveticaFont, (255, 255, 255), screen, 50, 60)
        screen.blit(bj_table, (-10, 0))

        hit_button = circle_surface("black", 50, 70, 180)  # (center coordinates), radius
        hit_mask = pygame.mask.from_surface(hit_button)

        stand_button = circle_surface("black", 50, 70, 180 + 120)  # (center coordinates), radius
        stand_mask = pygame.mask.from_surface(stand_button)

        double_down_button = circle_surface("black", 50, 70, 180 + 120 + 120)  # (center coordinates), radius
        double_down_mask = pygame.mask.from_surface(double_down_button)

        bet_amount_button = pygame.Rect(scroll_bar_rect.x - 50, 526, scroll_bar_rect.w + 100, 72)
        profile_picture = pygame.transform.scale(pfp_pictures[user_info[4]], (70, 70))

        bet_rect = pygame.Rect(bet_amount_button.x + bet_amount_button.w + 1, bet_amount_button.y + 36, 60, 30)
        undo_rect = pygame.Rect(bet_rect.x, bet_rect.y - bet_rect.h - 1, 60, 30)

        mone = None
        for i in range(len(game_state["seats"])):
            if game_state["seats"][i]["name"] == user_info[1]:
                mone = i
        taken_seat = mone

        if taken_seat is None and game_state["is_game_over"] is True and user_info[2] >= 1:
            screen.blit(table_seat1_noWidth, (0, 0))
            draw_text("sit", HelveticaFont, "white", screen, 200, 390)
            draw_text("here", HelveticaFont, "white", screen, 200, 404)

            screen.blit(table_seat2_noWidth, (0, 0))
            draw_text("sit", HelveticaFont, "white", screen, 400, 465)
            draw_text("here", HelveticaFont, "white", screen, 400, 479)

            screen.blit(table_seat3_noWidth, (0, 0))
            draw_text("sit", HelveticaFont, "white", screen, 595, 390)
            draw_text("here", HelveticaFont, "white", screen, 595, 404)

        if game_state["seats"][0]["name"] is not None:
            profile_rect = profile_picture.get_rect(center=(200, 400))
            screen.blit(pygame.transform.scale(pfp_pictures[int(game_state["seats"][0]["profile_picture"])],
                                               (70, 70)), profile_rect)
            draw_text(game_state["seats"][0]["name"], HelveticaFont, "white", screen, 200, 435)
            if game_state["seats"][0]["name"] == user_info[1]:
                draw_text(game_state["seats"][0]["name"], HelveticaFont, "red", screen, 200, 435)
            if game_state["seats"][0]["bet"] is not None:
                draw_text(game_state["seats"][0]["bet"], HelveticaFont, "white", screen, 200, 375)
            if game_state["seats"][0]["result"] is not None:
                for i in range(len(game_state["seats"][0]["cards"])):
                    screen.blit(cards[game_state["seats"][0]["cards"][i]], (180 + 15 * i, 290))
                draw_text(game_state["seats"][0]["result"][0], HelveticaFont, "black", screen, 200, 280)
                if game_state["seats"][0]["result"][1] is not None:
                    draw_text(game_state["seats"][0]["result"][1], HelveticaFont, "black", screen, 200, 300)
            if game_state["seats"][0]["wlp"] is not None:
                draw_text(game_state["seats"][0]["wlp"], ButtonFont, "black", screen, 200, 400)

        if game_state["seats"][1]["name"] is not None:
            profile_rect = profile_picture.get_rect(center=(400, 475))
            screen.blit(pygame.transform.scale(pfp_pictures[int(game_state["seats"][1]["profile_picture"])],
                                               (70, 70)), profile_rect)
            draw_text(game_state["seats"][1]["name"], HelveticaFont, "white", screen, 400, 510)
            if game_state["seats"][1]["name"] == user_info[1]:
                draw_text(game_state["seats"][1]["name"], HelveticaFont, "red", screen, 400, 510)
            if game_state["seats"][1]["bet"] is not None:
                draw_text(game_state["seats"][1]["bet"], HelveticaFont, "white", screen, 400, 450)
            if game_state["seats"][1]["result"] is not None:
                for i in range(len(game_state["seats"][1]["cards"])):
                    screen.blit(cards[game_state["seats"][1]["cards"][i]], (350 + 15 * i, 360))
                draw_text(game_state["seats"][1]["result"][0], HelveticaFont, "black", screen, 400, 350)
                if game_state["seats"][1]["result"][1] is not None:
                    draw_text(game_state["seats"][1]["result"][1], HelveticaFont, "black", screen, 400, 375)
            if game_state["seats"][1]["wlp"] is not None:
                draw_text(game_state["seats"][1]["wlp"], ButtonFont, "black", screen, 400, 475)

        if game_state["seats"][2]["name"] is not None:
            profile_rect = profile_picture.get_rect(center=(595, 400))
            screen.blit(pygame.transform.scale(pfp_pictures[int(game_state["seats"][2]["profile_picture"])],
                                               (70, 70)), profile_rect)
            draw_text(game_state["seats"][2]["name"], HelveticaFont, "white", screen, 595, 435)
            if game_state["seats"][2]["name"] == user_info[1]:
                draw_text(game_state["seats"][2]["name"], HelveticaFont, "red", screen, 595, 435)
            if game_state["seats"][2]["bet"] is not None:
                draw_text(game_state["seats"][2]["bet"], HelveticaFont, "white", screen, 595, 375)
            if game_state["seats"][2]["result"] is not None:
                for i in range(len(game_state["seats"][2]["cards"])):
                    screen.blit(cards[game_state["seats"][2]["cards"][i]], (530 + 15 * i, 290))
                draw_text(game_state["seats"][2]["result"][0], HelveticaFont, "black", screen, 595, 280)
                if game_state["seats"][2]["result"][1] is not None:
                    draw_text(game_state["seats"][2]["result"][1], HelveticaFont, "black", screen, 595, 300)
            if game_state["seats"][2]["wlp"] is not None:
                draw_text(game_state["seats"][2]["wlp"], ButtonFont, "black", screen, 595, 400)

        if game_state["dealer"]["result"][0] is not None:
            for i in range(len(game_state["dealer"]["cards"])):
                screen.blit(cards[game_state["dealer"]["cards"][i]], (360 + 15 * i, 150))
            draw_text(game_state["dealer"]["result"][0], HelveticaFont, "black", screen, 400, 240)

        if game_state["timer"][0] is not None and bone:
            start_time, close_time, server_current_time = game_state["timer"]
            client_current_time = time.time()

            # Calculate time difference between server and client
            time_diff = client_current_time - server_current_time

            # Adjust start_time and close_time for client
            adjusted_start_time = start_time + time_diff
            adjusted_close_time = close_time + time_diff
            bone = False
        if game_state["timer"][0] is not None and not bone:
            current_time = time.time()
            remaining_time = max(adjusted_close_time - current_time, 0)
            if remaining_time == 0:
                bone = True
                game_state["timer"] = [None, None, None]
                print("new ", game_state)
            total_width = 300
            bar_width = int(total_width * remaining_time / (adjusted_close_time - adjusted_start_time))
            pygame.draw.rect(screen, (0, 0, 0), (250, 122, total_width, 20))
            pygame.draw.rect(screen, (255, 0, 0), (250, 122, bar_width, 20))
            text = timer_font.render("Time Remaining To React: {:.1f}s".format(remaining_time), True, "white")
            if game_state["is_game_over"]:
                text = timer_font.render("Time Remaining To Bet: {:.1f}s".format(remaining_time), True, "white")
            # elif len(game_state["dealer"]["cards"]) > 1:
            #     text = font.render("Finishing Game...".format(remaining_time), True, "white")
            text_rec = text.get_rect(center=(250 + total_width / 2, 122 + 20 / 2))
            screen.blit(text, text_rec)

        if taken_seat is not None:
            if game_state["is_game_over"] is False:
                if len(game_state["seats"][taken_seat]["cards"]) > 0 and game_state["seats"][taken_seat][
                    "reaction"] is None and game_state["seats"][taken_seat]["result"][1] is None and len(
                        game_state["dealer"]["cards"]) == 1 and remaining_time != 0:
                    hit_button = circle_surface("green", 50, 70, 180)  # (center coordinates), radius

                screen.blit(hit_button, (0, 0))
                draw_text("hit", HelveticaFont, "white", screen, 70, 180)

                if len(game_state["seats"][taken_seat]["cards"]) > 0 and game_state["seats"][taken_seat][
                    "reaction"] is None and game_state["seats"][taken_seat]["result"][1] is None and len(
                        game_state["dealer"]["cards"]) == 1 and remaining_time != 0:
                    stand_button = circle_surface("red", 50, 70, 180 + 120)  # (center coordinates), radius
                screen.blit(stand_button, (0, 0))
                draw_text("stand", HelveticaFont, "white", screen, 70, 180 + 120)

                if len(game_state["seats"][taken_seat]["cards"]) > 0 and user_info[2] >= value_bet * 2 and \
                        game_state["seats"][taken_seat]["reaction"] is None and \
                        game_state["seats"][taken_seat]["result"][1] is None and len(
                    game_state["seats"][taken_seat]["cards"]) == 2 and len(
                        game_state["dealer"]["cards"]) == 1 and remaining_time != 0:
                    double_down_button = circle_surface("purple", 50, 70,
                                                        180 + 120 + 120)  # (center coordinates), radius

                screen.blit(double_down_button, (0, 0))
                draw_text("double", HelveticaFont, "white", screen, 70, 180 + 120 + 120 - 7)
                draw_text("down", HelveticaFont, "white", screen, 70, 180 + 120 + 120 + 7)
            else:
                pygame.draw.rect(screen, "black", bet_amount_button)
                draw_text("bet amount", HelveticaFont, "white", screen, bet_amount_button.x + bet_amount_button.w / 2,
                          bet_amount_button.y + 10)

                ##########

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

                pygame.draw.rect(screen, 'black', bet_rect)
                pygame.draw.rect(screen, 'black', undo_rect)

                if scroll_value != 0 and game_state["is_game_over"] is True and\
                        game_state["seats"][taken_seat]["bet"] is None:
                    pygame.draw.rect(screen, 'green', bet_rect)
                if game_state["seats"][taken_seat]["bet"] is not None and game_state["is_game_over"] is True:
                    pygame.draw.rect(screen, 'red', undo_rect)
                draw_text("bet", HelveticaFont, "white", screen, bet_rect.x + bet_rect.w / 2,
                          bet_rect.y + bet_rect.h / 2)
                draw_text("undo", HelveticaFont, "white", screen, undo_rect.x + undo_rect.w / 2,
                          undo_rect.y + undo_rect.h / 2)

        blackjack_rect = Highlighted_BJ.get_rect()
        blackjack_rect.center = (display_width // 2, 120 // 2)
        BlackJack_mask = pygame.mask.from_surface(Highlighted_BJ)
        if bj_txt_true:
            screen.blit(Highlighted_BJ, blackjack_rect)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEMOTION:
                if blackjack_rect.collidepoint(event.pos) and \
                        BlackJack_mask.get_at((event.pos[0] - blackjack_rect.x, event.pos[1] - blackjack_rect.y)):
                    bj_txt_true = True
                else:
                    bj_txt_true = False
            if event.type == pygame.QUIT:
                stop_event.set()
                build_and_send_message(conn, PROTOCOL_CLIENT["leave_game"],
                                       user_info[1] + DATA_DELIMITER + chosen_table + DATA_DELIMITER + str(taken_seat))
                info_thread.join()
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if taken_seat is not None and game_state["is_game_over"]:
                        build_and_send_message(conn, PROTOCOL_CLIENT["leave_seat"],
                                               chosen_table + DATA_DELIMITER + str(taken_seat))
                        taken_seat = None
                    elif taken_seat is None:
                        stop_event.set()
                        build_and_send_message(conn, PROTOCOL_CLIENT["leave_table"], chosen_table)
                        info_thread.join()
                        return user_info
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if blackjack_rect.collidepoint(event.pos) and \
                        BlackJack_mask.get_at((event.pos[0] - blackjack_rect.x, event.pos[1] - blackjack_rect.y)):
                    if taken_seat is not None and game_state["is_game_over"]:
                        build_and_send_message(conn, PROTOCOL_CLIENT["leave_seat"],
                                               chosen_table + DATA_DELIMITER + str(taken_seat))
                        taken_seat = None
                    elif taken_seat is None:
                        stop_event.set()
                        build_and_send_message(conn, PROTOCOL_CLIENT["leave_table"], chosen_table)
                        info_thread.join()
                        return user_info
                if table_seat1_mask.get_rect().collidepoint(event.pos) and \
                        table_seat1_mask.get_at(
                            (event.pos[0] - table_seat1_mask.get_rect().x,
                             event.pos[1] - table_seat1_mask.get_rect().y)) and taken_seat is None and \
                        game_state["seats"][0]["name"] is None \
                        and game_state["is_game_over"] and user_info[2] >= 1:
                    build_and_send_message(conn, PROTOCOL_CLIENT["join_seat"],
                                           str(user_info[4]) + DATA_DELIMITER + user_info[
                                               1] + DATA_DELIMITER + chosen_table + DATA_DELIMITER + '0')
                elif table_seat2.get_rect().collidepoint(event.pos) and \
                        table_seat2_mask.get_at(
                            (event.pos[0] - table_seat2_mask.get_rect().x,
                             event.pos[1] - table_seat2_mask.get_rect().y)) and taken_seat is None and \
                        game_state["seats"][1]["name"] is None \
                        and game_state["is_game_over"] and user_info[2] >= 1:
                    build_and_send_message(conn, PROTOCOL_CLIENT["join_seat"],
                                           str(user_info[4]) + DATA_DELIMITER + user_info[
                                               1] + DATA_DELIMITER + chosen_table + DATA_DELIMITER + '1')
                elif table_seat3_mask.get_rect().collidepoint(event.pos) and \
                        table_seat3_mask.get_at(
                            (event.pos[0] - table_seat3_mask.get_rect().x,
                             event.pos[1] - table_seat3_mask.get_rect().y)) and taken_seat is None and \
                        game_state["seats"][2]["name"] is None \
                        and game_state["is_game_over"] and user_info[2] >= 1:
                    build_and_send_message(conn, PROTOCOL_CLIENT["join_seat"],
                                           str(user_info[4]) + DATA_DELIMITER + user_info[
                                               1] + DATA_DELIMITER + chosen_table + DATA_DELIMITER + '2')
                if taken_seat is not None:
                    if hit_mask.get_rect().collidepoint(event.pos) and \
                            hit_mask.get_at(
                                (event.pos[0] - hit_mask.get_rect().x, event.pos[1] - hit_mask.get_rect().y)) \
                            and not game_state["is_game_over"] and remaining_time != 0 and \
                            game_state["seats"][taken_seat]["reaction"] is None and \
                            game_state["seats"][taken_seat]["result"][1] is None and len(
                            game_state["dealer"]["cards"]) == 1 and remaining_time != 0:
                        build_and_send_message(conn, PROTOCOL_CLIENT["reaction"],
                                               chosen_table + DATA_DELIMITER + str(taken_seat) + DATA_DELIMITER + "hit")
                    elif stand_mask.get_rect().collidepoint(event.pos) and \
                            stand_mask.get_at(
                                (event.pos[0] - stand_mask.get_rect().x, event.pos[1] - stand_mask.get_rect().y)) \
                            and not game_state["is_game_over"] and remaining_time != 0 and \
                            game_state["seats"][taken_seat]["reaction"] is None and \
                            game_state["seats"][taken_seat]["result"][1] is None and len(
                            game_state["dealer"]["cards"]) == 1 and remaining_time != 0:
                        build_and_send_message(conn, PROTOCOL_CLIENT["reaction"],
                                               chosen_table + DATA_DELIMITER + str(
                                                   taken_seat) + DATA_DELIMITER + "stand")
                    elif double_down_mask.get_rect().collidepoint(event.pos) and \
                            double_down_mask.get_at((event.pos[0] - double_down_mask.get_rect().x,
                                                     event.pos[1] - double_down_mask.get_rect().y)) \
                            and not game_state["is_game_over"] and remaining_time != 0 and user_info[
                        2] >= scroll_value * 2 and game_state["seats"][taken_seat]["reaction"] is None and \
                            game_state["seats"][taken_seat]["result"][1] is None and len(
                        game_state["seats"][taken_seat]["cards"]) == 2 and len(
                            game_state["dealer"]["cards"]) == 1 and remaining_time != 0:
                        build_and_send_message(conn, PROTOCOL_CLIENT["reaction"],
                                               chosen_table + DATA_DELIMITER + str(
                                                   taken_seat) + DATA_DELIMITER + "double_down")
                    elif scroll_bar_rect.collidepoint(event.pos) and game_state["seats"][taken_seat]["bet"] is None:
                        # Set the offset for the scroll handle
                        scroll_handle_rect.x = event.pos[0] - scroll_handle_rect.w / 2
                        if scroll_handle_rect.x < scroll_bar_rect.x:
                            scroll_handle_rect.x = scroll_bar_rect.x
                        elif scroll_handle_rect.x + scroll_handle_rect.w > scroll_bar_rect.x + scroll_bar_rect.w:
                            scroll_handle_rect.x = scroll_bar_rect.x + scroll_bar_rect.w - scroll_handle_rect.w
                        scroll_value = int((scroll_handle_rect.x - scroll_bar_rect.left) / (
                                scroll_bar_rect.width - scroll_handle_rect.width) * MAX_VALUE)
                        offset_x = 1
                    elif left_button_rect.collidepoint(event.pos) and game_state["seats"][taken_seat][
                            "bet"] is None and MAX_VALUE > 0:
                        scroll_value = max(0, scroll_value - 1)
                        scroll_handle_rect.x = int(
                            scroll_bar_rect.left + scroll_value / MAX_VALUE * (
                                    scroll_bar_rect.width - scroll_handle_rect.width))
                        offset_x = None
                    elif right_button_rect.collidepoint(event.pos) and game_state["seats"][taken_seat][
                            "bet"] is None and MAX_VALUE > 0:
                        scroll_value = min(MAX_VALUE, scroll_value + 1)
                        scroll_handle_rect.x = int(
                            scroll_bar_rect.left + scroll_value / MAX_VALUE * (
                                    scroll_bar_rect.width - scroll_handle_rect.width))
                        offset_x = None
                    elif bet_rect.collidepoint(event.pos) and scroll_value != 0 and game_state["is_game_over"] is True \
                            and game_state["seats"][taken_seat]["bet"] is None:
                        value_bet = scroll_value
                        scroll_value = 0
                        scroll_handle_rect.x = scroll_bar_rect.x
                        build_and_send_message(conn, PROTOCOL_CLIENT["change_bet"],
                                               chosen_table + DATA_DELIMITER + str(taken_seat) + DATA_DELIMITER + str(
                                                   value_bet))
                    elif undo_rect.collidepoint(event.pos) and game_state["seats"][taken_seat]["bet"] is not None and \
                            game_state["is_game_over"] is True:
                        build_and_send_message(conn, PROTOCOL_CLIENT["change_bet"],
                                               chosen_table + DATA_DELIMITER + str(taken_seat) + DATA_DELIMITER + str(
                                                   None))
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
        clock.tick(fps)


def help_menu():
    """function to get help in the logged in function"""
    bj_txt_true = False
    help_screen = pygame.Surface((600, 410))  # the size of your rect
    help_screen.set_alpha(200)  # alpha level

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

        help_screen.fill((0, 0, 0))  # this fills the entire surface
        screen.blit(help_screen, (100, 155))  # (0,0) are the top-left coordinates
        help_screen_dimensions = pygame.Rect(100, 155, 600, 410)

        draw_text("welcome to my blackjack cyber project!", HelveticaFont, "white", screen, 400, 180)
        draw_text("these are the rules for blackjack:", LowFont, "white", screen, 400, 210)
        draw_text("1. The goal is to beat the dealer's hand without going over a total of 21 points.",
                  LowFont, "white", screen, 110, 230, "topleft")
        draw_text("2. Each card has a point value: face cards are worth their number, face cards are worth 10 points ",
                  LowFont, "white", screen, 110, 255, "topleft")
        draw_text("      each, and an Ace can be worth 1 or 11 (depending on the player).",
                  LowFont, "white", screen, 110, 275, "topleft")
        draw_text("3. The dealer deals two cards to each player, and one card to himself. ",
                  LowFont, "white", screen, 110, 300, "topleft")
        draw_text("4. A player can 'hit', 'stand' or 'double down' in attempt to get as close to 21 as possible ",
                  LowFont, "white", screen, 110, 325, "topleft")
        draw_text("      without going over.",
                  LowFont, "white", screen, 110, 345, "topleft")
        draw_text("5. 'Hit' means receiving an additional card, and a player can continue to hit until they are ",
                  LowFont, "white", screen, 110, 370, "topleft")
        draw_text("      they are satisfied with their hand or until they exceed a total of 21 (bust -automatic loss).",
                  LowFont, "white", screen, 110, 390, "topleft")
        draw_text("6. 'Stand' means they keep their current total, and they can't do any other action.",
                  LowFont, "white", screen, 110, 415, "topleft")
        draw_text("7. 'Double Down' means they double their bet, and receive only one card. ",
                  LowFont, "white", screen, 110, 440, "topleft")
        draw_text("8. If a player's hand is closer to 21 than the dealer's hand without going over, the player wins. ",
                  LowFont, "white", screen, 110, 465, "topleft")
        draw_text("9. If they have the same value, it results in a tie(push) and the player doesn't lose any chips.",
                  LowFont, "white", screen, 110, 490, "topleft")
        draw_text("10. If a player gets a natural Blackjack, has only 2 cards that have the value of 21, he",
                  LowFont, "white", screen, 110, 515, "topleft")
        draw_text("      gets payed in 3:2 ratio",
                  LowFont, "white", screen, 110, 535, "topleft")
        draw_text("BlackJack", MainScreenFont, (255, 255, 255), screen, display_width // 2, 120 // 2)
        blackjack_rect = Highlighted_BJ.get_rect()
        blackjack_rect.center = (display_width // 2, 120 // 2)
        BlackJack_mask = pygame.mask.from_surface(Highlighted_BJ)
        if bj_txt_true:
            screen.blit(Highlighted_BJ, blackjack_rect)

        for event in pygame.event.get():
            if event.type == pygame.MOUSEMOTION:
                if blackjack_rect.collidepoint(event.pos) and \
                        BlackJack_mask.get_at((event.pos[0] - blackjack_rect.x, event.pos[1] - blackjack_rect.y)):
                    bj_txt_true = True
                else:
                    bj_txt_true = False
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
        clock.tick(fps)


def connection_stopped():
    """function to where the connection to the server has stopped"""
    while True:
        pygame.image.save(screen, "connection_stopped_screen.png")

        screen.fill((0, 0, 0))  # this fills the entire surface
        quit_button = pygame.Rect((display_width - 80) // 2, (display_height - 80) // 2, 80, 80)
        pygame.draw.rect(screen, "white", quit_button)
        draw_text("quit", ButtonFont, (0, 0, 0), screen, display_width / 2, display_height / 2)
        draw_text("The Connection To The Server Has Stopped!",
                  MediumFont, (255, 255, 255), screen, display_width / 2, 100)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if quit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()
        clock.tick(fps)


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
    try:
        main("127.0.0.1", 51235)
    except ConnectionResetError or ConnectionAbortedError:
        connection_stopped()
