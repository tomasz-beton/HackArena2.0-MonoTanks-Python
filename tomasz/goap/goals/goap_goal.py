class GOAPGoal:
    """
    Represents a goal for the GOAP planner.

    Attributes
    ----------
    is_valid: Callable[[], bool]
        A function that returns whether the goal is valid.
    priority: int
        The priority of the goal.
    get_desired_state: Callable[[], dict]
        A function that returns the desired state of the goal.
    """

    def __init__(self, is_valid, priority, get_desired_state):
        self.is_valid = is_valid
        self.priority = priority
        self.get_desired_state = get_desired_state

    def __repr__(self):
        return f"GOAPGoal<is_valid={self.is_valid}, priority={self.priority}>"