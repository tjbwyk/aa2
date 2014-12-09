from models.policies.probabilistic_policy import ProbabilisticPolicy
from models.plearning.plearner import Plearner
__author__ = 'xtroce'


class ProbabilisticPlearner(Plearner):
    def __init__(self, policy):
        super(ProbabilisticPlearner, self).__init__(policy)

    @classmethod
    def create_plearner(cls, field, agent):
        return ProbabilisticPlearner(ProbabilisticPolicy(field=field, agent=agent))

    def update(self, old_state, new_state, action, reward):
        #do nothing here since the policy does not change at all
        pass

