__author__ = 'sebastian_droeppelmann'

from policy import Policy


class RandomPredatorPolicy(Policy, object):
    """
      implementation of the policy of the predator
    """

    def __init__(self, agent, field, seed=None):
        super(RandomPredatorPolicy, self).__init__(agent, field, seed=seed)

    def get_probability_mapping(self, state):
        """
        returns the probability mapping according to the state,
        in case of the random policy simply the probabilities of the moves
        """
        return [(0.8, (0,0)), (0.05, (-1,0)), (0.05, (1,0)), (0.05, (0,-1)), (0.05, (0, 1))]
