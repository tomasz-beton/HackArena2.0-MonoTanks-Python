"""This module contains the enums used in the library.

Enums
-----
Direction
    Represents a direction.
MovementDirection
    Represents a movement direction.
RotationDirection
    Represents a rotation direction.
ZoneStatus
    Represents the status of a zone.
PacketType
    Represents the type of a packet.
"""

from enum import Enum, IntEnum


class Direction(IntEnum):
    """Represents a direction.

    Attributes
    ----------
    UP: :class:`int`
        Represents the up direction.
    RIGHT: :class:`int`
        Represents the right direction.
    DOWN: :class:`int`
        Represents the down direction.
    LEFT: :class:`int`
        Represents the left direction.
    """

    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3


class MovementDirection(IntEnum):
    """Represents a movement direction.

    Attributes
    ----------
    FORWARD: :class:`int`
        Represents the forward direction.
    BACKWARD: :class:`int`
        Represents the backward direction.
    """

    FORWARD = 0
    BACKWARD = 1


class RotationDirection(IntEnum):
    """Represents a rotation direction.

    Attributes
    ----------
    LEFT: :class:`int`
        Represents the left rotation
        direction (counter-clockwise).
    RIGHT: :class:`int`
        Represents the right rotation
        direction (clockwise)."""

    LEFT = 0
    RIGHT = 1


class ZoneStatus(str, Enum):
    """Represents the status of a zone.

    Attributes
    ----------
    NEUTRAL: :class:`str`
        Represents a neutral zone.
    BEING_CAPTURED: :class:`str`
        Represents a zone that is being captured.
    CAPTURED: :class:`str`
        Represents a captured zone.
    BEING_CONTESTED: :class:`str`
        Represents a zone that is being contested.
    BEING_RETAKEN: :class:`str`
        Represents a zone that is being retaken.
    """

    NEUTRAL = "NEUTRAL"
    BEING_CAPTURED = "BEING_CAPTURED"
    CAPTURED = "CAPTURED"
    BEING_CONTESTED = "BEING_CONTESTED"
    BEING_RETAKEN = "BEING_RETAKEN"


class PacketType(IntEnum):
    """Represents the type of a packet.

    Each packet type is represented by a 8-bit integer.

    Attributes
    ----------
    UNKNOWN: :class:`int`
        Represents an unknown packet type.
    HAS_PAYLOAD: :class:`int`
        Represents a flag that indicates that the packet has a payload.
    COMMUNICATION_GROUP: :class:`int`
        Represents a 4-bit group for communication packets.
    PING: :class:`int`
        Represents a ping packet.
    PONG: :class:`int`
        Represents a pong packet.
    CONNECTION_ACCEPTED: :class:`int`
        Represents a connection accepted packet.
    CONNECTION_REJECTED: :class:`int`
        Represents a connection rejected packet.
    LOBBY_GROUP: :class:`int`
        Represents a 4-bit group for lobby packets.
    LOBBY_DATA: :class:`int`
        Represents a lobby data packet.
    LOBBY_DELETED: :class:`int`
        Represents a lobby deleted packet.
    GAME_STATE_GROUP: :class:`int`
        Represents a 4-bit group for game state packets.
    GAME_START: :class:`int`
        Represents a game start packet.
    GAME_STATE: :class:`int`
        Represents a game state packet.
    GAME_END: :class:`int`
        Represents a game end packet.
    PLAYER_RESPONSE_ACTION_GROUP: :class:`int`
        Represents a 4-bit group for player response action packets.
    TANK_MOVEMENT: :class:`int`
        Represents a tank movement packet.
    TANK_ROTATION: :class:`int`
        Represents a tank rotation packet.
    TANK_SHOOT: :class:`int`
        Represents a tank shoot packet.
    RESPONSE_PASS: :class:`int`
        Represents a response pass packet.
    WARNING_GROUP: :class:`int`
        Represents a 4-bit group for warning packets.
    CUSTOM_WARNING: :class:`int`
        Represents a custom warning packet.
    PLAYER_ALREADY_MADE_ACTION_WARNING: :class:`int`
        Represents a player already made action warning packet.
    SLOW_RESPONSE_WARNING: :class:`int`
        Represents a slow response warning packet.
    ERROR_GROUP: :class:`int`
        Represents a 4-bit group for error packets.

    Notes
    -----
    The packet types are represented as follows
    (starting from the most significant bit):

    - The first 4 bits represent the group.
    - The 5th bit represents the payload flag.
    - The last 3 bits represent the type.
    """

    UNKNOWN = 0x0

    HAS_PAYLOAD = 0x8

    COMMUNICATION_GROUP = 0x10
    PING = COMMUNICATION_GROUP | 0x1
    PONG = COMMUNICATION_GROUP | 0x2
    CONNECTION_ACCEPTED = COMMUNICATION_GROUP | 0x3
    CONNECTION_REJECTED = COMMUNICATION_GROUP | HAS_PAYLOAD | 0x4

    LOBBY_GROUP = 0x20
    LOBBY_DATA = LOBBY_GROUP | HAS_PAYLOAD | 0x1
    LOBBY_DELETED = LOBBY_GROUP | 0x2

    GAME_STATE_GROUP = 0x30
    GAME_START = GAME_STATE_GROUP | 0x1
    GAME_STATE = GAME_STATE_GROUP | HAS_PAYLOAD | 0x2
    GAME_END = GAME_STATE_GROUP | HAS_PAYLOAD | 0x3

    PLAYER_RESPONSE_ACTION_GROUP = 0x40
    TANK_MOVEMENT = PLAYER_RESPONSE_ACTION_GROUP | HAS_PAYLOAD | 0x1
    TANK_ROTATION = PLAYER_RESPONSE_ACTION_GROUP | HAS_PAYLOAD | 0x2
    TANK_SHOOT = PLAYER_RESPONSE_ACTION_GROUP | HAS_PAYLOAD | 0x3
    RESPONSE_PASS = PLAYER_RESPONSE_ACTION_GROUP | HAS_PAYLOAD | 0x7

    WARNING_GROUP = 0xE0
    CUSTOM_WARNING = WARNING_GROUP | HAS_PAYLOAD | 0x1
    PLAYER_ALREADY_MADE_ACTION_WARNING = WARNING_GROUP | 0x2
    ACTION_IGNORED_DUE_TO_DEAD_WARNING = WARNING_GROUP | 0x3
    SLOW_RESPONSE_WARNING = WARNING_GROUP | 0x4

    ERROR_GROUP = 0xF0


class WarningType(IntEnum):
    """Represents the type of a warning.

    Attributes
    ----------
    CUSTOM: :class:`int`
        Represents a custom warning.
    PLAYER_ALREADY_MADE_ACTION: :class:`int`
        Represents a player already made action warning.
    ACTION_IGNORED_DUE_TO_DEAD: :class:`int`
        Represents an action ignored due to dead warning.
    SLOW_RESPONSE: :class:`int`
        Represents a slow response warning.
    """

    CUSTOM = PacketType.CUSTOM_WARNING
    PLAYER_ALREADY_MADE_ACTION = PacketType.PLAYER_ALREADY_MADE_ACTION_WARNING
    ACTION_IGNORED_DUE_TO_DEAD = PacketType.ACTION_IGNORED_DUE_TO_DEAD_WARNING
    SLOW_RESPONSE = PacketType.SLOW_RESPONSE_WARNING
