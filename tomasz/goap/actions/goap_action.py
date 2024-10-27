# is_valid()
# get_cost()
# get_preconditions()
# get_effects()
# perform()
from zone_conqueror import MyBot


class GOAPAction:
    """
    Represents an action for the GOAP planner.

    Attributes
    ----------
    cost: int
        The cost of the action.
    preconditions: dict
        The preconditions of the action.
    effects: dict
        The effects of the action.
    """

    def __init__(self, cost, preconditions, effects):
        self.cost = cost
        self.preconditions = preconditions
        self.effects = effects

    def __repr__(self):
        return f"GOAPAction<cost={self.cost}, preconditions={self.preconditions}, effects={self.effects}>"

    def is_valid(self, state):
        """
        Check if the action is valid in the given state.

        Parameters
        ----------
        state: dict
            The current state.

        Returns
        -------
        bool
            True if the action is valid.
        """
        for key, value in self.preconditions.items():
            if state.get(key) != value:
                return False
        return True

    def get_cost(self):
        """
        Get the cost of the action.

        Returns
        -------
        int
            The cost of the action.
        """
        return self.cost

    def get_preconditions(self):
        """
        Get the preconditions of the action.

        Returns
        -------
        dict
            The preconditions of the action.
        """
        return self.preconditions

    def get_effects(self):
        """
        Get the effects of the action.

        Returns
        -------
        dict
            The effects of the action.
        """
        return self.effects

    def perform(self, actor: MyBot) -> bool:
        """
        Perform the action.

        Parameters
        ----------
        actor: MyBot
            The actor performing the action.

        Returns
        -------
        bool
            True if the action was performed successfully.
        """
        pass