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
START = []
END = []
value_matrix = np.zeros((HEIGHT, WIDTH))
junctions = []
assert WIDTH % 2 == 1 and WIDTH >= 3
assert HEIGHT % 2 == 1 and HEIGHT >= 3


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


def get_maze():
    global START, END, value_matrix
    # find start and end position in the matrix
    START = (
        int(np.where(value_matrix == 2)[0][0]),
        int(np.where(value_matrix == 2)[1][0]),
    )
    END = (
        int(np.where(value_matrix == -2)[0][0]),
        int(np.where(value_matrix == -2)[1][0]),
    )
    printc(f"start: {START},    end: {END}")

    # assign value to each cell base on its distance to the end point
    for i, val in np.ndenumerate(value_matrix):
        if val == 1:
            # value_matrix[i] = ((i[0] - END[0]) ** 2) + ((i[1] - END[1]) ** 2)
            value_matrix[i] = abs(i[0] - END[0]) + abs(i[1] - END[1])
    printc(value_matrix)


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
        if maze[pos] != 0:
            possible_moves.append(pos)

    printc("init position: ", position, neighbor_cells, possible_moves)

    # move the head
    # TODO: tidyup this section
    if len(possible_moves) == 1:
        position = possible_moves[0]
    elif len(possible_moves) > 1:
        # in case of multiple possible moves, choose the cell that is closer to the end point
        min_val = 100000  # should be greater than the maximum disctance possible from end point
        min_val_pos = []
        for i in possible_moves:
            if value_matrix[i] < min_val:
                min_val = value_matrix[i]
                min_val_pos = i
        position = min_val_pos
        possible_moves.remove(min_val_pos)
        junctions.append(
            possible_moves
        )  # junctions are cells that multiple moves can be performed from them

    printc("final position: ", position, neighbor_cells, possible_moves)
    # TODO: define a history variable that contains all moves preformed. then you can copy history from beginning till history.index(junctions[0][i])
    # TODO: make this function recursive. check to see if we reached the end point or not. if we reached it we can append the path that we took to a list
    # TODO: and try other paths. (junctions)


##################
# STARTING POINT #
##################
# generate maze
# random.seed(4)
random.seed(int(random.random() * 10))
maze = generate_maze(HEIGHT, WIDTH)  # generated maze is a numpy ndarray
value_matrix = np.copy(maze)
printc(maze)


get_maze()
find_move(START)
