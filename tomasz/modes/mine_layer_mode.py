import logging

from hackathon_bot import SecondaryItemType, AbilityUse, Ability
from tomasz.a_star import get_movements_4n, is_walkable
from tomasz.modes.mode import Mode

log = logging.getLogger(__name__)
log.disabled = True


def can_mine_be_placed_safely(tomasz_map):
    movements = get_movements_4n()
    non_walkable = 0
    if (tomasz_map.agent.position[0] == 0 or tomasz_map.agent.position[1] == 0 or tomasz_map.agent.position[
        0] == tomasz_map.size[0] - 1 or tomasz_map.agent.position[
        1] == tomasz_map.size[1] - 1):
        return False

    for movement in movements:
        x = tomasz_map.agent.position[0] + movement[0]
        y = tomasz_map.agent.position[1] + movement[1]
        if not is_walkable(tomasz_map, (x, y)):
            non_walkable += 1

    log.info(f"non_walkable: {non_walkable}")
    return non_walkable < 3


class MineLayerMode(Mode):
    def get_priority(self, tomasz_map, my_bot):
        has_mine = tomasz_map.agent.entity.secondary_item == SecondaryItemType.MINE
        can_place = can_mine_be_placed_safely(tomasz_map)
        if not has_mine:
            log.info("MineLayerMode: I don't have a mine")
        return 0.2 if has_mine and can_place else 0

    def get_action(self, tomasz_map, my_bot):
        return AbilityUse(Ability.DROP_MINE)
