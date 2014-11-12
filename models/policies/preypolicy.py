from models.policies.policy import Policy
from models.predator import Predator


class PreyPolicy(Policy, object):
    """
    implementation of the policy of the prey
    """

    def __init__(self, agent, field, seed=None):
        super(PreyPolicy, self).__init__(agent, field,
                                         fixed_actions=[(0.8, (0, 0))],
                                         flex_actions=[(0, -1), (-1, 0), (0, 1), (1, 0)], seed=seed)

    def get_actions(self):
        return [(0,0),(0,1),(0,-1),(1,0),(-1,0)]

    def get_probability(self, state, next_state, action):
        cur_pred_loc, cur_prey_loc = state
        next_pred_loc, next_prey_loc = next_state

        next_prey_locations  = [ self.field.get_new_coordinates(cur_prey_loc,a) for a in self.get_actions()]
        #if action results in next state for predator, and the prey moves legally,
        #calculate chances otherwise the move is illegal
        if self.field.get_new_coordinates(cur_pred_loc, action) == next_pred_loc and next_prey_loc in next_prey_locations:
            #if the predator stands next to the prey and moves to it it has no chance to escape
            if next_pred_loc == cur_prey_loc:
                if cur_prey_loc == next_prey_loc:
                    return 1
                else:
                    return 0
            #chance of the prey standing still
            elif next_prey_loc == cur_prey_loc:
                return 0.8
            #if the prey is next to the predator but the predator moves not to the location of the
            #prey it just has 3 places to go, cause it can't move to the location of the
            elif self.field.get_distance(state) == 1:
                return 0.2/3
            #normal move in one direction
            else:
                return 0.2/4
        #if the next state can't be reached from this state
        else:
            return 0

    def get_next_locations(self, state):
        """
        updates the prey policy
        :param location:
        :return: all probabilities and according next states
        """
        cur_pred_loc, cur_prey_loc = state
        next_prey_locations  = [ self.field.get_new_coordinates(cur_prey_loc, a) for a in self.get_actions()]
        #the prey can't move to the predator
        if cur_pred_loc in next_prey_locations:
            next_prey_locations.remove(cur_pred_loc)
        return next_prey_locations
