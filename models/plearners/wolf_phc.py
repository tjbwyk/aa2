__author__ = 'fbuettner'
import numpy as np
import copy
from collections import defaultdict
from models.plearners.q_plearner import QPlearner
from models.policies.greedy_policy import GreedyPolicy


class Wolf_phc(QPlearner):
    def __init__(self, policy, field, agent, alpha=0.1, gamma=0, delta_l=1, delta_w=0.3):
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

    def init_plearner(self, **kwargs):
        self.state_visit_counts[self.field.state] += 1

    def pick_next_action(self, state):
        return self.policy.pick_next_action(state)

    def update(self, old_state, new_state, actions, rewards):
        # compute Q value for old state-action pair
        self.policy.value[old_state, actions.get(self.agent)] = self.compute_q_value(old_state, new_state, actions.get(self.agent), rewards.get(self.agent))
        # increase visit count for new state
        self.state_visit_counts[new_state] += 1

    def compute_q_value(self, old_state, new_state, action, reward):
        result = (1 - self.alpha) * self.policy.value[old_state, action] + self.alpha * (
            reward + self.gamma * self.max_action_value_for_q(new_state))
        return result

    @classmethod
    def create_greedy_plearner(cls, field, agent, epsilon=0.1, gamma=0.0, learning_rate=0.1,
                               discount_factor=0.7):
        """

        :param field:
        :param agent:
        :param epsilon: exploration probability
        :param gamma: Policy discount factor (set to 0 for greedy policy)
        :param learning_rate: Q-learning rate
        :param discount_factor: Q-learning discount factor
        :return:
        """
        # make sure initial probabilities for all actions are equal
        value_init = 1 / len(agent.actions)
        return Wolf_phc(
            policy=GreedyPolicy(field=field, agent=agent, value_init=value_init, epsilon=epsilon, gamma=gamma,
                                q_value_select=True),
            field=None, agent=agent, alpha=learning_rate, gamma=discount_factor)