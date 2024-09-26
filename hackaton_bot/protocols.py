"""A module that contains the protocols used in the library.

Protocols
---------
ServerSettings
    Represents the server settings.
GameStatePlayer
    Represents a player in the game state.
LobbyPlayer
    Represents a player in the lobby.
GameEndPlayer
    Represents a player in the game result.
Agent
    Represents the hackaton bot in the game state.
PlayerTurret
    Represents a turret of a player's tank.
AgentTurret
    Represents a turret of the hackaton bot's tank.
PlayerTank
    Represents a tank of a player.
AgentTank
    Represents a tank of the hackaton bot.
Wall
    Represents a wall in the game.
Bullet
    Represents a bullet in the game.
LobbyData
    Represents the lobby data.
Zone
    Represents a zone in the game.
NeutralZone
    Represents a neutral zone in the game.
BeingCapturedZone
    Represents a zone being captured in the game.
CapturedZone
    Represents a captured zone in the game.
BeingContestedZone
    Represents a zone being contested in the game.
BeingRetakenZone
    Represents a zone being retaken in the game.
Map
    Represents the map of the game state.
GameState
    Represents the game state.
GameResult
    Represents the game result.

Notes
-----
This module provides protocols for type hints.

Protocols are used to provide type hints for the classes
in the game state, lobby data, and game result.
"""

from __future__ import annotations

from typing import Protocol, Sequence, TypeVar, TYPE_CHECKING

if TYPE_CHECKING:
    from hackaton_bot.enums import Direction, ZoneStatus

    TileT = TypeVar("TileT", "Wall", "Bullet", "PlayerTank", "AgentTank", None)


class ServerSettings(Protocol):
    """Represents the server settings.

    Attributes
    ----------
    grid_dimension: :class:`int`
        The grid dimension.
    number_of_players: :class:`int`
        The number of players.
    seed: :class:`int`
        The seed of the game.
    ticks: :class:`int`
        The number of game ticks.
    broadcast_interval: :class:`int`
        The broadcast interval in miliseconds.
    eager_broadcast: :class:`bool`
        Whether to eager broadcast is enabled.
    """

    @property
    def grid_dimension(self) -> int:
        """The grid dimension."""

    @property
    def number_of_players(self) -> int:
        """The number of players."""

    @property
    def seed(self) -> int:
        """The seed of the game."""

    @property
    def ticks(self) -> int:
        """The number of game ticks.

        For example, if the number of ticks is 2000,
        and the broadcast interval is 50 milliseconds,
        the game will last for 100 seconds (2000 / (1000 / 50))
        """

    @property
    def broadcast_interval(self) -> int:
        """The broadcast interval.

        The interval in milliseconds between
        each broadcast game state.
        """

    @property
    def eager_broadcast(self) -> bool:
        """Whether eager broadcast is enabled.

        If `True`, the server will broadcast the game state
        immediately after all agents respond to the latest game state.

        If `False`, the server will broadcast the game state
        after the broadcast interval.

        This allows for a shorter waiting time for the next broadcast
        if all agents respond to the latest game state.

        As a **participant of Hackaton**, you can **ignore this**.
        """


class GameStatePlayer(Protocol):
    """Represents a player in the game.

    Attributes
    ----------
    id: :class:`str`
        The unique identifier of the player.
    nickname: :class:`str`
        The nickname of the player.
    color: :class:`int`
        The color of the player in format `0xAABBGGRR`.
    ping: :class:`int`
        The ping of the player.

    Notes
    -----
    This class is a protocol to provide type hints for
    the player in the game state.
    """

    @property
    def id(self) -> str:
        """The unique identifier of the player."""

    @property
    def nickname(self) -> str:
        """The nickname of the player."""

    @property
    def color(self) -> int:
        """The color of the player in format `0xAABBGGRR`."""

    @property
    def ping(self) -> int:
        """The ping of the player."""


