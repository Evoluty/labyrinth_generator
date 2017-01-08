#!/usr/bin/python3

import numpy as np
import random
from tkinter import *

from threading import Thread

# ################# #
# Convention: 		#
# Wall closed = 0	#
# Wall opened = 1	#
# ################# #

# Global var
lab = None
ver_walls = None
hor_walls = None
size_win = 1000


# Check if lab contains only zeros
def contains_only_zeros(matrix):
    for y in range(0, matrix.shape[0]):
        for x in range(0, matrix.shape[0]):
            if matrix.item(x, y) != 0:
                return False
    return True


# Open beginning and end of the lab
def open_entrees(size):
    global ver_walls, hor_walls

    if random.random() < 0.5:
        # Open top-bot
        cell_top = random.randint(0, size - 1)
        cell_bot = random.randint(0, size - 1)
        hor_walls.itemset((0, cell_top), 1)
        hor_walls.itemset((size, cell_bot), 1)
    else:
        # Open left-right
        cell_left = random.randint(0, size - 1)
        cell_right = random.randint(0, size - 1)
        ver_walls.itemset((cell_left, 0), 1)
        ver_walls.itemset((cell_right, size), 1)


# Initialize lists
def init_matrix(size):
    global lab, hor_walls, ver_walls

    # Init values of lab and the other two walls matrix
    lab = np.fromfunction(lambda i, j: j + size * i, (size, size), dtype=int)
    ver_walls = np.zeros((size, size + 1), dtype=np.int)
    hor_walls = np.zeros((size + 1, size), dtype=np.int)

    open_entrees(size)


# Returns the list of walls that split two paths not connected
def walls_splitting():
    global lab

    # Left list: vertical walls
    # Right list: horizontal walls
    res = ([], [])

    max_size = lab.shape[0]

    for j in range(0, max_size):
        for i in range(1, max_size):
            if lab.item(j, i) != lab.item(j, i - 1):
                couple = (i, j)
                res[0].append(couple)

    for j in range(1, max_size):
        for i in range(0, max_size):
            if lab.item(j, i) != lab.item(j - 1, i):
                couple = (i, j)
                res[1].append(couple)

    return res


# Put the whole path linked to the opened wall to the min value
def set_path_min_value(c1, c2):
    global lab

    value = min(lab.item(c1[1], c1[0]), lab.item(c2[1], c2[0]))
    old = max(lab.item(c1[1], c1[0]), lab.item(c2[1], c2[0]))

    for j in range(0, lab.shape[1]):
        for i in range(0, lab.shape[0]):
            if lab.item(j, i) == old:
                lab.itemset((j, i), value)


# Choose one random wall and opens it then call set_path_min_value function
def open_next_wall():
    global lab, hor_walls, ver_walls

    walls = walls_splitting()
    vertical_walls = walls[0]
    horizontal_walls = walls[1]

    if (random.random() < 0.5 and vertical_walls) or not horizontal_walls:
        number = random.randint(0, len(vertical_walls) - 1)

        x = vertical_walls[number][0]
        y = vertical_walls[number][1]
        x2 = x - 1
        y2 = y
        ver_walls.itemset((y, x), 1)
    else:
        number = random.randint(0, len(horizontal_walls) - 1)

        x = horizontal_walls[number][0]
        y = horizontal_walls[number][1]
        x2 = x
        y2 = y - 1
        hor_walls.itemset((y, x), 1)

    c1 = (x, y)
    c2 = (x2, y2)

    set_path_min_value(c1, c2)


# Draw the lab with PyQt
def draw_lab():
    global lab, ver_walls, hor_walls, size_win

    w = Tk()

    width_l = size_win / 100
    size_mat = lab.shape[0]
    size_line = size_win / size_mat

    canvas = Canvas(w, width=size_win, height=size_win, background='white')

    for j in range(0, size_mat + 1):
        for i in range(0, size_mat):
            if ver_walls.item(i, j) == 0:
                canvas.create_line(j * size_line, i * size_line - (width_l / 2), j * size_line,
                                   i * size_line + size_line + (width_l / 2),
                                   width=width_l)

    for j in range(0, size_mat):
        for i in range(0, size_mat + 1):
            if hor_walls.item(i, j) == 0:
                canvas.create_line(j * size_line - (width_l / 2), i * size_line,
                                   j * size_line + size_line + (width_l / 2), i * size_line,
                                   width=width_l)

    canvas.pack()
    w.mainloop()


