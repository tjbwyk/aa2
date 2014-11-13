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
        #initialize random number generator
        if seed is not None:
            random.seed(seed)

    def pick_next_action(self, style="probabilistic"):
        """
        selects an action according to the action probability distribution of the policy
        :param state:
        :param actions:
        :param style:
        :return:
        """
        if style == "probabilistic":
            move = random.random()
            # select the action that belongs to random move value
            probability = 0.0
            prob_map, states = self.get_next_states()
            while move > probability and len(prob_map) > 0:
                prob, action, preyaction = prob_map.pop()
                probability += prob
            return action, preyaction
        else:
            # given style not recognized
            raise ValueError("invalid value given for parameter style: " + str(style))