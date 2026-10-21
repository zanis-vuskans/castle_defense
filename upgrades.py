import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_COLOR 
from game import Game


class Upgrade:
    def __init__(self, game):
        self.game = game
        self.upgrade_cost = 10
        self.upgrade_multiplier = 1.5

    def upgrade_click_damage(self):
        if self.game.points >= self.upgrade_cost:
            self.game.points -= self.upgrade_cost
            self.game.click_damage += 1
            self.upgrade_cost = int(
                self.upgrade_cost * self.upgrade_multiplier
            )