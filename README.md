# Maze Project

> [!WARNING]
> for now `main.py` doesn't work correctly. please use the non-optimized version, `main_no_opt.py`.

A python program to find the shortest path in a given maze.

## General Description

My approach to finding the shortest path in a given maze was to check all possible paths and find the ones that reach the end. From there by calculating the cost of each path and sorting them in an ascending order I can find the one with the lowest cost which in other words is the shortest path.

For finding all possible paths in a maze we move the head until we reach a junction. For each possible move in the junction we move the head in that direction until we reach the end or a dead-end. If the head reaches the end in its path, then it's appended to a list that stores all paths that solve the maze otherwise it's dropped. By doing this recursively, we can find all possible paths in a maze.

I understand that this method can be very time consuming in a very large maze (like the map of a city) so I tried optimizing it by checking the next "N" moves in each junction. If the head doesn't get closer to the end in the next N moves, that path is dropped and assumed to not be the answer. This solution also has its own flaws but I think the benefits are greater than the downsides. Unfortunately I wasn't able to get it to work so it's still work in progress.

## Defintions

**Head** -- The Head is basically a pointer to the current cell that we are working with. For example we check its neighbors or append it to a path or move it to the next cell.

**Cell** -- Each cell in the maze is represented by it's (x,y) coordinates stored in a tuple.

**Path** -- A path is a sequence of moves. Each path is stored as a list of tuples which contain the (x,y) coordinates of each cell in the the path.

**Junction** -- A cell that multiple moves can be perfomed from.

## Functions

- ### `printc(*text, color, sep, end)`

  Prints colored text to the terminal using ANSI Codes and python's built-in print() function.

- ### `get_maze(maze)`

  Finds start and end point of the maze and assigns value to each cell based on their disctance from the end and stores them in `VALUE_MATRIX` global variable.

- ### `find_move(position)`

  Checks neighbor cells and returns a list of possible moves

- ### `move(position, history, possible_moves)`

  Moves the head in the given direction

- ### `find_path(position, history)`

  This is the main function. It finds the end and dead-ends by moving the head until there is no possible move to be performed.

- ### `check_junction(position, history, possible_moves)`

  Checks the number of possible moves that the head can perform

- ### `check_path(position, history, possible_moves)`

  Checks all possible paths in every junction

- ### `def find_shortest_path()`

  Finds the shortest path from `correct_paths` global variable by calculating the cost of each path and choosing the one with the lowest cost.

- ### `print_solution(shortest_path)`

  Prints the maze with the shortest path highlighted in green
