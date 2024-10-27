import numpy as np

def distance_l2(pos1, pos2):
    return np.sqrt((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2)

def out_of_bounds(x, y, size):
    return x < 0 or x >= size[0] or y < 0 or y >= size[1]
