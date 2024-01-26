import random

import numpy as np


def generate_maze(HEIGHT, WIDTH):
    EMPTY = " "
    MARK = "@"
    WALL = chr(9608)  # Character 9608 is '█'
    NORTH, SOUTH, EAST, WEST = "n", "s", "e", "w"
    NOTES = [EMPTY, MARK, WALL, NORTH, SOUTH, EAST, WEST]
    maze = {}
    for x in range(WIDTH):
        for y in range(HEIGHT):
            maze[(x, y)] = WALL
    hasVisited = [(1, 1)]
    maze_dict = visit(1, 1, maze, HEIGHT, WIDTH, NOTES, hasVisited)
    printMaze(maze, HEIGHT, WIDTH, MARK=MARK)
    return dict_to_array(maze_dict, HEIGHT, WIDTH, NOTES)


def printMaze(maze, HEIGHT, WIDTH, MARK="@", markX=None, markY=None):
    for y in range(HEIGHT):
        for x in range(WIDTH):
            if markX == x and markY == y:
                print(MARK * 2, end="")
            else:
                print(maze[(x, y)] * 2, end="")
        print()


def visit(x, y, maze, HEIGHT, WIDTH, NOTES, hasVisited):
    EMPTY, MARK, WALL, NORTH, SOUTH, EAST, WEST = NOTES

    maze[(x, y)] = EMPTY

    while True:
        unvisitedNeighbors = []
        if y > 1 and (x, y - 2) not in hasVisited:
            unvisitedNeighbors.append(NORTH)

        if y < HEIGHT - 2 and (x, y + 2) not in hasVisited:
            unvisitedNeighbors.append(SOUTH)

        if x > 1 and (x - 2, y) not in hasVisited:
            unvisitedNeighbors.append(WEST)

        if x < WIDTH - 2 and (x + 2, y) not in hasVisited:
            unvisitedNeighbors.append(EAST)

        if len(unvisitedNeighbors) == 0:
            return maze
        else:
            nextIntersection = random.choice(unvisitedNeighbors)
            if nextIntersection == NORTH:
                nextX = x
                nextY = y - 2
                maze[(x, y - 1)] = EMPTY  # Connecting hallway.
            elif nextIntersection == SOUTH:
                nextX = x
                nextY = y + 2
                maze[(x, y + 1)] = EMPTY  # Connecting hallway.
            elif nextIntersection == WEST:
                nextX = x - 2
                nextY = y
                maze[(x - 1, y)] = EMPTY  # Connecting hallway.
            elif nextIntersection == EAST:
                nextX = x + 2
                nextY = y
                maze[(x + 1, y)] = EMPTY  # Connecting hallway.
            hasVisited.append((nextX, nextY))  # Mark as visited.
            visit(
                nextX, nextY, maze, HEIGHT, WIDTH, NOTES, hasVisited
            )  # Recursively visit this space.


def dict_to_array(maze_dict, HEIGHT, WIDTH, NOTES):
    EMPTY, MARK, WALL, _, _, _, _ = NOTES
    maze_array = np.zeros((HEIGHT, WIDTH))
    for coord in maze_dict:
        if maze_dict[coord] == WALL:
            maze_array[coord[1], coord[0]] = 0
        elif maze_dict[coord] == EMPTY:
            maze_array[coord[1], coord[0]] = 1
        else:
            maze_array[coord[1], coord[0]] = 2
    nonzero_indices = np.nonzero(maze_array)
    rows, cols = nonzero_indices
    unique_rows = np.unique(rows)
    leftmost_nonzero_indices = [np.min(cols[rows == row]) for row in unique_rows]
    rightmost_nonzero_indices = [np.max(cols[rows == row]) for row in unique_rows]
    mincol = np.min(nonzero_indices[1])
    maxcol = np.max(nonzero_indices[1])
    gaussian_probs_left = np.abs(np.random.normal(0, 1, len(leftmost_nonzero_indices)))
    gaussian_probs_left = gaussian_probs_left / np.sum(gaussian_probs_left)
    gaussian_probs_right = np.abs(
        np.random.normal(0, 1, len(rightmost_nonzero_indices))
    )
    gaussian_probs_right = gaussian_probs_right / np.sum(gaussian_probs_right)
    start_point = [
        mincol,
        np.random.choice(leftmost_nonzero_indices, p=gaussian_probs_left),
    ]
    end_point = [
        maxcol,
        np.random.choice(rightmost_nonzero_indices, p=gaussian_probs_right),
    ]
    maze_array[start_point[0], start_point[1]] = 2
    maze_array[end_point[0], end_point[1]] = -2
    return maze_array
