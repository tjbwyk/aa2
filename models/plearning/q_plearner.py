import numpy as np
from models.plearning.plearner import Plearner
from models.policies.greedy_policy import GreedyPolicy
from models.policies.softmax_policy import SoftmaxPolicy


class QPlearner(Plearner):

    def __init__(self, policy, agent, learning_rate, discount_factor):
        super(QPlearner, self).__init__(policy)
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.agent = agent

    @classmethod
    def create_greedy_plearner(cls, field, agent, value_init=15, epsilon=0.1, gamma=0.0, learning_rate=0.1, discount_factor=0.7, q_value_select=True):
        """
        generator method to easily create a greedy learner
        :param field:
        :param agent:
        :param value_init:
        :param tau:
        :param learning_rate:
        :param discount_factor:
        :return:
        """
        return QPlearner(policy=GreedyPolicy(field=field, agent=agent,
                                      value_init=value_init, epsilon=epsilon,
                                      gamma=gamma, q_value_select=q_value_select),
                         agent=agent, learning_rate=learning_rate, discount_factor=discount_factor)

    @classmethod
    def create_softmax_plearner(cls, field, agent, value_init=15, tau=0.1, learning_rate=0.1, discount_factor=0.7):
        """
        generator method to easily create a softmax learner
        :param field:
        :param agent:
        :param value_init:
        :param tau:
        :param learning_rate:
        :param discount_factor:
        :return:
        """
        return QPlearner(policy=SoftmaxPolicy(field=field, agent=agent,
                                      value_init=value_init, tau=tau),
                         agent=agent, learning_rate=learning_rate, discount_factor=discount_factor)

    def update(self, old_state, new_state, action, reward):
        self.policy.value[old_state, action] = self.compute_q_value(old_state, new_state, action, reward)

    def compute_q_value(self, old_state, new_state, action, reward):
        result = self.policy.value[old_state, action] + \
                 self.learning_rate * (
                     reward +
                     self.discount_factor * self.max_action_value_for_q(new_state) -
                     self.policy.value[old_state, action]
                 )
        return result

    def max_action_value_for_q(self, state):
        max = -np.inf
        for action in self.agent.get_actions():
            tmp = self.policy.value[state, action]
            if tmp > max:
                max = tmp
        return max
