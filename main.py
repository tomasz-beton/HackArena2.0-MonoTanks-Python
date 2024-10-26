from hackathon_bot import *
from tomasz.goap.goals.capture_zones import CaptureZonesGoal
from tomasz.goap.goap_agent import GOAPAgent
from tomasz.map_parser import TomaszMap, TomaszAgent
from tomasz.movement import MovementSystem

def get_goals(game_state: GameState):
    return [CaptureZonesGoal(game_state)]


class MyBot(HackathonBot):
    movement: MovementSystem | None
    agent: GOAPAgent

    def __init__(self):
        self.movement = None
        self.agent = GOAPAgent(self, [])
        super().__init__()

    def on_lobby_data_received(self, lobby_data: LobbyData) -> None:
        pass

    def next_move(self, game_state: GameState) -> ResponseAction:
        game_map = TomaszMap(game_state.map)
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
