from models.policies.policy import Policy
import random


class ProbabilisticPolicy(Policy):
    """
    The probabilistic policy
    """

    def __init__(self, agent, field, value_init=None):
        super(ProbabilisticPolicy, self).__init__(agent, field, value_init)

    def pick_next_action(self, _state):
        move = random.random()
        # select the action that belongs to random move value
        probability = 0.0
        prob_map = self.get_probability_mapping()
        while move > probability and len(prob_map) > 0:
            prob, action = prob_map.pop()
            probability += prob
        return action

    def get_probability_mapping(self):
        """
        returns the probability mapping for the possible actions of the agent
        :return: a list of possible actions with the probability
        """
        return [(1/len(self.agent.get_actions()), action) for action in self.agent.get_actions()]