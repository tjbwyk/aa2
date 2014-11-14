from models.policies.policy import Policy


class PredatorPolicy(Policy, object):
    """
      implementation of the policy of the predator
    """

    def __init__(self, agent, field, seed=None):
        super(PredatorPolicy, self).__init__(agent, field, seed=seed)

    def get_probability_mapping(self, state):
        """
        returns the probability mapping according to the state: pi(s,a) for all a
        in case of the random policy simply the probabilities of the moves
        [(0.2, (0,0)), (0.2, (-1,0)), (0.2, (1,0)), (0.2, (0,-1)), (0.2, (0, 1))]
        since all moves are equally probable, simply return 0.2
        """
        return [(0.2, (0,0)), (0.2, (-1,0)), (0.2, (1,0)), (0.2, (0,-1)), (0.2, (0, 1))]


    def get_probability(self, state, next_state, action):
        """
        returns the probability of the state being next_state when undertaking action action: p(s'|s,a)
        :param state: the start state
        :param next_state: the resulting state
        :param action: the action taken in the start state
        :return: the probability of state leading to next_state given the action
        """

        cur_pred_loc, cur_prey_loc = state
        next_pred_loc, next_prey_loc = next_state

        next_prey_locations = self.field.get_prey().get_next_locations(state)
        #if action results in next state for predator, and the prey moves legally,
        #calculate chances otherwise the move is illegal
        if self.field.get_new_coordinates(cur_pred_loc, action) == next_pred_loc and next_prey_loc in next_prey_locations:
            #if the predator stands next to the prey and moves to it it has no chance to escape
            if next_pred_loc == cur_prey_loc:
                if cur_prey_loc == next_prey_loc:
                    return 1
                else:
                    return 0
            # TODO remove magic numbers?
            #chance of the prey standing still
            elif next_prey_loc == cur_prey_loc:
                return 0.8
            #if the prey is next to the predator but the predator moves not to the location of the
            #prey it just has 3 places to go, cause it can't move to the location of the predator
            elif self.field.get_distance(state) == 1:
                return 0.2/3
            #normal move in one direction
            else:
                return 0.2/4
        #if the next state can't be reached from this state
        else:
            return 0
