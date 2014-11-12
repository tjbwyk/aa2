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

    def get_probability(self, state, action):
        for prob, act in self.fixed_actions:
            if action == act:
                return prob

    def get_next_locations(self, location=None):
        if location is None:
            location = self.agent.location
        return [(prob, act, self.field.get_new_coordinates(location, act)) for prob, act in self.fixed_actions]

    def get_next_states(self):
        """
        returns a list of all next possible states and a mapping of all transition probabilities, with the actions of the two agents
        :return: a list of next states
        """
        next_states = []
        trans_prob = []
        # this just adds up to 0.05 ??
        add_up = []

        # TODO multiagent style
        prey = self.field.get_preys()[0]
        # loop over all possible next predator locations
        for this_prob, this_act, this_agent_next_location in self.get_next_locations():
            # loop over all possible next prey locations
            for prob, act, agentLocation in prey.policy.get_next_locations():
                # if this action moves the predator on the current prey location
                if this_agent_next_location == prey.location:
                    #
                    add_up.append((this_prob * prob, this_act, act))
                else:
                    #
                    trans_prob.append((this_prob * prob, this_act, act))

                next_states.append((prey.id, self.field.get_relative_position(this_agent_next_location, agentLocation)))

        if len(add_up) > 0:
            p = 0.0
            for prob, this_act, act in add_up:
                p += prob

            trans_prob.append((p, add_up[0][1], (0, 0)))

        return trans_prob, list(set(next_states))