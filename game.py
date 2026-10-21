
import pygame
import random
from constants import SCREEN_WIDTH, SCREEN_HEIGHT,SCREEN_COLOR
from enemy import Enemy
from player import Player
from shot import Shot
from button import Button
from upgrades import Upgrade


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

        saved = load_game()
        self.points = saved.get("points", 0)
        self.kills = saved.get("kills", 0)
        self.click_damage = saved.get("click_damage", 1)

        self.enemy = self.spawn_enemy()

        self.upgrades = Upgrade(self)
        self.upgrade_button = Button(
            SCREEN_WIDTH - 150 - margin,
            SCREEN_HEIGHT - 0 - margin,
            200,
            50,
            "",
        )
        self.update_upgrade_button()
        self.enemy = self.spawn_enemy()

    def update_upgrade_button(self):
        cost = self.upgrades.click_damage_cost()
        self.upgrade_button.set_text(f"Upgrade Click Damage ({cost} pts)")
        self.upgrade_button.enabled = self.upgrades.can_afford_click_damage()

    def to_save_data(self):
        return {
            "points": self.points,
            "kills": self.kills,
            "click_damage": self.click_damage,
        }

    def spawn_enemy(self):
        margin = 100
        x = random.randint(margin, SCREEN_WIDTH - margin)
        y = random.randint(margin, SCREEN_HEIGHT // 2 - margin)

        health = 5 + self.kills * 2
        return Enemy(x, y, max_health=health)

    def handle_click(self, pos):
        if self.upgrade_button.is_clicked(pos):
            self.upgrades.upgrade_click_damage()
            return  # don't shoot when clicking the button
        self.shoot(pos)
        

    def shoot(self, target_position):
        shot = self.player.shoot(target_position)

        if shot is not None:
            self.shots.append(shot)

    def update(self, dt):
        self.update_upgrade_button()
        
        for shot in self.shots[:]:
            shot.update(dt)

            if shot.position.distance_to(self.enemy.position) <= (
                shot.radius + self.enemy.radius
            ):
                self.shots.remove(shot)
                self.points += 1  

                if self.enemy.take_damage(self.click_damage):
                    self.points += 10
                    self.kills += 1
                    self.enemy = self.spawn_enemy()    

    def draw(self):
        self.screen.fill(SCREEN_COLOR)
        width, height = self.screen.get_size()

        self.enemy.draw(self.screen)
        self.player.draw(self.screen)

        self.upgrade_button.draw(self.screen)


        for shot in self.shots:
            shot.draw(self.screen)

        text = self.font.render(
            f"Points: {self.points} | Kills: {self.kills}",
            True,
            (255, 255, 255)
        )
        self.screen.blit(text, (10, 10))

        pygame.display.flip()
