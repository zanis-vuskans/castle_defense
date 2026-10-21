import pygame
from circleshape import CircleShape
from constants import SHOT_RADIUS, SHOT_COLOR, SHOT_LINE_WIDTH, SHOT_LINE_LENGTH

class Shot(CircleShape):
    def __init__(self, x: float, y: float) -> None:
        super().__init__(x, y, SHOT_RADIUS)

    def draw(self, screen: pygame.Surface) -> None:
        if self.velocity.length() == 0:
            return
        self.screen = screen
        color = SHOT_COLOR
        line_width = SHOT_LINE_WIDTH
        radius = SHOT_RADIUS
        position = (int(self.position.x), int(self.position.y))
        #pygame.draw.circle(screen, color, position, radius, line_width)

        direction = self.velocity.normalize()
        half = direction * (SHOT_LINE_LENGTH / 2)
        start = self.position - half
        end = self.position + half
        pygame.draw.line(screen, "white", start, end, 2)
    
    def update(self, dt: float) -> None:
        self.position += self.velocity * dt