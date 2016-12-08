import numpy as np
import random

# ################# #
# Convention: 		#
# Wall open   = 0	#
# Wall closed = 1	#
# ################# #


# Global var
lab = None
ver_walls = None
hor_walls = None


# Check if lab contains only zeros
def contains_only_zeros(matrix):
    for x in range(0, matrix[0].size):
        for y in range(0, matrix[0].size):
            if matrix[x, y] != 0:
                return False
    return True


# Open beginning and end of the lab
def open_entrees(size):
    global ver_walls, hor_walls

    if random.random() < 0.5:
        # Open top-bot
        cell_top = random.randint(0, size)
        cell_bot = random.randint(0, size)
        hor_walls[0, cell_top] = 1
        hor_walls[size, cell_bot] = 1
    else:
        # Open left-right
        cell_left = random.randint(0, size)
        cell_right = random.randint(0, size)
        ver_walls[cell_left, 0] = 1
        ver_walls[cell_right, size] = 1


# Initialize lists
def init_matrix(size):
    global lab, hor_walls, ver_walls

    # Init values of lab and the other two walls matrix
    lab = np.fromfunction(lambda i, j: j + size * i, (size, size), dtype=int)
    ver_walls = np.zeros((size + 1, size + 1), dtype=np.int)
    hor_walls = np.zeros((size + 1, size + 1), dtype=np.int)

    open_entrees(size)


# Put the whole path linked to the opened wall to the min value
def set_path_min_value(c1, c2):
    global lab

    value = min(lab[c1[0], c1[1]], lab[c2[0], c2[1]])
    old = max(lab[c1[0], c1[1]], lab[c2[0], c2[1]])

    for j in range(0, lab[0].size):
        for i in range(0, lab[0].size):
            if lab[i, j] == old:
                lab[i, j] = value


# Returns the list of walls that split two paths not connected
def walls_splitting():
    global lab, hor_walls, ver_walls

    # Left list: vertical walls
    # Right list: horizontal walls
    res = ([], [])

    max_size = lab[0].size

    for j in range(0, max_size):
        for i in range(0, max_size):
            if lab[i, j] != lab[i - 1, j]:
                couple = (i, j)
                res[0].append(couple)
            if lab[i, j] != lab[i, j - 1]:
                couple = (i, j)
                res[1].append(couple)
    return res


# Choose one random wall and opens it then call set_path_min_value function
def open_next_wall():
    global lab, hor_walls, ver_walls

    max_size = lab[0].size - 1

    walls = walls_splitting()
    vertical_walls = walls[0]
    horizontal_walls = walls[1]

    if (random.random() < 0.5 and vertical_walls) or not horizontal_walls:
        number = random.randint(0, len(vertical_walls) - 1)

        x = vertical_walls[number][0]
        y = vertical_walls[number][1]

        x2 = x - 1
        y2 = y
    else:
        number = random.randint(0, len(horizontal_walls) - 1)

        x = horizontal_walls[number][0]
        y = horizontal_walls[number][1]

        x2 = x
        y2 = y - 1

    c1 = (x, y)
    c2 = (x2, y2)

    set_path_min_value(c1, c2)

    print(lab)
    print("")


# Draw the lab with tkinter
def draw_lab():
    global lab, hor_walls, ver_walls
    pass


# Main function of the program
def main():
    global lab, hor_walls, ver_walls

    # size = int(input("Enter the size of the labyrinth: "))
    # init_matrix(size)
    init_matrix(5)

    i = 0
    while not (contains_only_zeros(lab)):
        print(i)
        open_next_wall()
        i += 1

    draw_lab()


# Launch main when file is called
if __name__ == '__main__':
    main()
