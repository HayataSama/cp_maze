import random

from colors import colors
from mazebackend import generate_maze

# get maze width and maze height from the user
WIDTH = int(input("Enter an odd number for Width: "))
HEIGHT = int(input("Enter an odd number for Height: "))
assert WIDTH % 2 == 1 and WIDTH >= 3
assert HEIGHT % 2 == 1 and HEIGHT >= 3

# generate maze
# random.seed(4)
random.seed(int(random.random() * 10))
maze = generate_maze(HEIGHT, WIDTH)  # generated maze is a numpy ndarray
print(maze)


def printc(*text, color="\033[0m"):
    """
    ### Summary:
        prints colored text to the terminal using ANSI Codes and python's built-in print() function

    ### Args:
        text: the text to be printed (accepts multiple values).
        color (str, optional): use colors.fg._color_ to select the text color. Defaults to white.
    """
    print(*[f"{color}{t}{colors.reset}" for t in text])
