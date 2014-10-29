from bisect import bisect
from logging import warning
from random import random


class Policy:
    """
    The policy describes the probabilities for a player to move in any direction.
    """

    def __init__(self, prob_stay, prob_north, prob_east, prob_south, prob_west):
        prob_sum = prob_stay + prob_north + prob_east + prob_south + prob_west
        if prob_sum > 1.0:
            warning("Sum of probabilities larger than 1, will be normalized to 1.")
        self.prob_stay = prob_stay / prob_sum
        self.prob_north = prob_north / prob_sum
        self.prob_east = prob_east / prob_sum
        self.prob_south = prob_south / prob_sum
        self.prob_west = prob_west / prob_sum
        self.directions = [(0, 0), (0, -1), (1, 0), (0, 1), (-1, 0)]

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