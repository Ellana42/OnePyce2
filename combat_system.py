from crew import Crew


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


class CombatSystem:
    def __init__(self, world, crew):
        self.world = world
        self.crew = crew

    def start_combat(self, enemies):
        fighter_name = input('A combat has started, who will fight ? Type your fighter\'s name : ')
        if not self.crew.is_in_the_crew(fighter_name):
            input('This is not a valid fighter ! Try again : ')

        for enemy in enemies:
            self.individual_fight(enemy)

    def individual_fight(self, enemy):
        pass





