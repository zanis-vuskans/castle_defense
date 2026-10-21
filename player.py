import pygame
import random

from constants import SHOT_SPEED
from shot import Shot
from circleshape import CircleShape



class Player(CircleShape):
    def __init__(self, x, y, radius=20):
        super().__init__(x, y, radius)
        self.shots = []

    def draw(self, screen):
        pygame.draw.circle(screen, (50, 50, 200), (int(self.position.x), int(self.position.y)), self.radius)

    def shoot(self, target_position):
        shot = Shot(self.position.x, self.position.y)

        direction = pygame.Vector2(target_position) - self.position

        if direction.length() == 0:
            return None

        shot.velocity = direction.normalize() * SHOT_SPEED
        return shot