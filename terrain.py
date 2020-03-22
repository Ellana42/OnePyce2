from random import randrange, random, seed, choices, shuffle
from math import sin, cos, pi, fabs, sqrt
import copy

from pygame import Rect, Color


class Terrain:

    @classmethod
    def get_terrains(cls):
        terrains = {
            "S": ("Sea", "Water"),
            "E": ("Pond","Water"),
            "M": ("Mountain","Mountain"),
            "F": ("Forest", "Forest"),
            "B": ("Wood", "Forest"),
            "P": ("Meadows", "Ground"),
            "C": ("Field", "Ground"),
            "X": ("Cliff", "Mountain"),
            "G": ("Beach", "Ground"),
            "R": ("Road", "Path"),
            "V": ("City", "Path"),
        }
        return {k: {"name": name, "type": terrain_type} for k, (name, terrain_type) in terrains.items()}

    def __init__(self):
        island_size = randrange(40, 80)
        width, height = island_size, island_size
        self.board = [[0 for _ in range(width)] for _ in range(height)]
        self.width, self.height = width, height

    def get_board(self):
        return self.board

    def get_dimensions(self):
        return self.width, self.height

    def copy_board(self):
        return copy.deepcopy(self.board)

    def get_random_positions(self, number):
        width, height = self.width, self.height
        board = self.board
        positions = set()
        for _ in range(number):
            while True:
                c, r = randrange(width), randrange(height)
                if board[r][c] == 0 and (c,r) not in positions:
                    positions.add((c,r))
                    break
        return positions

    def put_random_obstacles(self, what, number):
        width, height = self.width, self.height
        board = self.board
        for _ in range(number):
            while True:
                c, r = randrange(width), randrange(height)
                cell_content = board[r][c]
                if cell_content == 0:
                    board[r][c] = what
                    break

    def is_inside_board(self, r, c):
        width, height = self.width, self.height
        return c in range(width) and r in range(height)

    def one_pass(self, what, threshold, to_what='', direction=None):
        dir_x, dir_y = 0, 0
        if direction is not None:
            dir_x , dir_y = cos(direction), sin(direction)
        previous_board = self.copy_board()
        for r, line in enumerate(previous_board):
            for c, cell in enumerate(line):
                if cell == what:
                    for h, v in ((i, j) for i in range(-1, 2) for j in range(-1, 2) if (i,j) != (0,0)):
                        around_r, around_c = r + v, c + h
                        if direction is None:
                            threshold_kept = threshold
                        else:
                            threshold_kept = fabs(h * dir_x + v * dir_y) * threshold
                        if self.is_inside_board(around_r, around_c) and random() < threshold_kept and self.board[around_r][around_c] == 0:
                            self.board[around_r][around_c] = what if to_what == '' else to_what

    def multiple_pass(self, what, threshold, passes, to_what = '', direction=None):
        for _ in range(passes):
            self.one_pass(what, threshold, to_what, direction)

    def invert_board(self, fill):
        previous_board = self.copy_board()
        for r, line in enumerate(previous_board):
            for c, cell in enumerate(line):
                self.board[r][c] = fill if cell == 0 else 0

    def fill_with(self, what):
        for r, line in enumerate(self.board):
            for c, cell in enumerate(line):
                if cell == 0:
                    self.board[r][c] = what

    def draw_road(self, start, end):
        def possible_moves(c, r):
            return ((h, v) for h,v in {(-1, 0), (1, 0), (0, -1), (0, 1)} if self.board[r + v][c + h] == 0)

        def junction(c, r):
            return [(h, v) for h,v in {(-1, 0), (1, 0), (0, -1), (0, 1)} if self.board[r + v][c + h] in ('V', 'R') and (r + v != start[1] or c + h != start[0])]
        path = []
        c, r = start  # Current position
        c_e, r_e = end # Target position
        last_h, last_v = 0, 0 # Last move
        while c != c_e or r != r_e:
            if len(junction(c, r)) > 0:
                break
            d = sqrt((c_e - c) ** 2 + (r_e - r) ** 2) - 0.5
            dir_h, dir_v = 0, 0
            if d > 0:
                dir_h, dir_v = (c_e - c) / d , (r_e - r) /d
            weighted_moves_p = {}
            weighted_moves_n = {}
            weighted_moves = {}
            for move_h, move_v in possible_moves(c, r):
                if last_h + move_h == 0 and last_v + move_v == 0:
                    continue
                dir = move_h * dir_h + move_v * dir_v
                if dir > 0:
                    weighted_moves_p[(move_h, move_v)] = dir
                else:
                    weighted_moves_n[(move_h, move_v)] = dir
            if len(weighted_moves_p) > 0:
                weighted_moves = weighted_moves_p
                if (last_h, last_v) in weighted_moves:
                    weighted_moves[(last_h, last_v)] += 1
            elif len(weighted_moves_n) > 0:
                m = min(weighted_moves_n.values())
                weighted_moves = {k: v - m for k, v in weighted_moves_n.items()}

            if len(weighted_moves) == 0:
                break
            keys, values = list(zip(*(list(weighted_moves.items()))))
            if len(keys) > 1:
                try:
                    move = choices(keys, weights=values)
                except:
                    break
                move_h, move_v = move[0]
            else:
                move_h, move_v = keys[0]
            c += move_h
            r += move_v
            last_h, last_v = move_h, move_v
            if self.board[r][c] in ("R", "V"):
                break
            if c != c_e or r != r_e:
                path.append((c, r))
        for c, r in path:
            self.board[r][c] = "R"

    def update_board_at(self, positions, what):
        for c, r in positions:
            self.board[r][c] = what

    def generate_island(self):
        mountains_factor = 1.0
        mountains_thickness = 1.0
        woods = 1.0
        woods_thickness = 1.0
        ponds = 1.0
        ponds_thickness = 1.0
        meadow = 1.0
        meadow_thickness = 1.0

        # Island shaped creation
        self.board[self.height // 2][self.width // 2] = "X"
        self.multiple_pass("X", 0.08, int(min(self.height, self.width) * 1.2), direction=random() * pi)
        self.invert_board("S")

        cities = self.get_random_positions(randrange(7, 14))
        self.update_board_at(cities, "V")
        if len(cities) > 0:
            base_city = cities.pop()
            while len(cities) > 0:
                c, r = base_city
                distances = [((c_city, r_city), (c_city - c) ** 2 + (r_city - r) ** 2) for c_city, r_city in cities]
                # distances = sorted(distances, key=lambda x:x[1])
                shuffle(distances)
                for target_city, _ in distances[:2]:
                    self.draw_road(base_city, target_city)
                base_city = cities.pop()

        # Island shaped creation
        self.multiple_pass("S", 0.2, 1, to_what="G")   # Plage le long de la mer
        self.multiple_pass("G", 0.05, 4)  # Extension des plages
        self.multiple_pass("S", 0.05, 1, to_what="X") # Falaise le long de la mer
        self.multiple_pass("G", 0.05, 1, to_what="X") # Falaise le long du sable
        self.multiple_pass("X", 0.1, 4, direction=random() * pi) # Extension des falaises

        # Montains
        island_size = min(self.width, self.height)
        mountain_seeds = int(mountains_factor * island_size // 7)
        mountain_thickness = int(island_size * mountains_thickness) // 4

        self.put_random_obstacles("M", randrange(int(mountain_seeds * 0.8) , mountain_seeds))
        self.multiple_pass("M", 0.10, randrange(int(mountain_thickness * 0.8), mountain_thickness), direction=random() * pi)

        # Forêt jouxtant la montagne
        self.multiple_pass("M", 0.1, 1, "F")  # Départ à partir de la montagne
        self.multiple_pass("F", 0.1, 3, "F")  # Etendre un peu

        # Bois
        self.put_random_obstacles("B", int(woods * 8))
        self.multiple_pass("B", 0.2, int(woods * 3))

        # Etangs
        self.put_random_obstacles("E", int(ponds * 6))
        self.multiple_pass("E", 0.3, int(ponds * 3))

        # Prairie
        self.put_random_obstacles("P", int(6 * meadow))
        self.multiple_pass("P", 0.3, int(5 * meadow_thickness))

        # Champs
        self.fill_with("C")


if __name__ == "__main__":
    import pygame

    def display_colored_board(screen, board, width, height, size_x, size_y):
        terrains = {
            "S": Color(20, 196, 250),  # "Mer"
            "E": Color(162, 224, 242),  # Etang
            "M": Color(74, 43, 5),  # "Montagne"
            "F": Color(5, 74, 48),  # Forêt
            "B": Color(8, 196, 55),  # Bois
            "P": Color(194, 240, 43),  # "Prairie",
            "C": Color(222, 209, 109),  # "Champs",
            "X": Color(100, 75, 10),  # Falaises
            "G": Color(252, 236, 88),  # Plage
            "R": Color(255, 255, 255),  # Road
            "V": Color(255, 0, 0),  # City
        }
        f_x, f_y = int(size_x / width), int(size_y / height)
        for r, line in enumerate(board):
            for c, cell in enumerate(line):
                rect = Rect(c * f_x, r * f_y, f_x, f_y)
                pygame.draw.rect(screen, terrains[cell], rect)


    terrain = Terrain()
    terrain.generate_island()
    a_board = terrain.get_board()
    width, height = terrain.get_dimensions()

    pygame.init()
    screen_size = 800
    f = int(screen_size / max(width, height))
    size_x, size_y = width * f, height * f
    screen = pygame.display.set_mode((size_x, size_y))
    pygame.display.set_caption('OnePyce terrain generator')
    pygame.mouse.set_visible(0)

    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((250, 250, 250))
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
        screen.blit(background, (0, 0))
        display_colored_board(screen, a_board, width, height, size_x, size_y)
        pygame.display.flip()
        clock.tick(10)

