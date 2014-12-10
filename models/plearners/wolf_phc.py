__author__ = 'fbuettner'
import numpy as np
import copy
from collections import defaultdict
from models.plearners.q_plearner import QPlearner
from models.policies.mixed_policy import Mixed_policy


class Wolf_phc(QPlearner):
    def __init__(self, policy, field, agent, alpha=0.1, gamma=0, delta_l=0.9, delta_w=0.3):
        """
        Win-or-Learn-Fast Policy Hill Climbing
        :param alpha: learning rate
        :param gamma: discount factor
        :param delta_l: step size for losing
        :param delta_w: step size for winning (must be smaller than dl)
        :return:
        """
        if delta_w >= delta_l:
            raise ValueError("Parameter dw must be smaller than parameter dl")
        super(Wolf_phc, self).__init__(policy, field, agent)
        self.average_policy = copy.deepcopy(self.policy)
        self.state_visit_counts = defaultdict(lambda: 0)
        self.alpha = alpha
        self.gamma = gamma
        self.dl = delta_l
        self.dw = delta_w
        self.q_values = defaultdict(lambda: 0)

    def init_plearner(self, **kwargs):
        self.state_visit_counts[self.field.state] += 1

    def pick_next_action(self, state):
        return self.policy.pick_next_action(state)

    def update(self, old_state, new_state, actions, rewards):
        # compute Q value for old state-action pair
        self.q_values[old_state, actions.get(self.agent)] = self.compute_q_value(old_state, new_state,
                                                                                 actions.get(self.agent),
                                                                                 rewards.get(self.agent))
        # increase visit count for new state
        self.state_visit_counts[old_state] += 1
        # update estimate of average policy for all actions and old_state
        for action in self.agent.actions:
            self.average_policy.value[old_state, action] += (1.0 / self.state_visit_counts[old_state]) * (
                self.policy.value[old_state, action] - self.average_policy.value[old_state, action])
        # update policy(s, a) and constrain it to legal probability distribution
        if actions.get(self.agent) == self.max_action_value_for_q(old_state, return_arg=True):
            update_delta = self.choose_delta(old_state)
        else:
            update_delta = -(self.choose_delta(old_state) / (len(self.agent.actions) - 1))
        self.policy.value[old_state, actions.get(self.agent)] += update_delta

    def compute_q_value(self, old_state, new_state, action, reward):
        result = (1 - self.alpha) * self.q_values[old_state, action] + self.alpha * (
            reward + self.gamma * self.max_action_value_for_q(new_state))
        return result

    def max_action_value_for_q(self, state, return_arg=False):
        """
        search all action values for a given state and return the maximum value or maximizing action
        :param state: the given state
        :param return_arg: if true, return maximizing action. Else return maximum value
        :return: value or action
        """
        max = -np.inf
        argmax = None
        for action in self.agent.get_actions():
            tmp = self.q_values[state, action]
            if tmp > max:
                max = tmp
                argmax = action
        if return_arg:
            return argmax
        else:
            return max

    def choose_delta(self, state):
        policy_sum = sum(
            [self.policy.value[state, action] * self.q_values[state, action] for action in self.agent.actions])
        average_policy_sum = sum(
            [self.average_policy.value[state, action] * self.q_values[state, action] for action in self.agent.actions])
        if policy_sum > average_policy_sum:
            return self.dw
        else:
            return self.dl


    @classmethod
    def create_greedy_plearner(cls, field, agent, epsilon=0.1, learning_rate=0.1,
                               discount_factor=0.7):
        """

        :param field:
        :param agent:
        :param epsilon: exploration probability
        :param learning_rate: Q-learning rate
        :param discount_factor: Q-learning discount factor
        :return:
        """
        return Wolf_phc(
            policy=Mixed_policy(field=field, agent=agent, epsilon=epsilon),
            field=None, agent=agent, alpha=learning_rate, gamma=discount_factor)