def get_start():
    global lab, ver_walls, hor_walls

    size_mat = lab.shape[0]

    for y in range(0, size_mat):
        if hor_walls.item(0, y) == 1:
            return 0, y

    for x in range(0, size_mat):
        if ver_walls.item(x, 0) == 1:
            return x, 0

    return None


def get_exit():
    global lab, ver_walls, hor_walls

    size_mat = lab.shape[0]

    for y in range(0, size_mat):
        if hor_walls.item(size_mat, y) == 1:
            return size_mat, y

    for x in range(0, size_mat):
        if ver_walls.item(x, size_mat) == 1:
            return x, size_mat

    return None


def is_exit(x, y):
    global lab, ver_walls, hor_walls

    size_mat = lab.shape[0]

    if x == size_mat - 1 and hor_walls.item(x + 1, y) == 1:
        return True
    elif y == size_mat - 1 and ver_walls.item(x, y + 1) == 1:
        return True

    return False


def contains_exit(x, y, di):
    global lab, ver_walls, hor_walls

    size_mat = lab.shape[0]

    if x < 0 or y < 0:
        return False
    elif x >= size_mat or y >= size_mat:
        return False

    elif is_exit(x, y):
        return True

    elif di == "Top":
        if x - 1 < 0:
            return False
        if hor_walls.item(x, y) == 1 and contains_exit(x - 1, y, "Top"):
            return True
        if hor_walls.item(x, y) == 1 and contains_exit(x - 1, y, "Left"):
            return True
        if hor_walls.item(x, y) == 1 and contains_exit(x - 1, y, "Right"):
            return True

        return False

    elif di == "Bot":
        if x + 1 >= size_mat:
            return False
        if hor_walls.item(x + 1, y) == 1 and contains_exit(x + 1, y, "Bot"):
            return True
        if hor_walls.item(x + 1, y) == 1 and contains_exit(x + 1, y, "Left"):
            return True
        if hor_walls.item(x + 1, y) == 1 and contains_exit(x + 1, y, "Right"):
            return True

        return False

    elif di == "Left":
        if y - 1 < 0:
            return False
        if ver_walls.item(x, y) == 1 and contains_exit(x, y - 1, "Top"):
            return True
        if ver_walls.item(x, y) == 1 and contains_exit(x, y - 1, "Bot"):
            return True
        if ver_walls.item(x, y) == 1 and contains_exit(x, y - 1, "Left"):
            return True

        return False

    elif di == "Right":
        if y + 1 >= size_mat:
            return False
        if ver_walls.item(x, y + 1) == 1 and contains_exit(x, y + 1, "Top"):
            return True
        if ver_walls.item(x, y + 1) == 1 and contains_exit(x, y + 1, "Bot"):
            return True
        if ver_walls.item(x, y + 1) == 1 and contains_exit(x, y + 1, "Right"):
            return True

        return False

    else:
        return False


def get_exit_path(x, y):
    global lab, hor_walls, ver_walls

    # We are on the exit
    if is_exit(x, y):
        return [(x, y)]

    lab.itemset(x, y, 3)

    # We are in the labyrinth
    if contains_exit(x, y, "Top"):
        next_path = get_exit_path(x - 1, y)
    elif contains_exit(x, y, "Bot"):
        next_path = get_exit_path(x + 1, y)
    elif contains_exit(x, y, "Left"):
        next_path = get_exit_path(x, y - 1)
    else:
        next_path = get_exit_path(x, y + 1)

    return [(x, y)] + next_path


# Main function of the program
def main():
    global lab, hor_walls, ver_walls

    # size = int(input("Enter the size of the labyrinth: "))
    size = 10

    init_matrix(size)

    i = 0
    while not (contains_only_zeros(lab)):
        print(i)
        open_next_wall()
        i += 1

    print()
    print(hor_walls)
    print()
    print(ver_walls)
    print()
    print()

    thread = Thread(target=draw_lab, args=())
    thread.start()

    start = get_start()
    print(get_exit_path(start[0], start[1]))

    thread.join()


# Launch main when file is called
if __name__ == '__main__':
    main()
