from typing import List

from hackathon_bot import GameState
from tomasz.goap.actions.capture_zone import CaptureZoneAction
from tomasz.goap.actions.goap_action import GOAPAction
from tomasz.goap.goals.goap_goal import GOAPGoal
from tomasz.map_parser import TomaszMap


class GOAPActionPlanner:
    actions: List[GOAPAction]

    def __init__(self, actions: List[GOAPAction]):
        self.actions = actions

    def get_plan(self, goal: GOAPGoal):
        print("Getting plan for goal:", goal)

        desired_state = goal.get_desired_state()

        if len(desired_state) == 0:
            return []

        return self._find_best_plan(goal, desired_state)

    def _find_best_plan(self, goal: GOAPGoal, desired_state):
        root = {"action": goal, "state": desired_state, "children": []}

        if self._build_plans(root):
            plans = self._transform_tree_into_array(root)
            return self._get_cheapest_plan(plans)

        return []

    def _build_plans(self, step):
        has_followup = False
        state = step["state"].copy()

        if len(state) == 0:
            return True

        for action in self.actions:
            if not action.is_valid(state):
                continue

            should_use_action = False
            effects = action.get_effects()
            desired_state = state.copy()

            for s in desired_state:
                if s in effects:
                    desired_state.remove(s)
                    should_use_action = True

            if should_use_action:
                preconditions = action.get_preconditions()
                for p in preconditions:
                    desired_state.append(p)

                s = {"action": action, "state": desired_state, "children": []}

                if len(desired_state) == 0 or self._build_plans(s):
                    step["children"].append(s)
                    has_followup = True

        return has_followup

    def _transform_tree_into_array(self, root):
        plans = []
        for child in root["children"]:
            if len(child["children"]) == 0:
                plans.append({"actions": [child["action"]], "cost": child["action"].get_cost()})
            else:
                plans += self._transform_tree_into_array(child)

        return plans

    def _get_cheapest_plan(self, plans):
        best_plan = None
        for plan in plans:
            if not best_plan or plan["cost"] < best_plan["cost"]:
                best_plan = plan

        return best_plan["actions"]


def get_action_planner(game_state: GameState, tomasz_map: TomaszMap):
    return GOAPActionPlanner([
        CaptureZoneAction(game_state, tomasz_map)
    ])
