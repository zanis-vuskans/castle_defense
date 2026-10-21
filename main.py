import sys
import random
import pygame
pygame.init()
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_COLOR

from enemy import Enemy
from game import Game, load_game, save_game
from logger import log_state
from upgrades import Upgrade

def main():
    
    clock = pygame.time.Clock()
    dt = 0.0

    print(f"Starting with pygame version: {pygame.version.ver}")

    # Set up the display
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("My Game")

    game = Game(screen) 
    upgrade = Upgrade(game)  # Create an instance of the Upgrade class

    # Main game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_game(game.to_save_data())
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                game.handle_click(event.pos)

        # Game logic goes here
        log_state()

        dt = clock.tick(60) / 1000 # 60 FPS cap, dt in seconds
        game.update(dt)
        # Draw everything here
        game.draw()

        # Update the display
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()