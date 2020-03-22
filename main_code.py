from world import World
from displayer import Display
from crew import Crew

my_map = World(Crew(), 10, 10)
my_display = Display(my_map)

my_display.display_map([])

running = True


def get_input():
    while True:
        key = input("Input: ").lower()
        if key in "zqsdxei":
            return key


while running:
    keyboard_input = get_input()
    if keyboard_input == "x":
        running = False
        break
    events = my_map.update_world_and_events(keyboard_input)
    my_display.display_map(events)
