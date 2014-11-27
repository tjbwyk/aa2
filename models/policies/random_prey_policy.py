__author__ = 'sebastian_droeppelmann'

from policy import Policy


class RandomPreyPolicy(Policy, object):
    """
      implementation of the policy of the predator
    """

    def __init__(self, agent, field, seed=None, value_init=None):
        super(RandomPreyPolicy, self).__init__(agent, field, [], seed=seed, value_init=None)

    def get_probability_mapping(self, state):
        """
        returns the probability mapping according to the state: pi(s,a) for all a
        in case of the random policy simply the probabilities of the moves
        if the
        """
        return self.get_probability_mapping_relative(state)
        #return self.get_probability_mapping_complete(state)


    def get_probability_mapping_relative(self, state):
        if state == (0, 0):
            mapping = [(1, (0, 0))]

        else:
            mapping = [(0.8, (0, 0))]
            flex_actions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
            if self.field.get_distance(state) == 1:
                x, y = state
                flex_actions.remove((-1*x, -1*y))
            mapping.extend([(0.2 / len(flex_actions), a) for a in flex_actions])

        return mapping

    def get_probability_mapping_complete(self, state):
        cur_pred_pos, cur_prey_pos = state
        # if the predator is on top of the prey, it can't move anymore

        if cur_pred_pos == cur_prey_pos:
            mapping = [(1, (0, 0))]
        else:
            mapping = [(0.8, (0, 0))]
            flex_actions = [a for a in [(-1, 0), (1, 0), (0, -1), (0, 1)]
                            if self.field.get_new_coordinates(cur_prey_pos, a) != cur_pred_pos]
            mapping.extend([(0.2 / len(flex_actions), a) for a in flex_actions])
        return mapping
