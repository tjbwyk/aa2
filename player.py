__author__ = 'fbuettner'
from policy import Policy


class Player(object):
    """
    superclass for predator and prey
    implements common properties like position
    """
    def __init__(self, location):
        self.location = location
        self.field = None
        # set default policy
        self.policy = Policy(1, 0, 0, 0, 0)

    def set_policy(self, policy):
        self.policy = policy 

    def move(self,delta_x, delta_y):
        assert (abs(delta_x) + abs(delta_y) == 1), 'Only non-diagonal steps of 1 are allowed'
        self.location = self.field.get_new_coordinates(self.location, delta_x, delta_y)
