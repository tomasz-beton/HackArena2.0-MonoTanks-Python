from typing import List

from hackathon_bot import *
from tomasz.goap.goals.capture_zones import CaptureZonesGoal
from tomasz.goap.goap_agent import GOAPAgent
from tomasz.map import TomaszMap, TomaszAgent, TomaszMapWithHistory
from tomasz.modes.mode import Mode
from tomasz.modes.zone_capture_mode import ZoneCaptureMode
from tomasz.movement import MovementSystem

import logging
log = logging.getLogger(__name__)
log.disabled = False
logging.basicConfig(level=logging.INFO)



class MyBot(HackathonBot):
    movement: MovementSystem | None
    map: TomaszMapWithHistory = None
    modes: List[Mode]
    died: bool = False

    def __init__(self):
        self.movement = None
        self.agent = GOAPAgent(self, [])
        self.modes = [
            ZoneCaptureMode(),
        ]
        super().__init__()

    def on_lobby_data_received(self, lobby_data: LobbyData) -> None:
        pass

    def next_move(self, game_state: GameState) -> ResponseAction:
        if game_state.my_agent.is_dead:
            self.died = True
            return Pass()

        if self.map is None:
            self.map = TomaszMapWithHistory(game_state)
        else:
            self.map.update(TomaszMap(game_state))

        if not self.movement:
            self.movement = MovementSystem(self.map)

        if self.died and not game_state.my_agent.is_dead:
            log.info("Respawned")
            self.movement.update_map(self.map)
            self.died = False

        current_mode = self._get_best_mode()
        action = current_mode.get_action(self.map, self)

        log.info(f"Current mode: {current_mode}")
        log.info(f"Action: {action}")

        return action or Pass()

    def on_game_ended(self, game_result: GameResult) -> None:
        pass

    def on_warning_received(self, warning: WarningType, message: str | None) -> None:
        pass

    def _get_best_mode(self):
        best_mode = self.modes[0]
        best_priority = 0
        log.info(f"modes: {str(self.modes)}")
        for mode in self.modes:
            priority = mode.get_priority(self.map, self)
            if priority > best_priority:
                best_mode = mode
                best_priority = priority
        return best_mode


if __name__ == "__main__":
    bot = MyBot()
    bot.run()
