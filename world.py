from random import randrange
from item import Food, Npc
from crew import Nakama
from combat_system import Enemy


class World:

    def __init__(self, crew, width=10, height=10):
        self.items = {}
        self.npc = {}
        self.enemies = {}
        self.new_nakamas = {}
        self.obstacles = set()
        self.width = width
        self.height = height
        self.crew = crew
        self.random_map_generator()

    # World generation --------------------------------

    def empty_spot(self):
        occupied_slots = self.items.keys() | self.npc.keys() | self.enemies.keys() | self.obstacles | self.new_nakamas.keys()
        while True:
            random_coordinates = randrange(self.width), randrange(self.height)
            if random_coordinates not in occupied_slots:
                return random_coordinates

    def add_obstacles(self, nb_obstacles):
        for _ in range(nb_obstacles):
            self.obstacles.add(self.empty_spot())

    def add_items(self, nb_items):
        for _ in range(nb_items):
            self.items[self.empty_spot()] = Food()

    def add_npc(self, nb_npc):
        for _ in range(nb_npc):
            self.npc[self.empty_spot()] = Npc()

    def add_enemies(self, nb_enemies):
        for _ in range(nb_enemies):
            x, y = self.empty_spot()
            self.enemies[x, y] = Enemy(x, y)

    def add_future_nakamas(self, possible_nakamas):
        for nakama in possible_nakamas:
            self.new_nakamas[self.empty_spot()] = nakama

    def random_map_generator(self, nb_obstacles=10, nb_items=3, nb_npc=2, nb_enemies=1):
        self.add_obstacles(nb_obstacles)
        self.add_items(nb_items)
        self.add_npc(nb_npc)
        self.add_enemies(nb_enemies)
        self.add_future_nakamas(Nakama.get_possible_nakamas())

    # Movement mechanics --------------------------------
    def wanna_go(self, direction):
        x, y = self.crew.get_position()
        if direction == 'z':
            y -= 1
        elif direction == 'q':
            x -= 1
        elif direction == 's':
            y += 1
        elif direction == 'd':
            x += 1
        return x, y

    def is_outside(self, x, y):
        return not (x in range(self.width) and y in range(self.height))

    def is_obstacle(self, x, y):
        return (x, y) in self.obstacles

    def is_object(self, x, y):
        return (x, y) in self.items

    def is_npc(self, x, y):
        return (x, y) in self.npc

    def is_nakama(self, x, y):
        return (x, y) in self.new_nakamas

    def is_enemy(self):

    # TODO modify with terrain generation
    def get_terrain(self, x, y):
        return 'ground'

    def take_object(self, object_coordinates, item):
        self.crew.take_item(item)
        del self.items[object_coordinates]

    def get_new_nakama(self, nakama_coordinates, nakama):
        self.crew.add_nakama(nakama)
        del self.new_nakamas[nakama_coordinates]

    def starts_combat(self, x, y):
        combat = False
        for enemy in self.enemies.values():
            combat += enemy.is_in_range(x, y)
        return combat

    def update_world_and_events(self, key):
        events = []
        if key in 'zqsd':
            events.extend(self.movement_consequences(key))
        elif key == 'e':
            events.extend(self.crew.switch_nakama())
        elif key == 'i':
            events.extend(self.crew.use_item())
        return events

    def movement_consequences(self, direction):
        consequence = []
        x, y = self.wanna_go(direction)
        if self.is_outside(x, y) or self.is_obstacle(x, y):
            consequence.append('Ouch ! Can\'t go there !')
        elif self.is_npc(x, y):
            consequence.append(self.npc[x, y].talk())
        else:
            consequence.append('Let\'s go there')
            self.crew.move_to(x, y)
            consequence.extend(self.crew.gets_tired(self.get_terrain(x, y)))
        if self.is_object(x, y):
            self.take_object((x, y), self.items[(x, y)])
            consequence.append('Object picked up !')
        elif self.is_nakama(x, y):
            self.get_new_nakama((x, y), self.new_nakamas[x, y])
            consequence.append('Hurray ! We\'ve got a new Nakama !')
        if self.starts_combat(x, y):
            consequence.append('You started a combat!')
        return consequence
