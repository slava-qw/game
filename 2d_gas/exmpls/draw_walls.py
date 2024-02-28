import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Draw Lines with Space")

# Set up colors
black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 255, 0)

# Set up the fps
clock = pygame.time.Clock()

# Initialize variables
drawing = False
line_start = None
final_lines = []
# Main game loop
while True:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                drawing = True
                line_start = pygame.mouse.get_pos()

        elif event.type == pygame.MOUSEBUTTONUP:
            drawing = False
            line_end = pygame.mouse.get_pos()
            # Draw the line
            if line_start and line_end:
                final_lines.append([screen, green, line_start, line_end, 2])

    # Draw the background
    screen.fill(black)
    if final_lines:
        for final_line in final_lines:
            pygame.draw.line(*final_line)

    # Draw the current line if drawing
    if drawing and line_start:
        current_mouse_pos = pygame.mouse.get_pos()
        pygame.draw.line(screen, white, line_start, current_mouse_pos, 2)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)
