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
            return min(
                tomasz_map.agent.entity.turret.bullet_count * 0.5
                + 1 if tomasz_map.agent.entity.secondary_item else 0,
                1
            )
        else:
            return 0

    def get_action(self, tomasz_map, my_bot):
        if self.closest_tank:
            my_bot.alignment.set_target(self.closest_tank["pos"])

        alignment_action = my_bot.alignment.get_action()
        if alignment_action:
            return alignment_action
        
        if tomasz_map.agent.entity.secondary_item:
            weapon_kurwa = tomasz_map.agent.entity.secondary_item + 1
            return AbilityUse(weapon_kurwa)
        elif tomasz_map.agent.entity.turret.bullet_count > 0:
            return AbilityUse(Ability.FIRE_BULLET)
        else:
            return None
