from models.policies.policy import Policy


class GreedyPolicy(Policy):
    """
    The greedy policy
    """

    def __init__(self, agent, field, value_init=None, epsilon=.0, gamma=.0):
        super(Policy, self).__init__(agent, field, value_init)
        self.epsilon = epsilon
        self.gamma = gamma

    def pick_next_action(self, state):
            # if random.random() <= self.epsilon:
            #     return self.pick_next_action(state, style="probabilistic")
            # else:
            #     val = 0
            #     selected_states = []
            #     for next_state, action in self.field.get_next_states_relative(state, with_actions=True):
            #         if val < self.value[next_state]:
            #             selected_states = [(next_state, action)]
            #             val = self.value[next_state]
            #         elif val == self.value[next_state]:
            #             selected_states.append((next_state, action))
            #     if len(selected_states) == 1:
            #         next_state, action = selected_states[0]
            #     elif len(selected_states) > 1:
            #         next_state, action = random.choice(selected_states)
            #     else:
            #         raise ValueError("no state found")
            #     if action not in self.agent.get_actions():
            #         raise ValueError("action not in legal actions of agent from State: ", state, ", NextState: ",
            #                          next_state, ", action: ", action)
            # return action
            #             if "epsilon" in kwargs:
            #     epsilon = kwargs.get("epsilon")
            # else:
            #     epsilon = 0
            # if random.random() <= epsilon:
            #     return self.pick_next_action(state, style="probabilistic")
            # else:
            #     max_qval = -1
            #     max_action = (0, 0)
            #     for next_action in self.agent.get_actions():
            #         if max_qval < self.q_value[state, next_action]:
            #             max_action = next_action
            #             max_qval = self.q_value[state, next_action]
            #     return max_action
            # if "gamma" in kwargs:
            #     gamma = kwargs.get("gamma")
            # else:
            #     raise ValueError("style max_value requires parameter epsilon.")
            # action_value = 0
            # for action in self.agent.get_actions():
            #     tmp_v = 0
            #     for next_state in self.field.get_next_states(state, action):
            #         tmp_prob = self.get_probability(state, next_state, action)
            #         tmp_rew = self.field.get_reward(next_state) + gamma * self.value[next_state]
            #         tmp_v += tmp_prob * tmp_rew
            #     if tmp_v > action_value:
            #         best_action = action
            #         action_value = tmp_v
            # return best_action

        pass