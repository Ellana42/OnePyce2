from random import randrange
from item import Food, Npc, Enemy
from crew import Nakama, Crew
from terrain import Terrain


class World:

    def __init__(self):
        self.width, self.height = None, None
        self.spawn_point = (0, 0)
        self.items = {}
        self.npc = {}
        self.enemies = {}
        self.new_nakamas = {}
        self.obstacles = set()
        self.crew = Crew(self)
        self.board = None
        self.random_map_generator()
        self.combat_mode = False
        self.current_enemies = []

    # World generation --------------------------------

    def random_map_generator(self, nb_obstacles=0, nb_items=10, nb_npc=5, nb_enemies=8):
        terrain: Terrain = Terrain()
        terrain.generate_island()
        self.board = terrain.get_board()
        self.width, self.height = terrain.get_dimensions()
        self.add_obstacles(nb_obstacles)
        self.add_items(nb_items)
        self.add_npc(nb_npc)
        self.add_enemies(nb_enemies)
        self.add_future_nakamas(Nakama.get_possible_nakamas())
        self.spawn_point = self.empty_spot(only_on="PCGRV")
        self.crew.move_to(self.spawn_point[0], self.spawn_point[1])

    def empty_spot(self, only_on=None, avoids=None):
        while True:
            c, r = random_coordinates = randrange(self.width), randrange(self.height)
            if only_on is not None:
                if self.board[r][c] not in only_on:
                    continue
            if avoids is not None:
                if self.board[r][c] in avoids:
                    continue
            if random_coordinates not in self.obstacles and random_coordinates not in self.items \
                    and random_coordinates not in self.npc:
                return random_coordinates

    def add_obstacles(self, nb_obstacles):
        for _ in range(nb_obstacles):
            self.obstacles.add(self.empty_spot(avoids="SEMX"))

    def add_items(self, nb_items):
        for _ in range(nb_items):
            self.items[self.empty_spot(avoids="SEMX")] = Food()  # All items are food for now

    def add_npc(self, nb_npc):
        for _ in range(nb_npc):
            self.npc[self.empty_spot(only_on="PCGRV")] = Npc()

    def add_enemies(self, nb_enemies):
        for _ in range(nb_enemies):
            x, y = self.empty_spot(avoids='SEMX')
            self.enemies[x, y] = Enemy(x, y)

    def add_future_nakamas(self, possible_nakamas):
        for nakama in possible_nakamas:
            self.new_nakamas[self.empty_spot(only_on="PCGRV")] = nakama

    # Movement mechanics --------------------------------

    def wanna_go(self, direction):
        x, y = self.crew.get_position()
        if direction == 'up':
            y -= 1
        elif direction == 'left':
            x -= 1
        elif direction == 'down':
            y += 1
        elif direction == 'right':
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

    def is_enemy(self, x, y):
        return (x, y) in self.enemies

    def there_is_anything(self, x, y):
        index = self.is_enemy(x, y) | self.is_nakama(x, y) \
                | self.is_npc(x, y) | self.is_object(x, y) | self.is_obstacle(x, y)
        return index

    def get_tile_object(self, x, y):
        if not self.there_is_anything(x, y):
            return None
        if self.is_obstacle(x, y):
            return 'obstacle'
        elif self.is_object(x, y):
            return self.items[x, y]
        elif self.is_npc(x, y):
            return self.npc[x, y]
        elif self.is_nakama(x, y):
            return self.new_nakamas[x, y]
        elif self.is_enemy(x, y):
            return self.enemies[x, y]

    def get_terrain(self, x, y):
        return self.board[y][x]

    def player_respawn(self):
        self.crew.move_to(self.spawn_point[0], self.spawn_point[1])

    # World changes

    def update(self, command):
        events = []
        directions = ['left', 'right', 'down', 'up']
        if command in directions:
            events.extend(self.movement_consequences(command))
        elif command == 'switch':
            events.extend(self.crew.switch_nakama())
        elif command == 'item':
            events.extend(self.crew.use_item())
        return events

    def movement_consequences(self, direction):
        consequence = []
        x, y = self.wanna_go(direction)
        if self.is_outside(x, y) or self.is_obstacle(x, y) or self.is_enemy(x, y):
            consequence.append('Ouch ! Can\'t go there !')
        elif self.is_npc(x, y):
            consequence.append(self.npc[x, y].talk())
        else:
            self.crew.move_to(x, y)
            consequence.extend(self.crew.gets_tired(self.get_terrain(x, y)))
        if self.is_object(x, y):
            self.take_object((x, y), self.items[(x, y)])
            consequence.append('Object picked up !')
        elif self.is_nakama(x, y):
            self.get_new_nakama((x, y), self.new_nakamas[x, y])
            consequence.append('Hurray ! We\'ve got a new Nakama !')
        if self.starts_combat(x, y)[0]:
            consequence.append('A combat has started')
            self.combat_mode = True
            self.current_enemies = self.starts_combat(x, y)[1]
        return consequence

    # Player actions

    def take_object(self, object_coordinates, item):
        self.crew.take_item(item)
        del self.items[object_coordinates]

    def get_new_nakama(self, nakama_coordinates, nakama):
        self.crew.add_nakama(nakama)
        del self.new_nakamas[nakama_coordinates]

    # Combat system

    def starts_combat(self, x, y):
        combat = False
        enemies = []
        for enemy in self.enemies.values():
            if enemy.is_in_range(x, y):
                combat += True
                enemies.append(enemy)
        return combat, enemies

    def fight(self, fighter, enemy):
        self.individual_fight(fighter, enemy)
        print(fighter.health, enemy.health)
        if enemy.health <= 0:
            self.current_enemies.remove(enemy)
            del self.enemies[enemy.x, enemy.y]
        '''if fighter.health <= 0:
            if len(self.crew.crew) >= 2:
                self.crew.wounded_nakamas.append(fighter)
                self.crew.switch_nakama()
                self.crew.crew.remove(fighter)
            else:
                self.player_respawn()'''

    @classmethod
    def individual_fight(cls, fighter, enemy):
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

    # Discussion with other classes

    def get_dimensions(self):
        return self.width, self.height
