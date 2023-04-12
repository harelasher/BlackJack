import pygame

# Initialize Pygame
pygame.init()

# Set the font and size
font = pygame.font.SysFont(None, 48)

# Render the text with per-pixel alpha values
text_surface = font.render('Hello, World!', True, (255, 255, 255, 128))

# Draw the text on the screen
screen = pygame.display.set_mode((800, 600))
screen.blit(text_surface, (0, 0))

# Update the display
pygame.display.update()

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
