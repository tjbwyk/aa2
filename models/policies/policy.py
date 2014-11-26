import random
import collections
import numpy as np


class Policy:
    """
    The policy describes the probabilities for a player to move in any direction.
    """
    def __init__(self, agent, field, seed=None, value_init=None):

        # initialize random number generator
        if seed is not None:
            random.seed(seed)

        self.agent = agent
        self.field = field
        self.reset_planning(value_init)

        self.value = {state: 0.0 for state in self.field.get_all_states_with_terminal()}
        self.argmax_action = {state: (0,0) for state in self.field.get_all_states()}

        # Initialize Q(s,a) optimistically with a value of value_init
        self.q_value = collections.defaultdict(lambda: value_init)



    def reset_planning(self, value_init=None):
        self.value = {state: 0.0 for state in self.field.get_all_states_with_terminal()}
        self.argmax_action = {state: (0,0) for state in self.field.get_all_states()}

        # Initialize Q(s,a) optimistically with a value of value_init
        self.q_value = collections.defaultdict(lambda: value_init)

    def pick_next_action(self, state, **kwargs):
        """
        selects an action according to the action probability distribution of the policy
        :param state:
        :param actions:
        :param style:
            - probabilistic: select a random action with equal probability
            - greedy: select thee action that yields the highest immediate reward
            - egreedy: select greedy with probability 1-epsilon, and random with prob. epsilon
              (requires additional parameter epsilon)
            - max_value: select the action that yields the highest value (immediate reward + gamma*value_of_next_state)
              requires additional parameter gamma.
            - softmax: varies the action probabilities as a graded function of estimated value. The greedy action is
              still given the highest selection probability, but all the others are ranked and weighted according to
              their value estimates. See section 2.3 in Sutton&Barto. Requires additional parameter tau.
        :return:
        """
        if "style" in kwargs:
            style = kwargs.get("style")
        else:
            style = "probabilistic"

        if style == "probabilistic":
            move = random.random()
            # select the action that belongs to random move value
            probability = 0.0
            prob_map = self.get_probability_mapping(state)
            while move > probability and len(prob_map) > 0:
                prob, action = prob_map.pop()
                probability += prob
            return action

        elif style == "greedy":
            val = 0
            selected_states = []
            for next_state in self.field.get_next_states(state):
                if val < self.value[next_state]:
                    selected_states = [next_state]
                    val = self.value[next_state]
                elif val == self.value[next_state]:
                    selected_states.append(next_state)
            if len(selected_states) == 1:
                next_state = selected_states[0]
            elif len(selected_states) > 1:
                next_state = random.choice(selected_states)
            else:
                raise ValueError("no state found")
            pred_pos, prey_pos = state
            next_pred_pos, next_prey_pos = next_state
            action = self.field.get_relative_position(pred_pos, next_pred_pos)
            if action not in self.agent.get_actions():
                raise ValueError("action not in legal actions of agent from State: ", state, ", NextState: ",
                                 next_state, ", action: ", action)
            return action

        elif style == "q-greedy":
            max_qval = -1
            max_action = (0, 0)
            for next_action in self.agent.get_actions():
                if max_qval < self.q_value[state, next_action]:
                    max_action = next_action
                    max_qval = self.q_value[state, next_action]
            return max_action

        elif style == "q-egreedy":
            if "epsilon" in kwargs:
                epsilon = kwargs.get("epsilon")
            else:
                raise ValueError("style egreedy requires parameter epsilon.")
            if random.random() <= epsilon:
                return self.pick_next_action(state, style="probabilistic")
            else:
                return self.pick_next_action(state, style="q-greedy")

        elif style == "max_value":
            if "gamma" in kwargs:
                gamma = kwargs.get("gamma")
            else:
                raise ValueError("style max_value requires parameter epsilon.")
            action_value = 0
            for action in self.agent.get_actions():
                tmp_v = 0
                for next_state in self.field.get_next_states(state, action):
                    tmp_prob = self.get_probability(state, next_state, action)
                    tmp_rew = self.field.get_reward(next_state) + gamma * self.value[next_state]
                    tmp_v += tmp_prob * tmp_rew
                if tmp_v > action_value:
                    best_action = action
                    action_value = tmp_v
            return best_action

        elif style == "softmax":
            if "tau" in kwargs:
                tau = kwargs.get("tau")
            else:
                raise ValueError("style max_value requires parameter tau (aka temperature).")
            sum_of_action_values = sum([np.exp(self.qvalue[state, next_action]/tau)
                                        for next_action in self.agent.get_actions()])
            action_probabilities = [(np.exp(self.qvalue[state, next_action]/tau)/sum_of_action_values, next_action)
                                    for next_action in self.agent.get_actions()]
            # probabilistic style for these probabilities
            move = random.random()
            probability = 0.0
            while move > probability and len(action_probabilities) > 0:
                prob, action = action_probabilities.pop()
                probability += prob
            return action
        else:
            # given style not recognized
            raise ValueError("invalid value given for parameter style: " + str(style))
