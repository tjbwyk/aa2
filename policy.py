from bisect import bisect
from logging import warning
from random import random

class Policy:
    """
    The policy describes the probabilities for a player to move in any direction.
    """

    def __init__(self, a, f):
      self.agent = a
      self.field = f
      self.discountfactor = 1.0

    def get_direction(self):
        """
        get a direction to move to
        :return: x and y coordinates of movement
        """
        P = [self.prob_stay, self.prob_north, self.prob_east, self.prob_south, self.prob_west]
        cdf = [P[0]]
        for i in xrange(1, len(P)):
            cdf.append(cdf[-1] + P[i])
        random_ind = bisect(cdf, random())
        return self.directions[random_ind]

    def iterativePolicyEvaluation(self):
      pass
