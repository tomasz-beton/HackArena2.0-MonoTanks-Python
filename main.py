from typing import List

from hackathon_bot import *
from tomasz.alignment import AlignmentSystem
from tomasz.goap.goals.capture_zones import CaptureZonesGoal
from tomasz.goap.goap_agent import GOAPAgent
from tomasz.map import TomaszMap, TomaszAgent, TomaszMapWithHistory
from tomasz.modes.fight_mode import FightMode
from tomasz.modes.mine_layer_mode import MineLayerMode
from tomasz.modes.mode import Mode
from tomasz.modes.pickup_item_mode import PickUpItemMode
from tomasz.modes.rotate_mode import RotateMode
from tomasz.modes.wander_mode import WanderMode
from tomasz.modes.zone_capture_mode import ZoneCaptureMode
from tomasz.movement import MovementSystem

import logging
log = logging.getLogger(__name__)
log.disabled = False
logging.basicConfig(level=logging.INFO)

def use_item(item: SecondaryItemType) -> ResponseAction | None:
    if item == SecondaryItemType.DOUBLE_BULLET:
        return AbilityUse(Ability.FIRE_DOUBLE_BULLET)
    elif item == SecondaryItemType.LASER:
        return AbilityUse(Ability.USE_LASER)
    elif item == SecondaryItemType.RADAR:
        return AbilityUse(Ability.USE_RADAR)
    return None

class MyBot(HackathonBot):
    movement: MovementSystem | None
    alignment: AlignmentSystem | None
    map: TomaszMapWithHistory = None
    modes: List[Mode]
    died: bool = False

    def __init__(self):
        self.movement = None
        self.alignment = None
        self.agent = GOAPAgent(self, [])
        self.modes = [
            FightMode(),
            ZoneCaptureMode(),
            PickUpItemMode(),
            MineLayerMode(),
            RotateMode(),
            WanderMode(),
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

        if not self.alignment:
            self.alignment = AlignmentSystem(self.map, self.movement)

        if self.map.last_danger_map_change == 0:
            #log.warning("Danger map updated")
            self.movement.update_map(self.map)

        if self.died and not game_state.my_agent.is_dead:
            log.info("Respawned")
            self.movement.update_map(self.map)
            self.died = False

        current_mode = self._get_best_mode()
        action = current_mode.get_action(self.map, self)

        log.info(f"Current mode: {current_mode}")
        log.info(f"Action: {action}")

        if self.map.agent.entity.secondary_item:
            log.info("Dumping item")
            use_action = use_item(self.map.agent.entity.secondary_item)
            if use_action:
                return use_action

        return action or Pass()

    def on_game_ended(self, game_result: GameResult) -> None:
        pass

    def on_warning_received(self, warning: WarningType, message: str | None) -> None:
        pass

    def _get_best_mode(self):
        best_mode = self.modes[0]
        best_priority = 0
        #log.info(f"Picking best mode from: {str(self.modes)}")
        priorities = []
        for mode in self.modes:
            priority = mode.get_priority(self.map, self)
            priorities.append((mode, priority))
            if priority > best_priority:
                best_mode = mode
                best_priority = priority
        log.info(f"Priorities: {priorities}")
        log.info(f"Best mode: {best_mode}")
        return best_mode


if __name__ == "__main__":
    bot = MyBot()
    bot.run()
