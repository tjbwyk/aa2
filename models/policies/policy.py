import random


class Policy:
    """
    The policy describes the probabilities for a player to move in any direction.
    """

    def __init__(self, agent, field, fixed_actions=[], flex_actions=[], seed=None):
        self.agent = agent
        self.field = field
        self.fixed_actions = fixed_actions
        self.flex_actions = flex_actions

        if seed is not None:
            random.seed(seed)

    def get_next_states(self):
        """
        returns a list of all next possible states and a mapping of all transition probabilities, with the actions of the two agents
        :return: a list of next states
        """
        next_states = []
        trans_prob = []

        add_up = []

        prey = self.field.get_preys()[0]

        for this_prob, this_act, thisAgentLocation in self.get_next_locations():
            for prob, act, agentLocation in prey.policy.get_next_locations():
                # state.append(prob_this * prob)

                if thisAgentLocation == prey.location:
                    add_up.append((this_prob * prob, this_act, act))
                else:
                    trans_prob.append((this_prob * prob, this_act, act))

                next_states.append((prey.id, self.field.get_relative_position(thisAgentLocation, agentLocation)))

        if len(add_up) > 0:
            p = 0.0
            for prob, this_act, act in add_up:
                p += prob

            trans_prob.append((p, add_up[0][1], (0, 0)))

        return trans_prob, list(set(next_states))

    def pick_next_action(self, style="probabilistic"):
        """
        selects an action according to a state
        :param state:
        :param actions:
        :param style:
        :return:
        """
        if style == "probabilistic":
            move = random.random()
            probability = 0.0
            prob_map, states = self.get_next_states()
            while move > probability and len(prob_map) > 0:
                prob, action, preyaction = prob_map.pop()
                probability += prob
            return action, preyaction
        else:
            raise

    def get_next_locations_no_prob(self):
        return [loc for p, loc in self.get_next_locations()]

    def get_next_locations(self, location=None):
        pass

    def get_probability(self, state, action):
        pass

    def get_probability_mapping(self, state, actions):
        pass