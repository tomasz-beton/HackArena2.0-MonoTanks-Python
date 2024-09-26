from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Generic, TypeVar, TYPE_CHECKING

import humps

from hackaton_bot.enums import Direction, ZoneStatus
from hackaton_bot.payloads import GameEndPayload
from hackaton_bot.protocols import GameResult, GameState, LobbyData

if TYPE_CHECKING:
    from hackaton_bot.payloads import (
        GameStatePayload,
        LobbyDataPayload,
        RawMap,
        RawPlayer,
        RawTank,
        RawTurret,
        RawZone,
        ServerSettings,
    )


@dataclass(slots=True, frozen=True)
class _BasePlayer:
    id: str
    nickname: str
    color: int
    score: int | None = None
    ping: int | None = None
    ticks_to_regenerate: int | None = None

    @classmethod
    def from_raw(cls, raw: RawPlayer) -> _BasePlayer:
        """Creates a player from a raw player payload."""
        data = asdict(raw)
        data["ticks_to_regenerate"] = data.pop("ticks_to_regen", None)
        return cls(**data)


@dataclass(slots=True, frozen=True)
class _BaseTurret:
    direction: Direction
    bullet_count: int | None = None
    ticks_to_regenerate_bullet: int | None = None

    @classmethod
    def from_raw(cls, raw: RawTurret) -> _BaseTurret:
        """Creates a turret from a raw turret payload."""
        data = asdict(raw)
        data["ticks_to_regenerate_bullet"] = data.pop("ticks_to_regen_bullet", None)
        return cls(**data)


@dataclass(slots=True, frozen=True)
class _BaseTank:
    owner_id: str
    direction: Direction
    turret: _BaseTurret
    health: int | None = None

    @classmethod
    def from_raw(cls, raw: RawTank) -> _BaseTank:
        """Creates a tank from a raw tank payload."""
        data = asdict(raw)
        data["turret"] = _BaseTurret.from_raw(raw.turret)
        return cls(**data)


@dataclass(slots=True, frozen=True)
class _BaseWall:
    pass


@dataclass(slots=True, frozen=True)
class _BaseBullet:
    id: int
    speed: float
    direction: Direction

    @classmethod
    def from_raw(cls, raw: dict) -> _BaseBullet:
        """Creates a bullet from a raw bullet payload."""
        return cls(**asdict(raw))


@dataclass(slots=True, frozen=True)
class _Zone:

    x: int
    y: int
    width: int
    height: int
    index: int
    status: ZoneStatus
    player_id: str | None = None
    captured_by_id: str | None = None
    retaken_by_id: str | None = None
    remaining_ticks: int | None = None

    @classmethod
    def from_raw(cls, raw: RawZone) -> _Zone:
        """Creates a zone from a raw zone payload."""
        data = asdict(raw)
        data["status"] = ZoneStatus(humps.decamelize(data["status"]).upper())
        return cls(**data)


@dataclass(slots=True, frozen=True)
class _LobbyData:
    my_id: str
    players: tuple[_BasePlayer]
    server_settings: ServerSettings

    @classmethod
    def from_payload(cls, payload: LobbyDataPayload) -> _LobbyData:
        """Creates a lobby data from a lobby data payload."""
        players = tuple(_BasePlayer.from_raw(p) for p in payload.players)
        return cls(payload.player_id, players, payload.server_settings)


_TileT = TypeVar("_TileT", _BaseTank, _BaseWall, _BaseBullet, None)


@dataclass(slots=True, frozen=True)
class _Tile(Generic[_TileT]):
    obj: _TileT | None
    zone: _Zone | None
    is_visible: bool


@dataclass(slots=True, frozen=True)
class _Map:
    tiles: tuple[tuple[_Tile]]
    zones: tuple[_Zone]
    visibility: tuple[str]

    @classmethod
    def from_raw(cls, raw: RawMap) -> _Map:
        """Creates a map from a raw map payload."""
        zones = tuple(_Zone.from_raw(z) for z in raw.zones)

        tiles = []
        for x, row in enumerate(raw.tiles):
            tab = []
            for y, raw_tile in enumerate(row):
                obj = raw_tile[0] if raw_tile else None
                if obj is None:
                    tile_obj = None
                elif obj.type == "tank":
                    tile_obj = _BaseTank.from_raw(obj.entity)
                elif obj.type == "wall":
                    tile_obj = _BaseWall()
                elif obj.type == "bullet":
                    tile_obj = _BaseBullet.from_raw(obj.entity)
                else:
                    raise ValueError(f"Unknown tile type: {obj.type}")

                is_visible = raw.visibility[x][y] == "1"
                zone = next(
                    (
                        z
                        for z in zones
                        if z.x <= x < z.x + z.width and z.y <= y < z.y + z.height
                    ),
                    None,
                )
                tab.append(_Tile(tile_obj, zone, is_visible))
            tiles.append(tuple(tab))

        return _Map(tuple(tiles), tuple(zones), raw.visibility)


@dataclass(slots=True, frozen=True)
class _GameState:

    id: str
    tick: int
    my_agent: _BasePlayer
    players: tuple[_BasePlayer]
    map: _Map

    @classmethod
    def from_payload(cls, payload: GameStatePayload, agent_id: str) -> _GameState:
        """Creates a game state from a game state payload."""

        players = [_BasePlayer.from_raw(p) for p in payload.players]
        agent = next(p for p in players if p.id == agent_id)

        return cls(
            id=payload.id,
            tick=payload.tick,
            my_agent=agent,
            players=players,
            map=_Map.from_raw(payload.map),
        )


@dataclass(slots=True, frozen=True)
class _GameResult:

    players: tuple[_BasePlayer]

    @classmethod
    def from_payload(cls, payload: GameEndPayload) -> _GameResult:
        """Creates game results from a game end payload."""
        players = tuple(_BasePlayer.from_raw(p) for p in payload.players)
        return cls(players)


class Initializer:
    """Initializes the game models from the raw payloads."""

    @staticmethod
    def get_game_state(payload: GameStatePayload, agent_id: str) -> GameState:
        """Creates a game state from a game state payload."""
        return _GameState.from_payload(payload, agent_id)

    @staticmethod
    def get_lobby_data(payload: LobbyDataPayload) -> LobbyData:
        """Creates a lobby data from a lobby data payload."""
        return _LobbyData.from_payload(payload)

    @staticmethod
    def get_game_result(payload: GameEndPayload) -> GameResult:
        """Creates game result from a game end payload."""
        return _GameResult.from_payload(payload)
