import random
import copy

terrains = {
    "S" : "Mer",
    "P" : "Prairie",
    "M" : "Montagne",
    "F" : "Forêt",
    "C" : "Champs",
    "E" : "Etangs",
    "B" : "Bois"
}

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
                    if is_inside_board(board, around_r, around_c) and random.random() < threshold:
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

width, height = 60, 60
a_board = init_board(width, height)

# Island shaped creation
a_board[height // 2][width // 2] = "X"
multiple_pass(a_board, "X", 0.08, int(min(height, width) / 1))
invert_board(a_board, "S")
print_board(a_board)

# Montagne
put_random_obstacles(a_board, "M", 10)
multiple_pass(a_board, "M", 0.1, 10)
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


