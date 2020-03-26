import pygame

from world import World

from terrain import Terrain
from pygame import Rect, Color
'''
class FancyDisplay:
    def __init__(self, world):
        self.world: World = world
        self.height, self.width = self.world.get_dimensions()
        self.screen_size = self.convert_coordinates(self.height, self.width)
        pg.init()
        self.window = pg.display.set_mode((self.screen_size))
        pg.display.set_caption('OnePyce')

        self.grass = pg.image.load('graphics/terrain/grass.png').convert()
        self.land = pg.image.load('graphics/terrain/land.png').convert()
        self.mountain = pg.image.load('graphics/terrain/mountain.png').convert()
        self.water = pg.image.load('graphics/terrain/water.png').convert()
        self.wood = pg.image.load('graphics/terrain/wood.png').convert()


    def init_display(self):
        pass

    def display_world(self, events):
        board = self.world.board
        while True:
            for y in range(self.height):
                for x in range(self.width):
                    cell = board[y][x]
                    if cell == "S" or cell == 'E':
                        #self.window.blit(self.water, self.convert_coordinates(x, y))
                        rect = Rect(x * 16, y * 16, 16, 16)
                        pg.draw.rect(self.window, Color(100, 80, 250), rect)
                    else:
                        # self.window.blit(self.grass, self.convert_coordinates(x, y))
                        rect = Rect(x * 16, y * 16, 16, 16)
                        pg.draw.rect(self.window, Color(100, 80, 250), rect)
            pg.display.flip()

    @classmethod
    def convert_coordinates(cls, x, y):
        resolution = 16
        return resolution * x, resolution * y'''



class FancyDisplay:
    def __init__(self, world):
        self.world = world
        self.board = self.world.board
        self.width, self.height = self.world.get_dimensions()

        pygame.init()
        self.resolution = 16
        self.size_x, self.size_y = self.width * self.resolution, self.height * self.resolution
        self.screen = pygame.display.set_mode((self.size_x, self.size_y))
        pygame.display.set_caption('OnePyce terrain generator')

        self.grass = pygame.image.load('graphics/terrain/grass.png')
        self.land = pygame.image.load('graphics/terrain/land.png')
        self.mountain = pygame.image.load('graphics/terrain/mountain.png')
        self.water = pygame.image.load('graphics/terrain/water.png')
        self.wood = pygame.image.load('graphics/terrain/wood.png')

    def display_world(self, events):


        for y in range(self.height):
            for x in range(self.width):
                cell = self.board[y][x]
                if cell == 'S':
                    self.screen.blit(self.water, self.convert(x, y))
                elif cell == 'X':
                    self.screen.blit(self.mountain, self.convert(x, y))
                else:
                    self.screen.blit(self.grass, self.convert(x, y))
        pygame.display.update()

    def main_loop(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False
            self.display_terrain()
            pygame.display.flip()

    def convert(self, x, y):
        return self.resolution * x, self.resolution * y

    def get_terrain_graphic(self, x, y):
        terrain_type = self.board[y][x]
        pass


