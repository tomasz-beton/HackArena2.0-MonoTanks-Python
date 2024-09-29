"""Tests for the actions module."""

import pytest
from hackathon_bot import (
    Movement,
    Rotation,
    Shoot,
    MovementDirection,
    RotationDirection,
)

# pylint: disable=invalid-name


@pytest.mark.parametrize(
    "direction", [MovementDirection.FORWARD, MovementDirection.BACKWARD]
)
def test_Movement_to_payload(direction):
    """Test Movement.to_payload method."""

    movement = Movement(direction)
    payload = movement.to_payload("game_state_id")

    assert payload.game_state_id == "game_state_id"
    assert payload.direction == direction


@pytest.mark.parametrize(
    "tank_rotation_direction, turret_rotation_direction",
    [
        (RotationDirection.LEFT, RotationDirection.LEFT),
        (RotationDirection.LEFT, RotationDirection.RIGHT),
        (RotationDirection.LEFT, None),
        (RotationDirection.RIGHT, RotationDirection.LEFT),
        (RotationDirection.RIGHT, RotationDirection.RIGHT),
        (RotationDirection.RIGHT, None),
        (None, RotationDirection.LEFT),
        (None, RotationDirection.RIGHT),
        (None, None),
    ],
)
def test_Rotation_to_payload(tank_rotation_direction, turret_rotation_direction):
    """Test Rotation.to_payload method."""

    rotation = Rotation(tank_rotation_direction, turret_rotation_direction)
    payload = rotation.to_payload("game_state_id")

    assert payload.game_state_id == "game_state_id"
    assert payload.tank_rotation == tank_rotation_direction
    assert payload.turret_rotation == turret_rotation_direction


def test_Shoot_to_payload():
    """Test Shoot.to_payload method."""

    shoot = Shoot()
    payload = shoot.to_payload("game_state_id")

    assert payload.game_state_id == "game_state_id"
