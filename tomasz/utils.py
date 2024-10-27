import numpy as np
from typing import Tuple
from tomasz.map import TomaszMap

from hackathon_bot import *

def distance_l2(pos1, pos2):
    return np.sqrt((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2)

def distance_l1(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

def distance_l_inf(pos1, pos2):
    return max(abs(pos1[0] - pos2[0]), abs(pos1[1] - pos2[1]))

def distance_min(pos1, pos2):
    return min(abs(pos1[0] - pos2[0]), abs(pos1[1] - pos2[1]))

def out_of_bounds(x, y, size):
    #print(x, y, size)
    return x < 0 or x >= size[0] or y < 0 or y >= size[1]


direction_to_delta = {
    Direction.UP: (-1, 0),
    Direction.DOWN: (1, 0),
    Direction.LEFT: (0, -1),
    Direction.RIGHT: (0, 1)
}

oridentation_to_delta = {
    Orientation.HORIZONTAL: ((0, 1), (0, -1)),
    Orientation.VERTICAL: ((1, 0), (-1, 0)),
}

def propagate(
        grid: np.ndarray, 
        map: TomaszMap, 
        start_pos: Tuple[int, int], 
        dir: Direction | Orientation | Tuple[int, int] | str,
        decay=1,
        start_pos_not_included=False
    ):
    """
    Propagate a value from a start position in a direction until a wall is hit.

    Args:
        grid: The grid to propagate the value on
        start_pos: The starting position
        dir: The direction to propagate in
        decay: The decay factor for the value
    """
    if isinstance(dir, Direction):
        delta = direction_to_delta[dir]
        propagate(grid, map, start_pos, delta, decay, start_pos_not_included)
        return
    elif isinstance(dir, Orientation):
        delta1, delta2 = oridentation_to_delta[dir]
        propagate(grid, map, start_pos, delta1, decay, start_pos_not_included)
        propagate(grid, map, start_pos, delta2, decay, start_pos_not_included)
        return
    elif dir == "ALL":
        for delta in direction_to_delta.values():
            propagate(grid, map, start_pos, delta, decay, start_pos_not_included)
        return

    x, y = start_pos
    delta_x, delta_y = dir

    value = 1
    for _ in range(map.size[0]):
        x += delta_x
        y += delta_y
        if out_of_bounds(x, y, map.size) or map.walls_arr[x, y]:
            break
        grid[x, y] = 1 - (1 - grid[x, y]) * (1 - value)
        value *= decay

    if start_pos_not_included:
        grid[start_pos] = 0
    else:
        grid[start_pos] = 1

    return
