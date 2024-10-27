import math

from tomasz.map import TomaszMapWithHistory


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


def is_walkable(tomasz_map: TomaszMapWithHistory, tile_coordinates, danger_threshold=0.2):
    """
    Check if the neighbor is walkable.

    Parameters
    ----------
    tomasz_map: TomaszMapWithHistory
        Parsed map.
    tile_coordinates: (int, int)
        The tile to check.
    danger_threshold: float
        The danger threshold.

    Returns
    -------
    bool
        True if the neighbor is walkable.
    """
    x, y = tile_coordinates
    if x < 0 or y < 0:
        return False
    if x >= tomasz_map.size[0] or y >= tomasz_map.size[1]:
        return False
    if tomasz_map.walls_arr[x, y] == 1 or tomasz_map.danger[x, y] > danger_threshold:
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


def a_star(tomasz_map: TomaszMapWithHistory, start: (int, int), goal: (int, int), heuristic=euclidean_distance):
    """
    A* algorithm to find the shortest path between two points on the map.

    Parameters
    ----------
    tomasz_map: TomaszMapWithHistory
        Parsed map. Containing the occupancy grid (walls_arr). Rows[Columns]
    start: (int, int)
        The starting point, (x, y).
    goal: (int, int)
        The goal point, (x, y).
    heuristic: Callable[[int, int], float]
        The heuristic function to estimate the cost to reach the goal.

    Returns
    -------
    List
        Array of points to reach the goal.
    """
    movements = _get_movements_4n()

    # The set of nodes already evaluated.
    closed_set = set()

    # The set of currently discovered nodes that are not evaluated yet.
    # Initially, only the start node is known.
    open_set = {start}

    # For each node, which node it can most efficiently be reached from.
    # If a node can be reached from many nodes, came_from will eventually contain the
    # most efficient previous step.
    came_from = {}

    # For each node, the cost of getting from the start node to that node.
    g_score = {start: 0.0}

    # The cost of going from start to start is zero.
    # For each node, the total cost of getting from the start node to the goal
    # by passing by that node. That value is partly known, partly heuristic.
    f_score = {start: heuristic(start, goal)}

    while open_set:
        # Get the node in open_set having the lowest f_score[] value
        current = min(open_set, key=lambda x: f_score[x])

        if current == goal:
            return _reconstruct_path(came_from, current)

        open_set.remove(current)
        closed_set.add(current)

        for dx, dy, _ in movements:
            neighbor = current[0] + dx, current[1] + dy

            if not is_walkable(tomasz_map, neighbor):
                continue

            # The distance from start to a neighbor
            tentative_g_score = g_score[current] + 1

            if neighbor in closed_set and tentative_g_score >= g_score.get(neighbor, 0):
                continue

            if neighbor not in open_set or tentative_g_score < g_score.get(neighbor, 0):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = g_score[neighbor] + heuristic(neighbor, goal)
                open_set.add(neighbor)

    return []
