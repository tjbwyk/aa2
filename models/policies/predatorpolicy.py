from models.policies.policy import Policy
from models.prey import Prey
import itertools


class PredatorPolicy(Policy, object):
    """
      implementaion of the policy of the predator
    """

    def __init__(self, agent, field, seed=None):
        super(PredatorPolicy, self).__init__(agent, field,
                                             fixed_actions=[(0.8, (0, 0)), (0.05, (0, -1)), (0.05, (-1, 0)),
                                                            (0.05, (0, 1)), (0.05, (1, 0))],
                                             flex_actions=[], seed=seed)

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

        next_prey_locations  = self.field.get_preys()[0].get_next_locations(cur_prey_loc)
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

    def get_next_states(self, state):
        cur_pred_pos, cur_prey_pos = state
        next_pred_positions =  self.get_next_locations(cur_pred_pos)
        next_prey_positions =  self.field.get_preys()[0].get_next_locations(cur_prey_pos)
        #initialize all next possible states except when the predator moves t the prey
        next_states = [(next_pred_pos, next_prey_pos)
                       for next_pred_pos in next_pred_positions
                       for next_prey_pos in next_prey_positions
                       if cur_prey_pos != next_pred_pos]

        #if predator moves to the prey, the prey always stays where it is
        if cur_prey_pos in next_pred_positions:
            next_states.append((cur_prey_pos), (cur_prey_pos))