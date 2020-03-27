import pygame
import random


class FancyDisplay:
    def __init__(self, world):
        self.world = world
        self.board = self.world.board
        self.width, self.height = self.world.get_dimensions()

        pygame.init()
        self.resolution = 32
        self.vision_width, self.vision_height = 31, 21
        self.size_x, self.size_y = self.vision_width * self.resolution, self.vision_height * self.resolution
        self.screen = pygame.display.set_mode((self.size_x, self.size_y))
        pygame.display.set_caption('OnePyce terrain generator')
        self.clock = pygame.time.Clock()

        self.sheet = pygame.image.load('graphics/terrain.png').convert_alpha()
        self.sheet2 = pygame.image.load('graphics/terrain2.png').convert_alpha()
        self.terrain = self.strip_from_sheet(self.sheet, (0, 0), (32, 32), 32, 32)
        self.terrain2 = self.strip_from_sheet(self.sheet2, (0, 0),  (32, 32), 32, 32)
        self.player = pygame.image.load('graphics/player_icons/luffy.png').convert_alpha()
        self.npc = pygame.image.load('graphics/npc.png').convert_alpha()
        self.enemy = pygame.image.load('graphics/enemy.png').convert_alpha()

        self.terrain_dict = {'S': 124, 'E': 189, 'M': 549, 'F': 198, 'B': 771,
                             'P': 357, 'C': 304, 'X': 12, 'G': 307,
                             'R': 422, 'V': 589 }

    def display_world(self, events):
        x_p, y_p = self.world.crew.x, self.world.crew.y
        for v_y in range(self.vision_height):
            for v_x in range(self.vision_width):
                x = v_x + x_p - self.vision_width // 2
                y = v_y + y_p - self.vision_height // 2
                if x in range(self.width) and y in range(self.height):
                    cell = self.board[y][x]
                else:
                    cell = 'S'
                if cell in self.terrain_dict:
                    self.screen.blit(self.terrain[self.terrain_dict[cell]], self.convert(v_x, v_y))
                if (x, y) in self.world.obstacles:
                    self.screen.blit(self.terrain[0], self.convert(v_x, v_y))
                elif (x, y) in self.world.npc:
                    self.screen.blit(self.npc, self.convert(v_x, v_y))
                elif (x, y) == (x_p, y_p):
                    self.screen.blit(self.player, self.convert(v_x, v_y))
                elif (x, y) in self.world.items:
                    self.screen.blit(self.terrain2[463], self.convert(v_x, v_y))
                elif (x, y) in self.world.new_nakamas:
                    nakama = self.world.new_nakamas[x, y]
                    self.screen.blit(self.npc, self.convert(v_x, v_y))
                elif (x, y) in self.world.enemies:
                    self.screen.blit(self.enemy, self.convert(v_x, v_y))

        pygame.display.update()
        self.clock.tick(10)

    def convert(self, x, y):
        return self.resolution * x, self.resolution * y

    def get_terrain_graphic(self, x, y):
        terrain_type = self.board[y][x]
        pass

    def orientation_modifier(self, x, y):
        current_block = self.board[y][x]
        orientation_dic = [[0, 1, 1, 0], [0, 1, 1, 1], [0, 0, 1, 1],
                           [1, 1, 1, 0], [1, 1, 1, 1], [1, 0, 1, 1],
                           [1, 1, 0, 0], [1, 1, 0, 1], [1, 0, 0, 1],
                           [0, 0, 0, 0], [1, 0, 0, 0], [0, 1, 0, 0],
                           [0, 0, 1, 0], [0, 0, 0, 1], [1, 0, 1, 0],
                           [0, 1, 0, 1]]

        surrounding_blocks = {'upper_block': self.board[y + 1][x], 'right_block': self.board[y][x + 1],
                              'down_block': self.board[y - 1][x], 'left_block': self.board[y][x - 1]}
        block_orientation = []
        subterrain_type = None
        for block in surrounding_blocks.values():
            if block == current_block:
                block_orientation.append(1)
            else:
                block_orientation.append(0)
                subterrain_type = block
        orientation = orientation_dic.index(block_orientation)
        modifier_list = [0, 1, 2, 32, 33, 34, 64, 65, 66, - 64, - 64, - 64, - 64, - 64, - 64, - 64]
        return modifier_list[orientation], subterrain_type

    @classmethod
    def strip_from_sheet(cls, sheet, start, size, columns, rows):
        frames = []
        for j in range(rows):
            for i in range(columns):
                location = (start[0] + size[0] * i, start[1] + size[1] * j)
                frames.append(sheet.subsurface(pygame.Rect(location, size)))
        return frames
