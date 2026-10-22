import pygame
from constants import SCREEN_WIDTH


class Wall:
    def __init__(self, y, max_health=100, image_path="assets/Castle_wall_horizontal.png"):
        raw = pygame.image.load(image_path).convert_alpha()

        bounds = raw.get_bounding_rect(min_alpha=128)
        self.tile = raw.subsurface((bounds.x, 0, bounds.width, raw.get_height())).copy()
        self.tile_w, self.tile_h = self.tile.get_size()

        self.y = y
        self.max_health = max_health
        self.health = max_health

        # Build the full-width strip once, not every frame
        self.image = self._build_strip()
        self.rect = self.image.get_rect(topleft=(0, self.y))

    def _build_strip(self):
        strip = pygame.Surface((SCREEN_WIDTH, self.tile_h), pygame.SRCALPHA)
        overlap = 8
        step = self.tile_w - overlap
        for x in range(0, SCREEN_WIDTH, step):
            strip.blit(self.tile, (x, 0))
        return strip

    def take_damage(self, amount):
        self.health = max(0, self.health - amount)
        return self.health <= 0   # True if destroyed

    def repair(self, amount):
        self.health = min(self.max_health, self.health + amount)

    def upgrade_max_health(self, amount):
        self.max_health += amount
        self.health += amount

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        self._draw_health_bar(screen)

    def _draw_health_bar(self, screen):
        bar_w, bar_h = 200, 10
        x = (SCREEN_WIDTH - bar_w) // 2
        y = self.rect.top - bar_h - 40
        ratio = self.health / self.max_health
        pygame.draw.rect(screen, (80, 0, 0), (x, y, bar_w, bar_h))
        pygame.draw.rect(screen, (0, 200, 0), (x, y, bar_w * ratio, bar_h))