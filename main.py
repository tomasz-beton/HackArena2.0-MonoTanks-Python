from hackathon_bot import (
    HackathonBot,
    LobbyData,
    GameState,
    GameResult,
    ResponseAction,
    WarningType,
)


class MyBot(HackathonBot):

    def on_lobby_data_received(self, lobby_data: LobbyData) -> None:
        pass

    def next_move(self, game_state: GameState) -> ResponseAction:
        pass

    def on_game_ended(self, game_result: GameResult) -> None:
        pass

    def on_warning_received(self, warning: WarningType, message: str | None) -> None:
        pass


if __name__ == "__main__":
    bot = MyBot()
    bot.run()
