from crew import Nakama


class Display:
    def __init__(self, world):
        self.world = world
        self.height = world.height
        self.width = world.width
        self.empty_space = '　'
        self.obstacle = '田'
        self.object = '圓'
        self.npc = '人'
        self.enemy = '力'
        self.sea = '~~'

    def display_map(self, events):
        board = self.world.board
        h, w = self.height, self.width
        player_icon = self.world.crew.get_nakama().get_icon()

        print('[', end='')
        for item in self.world.crew.get_inventory():
            print(item.get_item_id(), end='')
        print(']')

        for nakama in self.world.crew.get_crew():
            print(nakama.get_icon(), end=' ')
        print('Energy level : ' + str(self.world.crew.energy_level))
        print()

        print('＿' * (w + 2))
        for y in range(h):
            print("|", end='')
            for x in range(w):
                if (x, y) in self.world.obstacles:
                    print(self.obstacle, end='')
                elif (x, y) in self.world.npc:
                    print(self.npc, end='')
                elif (x, y) == (self.world.crew.x, self.world.crew.y):
                    print(player_icon, end='')
                elif (x, y) in self.world.items:
                    print(self.object, end='')
                elif (x, y) in self.world.new_nakamas:
                    nakama = self.world.new_nakamas[x, y]
                    print(Nakama.get_nakama_skin()[type(nakama)], end='')
                elif (x, y) in self.world.enemies:
                    print(self.enemy, end='')
                else:
                    cell = board[y][x]
                    if cell == "S" or cell == 'E':
                        print(self.sea, end='')
                    else:
                        print(self.empty_space, end='')
            print("  |")

        print('＿' * (w + 2))

        for event in events:
            print(event)
