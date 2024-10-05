from random import Random

from hackathon_bot import (
    HackathonBot,
    LobbyData,
    GameState,
    GameResult,
    ResponseAction,
    WarningType,
)
from hackathon_bot.actions import Movement, Rotation, Shoot
from hackathon_bot.enums import MovementDirection, RotationDirection


class MyBot(HackathonBot):

    random: Random

    def on_lobby_data_received(self, lobby_data: LobbyData) -> None:
        self.random = Random(lobby_data.server_settings.seed)

    def next_move(self, game_state: GameState) -> ResponseAction:

        pckg = self.random.randint(0, 2)

        if pckg == 0:
            p1 = self.random.randint(0, 1)
            if p1 == 0:
                return Movement(MovementDirection.FORWARD)
            else:
                return Movement(MovementDirection.BACKWARD)
        elif pckg == 1:
            p2 = self.random.randint(0, 2)
            p3 = self.random.randint(0, 2)
            if p2 == 0:
                pp2 = RotationDirection.LEFT
            elif p2 == 1:
                pp2 = RotationDirection.RIGHT
            else:
                pp2 = None
            if p3 == 0:
                pp3 = RotationDirection.LEFT
            elif p3 == 1:
                pp3 = RotationDirection.RIGHT
            else:
                pp3 = None
            return Rotation(pp2, pp3)
        else:
            return Shoot()

    def on_game_ended(self, game_result: GameResult) -> None:
        print(game_result)

    def on_warning_received(self, warning: WarningType, message: str | None) -> None:
        print(warning, message)


if __name__ == "__main__":
    bot = MyBot()
    bot.run()
