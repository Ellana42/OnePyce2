from world import World
from displayer import Display
from fancy_displayer import FancyDisplay


class Game:

    def __init__(self):
        self.world = World()
        self.display = FancyDisplay(self.world)
        self.inputer = InputerPygame(self.world)
        self.current_state = self.movement
        self.running = True

    # Main code :

    def main_loop(self):
        while self.running:
            self.current_state()

    def switch_state(self, new_state):
        self.current_state = new_state

    # Different states :

    def combat(self):
        while len(self.world.current_enemies) > 0:
            for enemy in self.world.current_enemies:
                fighter = self.inputer.get_fighter()
                self.world.fight(fighter, enemy)
                if fighter == 'quit':
                    self.running = False
        self.switch_state(self.movement)

    def movement(self):
        direction = self.inputer.get_input()
        if direction == 'quit':
            self.running = False
        events = self.world.update(direction)
        self.display.display_world(events)
        for event in events:
            if event == 'A combat has started':
                self.switch_state(self.combat)

    # Get input functions

    '''def input_to_event(self, key):
        return self.input_translation[key]

    def get_input(self):
        while True:
            key = input("Input: ").lower()
            if key in self.input_translation:
                return self.input_translation[key]

    def get_fighter(self):
        while True:
            name_input = input('Who will fight ? ')
            if self.world.crew.is_in_the_crew(name_input):
                return self.world.crew.get_corresponding_crew_member(name_input)
            elif name_input == 'x':
                return 'quit'''


class Inputer:
    def __init__(self, world):
        self.input_translation = {'z': 'up', 'q': 'left', 's': 'down', 'd': 'right', 'e': 'switch', 'i': 'item',
                                  'x': 'quit'}
        self.world = world

    def get_input(self):
        while True:
            key = input("Input: ").lower()
            if key in self.input_translation:
                return self.input_translation[key]

    def get_fighter(self):
        while True:
            name_input = input('Who will fight ? ')
            if self.world.crew.is_in_the_crew(name_input):
                return self.world.crew.get_corresponding_crew_member(name_input)
            elif name_input == 'x':
                return 'quit'


import pygame


class InputerPygame:
    def __init__(self, world):
        self.input_translation = {pygame.K_UP: 'up', pygame.K_LEFT: 'left', pygame.K_DOWN: 'down',
                                  pygame.K_RIGHT: 'right', pygame.K_e: 'switch', pygame.K_i: 'item'}
        self.world = world
        self.last_direction = None

    def get_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'quit'
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return 'quit'
            if event.type == pygame.KEYDOWN:
                if event.key in self.input_translation:
                    self.last_direction = self.input_translation[event.key]

            if event.type == pygame.KEYUP:
                self.last_direction = None
        return self.last_direction

    def get_fighter(self):
        while True:
            name_input = input('Who will fight ? ')
            if self.world.crew.is_in_the_crew(name_input):
                return self.world.crew.get_corresponding_crew_member(name_input)
            elif name_input == 'x':
                return 'quit'
