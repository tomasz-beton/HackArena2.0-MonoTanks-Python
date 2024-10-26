import math

from tomasz.map_parser import TomaszMap


def euclidean_distance(point1: (int, int), point2: (int, int)):
    """
    Get the Euclidean distance between two points
    Parameters
    ----------
    point1: (int, int)
    point2: (int, int)

    Returns
    -------
    float

    """
    x1, y1 = point1
    x2, y2 = point2

    dist2 = (x1 - x2) ** 2 + (y1 - y2) ** 2

    return math.sqrt(dist2)


def _get_movements_4n():
    """
    Get all possible 4-connectivity movements.

    Returns
    -------
    list
        List of movements as (delta_x, delta_y, cost)
    """
    return [(1, 0, 1.0), (0, 1, 1.0), (-1, 0, 1.0), (0, -1, 1.0)]


def _is_walkable(map, neighbor):
    """
    Check if the neighbor is walkable.

    Parameters
    ----------
    map: TomaszMap
        Parsed map.
    neighbor: (int, int)
        The neighbor to check.

    Returns
    -------
    bool
        True if the neighbor is walkable.
    """
    x, y = neighbor
    if x < 0 or y < 0:
        return False
    if x >= map.size[0] or y >= map.size[1]:
        return False
    if map.walls_arr[x, y] == 1:
        return False
    return True


def _reconstruct_path(came_from, current):
    """
    Reconstruct the path from the came_from dictionary.

    Parameters
    ----------
    came_from: dict
        The dictionary containing the path.
    current: (int, int)
        The current point.

    Returns
    -------
    list
        The path from the start to the current point.
    """
    total_path = [current]
    while current in came_from:
        current = came_from[current]
        total_path.append(current)
        return total_path[:-1][::-1]


def a_star(map: TomaszMap, start: (int, int), goal: (int, int), heuristic=euclidean_distance):
    """
    A* algorithm to find the shortest path between two points on the map.

    Parameters
    ----------
    map: TomaszMap
        Parsed map.
    start: (int, int)
        The starting point, (x, y).
    goal: (int, int)
        The goal point, (x, y).
    heuristic: Callable[[int, int], float]
        The heuristic function to estimate the cost to reach the goal.

    Returns
    -------
    list
        List of points to reach the goal.
    """
    movements = _get_movements_4n()

    # The set of nodes already evaluated
    closed_set = set()

    # The set of currently discovered nodes that are not evaluated yet.
    # Initially, only the start node is known.
    open_set = {start}

    # For each node, which node it can most efficiently be reached from.
    # If a node can be reached from many nodes, came_from will eventually contain the most efficient previous step.
    came_from = {}

    # For each node, the cost of getting from the start node to that node.
    g_score = {start: 0}

    # For each node, the total cost of getting from the start node to the goal
    # by passing by that node. That value is partly known, partly heuristic.
    f_score = {start: g_score[start] + heuristic(start, goal)}

    while open_set:
        # Get the node in open_set having the lowest f_score[] value
        current = min(open_set, key=lambda x: f_score[x])

        if current == goal:
            return _reconstruct_path(came_from, current)

        open_set.remove(current)
        closed_set.add(current)

        for dx, dy, cost in movements:
            neighbor = (current[0] + dx, current[1] + dy)

            # Ignore the neighbor which is not walkable
            if not _is_walkable(map, neighbor):
                continue

            # Ignore the neighbor which is already evaluated
            if neighbor in closed_set:
                continue

            # The distance from start to a neighbor
            tentative_g_score = g_score[current] + cost

            if neighbor not in open_set:
                open_set.add(neighbor)
            elif tentative_g_score >= g_score[neighbor]:
                continue

            # This path is the best until now. Record it!
            came_from[neighbor] = current
            g_score[neighbor] = tentative_g_score
            f_score[neighbor] = g_score[neighbor] + heuristic(neighbor, goal)

    raise ValueError("Failed to find path")
