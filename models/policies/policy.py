import random


class Policy:
    """
    The policy describes the probabilities for a player to move in any direction.
    """
    def __init__(self, agent, field, seed=None):
        self.agent = agent
        self.field = field

        #initialize random number generator
        if seed is not None:
            random.seed(seed)

    def pick_next_action(self, state, style="probabilistic"):
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
            prob_map = self.get_probability_mapping(state)
            while move > probability and len(prob_map) > 0:
                prob, action = prob_map.pop()
                probability += prob
            return action
        else:
            # given style not recognized
            raise ValueError("invalid value given for parameter style: " + str(style))