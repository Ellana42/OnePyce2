import world
from displayer import Display

my_map = world.World()
my_display = Display(my_map)

my_display.display_map([])

running = True
combat_mode = False
input_translation = {'z': 'up', 'q': 'left', 's': 'down', 'd': 'right', 'e': 'switch', 'i': 'item', 'x': 'quit'}


def input_to_event(key):
    return input_translation[key]


def get_input():
    while True:
        key = input("Input: ").lower()
        if key in input_translation:
            return key


def get_fighter():
    while True:
        name_input = input('Who will fight ? ')
        if name_input in my_map.crew.is_in_the_crew(name_input):
            return my_map.crew.get_corresponding_crew_member(name_input)


while running:
    command = input_to_event(get_input())
    if command == 'quit':
        running = False
        break
    events = my_map.update(command)
    my_display.display_map(events)
