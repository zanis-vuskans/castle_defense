import random
import pygame
from constants import ENEMY_NAMES

class Enemy:
    def __init__(self, x, y, radius=40, max_health=5):
        self.x = x
        self.y = y
        self.radius = radius
        self.max_health = max_health
        self.health = max_health
        self.position = pygame.Vector2(x, y)
 
    def contains(self, pos):
        return self.position.distance_to(pos) <= self.radius
 
    def take_damage(self, amount):
        self.health -= amount
        return self.health <= 0  # True if dead
 
    def draw(self, screen):
        pygame.draw.circle(screen, (200, 50, 50), (self.x, self.y), self.radius)
        # health bar above the enemy
        bar_w = self.radius * 2
        bar_h = 8
        bar_x = self.x - self.radius
        bar_y = self.y - self.radius - 16
        pygame.draw.rect(screen, (60, 60, 60), (bar_x, bar_y, bar_w, bar_h))
        fill = bar_w * max(self.health, 0) / self.max_health
        pygame.draw.rect(screen, (50, 200, 50), (bar_x, bar_y, fill, bar_h))