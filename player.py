import pygame

from constants import SHOT_SPEED
from shot import Shot


class Player:
    def __init__(self, x, y, radius=20):
        self.position = pygame.Vector2(x, y)
        self.radius = radius

    def draw(self, screen):
        pygame.draw.circle(
            screen, (50, 50, 200), (int(self.position.x), int(self.position.y)), self.radius
        )

    def shoot(self, target_position):
        direction = pygame.Vector2(target_position) - self.position
        if direction.length() == 0:
            return None

        shot = Shot(self.position.x, self.position.y)
        shot.velocity = direction.normalize() * SHOT_SPEED
        return shot