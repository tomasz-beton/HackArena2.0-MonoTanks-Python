import logging

from hackathon_bot import ItemType, Pass
from tomasz.map import TomaszMapWithHistory, TomaszAgent
from tomasz.modes.mode import Mode

log = logging.getLogger(__name__)
log.disabled = False

"""
This mode is responsible for picking up items. We want the priority to scale with item type and distance to the item.
"""

ITEM_PRIORITIES = {
    ItemType.LASER: 0.4,
    ItemType.DOUBLE_BULLET: 0.6,
    ItemType.RADAR: 0.7,
    ItemType.MINE: 0.3
}


def get_item_priority(item_type: ItemType):
    return ITEM_PRIORITIES.get(item_type, 0)


def get_item_distance(item, agent: TomaszAgent):
    return abs(item['pos'][0] - agent.position[0]) + abs(item['pos'][1] - agent.position[1])


def get_closest_item(tomasz_map: TomaszMapWithHistory):
    closest_item = None
    closest_distance = float('inf')
    if tomasz_map.agent:
        for item in tomasz_map.items:
            distance = get_item_distance(item, tomasz_map.agent)
            if distance < closest_distance:
                closest_distance = distance
                closest_item = item
    return closest_item


def get_item_distance_priority(item, agent: TomaszAgent):
    distance = get_item_distance(item, agent)
    if distance <= 1:
        return 1
    elif distance <= 2:
        return 0.8
    elif distance <= 3:
        return 0.7
    elif distance <= 4:
        return 0.5
    else:
        return 0.3

def get_item_age_priority(item):
    return max(0, 1 - item["ticks_since_seen"] / 100)




class PickUpItemMode(Mode):
    best_item = None
    # forget items that we failed to reach
    # {
    #   (x,y): game_tick
    # }
    forget_items = {}

    def get_best_item(self, tomasz_map: TomaszMapWithHistory):
        best_item = None
        best_priority = 0
        for item in tomasz_map.items:
            item_priority = get_item_priority(item["item_type"])
            distance_priority = get_item_distance_priority(item, tomasz_map.agent)
            age_priority = get_item_age_priority(item)
            priority = item_priority * distance_priority * age_priority

            if item["pos"] in self.forget_items:
                if tomasz_map.game_state.tick - self.forget_items[item["pos"]] > 100:
                    del self.forget_items[item["pos"]]
                else:
                    continue

            if priority > best_priority:
                best_priority = priority
                best_item = item
        return best_item

    def get_priority(self, tomasz_map, my_bot):
        if tomasz_map.agent.entity.secondary_item:
            log.info("Already have item")
            return 0

        self.best_item = self.get_best_item(tomasz_map)
        if self.best_item:
            log.info(f"Found best item: {self.best_item}")
            if my_bot.movement.path_finding_failed:
                log.warning("Path finding failed clearing best_item")
                # forget this item for a while
                self.forget_items[self.best_item["pos"]] = tomasz_map.game_state.tick
                self.best_item = None
                return 0
            return get_item_distance_priority(self.best_item, tomasz_map.agent)
        else:
            log.info("No items found")
        return 0

    def get_action(self, tomasz_map, my_bot):
        if self.best_item and my_bot.movement:
            log.info(f"Moving to item: {self.best_item['type']}, at: {self.best_item['pos'][1]}, {self.best_item['pos'][0]}")
            my_bot.movement.target = self.best_item['pos']

            return my_bot.movement.get_action(tomasz_map.agent)

        return Pass()
