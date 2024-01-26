import random

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
