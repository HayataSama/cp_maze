###########
# IMPORTS #
###########
import random

import numpy as np
from colors import colors
from mazebackend import generate_maze

####################
# GLOBAL VARIABLES #
####################
# get maze width and maze height from the user
WIDTH = int(input("Enter an odd number for Width: "))
HEIGHT = int(input("Enter an odd number for Height: "))
assert WIDTH % 2 == 1 and WIDTH >= 3
assert HEIGHT % 2 == 1 and HEIGHT >= 3
history = []  # list of moves that are performed in each path
correct_paths = []  # list of paths that reach the end
dead_ends = []  # list of paths that reach a dead-end


########################
# FUNCTION DEFINITIONS #
########################
def printc(*text, color="\033[0m", sep=" ", end="\n"):
    """
    ### Summary:
        prints colored text to the terminal using ANSI Codes and python's built-in print() function.

    ### Args:
        text: the text to be printed (accepts multiple values).
        color (str, optional): use colors.fg._color_ to select the text color. Defaults to white.
        sep (str, optional) Defaults to " ".
        end (str, optional) Defaults to "\n".
    """
    print(*[f"{color}{t}{colors.reset}" for t in text], end=end, sep=sep)


def get_maze(maze):
    value_matrix = np.copy(maze)
    # find start and end position in the matrix
    start = (
        int(np.where(value_matrix == 2)[0][0]),
        int(np.where(value_matrix == 2)[1][0]),
    )
    end = (
        int(np.where(value_matrix == -2)[0][0]),
        int(np.where(value_matrix == -2)[1][0]),
    )
    history.append(start)
    # assign value to each cell base on its distance to the end point
    for i, val in np.ndenumerate(value_matrix):
        if val != 0:
            # value_matrix[i] = ((i[0] - end[0]) ** 2) + ((i[1] - end[1]) ** 2)
            value_matrix[i] = abs(i[0] - end[0]) + abs(i[1] - end[1])

    printc(f"\ncell values:\n{value_matrix}")
    return start, end, value_matrix


def find_move(position):
    # find all 4 neighbor cells for a given position
    neighbor_cells = [
        (position[0], position[1] + 1),  # right
        (position[0] - 1, position[1]),  # top
        (position[0], position[1] - 1),  # left
        (position[0] + 1, position[1]),  # bottom
    ]

    # find all possible moves for a given position
    possible_moves = []
    for pos in neighbor_cells:
        if (MAZE[pos] == 1 or MAZE[pos] == -2) and pos != history[-1]:
            possible_moves.append(pos)

    return possible_moves


def move(position, possible_moves):
    # if at a given point, multiple moves can be performed, choose the one that gets the head closer to the end point first
    min_val = (
        100000  # should be greater than the maximum distance possible from end point
    )
    for i in possible_moves:
        if VALUE_MATRIX[i] < min_val:
            min_val = VALUE_MATRIX[i]
            min_val_pos = i
    history.append(position)
    position = min_val_pos
    return position


def find_path(position):
    # finds a path, it can lead to the end point or a dead-end
    possible_moves = find_move(position)
    history.pop()  # this makes sure the START position is not duplicated
    while len(possible_moves) != 0:
        position = move(position, possible_moves)
        possible_moves = find_move(position)
        # check whether we have reached the end or a dead-end
        if position == END:
            history.append(position)  # history does not contain the current position
            correct_paths.append(history)
            printc("reached the end!")
            printc(f"path: {history}")
            history.clear()
            break
        if position != END and len(possible_moves) == 0:
            history.append(position)  # history does not contain the current position
            dead_ends.append(history)
            printc("reached a dead-end")
            printc(f"path: {history}")
            history.clear()
            break


##################
# STARTING POINT #
##################
# generate maze
# random.seed(4)
random.seed(int(random.random() * 10))
MAZE = generate_maze(HEIGHT, WIDTH)  # generated maze is a numpy ndarray
printc(f"\nmaze:\n{MAZE}")

START, END, VALUE_MATRIX = get_maze(MAZE)
find_path(START)

# TODO: define junctions variable to find other paths. it should probably be a dictionary so each junction's relationship (parent, child, sibling) with other junctions is specified.
