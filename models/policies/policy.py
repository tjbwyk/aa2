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
        returns a list of all next possible states
        :return: a list of next states
        """
        next_states = []

        #TODO multiagent style
        for thisAgentLocation in self.agent.get_next_locations():
            prey = self.field.get_preys()[0]
            for agentLocation in prey.get_next_locations():
                #if not thisAgentLocation == prey.location:
                #state.append(prob_this * prob)
                print thisAgentLocation, agentLocation
                next_states.append((prey.id, self.field.get_relative_position(thisAgentLocation, agentLocation)))

        return list(next_states)

    def pick_next_action(self, state, actions, style="probabilistic"):
        """
        selects a action according to a state
        :param state:
        :param actions:
        :param style:
        :return:
        """
        if style == "probabilistic":
            move = random.random()
            probability = 0.0
            prob_map = self.get_probability_mapping(state, actions)
            while move > probability and len(actions) > 0:
                prob, action = prob_map.pop()
                probability += prob
            return action
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