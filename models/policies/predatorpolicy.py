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

    def get_action_probability(self, state, action):
        """
        get the probability for an action to be taken in a current state.
        :param state: the current state (location)
        :param action: the desired action
        :return: the probability of this action according to this policy
        """
        # TODO argument "state" unused?
        for prob, act in self.fixed_actions:
            if action == act:
                return prob

    def get_next_locations(self, location):
        """
        get all possible next locations to go to from location
        :param location: current location.
        :return: list of all possible locations according to the actions
        """
        # return the resulting locations for all possible actions of this predator
        return [self.field.get_new_coordinates(location, act) for act in self.get_actions()]

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


    def get_next_states(self, state):
        """
        returns a list of all next possible states and a mapping of all transition probabilities, with the actions of the two agents
        :param state:
        :return: a list of next states
        """

        # list of possible next states
        next_states = []
        # transition probabilities to the next states
        trans_prob = []
        # TODO this just adds up to 0.05 ??
        add_up = []

        pred_loc, prey_loc = state

        # TODO multiagent style
        prey = self.field.get_preys()[0]
        # loop over all possible next predator locations
        for predator_action_prob, predator_action, predator_next_location in self.get_next_locations(pred_loc):
            # loop over all possible next prey locations
            for prey_action_prob, prey_action, prey_next_location in prey.policy.get_next_locations(prey_loc):
                # if this action moves the predator on the current prey location
                if predator_next_location == prey.location:
                    # probabilities of all possible prey movements from here
                    add_up.append((predator_action_prob * prey_action_prob, predator_action, prey_action))
                else:
                    # add the probability of this next state to the list
                    trans_prob.append((predator_action_prob * prey_action_prob, predator_action, prey_action))
                # append this next state to the list of possible next states
                next_states.append((predator_next_location, prey_next_location))
        # TODO what is this?
        if len(add_up) > 0:
            p = 0.0
            for prey_action_prob, predator_action, prey_action in add_up:
                p += prey_action_prob
            trans_prob.append((p, add_up[0][1], (0, 0)))
        # datatype set automatically removes duplicate states
        return trans_prob, list(set(next_states))

    def get_next_state_probabilities(self, action):
        """
        calculate the probability to enter state s' from state s, taking action a: p(s'|s,a)
        :param action:
        :return:
        """
