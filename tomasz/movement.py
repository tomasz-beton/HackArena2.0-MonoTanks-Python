import logging
import random
from typing import Tuple

from hackathon_bot import Movement, Rotation, MovementDirection, Direction, RotationDirection
from tomasz.a_star import a_star
from tomasz.map import TomaszAgent, TomaszMap, TomaszMapWithHistory

log = logging.getLogger(__name__)
log.disabled = False


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
    log.info(f"move_delta: {move_delta}, current_direction: {current_direction}")
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
    log.info(f"move_delta: {move_delta}, current_direction: {current_direction}")
    return move_delta == (0, -1) and current_direction == Direction.DOWN or move_delta == (
        1, 0) and current_direction == Direction.LEFT or move_delta == (
        0, 1) and current_direction == Direction.UP or move_delta == (-1, 0) and current_direction == Direction.RIGHT

def parse_dir_to_delta(dir):
    if dir == Direction.UP:
        return (0, -1)
    if dir == Direction.DOWN:
        return (0, 1)
    if dir == Direction.LEFT:
        return (-1, 0)
    if dir == Direction.RIGHT:
        return (1, 0)
    return None


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


def get_random_movement() -> Movement | Rotation:
    """
    Get a random movement action.

    Returns
    -------
    Movement | Rotation
        The movement action.
    """

    if random.randint(0, 100) % 2 == 0:
        return Movement(random.choice(list(MovementDirection)))
    return Rotation(random.choice(list(RotationDirection)), None)

def get_movement_action(agent: TomaszAgent, next_pos: Tuple[int, int], allow_backwards=False, allow_random=True) -> Movement | Rotation | None:
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

    if abs(move_delta[0]) > 1 or abs(move_delta[1]) > 1:
        log.error(f"Invalid move delta: {move_delta}")
        return None

    if _is_facing_right_direction(move_delta, agent.entity.direction):
        return Movement(MovementDirection.FORWARD)

    if _is_facing_opposite_direction(move_delta, agent.entity.direction) and allow_backwards:
        return Movement(MovementDirection.BACKWARD)


    rotation = Rotation(_get_needed_rotation(move_delta, agent.entity.direction), RotationDirection.LEFT)
    if rotation.tank_rotation_direction is None:
        log.warning("Empty rotation! Making random movement\n"*10)
        return None

    return rotation


class MovementSystem:
    path: list = []
    target: (int, int) = None
    tomasz_map: TomaszMapWithHistory = None
    target_reached: bool = False
    path_finding_failed: bool = False
    fails_counter: int = 0
    _next_position: (int, int) = None

    def __init__(self, tomasz_map: TomaszMapWithHistory):
        self.tomasz_map = tomasz_map
        log.info("Movement system initialized")

    def get_action(self, tomasz_agent: TomaszAgent) -> Movement | Rotation | None:
        log.info("My position: " + str(tomasz_agent.position))
        if not self.target:
            log.info("nic nie robie opiedalam sie")
            return None

        if not self.path:
            log.info(f"Looking for path from {tomasz_agent.position} to {self.target}")
            allow_danger = self.fails_counter > 3
            if allow_danger:
                log.warning("Allowing dangerous path")
            self.path = a_star(self.tomasz_map, tomasz_agent.position, self.target, allow_danger)
            if not self.path:
                log.info("Failed to find path :(")
                self.path_finding_failed = True
                self.fails_counter += 1
                self.target_reached = False
                self.target = None
                return None
            else:
                self.path_finding_failed = False
                self.fails_counter = 0
                self.target_reached = False
                log.info("I have a path now! " + str(self.path))

        if self.path:
            if self.target == tomasz_agent.position:
                log.info("Target reached :D")
                self.target_reached = True
                self.target = None
                self.path = []
                return None

            if tomasz_agent.position == self._next_position:
                log.info("I reached the next position!")
                self._next_position = None

            if not self._next_position:
                log.info("Setting next position")
                self._next_position = self.path.pop(0)

            movement_action = get_movement_action(tomasz_agent, self._next_position)
            if not movement_action:
                log.warning("Performing random movement and updating map!!\n" * 10)
                movement_action = get_random_movement()
                self.update_map(self.tomasz_map)
            log.info(f"Moving from {tomasz_agent.position} to {self._next_position} with {movement_action}")
            return movement_action

    def update_map(self, tomasz_map: TomaszMapWithHistory):
        self.tomasz_map = tomasz_map
        self._next_position = None
        self.target_reached = False
        if self.target:
            self.path = a_star(self.tomasz_map, self.tomasz_map.agent.position, self.target)
