import random
import copy


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
    print('-' * (width + 2))
    for r, line in enumerate(board):
        print('|', end='')
        for cell in line:
            print(' ' if cell == 0 else chr(64 + cell), end='')
        print('|')
    print('-' * (width + 2))


def is_inside_board(board, r, c):
    width, height = get_board_dimension(board)
    return c in range(width) and r in range(height)


def one_pass(board, what, threshold):
    previous_board = copy_board(board)
    for r, line in enumerate(previous_board):
        for c, cell in enumerate(line):
            if cell == what:
                for h, v in ((i, j) for i in range(-1, 2) for j in range(-1, 2) if (i, j) != (0, 0)):
                    around_r, around_c = r + v, c + h
                    if is_inside_board(board, around_r, around_c) and random.random() < threshold:
                        board[around_r][around_c] = what


def multiple_pass(board, what, threshold, passes):
    for _ in range(passes):
        one_pass(board, what, threshold)


width, height = 100, 20
a_board = init_board(width, height)
put_random_obstacles(a_board, 1, 10)
multiple_pass(a_board, 1, 0.1, 10)
print_board(a_board)
put_random_obstacles(a_board, 2, 4)
multiple_pass(a_board, 2, 0.3, 8)
print_board(a_board)