class LobbyPlayer(Protocol):
    """Represents a player in the lobby.

    Attributes
    ----------
    id: :class:`str`
        The unique identifier of the player.
    nickname: :class:`str`
        The nickname of the player.
    color: :class:`int`
        The color of the player in format `0xAABBGGRR`.

    Notes
    -----
    This class is a protocol to provide type hints for
    the player in the lobby.
    """

    @property
    def id(self) -> str:
        """The unique identifier of the player."""

    @property
    def nickname(self) -> str:
        """The nickname of the player."""

    @property
    def color(self) -> int:
        """The color of the player in format `0xAABBGGRR`."""


class GameEndPlayer(Protocol):
    """Represents a player in the game result.

    Attributes
    ----------
    id: :class:`str`
        The unique identifier of the player.
    nickname: :class:`str`
        The nickname of the player.
    color: :class:`int`
        The color of the player in format `0xAABBGGRR`.
    score: :class:`int`
        The score of the player.

    Notes
    -----
    This class is a protocol to provide type hints for
    the player in the game result.
    """

    @property
    def id(self) -> str:
        """The unique identifier of the player."""

    @property
    def nickname(self) -> str:
        """The nickname of the player."""

    @property
    def color(self) -> int:
        """The color of the player in format `0xAABBGGRR`."""

    @property
    def score(self) -> int:
        """The score of the player."""


class Agent(GameStatePlayer, Protocol):
    """Represents your agent (bot) in the game.

    Attributes
    ----------
    id: :class:`str`
        Your unique identifier.
    nickname: :class:`str`
        Your nickname.
    color: :class:`int`
        Your color in format `0xAABBGGRR`.
    ping: :class:`int`
        Your ping.
    ticks_to_regenerate: :class:`int` | `None`
        The number of ticks to regenerate your tank.
        If `None`, you are not dead.

    Notes
    -----
    This class is a protocol to provide type hints
    for the agent in the game state.
    """

    @property
    def ticks_to_regenerate(self) -> int | None:
        """The number of ticks to regenerate your tank.

        If `None`, you are not dead.
        """


class PlayerTurret(Protocol):
    """Represents a turret of a player's tank.

    Attributes
    ----------
    direction: :class:`Direction`
        The direction of the turret.

    Notes
    -----
    This class is a protocol to provide type hints for
    the turret of a player's tank.
    """

    @property
    def direction(self) -> Direction:
        """The direction of the turret."""


class AgentTurret(Protocol):
    """Represents a turret of your agent's tank.

    Attributes
    ----------
    direction: :class:`Direction`
        The direction of the turret.
    bullet_count: :class:`int`
        The number of bullets in the turret.
    ticks_to_regenerate_bullet: :class:`int` | `None`
        The number of ticks to regenerate a bullet.
        If `None`, the turret has full bullets.

    Notes
    -----
    This class is a protocol to provide type hints for
    the turret of your agent's tank.
    """

    @property
    def direction(self) -> Direction:
        """The direction of your tank's turret."""

    @property
    def bullet_count(self) -> int:
        """The number of bullets in your tank's turret."""

    @property
    def ticks_to_regenerate_bullet(self) -> int | None:
        """The number of ticks to regenerate a bullet in your tank's turret.

        If `None`, your turret has full bullets.
        """


class PlayerTank(Protocol):
    """Represents a tank of a player.

    Attributes
    ----------
    owner_id: :class:`str`
        The unique identifier of the owner.
    direction: :class:`Direction`
        The direction of the tank.
    turret: :class:`PlayerTurret`
        The turret of the tank.

    Notes
    -----
    This class is a protocol to provide type hints for
    the tank of a player.
    """

    @property
    def owner_id(self) -> str:
        """The unique identifier of the owner."""

    @property
    def direction(self) -> Direction:
        """The direction of the tank."""

    @property
    def turret(self) -> PlayerTurret:
        """The turret of the tank."""


