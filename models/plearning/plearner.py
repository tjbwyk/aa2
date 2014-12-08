__author__ = 'Fritjof'


class Plearner(object):
    def __init__(self, policy):
        self.policy = policy

    def update(self, old_state, new_state, action, reward):
        pass

    def pick_next_action(self, state):
        self.policy.pick_next_action(state)