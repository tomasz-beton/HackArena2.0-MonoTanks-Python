import random
from typing import Tuple

from tomasz.a_star import is_walkable
from tomasz.modes.mode import Mode


def get_walkable_tiles(tomasz_map, tomasz_agent, radius):
    walkable_tiles = []
    for x in range(tomasz_agent.position[0] - radius, tomasz_agent.position[0] + radius + 1):
        for y in range(tomasz_agent.position[1] - radius, tomasz_agent.position[1] + radius + 1):
            if is_walkable(tomasz_map, (x, y), 0):
                walkable_tiles.append((x, y))
    return walkable_tiles

class WanderMode(Mode):

    def get_priority(self, tomasz_map, my_bot):
        return 0.1

    def get_action(self, tomasz_map, my_bot):
        if not my_bot.movement.target or my_bot.movement.path_finding_failed:
            my_bot.movement.target = random.choice(get_walkable_tiles(tomasz_map, tomasz_map.agent, 5))

        return my_bot.movement.get_action(tomasz_map.agent)