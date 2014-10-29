__author__ = 'fbuettner'
from policy import Policy


class Player:
    """
    superclass for predator and prey
    implements common properties like position
    """
    def __init__(self, x, y, field):
        self.x = x
        self.y = y
        self.field = field
        # set default policy
        self.policy = Policy(1, 0, 0, 0, 0)

    def set_policy(self, policy):
        self.policy = policy

    def move(self,delta_x, delta_y):
        assert (abs(delta_x) + abs(delta_y) == 1), 'Only non-diagonal steps of 1 are allowed'
        self.x, self.y = self.field.get_new_coordinates(self.x, self.y, delta_x, delta_y)
