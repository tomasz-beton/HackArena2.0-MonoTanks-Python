import logging

from hackathon_bot import AbilityUse, Ability
from tomasz.modes.mode import Mode

log = logging.getLogger(__name__)
log.disabled = True


class FightMode(Mode):
    closest_tank = None

    def get_priority(self, tomasz_map, my_bot):
        self.closest_tank = my_bot.alignment.get_closest_enemy(tomasz_map)

        if self.closest_tank:
            return 1
        else:
            return 0

    def get_action(self, tomasz_map, my_bot):
        if self.closest_tank:
            my_bot.alignment.target = self.closest_tank["pos"]

        return my_bot.movement.get_action(tomasz_map.agent) or AbilityUse(Ability.FIRE_BULLET)
