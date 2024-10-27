from hackathon_bot import GameState, CapturedZone, HackathonBot
from tomasz.goap.actions.goap_action import GOAPAction
from tomasz.map_parser import TomaszMap
from zone_conqueror import MyBot


class CaptureZoneAction(GOAPAction):
    game_state: GameState
    game_map: TomaszMap

    def __init__(self, game_state: GameState, game_map: TomaszMap):
        self.game_state = game_state
        self.game_map = game_map
        super().__init__(cost=1, preconditions={}, effects={"zone_captured": True})

    # def _get_available_zones(self):
    #     available_zones = []
    #     for zone in self.game_state.map.zones:
    #         if isinstance(zone, CapturedZone):
    #             if zone.player_id == self.game_state.my_agent.id:
    #                 continue
    #         available_zones.append(zone)
    #     return available_zones

    def _get_closest_available_zone(self):
        closest_zone = None
        closest_distance = float('inf')
        for zone in self.game_state.map.zones:
            distance = abs(zone.x - self.game_map.agent.position[0]) + abs(zone.y - self.game_map.agent.position[1])
            if distance < closest_distance:
                if isinstance(zone, CapturedZone):
                    if zone.player_id == self.game_state.my_agent.id:
                        continue
                closest_distance = distance
                closest_zone = zone

        return closest_zone

    def is_valid(self, state):
        return self._get_closest_available_zone() is not None

    def perform(self, actor: MyBot):
        closest_zone = self._get_closest_available_zone()
        actor.movement.target = (closest_zone.x, closest_zone.y)

        return True
