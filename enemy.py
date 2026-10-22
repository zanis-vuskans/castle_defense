import pygame

class Enemy:
    def __init__(self, x, y, radius=40, max_health=5,
                 speed=30, contact_damage=5, knockback=80):
        self.radius = radius
        self.max_health = max_health
        self.health = max_health
        self.position = pygame.Vector2(x, y)
        self.speed = speed                  # pixels per second
        self.contact_damage = contact_damage
        self.knockback = knockback          # pixels pushed back on wall hit

    def contains(self, pos):
        return self.position.distance_to(pos) <= self.radius

    def take_damage(self, amount):
        self.health -= amount
        return self.health <= 0  # True if dead

    def update(self, dt, wall):
        """Move toward the wall. Returns damage dealt to the wall this frame (0 if none)."""
        self.position.y += self.speed * dt

        if self.position.y + self.radius >= wall.rect.top:
            # push back so we're just above the wall, then a bit further
            self.position.y = wall.rect.top - self.radius - self.knockback
            return self.contact_damage
        return 0

    def draw(self, screen):
        pos = (int(self.position.x), int(self.position.y))
        pygame.draw.circle(screen, (200, 50, 50), pos, self.radius)
        # health bar above the enemy
        bar_w = self.radius * 2
        bar_h = 8
        bar_x = self.position.x - self.radius
        bar_y = self.position.y - self.radius - 16
        pygame.draw.rect(screen, (60, 60, 60), (bar_x, bar_y, bar_w, bar_h))
        fill = bar_w * max(self.health, 0) / self.max_health
        pygame.draw.rect(screen, (50, 200, 50), (bar_x, bar_y, fill, bar_h))