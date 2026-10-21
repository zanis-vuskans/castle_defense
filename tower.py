import pygame

from shot import Shot
from constants import SHOT_SPEED


class Tower:
    def __init__(self, x, y, radius=20, damage=1, fire_rate=2.0, range_=2500):
        self.position = pygame.Vector2(x, y)
        self.radius = radius
        self.damage = damage
        self.fire_rate = fire_rate      # shots per second
        self.range = range_
        self.cooldown = 0.0

    def draw(self, screen):
        pygame.draw.circle(
            screen, (50, 50, 200), (int(self.position.x), int(self.position.y)), self.radius
        )

    def find_target(self, enemies):
        closest = None
        closest_dist = self.range
        for enemy in enemies:
            dist = self.position.distance_to(enemy.position)
            if dist <= closest_dist:
                closest = enemy
                closest_dist = dist
        return closest

    def update(self, dt, enemies):
        self.cooldown -= dt
        if self.cooldown > 0:
            return None
        
        

        target = self.find_target(enemies)
        if target is None:
            return None

        shot = self.shoot(target.position)
        if shot:
            shot.damage = self.damage
            self.cooldown = 1.0 / self.fire_rate
        return shot

    def shoot(self, target_position):
        direction = pygame.Vector2(target_position) - self.position
        if direction.length() == 0:
            return None
        shot = Shot(self.position.x, self.position.y)
        shot.velocity = direction.normalize() * SHOT_SPEED
        return shot