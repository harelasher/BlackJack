import pygame

# Initialize Pygame
pygame.init()

# Set the window size
window_size = (400, 400)

# Create the window
screen = pygame.display.set_mode(window_size)

# Set the background color
bg_color = (255, 255, 255)

# Set the rectangle properties
rect_x, rect_y = 200, 50
rect_width, rect_height = 100, 100
rect_color = (0, 0, 255)

# Set the font and text properties
font_name = 'freesansbold.ttf'
font_size = 32
text_color = (255, 0, 0)
text = 'Hello, Pygame!'

# Render the text
font = pygame.font.Font(font_name, font_size)
text_surface = font.render(text, True, text_color)
text_rect = text_surface.get_rect()
text_rect.center = (rect_x + rect_width // 2, rect_y + rect_height // 2)

# Run the game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the screen with the background color
    screen.fill(bg_color)

    # Draw the rectangle
    pygame.draw.rect(screen, rect_color, (rect_x, rect_y, rect_width, rect_height))

    # Draw the text
    screen.blit(text_surface, text_rect)

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
