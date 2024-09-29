"""Tests for the hackathon_bot module."""

from __future__ import annotations

import asyncio
import json
from dataclasses import dataclass
from typing import ClassVar
from unittest.mock import AsyncMock, Mock, patch

import pytest
import websockets

from hackathon_bot import argparser
from hackathon_bot.actions import ResponseAction
from hackathon_bot.enums import PacketType
from hackathon_bot.hackathon_bot import HackathonBot
from hackathon_bot.models import GameResultModel, GameStateModel, LobbyDataModel
from hackathon_bot.payloads import (
    GameEndPayload,
    GameStatePayload,
    LobbyDataPayload,
    Payload,
)
from hackathon_bot.protocols import GameResult, GameState, LobbyData

# pylint: disable=protected-access


@dataclass(slots=True, frozen=True)
class TestPayload(Payload):
    """Represents a test payload."""

    __test__ = False


@dataclass(slots=True, frozen=True)
class TestResponseAction(ResponseAction):
    """Represents a test response action."""

    __test__ = False

    packet_type: ClassVar[PacketType] = PacketType.UNKNOWN

    def to_payload(self, game_state_id: str) -> TestPayload:
        return TestPayload()


class TestBot(HackathonBot):  # pylint: disable=too-many-instance-attributes
    """Represents a test bot."""

    __test__ = False

    async def on_lobby_data_received(self, lobby_data: LobbyData) -> None: ...

    async def next_move(self, game_state: GameState) -> ResponseAction: ...

    async def on_game_ended(self, game_result: GameResult) -> None: ...


class TestWebsocket:
    """Represents a test websocket."""

    async def __aenter__(self) -> TestWebsocket:
        return self

    async def __aexit__(self, exc_type, exc_value, traceback) -> None:
        pass

    def __call__(self, url) -> TestWebsocket:
        return self

    async def recv(self) -> str:
        """Receive a message.

        This method contains a small delay to simulate a real websocket connection.
        """
        await asyncio.sleep(0.05)
        return json.dumps({"type": int(PacketType.UNKNOWN)})


def test_get_server_url() -> None:
    """Test _get_server_url method."""

    args = argparser.Arguments("localhost", 8080, "C0D3", "testBot")

    assert (
        TestBot()._get_server_url(args)
        == "ws://localhost:8080/?nickname=testBot&playerType=hackathonBot&joinCode=C0D3"
    )


@pytest.mark.asyncio
async def test_send_packet() -> None:
    """Test _send_packet method."""

    bot = TestBot()
    websocket = Mock()
    websocket.send = AsyncMock()

    await bot._send_packet(
        websocket,
        PacketType.UNKNOWN,
        TestPayload(),
    )

    websocket.send.assert_called_once()


