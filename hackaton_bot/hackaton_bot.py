"""The main module for the hackaton bot.

This module contains the main class for the hackaton bot.

Classes
-------
HackatonBot
    Represents the hackaton bot.

Examples
--------
To run the hackaton bot, create a new class that inherits
from the `HackatonBot` class and implement the required methods.
Then, create an instance of the bot and run it using the `run` method
in an `asyncio` event loop.

.. code-block:: python

    import asyncio

    from hackaton_bot import HackatonBot, GameState, GameResult, LobbyData, ResponseAction

    class MyBot(HackatonBot):

        async def on_lobby_data_received(self, lobby_data: LobbyData) -> None:
            # Implement the lobby data received logic here

        async def next_move(self, game_state: GameState) -> ResponseAction:
            # Implement the next move logic here
            # Return a response action

        async def on_game_ended(self, game_result: GameResult) -> None:
            # Implement the game ended logic here

    if __name__ == "__main__":
        bot = MyBot()
        asyncio.run(bot.run())
"""

import asyncio
import json
import traceback
from abc import ABC, abstractmethod
from dataclasses import asdict
from typing import final

import humps
import websockets
from websockets import WebSocketClientProtocol as WebSocket

from . import argparser
from .actions import ResponseAction
from .enums import PacketType
from .models import GameStateModel, GameResultModel, LobbyDataModel
from .payloads import (
    ConnectionRejectedPayload,
    GameEndPayload,
    GameStatePayload,
    LobbyDataPayload,
    Payload,
)
from .protocols import GameState, GameResult, LobbyData


