import random
from typing import Tuple

from tomasz.modes.mode import Mode


class WanderMode(Mode):

    def get_priority(self, tomasz_map, my_bot):
        return 0.1

    def get_action(self, tomasz_map, my_bot):
        if not my_bot.movement.target:
            my_bot.movement.target = (tomasz_map.agent.position[0] + random.randint(-5, 5), tomasz_map.agent.position[1] + random.randint(-5, 5))

        return my_bot.movement.get_action(tomasz_map.agent)