import pygame


class FancyDisplay:
    def __init__(self, world):
        self.world = world
        self.board = self.world.board
        self.width, self.height = self.world.get_dimensions()

        pygame.init()
        self.resolution = 32
        self.v_width, self.v_height = 31, 21
        self.size_x, self.size_y = self.v_width * self.resolution, self.v_height * self.resolution
        self.screen = pygame.display.set_mode((self.size_x, self.size_y))
        pygame.display.set_caption('OnePyce terrain generator')
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font('freesansbold.ttf', 15)

        self.sheet = pygame.image.load('graphics/terrain.png').convert_alpha()
        self.sheet2 = pygame.image.load('graphics/terrain2.png').convert_alpha()
        self.terrain = self.strip_from_sheet(self.sheet, (0, 0), (32, 32), 32, 32)
        self.terrain2 = self.strip_from_sheet(self.sheet2, (0, 0), (32, 32), 32, 32)

        self.terrain_dict = {'S': 124, 'E': 189, 'M': 106, 'F': 358, 'B': 360,
                             'P': 353, 'C': 352, 'X': 106, 'G': 307,
                             'R': 701, 'V': 489}

    def display_world(self, events):
        x_p, y_p = self.world.crew.x, self.world.crew.y

        for v_y in range(self.v_height):
            for v_x in range(self.v_width):

                x = v_x + x_p - self.v_width // 2
                y = v_y + y_p - self.v_height // 2

                self.cell_display(x, y, v_x, v_y)

                things = self.world.get_tile_object(x, y)
                if things is not None and things != 'obstacle':
                    self.display(things.get_icon(), v_x, v_y)

                elif (x, y) == (x_p, y_p):
                    self.display(self.world.crew.get_icon(), v_x, v_y)

                info_box = InfoBox(self)
                info_box.show()
                info_box.write('Energy : ' + str(self.world.crew.get_energy()))
                info_box.write(str([nakama.get_name() for nakama in self.world.crew.crew]))

                chat_box = ChatBox(self)
                chat_box.show()
                chat_box.write('Hello peasant')

        pygame.display.update()
        self.clock.tick(10)

    def cell_display(self, x, y, v_x, v_y):
        if x in range(self.width) and y in range(self.height):
            cell = self.board[y][x]
        else:
            cell = 'S'

        self.display(self.terrain[self.terrain_dict[cell]], v_x, v_y)

    def convert(self, x, y):
        return self.resolution * x, self.resolution * y

    def display(self, image, x, y):
        self.screen.blit(image, self.convert(x, y))

    @classmethod
    def strip_from_sheet(cls, sheet, start, size, columns, rows):
        frames = []
        for j in range(rows):
            for i in range(columns):
                location = (start[0] + size[0] * i, start[1] + size[1] * j)
                frames.append(sheet.subsurface(pygame.Rect(location, size)))
        return frames


class TextBox:
    def __init__(self, disp):
        self.width, self.height = 5, 5
        self.color = (173, 161, 117)
        self.disp = disp
        self.screen = self.disp.screen
        self.res = self.disp.resolution
        self.screen_width, self.screen_height = self.disp.v_width, self.disp.v_height
        self.x, self.y = self.screen_width // 2, self.screen_height // 2
        self.text = []
        self.text_color = (0, 0, 0)
        self.font = self.disp.font

    def show(self):
        pygame.draw.rect(self.screen, self.color, (
            self.res * self.x, self.res * self.y, self.res * self.width, self.res * self.height))

    def write(self, text, next_line=True):
        line = len(self.text) - 1
        self.text.append(text)
        rendered_text = self.font.render(text, True, self.text_color).convert_alpha()
        self.disp.display(rendered_text, self.x + 0.5, self.y + 1.5 + line)


class InfoBox(TextBox):
    def __init__(self, disp):
        super().__init__(disp)
        self.width, self.height = 4, 5
        self.x, self.y = self.screen_width - 5, 1


class ChatBox(TextBox):
    def __init__(self, disp):
        super().__init__(disp)
        self.width, self.height = 7, 3
        self.x, self.y = self.screen_width - 8, self.screen_height - 4

    '''def orientation(self, x, y):
        set_block = self.board[y][x]
        surroundings = [self.board[y + 1][x], self.board[y][x + 1], self.board[y - 1][x], self.board[y][x - 1]]
        block_type = int("".join(str(x) for x in [int(block == set_block) for block in surroundings]), 2)
        subterrain = 'P'
        if block_type != 0:
            subterrain = 'P'
        return self.modifier(block_type, set_block), subterrain

    @classmethod
    def modifier(cls, block_type, set_block):
        modifiers = [-97, 0, 0, 33, 0, 0, 31, 32, 0, -31, 0, 1, -33, -32, -1, 0]
        if set_block in 'SVR':
            return 0
        else:
            return modifiers[block_type]'''
