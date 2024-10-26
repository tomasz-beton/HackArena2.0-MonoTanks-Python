from hackathon_bot import GameState, CapturedZone
from tomasz.goap.goals.goap_goal import GOAPGoal


class CaptureZonesGoal(GOAPGoal):
    game_state: GameState = None

    def __init__(self, game_state: GameState, priority: int = 1):
        self.game_state = game_state
        super().__init__(self.is_valid, priority, self.get_desired_state)

    def is_valid(self):
        all_captured = True
        for zone in self.game_state.map.zones:
            if isinstance(zone, CapturedZone) and zone.player_id != self.game_state.my_agent.id:
                all_captured = False
                break

        return not all_captured

    def get_desired_state(self):
        return {"zones_captured": True}