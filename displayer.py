class Display:
    def __init__(self, map):
        self.map = map
        self.height = map.height
        self.width = map.width
        self.empty_space = '　'
        self.obstacle = '田'
        self.object = '圓'
        self.npc = '人'

    def display_map(self, events):
        h, w = self.height, self.width
        player_icon = self.map.crew.get_nakama().get_icon()

        print('[', end='')
        for item in self.map.crew.get_inventory():
            print(item.get_item_id(), end='')
        print(']')

        for nakama in self.map.crew.get_crew():
            print(nakama.get_icon(), end=' ')
        print('Energy level : ' + str(self.map.crew.energy_level))
        print()

        print('＿' * (w + 2))
        for y in range(h):
            print("|", end='')
            for x in range(w):
                if (x, y) in self.map.obstacles:
                    print(self.obstacle, end='')
                elif (x, y) in self.map.npc:
                    print(self.npc, end='')
                elif (x, y) == (self.map.crew.x, self.map.crew.y):
                    print(player_icon, end='')
                elif (x, y) in self.map.items:
                    print(self.object, end='')
                else:
                    print(self.empty_space, end='')
            print("  |")

        print('＿' * (w + 2))

        for event in events:
            print(event)
