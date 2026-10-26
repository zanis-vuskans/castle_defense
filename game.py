import pygame
import random
from constants import MAX_TOWERS, SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_COLOR
from enemy import Enemy
from player import Player
from shot import Shot
from button import Button
from tower import Tower
from upgrades import Upgrades, Upgrade
from wall import Wall


import json
import os

SAVE_FILE = "save.json"

DEFAULT_SAVE = {
    "points": 0,
    "kills": 0,
    "click_damage": 10,
    "tower_count": 0,
    "tower_damage": 1,
    "tower_fire_rate": 2.0,
    "wall_max_health": 100,
    "wall_health": 100,
}


def save_game(data):
    with open(SAVE_FILE, "w") as f:
        json.dump(data, f, indent=2)

def load_game():
    if not os.path.exists(SAVE_FILE):
        return {}  # first launch, no save yet
    try:
        with open(SAVE_FILE) as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return {}  # corrupted file, start fresh


class Game:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 36)
        self.big_font = pygame.font.Font(None, 96)

        # game over UI
        self.game_over = False
        self.final_kills = 0
        self.restart_rect = pygame.Rect(0, 0, 220, 60)
        self.restart_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 120)

        self.apply_state(load_game())

    def apply_state(self, saved):
        """(Re)build all game state from a save dict."""
        margin = 100
        self.player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - margin)

        self.shots = []
        self.towers = []
        self.enemies = []

        self.points = saved.get("points", 0)
        self.kills = saved.get("kills", 0)
        self.click_damage = saved.get("click_damage", 10)

        # Wall
        self.wall = Wall(y=SCREEN_HEIGHT - 200,
                         max_health=saved.get("wall_max_health", 100))
        self.wall.health = saved.get("wall_health", self.wall.max_health)

        # Tower Stats
        self.tower_count = min(saved.get("tower_count", 0), MAX_TOWERS)
        self.tower_damage = saved.get("tower_damage", 1)
        self.tower_fire_rate = saved.get("tower_fire_rate", 2.0)
        self.sync_towers()

        self.spawn_timer = 0.0
        self.enemies.append(self.spawn_enemy())
        self.upgrades = Upgrades(self)
        self.upgrades.update()

    def to_save_data(self):
        # if the player quits on the game over screen, don't keep a dead save
        if self.game_over:
            return dict(DEFAULT_SAVE)
        return {
            "points": self.points,
            "kills": self.kills,
            "click_damage": self.click_damage,
            "tower_count": self.tower_count,
            "tower_damage": self.tower_damage,
            "tower_fire_rate": self.tower_fire_rate,
            "wall_max_health": self.wall.max_health,
            "wall_health": self.wall.health,
        }

    def spawn_interval(self):
        # seconds between spawns: starts at 3s, drops to a floor of 0.6s
        return max(0.6, 3.0 - self.kills * 0.04)

    def max_enemies(self):
        # starts at 1, +1 every 10 kills, capped at 12
        return min(1 + self.kills // 10, 12)

    def spawn_enemy(self):
        margin = 100
        radius = 40
        y = radius
        # try a few times to avoid spawning on top of another enemy
        for _ in range(10):
            x = random.randint(margin, SCREEN_WIDTH - margin)
            if all(abs(x - e.position.x) > radius * 2 or e.position.y > radius * 3
                   for e in self.enemies):
                break
        health = 50 + self.kills * 2
        return Enemy(x, y, radius=radius, max_health=health)

    def handle_click(self, pos):
        if self.game_over:
            if self.restart_rect.collidepoint(pos):
                self.restart()
            return
        if self.upgrades.handle_click(pos):
            return
        self.shoot(pos)

    def shoot(self, target_position):
        shot = self.player.shoot(target_position)
        if shot is not None:
            shot.damage = self.click_damage
            self.shots.append(shot)

    def on_wall_destroyed(self):
        self.game_over = True
        self.final_kills = self.kills
        self.enemies.clear()
        self.shots.clear()

    def restart(self):
        # reset the save file to defaults, then rebuild the game from it
        save_game(dict(DEFAULT_SAVE))
        self.game_over = False
        self.final_kills = 0
        self.apply_state(dict(DEFAULT_SAVE))

    def sync_towers(self):
        self.tower_count = min(self.tower_count, MAX_TOWERS)

        # create any missing towers (positions get set below)
        while len(self.towers) < self.tower_count:
            self.towers.append(Tower(0, 0))

        # lay them out in a horizontal line, evenly spaced
        margin = 100
        y = SCREEN_HEIGHT - margin - 80   # row sits just above the player
        count = len(self.towers)
        spacing = (SCREEN_WIDTH - 2 * margin) / max(count - 1, 1)

        for i, tower in enumerate(self.towers):
            if count == 1:
                x = SCREEN_WIDTH // 2
            else:
                x = margin + i * spacing
            tower.position = pygame.Vector2(x, y)

            # apply current upgrade stats
            tower.damage = self.tower_damage
            tower.fire_rate = self.tower_fire_rate

    def update(self, dt):
        if self.game_over:
            return

        self.upgrades.update()

        # --- spawning ---
        self.spawn_timer += dt
        if not self.enemies:
            # never leave the screen empty
            self.enemies.append(self.spawn_enemy())
            self.spawn_timer = 0.0
        elif (self.spawn_timer >= self.spawn_interval()
              and len(self.enemies) < self.max_enemies()):
            self.enemies.append(self.spawn_enemy())
            self.spawn_timer = 0.0

        # --- enemies vs wall ---
        for enemy in self.enemies:
            damage = enemy.update(dt, self.wall)
            if damage and self.wall.take_damage(damage):
                self.on_wall_destroyed()
                return

        # --- towers ---
        for tower in self.towers:
            shot = tower.update(dt, self.enemies)
            if shot:
                self.shots.append(shot)

        # --- shots ---
        screen_rect = self.screen.get_rect()

        for shot in self.shots[:]:
            shot.update(dt)

            hit = next((e for e in self.enemies if shot.collides_with(e)), None)
            if hit:
                self.shots.remove(shot)
                self.points += 1

                if hit.take_damage(shot.damage):
                    self.points += 10
                    self.kills += 1
                    self.enemies.remove(hit)

            elif not screen_rect.collidepoint(shot.position):
                self.shots.remove(shot)

    def draw_game_over(self):
        self.screen.fill((0, 0, 0))

        title = self.big_font.render("GAME OVER", True, (255, 255, 255))
        self.screen.blit(title, title.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 80)))

        kills = self.font.render(f"Total kills: {self.final_kills}", True, (255, 255, 255))
        self.screen.blit(kills, kills.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 10)))

        hovered = self.restart_rect.collidepoint(pygame.mouse.get_pos())
        color = (90, 90, 90) if hovered else (50, 50, 50)
        pygame.draw.rect(self.screen, color, self.restart_rect, border_radius=8)
        pygame.draw.rect(self.screen, (255, 255, 255), self.restart_rect, 2, border_radius=8)
        label = self.font.render("Restart", True, (255, 255, 255))
        self.screen.blit(label, label.get_rect(center=self.restart_rect.center))

        pygame.display.flip()

    def draw(self):
        if self.game_over:
            self.draw_game_over()
            return

        self.screen.fill(SCREEN_COLOR)

        for enemy in self.enemies:
            enemy.draw(self.screen)
        self.wall.draw(self.screen)
        self.player.draw(self.screen)

        for tower in self.towers:
            tower.draw(self.screen)

        self.upgrades.draw(self.screen)

        for shot in self.shots:
            shot.draw(self.screen)

        text = self.font.render(
            f"Points: {self.points} | Kills: {self.kills}",
            True,
            (255, 255, 255)
        )
        self.screen.blit(text, (10, 10))

        pygame.display.flip()