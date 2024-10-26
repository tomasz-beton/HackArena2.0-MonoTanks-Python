from hackathon_bot import Movement, Rotation, MovementDirection, Direction, RotationDirection
from tomasz.map_parser import TomaszAgent
from typing import Tuple


def get_move_delta(current, next):
    """
    Get the move delta between two points.

    Parameters
    ----------
    current: (int, int)
        The current point.
    next: (int, int)
        The next point.

    Returns
    -------
    (int, int)
        The move delta.
    """
    return next[0] - current[0], next[1] - current[1]


def _is_facing_right_direction(move_delta, current_direction):
    """
    Check if the agent is facing the right direction.

    Parameters
    ----------
    move_delta: (int, int)
        The move delta.
    current_direction: int
        The current direction.

    Returns
    -------
    bool
        True if the agent is facing the right direction.
    """
    return move_delta == (0, -1) and current_direction == Direction.UP or move_delta == (
    1, 0) and current_direction == Direction.RIGHT or move_delta == (
    0, 1) and current_direction == Direction.DOWN or move_delta == (-1, 0) and current_direction == Direction.LEFT


def _is_facing_opposite_direction(move_delta, current_direction):
    """
    Check if the agent is facing the opposite direction.

    Parameters
    ----------
    move_delta: (int, int)
        The move delta.
    current_direction: int
        The current direction.

    Returns
    -------
    bool
        True if the agent is facing the opposite direction.
    """
    return move_delta == (0, -1) and current_direction == Direction.DOWN or move_delta == (
    1, 0) and current_direction == Direction.LEFT or move_delta == (
    0, 1) and current_direction == Direction.UP or move_delta == (-1, 0) and current_direction == Direction.RIGHT


def _get_needed_rotation(move_delta, current_direction) -> RotationDirection:
    """
    The tank can rotate by 90 degrees to the left or right. We want to rotate the tank so that it faces the right direction.
    Parameters
    ----------
    move_delta
    current_direction

    Returns
    -------
    RotationDirection
    """

    if move_delta == (1, 0):
        if current_direction == Direction.UP:
            return RotationDirection.RIGHT
        if current_direction == Direction.DOWN:
            return RotationDirection.LEFT
        if current_direction == Direction.LEFT:
            return RotationDirection.RIGHT

    elif move_delta == (-1, 0):
        if current_direction == Direction.UP:
            return RotationDirection.LEFT
        if current_direction == Direction.DOWN:
            return RotationDirection.RIGHT
        if current_direction == Direction.RIGHT:
            return RotationDirection.RIGHT

    elif move_delta == (0, -1):
        if current_direction == Direction.RIGHT:
            return RotationDirection.LEFT
        if current_direction == Direction.LEFT:
            return RotationDirection.RIGHT
        if current_direction == Direction.DOWN:
            return RotationDirection.RIGHT

    elif move_delta == (0, 1):
        if current_direction == Direction.RIGHT:
            return RotationDirection.RIGHT
        if current_direction == Direction.LEFT:
            return RotationDirection.LEFT
        if current_direction == Direction.UP:
            return RotationDirection.RIGHT


def get_movement_action(agent: TomaszAgent, next_pos: Tuple[int, int], allow_backwards=False) -> Movement | Rotation:
    """
    Get the movement action to move the agent to the next position.

    Parameters
    ----------
    allow_backwards: bool
        Whether to allow moving backwards
    agent: TomaszAgent
        The agent.
    next_pos: (int, int)
        The next position.

    Returns
    -------
    Movement | Rotation
        The movement action.
    """
    move_delta = get_move_delta(agent.position, next_pos)

    if _is_facing_right_direction(move_delta, agent.entity.direction):
        return Movement(MovementDirection.FORWARD)

    if _is_facing_opposite_direction(move_delta, agent.entity.direction) and allow_backwards:
        return Movement(MovementDirection.BACKWARD)

    return Rotation(_get_needed_rotation(move_delta, agent.entity.direction), None)
