import pygame
import sys

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

# Player

screen.blit(overlay, (0, 0))
MainScreenFont = pygame.font.SysFont("gabriola", 80)
ButtonFont = pygame.font.Font("Fonts/Copperplate Gothic Bold Regular.ttf", 28)

# (rect_x + rect_width // 2, rect_y + rect_height // 2) -- (
def MainMenu():
    screen.blit(overlay, (0, 0))
    draw_text("BlackJack", MainScreenFont, (255, 255, 255), screen, 280, 28)

    pygame.draw.rect(screen, "white", [260, 200, 270, 65], 3, border_radius=10)

    text = ButtonFont.render("play!", True, 'white')
    text_rect = text.get_rect(center=(260 / 2, 200 / 2))
    screen.blit(text, text_rect)

    draw_text("play", ButtonFont, (255, 255, 255), screen, 360, 215)
    pygame.draw.rect(screen, "white", [260, 310, 270, 65], 3, border_radius=10)
    pygame.draw.rect(screen, "white", [260, 420, 270, 65], 3, border_radius=10)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        pygame.display.update()


def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)


MainMenu()
