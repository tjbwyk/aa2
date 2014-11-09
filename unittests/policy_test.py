import unittest
from collections import Counter

from models.policies.policy import Policy
from models.field import Field
from models.predator import Predator
from models.policies.predatorpolicy import PredatorPolicy
from models.policies.preypolicy import PreyPolicy
from models.prey import Prey

class testPolicy(unittest.TestCase):

    # def testPredatorPolicy(self):
    #     field = Field(3, 3)
    #     predator = Predator((1, 1))
    #     policy = PredatorPolicy()
    #
    #     field.add_player(predator)
    #     field.print_field()
    #
    # def testPreyPolicy1(self):
    #     field = Field(3, 3)
    #     predator = Predator((1, 1))
    #     policy = PredatorPolicy()
    #
    #     field.add_player(predator)
    #     field.print_field()

    def testGetStates(self):
        field = Field(3, 3)
        predator = Predator((1, 0))
        predator.add_policy(PredatorPolicy(agent=predator, field=field))
        field.add_player(predator)
        prey = Prey((0, 0))
        prey.add_policy(PreyPolicy(agent=prey, field=field))
        field.add_player(prey)

        print predator.policy.get_next_states()

if __name__ == '__main__':
    unittest.main()
