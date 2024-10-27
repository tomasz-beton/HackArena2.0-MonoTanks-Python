from typing import List

from hackathon_bot import GameState
from tomasz.goap.actions.goap_action import GOAPAction
from tomasz.goap.goals.goap_goal import GOAPGoal
from tomasz.goap.goap_action_planner import get_action_planner
from tomasz.map import TomaszMap
from zone_conqueror import MyBot


class GOAPAgent:
    _goals: List[GOAPGoal]
    _current_goal: GOAPGoal | None
    _current_plan: List[GOAPAction]
    _current_plan_step: int
    _actor: MyBot

    def __init__(self, actor: MyBot, goals: List[GOAPGoal]):
        self._actor = actor
        self._goals = goals

    def _best_goal(self):
        best_goal = None

        for goal in self._goals:
            if goal.is_valid() and (not best_goal or goal.priority > best_goal.priority):
                best_goal = goal

        return best_goal

    def _follow_plan(self):
        if not self._current_plan:
            return

        is_step_done = self._current_plan[self._current_plan_step].perform(self._actor)
        if is_step_done:
            self._current_plan_step += 1

            if self._current_plan_step >= len(self._current_plan):
                self._current_plan = []
                self._current_plan_step = 0

    def update_goals(self, goals: List[GOAPGoal]):
        self._goals = goals

    def process(self, game_state: GameState, tomasz_map: TomaszMap):
        goal = self._best_goal()

        if not self._current_goal or goal != self._current_goal:
            self._current_goal = goal
            self._current_plan = get_action_planner(game_state, tomasz_map).get_plan(goal)
            self._current_plan_step = 0
        else:
            self._follow_plan()