from world import World
from displayer import Display


class Game:

    def __init__(self):
        self.input_translation = {'z': 'up', 'q': 'left', 's': 'down', 'd': 'right', 'e': 'switch', 'i': 'item',
                                  'x': 'quit'}
        self.world = World()
        self.display = Display(self.world)
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
                fighter = self.get_fighter()
                self.world.fight(fighter, enemy)
                if fighter == 'quit':
                    self.running = False
        self.switch_state(self.movement)

    def movement(self):
        direction = self.get_input()
        if direction == 'quit':
            self.running = False
        events = self.world.update(direction)
        self.display.display_map(events)
        for event in events:
            if event == 'A combat has started':
                self.switch_state(self.combat)

    # Get input functions

    def input_to_event(self, key):
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
                return 'quit'
