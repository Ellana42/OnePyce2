import pygame
import random


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

                InfoBox(self).show()
                ChatBox(self).show()

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

    def convert1(self, x):
        return self.resolution * x

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


class TextBox:
    def __init__(self, display):
        self.width, self.height = 5, 5
        self.color = (173, 161, 117)
        self.display = display
        self.screen = self.display.screen
        self.res = self.display.resolution
        self.screen_width, self.screen_height = self.display.v_width, self.display.v_height
        self.x, self.y = self.screen_width // 2, self.screen_height // 2
        self.text = []
        self.text_color = (0, 0, 0)
        self.font = pygame.font.Font('freesansbold.ttf', 15)

    def show(self):
        pygame.draw.rect(self.screen, self.color, (
            self.res * self.x, self.res * self.y, self.res * self.width, self.res * self.height))

    def write(self, text, next_line=True):
        line = len(self.text) - 1
        self.text.append(text)
        rendered_text = self.font.render(text, True, self.text_color).convert_alpha()
        self.display(rendered_text, self.v_width - 7.5, self.v_height - 3.5)


class InfoBox(TextBox):
    def __init__(self, display):
        super().__init__(display)
        self.width, self.height = 4, 5
        self.x, self.y = self.screen_width - 5, 1


class ChatBox(TextBox):
    def __init__(self, display):
        super().__init__(display)
        self.width, self.height = 7, 3
        self.x, self.y = self.screen_width - 8, self.screen_height - 4


self.display_up('Energy : ' + str(self.world.crew.get_energy()))
self.display_up(str([nakama.get_name() for nakama in self.world.crew.crew]), 1)
self.display_down('Hello peasant')


def display_up(self, text, line_number=0, color=(0, 0, 0)):
    self.display_text(text, self.v_width - 4.5, 1.5 + line_number, color)


def display_down(self, text, color=(0, 0, 0)):



def display_text(self, text, x, y, color=(0, 0, 0)):
    rendered_text = self.font.render(text, True, color).convert_alpha()
    self.display(rendered_text, x, y)
