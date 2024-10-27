from hackathon_bot import ResponseAction
from tomasz.BotWithSystems import BotWithSystems
from tomasz.map import TomaszMapWithHistory

class Mode:
    def get_priority(self, tomasz_map: TomaszMapWithHistory, my_bot: BotWithSystems) -> float:
        """
        Returns the priority of the mode. The mode with the highest priority will be chosen.
        Parameters
        ----------
        tomasz_map
            The current map with history
        my_bot
            The bot

        Returns
        -------
        float
            Mode priority ranging from 0 to 1
        """
        pass

    def get_action(self, tomasz_map: TomaszMapWithHistory, my_bot: BotWithSystems) -> ResponseAction | None:
        """
        Returns the action to be performed by the bot.
        Parameters
        ----------
        tomasz_map
        my_bot

        Returns
        -------
        ResponseAction
        """
        pass

    def __repr__(self):
        return self.__class__.__name__