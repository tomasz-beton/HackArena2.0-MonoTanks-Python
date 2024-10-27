"""This is an example of a bot participating in the HackArena 2.0.

This bot will randomly move around the map,
use abilities and print the map to the console.
"""

import os
import random

from hackathon_bot import *
from tomasz.map import TomaszMap, TomaszMapWithHistory
import time


class ExampleBot(HackathonBot):
    map = None

    def on_lobby_data_received(self, lobby_data: LobbyData) -> None:
        print(f"Lobby data received: {lobby_data}")

    def next_move(self, game_state: GameState) -> ResponseAction:
        t1 = time.perf_counter()
        if self.map is None:
            self.map = TomaszMapWithHistory(game_state)
        else:
            new_map = TomaszMap(game_state)
            self.map.update(new_map)
        t2 = time.perf_counter()
        print(f"Time to update map: {1e3*(t2 - t1):.2f} ms")

        print(self.map)
        self.map.pretty_print()

        # Check if the agent is dead
        if game_state.my_agent.is_dead:
            # Return pass to avoid warnings from the server
            # when the bot tries to make an action with a dead tank
            return Pass()

        return self._get_random_action()

    def on_game_ended(self, game_result: GameResult) -> None:
        print(f"Game ended: {game_result}")

    def on_warning_received(self, warning: WarningType, message: str | None) -> None:
        print(f"Warning received: {warning} - {message}")

    def _get_random_action(self):
        return random.choice(
            [
                Movement(MovementDirection.FORWARD),
                Movement(MovementDirection.BACKWARD),
                Rotation(RotationDirection.LEFT, RotationDirection.LEFT),
                Rotation(RotationDirection.LEFT, RotationDirection.RIGHT),
                Rotation(RotationDirection.LEFT, None),
                Rotation(RotationDirection.RIGHT, RotationDirection.LEFT),
                Rotation(RotationDirection.RIGHT, RotationDirection.RIGHT),
                Rotation(RotationDirection.RIGHT, None),
                Rotation(None, RotationDirection.LEFT),
                Rotation(None, RotationDirection.RIGHT),
                Rotation(None, None),  # Useless, better use Pass()
                AbilityUse(Ability.FIRE_BULLET),
                AbilityUse(Ability.FIRE_DOUBLE_BULLET),
                AbilityUse(Ability.USE_LASER),
                AbilityUse(Ability.USE_RADAR),
                AbilityUse(Ability.DROP_MINE),
                Pass(),
            ]
        )

if __name__ == "__main__":
    bot = ExampleBot()
    bot.run()
