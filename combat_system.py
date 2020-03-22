
class Enemy:
    def __init__(self, x, y):
        self.id_number = 10000
        self.life = 30
        self.attack_range = 1
        self.strength = 10
        self.weaknesses = {}
        self.special_powers = {}
        self.x = x
        self.y = y

    def get_life(self):
        return self.life

    def is_in_range(self, x, y):  # TODO take of the edges
        return abs(self.x - x) <= self.attack_range and abs(self.y - y) <= self.attack_range


class Combat:
    def __init__(self, player, enemy):
        self.player = player
        self.enemy = enemy

    def start_combat(self):





