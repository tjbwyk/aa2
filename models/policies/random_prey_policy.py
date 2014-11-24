__author__ = 'sebastian_droeppelmann'

from policy import Policy


class RandomPreyPolicy(Policy, object):
    """
      implementation of the policy of the predator
    """

    def __init__(self, agent, field, seed=None):
        super(RandomPreyPolicy, self).__init__(agent, field, seed=seed)