"""This is an example of a bot participating in the HackArena 2.0.

This bot will randomly move around the map,
use abilities and print the map to the console.
"""

import os
import random

from hackathon_bot import *
from tomasz. map_parser import TomaszMap


class ExampleBot(HackathonBot):

    def on_lobby_data_received(self, lobby_data: LobbyData) -> None:
        print(f"Lobby data received: {lobby_data}")

    def next_move(self, game_state: GameState) -> ResponseAction:
        self._print_map(game_state.map)

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

    def _print_map(self, game_map: Map):
        #os.system("cls" if os.name == "nt" else "clear")
        map = TomaszMap(game_map)
        # print(map)
        map.pretty_print()



if __name__ == "__main__":
    bot = ExampleBot()
    bot.run()
