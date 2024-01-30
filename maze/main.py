"""
# Summary
A python program to find the shortest path in a given maze.
"""


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
correct_paths = []  # list of paths that reach the end
dead_ends = []  # list of paths that reach a dead-end
solved_maze = []  # MAZE with the shortest path specified
MAZE = np.array((HEIGHT, WIDTH))  # randomly generated maze
START = tuple()  # start point
END = tuple()  # end point
VALUE_MATRIX = np.array((HEIGHT, WIDTH))  # MAZE with cell values specified


########################
# FUNCTION DEFINITIONS #
########################
def printc(*text: object, color="\033[0m", sep=" ", end="\n") -> None:
    """
    ### Summary:
        prints colored text to the terminal using ANSI Codes and python's built-in print() function.

    ### Args:
        text: the text to be printed (accepts multiple values).
        color (str, optional): use colors.fg.color to select the text color. Defaults to white.
        sep (str, optional): Defaults to " ".
        end (str, optional): Defaults to "\\n".
    """
    print(*[f"{color}{t}{colors.reset}" for t in text], end=end, sep=sep)


def get_maze(maze):
    """
    ### Summary:
        Finds start and end point of the maze and assigns value to each cell base on their disctance from the end.

    ### Args:
        maze (np.ndarray): Generated maze from mazebackend.py

    ### Returns:
        tuple: Start point
        tuple: End point
        np.ndarray: Value matrix
    """
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
    # assign value to each cell base on its distance to the end point
    for i, val in np.ndenumerate(value_matrix):
        if val != 0:
            # value_matrix[i] = ((i[0] - end[0]) ** 2) + ((i[1] - end[1]) ** 2)
            value_matrix[i] = abs(i[0] - end[0]) + abs(i[1] - end[1])

    printc(f"\ncell values:\n{value_matrix}")
    return start, end, value_matrix


def find_move(position: tuple, history: list) -> list:
    """
    ### Summary:
    Checks neighbor cells and returns a list of possible moves

    Args:
        position (tuple): Current position of the head
        history (list): List of moves that are preformed until now

    Returns:
        list: List of all possible moves
    """
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
        if (
            (MAZE[pos] == 1 or MAZE[pos] == -2)
            and pos not in history
            and position != END
        ):
            possible_moves.append(pos)

    return possible_moves


def find_shortest_path() -> list:
    """
    ### summary:
    Finds the shortest path from correct_paths global variable

    ### Returns:
        list: List of moves performed in the shortest path
    """
    global VALUE_MATRIX, correct_paths
    # calculate the cost of each path
    my_dict = {}
    cost = [0 for i in range(len(correct_paths))]
    for i, path in enumerate(correct_paths):
        for j, pos in enumerate(path):
            cost[i] += VALUE_MATRIX[pos]
        my_dict.update({cost[i]: path})
    # find the shortest path
    shortest_path = sorted(my_dict.items())[0][1]
    return shortest_path


def print_solution(shortest_path: list) -> None:
    """
    ### Summary:
    Prints the maze and the shortest path

    ### Args:
        shortest_path (list): List of moves performed in the shortest path
    """
    # generate solution maze
    for i, row in enumerate(solved_maze):
        for j, cell in enumerate(row):
            if (i, j) in shortest_path:
                solved_maze[i][j] = colors.fg.green + (chr(9608) * 2) + colors.reset
            elif cell == 0:
                solved_maze[i][j] = colors.reset + (chr(9608) * 2)
            elif cell == 1:
                solved_maze[i][j] = colors.reset + "  "

    # print solution maze
    for i, row in enumerate(solved_maze):
        for j, cell in enumerate(row):
            print(cell, end="")
        print()


def find_path(position, n, history, cost):
    if n == -1:
        while True:
            possible_moves = find_move(position, history)
            position, history = check_junction(position, history, possible_moves)
            if position == (-1, -1) and history == []:
                break
    elif n > 0:
        for i in range(n):
            possible_moves = find_move(position, history)
            position, history = check_junction(position, history, possible_moves)
            cost += VALUE_MATRIX[position]
            possible_moves = find_move(position, history)
            if position == END or (position != END and len(possible_moves) == 0):
                break
        return position, history, cost, possible_moves


def check_junction(position, history, possible_moves):
    if len(possible_moves) == 0:  # dead end
        return (-1, -1), []
    elif len(possible_moves) == 1:  # move
        position, history = move(position, history, possible_moves)
        if position == END:
            correct_paths.append(history)
        return position, history
    elif len(possible_moves) > 1:
        check_good_path(position, history, possible_moves)
        return (-1, -1), []


def check_good_path(position, history, possible_moves):
    junction = position
    for i in possible_moves:
        position = i
        cost = VALUE_MATRIX[position]
        history.append(i)
        position, history, cost, possible_moves = find_path(
            position, 5 - 1, history, cost
        )  # n is 5

        if position == END:
            correct_paths.append(history)
        elif len(possible_moves) == 0:
            pass
        elif len(possible_moves) != 0 and (cost - VALUE_MATRIX[junction] * 5 <= -2):
            find_path(position, -1, history, 0)
            # or
            # k = history.index(i)
            # history = history[: k + 1]
            # find_path(i, -1, history, 0)
        elif len(possible_moves) != 0 and (cost - VALUE_MATRIX[junction] * 5 > -2):
            pass
        # prepare history for the next move in the junction
        k = history.index(junction)
        history = history[: k + 1]


def move(position, history, possible_moves):
    position = possible_moves[0]
    history.append(position)
    return position, history


##################
# STARTING POINT #
##################
# generate maze
random.seed(135)
# random.seed(int(random.random() * 10))
MAZE = generate_maze(HEIGHT, WIDTH)  # generated maze is a numpy ndarray
printc(f"\nmaze:\n{MAZE}")
solved_maze = MAZE.astype("int").tolist()

START, END, VALUE_MATRIX = get_maze(MAZE)

# ! doesn't work in some situations. try 13x13
find_path(START, -1, [START], 0)
shortest_path = find_shortest_path()
print_solution(shortest_path)

# * mishe vase inke hata az in ham efficient tar she, ye flag noJunction tooye find_path tarif konim ke baes she vaghti darim khode junction haro baresi mikonim, dige junction haye oonaro check nakonim
