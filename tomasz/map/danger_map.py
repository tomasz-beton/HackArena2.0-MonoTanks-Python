from tomasz.map import TomaszMap
import numpy as np
from hackathon_bot import *
from typing import Tuple
from tomasz.utils import propagate




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
                    propagate(danger_map, map, (i, j), entity['dir'], decay=0.9, start_pos_not_included=True)
                elif entity['type'] == 'laser':
                    propagate(danger_map, map, (i, j), entity['ori'], decay=1)
                elif entity['type'] == 'tank' and not entity['agent']:
                    propagate(danger_map, map, (i, j), entity['turret_dir'], decay=0.7)

    return danger_map


def visualize_danger(danger_map: np.ndarray) -> np.ndarray:
    # Define symbols for different danger levels (from light to dark)
    symbols = [' ', '░', '▒', '▓', '█']
    
    # Initialize char_map with spaces, matching the shape of danger_map
    char_map = np.full(danger_map.shape, " ", dtype=str)
    
    for j in range(danger_map.shape[0]):
        for i in range(danger_map.shape[1]):
            # Map the danger level to an index in symbols
            level = int(danger_map[i, j] * (len(symbols) - 1))
            char_map[i, j] = symbols[level]
    
    return char_map.T


def get_sight(map: TomaszMap):
    sight_map = np.zeros(map.size, dtype=int)
    for enemy in map.tanks:
        for delta in direction_to_delta.values():
            propagate(sight_map, map, enemy['pos'], delta, decay=1)
    return sight_map
        
