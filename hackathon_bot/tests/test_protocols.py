"""Tests for the protocols module.

Some of the protocols contain weird attributes like __instancecheck_something__.
These are used to distinguish between different classes that have the same
data structure. This is necessary to allow using isinstance() with models.

Without these attributes, isinstance() will return True for all the protocols
that have the same data structure, which is not the desired behavior.

The tests check if the models are instances of the protocols that they should be
instances of. The tests are parametrized to test all the possible
combinations of similar model applications.
"""

import pytest

from hackathon_bot import models
from hackathon_bot.enums import BulletType, Direction, ZoneStatus
from hackathon_bot.models import (
    AgentTankModel,
    WallModel,
    ZoneModel,
    BulletModel,
)
from hackathon_bot.payloads import RawZone
from hackathon_bot.protocols import (
    BeingCapturedZone,
    BeingContestedZone,
    BeingRetakenZone,
    CapturedZone,
    NeutralZone,
    PlayerTank,
)

wall = models.WallModel()
zone = models.ZoneModel(0, 0, 1, 1, 65, ZoneStatus.NEUTRAL)
turret = models.TurretModel(Direction.LEFT)
player_tank = models.TankModel("id", Direction.LEFT, turret)
agent_tank = models.AgentTankModel("id", Direction.LEFT, turret)
bullet = models.BulletModel(1, BulletType.BASIC, 1.0, Direction.LEFT)


@pytest.mark.parametrize(
    "entity, expected",
    [
        (wall, True),
        (bullet, False),
        (player_tank, False),
        (agent_tank, False),
    ],
)
def test_tile_entity_isinstance_wall(entity, expected):
    """Test if entity (Model) is instance of Wall (Protocol)."""
    assert isinstance(entity, WallModel) == expected


@pytest.mark.parametrize(
    "entity, expected",
    [
        (wall, False),
        (bullet, False),
        (player_tank, True),
        (agent_tank, True),
    ],
)
def test_tile_entity_isinstance_tank(entity, expected):
    """Test if entity (Model) is instance of Tank (Protocol)."""
    assert isinstance(entity, PlayerTank) == expected


@pytest.mark.parametrize(
    "entity, expected",
    [
        (wall, False),
        (bullet, False),
        (player_tank, False),
        (agent_tank, True),
    ],
)
def test_tile_entity_isinstance_agent_tank(entity, expected):
    """Test if entity (Model) is instance of AgentTank (Protocol)."""
    assert isinstance(entity, AgentTankModel) == expected


@pytest.mark.parametrize(
    "entity, expected",
    [
        (wall, False),
        (bullet, True),
        (player_tank, False),
        (agent_tank, False),
    ],
)
def test_tile_entity_isinstance_bullet(entity, expected):
    """Test if entity (Model) is instance of Bullet (Protocol)."""
    assert isinstance(entity, BulletModel) == expected


@pytest.mark.parametrize(
    "zone_status, expected",
    [
        ("neutral", True),
        ("being_captured", False),
        ("captured", False),
        ("being_contested", False),
        ("being_retaken", False),
    ],
)
def test_zone_isinstance_neutral(zone_status, expected):
    """Test if zone (Model) is instance of NeutralZone (Protocol)."""
    raw_zone = RawZone(0, 0, 1, 1, 65, zone_status)
    neutral_zone = ZoneModel.from_raw(raw_zone)
    assert isinstance(neutral_zone, NeutralZone) == expected


@pytest.mark.parametrize(
    "zone_status, expected",
    [
        ("neutral", False),
        ("being_captured", True),
        ("captured", False),
        ("being_contested", False),
        ("being_retaken", False),
    ],
)
def test_zone_isinstance_being_captured(zone_status, expected):
    """Test if zone (Model) is instance of BeingCapturedZone (Protocol)."""
    raw_zone = RawZone(0, 0, 1, 1, 65, zone_status)
    being_captured_zone = ZoneModel.from_raw(raw_zone)
    assert isinstance(being_captured_zone, BeingCapturedZone) == expected


@pytest.mark.parametrize(
    "zone_status, expected",
    [
        ("neutral", False),
        ("being_captured", False),
        ("captured", True),
        ("being_contested", False),
        ("being_retaken", False),
    ],
)
def test_zone_isinstance_captured(zone_status, expected):
    """Test if zone (Model) is instance of CapturedZone (Protocol)."""
    raw_zone = RawZone(0, 0, 1, 1, 65, zone_status)
    captured_zone = ZoneModel.from_raw(raw_zone)
    assert isinstance(captured_zone, CapturedZone) == expected


@pytest.mark.parametrize(
    "zone_status, expected",
    [
        ("neutral", False),
        ("being_captured", False),
        ("captured", False),
        ("being_contested", True),
        ("being_retaken", False),
    ],
)
def test_zone_isinstance_being_contested(zone_status, expected):
    """Test if zone (Model) is instance of BeingContestedZone (Protocol)."""
    raw_zone = RawZone(0, 0, 1, 1, 65, zone_status)
    being_contested_zone = ZoneModel.from_raw(raw_zone)
    assert isinstance(being_contested_zone, BeingContestedZone) == expected


@pytest.mark.parametrize(
    "zone_status, expected",
    [
        ("neutral", False),
        ("being_captured", False),
        ("captured", False),
        ("being_contested", False),
        ("being_retaken", True),
    ],
)
def test_zone_isinstance_being_retaken(zone_status, expected):
    """Test if zone (Model) is instance of BeingRetakenZone (Protocol)."""
    raw_zone = RawZone(0, 0, 1, 1, 65, zone_status)
    being_retaken_zone = ZoneModel.from_raw(raw_zone)
    assert isinstance(being_retaken_zone, BeingRetakenZone) == expected
