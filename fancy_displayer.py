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

        self.info_box = InfoBox(self)
        self.chat_box = ChatBox(self)
        self.i = 0

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

                for event in events:
                    self.chat_box.update(event, 0)
                    if event == 'Hurray ! We\'ve got a new Nakama !':
                        i = 1
                        for nakama in self.world.crew.crew:
                            self.info_box.update(nakama.get_name() +'    ' + str(nakama.get_health()), i)
                            i += 1

                if self.world.crew.get_energy() % 10 == 0:
                    self.info_box.update('Energy : ' + str(self.world.crew.get_energy()), 0)
                self.info_box.show()
                self.chat_box.show()

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
        self.rendered_text = None
        self.empty_surface = self.font.render('', True, self.text_color).convert_alpha()

    def show(self):
        pygame.draw.rect(self.screen, self.color, (
            self.res * self.x, self.res * self.y, self.res * self.width, self.res * self.height))
        i = 0
        for line in self.rendered_text:
            self.disp.display(line, self.x + 0.5, self.y + 0.5 + i)
            i += 1

    def update(self, text, line):
        self.rendered_text[line] = self.font.render(text, True, self.text_color).convert_alpha()


class InfoBox(TextBox):
    def __init__(self, disp):
        super().__init__(disp)
        self.width, self.height = 4, 5
        self.x, self.y = self.screen_width - (self.width + 1), 1
        self.rendered_text = [self.font.render('Energy', True, self.text_color).convert_alpha(),
                              self.font.render('Luffy', True, self.text_color).convert_alpha(),
                              self.empty_surface,
                              self.empty_surface,
                              self.empty_surface,
                              self.empty_surface,
                              ]


class ChatBox(TextBox):
    def __init__(self, disp):
        super().__init__(disp)
        self.width, self.height = 10, 3
        self.x, self.y = self.screen_width - (self.width + 1), self.screen_height - (self.height + 1)
        self.rendered_text = [self.font.render('Nothing here', True, self.text_color).convert_alpha()]
