from random import randrange, randint
import pygame


class Item:
    def __init__(self):
        self.id_number = randint(0, 100)
        self.icon = pygame.image.load('graphics/item.png')

    def get_item_id(self):
        return self.id_number

    def get_icon(self):
        return self.icon


class Food(Item):
    def __init__(self):
        super().__init__()
        self.energetic_value = randrange(50)

    def get_energetic_value(self):
        return self.energetic_value


class Npc:
    def __init__(self):
        self.id_number = randint(100, 200)
        self.icon = pygame.image.load('graphics/npc.png')

    def talk(self):
        return str(self.id_number) + '=' * 10 + ' Good morning peasant ! ' + '=' * 10

    def get_icon(self):
        return self.icon


class Enemy:
    def __init__(self, x, y):
        self.id_number = 10000
        self.icon = pygame.image.load('graphics/enemy.png')
        self.health = 30
        self.attack_range = 1
        self.strength = 10
        self.weaknesses = {}
        self.special_powers = {}
        self.x = x
        self.y = y
        self.combat_characteristics = {
            'close_attack': 30,
            'range_attack': 5,
            'morale_attack': 5,
            'close_defense': 5,
            'range_defense': 5,
            'morale_defense': 5
        }

    def get_life(self):
        return self.health

    def is_in_range(self, x, y):
        return abs(self.x - x) <= self.attack_range and abs(self.y - y) <= self.attack_range

    def get_icon(self):
        return self.icon
