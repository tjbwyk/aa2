from random import randint

class Player(object):
    """
    superclass for predator and prey
    implements common properties like position
    """

    def __init__(self, location=(0, 0), actions=[(0, 0), (-1, 0), (1, 0), (0, -1), (0, 1)],
                 policy=None, id="", tripping_prob = 0.0):
        self.location = location
        self.actions = actions
        self.policy = policy
        self.tripping_prob = tripping_prob
        self.id = str(id) if id != "" else str(randint(30, 99))

    def __hash__(self):
        return hash((self.id, self.location))

    def __eq__(self, other):
        return (self.id, self.location) == (other.name, other.location)

    def get_actions(self):
        """
        returns the possible actions for the player
        :return: the possible actions
        """
        return list(self.actions)

    def act(self, state):
        """
        update the location according to the action in the policy
        :return: nothing
        """
        if self.policy is None:
            print "No Policy set for Player, ", self
            raise
        else:
            action = self.policy.pick_next_action(state)
            return action

    def update(self, old_state, new_state, action, reward):
        """
        This function gets the new state and a reward from the field after picking an action.
        Then it uses these values to update the player's policy.
        :param old_state:
        :param new_state:
        :param action:
        :param reward:
        :return:
        """
        self.policy.update(old_state, new_state, action, reward)
