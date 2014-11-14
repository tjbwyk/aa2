__author__ = 'fbuettner'


class Player(object):
    """
    superclass for predator and prey
    implements common properties like position
    """

    def __init__(self, location=(0, 0), actions=[(0, 0), (-1, 0), (1, 0), (0, -1), (0, 1)],
                 policy=None, field=None, id_number=""):
        self.location = location
        self.actions = actions
        self.field = field
        self.policy = policy
        self.id = self.__str__() + id_number

    def get_actions(self):
        """
        returns the possible actions for the player
        :return: the possible actions
        """
        return self.actions

    def act(self, seed=None):
        """
        update the location according to the action in the policy
        :return: nothing
        """
        if self.policy is None:
            print "No Policy set for Player, ", self.id
            raise
        else:
            action = self.policy.pick_next_action(self.field.get_current_state())
            self.location = self.field.get_new_coordinates(self.location, action)
