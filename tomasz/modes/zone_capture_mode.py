from hackathon_bot import CapturedZone, Pass, NeutralZone, BeingCapturedZone, BeingRetakenZone
from tomasz.modes.mode import Mode


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


class ZoneCaptureMode(Mode):

    def get_priority(self, tomasz_map, my_bot):
        return (1-are_all_zones_captured(tomasz_map)) * 0.65

    def get_action(self, tomasz_map, my_bot):
        closest_zone = get_closest_zone(tomasz_map)
        if closest_zone and my_bot.movement:
            my_bot.movement.target = (closest_zone.x, closest_zone.y)
        else:
            my_bot.movement.target = None
        return my_bot.movement.get_action(tomasz_map.agent)