class AgentTank(Protocol):
    """Represents a tank of your agent.

    Attributes
    ----------
    owner_id: :class:`str`
        Your unique identifier.
    direction: :class:`Direction`
        The direction of your tank.
    turret: :class:`AgentTurret`
        The turret of your tank.
    health: :class:`int` | `None`
        The health of your tank.
        If `None`, your tank is dead.

    Notes
    -----
    This class is a protocol to provide type hints for
    the tank of your agent.
    """

    @property
    def owner_id(self) -> str:
        """Your unique identifier."""

    @property
    def direction(self) -> Direction:
        """The direction of your tank."""

    @property
    def turret(self) -> AgentTurret:
        """The turret of your tank."""

    @property
    def health(self) -> int | None:
        """The health of your tank.

        If `None`, your tank is dead.
        """


class Wall(Protocol):
    """Represents a wall in the game.

    Notes
    -----
    This class is a protocol to provide type hints for
    the wall in the game.
    """


class Bullet(Protocol):
    """Represents a bullet in the game.

    Attributes
    ----------
    id: :class:`int`
        The unique identifier of the bullet.
    speed: :class:`float`
        The speed of the bullet.
    direction: :class:`Direction`
        The direction of the bullet.

    Notes
    -----
    This class is a protocol to provide type hints for
    the bullet in the game.
    """

    id: int
    speed: float
    direction: Direction


class LobbyData(Protocol):
    """Represents the lobby data.

    Attributes
    ----------
    my_id: :class:`str`
        Your unique identifier.
    players: Sequence[:class:`LobbyPlayer`]
        The sequence of players in the lobby.
    server_settings: :class:`ServerSettings`
        The server settings.

    Notes
    -----
    This class is a protocol to provide type hints for
    the lobby data.
    """

    @property
    def my_id(self) -> str:
        """Your unique identifier."""

    @property
    def players(self) -> Sequence[LobbyPlayer]:
        """The sequence of players in the lobby."""

    @property
    def server_settings(self) -> ServerSettings:
        """The server settings."""


class Zone(Protocol):
    """Represents a zone in the game.

    The zone can be one of the following:
    - :class:`NeutralZone`
    - :class:`BeingCapturedZone`
    - :class:`CapturedZone`
    - :class:`BeingContestedZone`
    - :class:`BeingRetakenZone`

    To check the current state of a zone,
    refer to its status property.

    You can access additional attributes of a zone
    depending on its type by following this pattern:

    .. code-block:: python
        if zone.status is ZoneStatus.NEUTRAL:
            zone_neutral: NeutralZone = zone
        elif zone.status is ZoneStatus.BEING_CAPTURED:
            zone_captured: BeingCapturedZone = zone
            zone_captured.remaining_ticks
        elif # ...

    Attributes
    ----------
    x: :class:`int`
        The x-coordinate of the zone.
    y: :class:`int`
        The y-coordinate of the zone.
    width: :class:`int`
        The width of the zone.
    height: :class:`int`
        The height of the zone.
    index: :class:`int`
        The index of the zone.
    status: :class:`ZoneStatus`
        The status of the zone.

    Notes
    -----
    This class is a protocol to provide type hints for
    the zone in the game.
    """

    @property
    def x(self) -> int:
        """The x-coordinate of the zone."""

    @property
    def y(self) -> int:
        """The y-coordinate of the zone."""

    @property
    def width(self) -> int:
        """The width of the zone."""

    @property
    def height(self) -> int:
        """The height of the zone."""

    @property
    def index(self) -> int:
        """The index of the zone."""

    @property
    def status(self) -> ZoneStatus:
        """The status of the zone."""


class NeutralZone(Zone, Protocol):
    """Represents a neutral zone in the game.

    Notes
    -----
    This class is a protocol to provide type hints for
    the neutral zone in the game.
    """


class BeingCapturedZone(Zone, Protocol):
    """Represents a zone being captured in the game.

    Attributes
    ----------
    player_id: :class:`str`
        The unique identifier of the player capturing the zone.
    remaining_ticks: :class:`int`
        The remaining ticks to capture the zone.

    Notes
    -----
    This class is a protocol to provide type hints for
    the zone being captured in the game.
    """

    @property
    def player_id(self) -> str:
        """The unique identifier of the player capturing the zone."""

    @property
    def remaining_ticks(self) -> int:
        """The remaining ticks to capture the zone."""


