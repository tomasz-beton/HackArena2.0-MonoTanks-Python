import logging

from hackathon_bot import AbilityUse, Ability
from .mode import Mode

log = logging.getLogger(__name__)
log.disabled = True


class FightMode(Mode):
    closest_tank = None

    def get_priority(self, tomasz_map, my_bot):
        self.closest_tank = my_bot.alignment.get_closest_enemy()

        if self.closest_tank:
            return 1
        else:
            return 0

    def get_action(self, tomasz_map, my_bot):
        if self.closest_tank:
            my_bot.alignment.set_target(self.closest_tank["pos"])

        return my_bot.alignment.get_action() or AbilityUse(Ability.FIRE_BULLET)
