# upgrades.py
class Upgrade:
    def __init__(self, game):
        self.game = game
        self.base_cost = 10
        self.multiplier = 1.5

    def click_damage_cost(self):
        # click_damage starts at 1, so the first upgrade costs base_cost
        return int(self.base_cost * self.multiplier ** (self.game.click_damage - 1))

    def can_afford_click_damage(self):
        return self.game.points >= self.click_damage_cost()

    def upgrade_click_damage(self):
        if not self.can_afford_click_damage():
            return False
        self.game.points -= self.click_damage_cost()
        self.game.click_damage += 1
        return True