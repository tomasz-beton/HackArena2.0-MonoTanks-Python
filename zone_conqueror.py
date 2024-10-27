import random

from hackathon_bot import *
from tomasz.map import TomaszMap, TomaszAgent
from tomasz.movement import MovementSystem


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


class MyBot(HackathonBot):
    movement: MovementSystem | None
    is_capturing: bool = False
    target_zone: Zone | None = None
    wait: int = 0

    def __init__(self):
        self.movement = None
        super().__init__()

    def on_lobby_data_received(self, lobby_data: LobbyData) -> None:
        pass

    def next_move(self, game_state: GameState) -> ResponseAction:
        game_map = TomaszMap(game_state.map)
        if not self.movement:
            self.movement = MovementSystem(game_map)

        if self.wait > 0:
            self.wait -= 1
            return Pass()

        if not self.movement.target and not self.is_capturing:
            self.target_zone = get_closest_available_zone(game_state, game_map.agent)
            if self.target_zone:
                self.movement.target = (self.target_zone.x, self.target_zone.y)


        current_zone = get_current_zone(game_state, game_map.agent)
        if current_zone and current_zone.status == ZoneStatus.BEING_CAPTURED:
            self.is_capturing = True

        if self.is_capturing and current_zone and current_zone.status == ZoneStatus.CAPTURED:
            self.is_capturing = False
            self.target_zone = None
            self.movement.target = None

        action = self.movement.get_action(game_map.agent)
        return action or Pass()

    def on_game_ended(self, game_result: GameResult) -> None:
        pass

    def on_warning_received(self, warning: WarningType, message: str | None) -> None:
        pass


if __name__ == "__main__":
    bot = MyBot()
    bot.run()
