from models.policies.policy import Policy
import random


class ProbabilisticPolicy(Policy):
    """
    The probabilistic policy
    """

    def __init__(self, agent, field, value_init=None):
        super(Policy, self).__init__(agent, field, value_init)

    def pick_next_action(self, state):
            # move = random.random()
            # # select the action that belongs to random move value
            # probability = 0.0
            # prob_map = self.get_probability_mapping(state)
            # while move > probability and len(prob_map) > 0:
            #     prob, action = prob_map.pop()
            #     probability += prob
            # if 'action' not in locals():
            #     print state
            # return action
        pass