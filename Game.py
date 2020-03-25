from world import World
from displayer import Display


class Game:

    def __init__(self):
        self.input_translation = {'z': 'up', 'q': 'left', 's': 'down', 'd': 'right', 'e': 'switch', 'i': 'item',
                                  'x': 'quit'}
        self.world = World()
        self.display = Display(self.world)
        self.current_state = self.movement

    def main_loop(self):
        while True:
            self.current_state()

    def combat(self):
        fighter = self.get_fighter()


    def movement(self):
        direction = self.get_input()
        events = self.world.update(direction)
        self.display.display_map(events)
        for event in events:
            if event == 'A combat has started':
                self.switch_state(combat)

    def input_to_event(self, key):
        return self.input_translation[key]

    def get_input(self):
        while True:
            key = input("Input: ").lower()
            if key in self.input_translation:
                return key

    def get_fighter(self):
        while True:
            name_input = input('Who will fight ? ')
            if name_input in self.world.crew.is_in_the_crew(name_input):
                return self.world.crew.get_corresponding_crew_member(name_input)

    def switch_state(self, new_state):
        self.current_state = new_state


    '''def start_game(self):
        running = True
        self.display.display_map(events=[])
        while running:
            command = self.input_to_event(self.get_input())
            if command == 'quit':
                running = False
                break
            while self.world.combat_mode:
                fighter = self.get_fighter()
                events = self.world.update(fighter)

            events = self.world.update(command)
            self.display.display_map(events)'''
