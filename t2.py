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

visual_eye = pygame.transform.scale(pygame.image.load('Pictures/visual eye.png'), (50, 50))
left_arrow = pygame.transform.scale(pygame.image.load('Pictures/left-arrow.png'), (64, 64))
right_arrow = pygame.transform.rotate(pygame.transform.scale(pygame.image.load('Pictures/left-arrow.png'),
                                                             (64, 64)), 180)

Highlighted_BJ = pygame.image.load('BlackJack_Highlighted.png').convert_alpha()
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
    card_image = pygame.image.load(f"cards/{card_name}.png")
    cards[card_name] = pygame.transform.scale(card_image, (48, 68))

bj_table = pygame.image.load('Pictures/blackjack_table.png').convert_alpha()
# Fonts
MainScreenFont = pygame.font.SysFont("gabriola", 80)
ButtonFont = pygame.font.Font("Fonts/Copperplate Gothic Bold Regular.ttf", 28)
MediumFont = pygame.font.SysFont("gabriola", 40)
LowFont = pygame.font.SysFont("gabriola", 20)
HelveticaFont = pygame.font.Font('Fonts/Copperplate Gothic Bold Regular.ttf', 20)

clock = pygame.time.Clock()
_circle_cache = {}

fps = 60



def lol():
    while True:
        screen.fill((0, 0, 0))  # this fills the entire surface
        quit_button = pygame.Rect((display_width - 80) // 2, (display_height - 80) // 2, 80, 80)
        pygame.draw.rect(screen, "white", quit_button)
        draw_text("quit", ButtonFont, (0, 0, 0), screen, display_width / 2, display_height / 2)
        draw_text("The Connection To The Server Has Stopped!", MediumFont, (255, 255, 255), screen, display_width / 2, 100)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if quit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()
        clock.tick(fps)

lol()