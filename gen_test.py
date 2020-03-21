import random
import copy
import pygame
from pygame.locals import *
from pygame import Rect, Color

def init_board(width, height):
    return [[0 for _ in range(width)] for _ in range(height)]


def get_board_dimension(board):
    if len(board) == 0:
        return 0, 0
    return len(board[0]), len(board)


def copy_board(board):
    return copy.deepcopy(board)


def put_random_obstacles(board, what, number):
    width, height = get_board_dimension(board)
    for _ in range(number):
        while True:
            c, r = random.randrange(width), random.randrange(height)
            cell_content = board[r][c]
            if cell_content == 0:
                board[r][c] = what
                break


def print_board(board):
    width, height = get_board_dimension(board)
    print('-' * (width +2))
    for r, line in enumerate(board):
        print('|', end='')
        for cell in line:
            print(' ' if cell == 0 else cell, end='')
        print('|')
    print('-' * (width +2))


def is_inside_board(board, r, c):
    width, height = get_board_dimension(board)
    return c in range(width) and r in range(height)


def one_pass(board, what, threshold, to_what = ''):
    previous_board = copy_board(board)
    for r, line in enumerate(previous_board):
        for c, cell in enumerate(line):
            if cell == what:
                for h, v in ((i, j) for i in range(-1, 2) for j in range(-1, 2) if (i,j) != (0,0)):
                    around_r, around_c = r + v, c + h
                    if is_inside_board(board, around_r, around_c) and random.random() < threshold and board[around_r][around_c] == 0:
                        board[around_r][around_c] = what if to_what == '' else to_what


def multiple_pass(board, what, threshold, passes, to_what = ''):
    for _ in range(passes):
        one_pass(board, what, threshold, to_what)

def invert_board(board, fill):
    previous_board = copy_board(board)
    for r, line in enumerate(previous_board):
        for c, cell in enumerate(line):
            board[r][c] = fill if cell == 0 else 0


def fill_with(board, what):
    for r, line in enumerate(board):
        for c, cell in enumerate(line):
            if cell == 0:
                board[r][c] = what




width, height = 120, 120

a_board = init_board(width, height)

# Island shaped creation
a_board[height // 2][width // 2] = "X"
multiple_pass(a_board, "X", 0.08, int(min(height, width) / 1))
invert_board(a_board, "S")
print_board(a_board)

# Montagne
put_random_obstacles(a_board, "M", 10)
multiple_pass(a_board, "M", 0.10, 10)
print_board(a_board)

# Forêt jouxtant la montagne
multiple_pass(a_board, "M", 0.1, 1, "F")  # Départ à partir de la montagne
print_board(a_board)
multiple_pass(a_board, "F", 0.1, 2, "F")  # Etendre un peu
print_board(a_board)

# Bois
put_random_obstacles(a_board, "B", 4)
multiple_pass(a_board, "B", 0.2, 2)
print_board(a_board)

# Etangs
put_random_obstacles(a_board, "E", 3)
multiple_pass(a_board, "E", 0.3, 2)
print_board(a_board)

# Prairie
put_random_obstacles(a_board, "P", 6)
multiple_pass(a_board, "P", 0.3, 5)
print_board(a_board)

# Champs
fill_with(a_board, "C")
print_board(a_board)


def display_colored_board(screen, board, size_x, size_y):
    terrains = {
        "S": Color(20, 196, 250),            # "Mer"
        "E": Color(162, 224, 242),             # Etang
        "M": Color(74, 43,5),        # "Montagne"
        "F": Color(5, 74, 48),          # Forêt
        "B": Color(8,196, 55),         # Bois
        "P": Color(128, 222, 109),           # "Prairie",
        "C": Color(222, 209, 109),          # "Champs",
        "F": Color(100, 75, 10),        # Falaises
        "G": Color(252, 236, 88),       # Plage
    }
    width, height = get_board_dimension(board)
    f_x, f_y = int(size_x / width), int(size_y / height)
    for r, line in enumerate(board):
        for c, cell in enumerate(line):
            rect = Rect(c * f_x, r * f_y, f_x, f_y)
            pygame.draw.rect(screen, terrains[cell], rect)

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
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN and event.key == K_ESCAPE:
            running = False
    screen.blit(background, (0, 0))
    display_colored_board(screen, a_board, size_x, size_y)
    pygame.display.flip()
    clock.tick(10)

