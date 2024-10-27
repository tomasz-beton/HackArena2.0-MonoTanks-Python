from tomasz.map import TomaszMap
import numpy as np
from hackathon_bot import *
from typing import Tuple
from tomasz.utils import out_of_bounds

direction_to_delta = {
    Direction.UP: (-1, 0),
    Direction.DOWN: (1, 0),
    Direction.LEFT: (0, -1),
    Direction.RIGHT: (0, 1)
}

oridentation_to_delta = {
    Orientation.HORIZONTAL: (0, 1),
    Orientation.VERTICAL: (1, 0)
}

def propagate(grid: np.ndarray, map: TomaszMap, start_pos: Tuple[int, int], delta: Tuple[int, int], decay=0.9):
    x, y = start_pos
    delta_x, delta_y = delta

    value = 1
    for _ in range(20):
        x += delta_x
        y += delta_y
        if out_of_bounds(x, y, map.size) or map.walls_arr[x, y]:
            break
        grid[x, y] = 1 - (1 - grid[x, y]) * (1 - value)
        value *= decay

    return grid

def get_danger(map: TomaszMap):
    # mines are danger 
    # bullets and their future positions are danger
    # lasers are danger
    # tanks are danger

    danger_map = np.zeros(map.size, dtype=float)
    for i in range(map.size[0]):
        for j in range(map.size[1]):
            for entity in map.entities_grid[i, j]:
                if entity['type'] == 'mine':
                    danger_map[i, j] = 1
                elif entity['type'] == 'bullet':
                    delta = direction_to_delta[entity['dir']]
                    propagate(danger_map, map, (i, j), delta, decay=0.9)
                elif entity['type'] == 'laser':
                    delta1 = oridentation_to_delta[entity['ori']]
                    delta2 = (-delta1[0], -delta1[1])
                    propagate(danger_map, map, (i, j), delta1, decay=1)
                    propagate(danger_map, map, (i, j), delta2, decay=1)
                    danger_map[i, j] = 1
                elif entity['type'] == 'tank':
                    delta = direction_to_delta[entity['turret_dir']]
                    propagate(danger_map, map, (i, j), delta1, decay=0.7)

    return danger_map


def visualize_danger(danger_map: np.ndarray) -> np.ndarray:
    # Define symbols for different danger levels (from light to dark)
    symbols = [' ', '░', '▒', '▓', '█']
    
    # Initialize char_map with spaces, matching the shape of danger_map
    char_map = np.full(danger_map.shape, " ", dtype=str)
    
    for i in range(danger_map.shape[0]):
        for j in range(danger_map.shape[1]):
            # Map the danger level to an index in symbols
            level = int(danger_map[i, j] * (len(symbols) - 1))
            char_map[i, j] = symbols[level]
    
    return char_map


def get_sight(map: TomaszMap):
    sight_map = np.zeros(map.size, dtype=int)
    for enemy in map.tanks:
        for delta in direction_to_delta.values():
            propagate(sight_map, map, enemy['pos'], delta, decay=1)
    return sight_map
        
