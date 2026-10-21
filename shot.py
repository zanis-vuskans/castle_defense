import pygame
from constants import SHOT_RADIUS, SHOT_COLOR, SHOT_LINE_WIDTH, SHOT_LINE_LENGTH


class Shot(pygame.sprite.Sprite):
    def __init__(self, x: float, y: float) -> None:
        self.damage = 10
        # same container logic CircleShape had
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()

        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.radius = SHOT_RADIUS  # still used for collision checks

    def draw(self, screen: pygame.Surface) -> None:
        if self.velocity.length() == 0:
            return
        direction = self.velocity.normalize()
        half = direction * (SHOT_LINE_LENGTH / 2)
        start = self.position - half
        end = self.position + half
        pygame.draw.line(screen, SHOT_COLOR, start, end, SHOT_LINE_WIDTH)

    def update(self, dt: float) -> None:
        self.position += self.velocity * dt

    def collides_with(self, other) -> bool:
        return self.position.distance_to(other.position) <= self.radius + other.radius