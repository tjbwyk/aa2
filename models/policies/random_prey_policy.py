__author__ = 'sebastian_droeppelmann'

from policy import Policy


class RandomPreyPolicy(Policy, object):
    """
      implementation of the policy of the predator
    """

    def __init__(self, agent, field, seed=None):
        super(RandomPreyPolicy, self).__init__(agent, field, seed=seed)

    def get_probability_mapping(self, state):
        """
        returns the probability mapping according to the state,
        in case of the random policy simply the probabilities of the moves
        """
        cur_pred_pos, cur_prey_pos = state
        mapping = [(0.8, (0,0))]
        flex_actions = [action for action in [(-1,0), (1,0), (0,-1), (0, 1)]
                        if self.field.get_new_coordinates(cur_prey_pos, action) != cur_pred_pos]
        mapping.extend([ (0.2/len(flex_actions), action) for action in flex_actions])
        return mapping
