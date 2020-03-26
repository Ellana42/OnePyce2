import pygame


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

        self.sheet = pygame.image.load('graphics/terrain.png')
        self.terrain = self.strip_from_sheet(self.sheet, (0, 0), (32, 32), 32, 32)

        self.player = pygame.image.load('graphics/player_icons/luffy.png').convert_alpha()

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
                if cell == 'S':
                    self.screen.blit(self.terrain[124], self.convert(v_x, v_y))
                elif cell == 'X':
                    self.screen.blit(self.terrain[109], self.convert(v_x, v_y))
                else:
                    self.screen.blit(self.terrain[97], self.convert(v_x, v_y))
                if (x, y) in self.world.obstacles:
                    pass
                elif (x, y) in self.world.npc:
                    pass
                elif (x, y) == (x_p, y_p):
                    self.screen.blit(self.player, self.convert(v_x, v_y))
                elif (x, y) in self.world.items:
                    pass
                elif (x, y) in self.world.new_nakamas:
                    nakama = self.world.new_nakamas[x, y]
                    pass
                elif (x, y) in self.world.enemies:
                    pass

        pygame.display.update()
        self.clock.tick(10)

    """def main_loop(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False
            self.display_terrain()
            pygame.display.flip()"""

    def convert(self, x, y):
        return self.resolution * x, self.resolution * y

    def get_terrain_graphic(self, x, y):
        terrain_type = self.board[y][x]
        pass

    @classmethod
    def strip_from_sheet(cls, sheet, start, size, columns, rows):
        frames = []
        for j in range(rows):
            for i in range(columns):
                location = (start[0] + size[0] * i, start[1] + size[1] * j)
                frames.append(sheet.subsurface(pygame.Rect(location, size)))
        return frames





