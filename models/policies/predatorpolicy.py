from models.policies.policy import Policy
from models.prey import Prey
import itertools

class PredatorPolicy(Policy, object):
    """
      implementaion of the policy of the predator
    """

    def __init__(self, agent, field, seed=None):
        super(PredatorPolicy, self).__init__(agent, field,
                                             fixed_actions=[(0.8, (0, 0)), (0.05, (0, -1)), (0.05, (-1, 0)),
                                                            (0.05, (0, 1)), (0.05, (1, 0))],
                                             flex_actions=[], seed=seed)

    def get_probability(self, state, action):
        for prob, act in self.fixed_actions:
            if action == act:
                return prob

    def get_next_locations(self, location=None):
        if location is None:
            location = self.agent.location
        return [(prob, act, self.field.get_new_coordinates(location, act)) for prob, act in self.fixed_actions]
