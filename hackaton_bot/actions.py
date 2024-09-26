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
from dataclasses import dataclass
from typing import ClassVar, final

from hackaton_bot.enums import MovementDirection, PacketType
from hackaton_bot.payloads import (
    ResponseActionPayload,
    TankMovementPayload,
    TankRotationPayload,
    TankShootPayload,
)


@dataclass(slots=True, frozen=True)
class ResponseAction(ABC):
    """Base class for response actions."""

    packet_type: PacketType

    @abstractmethod
    def to_payload(self, game_state_id: str) -> ResponseActionPayload:
        """Converts the response action to a payload."""


@dataclass(slots=True, frozen=True)
class Movement(ResponseAction):
    """Represents a movement response action."""

    packet_type: ClassVar[PacketType] = PacketType.TANK_MOVEMENT
    movement_direction: MovementDirection

    @final
    def to_payload(self, game_state_id: str) -> TankMovementPayload:
        return TankMovementPayload(game_state_id, self.movement_direction)


@dataclass(slots=True, frozen=True)
class Rotation(ResponseAction):
    """Represents a rotation response action."""

    packet_type: ClassVar[PacketType] = PacketType.TANK_ROTATION
    tank_rotation_direction: MovementDirection | None
    turret_rotation_direction: MovementDirection | None

    @final
    def to_payload(self, game_state_id: str) -> TankRotationPayload:
        return TankRotationPayload(
            game_state_id,
            self.tank_rotation_direction,
            self.turret_rotation_direction,
        )


@dataclass(slots=True, frozen=True)
class Shoot(ResponseAction):
    """Represents a shoot response action."""

    packet_type: ClassVar[PacketType] = PacketType.TANK_SHOOT

    @final
    def to_payload(self, game_state_id: str) -> TankShootPayload:
        return TankShootPayload(game_state_id)