class HackatonBot(ABC):
    """Represents the hackaton bot.

    This class is used to create a new hackaton bot.

    Examples
    --------
    To run the hackaton bot, create a new class that inherits
    from the `HackatonBot` class and implement the required methods.
    Then, create an instance of the bot and run it using the `run` method
    in an `asyncio` event loop.

    .. code-block:: python

        import asyncio

        from hackaton_bot import HackatonBot, GameState, GameResult, LobbyData, ResponseAction

        class MyBot(HackatonBot):

            async def on_lobby_data_received(self, lobby_data: LobbyData) -> None:
                # Implement the lobby data received logic here

            async def next_move(self, game_state: GameState) -> ResponseAction:
                # Implement the next move logic here
                # Return a response action (example below)

            async def on_game_ended(self, game_result: GameResult) -> None:
                # Implement the game ended logic here

        if __name__ == "__main__":
            bot = MyBot()
            asyncio.run(bot.run())

    The `next_move` method should return a response action.
    The response action can be a `Movement`, `Rotation`, or `Shoot` action.

    .. code-block:: python

        from hackaton_bot import (
            Movement,
            MovementDirection,
            Rotation,
            RotationDirection,
            Shoot,
        )

        async def next_move(self, game_state: GameState) -> ResponseAction:
            return Movement(MovementDirection.FORWARD)
            # or
            return Rotation(RotationDirection.LEFT, None)
            # or
            return Shoot()
    """

    _lobby_data: LobbyDataModel
    _is_processing: bool = False

    def _get_server_url(self, args: argparser.Arguments) -> str:
        url = f"ws://{args.host}:{args.port}/?nickname={args.nickname}&playerType=hackatonBot"

        if args.code:
            url += f"&joinCode={args.code}"

        return url

    @abstractmethod
    async def on_lobby_data_received(self, lobby_data: LobbyData) -> None:
        """Called when the lobby data is received.

        Parameters
        ----------
        lobby_data: :class:`LobbyData`
            The lobby data received from the server.
        """

    @abstractmethod
    async def next_move(self, game_state: GameState) -> ResponseAction:
        """Called when the bot should make the next move.

        Parameters
        ----------
        game_state: :class:`GameState`
            The current game state.

        Returns
        -------
        ResponseAction
            The response action for the next move.

        Examples
        --------
        The response action can be a `Movement`, `Rotation`, or `Shoot` action.

        .. code-block:: python

            from hackaton_bot import HackatonBot, GameState, GameResult, LobbyData, ResponseAction

            class MyBot(HackatonBot):

                # Other methods

                async def next_move(self, game_state: GameState) -> ResponseAction:
                    return Movement(MovementDirection.FORWARD)
                    # or
                    return Rotation(RotationDirection.LEFT, None)
                    # or
                    return Shoot()
        """

    @abstractmethod
    async def on_game_ended(self, game_result: GameResult) -> None:
        """Called when the game has ended.

        Parameters
        ----------
        game_result: :class:`GameResult
            The game result with the scores of the players.
        """

    @final
    async def _send_packet(
        self,
        websocket,
        packet_type: PacketType,
        payload: Payload | None = None,
    ):
        packet = {"type": packet_type.value}

        if payload:
            packet["payload"] = humps.camelize(asdict(payload))

        await websocket.send(json.dumps(packet))

    @final
    async def _handle_ping_packet(self, websocket: WebSocket) -> None:
        await self._send_packet(websocket, PacketType.PONG)

    @final
    async def _handle_next_move(
        self, websocket: WebSocket, game_state: GameStateModel
    ) -> None:
        if self._is_processing:
            print("Skipping next game state due to ongoing processing!")
            return None

        self._is_processing = True

        try:
            response_action = await self.next_move(game_state)
        except KeyboardInterrupt as e:
            raise e
        except Exception as e:  # pylint: disable=broad-except
            print(f"An error occurred during next move: {e}")
            print(traceback.format_exc())
            return
        finally:
            self._is_processing = False

        if response_action:
            payload = response_action.to_payload(game_state.id)
            await self._send_packet(websocket, response_action.packet_type, payload)

    @final
    async def _handle_messages(  # pylint: disable=too-many-return-statements
        self, websocket: WebSocket, message: websockets.Data
    ) -> None:
        data = humps.decamelize(json.loads(message))

        packet_type = PacketType(data["type"])

        if packet_type == PacketType.PING:
            asyncio.create_task(self._handle_ping_packet(websocket))
            return

        if packet_type == PacketType.GAME_STATE:
            payload = GameStatePayload.from_json(data["payload"])
            player_id = self._lobby_data.player_id
            game_state = GameStateModel.from_payload(payload, player_id)
            asyncio.create_task(self._handle_next_move(websocket, game_state))
            return

        if packet_type == PacketType.LOBBY_DATA:
            payload = LobbyDataPayload.from_json(data["payload"])
            lobby_data = LobbyDataModel.from_payload(payload)
            self._lobby_data = lobby_data
            asyncio.create_task(self.on_lobby_data_received(lobby_data))
            return

        if packet_type == PacketType.CONNECTION_ACCEPTED:
            print("Connected to the server")
            return

        if packet_type == PacketType.CONNECTION_REJECTED:
            payload = ConnectionRejectedPayload.from_json(data["payload"])
            print(f"Connection rejected: {payload.reason}")
            return

        if packet_type == PacketType.GAME_START:
            print("Game started")
            return

        if packet_type == PacketType.GAME_END:
            payload = GameEndPayload.from_json(data["payload"])
            game_result = GameResultModel.from_payload(payload)
            asyncio.create_task(self.on_game_ended(game_result))
            return

    @final
    async def run(self) -> None:
        """Connects to the server and runs the hackaton bot.

        This method must be called using the `asyncio.run` function.

        Examples
        --------

        .. code-block:: python

            import asyncio
            from hackaton_bot import HackatonBot

            class MyBot(HackatonBot):
                # Your bot implementation here

            if __name__ == "__main__":
                bot = MyBot()
                asyncio.run(bot.run())
        """

        args = argparser.get_args()

        async with websockets.connect(self._get_server_url(args)) as websocket:
            while True:
                try:
                    message = await websocket.recv()
                    await self._handle_messages(websocket, message)
                except Exception as e:  # pylint: disable=broad-except
                    print(f"An error occurred: {e}")  # pragma: no cover
                    print(traceback.format_exc())  # pragma: no cover