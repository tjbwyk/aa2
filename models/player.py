__author__ = 'fbuettner'
import random


class Player(object):
    """
    superclass for predator and prey
    implements common properties like position
    """

    def __init__(self, location=(0, 0)):
        self.location = location
        self.field = None


    def set_policy(self, policy):
        self.policy = policy

    def act(self, seed=None):
        if (self.policy == None):
            print "No Policy set!"
            raise

        if seed != None:
            random.seed(seed)

        move = random.random()
        nextPositions = self.policy.getNextPositions()
        probability, state = nextPositions.pop()

        while move > probability and len(nextPositions) > 0:
            prob, state = nextPositions.pop()
            probability += prob

        self.location = state
