import numpy as np
from typing import Tuple
from tomasz.map import TomaszMap

from hackathon_bot import *

def distance_l2(pos1, pos2):
    return np.sqrt((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2)

def out_of_bounds(x, y, size):
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


def possible_moves(pos, ori, walls):
    if ori == Orientation.HORIZONTAL:
        moves = { (pos[0] -1, pos[1]), (pos[0] + 1, pos[1]) }
    else:
        moves = { (pos[0], pos[1] - 1), (pos[0], pos[1] + 1) }

    moves = { move for move in moves if not out_of_bounds(*move, walls.size) and not walls[move] }
    return moves

def shortest_path_dfs(start_pos: (int, int), start_dir: Orientation, walls: np.ndarray, target: Tuple[int, int] | np.ndarray):
    visited = {
        Orientation.HORIZONTAL: np.zeros((walls.shape), dtype=bool),
        Orientation.VERTICAL: np.zeros((walls.shape), dtype=bool),
    }

    if isinstance(target, tuple):
        target = np.zeros(walls.shape, dtype=bool)
        target[target] = True

    def dfs(pos, ori, path):
        if target[pos]:
            return path

        visited[ori][pos] = True

        for move in possible_moves(pos, ori, walls):
            if visited[ori][move]:
                continue

            result = dfs(move, ori, path + [move])
            if result:
                return result
            
        if isinstance(path[-1], Orientation):
            # we dont want to chagne orientation if we just changed it
            return None
        
        new_ori = Orientation.HORIZONTAL if ori == Orientation.VERTICAL else Orientation.VERTICAL
        result = dfs(move, new_ori, path + [new_ori])
        if result:
            return result


        return None
    

    return dfs(start_pos, start_dir, [start_pos])
