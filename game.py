import sys
import pygame
from pygame.locals import *


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
Man = pygame.image.load('Pictures/woman.png')

# Fonts
MainScreenFont = pygame.font.SysFont("gabriola", 80)
ButtonFont = pygame.font.Font("Fonts/Copperplate Gothic Bold Regular.ttf", 28)
LowFont = pygame.font.SysFont("gabriola", 20)

clock = pygame.time.Clock()


def MainMenu():
    while True:
        screen.blit(overlay, (0, 0))

        draw_text("BlackJack", MainScreenFont, (255, 255, 255), screen, display_width // 2, 120 // 2)
        draw_text("By Harel Asher", LowFont, (255, 255, 255), screen, display_width // 2, 220 // 2)

        PlayButton = pygame.Rect(265, 200, 270, 65)
        pygame.draw.rect(screen, "white", PlayButton, 3, border_radius=10)
        draw_text("play", ButtonFont, (255, 255, 255), screen, (PlayButton.x + PlayButton.w // 2),
                  (PlayButton.y + PlayButton.h // 2))

        HelpButton = pygame.Rect(PlayButton.x, PlayButton.y + 110, PlayButton.w, PlayButton.h)
        pygame.draw.rect(screen, "white", HelpButton, 3, border_radius=10)
        draw_text("help", ButtonFont, (255, 255, 255), screen, (HelpButton.x + HelpButton.w // 2),
                  (HelpButton.y + HelpButton.h // 2))

        QuitButton = pygame.Rect(PlayButton.x, HelpButton.y + 110, PlayButton.w, PlayButton.h)
        pygame.draw.rect(screen, "white", QuitButton, 3, border_radius=10)
        draw_text("quit", ButtonFont, (255, 255, 255), screen, (HelpButton.x + HelpButton.w // 2),
                  (QuitButton.y + HelpButton.h // 2))

        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        mx, my = pygame.mouse.get_pos()
        if PlayButton.collidepoint((mx, my)):
            if click:
                PlayMenu()
        if HelpButton.collidepoint((mx, my)):
            if click:
                HelpMenu()
        if QuitButton.collidepoint((mx, my)):
            if click:
                sys.exit()

        pygame.display.update()
        clock.tick(120)


def PlayMenu():
    running = True
    while running:
        screen.blit(overlay, (0, 0))

        draw_text("BlackJack", MainScreenFont, (255, 255, 255), screen, display_width // 2, 120 // 2)
        draw_text("By Harel Asher", LowFont, (255, 255, 255), screen, display_width // 2, 220 // 2)

        screen.blit(Man, (display_width / 1.15, 120 // 2 - 32))
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return

        pygame.display.update()
        clock.tick(120)


def HelpMenu():
    while True:
        screen.blit(overlay, (0, 0))

        draw_text("BlackJack", MainScreenFont, (255, 255, 255), screen, display_width // 2, 120 // 2)
        draw_text("By Harel Asher", LowFont, (255, 255, 255), screen, display_width // 2, 220 // 2)

        PlayButton = pygame.Rect(265, 200, 270, 65)
        pygame.draw.rect(screen, "white", PlayButton, 3, border_radius=10)
        draw_text("play", ButtonFont, (255, 255, 255), screen, (PlayButton.x + PlayButton.w // 2),
                  (PlayButton.y + PlayButton.h // 2))

        HelpButton = pygame.Rect(PlayButton.x, PlayButton.y + 110, PlayButton.w, PlayButton.h)
        pygame.draw.rect(screen, "white", HelpButton, 3, border_radius=10)
        draw_text("help", ButtonFont, (255, 255, 255), screen, (HelpButton.x + HelpButton.w // 2),
                  (HelpButton.y + HelpButton.h // 2))

        QuitButton = pygame.Rect(PlayButton.x, HelpButton.y + 110, PlayButton.w, PlayButton.h)
        pygame.draw.rect(screen, "white", QuitButton, 3, border_radius=10)
        draw_text("quit", ButtonFont, (255, 255, 255), screen, (HelpButton.x + HelpButton.w // 2),
                  (QuitButton.y + HelpButton.h // 2))

        s = pygame.Surface((640, 490), pygame.SRCALPHA)  # per-pixel alpha
        s.fill((0, 0, 0, 128))  # notice the alpha value in the color
        screen.blit(s, (80, 55))

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return

        pygame.display.update()
        clock.tick(120)


MainMenu()
