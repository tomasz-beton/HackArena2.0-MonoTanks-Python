import random
from typing import Tuple
from hackathon_bot import CapturedZone, Pass, NeutralZone, BeingCapturedZone, BeingRetakenZone
from tomasz.modes.mode import Mode
from tomasz.utils import distance_l1

import logging
log = logging.getLogger(__name__)
log.disabled = False

def are_all_zones_captured(tomasz_map):
    all_captured = True
    for zone in tomasz_map.game_state.map.zones:
        if isinstance(zone, CapturedZone) and zone.player_id != tomasz_map.game_state.my_agent.id:
            all_captured = False
            break
        if isinstance(zone, NeutralZone):
            all_captured = False
            break
        if isinstance(zone, BeingCapturedZone):
            all_captured = False
            break
        if isinstance(zone, BeingRetakenZone):
            all_captured = False
            break

    return all_captured

def get_closest_zone(tomasz_map):
    closest_zone = None
    closest_distance = float('inf')
    if tomasz_map.agent:
        for zone in tomasz_map.game_state.map.zones:
            distance = abs(zone.x - tomasz_map.agent.position[0]) + abs(zone.y - tomasz_map.agent.position[1])
            if distance < closest_distance:
                if isinstance(zone, CapturedZone):
                    if zone.player_id == tomasz_map.game_state.my_agent.id:
                        continue
                closest_distance = distance
                closest_zone = zone
    return closest_zone


def get_closest_tile_at_zone(tomasz_map, zone)->Tuple[int, int]:
    zone_pos = tomasz_map.zones[chr(zone.index)].pos
    my_pos = tomasz_map.agent.position
    closest_zone_pos = min(zone_pos, key=lambda x: distance_l1(x, my_pos))
    return zone_pos, closest_zone_pos


class ZoneCaptureMode(Mode):

    def get_priority(self, tomasz_map, my_bot):
        return (1-are_all_zones_captured(tomasz_map)) * 0.65

    def get_action(self, tomasz_map, my_bot):
        closest_zone = get_closest_zone(tomasz_map)
        # log.warning(f"closest_zone x y: {closest_zone.x, closest_zone.y}")
        zone_pos, closest_zone_pos = get_closest_tile_at_zone(tomasz_map, closest_zone)
        # log.warning(f"closes_zone_pos: {closest_zone_pos}")
        log.warning(f"zone_pos: {zone_pos}")
        # log.warning(f"my_pos: {tomasz_map.agent.position}, target: {my_bot.movement.target}")

        # if closest_zone and my_bot.movement:
        #     my_bot.movement.target = closest_zone_pos
        # else:
        #     my_bot.movement.target = None

        if tomasz_map.agent.position in zone_pos:
            my_bot.movement.target = random.choice(zone_pos)
            log.warning(f"In the zone already, walk target: {my_bot.movement.target}")

        else:
            log.warning(f"Not in the zone yet, target is : {my_bot.movement.target}")
            my_bot.movement.target = closest_zone_pos
        return my_bot.movement.get_action(tomasz_map.agent)
