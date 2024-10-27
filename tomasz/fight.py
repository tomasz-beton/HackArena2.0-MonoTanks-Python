from tomasz.map import TomaszMapWithHistory, TomaszAgent
from tomasz.map.danger_map import get_danger
from tomasz.utils import distance_l2, distance_l1, distance_min, distance_l_inf
import numpy as np
from tomasz.utils import out_of_bounds, propagate, Orientation
from typing import Tuple
from tomasz.movement import MovementSystem, _get_needed_rotation, parse_dir_to_delta
from hackathon_bot import *

import logging
log = logging.getLogger(__name__)
log.disabled = False


class AlignmentSystem:
    def __init__(self, tomasz_map: TomaszMapWithHistory, movement_system: MovementSystem):
        self.map = tomasz_map
        self.movement_system = movement_system

        self.is_aligned = False
        self.target = None

    def get_closest_enemy(self, distance = "l_min", only_visible=True):
        tomasz = self.map.agent
        enemies = self.map.tanks
        enemies = [enemy for enemy in enemies if not enemy["agent"]]
        if only_visible:
            enemies = [enemy for enemy in enemies if self.map.visible_arr[enemy["pos"]]]
        if len(enemies) == 0:
            return None
        
        if distance == "l1":
            distance = distance_l1
        elif distance == "l2":
            distance = distance_l2
        elif distance == "l_min":
            distance = distance_min
        elif distance == "l_inf":
            distance = distance_l_inf
        else:
            raise ValueError("Invalid distance metric")
    
        closest_enemy = min(enemies, key=lambda e: distance(tomasz.position, e["pos"]))
        return closest_enemy
    

    def _closest_point(self, bool_array, start, distance="l1"):
        true_points = np.argwhere(bool_array)
        
        if true_points.size == 0:
            return None
        
        if distance == "l1":
            distances = np.sum(np.abs(true_points - start), axis=1)
        elif distance == "l2":
            distances = np.sum((true_points - start) ** 2, axis=1)
        else:
            raise ValueError("Invalid distance metric")

        min_index = np.argmin(distances)
        
        x, y = true_points[min_index]
        return (int(x), int(y))
    

    def _get_turret_rotation(self, position: Tuple[int, int], target: Tuple[int, int], current_dir: Direction):
        if position == target:
            log.warning("position == target what the hell")
            return None
        if position[1] == target[1]:
            if position[0] > target[0]:
                desired_dir = Direction.LEFT
            else:
                desired_dir = Direction.RIGHT
        elif position[0] == target[0]:
            if position[1] > target[1]:
                desired_dir = Direction.UP
            else:
                desired_dir = Direction.DOWN
        else:
            log.warning("position and target are not aligned")
            return None
        
        log.warning(f"desired_dir: {desired_dir}")
        log.warning(f"current_dir: {current_dir}")
        delta = parse_dir_to_delta(desired_dir)
        log.warning(f"delta: {delta}")
        result = _get_needed_rotation(delta, current_dir)
        log.warning(f"result: {result}")

        return result
        

    def get_action(self):
        log.info("get_action")
        if self.is_aligned:
            log.info("is aligned")
            return None
        
        tomasz = self.map.agent
        log.warning(f"tomasz: {tomasz.position} {tomasz.direction}, {tomasz.entity}")
        closest_enemy = self.get_closest_enemy()
        log.info(f"closest_enemy: {closest_enemy}")
        if closest_enemy is None:
            log.info("no enemies?")
            return
        
        sight = np.zeros(self.map.size, dtype=bool)
        propagate(sight, self.map, closest_enemy["pos"], "ALL", decay=1)
        
        if sight[tomasz.position]:
            log.info("we have a sight on the enemy")

            rot = self.get_turret_rotation(tomasz.position, closest_enemy["pos"], tomasz.entity.turret.direction)
            if rot is not None:
                log.info("rotating turret!")
                return Rotation(None, rot)
            
            self.is_aligned = True
            return None
        
        closest_sight_point = self._closest_point(sight, tomasz.position)
        if closest_sight_point is None:
            log.info("no point in sight? this should not happen")
            return
        
        self.movement_system.target = closest_sight_point
        move = self.movement_system.get_action(tomasz)

        return move
    
    def check_alignment(self):
        tomasz = self.map.agent
        closest_enemy = self.get_closest_enemy()
        sight = np.zeros(self.map.size, dtype=bool)
        propagate(sight, self.map, closest_enemy["pos"], "ALL", decay=1)
        
        if not sight[tomasz.position]:
            self.is_aligned = False
            return False
        
        rot = self.get_turret_rotation(tomasz.position, closest_enemy["pos"], tomasz.entity.turret.direction)
        if rot is not None:
            self.is_aligned = False
            return False
        
        self.is_aligned = True
            
        return True


# def possible_moves(pos, ori, walls):
#     if ori == Orientation.HORIZONTAL:
#         moves = { (pos[0] -1, pos[1]), (pos[0] + 1, pos[1]) }
#     else:
#         moves = { (pos[0], pos[1] - 1), (pos[0], pos[1] + 1) }

#     moves = { move for move in moves if not out_of_bounds(*move, walls.shape) and not walls[move] }
#     return moves


# def find_path_dfs(start_pos: Tuple[int, int], start_dir: Orientation, walls: np.ndarray, target: np.ndarray, max_depth: int = 10):
#     visited = {
#         Orientation.HORIZONTAL: np.zeros((walls.shape), dtype=bool),
#         Orientation.VERTICAL: np.zeros((walls.shape), dtype=bool),
#     }

#     if isinstance(target, tuple):
#         target_pos = target
#         target = np.zeros(walls.shape, dtype=bool)
#         target[target_pos] = True

#     def dfs(pos, ori, path):
#         if target[pos]:
#             return path

#         if len(path) > max_depth:
#             return None

#         visited[ori][pos] = True
#         for move in possible_moves(pos, ori, walls):
#             if visited[ori][move]:
#                 continue

#             result = dfs(move, ori, path + [move])
#             if result:
#                 return result
            
#         if not isinstance(path[-1], tuple): 
#             # if we just changed orientation, we dont do it again
#             return None
        
#         new_ori = Orientation.HORIZONTAL if ori == Orientation.VERTICAL else Orientation.VERTICAL
#         result = dfs(pos, new_ori, path + [new_ori])
#         if result:
#             return result

#         return None
    
#     return dfs(start_pos, start_dir, [start_pos])