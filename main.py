import asyncio

from hackaton_bot import (
    HackatonBot,
    LobbyData,
    GameState,
    GameResult,
    ResponseAction,
)


class MyBot(HackatonBot):

    async def on_lobby_data_received(self, lobby_data: LobbyData) -> None:
        pass

    async def next_move(self, game_state: GameState) -> ResponseAction:
        pass

    async def on_game_ended(self, game_result: GameResult) -> None:
        pass


if __name__ == "__main__":
    bot = MyBot()
    asyncio.run(bot.run())
