from random import randrange, randint


class Item:
    def __init__(self):
        self.id_number = randint(0, 100)

    def get_item_id(self):
        return self.id_number


class Food(Item):
    def __init__(self):
        super().__init__()
        self.energetic_value = randrange(50)

    def get_energetic_value(self):
        return self.energetic_value


class Npc:
    def __init__(self):
        self.id_number = randint(100, 200)

    def talk(self):
        return str(self.id_number) + '=' * 10 + ' Good morning peasant ! ' + '=' * 10


class Enemy:
    def __init__(self, x, y):
        self.id_number = 10000
        self.health = 30
        self.attack_range = 1
        self.strength = 10
        self.weaknesses = {}
        self.special_powers = {}
        self.x = x
        self.y = y
        self.combat_characteristics = {
            'close_attack': 5,
            'range_attack': 5,
            'morale_attack': 5,
            'close_defense': 5,
            'range_defense': 5,
            'morale_defense': 5
        }

    def get_life(self):
        return self.health

    def is_in_range(self, x, y):  # TODO take of the edges
        return abs(self.x - x) <= self.attack_range and abs(self.y - y) <= self.attack_range
