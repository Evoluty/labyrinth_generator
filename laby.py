from tkinter import *
import numpy as np
import random

# ################# #
# Convention: 		#
# Wall open   = 0	#
# Wall closed = 1	#
# ################# #


# Global var
laby = None
wallsVert = None
wallsHor = None


# Check if laby contains only zeros
def contains_only_zeros(matrix):
    for x in range(0, matrix[0].size):
        for y in range(0, matrix[0].size):
            if matrix[x, y] != 0:
                return False
    return True


# Open beginning and end of the laby
def open_entrees(size):
    global wallsVert, wallsHor

    if random.random() < 0.5:
        # Open top-bot
        cell_top = random.randint(0, size)
        cell_bot = random.randint(0, size)
        wallsHor[0, cell_top] = 1
        wallsHor[size, cell_bot] = 1
    else:
        # Open left-right
        cell_left = random.randint(0, size)
        cell_right = random.randint(0, size)
        wallsVert[cell_left, 0] = 1
        wallsVert[cell_right, size] = 1


# Initialize lists
def init_matrix(size):
    global laby, wallsHor, wallsVert

    # Init values of laby and the other two walls matrix
    laby = np.fromfunction(lambda i, j: j + size * i, (size, size), dtype=int)
    wallsVert = np.zeros((size + 1, size + 1), dtype=np.int)
    wallsHor = np.zeros((size + 1, size + 1), dtype=np.int)

    open_entrees(size)


# Put the whole path linked to the opened wall to the min value
def set_path_min_value(c1, c2):
    global laby

    value = min(laby[c1[0], c1[1]], laby[c2[0], c2[1]])
    old = max(laby[c1[0], c1[1]], laby[c2[0], c2[1]])

    for j in range(0, laby[0].size):
        for i in range(0, laby[0].size):
            if laby[i, j] == old:
                laby[i, j] = value


# Returns the list of walls that split two paths not connected
def walls_splitting():
    global laby, wallsHor, wallsVert

    # Left list: vertical walls
    # Right list: horizontal walls
    res = ([], [])

    max_size = laby[0].size - 1

    for j in range(1, max_size):
        for i in range(1, max_size):
            if laby[i, j] != laby[i-1, j]:
                res[0].append((i, j))
            if laby[i, j] != laby[i, j-1]:
                res[1].append((i, j))
    return res


# Choose one random wall and opens it then call set_path_min_value function
def open_next_wall():
    global laby, wallsHor, wallsVert

    max_size = laby[0].size - 1

    x = random.randint(0, max_size)
    y = random.randint(0, max_size)

    c1 = (x, y)

    # Check if corner
    if x == 0 and y == 0:
        direction = random.choice([2, 3])
    elif x == 0 and y == max_size:
        direction = random.choice([1, 2])
    elif x == max_size and y == 0:
        direction = random.choice([3, 4])
    elif x == max_size and y == max_size:
        direction = random.choice([1, 4])
    # Check if edge
    elif x == 0:
        direction = random.choice([1, 2, 3])
    elif x == max_size:
        direction = random.choice([1, 3, 4])
    elif y == 0:
        direction = random.choice([2, 3, 4])
    elif y == max_size:
        direction = random.choice([1, 2, 4])
    # Else go everywhere
    else:
        direction = random.randint(0, 5)

    # TOP
    if direction == 1:
        c2 = (x, y - 1)
        wallsHor[x, y] = 1
    # RIGHT
    elif direction == 2:
        c2 = (x + 1, y)
        wallsVert[x+1, y] = 1
    # BOTTOM
    elif direction == 3:
        c2 = (x, y + 1)
        wallsHor[x, y+1] = 1
    # LEFT
    else:
        c2 = (x - 1, y)
        wallsVert[x, y] = 1

    set_path_min_value(c1, c2)

    print(laby)
    print("")
    print(wallsVert)
    print("")
    print(wallsHor)
    print("")


# Draw the lab with tkinter
def draw_lab():
    global laby, wallsHor, wallsVert
    pass


# Main function of the program
def main():
    global laby, wallsHor, wallsVert

    size = int(input("Enter the size of the labyrinth: "))
    init_matrix(size)

    i = 0
    while not(contains_only_zeros(laby)):
        open_next_wall()
        i += 1

    draw_lab()

    print(laby)
    print("")
    print(wallsVert)
    print("")
    print(wallsHor)


# Launch main when file is called
if __name__ == '__main__':
    main()
