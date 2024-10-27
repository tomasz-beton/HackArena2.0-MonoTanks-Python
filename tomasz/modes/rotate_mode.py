from hackathon_bot import Rotation, RotationDirection
from tomasz.modes.mode import Mode


class RotateMode(Mode):
    last_tick = 0
    performed_count = 0

    def get_priority(self, tomasz_map, my_bot):
        return max(0.0, 1 - self.performed_count / 5) * 0.1 + 0.01

    def get_action(self, tomasz_map, my_bot):
        if tomasz_map.game_state.tick - self.last_tick < 100:
            self.performed_count += 1
        else:
            self.performed_count = 0
        self.last_tick = tomasz_map.game_state.tick

        return Rotation(RotationDirection.RIGHT, RotationDirection.LEFT)