@pytest.mark.asyncio
async def test_run(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test run method."""

    monkeypatch.setattr(argparser, "get_args", Mock())
    monkeypatch.setattr(websockets, "connect", TestWebsocket())

    bot = TestBot()
    bot._get_server_url = Mock(return_value="ws://localhost:8080")

    # Run the bot for a short period of time
    # because method `run` is an infinite loop
    try:
        await asyncio.wait_for(bot.run(), timeout=0.2)
    except asyncio.TimeoutError:
        pass


@pytest.mark.asyncio
async def test_handle_messages__ping() -> None:
    """Test _handle_messages method with a ping packet."""

    ws = Mock()
    bot = TestBot()
    bot._handle_ping_packet = AsyncMock()

    with patch.object(
        bot, "_handle_ping_packet", new_callable=AsyncMock
    ) as mock_handle_ping:
        await bot._handle_messages(ws, json.dumps({"type": PacketType.PING}))
        mock_handle_ping.assert_called_once_with(ws)


@pytest.mark.asyncio
async def test_handle_messages__game_state(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test _handle_messages method with a game state packet."""

    ws = Mock()
    bot = TestBot()
    bot._lobby_data = Mock()
    bot._handle_next_move = AsyncMock()

    game_state = Mock()

    monkeypatch.setattr(GameStatePayload, "from_json", Mock())
    monkeypatch.setattr(GameStateModel, "from_payload", Mock(return_value=game_state))

    # Check if the _handle_next_move method was called with the game state
    with patch.object(
        bot, "_handle_next_move", new_callable=AsyncMock
    ) as mock_handle_game_state:
        await bot._handle_messages(
            ws, json.dumps({"type": PacketType.GAME_STATE, "payload": {}})
        )
        mock_handle_game_state.assert_called_once_with(ws, game_state)


@pytest.mark.asyncio
async def test_handle_messages__lobby_data(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test _handle_messages method with a lobby data packet."""

    ws = Mock()
    bot = TestBot()
    bot.on_lobby_data_received = AsyncMock()

    lobby_data = Mock()

    monkeypatch.setattr(LobbyDataPayload, "from_json", Mock(return_value=TestPayload()))
    monkeypatch.setattr(LobbyDataModel, "from_payload", Mock(return_value=lobby_data))

    # Check if the on_lobby_data_received method was called with the lobby data
    with patch.object(
        bot, "on_lobby_data_received", new_callable=AsyncMock
    ) as mock_handle_lobby_data:
        await bot._handle_messages(
            ws, json.dumps({"type": PacketType.LOBBY_DATA, "payload": {}})
        )
        mock_handle_lobby_data.assert_called_once_with(lobby_data)

    # Check if the lobby data was set correctly
    assert bot._lobby_data == lobby_data


@pytest.mark.asyncio
async def test_handle_messages__connection_accepted() -> None:
    """Test _handle_messages method with a connection accepted packet."""

    bot = TestBot()
    ws = Mock()

    # Check if the method does not raise an exception
    await bot._handle_messages(ws, json.dumps({"type": PacketType.CONNECTION_ACCEPTED}))


@pytest.mark.asyncio
async def test_handle_messages__connection_rejected() -> None:
    """Test _handle_messages method with a connection rejected packet."""

    bot = TestBot()
    ws = Mock()

    # Check if the reason is printed
    with patch("builtins.print") as mock_print:
        await bot._handle_messages(
            ws,
            json.dumps(
                {"type": PacketType.CONNECTION_REJECTED, "payload": {"reason": "test"}}
            ),
        )

        mock_print.assert_called_once_with("Connection rejected: test")


@pytest.mark.asyncio
async def test_handle_messages__game_start() -> None:
    """Test _handle_messages method with a game start packet."""

    bot = TestBot()
    ws = Mock()

    # Check if the method does not raise an exception
    await bot._handle_messages(ws, json.dumps({"type": PacketType.GAME_START}))


@pytest.mark.asyncio
async def test_handle_messages__game_end(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test _handle_messages method with a game end packet."""
    bot = TestBot()
    ws = Mock()

    game_result = Mock()

    monkeypatch.setattr(GameEndPayload, "from_json", Mock(return_value=TestPayload()))
    monkeypatch.setattr(GameResultModel, "from_payload", Mock(return_value=game_result))

    # Check if the on_game_ended method was called with the game result
    with patch.object(
        bot, "on_game_ended", new_callable=AsyncMock
    ) as mock_handle_game_end:
        await bot._handle_messages(
            ws, json.dumps({"type": PacketType.GAME_END, "payload": {}})
        )
        mock_handle_game_end.assert_called_once_with(game_result)


@pytest.mark.asyncio
async def test_handle_ping_packet() -> None:
    """Test _handle_ping_packet method.

    This method should send a pong packet."""

    bot = TestBot()
    websocket = Mock()
    bot._send_packet = AsyncMock()

    await bot._handle_ping_packet(websocket)

    bot._send_packet.assert_called_once_with(websocket, PacketType.PONG)


@pytest.mark.asyncio
async def test_handle_next_move__is_processing():
    """Test _handle_next_move method when the bot is processing.

    The method should not call the next_move method.
    """

    bot = TestBot()
    bot._is_processing = True
    ws = Mock()

    bot.next_move = AsyncMock()

    await bot._handle_next_move(ws, TestPayload())

    bot.next_move.assert_not_called()


@pytest.mark.asyncio
async def test_handle_next_move__is_not_processing():
    """Test _handle_next_move method when the bot is not processing.

    The method should call the next_move method.
    After receiving the response action, the method
    should set the _is_processing flag to False and send a packet.
    """

    bot = TestBot()
    bot._is_processing = False
    ws = Mock()
    game_state = Mock()

    bot.next_move = AsyncMock(return_value=TestResponseAction())
    bot._send_packet = AsyncMock()

    await bot._handle_next_move(ws, game_state)

    # Check if the next_move method was called and sent a packet
    bot.next_move.assert_called_once_with(game_state)

    # Check if the _is_processing flag was set to False
    assert bot._is_processing is False

    # Check if the packet was sent
    bot._send_packet.assert_called_once()


@pytest.mark.asyncio
async def test_handle_next_move__keyboard_interrupt():
    """Test _handle_next_move method when a KeyboardInterrupt is raised."""

    bot = TestBot()
    bot._is_processing = False
    ws = Mock()

    bot.next_move = AsyncMock(side_effect=KeyboardInterrupt)

    with pytest.raises(KeyboardInterrupt):
        await bot._handle_next_move(ws, Mock())


@pytest.mark.asyncio
async def test_handle_next_move__next_move_failed():
    """Test _handle_next_move method when
    the next_move method raises an exception.

    The method should print the error and
    set the _is_processing flag to False.
    """

    bot = TestBot()
    bot._is_processing = False
    ws = Mock()

    bot.next_move = AsyncMock(side_effect=Exception)

    # Check if the error is printed
    with patch("builtins.print") as mock_print:
        await bot._handle_next_move(ws, TestPayload())
        mock_print.assert_called()

    # Check if the next_move method was called
    bot.next_move.assert_called_once()

    # Check if the _is_processing flag was set to False
    assert bot._is_processing is False
