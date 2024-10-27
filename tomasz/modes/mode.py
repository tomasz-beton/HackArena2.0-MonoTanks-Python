from hackathon_bot import ResponseAction
from tomasz.map import TomaszMapWithHistory
from zone_conqueror import MyBot


class Mode:
    def get_priority(self, tomasz_map: TomaszMapWithHistory, my_bot: MyBot) -> float:
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

    def get_action(self, tomasz_map: TomaszMapWithHistory, my_bot: MyBot) -> ResponseAction | None:
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