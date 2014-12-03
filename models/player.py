class Player(object):
    """
    superclass for predator and prey
    implements common properties like position
    """

    def __init__(self, location=(0, 0), actions=[(0, 0), (-1, 0), (1, 0), (0, -1), (0, 1)],
                 policy=None, id="", tripping_prob = .0):
        self.location = location
        self.actions = actions
        self.policy = policy
        self.tripping_prob = tripping_prob
        self.id = id

    def get_actions(self):
        """
        returns the possible actions for the player
        :return: the possible actions
        """
        return list(self.actions)

    def act(self,state):
        """
        update the location according to the action in the policy
        :return: nothing
        """
        if self.policy is None:
            print "No Policy set for Player, ", self.id
            raise
        else:
            action = self.policy.pick_next_action(state)
            return action
