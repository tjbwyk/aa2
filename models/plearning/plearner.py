__author__ = 'Fritjof'


class Plearner:
    def __init__(self, policy):
        self.policy = policy

    def update(self, old_state, new_state, action, reward):
        pass