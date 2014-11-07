from bisect import bisect
from random import random


class Policy:
    """
    The policy describes the probabilities for a player to move in any direction.
    """

    def __init__(self, a, f):
      self.agent = a
      self.field = f

    def getNextStates(self):
        pass

    def getNextPositions(self):
        pass
    def getNextPositionsNoProb(self):
        return [loc for p,loc in self.getNextPositions()]
    def prob_of_action(self,state,action):



    def iterativePolicyEvaluation(self):
      pass
