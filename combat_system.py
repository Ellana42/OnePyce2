from crew import Crew
from main_code import get_fighter


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


class CombatSystem:
    def __init__(self, world, crew):
        self.world = world
        self.crew = crew

    def combat_mode(self, enemies):
        for enemy in enemies:
            while enemy.health > 0:
                fighter = get_fighter()
                self.individual_fight(fighter, enemy)
                if fighter.health <= 0:
                    self.crew.respawn(fighter)
        return []

    def individual_fight(self, fighter, enemy):
        fighter_stats = fighter.combat_characteristics
        enemy_stats = enemy.combat_characteristics
        enemy_hurt = enemy_stats['close_defense'] - fighter_stats['close_attack'] + \
                     enemy_stats['range_defense'] - fighter_stats['range_attack'] + \
                     enemy_stats['morale_defense'] - fighter_stats['morale_attack']

        fighter_hurt = fighter_stats['close_defense'] - enemy_stats['close_attack'] + \
                     fighter_stats['range_defense'] - enemy_stats['range_attack'] + \
                     fighter_stats['morale_defense'] - enemy_stats['morale_attack']

        enemy.health += enemy_hurt if enemy_hurt < 0 else 0
        fighter.health += fighter_hurt if fighter_hurt < 0 else 0
        print('The enemy still has ' + str(enemy.health) + ' health points.')
        print('You still have ' + str(fighter.health) + ' health points.')







