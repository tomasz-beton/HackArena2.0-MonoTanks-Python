"""This module contains the response actions that the bot can take.

The response actions are used to define the bot's next move in the game.

Classes
-------
ResponseAction
    Base class for response actions.
Movement
    Represents a movement response action.
Rotation
    Represents a rotation response action.
Shoot
    Represents a shoot response action.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import ClassVar, final

from .enums import (
    MovementDirection,
    PacketType,
    RotationDirection,
)
from .payloads import (
    ResponseActionPayload,
    TankMovementPayload,
    TankRotationPayload,
    TankShootPayload,
)


__all__ = (
    "ResponseAction",
    "Movement",
    "Rotation",
    "Shoot",
)


@dataclass(slots=True, frozen=True)
class ResponseAction(ABC):
    """Base class for response actions."""

    packet_type: PacketType = field(init=False)

    @abstractmethod
    def to_payload(self, game_state_id: str) -> ResponseActionPayload:
        """Converts the response action to a payload."""


@dataclass(slots=True, frozen=True)
class Movement(ResponseAction):
    """Represents a movement response action.

    Example
    -------

    .. code-block:: python
        from hackaton_bot import Movement, MovementDirection
        movement = Movement(MovementDirection.FORWARD)
    """

    movement_direction: MovementDirection
    packet_type: ClassVar[PacketType] = PacketType.TANK_MOVEMENT

    @final
    def to_payload(self, game_state_id: str) -> TankMovementPayload:
        return TankMovementPayload(game_state_id, self.movement_direction)


@dataclass(slots=True, frozen=True)
class Rotation(ResponseAction):
    """Represents a rotation response action.

    Example
    -------

    .. code-block:: python
        from hackaton_bot import Rotation, RotationDirection
        rotation = Rotation(RotationDirection.LEFT, RotationDirection.RIGHT)
    """

    tank_rotation_direction: RotationDirection | None
    turret_rotation_direction: RotationDirection | None
    packet_type: ClassVar[PacketType] = PacketType.TANK_ROTATION

    @final
    def to_payload(self, game_state_id: str) -> TankRotationPayload:
        return TankRotationPayload(
            game_state_id,
            self.tank_rotation_direction,
            self.turret_rotation_direction,
        )


@dataclass(slots=True, frozen=True)
class Shoot(ResponseAction):
    """Represents a shoot response action.

    Example
    -------

    .. code-block:: python
        from hackaton_bot import Shoot
        shoot = Shoot()
    """

    packet_type: ClassVar[PacketType] = PacketType.TANK_SHOOT

    @final
    def to_payload(self, game_state_id: str) -> TankShootPayload:
        return TankShootPayload(game_state_id)
