import random
import collections
import numpy as np


class Policy:
    """
    The policy describes the probabilities for a player to move in any direction.
    """

    def __init__(self, agent, field, value_init=None):
        self.agent = agent
        self.field = field
        self.reset_planning(value_init)

    def reset_planning(self, value_init=None):
        self.value = {state: 0.0 for state in self.field.get_all_states_with_terminal()}

        # Initialize Q(s,a) optimistically with a value of value_init
        self.q_value = collections.defaultdict(lambda: value_init)

        for action in self.agent.get_actions():
            self.q_value[(0, 0), action] = 0


    def pick_next_action(self, state):
        """
        selects an action according to the action probability distribution of the policy
        :param state:
        :param actions:
        :param style:
            - probabilistic: select a random action with equal probability. This is the default.
            - greedy: select thee action that yields the highest immediate reward. Optional parameter epsilon makes an
              epsilon-greedy selection (random non-greedy action with probability epsilon)
            - q-greedy: like greedy, but based on Q-Values (state-action values) instead of state-values. Optional
              parameter epsilon.
            - max_value: select the action that yields the highest value (immediate reward + gamma*value_of_next_state)
              requires additional parameter gamma.
            - softmax: varies the action probabilities as a graded function of estimated value. The greedy action is
              still given the highest selection probability, but all the others are ranked and weighted according to
              their value estimates. See section 2.3 in Sutton&Barto. Requires additional parameter tau.
        :return: action tuple according to policy
        """
        pass