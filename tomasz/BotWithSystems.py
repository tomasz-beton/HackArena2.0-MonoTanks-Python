from abc import ABC

from hackathon_bot import HackathonBot
from tomasz.alignment import AlignmentSystem
from tomasz.movement import MovementSystem


class BotWithSystems(HackathonBot, ABC):
    movement: MovementSystem | None
    alignment: AlignmentSystem | None