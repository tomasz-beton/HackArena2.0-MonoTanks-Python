from hackathon_bot import *
from tomasz.goap.goals.capture_zones import CaptureZonesGoal
from tomasz.goap.goap_agent import GOAPAgent
from tomasz.map import TomaszMap, TomaszAgent, TomaszMapWithHistory
from tomasz.movement import MovementSystem

import logging
log = logging.getLogger(__name__)
log.disabled = False
logging.basicConfig(level=logging.INFO)


def get_closest_available_zone(game_state: GameState, tomasz_agent: TomaszAgent):
    closest_zone = None
    closest_distance = float('inf')
    for zone in game_state.map.zones:
        distance = abs(zone.x - tomasz_agent.position[0]) + abs(zone.y - tomasz_agent.position[1])
        if distance < closest_distance:
            if isinstance(zone, CapturedZone):
                if zone.player_id == game_state.my_agent.id:
                    continue
            closest_distance = distance
            closest_zone = zone
    return closest_zone


def get_current_zone(game_state: GameState, tomasz_agent: TomaszAgent):
    for zone in game_state.map.zones:
        if zone.x == tomasz_agent.position[0] and zone.y == tomasz_agent.position[1]:
            return zone
    return None


def get_goals(game_state: GameState):
    return [CaptureZonesGoal(game_state)]


class MyBot(HackathonBot):
    movement: MovementSystem | None
    is_capturing: bool = False
    target_zone: Zone | None = None
    wait: int = 0
    map: TomaszMapWithHistory = None
    agent: GOAPAgent

    def __init__(self):
        self.movement = None
        self.agent = GOAPAgent(self, [])
        super().__init__()

    def on_lobby_data_received(self, lobby_data: LobbyData) -> None:
        pass

    def next_move(self, game_state: GameState) -> ResponseAction:
        if self.map is None:
            self.map = TomaszMapWithHistory(game_state)
        else:
            self.map.update(TomaszMap(game_state))

        game_map = TomaszMap(game_state)
        self.agent.update_goals(get_goals(game_state))
        if not self.movement:
            self.movement = MovementSystem(game_map)

        self.agent.process(game_state, game_map)

        action = self.movement.get_action(game_map.agent)
        return action or Pass()

    def on_game_ended(self, game_result: GameResult) -> None:
        pass

    def on_warning_received(self, warning: WarningType, message: str | None) -> None:
        pass


if __name__ == "__main__":
    bot = MyBot()
    bot.run()