class CapturedZone(Zone, Protocol):
    """Represents a captured zone in the game.

    Attributes
    ----------
    player_id: :class:`str`
        The unique identifier of the player capturing the zone.

    Notes
    -----
    This class is a protocol to provide type hints for
    the captured zone in the game.
    """

    @property
    def player_id(self) -> str:
        """The unique identifier of the player capturing the zone."""


class BeingContestedZone(Zone, Protocol):
    """Represents a zone being contested in the game.

    Attributes
    ----------
    captured_by_id: :class:`str` | `None`
        The unique identifier of the player capturing
        the zone if any. Otherwise, `None`.

    Notes
    -----
    This class is a protocol to provide type hints for
    the zone being contested in the game.
    """

    @property
    def captured_by_id(self) -> str | None:
        """The unique identifier of the player capturing the zone if any.

        Otherwise, `None`.
        """


class BeingRetakenZone(Zone, Protocol):
    """Represents a zone being retaken in the game.

    Attributes
    ----------
    captured_by_id: :class:`str`
        The unique identifier of the player capturing the zone.
    retaken_by_id: :class:`str`
        The unique identifier of the player retaking the zone.
    remaining_ticks: :class:`int`
        The remaining ticks to retake the zone.

    Notes
    -----
    This class is a protocol to provide type hints for
    the zone being retaken in the game.
    """

    @property
    def captured_by_id(self) -> str:
        """The unique identifier of the player capturing the zone."""

    @property
    def retaken_by_id(self) -> str:
        """The unique identifier of the player retaking the zone."""

    @property
    def remaining_ticks(self) -> int:
        """The remaining ticks to retake the zone."""


class Map(Protocol):
    """Represents the map of the game state.

    Attributes
    ----------
    tiles: tuple[tuple[:class:`TileT`]]
        The tiles of the map in a 2D tuple,
        where the first index is the x-coordinate
        and the second index is the y-coordinate.

        Each tile can be one of the following:
        - :class:`Wall`
        - :class:`Bullet`
        - :class:`PlayerTank`
        - :class:`AgentTank`
        - `None`
    zones: Sequence[:class:`Zone`]
        The zones on the map.
    """

    @property
    def tiles(self) -> tuple[tuple[TileT]]:
        """The tiles of the map in a 2D tuple.

        The first index is the x-coordinate
        and the second index is the y-coordinate.

        Each tile can be one of the following:
        - :class:`Wall`
        - :class:`Bullet`
        - :class:`PlayerTank`
        - :class:`AgentTank`
        - `None`
        """

    @property
    def zones(self) -> tuple[Zone]:
        """The zones on the map."""


class GameState(Protocol):
    """Represents the game state.

    Attributes
    ----------
    id: :class:`str`
        The unique identifier of the game state.
    tick: :class:`int`
        The tick of the game state.
    my_agent: :class:`Agent`
        Your agent in the game.
    players: Sequence[:class:`GameStatePlayer`]
        The sequence of players in the game state.
    map: :class:`Map`
        The map of the game state.

    Notes
    -----
    This class is a protocol to provide type hints for
    the game state.
    """

    @property
    def id(self) -> str:
        """The unique identifier of the game state.

        This identifier is required by the server when
        sending the response payload of your action.
        This allows for a shorter waiting time for the next
        broadcast if all agents respond to the latest game state.

        As a **participant of Hackaton**, you can **ignore this**.
        Attaching the identifier to the response payload is done by
        this library automatically.
        """

    @property
    def tick(self) -> int:
        """The tick of the game state."""

    @property
    def my_agent(self) -> Agent:
        """Your agent in the game."""

    @property
    def players(self) -> Sequence[GameStatePlayer]:
        """The sequence of players in the game state."""

    @property
    def map(self) -> Map:
        """The map of the game state."""


class GameResult(Protocol):
    """Represents the game result.

    Attributes
    ----------
    players: Sequence[:class:`GameEndPlayer`]
        The sequence of players in the game result.

    Notes
    -----
    This class is a protocol to provide type hints for
    the game result.
    """

    @property
    def players(self) -> Sequence[GameEndPlayer]:
        """The sequence of players in the game result."""
