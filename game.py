
import pygame
import random
from constants import SCREEN_WIDTH, SCREEN_HEIGHT,SCREEN_COLOR
from enemy import Enemy
from player import Player
from shot import Shot
from button import Button
from tower import Tower
from upgrades import Upgrades, Upgrade


import json
import os

SAVE_FILE = "save.json"

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
        margin = 100
        self.font = pygame.font.Font(None, 36)
        self.player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - margin)

        self.shots = []
        self.towers = []
        self.enemies = []

        saved = load_game()
        self.points = saved.get("points", 0)
        self.kills = saved.get("kills", 0)

        # Player's click damage, default is 1 if not found in save
        self.click_damage = saved.get("click_damage", 10)

        # Tower Stats
        self.tower_count = saved.get("tower_count", 0)
        self.tower_damage = saved.get("tower_damage", 1)
        self.tower_fire_rate = saved.get("tower_fire_rate", 2.0)    

        self.sync_towers()
        

        self.enemy = self.spawn_enemy()
        self.upgrades = Upgrades(self)
        self.upgrades.update() 

    
    def to_save_data(self):
        return {
            "points": self.points,
            "kills": self.kills,
            "click_damage": self.click_damage,
            "tower_count": self.tower_count,
            "tower_damage": self.tower_damage,
            "tower_fire_rate": self.tower_fire_rate,
        }

    def spawn_enemy(self):
        margin = 100
        x = random.randint(margin, SCREEN_WIDTH - margin)
        y = random.randint(margin, SCREEN_HEIGHT // 2 - margin)
        health = 50 + self.kills * 2
        return Enemy(x, y, max_health=health)

    def handle_click(self, pos):
        if self.upgrades.handle_click(pos):
            return
        self.shoot(pos)



    def shoot(self, target_position):
        shot = self.player.shoot(target_position)
        if shot is not None:
            shot.damage = self.click_damage
            self.shots.append(shot)

    def sync_towers(self):
        margin = 100

        # create towers until we have as many as tower_count says
        while len(self.towers) < self.tower_count:
            x = random.randint(margin, SCREEN_WIDTH - margin)
            y = random.randint(margin, SCREEN_HEIGHT - margin)
            self.towers.append(Tower(x, y))

        # apply current upgrade stats to every tower
        for tower in self.towers:
            tower.damage = self.tower_damage
            tower.fire_rate = self.tower_fire_rate

    def update(self, dt):
        self.upgrades.update()

        for tower in self.towers:
            shot = tower.update(dt, [self.enemy])
            if shot:
                self.shots.append(shot)

        screen_rect = self.screen.get_rect()

        for shot in self.shots[:]:
            shot.update(dt)

            if shot.collides_with(self.enemy):
                self.shots.remove(shot)
                self.points += 1

                if self.enemy.take_damage(shot.damage):
                    self.points += 10
                    self.kills += 1
                    self.enemy = self.spawn_enemy()

            elif not screen_rect.collidepoint(shot.position):
                self.shots.remove(shot)    

    def draw(self):
        self.screen.fill(SCREEN_COLOR)

        self.enemy.draw(self.screen)
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
