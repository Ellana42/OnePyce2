import pygame


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

        self.grass = pygame.image.load('graphics/terrain/grass.png').convert()
        self.land = pygame.image.load('graphics/terrain/land.png').convert()
        self.mountain = pygame.image.load('graphics/terrain/mountain.png').convert()
        self.water = pygame.image.load('graphics/terrain/water.png').convert()
        self.wood = pygame.image.load('graphics/terrain/wood.png').convert()

        self.player = pygame.image.load('graphics/player_icons/luffy.png').convert_alpha()

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
                if (x, y) in self.world.obstacles:
                    pass
                elif (x, y) in self.world.npc:
                    pass
                elif (x, y) == (self.world.crew.x, self.world.crew.y):
                    self.screen.blit(self.player, self.convert(x, y))
                elif (x, y) in self.world.items:
                    pass
                elif (x, y) in self.world.new_nakamas:
                    nakama = self.world.new_nakamas[x, y]
                    pass
                elif (x, y) in self.world.enemies:
                    pass
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




