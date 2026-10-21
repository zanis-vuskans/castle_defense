import sys
import random
import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_COLOR
from logger import log_state

pygame.init()
clock = pygame.time.Clock()
dt = 0.0

def main():

    print(f"Starting with pygame version: {pygame.version.ver}")

    # Set up the display
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("My Game")

    # Main game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Game logic goes here
        log_state()

        dt = clock.tick(60) / 1000


        # Always ask for the current size
        width, height = screen.get_size()

        screen.fill(SCREEN_COLOR)

        # Position things as fractions of the screen
        button_rect = pygame.Rect(0, 0, width * 0.2, height * 0.08)
        button_rect.center = (width // 2, int(height * 0.8))
        pygame.draw.rect(screen, (200, 200, 200), button_rect)

        # Draw everything here

        # Update the display
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()