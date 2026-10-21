# upgrades.py
from button import Button
from constants import SCREEN_WIDTH, SCREEN_HEIGHT


class Upgrade:
    def __init__(self, game, label, stat, start, step=1, base_cost=10, multiplier=1.5):
        self.game = game
        self.label = label          # text shown on the button
        self.stat = stat            # attribute name on Game, e.g. "click_damage"
        self.start = start          # the stat's starting value
        self.step = step            # how much one purchase adds
        self.base_cost = base_cost
        self.multiplier = multiplier
        self.button = Button(0, 0, 200, 50, "")

    def level(self):
        # how many times it has been bought, derived from the saved stat
        value = getattr(self.game, self.stat)
        return round((value - self.start) / self.step)

    def cost(self):
        return int(self.base_cost * self.multiplier ** self.level())

    def can_afford(self):
        return self.game.points >= self.cost()

    def buy(self):
        if not self.can_afford():
            return False
        self.game.points -= self.cost()
        setattr(self.game, self.stat, getattr(self.game, self.stat) + self.step)
        return True

    def refresh_button(self):
        self.button.set_text(f"{self.label} ({self.cost()} pts)")
        self.button.enabled = self.can_afford()


class Upgrades:
    def __init__(self, game, margin=20, gap=10):
        self.game = game
        self.list = [
            Upgrade(game, "Click Damage",    "click_damage",    start=10,   step=5),
            Upgrade(game, "Tower Damage",    "tower_damage",    start=1,   step=1),
            Upgrade(game, "Tower Fire Rate", "tower_fire_rate", start=2.0, step=0.5),
            Upgrade(game, "Buy Tower",       "tower_count",     start=0,   step=1, base_cost=500),
        ]

        # Stack buttons upward from the bottom-right corner
        y = SCREEN_HEIGHT - margin
        for upgrade in self.list:
            rect = upgrade.button.rect
            rect.bottomright = (SCREEN_WIDTH - margin, y)
            y -= rect.height + gap

    def update(self):
        for upgrade in self.list:
            upgrade.refresh_button()

    def draw(self, screen):
        for upgrade in self.list:
            upgrade.button.draw(screen)

    def handle_click(self, pos):
        for upgrade in self.list:
            if upgrade.button.is_clicked(pos):
                if upgrade.buy():
                    self.game.sync_towers()
                return True
        return False